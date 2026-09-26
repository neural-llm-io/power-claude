#!/usr/bin/env bash
# Fail-closed: missing chrome → BLOCKED_ENVIRONMENT (never N/A PASS);
# live chrome dump-dom proves pricing page Power Claude + pricing signals.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROVE="$ROOT/scripts/complete-e2e/browser_pricing_prove.py"
RUNTIME="$ROOT/configs/complete-e2e/runtime.json"
[[ -f "$PROVE" && -f "$RUNTIME" ]] || {
  echo "FAIL browser-pricing-prove: missing script or runtime.json" >&2
  exit 1
}

tmp="$(mktemp -d "${TMPDIR:-/tmp}/pc-ce2e-browser-pricing-prove-XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

# 1) Missing chrome must BLOCKED_ENVIRONMENT (tips #500-502).
set +e
python3 "$PROVE" --chrome-bin /no/such/chrome/binary --out "$tmp/blocked.json" \
  >"$tmp/blocked.stdout.json" 2>"$tmp/blocked.stderr.txt"
blocked_rc=$?
set -e
python3 - "$tmp/blocked.stdout.json" "$tmp/blocked.json" "$blocked_rc" <<'PY'
import json, sys
from pathlib import Path
stdout_path, receipt_path, rc_s = sys.argv[1:]
rc = int(rc_s)
stdout = json.loads(Path(stdout_path).read_text(encoding="utf-8"))
receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
assert stdout == receipt
assert rc != 0, "missing chrome must exit non-zero"
assert receipt.get("ok") is False, receipt
assert receipt.get("blocked_environment") is True, receipt
assert receipt.get("environment_status") == "BLOCKED_ENVIRONMENT", receipt
assert receipt.get("behavior_proven") is False, receipt
cases = (receipt.get("behavior") or {}).get("cases") or []
assert any(c.get("id") == "browser_pricing_page" and c.get("ok") is False for c in cases), cases
print("PASS  browser_pricing_prove blocked_environment on missing chrome")
PY

# 2) Live chrome dump-dom must prove pricing page (real DOM, not urllib).
set +e
python3 "$PROVE" --out "$tmp/live.json" >"$tmp/live.stdout.json" 2>"$tmp/live.stderr.txt"
live_rc=$?
set -e
python3 - "$tmp/live.stdout.json" "$tmp/live.json" "$RUNTIME" "$live_rc" "$tmp/live.stderr.txt" <<'PY'
import json, sys
from pathlib import Path
stdout_path, receipt_path, runtime_path, rc_s, stderr_path = sys.argv[1:]
rc = int(rc_s)
stderr = Path(stderr_path).read_text(encoding="utf-8", errors="replace")
stdout = json.loads(Path(stdout_path).read_text(encoding="utf-8"))
receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
runtime = json.loads(Path(runtime_path).read_text(encoding="utf-8"))
assert stdout == receipt
assert rc == 0, f"live browser pricing prove exited {rc}; stderr=\n{stderr[-2000:]}"
assert receipt.get("ok") is True, receipt
assert receipt.get("behavior_proven") is True, receipt
assert receipt.get("blocked_environment") is False, receipt
assert receipt.get("environment_status") == "live", receipt
cases = (receipt.get("behavior") or {}).get("cases") or []
assert any(c.get("id") == "browser_pricing_page" and c.get("ok") is True for c in cases), cases
detail = next(c.get("detail") for c in cases if c.get("id") == "browser_pricing_page")
assert "Power Claude" in detail or "pricing signals" in detail, detail
ids = {a.get("id") for a in (runtime.get("adapters") or [])}
assert "power-claude-browser-pricing-prove" in ids, ids
print("PASS  browser_pricing_prove live DOM")
PY

echo "PASS complete-e2e-browser-pricing-prove"
