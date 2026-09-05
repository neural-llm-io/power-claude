#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
root = Path(__file__).resolve().parents[2]
readme = (root / "README.md").read_text(encoding="utf-8", errors="replace")
refs = sorted(set(re.findall(r"(media/[A-Za-z0-9_./\\-]+)", readme)))
missing = []
ok = []
for ref in refs:
    ref = ref.rstrip(").,]")
    p = root / ref
    (ok if p.exists() else missing).append(ref)
print(f"checked={len(refs)} present={len(ok)} missing={len(missing)}")
for m in missing: print(f"MISSING {m}")
sys.exit(1 if missing else 0)
