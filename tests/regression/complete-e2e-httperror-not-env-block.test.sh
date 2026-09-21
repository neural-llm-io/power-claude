#!/usr/bin/env bash
# Fail-closed: marketplace HTTP 4xx / HTTPError must NOT classify as BLOCKED_ENVIRONMENT.
# Real infra blocks (URLError, Connection refused) still must.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXEC="$ROOT/scripts/complete-e2e/execute-consumer.py"
PROVE="$ROOT/scripts/complete-e2e/prove.py"
[[ -f "$EXEC" && -f "$PROVE" ]] || {
  echo "FAIL httperror-not-env-block: missing execute-consumer.py or prove.py" >&2
  exit 1
}

python3 - "$EXEC" "$PROVE" <<'PY'
import importlib.util
import sys
from pathlib import Path

def load(path: Path):
    name = path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

exec_mod = load(Path(sys.argv[1]))
prove_mod = load(Path(sys.argv[2]))

assert "HTTPError" not in exec_mod.BLOCK_MARKERS, exec_mod.BLOCK_MARKERS
assert "HTTPError" not in prove_mod.BLOCK_MARKERS, prove_mod.BLOCK_MARKERS
assert "URLError" in exec_mod.BLOCK_MARKERS
assert "URLError" in prove_mod.BLOCK_MARKERS
assert "Connection refused" in exec_mod.BLOCK_MARKERS
assert "Connection refused" in prove_mod.BLOCK_MARKERS

not_blocked = [
    "HTTP Error 404: Not Found",
    "marketplace listing HTTPError: HTTP Error 404: Not Found",
    "urllib.error.HTTPError: HTTP Error 404: Not Found",
    "marketplace_api FAIL HTTPError 404",
]
still_blocked = [
    "urllib.error.URLError: <urlopen error [Errno 111] Connection refused>",
    "Connection refused",
    "Temporary failure in name resolution",
    "URLError: timed out",
]

for blob in not_blocked:
    assert exec_mod._looks_blocked(blob) is False, blob
    assert prove_mod._looks_blocked([blob]) is False, blob

for blob in still_blocked:
    assert exec_mod._looks_blocked(blob) is True, blob
    assert prove_mod._looks_blocked([blob]) is True, blob

print(
    "PASS complete-e2e-httperror-not-env-block: "
    "HTTP 4xx/HTTPError not env-block; URLError/Connection refused still blocked"
)
PY
