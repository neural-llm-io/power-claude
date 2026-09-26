#!/usr/bin/env python3
"""Fail-closed live browser prove for the Open VSX Power Claude listing.

Opens https://open-vsx.org/extension/neural-llm/power-claude (or PC_OPENVSX_URL)
via chrome/chromium --dump-dom (real browser DOM, NOT urllib). Open VSX is an SPA:
urllib gets an empty shell; chrome virtual-time renders Power Claude + Install/Download.
Distinct from open_vsx_* urllib API/HEAD cases and browser_product/pricing pages.

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
RECEIPT_PATH = RECEIPT_DIR / "browser-openvsx-prove-receipt.json"
SCHEMA = "hurc-complete-e2e-power-claude-browser-openvsx/v1"
DEFAULT_URL = "https://open-vsx.org/extension/neural-llm/power-claude"

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
        "prover": "scripts/complete-e2e/browser_openvsx_prove.py",
        "chrome": chrome,
        "url": url,
        "behavior": {
            "status": "blocked",
            "cases": [
                {
                    "id": "browser_openvsx_page",
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
        "prover": "scripts/complete-e2e/browser_openvsx_prove.py",
        "chrome": chrome,
        "url": url,
        "behavior": {
            "status": "fail",
            "cases": [
                {
                    "id": "browser_openvsx_page",
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
        "prover": "scripts/complete-e2e/browser_openvsx_prove.py",
        "chrome": chrome,
        "url": url,
        "behavior": {
            "status": "ok",
            "cases": [
                {
                    "id": "browser_openvsx_page",
                    "ok": True,
                    "detail": detail,
                }
            ],
        },
    }


def _dump_dom(chrome: str, url: str, timeout_sec: int = 60) -> tuple[int, str, str]:
    """Run chrome --dump-dom; return (rc, stdout_dom, stderr)."""
    ud = tempfile.mkdtemp(prefix="pc-browser-openvsx-prove-")
    try:
        cmd = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--user-data-dir={ud}",
            "--virtual-time-budget=15000",
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
    """Real DOM checks — Power Claude + Open VSX listing signals (not urllib API theater)."""
    if not dom or len(dom) < 200:
        return False, "dump-dom empty/too short"
    if "Power Claude" not in dom:
        return False, "DOM missing Power Claude"
    # Extension identity + publisher namespace (SPA-rendered; urllib shell lacks these).
    has_ext_id = "power-claude" in dom
    has_publisher = "neural-llm" in dom
    # Install/Download CTA cluster on Open VSX listing (distinct from product/pricing CTAs).
    has_cta = bool(
        re.search(r"\b(Install|Download)\b", dom, re.I)
    ) or (".vsix" in dom.lower())
    if not (has_ext_id and has_publisher and has_cta):
        return False, (
            "DOM missing Open VSX listing signals "
            f"(ext_id={has_ext_id}, publisher={has_publisher}, cta={has_cta})"
        )
    detail = (
        "browser DOM proves Power Claude + Open VSX listing signals"
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
        prog="browser_openvsx_prove.py",
        description="Fail-closed chrome/chromium DOM prove for Open VSX listing",
    )
    ap.add_argument("--out", default="", help="optional receipt output path")
    ap.add_argument("--url", default="", help="Open VSX listing URL override")
    ap.add_argument(
        "--chrome-bin",
        default="",
        help="explicit chrome/chromium binary (also PC_CHROME_PATH)",
    )
    ap.add_argument("-V", "--version", action="store_true")
    args = ap.parse_args(argv)
    if args.version:
        print("power-claude-browser-openvsx-prove 1.0.0")
        return 0

    url = (args.url or os.environ.get("PC_OPENVSX_URL") or DEFAULT_URL).strip()
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
            "FAIL  browser_openvsx_page: chrome/chromium missing → BLOCKED_ENVIRONMENT",
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
        print(f"FAIL  browser_openvsx_page: {detail}", file=sys.stderr)
        return 1

    ok, detail = _assert_dom(dom)
    if not ok:
        receipt = _fail_receipt(detail=detail, chrome=chrome, url=url, blocked=False)
        _emit(receipt, out_path)
        print(f"FAIL  browser_openvsx_page: {detail}", file=sys.stderr)
        return 1

    receipt = _ok_receipt(detail=detail, chrome=chrome, url=url)
    _emit(receipt, out_path)
    print(f"PASS  browser_openvsx_page: {detail}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
