#!/usr/bin/env python3
"""release-ready gate for public power-claude mirror."""
# Never ALLOW_UNPROVEN. Never fake CERTIFIED.
from __future__ import annotations
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def pass_(m): print("  PASS  " + m, flush=True)
def fail_(m): print("  FAIL  " + m, flush=True)

def purge_bytecode() -> None:
    for p in list(ROOT.rglob("*")):
        if ".git" in p.parts:
            continue
        if p.name == "__pycache__" and p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.suffix == ".pyc" and p.is_file():
            p.unlink(missing_ok=True)

def run_gate(label: str, script: str, extra_args: list[str] | None = None) -> bool:
    path = ROOT / script
    print("Gate -- " + label)
    if not path.is_file():
        fail_(label + " missing " + script)
        return False
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = ["bash", str(path)] + (extra_args or [])
    r = subprocess.run(cmd, cwd=str(ROOT), env=env)
    if r.returncode == 0:
        pass_(label)
        return True
    fail_(label)
    return False

def main() -> int:
    print("power-claude release-ready")
    print("----------------------------------------")
    print("Policy: never ALLOW_UNPROVEN; never fake CERTIFIED")
    purge_bytecode()
    ok = True
    # enforce --fix first so bytecode from prior runs is cleared
    if not run_gate("enforce --fix", "scripts/enforce/run.sh", ["--fix"]):
        ok = False
    purge_bytecode()
    if not run_gate("tidy --full", "scripts/tidy/run.sh"):
        ok = False
    purge_bytecode()
    if not run_gate("verify", "scripts/verify/run.sh"):
        ok = False
    purge_bytecode()
    print("----------------------------------------")
    if ok:
        print("RELEASE_READY: PASS")
        print("Note: PASS means consumer scripts floor gates green — not a product CERTIFIED claim.")
        return 0
    print("RELEASE_READY: FAIL")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
