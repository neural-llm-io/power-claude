#!/usr/bin/env bash
# Fail-closed gate: runtime.json adapter argv targets must exist; phantom path => MISSING_PROVER.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GATE="$ROOT/scripts/complete-e2e/check-adapter-paths.py"
RUNTIME="$ROOT/configs/complete-e2e/runtime.json"
[[ -f "$GATE" && -f "$RUNTIME" ]] || {
  echo "FAIL adapter-paths: missing check-adapter-paths.py or runtime.json" >&2
  exit 1
}

tmp="$(mktemp -d "${TMPDIR:-/tmp}/pc-ce2e-adapter-paths-XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

# Live runtime must PASS path occupancy (behavior_proven stays false).
set +e
python3 "$GATE" >"$tmp/live.out" 2>"$tmp/live.err"
live_rc=$?
set -e

python3 - "$tmp/live.out" "$tmp/live.err" "$RUNTIME" "$live_rc" <<'PY'
import json
import sys
from pathlib import Path

out_path, err_path, runtime_path, rc_s = sys.argv[1:]
rc = int(rc_s)
receipt = json.loads(Path(out_path).read_text(encoding="utf-8"))
stderr = Path(err_path).read_text(encoding="utf-8", errors="replace")
runtime = json.loads(Path(runtime_path).read_text(encoding="utf-8"))

assert rc == 0, f"live gate exited {rc}; stderr=\n{stderr[-2000:]}"
assert receipt.get("schema") == "hurc-complete-e2e-power-claude-adapter-paths/v1", receipt
assert receipt.get("ok") is True, receipt
assert receipt.get("error") in (None, ""), receipt
# Theater-kill: path occupancy must never attest behavior_proven.
assert receipt.get("behavior_proven") is False, receipt
assert receipt.get("targets_checked", 0) >= 4, receipt
assert "ADAPTER_PATHS: PASS" in stderr, stderr[-1000:]

adapters = runtime.get("adapters") or []
ids = {a.get("id") for a in adapters}
assert "power-claude-adapter-paths" in ids, ids
gate_adapter = next(a for a in adapters if a.get("id") == "power-claude-adapter-paths")
assert gate_adapter.get("kind") == "prover", gate_adapter
assert gate_adapter.get("argv") == [
    "python3",
    "scripts/complete-e2e/check-adapter-paths.py",
], gate_adapter
assert gate_adapter.get("fail_closed_on_unreachable") is True, gate_adapter
# Every adapter argv path-like target exists on disk (same rule as the gate).
root = Path(runtime_path).resolve().parents[2]
for a in adapters:
    argv = a.get("argv") or []
    for tok in argv:
        if not isinstance(tok, str) or tok.startswith("-"):
            continue
        if tok in {"python3", "python", "bash", "sh"}:
            continue
        if "/" in tok or tok.endswith((".py", ".sh")):
            assert (root / tok).is_file(), f"missing {tok} for {a.get('id')}"

print("PASS complete-e2e-adapter-paths: live runtime argv paths present; behavior_proven=false")
PY

# Plant a runtime with a phantom prover argv target — must MISSING_PROVER.
python3 - "$tmp/phantom-runtime.json" <<'PY'
import json
from pathlib import Path
path = Path(__import__("sys").argv[1])
phantom = {
    "schema": "hurc-complete-e2e-runtime/v1",
    "description": "planted phantom adapter for MISSING_PROVER regression",
    "adapters": [
        {
            "id": "power-claude-list-surfaces",
            "kind": "cli",
            "surface_kind": "cli",
            "timeout_sec": 30,
            "argv": ["python3", "scripts/complete-e2e/list-surfaces.py"],
        },
        {
            "id": "power-claude-phantom-prover",
            "kind": "prover",
            "surface_kind": "cli",
            "timeout_sec": 30,
            "fail_closed_on_unreachable": True,
            "argv": [
                "python3",
                "scripts/complete-e2e/DOES_NOT_EXIST_phantom_prover.py",
            ],
        },
    ],
}
path.write_text(json.dumps(phantom, indent=2) + "\n", encoding="utf-8")
PY

set +e
python3 "$GATE" --runtime "$tmp/phantom-runtime.json" >"$tmp/phantom.out" 2>"$tmp/phantom.err"
phantom_rc=$?
set -e

python3 - "$tmp/phantom.out" "$tmp/phantom.err" "$phantom_rc" <<'PY'
import json
import sys
from pathlib import Path

out_path, err_path, rc_s = sys.argv[1:]
rc = int(rc_s)
receipt = json.loads(Path(out_path).read_text(encoding="utf-8"))
stderr = Path(err_path).read_text(encoding="utf-8", errors="replace")

assert rc != 0, "phantom argv target must fail-closed (got rc=0)"
assert receipt.get("ok") is False, receipt
assert receipt.get("error") == "MISSING_PROVER", receipt
assert receipt.get("behavior_proven") is False, receipt
missing = receipt.get("missing") or []
blob = " ".join(missing) + " " + str(receipt.get("detail") or "")
assert "DOES_NOT_EXIST_phantom_prover.py" in blob, receipt
assert "MISSING_PROVER" in stderr, stderr[-1000:]
assert "ADAPTER_PATHS: FAIL" in stderr, stderr[-1000:]

print(
    "PASS complete-e2e-adapter-paths: phantom argv target => MISSING_PROVER fail-closed"
)
PY
