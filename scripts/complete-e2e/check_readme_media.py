#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
root = Path(__file__).resolve().parents[2]
readme = (root / "README.md").read_text(encoding="utf-8", errors="replace")
refs = sorted(set(re.findall(r"(media/[A-Za-z0-9_./\\-]+)", readme)))
missing = []
ok = []
empty = []
for ref in refs:
    ref = ref.rstrip(").,]")
    p = root / ref
    if not p.exists():
        missing.append(ref)
    elif p.is_file() and p.stat().st_size == 0:
        empty.append(ref)
    else:
        ok.append(ref)
print(f"checked={len(refs)} present={len(ok)} missing={len(missing)} empty={len(empty)}")
for m in missing: print(f"MISSING {m}")
for e in empty: print(f"EMPTY {e}")
sys.exit(1 if missing or empty else 0)
