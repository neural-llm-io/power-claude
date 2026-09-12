#!/usr/bin/env python3
"""Live consumer prove wrapper + fail-closed prove receipt (NDP/hurc contract shape)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RECEIPT_DIR = HERE / ".receipts"
RECEIPT_PATH = RECEIPT_DIR / "prove-receipt.json"
SCHEMA = "hurc-complete-e2e-power-claude-prove/v1"

BLOCK_MARKERS = (
    "URLError",
    "HTTPError",
    "timed out",
    "Temporary failure in name resolution",
    "Network is unreachable",
    "Connection refused",
    "Name or service not known",
    "nodename nor servname",
    "getaddrinfo failed",
    "Failed to connect",
    "network is down",
    "Could not resolve host",
    "ENOTFOUND",
    "ECONNREFUSED",
    "ETIMEDOUT",
)


def _run_case(case_id: str, script: Path, env: dict[str, str]) -> dict[str, Any]:
    if not script.is_file():
        return {
            "id": case_id,
            "ok": False,
            "detail": f"missing script {script.relative_to(ROOT)}",
            "returncode": 127,
            "stdout": "",
            "stderr": "",
        }
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    detail = out.strip().splitlines()[-1] if out.strip() else f"exit {proc.returncode}"
    return {
        "id": case_id,
        "ok": proc.returncode == 0,
        "detail": detail[:500],
        "returncode": proc.returncode,
        "stdout": proc.stdout or "",
        "stderr": proc.stderr or "",
    }


def _looks_blocked(cases: list[dict[str, Any]]) -> bool:
    blob = "\n".join(
        (c.get("stdout") or "") + "\n" + (c.get("stderr") or "") + "\n" + (c.get("detail") or "")
        for c in cases
        if not c.get("ok")
    )
    low = blob.lower()
    for marker in BLOCK_MARKERS:
        if marker.lower() in low:
            return True
    return False


def _build_receipt(cases_raw: list[dict[str, Any]], skipped_npm: bool) -> dict[str, Any]:
    cases = [{"id": c["id"], "ok": bool(c["ok"]), "detail": c["detail"]} for c in cases_raw]
    all_ok = bool(cases) and all(c["ok"] for c in cases)
    blocked = (not all_ok) and _looks_blocked(cases_raw)
    # Skip-npm is not a full live consumer prove — never greenwash as behavior_proven.
    real_prove = all_ok and not skipped_npm and any(
        c["id"] in {"consumer_complete_e2e", "readme_media"} and c["ok"] for c in cases
    )
    if blocked:
        env_status = "BLOCKED_ENVIRONMENT"
        ok = False
        behavior_proven = False
    elif not all_ok:
        env_status = "prove_failed"
        ok = False
        behavior_proven = False
    elif skipped_npm:
        env_status = "partial_skip_npm"
        ok = False
        behavior_proven = False
    else:
        env_status = "live"
        ok = True
        behavior_proven = bool(real_prove)

    return {
        "schema": SCHEMA,
        "ok": ok,
        "environment_status": env_status,
        "blocked_environment": bool(blocked),
        "behavior_proven": bool(behavior_proven and ok),
        "prover": "scripts/complete-e2e/check_readme_media.py + scripts/complete-e2e/consumer.py",
        "behavior": {
            "status": "ok" if behavior_proven and ok else ("blocked" if blocked else "fail"),
            "cases": cases,
        },
    }


def _emit_receipt(receipt: dict[str, Any], out_path: Path | None) -> None:
    text = json.dumps(receipt, indent=2) + "\n"
    sys.stdout.write(text)
    sys.stdout.flush()
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(text, encoding="utf-8")
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")


def _receipt_mode(argv: list[str]) -> int:
    out_path: Path | None = None
    args = list(argv)
    if "--out" in args:
        i = args.index("--out")
        if i + 1 >= len(args):
            print("prove.py --receipt: --out requires a path", file=sys.stderr)
            return 2
        out_path = Path(args[i + 1])
        del args[i : i + 2]
    # strip --receipt itself if still present
    args = [a for a in args if a != "--receipt"]
    if args:
        print("usage: prove.py --receipt [--out PATH]", file=sys.stderr)
        return 2

    env = os.environ.copy()
    skipped_npm = env.get("PC_SKIP_NPM") == "1"
    cases_raw = [
        _run_case("readme_media", HERE / "check_readme_media.py", env),
        _run_case("consumer_complete_e2e", HERE / "consumer.py", env),
    ]
    # Mirror run.py human summary on stderr so stdout stays receipt-only.
    print("power-claude complete-e2e (prove-receipt)", file=sys.stderr)
    print("----------------------------------------", file=sys.stderr)
    for c in cases_raw:
        label = "PASS" if c["ok"] else "FAIL"
        print(f"  {label}  {c['id']}: {c['detail'][:120]}", file=sys.stderr)
        # Also forward captured streams to stderr for diagnosis
        if c.get("stdout"):
            sys.stderr.write(c["stdout"])
            if not str(c["stdout"]).endswith("\n"):
                sys.stderr.write("\n")
        if c.get("stderr"):
            sys.stderr.write(c["stderr"])
            if not str(c["stderr"]).endswith("\n"):
                sys.stderr.write("\n")
    receipt = _build_receipt(cases_raw, skipped_npm=skipped_npm)
    print("----------------------------------------", file=sys.stderr)
    print(
        "COMPLETE_E2E: PASS" if receipt["ok"] and receipt["behavior_proven"] else "COMPLETE_E2E: FAIL",
        file=sys.stderr,
    )
    _emit_receipt(receipt, out_path)
    # Fail closed: non-zero unless ok and behavior_proven.
    return 0 if (receipt.get("ok") is True and receipt.get("behavior_proven") is True) else 1


def main() -> int:
    argv = sys.argv[1:]
    a = set(argv)
    if a & {"-h", "--help"}:
        print(
            "power-claude-prove: wraps scripts/complete-e2e/run.py live consumer proofs; "
            "use --receipt for fail-closed JSON receipt (stdout + .receipts/)"
        )
        return 0
    if a & {"-V", "--version"}:
        print("power-claude-prove 1.1.0")
        return 0
    if "--receipt" in a:
        return _receipt_mode(argv)

    # Default: live wrap of run.py (existing), plus best-effort file receipt from exit code.
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/complete-e2e/run.py")],
        cwd=str(ROOT),
    )
    # File-only receipt after live run (stdout remains run.py human output).
    ok_live = proc.returncode == 0
    skipped_npm = os.environ.get("PC_SKIP_NPM") == "1"
    cases = [
        {
            "id": "readme_media",
            "ok": ok_live,
            "detail": "bundled via run.py (see live output)",
        },
        {
            "id": "consumer_complete_e2e",
            "ok": ok_live and not skipped_npm,
            "detail": "bundled via run.py (see live output)",
        },
    ]
    receipt = {
        "schema": SCHEMA,
        "ok": bool(ok_live and not skipped_npm),
        "environment_status": "live" if ok_live and not skipped_npm else ("partial_skip_npm" if skipped_npm else "prove_failed"),
        "blocked_environment": False,
        "behavior_proven": bool(ok_live and not skipped_npm),
        "prover": "scripts/complete-e2e/run.py",
        "behavior": {"status": "ok" if ok_live and not skipped_npm else "fail", "cases": cases},
    }
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
