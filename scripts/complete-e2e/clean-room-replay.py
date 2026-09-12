#!/usr/bin/env python3
"""Clean-room replay gate for authoritative complete-e2e prove receipt.

Deletes any on-disk prove receipt, re-runs prove.py --receipt, then fail-closed
if the receipt is missing, stale (mtime before replay start), or
behavior_proven is not true. Also requires ok=true, live env, and the richer
domain behavior.cases (packed_cli_help, packed_dual_bin_version,
registry_metadata, marketplace_api, marketplace_vsix_download, open_vsx_vsix_download,
product_site_links, pricing_page_links).

This closes the MISSING_PROVER gap where a stale/planted receipt could be
trusted without a fresh prove. Inventory/list paths must never substitute.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RECEIPT_DIR = HERE / ".receipts"
RECEIPT_PATH = RECEIPT_DIR / "prove-receipt.json"
PROVE = HERE / "prove.py"
SCHEMA = "hurc-complete-e2e-power-claude-prove/v1"
RICH_CASE_IDS = (
    "packed_cli_help",
    "packed_dual_bin_version",
    "registry_metadata",
    "marketplace_api",
    "marketplace_vsix_download",
    "open_vsx_vsix_download",
    "product_site_links",
    "pricing_page_links",
)
# Allow tiny clock skew between wall start and filesystem mtime.
MTIME_SKEW_SEC = 2.0


def _fail(msg: str) -> int:
    print(f"FAIL  clean-room-replay: {msg}", file=sys.stderr)
    print("CLEAN_ROOM_REPLAY: FAIL", file=sys.stderr)
    return 1


def _load_receipt(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _validate_receipt(receipt: dict[str, Any]) -> str | None:
    if receipt.get("schema") != SCHEMA:
        return f"schema want {SCHEMA} got {receipt.get('schema')!r}"
    if receipt.get("ok") is not True:
        return f"ok!=true ({receipt.get('ok')!r})"
    if receipt.get("behavior_proven") is not True:
        return f"behavior_proven!=true ({receipt.get('behavior_proven')!r})"
    if receipt.get("blocked_environment") is True:
        return "blocked_environment=true"
    if receipt.get("environment_status") != "live":
        return f"environment_status!='live' ({receipt.get('environment_status')!r})"
    cases = (receipt.get("behavior") or {}).get("cases")
    if not isinstance(cases, list) or len(cases) < 10:
        return f"behavior.cases too short: {cases!r}"
    by_id = {c.get("id"): c for c in cases if isinstance(c, dict)}
    for need in ("readme_media", "consumer_complete_e2e", *RICH_CASE_IDS):
        c = by_id.get(need)
        if not c:
            return f"missing case {need}"
        if c.get("ok") is not True:
            return f"case {need} ok!=true"
    return None


def main() -> int:
    argv = sys.argv[1:]
    a = set(argv)
    if a & {"-h", "--help"}:
        print(
            "power-claude-clean-room-replay: delete prove receipt, re-run "
            "prove.py --receipt, fail-closed on missing/stale/behavior_proven!=true"
        )
        return 0
    if a & {"-V", "--version"}:
        print("power-claude-clean-room-replay 1.0.0")
        return 0
    if argv:
        print("usage: clean-room-replay.py", file=sys.stderr)
        return 2

    if not PROVE.is_file():
        return _fail("missing scripts/complete-e2e/prove.py")

    # Skip-npm cannot greenwash a clean-room replay.
    if os.environ.get("PC_SKIP_NPM") == "1":
        return _fail("PC_SKIP_NPM=1 is not a clean-room prove (refusing)")

    print("power-claude complete-e2e (clean-room-replay)", file=sys.stderr)
    print("----------------------------------------", file=sys.stderr)

    t0 = time.time()
    # Clean room: never trust a pre-existing receipt.
    if RECEIPT_PATH.is_file():
        RECEIPT_PATH.unlink()
        print("  .     removed stale prove-receipt.json", file=sys.stderr)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.pop("PC_SKIP_NPM", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    proc = subprocess.run(
        [sys.executable, str(PROVE), "--receipt"],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    # Forward prove stderr (live progress); stdout is receipt JSON.
    if proc.stderr:
        sys.stderr.write(proc.stderr)
        if not proc.stderr.endswith("\n"):
            sys.stderr.write("\n")

    if proc.returncode != 0:
        return _fail(f"prove.py --receipt exited {proc.returncode}")

    if not RECEIPT_PATH.is_file():
        return _fail(f"receipt missing after prove: {RECEIPT_PATH.relative_to(ROOT)}")

    mtime = RECEIPT_PATH.stat().st_mtime
    if mtime < (t0 - MTIME_SKEW_SEC):
        return _fail(
            f"receipt stale: mtime={mtime:.3f} < replay_start={t0:.3f} "
            f"(skew_allow={MTIME_SKEW_SEC})"
        )

    # Prefer on-disk receipt; cross-check stdout JSON when present.
    file_receipt = _load_receipt(RECEIPT_PATH)
    if file_receipt is None:
        return _fail("receipt unreadable/invalid JSON after prove")

    stdout_text = (proc.stdout or "").strip()
    if stdout_text:
        try:
            stdout_receipt = json.loads(stdout_text)
        except json.JSONDecodeError:
            return _fail("prove stdout is not valid receipt JSON")
        if stdout_receipt != file_receipt:
            return _fail("stdout receipt differs from on-disk prove-receipt.json")

    err = _validate_receipt(file_receipt)
    if err:
        return _fail(err)

    print("----------------------------------------", file=sys.stderr)
    print(
        "  PASS  clean-room replay: fresh receipt ok+behavior_proven "
        "readme_media+consumer_complete_e2e+"
        + "+".join(RICH_CASE_IDS),
        file=sys.stderr,
    )
    print("CLEAN_ROOM_REPLAY: PASS", file=sys.stderr)
    # Emit validated receipt on stdout for harness consumers.
    sys.stdout.write(json.dumps(file_receipt, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
