#!/usr/bin/env python3
"""Live consumer prove wrapper + fail-closed prove receipt (NDP/hurc contract shape).

--receipt runs readme_media + execute-consumer (live consumer domain cases) and emits
a fail-closed receipt. Richer behavior.cases ids (packed_cli_help,
packed_dual_bin_version, registry_metadata, marketplace_api, marketplace_vsix_download,
marketplace_asset_heads, open_vsx_vsix_download, product_site_links, pricing_page_links)
are required for behavior_proven when prove succeeds.
"""
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

# Domain cases surfaced by execute-consumer (must appear in prove receipt on success).
RICH_CASE_IDS = (
    "packed_cli_help",
    "packed_dual_bin_version",
    "registry_metadata",
    "marketplace_api",
    "marketplace_vsix_download",
    "marketplace_asset_heads",
    "open_vsx_vsix_download",
    "product_site_links",
    "pricing_page_links",
)

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


def _run_script(script: Path, extra_argv: list[str], env: dict[str, str]) -> dict[str, Any]:
    if not script.is_file():
        return {
            "ok": False,
            "detail": f"missing script {script.relative_to(ROOT)}",
            "returncode": 127,
            "stdout": "",
            "stderr": "",
        }
    proc = subprocess.run(
        [sys.executable, str(script), *extra_argv],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    detail = out.strip().splitlines()[-1] if out.strip() else f"exit {proc.returncode}"
    return {
        "ok": proc.returncode == 0,
        "detail": detail[:500],
        "returncode": proc.returncode,
        "stdout": proc.stdout or "",
        "stderr": proc.stderr or "",
    }


def _looks_blocked(blobs: list[str]) -> bool:
    blob = "\n".join(blobs)
    low = blob.lower()
    for marker in BLOCK_MARKERS:
        if marker.lower() in low:
            return True
    return False


def _parse_execute_receipt(stdout: str) -> dict[str, Any] | None:
    text = (stdout or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Best-effort: last JSON object in stdout
        start = text.rfind("{")
        if start < 0:
            return None
        try:
            return json.loads(text[start:])
        except json.JSONDecodeError:
            return None


def _build_receipt(
    *,
    readme: dict[str, Any],
    execute: dict[str, Any],
    execute_receipt: dict[str, Any] | None,
    skipped_npm: bool,
) -> dict[str, Any]:
    cases: list[dict[str, Any]] = [
        {
            "id": "readme_media",
            "ok": bool(readme.get("ok")),
            "detail": readme.get("detail") or "",
        },
        {
            "id": "consumer_complete_e2e",
            "ok": bool(execute.get("ok")) and bool(execute_receipt and execute_receipt.get("ok")),
            "detail": (
                (execute_receipt or {}).get("behavior", {}).get("status")
                if execute_receipt
                else execute.get("detail") or ""
            )
            or (execute.get("detail") or ""),
        },
    ]

    # Fold named domain cases from execute receipt (required richer ids).
    rich_from_exec: dict[str, dict[str, Any]] = {}
    if execute_receipt:
        for c in (execute_receipt.get("behavior") or {}).get("cases") or []:
            cid = c.get("id")
            if cid in RICH_CASE_IDS:
                rich_from_exec[cid] = {
                    "id": cid,
                    "ok": bool(c.get("ok")),
                    "detail": c.get("detail") or "",
                }
    for cid in RICH_CASE_IDS:
        if cid in rich_from_exec:
            cases.append(rich_from_exec[cid])
        else:
            cases.append(
                {
                    "id": cid,
                    "ok": False,
                    "detail": "missing from execute-consumer receipt",
                }
            )

    all_ok = bool(cases) and all(c["ok"] for c in cases)
    blocked = (not all_ok) and _looks_blocked(
        [
            readme.get("stdout") or "",
            readme.get("stderr") or "",
            readme.get("detail") or "",
            execute.get("stdout") or "",
            execute.get("stderr") or "",
            execute.get("detail") or "",
            json.dumps(execute_receipt) if execute_receipt else "",
        ]
    )
    # Skip-npm is not a full live consumer prove — never greenwash as behavior_proven.
    rich_ok = all(
        any(c["id"] == rid and c["ok"] for c in cases) for rid in RICH_CASE_IDS
    )
    real_prove = (
        all_ok
        and not skipped_npm
        and any(c["id"] == "consumer_complete_e2e" and c["ok"] for c in cases)
        and any(c["id"] == "readme_media" and c["ok"] for c in cases)
        and rich_ok
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
        "prover": (
            "scripts/complete-e2e/check_readme_media.py + "
            "scripts/complete-e2e/execute-consumer.py"
        ),
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

    print("power-claude complete-e2e (prove-receipt)", file=sys.stderr)
    print("----------------------------------------", file=sys.stderr)

    # Fail-closed: runtime.json adapter argv targets must exist (MISSING_PROVER).
    # Path occupancy is not a live prove — never greenwash behavior_proven here.
    gate = _run_script(HERE / "check-adapter-paths.py", [], env)
    gate_receipt = _parse_execute_receipt(gate.get("stdout") or "")
    gate_detail = (
        (gate_receipt or {}).get("detail")
        or gate.get("detail")
        or "MISSING_PROVER"
    )
    print(
        f"  {'PASS' if gate['ok'] else 'FAIL'}  adapter_paths: {str(gate_detail)[:160]}",
        file=sys.stderr,
    )
    if gate.get("stderr"):
        sys.stderr.write(gate["stderr"])
        if not str(gate["stderr"]).endswith("\n"):
            sys.stderr.write("\n")
    if not gate.get("ok"):
        receipt = {
            "schema": SCHEMA,
            "ok": False,
            "environment_status": "MISSING_PROVER",
            "blocked_environment": False,
            "behavior_proven": False,
            "prover": "scripts/complete-e2e/check-adapter-paths.py",
            "behavior": {
                "status": "fail",
                "cases": [
                    {
                        "id": "adapter_paths",
                        "ok": False,
                        "detail": gate_detail,
                    }
                ],
            },
        }
        print("----------------------------------------", file=sys.stderr)
        print("COMPLETE_E2E: FAIL", file=sys.stderr)
        _emit_receipt(receipt, out_path)
        return 1

    readme = _run_script(HERE / "check_readme_media.py", [], env)
    print(
        f"  {'PASS' if readme['ok'] else 'FAIL'}  readme_media: {readme['detail'][:120]}",
        file=sys.stderr,
    )
    if readme.get("stdout"):
        sys.stderr.write(readme["stdout"])
        if not str(readme["stdout"]).endswith("\n"):
            sys.stderr.write("\n")
    if readme.get("stderr"):
        sys.stderr.write(readme["stderr"])
        if not str(readme["stderr"]).endswith("\n"):
            sys.stderr.write("\n")

    # Require live execute path (runs consumer; emits domain cases).
    execute = _run_script(HERE / "execute-consumer.py", [], env)
    execute_receipt = _parse_execute_receipt(execute.get("stdout") or "")
    print(
        f"  {'PASS' if execute['ok'] else 'FAIL'}  execute-consumer: {execute['detail'][:120]}",
        file=sys.stderr,
    )
    # Forward execute stderr (consumer live output lives there).
    if execute.get("stderr"):
        sys.stderr.write(execute["stderr"])
        if not str(execute["stderr"]).endswith("\n"):
            sys.stderr.write("\n")

    receipt = _build_receipt(
        readme=readme,
        execute=execute,
        execute_receipt=execute_receipt,
        skipped_npm=skipped_npm,
    )
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
            "power-claude-prove: wraps execute-consumer + readme_media live proofs; "
            "use --receipt for fail-closed JSON receipt (stdout + .receipts/)"
        )
        return 0
    if a & {"-V", "--version"}:
        print("power-claude-prove 1.2.0")
        return 0
    if "--receipt" in a:
        return _receipt_mode(argv)

    # Default: live wrap of run.py for human COMPLETE_E2E output.
    # Theater-kill: NEVER attest behavior_proven without --receipt (rich execute path).
    # A file receipt may exist for diagnostics but behavior_proven stays false.
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/complete-e2e/run.py")],
        cwd=str(ROOT),
    )
    ok_live = proc.returncode == 0
    skipped_npm = os.environ.get("PC_SKIP_NPM") == "1"
    cases = [
        {
            "id": "readme_media",
            "ok": ok_live,
            "detail": "bundled via run.py (see live output); use --receipt to attest",
        },
        {
            "id": "consumer_complete_e2e",
            "ok": ok_live and not skipped_npm,
            "detail": "bundled via run.py (see live output); use --receipt to attest",
        },
    ]
    receipt = {
        "schema": SCHEMA,
        "ok": False,
        "environment_status": (
            "receipt_mode_required"
            if ok_live and not skipped_npm
            else ("partial_skip_npm" if skipped_npm else "prove_failed")
        ),
        "blocked_environment": False,
        # Fail-closed: only prove.py --receipt (execute-consumer rich cases) may attest.
        "behavior_proven": False,
        "prover": "scripts/complete-e2e/run.py",
        "behavior": {
            "status": "fail",
            "cases": cases,
        },
    }
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
