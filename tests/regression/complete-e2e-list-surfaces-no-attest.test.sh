#!/usr/bin/env bash
# Fail-closed gate: list-surfaces inventory MUST NEVER set behavior_proven true.
# Inventory is not a prove/execute path — self-attestation is forbidden.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LIST="$ROOT/scripts/complete-e2e/list-surfaces.py"
RUNTIME="$ROOT/configs/complete-e2e/runtime.json"
[[ -f "$LIST" && -f "$RUNTIME" ]] || { echo "FAIL list-surfaces-no-attest: missing list-surfaces.py or runtime.json" >&2; exit 1; }

tmp="$(mktemp -d "${TMPDIR:-/tmp}/pc-ce2e-list-no-attest-XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

set +e
python3 "$LIST" >"$tmp/stdout.json" 2>"$tmp/stderr.txt"
rc=$?
set -e

python3 - "$tmp/stdout.json" "$RUNTIME" "$tmp/stderr.txt" "$rc" "$LIST" <<'PY'
import json
import sys
from pathlib import Path

stdout_path, runtime_path, stderr_path, rc_s, list_path = sys.argv[1:]
rc = int(rc_s)
stderr = Path(stderr_path).read_text(encoding="utf-8", errors="replace")
assert rc == 0, f"list-surfaces exited {rc}; stderr=\n{stderr[-2000:]}"

payload = json.loads(Path(stdout_path).read_text(encoding="utf-8"))
assert payload.get("schema") == "hurc-complete-e2e-runtime-surfaces/v1", payload

# Core guard: behavior_proven must never be true (omit OR explicit false both OK).
if "behavior_proven" in payload:
    assert payload.get("behavior_proven") is False, (
        "list-surfaces must never set behavior_proven true; got "
        + repr(payload.get("behavior_proven"))
    )
# Soft prefer: if present, must be JSON false (not 0/"false"/None theater).
if "behavior_proven" in payload:
    assert payload["behavior_proven"] is False and type(payload["behavior_proven"]) is bool, payload

# Must still inventory surfaces.
surfaces = payload.get("surfaces")
assert isinstance(surfaces, list) and len(surfaces) >= 1, surfaces
ids = {s.get("id") for s in surfaces}
assert "cli:prove" in ids or "cli:complete-e2e" in ids, ids

# Source must not contain a true-assignment path for behavior_proven.
src = Path(list_path).read_text(encoding="utf-8")
banned_true_literals = (
    '"behavior_proven": true',
    '"behavior_proven":true',
    "'behavior_proven': True",
    '"behavior_proven": True',
    "behavior_proven=True",
    "behavior_proven = True",
)
for lit in banned_true_literals:
    assert lit not in src, f"list-surfaces.py contains forbidden attestation literal: {lit!r}"

# Runtime: list adapter must remain inventory cli — never a prover that self-attests.
runtime = json.loads(Path(runtime_path).read_text(encoding="utf-8"))
adapters = runtime.get("adapters") or []
list_adapters = [a for a in adapters if a.get("id") == "power-claude-list-surfaces"]
assert len(list_adapters) == 1, adapters
la = list_adapters[0]
assert la.get("kind") == "cli", la
assert la.get("kind") != "prover", la
assert la.get("argv") == ["python3", "scripts/complete-e2e/list-surfaces.py"], la
# No other adapter may point list-surfaces as a prover.
for a in adapters:
    argv = a.get("argv") or []
    joined = " ".join(str(x) for x in argv)
    if "list-surfaces" in joined:
        assert a.get("kind") != "prover", a
        assert a.get("id") == "power-claude-list-surfaces", a

print("PASS complete-e2e-list-surfaces-no-attest: behavior_proven!=true; list not registered as prover")
PY
