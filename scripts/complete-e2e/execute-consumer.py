#!/usr/bin/env python3
"""Live consumer execute adapter: runs consumer.py and emits execute receipt.

behavior_proven=true ONLY when ok=true after a real consumer execute (not inventory,
not skip-npm, not tautology). Named behavior.cases map PASS lines from consumer to
domain outcomes (subprocess CLI help, packed dual-bin --version, npm registry
metadata, marketplace API, marketplace vsix HEAD, marketplace license/details/icon
HEADs, open-vsx vsix download HEAD, product/pricing site cross-links).
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
RECEIPT_PATH = RECEIPT_DIR / "execute-receipt.json"
SCHEMA = "hurc-complete-e2e-power-claude-execute/v1"

# Domain cases already proven by consumer.py — each requires real PASS markers
# tied to subprocess / network outcomes (not assertTrue(true)).
CASE_MARKERS: dict[str, tuple[str, ...]] = {
    "packed_cli_help": (
        "PASS  packed CLI help",
        "PASS  packed CLI help lists consumer commands",
    ),
    # Dual-bin packed consumer: pc + power-claude --version must both match package version.
    "packed_dual_bin_version": (
        "PASS  packed CLI --version matches ",
        "PASS  packed power-claude --version matches ",
    ),
    "registry_metadata": (
        "PASS  registry metadata name/version/bin",
        "PASS  registry tarball HEAD",
    ),
    "marketplace_api": (
        "PASS  marketplace api publisher/name",
        "PASS  marketplace listing body proves Power Claude",
    ),
    "marketplace_vsix_download": (
        "PASS  marketplace vsix HEAD",
    ),
    # Marketplace listing assets already proven by consumer.py (same gallery files loop).
    "marketplace_asset_heads": (
        "PASS  marketplace license HEAD",
        "PASS  marketplace details HEAD",
        "PASS  marketplace icon HEAD",
    ),
    # Live customer surfaces already proven by consumer.py — require named cases.
    "open_vsx_vsix_download": (
        "PASS  open-vsx vsix download HEAD",
    ),
    "product_site_links": (
        "PASS  product site links pricing",
        "PASS  product site links marketplace",
        "PASS  product site links open-vsx",
    ),
    "pricing_page_links": (
        "PASS  pricing page links product",
        "PASS  pricing page links marketplace",
        "PASS  pricing page links open-vsx",
    ),
}

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


def _looks_blocked(blob: str) -> bool:
    low = blob.lower()
    for marker in BLOCK_MARKERS:
        if marker.lower() in low:
            return True
    return False


def _case_from_output(case_id: str, markers: tuple[str, ...], output: str) -> dict[str, Any]:
    missing = [m for m in markers if m not in output]
    if missing:
        return {
            "id": case_id,
            "ok": False,
            "detail": "missing markers: " + "; ".join(missing),
        }
    # Surface the last matching PASS line as detail (real consumer evidence).
    last = ""
    for line in output.splitlines():
        for m in markers:
            if m in line:
                last = line.strip()
    return {"id": case_id, "ok": True, "detail": last or markers[0]}


def _build_receipt(
    *,
    consumer_rc: int,
    output: str,
    skipped_npm: bool,
) -> dict[str, Any]:
    cases = [
        _case_from_output(cid, markers, output)
        for cid, markers in CASE_MARKERS.items()
    ]
    cases_ok = bool(cases) and all(c["ok"] for c in cases)
    consumer_ok = consumer_rc == 0
    blocked = (not consumer_ok or not cases_ok) and _looks_blocked(output)

    if skipped_npm:
        env_status = "partial_skip_npm"
        ok = False
        behavior_proven = False
    elif blocked:
        env_status = "BLOCKED_ENVIRONMENT"
        ok = False
        behavior_proven = False
    elif not consumer_ok or not cases_ok:
        env_status = "execute_failed"
        ok = False
        behavior_proven = False
    else:
        env_status = "live"
        ok = True
        # Real execute only: consumer exit 0 + named domain cases from PASS lines.
        behavior_proven = True

    return {
        "schema": SCHEMA,
        "ok": bool(ok),
        "environment_status": env_status,
        "blocked_environment": bool(blocked),
        "behavior_proven": bool(behavior_proven and ok),
        "executor": "scripts/complete-e2e/consumer.py",
        "consumer_returncode": consumer_rc,
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


def main() -> int:
    argv = sys.argv[1:]
    a = set(argv)
    if a & {"-h", "--help"}:
        print(
            "power-claude-execute-consumer: runs live consumer.py and emits execute "
            "receipt JSON (stdout + .receipts/); use --out PATH to also write a copy"
        )
        return 0
    if a & {"-V", "--version"}:
        print("power-claude-execute-consumer 1.0.0")
        return 0

    out_path: Path | None = None
    args = list(argv)
    if "--out" in args:
        i = args.index("--out")
        if i + 1 >= len(args):
            print("execute-consumer.py: --out requires a path", file=sys.stderr)
            return 2
        out_path = Path(args[i + 1])
        del args[i : i + 2]
    if args:
        print("usage: execute-consumer.py [--out PATH]", file=sys.stderr)
        return 2

    consumer = HERE / "consumer.py"
    if not consumer.is_file():
        print("execute-consumer: missing consumer.py", file=sys.stderr)
        return 2

    env = os.environ.copy()
    skipped_npm = env.get("PC_SKIP_NPM") == "1"

    print("power-claude complete-e2e (execute-consumer)", file=sys.stderr)
    print("----------------------------------------", file=sys.stderr)
    proc = subprocess.run(
        [sys.executable, str(consumer)],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    # Forward consumer streams to stderr so stdout stays receipt-only.
    if proc.stdout:
        sys.stderr.write(proc.stdout)
        if not proc.stdout.endswith("\n"):
            sys.stderr.write("\n")
    if proc.stderr:
        sys.stderr.write(proc.stderr)
        if not proc.stderr.endswith("\n"):
            sys.stderr.write("\n")

    receipt = _build_receipt(
        consumer_rc=proc.returncode,
        output=output,
        skipped_npm=skipped_npm,
    )
    print("----------------------------------------", file=sys.stderr)
    print(
        "EXECUTE: PASS" if receipt["ok"] and receipt["behavior_proven"] else "EXECUTE: FAIL",
        file=sys.stderr,
    )
    _emit_receipt(receipt, out_path)
    return 0 if (receipt.get("ok") is True and receipt.get("behavior_proven") is True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
