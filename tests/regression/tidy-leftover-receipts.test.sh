#!/usr/bin/env bash
# Fail-closed: tidy must FAIL on leftover .receipts without --full, and
# --full must purge leftovers then PASS. Also require .gitignore +.receipts
# coverage and no git-tracked receipts.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TIDY_PY="$ROOT/scripts/tidy/run.py"
GI="$ROOT/.gitignore"
RECEIPT_DIR="$ROOT/scripts/complete-e2e/.receipts"
PLANTED="$RECEIPT_DIR/prove-receipt.json"

[[ -f "$TIDY_PY" ]] || { echo "FAIL tidy-leftover: missing scripts/tidy/run.py" >&2; exit 1; }
[[ -f "$GI" ]] || { echo "FAIL tidy-leftover: missing .gitignore" >&2; exit 1; }

# gitignore must cover bytecode + .receipts
python3 - "$GI" <<'PY'
import sys
from pathlib import Path
gi = Path(sys.argv[1]).read_text(encoding="utf-8")
assert "__pycache__" in gi or "*.pyc" in gi, "gitignore missing bytecode"
assert ".receipts/" in gi or ".receipts" in gi, "gitignore missing .receipts/"
print("ok gitignore covers bytecode + .receipts")
PY

# git must not already track receipts
python3 - "$ROOT" <<'PY'
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
r = subprocess.run(["git", "ls-files", "-z"], cwd=str(root), capture_output=True)
assert r.returncode == 0, r.stderr
tracked = []
for raw in (r.stdout or b"").split(b"\0"):
    if not raw:
        continue
    rel = raw.decode("utf-8", errors="replace")
    parts = Path(rel).parts
    if ".receipts" in parts or Path(rel).name in ("prove-receipt.json", "execute-receipt.json"):
        tracked.append(rel)
assert not tracked, f"git already tracks receipts: {tracked}"
print("ok no tracked receipts")
PY

# Ensure clean starting point for PASS path: remove any prior leftovers.
rm -rf "$RECEIPT_DIR"
find "$ROOT" -type d -name '__pycache__' -not -path '*/.git/*' -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type f -name '*.pyc' -not -path '*/.git/*' -delete 2>/dev/null || true

# Clean tree + --full => PASS
set +e
python3 "$TIDY_PY" --full >"$ROOT/tmp-tidy-clean.out" 2>&1
rc_clean=$?
set -e
if [[ "$rc_clean" -ne 0 ]] || ! grep -q 'TIDY: PASS' "$ROOT/tmp-tidy-clean.out"; then
  echo "FAIL tidy-leftover: clean --full expected PASS rc=0" >&2
  cat "$ROOT/tmp-tidy-clean.out" >&2
  rm -f "$ROOT/tmp-tidy-clean.out"
  exit 1
fi
rm -f "$ROOT/tmp-tidy-clean.out"

# Plant leftover receipt => tidy without --full must FAIL
mkdir -p "$RECEIPT_DIR"
cat > "$PLANTED" <<'JSON'
{"schema":"planted-leftover","ok":true,"behavior_proven":true,"prover":"PLANTED_LEFTOVER"}
JSON

set +e
python3 "$TIDY_PY" >"$ROOT/tmp-tidy-plant.out" 2>&1
rc_plant=$?
set -e
if [[ "$rc_plant" -eq 0 ]] || ! grep -q 'TIDY: FAIL' "$ROOT/tmp-tidy-plant.out"; then
  echo "FAIL tidy-leftover: planted leftover expected FAIL rc!=0" >&2
  cat "$ROOT/tmp-tidy-plant.out" >&2
  rm -rf "$RECEIPT_DIR" "$ROOT/tmp-tidy-plant.out"
  exit 1
fi
if ! grep -q 'leftover receipts' "$ROOT/tmp-tidy-plant.out"; then
  echo "FAIL tidy-leftover: expected leftover receipts FAIL line" >&2
  cat "$ROOT/tmp-tidy-plant.out" >&2
  rm -rf "$RECEIPT_DIR" "$ROOT/tmp-tidy-plant.out"
  exit 1
fi
# Planted file must still exist (check mode does not purge)
[[ -f "$PLANTED" ]] || { echo "FAIL tidy-leftover: check mode deleted planted receipt" >&2; exit 1; }
rm -f "$ROOT/tmp-tidy-plant.out"

# --full must purge planted leftover then PASS
set +e
python3 "$TIDY_PY" --full >"$ROOT/tmp-tidy-fix.out" 2>&1
rc_fix=$?
set -e
if [[ "$rc_fix" -ne 0 ]] || ! grep -q 'TIDY: PASS' "$ROOT/tmp-tidy-fix.out"; then
  echo "FAIL tidy-leftover: --full after plant expected PASS" >&2
  cat "$ROOT/tmp-tidy-fix.out" >&2
  rm -rf "$RECEIPT_DIR" "$ROOT/tmp-tidy-fix.out"
  exit 1
fi
if [[ -f "$PLANTED" ]]; then
  echo "FAIL tidy-leftover: --full left planted receipt on disk" >&2
  rm -rf "$RECEIPT_DIR" "$ROOT/tmp-tidy-fix.out"
  exit 1
fi
rm -f "$ROOT/tmp-tidy-fix.out"
rm -rf "$RECEIPT_DIR"

echo "PASS tidy-leftover-receipts: clean --full PASS; planted leftover FAIL; --full purges"
