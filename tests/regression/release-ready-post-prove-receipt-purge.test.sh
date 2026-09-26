#!/usr/bin/env bash
# Fail-closed: release-ready must purge canonical .receipts/ AFTER prove --receipt
# (tidy runs before prove; prove always writes leftovers even on prove_failed).
# Theater-kill / honesty unit — does not require marketplace green.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RR_PY="$ROOT/scripts/release-ready/run.py"
RECEIPT_DIR="$ROOT/scripts/complete-e2e/.receipts"
PLANTED="$RECEIPT_DIR/prove-receipt.json"
OUTSIDE="$ROOT/browser-openvsx-prove-receipt.json"

[[ -f "$RR_PY" ]] || { echo "FAIL rr-post-prove-purge: missing scripts/release-ready/run.py" >&2; exit 1; }

# Source contract: purge_leftover_receipts exists and is invoked after run_prove_receipt.
python3 - "$RR_PY" <<'PY'
import ast
import sys
from pathlib import Path

src_path = Path(sys.argv[1])
src = src_path.read_text(encoding="utf-8")
tree = ast.parse(src, filename=str(src_path))

funcs = {
    n.name
    for n in ast.walk(tree)
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
}
assert "purge_leftover_receipts" in funcs, "missing purge_leftover_receipts()"
assert "run_prove_receipt" in funcs, "missing run_prove_receipt()"

# Find main() call order: run_prove_receipt then purge_leftover_receipts.
main = None
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name == "main":
        main = n
        break
assert main is not None, "missing main()"

call_names: list[str] = []
for node in ast.walk(main):
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Name):
            call_names.append(f.id)

assert "run_prove_receipt" in call_names, "main must call run_prove_receipt"
assert "purge_leftover_receipts" in call_names, "main must call purge_leftover_receipts"
i_prove = call_names.index("run_prove_receipt")
i_purge = call_names.index("purge_leftover_receipts")
assert i_prove < i_purge, (
    "purge_leftover_receipts must run AFTER run_prove_receipt "
    f"(order={call_names})"
)
# Must not only purge bytecode after prove (the pre-fix theater gap).
assert "post-prove leftover receipt purge" in src, (
    "release-ready must label Gate -- post-prove leftover receipt purge"
)
print("ok source: purge_leftover_receipts after run_prove_receipt")
PY

# Functional: plant leftovers as prove --receipt does on prove_failed; purge must clear.
rm -rf "$RECEIPT_DIR"
rm -f "$OUTSIDE"
mkdir -p "$RECEIPT_DIR"
cat > "$PLANTED" <<'JSON'
{"schema":"planted-leftover","ok":false,"behavior_proven":false,"environment_status":"prove_failed","prover":"PLANTED_POST_PROVE"}
JSON
# Also plant a browser receipt basename outside .receipts/ (same class as #105).
cat > "$OUTSIDE" <<'JSON'
{"schema":"planted-leftover-browser","ok":false,"behavior_proven":false,"prover":"PLANTED_BROWSER_OUTSIDE"}
JSON

python3 - "$ROOT" <<'PY'
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1])
rr = root / "scripts" / "release-ready" / "run.py"
spec = importlib.util.spec_from_file_location("pc_release_ready", rr)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

planted = root / "scripts" / "complete-e2e" / ".receipts" / "prove-receipt.json"
outside = root / "browser-openvsx-prove-receipt.json"
assert planted.is_file(), "planted canonical receipt missing"
assert outside.is_file(), "planted outside browser receipt missing"

ok = mod.purge_leftover_receipts()
assert ok is True, "purge_leftover_receipts must return True after clearing"
assert not planted.exists(), "canonical prove-receipt.json must be purged"
assert not outside.exists(), "outside browser receipt must be purged"
leftover = mod._find_leftover_receipts()
assert not leftover, f"leftovers remain after purge: {leftover}"
print("ok purge_leftover_receipts clears planted prove_failed leftovers")
PY

# Fail-closed: if a leftover cannot be removed, purge must FAIL (not greenwash).
# Simulate by planting a leftover under a non-writable directory when possible;
# otherwise verify the remain-path by monkeypatching _remove_path to no-op.
python3 - "$ROOT" <<'PY'
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1])
rr = root / "scripts" / "release-ready" / "run.py"
spec = importlib.util.spec_from_file_location("pc_release_ready2", rr)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

receipt_dir = root / "scripts" / "complete-e2e" / ".receipts"
receipt_dir.mkdir(parents=True, exist_ok=True)
stuck = receipt_dir / "prove-receipt.json"
stuck.write_text(
    '{"schema":"stuck-leftover","ok":true,"behavior_proven":true}\n',
    encoding="utf-8",
)

# No-op remover → leftover must remain → purge returns False (fail-closed).
mod._remove_path = lambda p: None  # type: ignore[assignment]
ok = mod.purge_leftover_receipts()
assert ok is False, "purge must FAIL when leftovers remain after purge attempt"
assert stuck.is_file(), "stuck leftover should still exist for this check"
# Real purge for cleanup
importlib.reload  # keep linter quiet
spec2 = importlib.util.spec_from_file_location("pc_release_ready3", rr)
mod2 = importlib.util.module_from_spec(spec2)
assert spec2 and spec2.loader
spec2.loader.exec_module(mod2)
assert mod2.purge_leftover_receipts() is True
assert not stuck.exists()
print("ok purge fail-closed when leftover remains")
PY

rm -rf "$RECEIPT_DIR"
rm -f "$OUTSIDE"

echo "PASS release-ready-post-prove-receipt-purge: source order + purge prove_failed leftovers + fail-closed remain"
