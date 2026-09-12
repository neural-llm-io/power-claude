#!/usr/bin/env bash
# Fail-closed gate: execute-consumer receipt must attest ok+behavior_proven with named cases.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXEC="$ROOT/scripts/complete-e2e/execute-consumer.py"
RUNTIME="$ROOT/configs/complete-e2e/runtime.json"
[[ -f "$EXEC" && -f "$RUNTIME" ]] || { echo "FAIL execute-receipt: missing execute-consumer.py or runtime.json" >&2; exit 1; }

tmp="$(mktemp -d "${TMPDIR:-/tmp}/pc-ce2e-execute-receipt-XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

# Unset skip so receipt cannot greenwash a partial execute.
unset PC_SKIP_NPM || true

set +e
python3 "$EXEC" --out "$tmp/receipt.json" >"$tmp/stdout.json" 2>"$tmp/stderr.txt"
rc=$?
set -e

python3 - "$tmp/stdout.json" "$tmp/receipt.json" "$RUNTIME" "$tmp/stderr.txt" "$rc" <<'PY'
import json
import sys
from pathlib import Path

stdout_path, receipt_path, runtime_path, stderr_path, rc_s = sys.argv[1:]
rc = int(rc_s)
stdout_receipt = json.loads(Path(stdout_path).read_text(encoding="utf-8"))
file_receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
runtime = json.loads(Path(runtime_path).read_text(encoding="utf-8"))
stderr = Path(stderr_path).read_text(encoding="utf-8", errors="replace")

assert stdout_receipt == file_receipt, "stdout receipt differs from --out receipt"
assert stdout_receipt.get("ok") is True, stdout_receipt
assert stdout_receipt.get("behavior_proven") is True, stdout_receipt
assert stdout_receipt.get("blocked_environment") is False, stdout_receipt
assert stdout_receipt.get("environment_status") == "live", stdout_receipt
assert stdout_receipt.get("schema") == "hurc-complete-e2e-power-claude-execute/v1", stdout_receipt
cases = stdout_receipt.get("behavior", {}).get("cases")
assert isinstance(cases, list) and len(cases) >= 2, cases
ids = {c.get("id") for c in cases}
# At least one named domain case ok; prefer the three consumer-proven outcomes.
named = {
    "packed_cli_help",
    "packed_dual_bin_version",
    "registry_metadata",
    "marketplace_api",
    "marketplace_vsix_download",
    "marketplace_asset_heads",
    "open_vsx_vsix_download",
    "open_vsx_asset_heads",
    "product_site_links",
    "pricing_page_links",
}
assert named <= ids, ids
assert all(c.get("ok") is True for c in cases if c.get("id") in named), cases
# Fail-closed: every required live customer-surface case must be present+ok.
assert all(c.get("ok") is True for c in cases), cases
assert rc == 0, f"execute-consumer exited {rc}; stderr=\n{stderr[-2000:]}"

adapters = runtime.get("adapters") or []
ids_rt = {a.get("id") for a in adapters}
assert "power-claude-list-surfaces" in ids_rt, ids_rt
assert "power-claude-execute-consumer" in ids_rt, ids_rt
assert "power-claude-prove-receipt" in ids_rt, ids_rt
# list / execute / prove cells — no inventory-as-prove, execute is distinct.
assert "power-claude-prove-run" not in ids_rt, ids_rt
exec_adapter = next(a for a in adapters if a.get("id") == "power-claude-execute-consumer")
assert exec_adapter.get("argv") == ["python3", "scripts/complete-e2e/execute-consumer.py"], exec_adapter
assert exec_adapter.get("kind") != "prover", exec_adapter
list_adapter = next(a for a in adapters if a.get("id") == "power-claude-list-surfaces")
assert list_adapter.get("argv") == ["python3", "scripts/complete-e2e/list-surfaces.py"], list_adapter
receipt_adapter = next(a for a in adapters if a.get("id") == "power-claude-prove-receipt")
assert receipt_adapter.get("argv") == ["python3", "scripts/complete-e2e/prove.py", "--receipt"], receipt_adapter

print(
    "PASS complete-e2e-execute-receipt: ok=true behavior_proven=true live cases "
    + ",".join(sorted(ids & named))
)
PY
