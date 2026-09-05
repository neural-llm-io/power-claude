#!/usr/bin/env python3
"""tidy --full floor for public power-claude mirror."""
from __future__ import annotations
import py_compile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def pass_(m): print("  PASS  " + m, flush=True)
def fail_(m): print("  FAIL  " + m, flush=True)
def main():
    print("power-claude tidy --full")
    print("----------------------------------------")
    rc = 0
    print("Layer 1 -- no bytecode junk")
    junk = []
    for p in ROOT.rglob("*"):
        if ".git" in p.parts: continue
        if p.name == "__pycache__" or p.suffix == ".pyc": junk.append(p)
    if not junk: pass_("no __pycache__/.pyc")
    else:
        fail_("bytecode: " + ", ".join(str(x.relative_to(ROOT)) for x in junk[:8]))
        rc = 1
    print("Layer 2 -- scripts compile + shebang")
    scripts_root = ROOT / "scripts"
    py_files = sorted(scripts_root.rglob("*.py")) if scripts_root.is_dir() else []
    sh_files = sorted(scripts_root.rglob("*.sh")) if scripts_root.is_dir() else []
    for py in py_files:
        if "__pycache__" in py.parts: continue
        try:
            py_compile.compile(str(py), doraise=True)
            pass_("compile " + str(py.relative_to(ROOT)))
        except Exception as e:
            fail_("compile " + str(py.relative_to(ROOT)) + ": " + str(e))
            rc = 1
    for sh in sh_files:
        text = sh.read_text(encoding="utf-8", errors="replace")
        if text.startswith("#!"): pass_("shebang " + str(sh.relative_to(ROOT)))
        else:
            fail_("missing shebang " + str(sh.relative_to(ROOT)))
            rc = 1
    print("Layer 3 -- gitignore covers bytecode")
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8", errors="replace")
    if "__pycache__" in gi or "*.pyc" in gi: pass_(".gitignore covers bytecode")
    else:
        fail_(".gitignore missing __pycache__/*.pyc")
        rc = 1
    print("----------------------------------------")
    print("TIDY: PASS" if rc == 0 else "TIDY: FAIL")
    return rc
if __name__ == "__main__":
    raise SystemExit(main())
