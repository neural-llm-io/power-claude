#!/usr/bin/env bash
# Fail-closed gate: clean-room replay must delete any planted/stale prove receipt,
# re-run prove.py --receipt, and fail if receipt missing/stale/behavior_proven!=true.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPLAY="$ROOT/scripts/complete-e2e/clean-room-replay.py"
PROVE="$ROOT/scripts/complete-e2e/prove.py"
RUNTIME="$ROOT/configs/complete-e2e/runtime.json"
RECEIPT="$ROOT/scripts/complete-e2e/.receipts/prove-receipt.json"
[[ -f "$REPLAY" && -f "$PROVE" && -f "$RUNTIME" ]] || {
  echo "FAIL clean-room-replay: missing replay/prove/runtime" >&2
  exit 1
}

tmp="$(mktemp -d "${TMPDIR:-/tmp}/pc-ce2e-clean-room-XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

unset PC_SKIP_NPM || true

# Plant a FAKE stale green receipt (would greenwash if replay trusted disk without re-run).
mkdir -p "$(dirname "$RECEIPT")"
python3 - "$RECEIPT" <<'PY'
import json, os, time
from pathlib import Path
path = Path(__import__("sys").argv[1])
fake = {
    "schema": "hurc-complete-e2e-power-claude-prove/v1",
    "ok": True,
    "environment_status": "live",
    "blocked_environment": False,
    "behavior_proven": True,
    "prover": "PLANTED_STALE_FAKE",
    "behavior": {
        "status": "ok",
        "cases": [
            {"id": "readme_media", "ok": True, "detail": "PLANTED"},
            {"id": "consumer_complete_e2e", "ok": True, "detail": "PLANTED"},
            {"id": "packed_cli_help", "ok": True, "detail": "PLANTED"},
            {"id": "registry_metadata", "ok": True, "detail": "PLANTED"},
            {"id": "marketplace_api", "ok": True, "detail": "PLANTED"},
        ],
    },
}
path.write_text(json.dumps(fake, indent=2) + "\n", encoding="utf-8")
# Age the file well before replay start so a non-rewriting path would be "stale".
old = time.time() - 3600
os.utime(path, (old, old))
print("planted stale fake receipt mtime=", path.stat().st_mtime)
PY

# PC_SKIP_NPM must refuse (theater-kill).
set +e
PC_SKIP_NPM=1 python3 "$REPLAY" >"$tmp/skip.out" 2>"$tmp/skip.err"
skip_rc=$?
set -e
[[ "$skip_rc" -ne 0 ]] || { echo "FAIL: clean-room must refuse PC_SKIP_NPM=1" >&2; exit 1; }
grep -q "PC_SKIP_NPM" "$tmp/skip.err" || { echo "FAIL: skip refuse message missing" >&2; cat "$tmp/skip.err" >&2; exit 1; }

# Live clean-room replay must PASS and overwrite the planted fake.
set +e
python3 "$REPLAY" >"$tmp/stdout.json" 2>"$tmp/stderr.txt"
rc=$?
set -e

python3 - "$tmp/stdout.json" "$RECEIPT" "$RUNTIME" "$tmp/stderr.txt" "$rc" <<'PY'
import json
import sys
from pathlib import Path

stdout_path, receipt_path, runtime_path, stderr_path, rc_s = sys.argv[1:]
rc = int(rc_s)
stderr = Path(stderr_path).read_text(encoding="utf-8", errors="replace")
assert rc == 0, f"clean-room-replay exited {rc}; stderr=\n{stderr[-2500:]}"

stdout_receipt = json.loads(Path(stdout_path).read_text(encoding="utf-8"))
file_receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
runtime = json.loads(Path(runtime_path).read_text(encoding="utf-8"))

assert stdout_receipt == file_receipt, "stdout receipt differs from on-disk prove-receipt"
assert file_receipt.get("ok") is True, file_receipt
assert file_receipt.get("behavior_proven") is True, file_receipt
assert file_receipt.get("environment_status") == "live", file_receipt
assert file_receipt.get("prover") != "PLANTED_STALE_FAKE", (
    "clean-room trusted planted stale receipt without re-prove"
)
# Real prove path mentions execute-consumer / check_readme_media.
prover = str(file_receipt.get("prover") or "")
assert "execute-consumer" in prover or "check_readme_media" in prover, prover
cases = file_receipt.get("behavior", {}).get("cases") or []
details = " ".join(str(c.get("detail") or "") for c in cases)
assert "PLANTED" not in details, "planted fake case details survived replay"
ids = {c.get("id") for c in cases}
for rid in (
    "readme_media",
    "consumer_complete_e2e",
    "packed_cli_help",
    "packed_dual_bin_version",
    "registry_metadata",
    "marketplace_api",
    "marketplace_vsix_download",
    "open_vsx_vsix_download",
    "product_site_links",
    "pricing_page_links",
):
    assert rid in ids, ids
assert all(c.get("ok") is True for c in cases), cases

adapters = runtime.get("adapters") or []
ids_rt = {a.get("id") for a in adapters}
assert "power-claude-list-surfaces" in ids_rt, ids_rt
assert "power-claude-execute-consumer" in ids_rt, ids_rt
assert "power-claude-prove-receipt" in ids_rt, ids_rt
assert "power-claude-clean-room-replay" in ids_rt, ids_rt
replay_adapter = next(a for a in adapters if a.get("id") == "power-claude-clean-room-replay")
assert replay_adapter.get("kind") == "prover", replay_adapter
assert replay_adapter.get("argv") == [
    "python3",
    "scripts/complete-e2e/clean-room-replay.py",
], replay_adapter
assert replay_adapter.get("fail_closed_on_unreachable") is True, replay_adapter
assert "CLEAN_ROOM_REPLAY: PASS" in stderr, stderr[-1500:]

print(
    "PASS complete-e2e-clean-room-replay: deleted planted stale receipt; "
    "re-ran prove --receipt; ok+behavior_proven; runtime prover cell present"
)
PY
