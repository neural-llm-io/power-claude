#!/usr/bin/env bash
# Fail-closed gate: scripts/enforce/run.py must actually RUN key regressions
# (subprocess), not merely assert Path.is_file presence (theater).
# Running tests is a check — even under --fix (not a chmod-fix).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENFORCE_PY="$ROOT/scripts/enforce/run.py"
[[ -f "$ENFORCE_PY" ]] || { echo "FAIL enforce-runs: missing scripts/enforce/run.py" >&2; exit 1; }

python3 - "$ENFORCE_PY" <<'PY'
import ast
import sys
from pathlib import Path

src_path = Path(sys.argv[1])
src = src_path.read_text(encoding="utf-8")
tree = ast.parse(src, filename=str(src_path))

required = [
    "tests/regression/complete-e2e-execute-receipt.test.sh",
    "tests/regression/complete-e2e-prove-receipt.test.sh",
    "tests/regression/complete-e2e-clean-room-replay.test.sh",
]

has_subprocess_run = False
string_consts: set[str] = set()

for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        func = node.func
        if (
            isinstance(func, ast.Attribute)
            and func.attr == "run"
            and isinstance(func.value, ast.Name)
            and func.value.id == "subprocess"
        ):
            has_subprocess_run = True
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        string_consts.add(node.value)

assert has_subprocess_run, (
    "enforce/run.py must call subprocess.run to execute regressions "
    "(presence-only is theater)"
)

for rel in required:
    assert rel in string_consts, f"missing live regression constant: {rel}"

assert "Layer 3b" in src or "run fail-closed regressions" in src, (
    "enforce must have an explicit run-fail-closed-regressions layer"
)

# --fix must not skip regression execution (running tests is check, not fix).
state = {"saw_regression_for": False, "bad_fix_gate": False}


class FixGateChecker(ast.NodeVisitor):
    def __init__(self) -> None:
        self.stack: list[ast.AST] = []

    def generic_visit(self, node: ast.AST) -> None:
        self.stack.append(node)
        super().generic_visit(node)
        self.stack.pop()

    def visit_For(self, node: ast.For) -> None:
        it = node.iter
        name = it.id if isinstance(it, ast.Name) else None
        if name and "regression" in name.lower():
            state["saw_regression_for"] = True
            for anc in self.stack:
                if not isinstance(anc, ast.If):
                    continue
                test = anc.test
                if isinstance(test, ast.Name) and test.id == "do_fix":
                    state["bad_fix_gate"] = True
                if (
                    isinstance(test, ast.UnaryOp)
                    and isinstance(test.op, ast.Not)
                    and isinstance(test.operand, ast.Name)
                    and test.operand.id == "do_fix"
                ):
                    state["bad_fix_gate"] = True
        self.generic_visit(node)


FixGateChecker().visit(tree)
assert state["saw_regression_for"], (
    "enforce/run.py must iterate a live_regressions (or *regression*) list"
)
assert not state["bad_fix_gate"], (
    "live regression runs must not be gated on do_fix "
    "(--fix path: running tests is check, not chmod-fix)"
)

assert "not a chmod-fix" in src, (
    "enforce must document that regression runs are checks under --fix"
)

print(
    "PASS enforce-runs-fail-closed-regressions: subprocess.run executes "
    + ",".join(required)
    + "; not presence-only; not --fix-gated"
)
PY
