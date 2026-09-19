#!/usr/bin/env python3
"""Fail-closed live browser prove for the Power Claude product page.

Opens https://neural-llm.com/power-claude (or PC_PRODUCT_URL) via chrome/chromium
--dump-dom (real browser DOM, NOT urllib). Asserts visible Power Claude branding
and install CTA text.

No chrome/chromium → BLOCKED_ENVIRONMENT (ok=false, behavior_proven=false), never
fake N/A PASS. Hurc tips #500-502: missing browser is blocked, not greenwash.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
RECEIPT_DIR = HERE / ".receipts"
RECEIPT_PATH = RECEIPT_DIR / "browser-product-prove-receipt.json"
SCHEMA = "hurc-complete-e2e-power-claude-browser-product/v1"
DEFAULT_URL = "https://neural-llm.com/power-claude"

CHROME_CANDIDATES = (
    "google-chrome-stable",
    "google-chrome",
    "chromium",
    "chromium-browser",
    "chrome-headless-shell",
    "chromium-headless-shell",
)


def _find_chrome(explicit: str | None) -> str | None:
    if explicit:
        p = Path(explicit)
        return str(p) if p.is_file() and os.access(p, os.X_OK) else None
    env = (os.environ.get("PC_CHROME_PATH") or "").strip()
    if env:
        p = Path(env)
        if p.is_file() and os.access(p, os.X_OK):
            return str(p)
    for name in CHROME_CANDIDATES:
        found = shutil.which(name)
        if found:
            return found
    return None


def _blocked_receipt(*, detail: str, chrome: str | None = None, url: str = DEFAULT_URL) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "ok": False,
        "environment_status": "BLOCKED_ENVIRONMENT",
        "blocked_environment": True,
        "behavior_proven": False,
        "prover": "scripts/complete-e2e/browser_product_prove.py",
        "chrome": chrome,
        "url": url,
        "behavior": {
            "status": "blocked",
            "cases": [
                {
                    "id": "browser_product_page",
                    "ok": False,
                    "detail": detail,
                }
            ],
        },
    }


def _fail_receipt(*, detail: str, chrome: str | None, url: str, blocked: bool = False) -> dict[str, Any]:
    if blocked:
        return _blocked_receipt(detail=detail, chrome=chrome, url=url)
    return {
        "schema": SCHEMA,
        "ok": False,
        "environment_status": "prove_failed",
        "blocked_environment": False,
        "behavior_proven": False,
        "prover": "scripts/complete-e2e/browser_product_prove.py",
        "chrome": chrome,
        "url": url,
        "behavior": {
            "status": "fail",
            "cases": [
                {
                    "id": "browser_product_page",
                    "ok": False,
                    "detail": detail,
                }
            ],
        },
    }


def _ok_receipt(*, detail: str, chrome: str, url: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "ok": True,
        "environment_status": "live",
        "blocked_environment": False,
        "behavior_proven": True,
        "prover": "scripts/complete-e2e/browser_product_prove.py",
        "chrome": chrome,
        "url": url,
        "behavior": {
            "status": "ok",
            "cases": [
                {
                    "id": "browser_product_page",
                    "ok": True,
                    "detail": detail,
                }
            ],
        },
    }


def _dump_dom(chrome: str, url: str, timeout_sec: int = 60) -> tuple[int, str, str]:
    """Run chrome --dump-dom; return (rc, stdout_dom, stderr)."""
    ud = tempfile.mkdtemp(prefix="pc-browser-prove-")
    try:
        cmd = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--user-data-dir={ud}",
            "--virtual-time-budget=12000",
            "--dump-dom",
            url,
        ]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        err = (exc.stderr or "") if isinstance(exc.stderr, str) else f"timeout after {timeout_sec}s"
        return 124, out, err
    except OSError as exc:
        return 127, "", f"OSError launching chrome: {exc}"
    finally:
        shutil.rmtree(ud, ignore_errors=True)


def _assert_dom(dom: str) -> tuple[bool, str]:
    """Real DOM checks — Power Claude brand + install CTA (not urllib body theater)."""
    if not dom or len(dom) < 200:
        return False, "dump-dom empty/too short"
    if "Power Claude" not in dom:
        return False, "DOM missing Power Claude"
    # Install CTA cluster: hero/primary data-cta or explicit install/download/trial CTA text.
    has_cta_attr = "data-cta=" in dom
    has_cta_text = bool(
        re.search(
            r"(Premium Trial|download Free|Download Free|Start .*Trial|Install|marketplace\.visualstudio)",
            dom,
            re.I,
        )
    )
    has_cta_btn = ("pc-cta-button" in dom) or ("nllm-btn--primary" in dom)
    if not (has_cta_attr and has_cta_text and has_cta_btn):
        return False, (
            "DOM missing install CTA "
            f"(data-cta={has_cta_attr}, cta_text={has_cta_text}, cta_btn={has_cta_btn})"
        )
    # Prefer hero headline presence as visible brand signal.
    hero = "pc-hero__headline" in dom or "pc-hero__ctas" in dom
    detail = (
        "browser DOM proves Power Claude + install CTA"
        + (" + hero" if hero else "")
        + f" (dom_bytes={len(dom)})"
    )
    return True, detail


def _emit(receipt: dict[str, Any], out_path: Path | None) -> None:
    text = json.dumps(receipt, indent=2) + "\n"
    sys.stdout.write(text)
    sys.stdout.flush()
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(text, encoding="utf-8")
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="browser_product_prove.py",
        description="Fail-closed chrome/chromium DOM prove for product page",
    )
    ap.add_argument("--out", default="", help="optional receipt output path")
    ap.add_argument("--url", default="", help="product page URL override")
    ap.add_argument(
        "--chrome-bin",
        default="",
        help="explicit chrome/chromium binary (also PC_CHROME_PATH)",
    )
    ap.add_argument("-V", "--version", action="store_true")
    args = ap.parse_args(argv)
    if args.version:
        print("power-claude-browser-product-prove 1.0.0")
        return 0

    url = (args.url or os.environ.get("PC_PRODUCT_URL") or DEFAULT_URL).strip()
    out_path = Path(args.out) if args.out else None
    chrome = _find_chrome(args.chrome_bin or None)

    if not chrome:
        receipt = _blocked_receipt(
            detail="chrome/chromium not found (BLOCKED_ENVIRONMENT; not N/A PASS)",
            chrome=None,
            url=url,
        )
        _emit(receipt, out_path)
        print(
            "FAIL  browser_product_page: chrome/chromium missing → BLOCKED_ENVIRONMENT",
            file=sys.stderr,
        )
        return 1

    rc, dom, err = _dump_dom(chrome, url)
    if rc != 0 or not dom.strip():
        # Launch/env failure with chrome present but unusable → blocked, not fake pass.
        low = (err or "").lower()
        blocked = any(
            m in low
            for m in (
                "no space left",
                "cannot open",
                "not found",
                "permission denied",
                "snap-confine",
                "zygote",
            )
        ) or rc in (127, 134)
        err_lines = [ln for ln in (err or "").strip().splitlines() if ln.strip()]
        err_tail = err_lines[-1] if err_lines else "(no stderr)"
        detail = f"chrome dump-dom failed rc={rc}: {err_tail}"
        receipt = _fail_receipt(detail=detail, chrome=chrome, url=url, blocked=blocked or rc == 134)
        _emit(receipt, out_path)
        print(f"FAIL  browser_product_page: {detail}", file=sys.stderr)
        return 1

    ok, detail = _assert_dom(dom)
    if not ok:
        receipt = _fail_receipt(detail=detail, chrome=chrome, url=url, blocked=False)
        _emit(receipt, out_path)
        print(f"FAIL  browser_product_page: {detail}", file=sys.stderr)
        return 1

    receipt = _ok_receipt(detail=detail, chrome=chrome, url=url)
    _emit(receipt, out_path)
    print(f"PASS  browser_product_page: {detail}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
