#!/usr/bin/env bash
# Theater-kill: packed_cli_help_documents must require doctor/resume
# --help mentions emergency. Shallow packed_cli_help_cluster markers are
# prefixes of those lines; without elevating, cluster + docs (recover/etc.)
# can greenwash execute/prove without the emergency document PASS lines.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXEC="$ROOT/scripts/complete-e2e/execute-consumer.py"
[[ -f "$EXEC" ]] || { echo "FAIL help-documents-emergency: missing execute-consumer.py" >&2; exit 1; }

python3 - "$EXEC" <<'PY'
import importlib.util
import sys
from pathlib import Path

exec_path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("execute_consumer", exec_path)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

docs = mod.CASE_MARKERS["packed_cli_help_documents"]
cluster = mod.CASE_MARKERS["packed_cli_help_cluster"]

need = (
    "PASS  packed CLI doctor --help mentions emergency",
    "PASS  packed CLI resume --help mentions emergency",
)
for m in need:
    assert m in docs, f"missing elevated marker in packed_cli_help_documents: {m!r}"

# Prefix-shadow: shallow cluster markers are literal prefixes of mentions lines.
assert "PASS  packed CLI doctor --help" in cluster
assert "PASS  packed CLI resume --help" in cluster
assert "PASS  packed CLI doctor --help mentions emergency".startswith(
    "PASS  packed CLI doctor --help"
)
assert "PASS  packed CLI resume --help mentions emergency".startswith(
    "PASS  packed CLI resume --help"
)

# Theater: all cluster + docs EXCEPT mentions emergency → docs must FAIL.
shallow_lines = [f"  {m}" for m in cluster]
shallow_lines += [f"  {m}" for m in docs if "mentions emergency" not in m]
shallow_out = "\n".join(shallow_lines) + "\n"
c = mod._case_from_output("packed_cli_help_cluster", cluster, shallow_out)
d = mod._case_from_output("packed_cli_help_documents", docs, shallow_out)
assert c["ok"] is True, c
assert d["ok"] is False, (
    "theater: packed_cli_help_documents greened without mentions emergency: "
    + repr(d)
)
assert "mentions emergency" in (d.get("detail") or ""), d

# Honest: add both mentions lines → docs PASS.
honest = shallow_out + "\n".join(f"  {m}" for m in need) + "\n"
d2 = mod._case_from_output("packed_cli_help_documents", docs, honest)
assert d2["ok"] is True, d2

print(
    "PASS complete-e2e-help-documents-emergency-markers: "
    "mentions emergency elevated; shallow-without-emergency fails documents"
)
PY
