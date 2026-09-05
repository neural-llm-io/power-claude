#!/usr/bin/env python3
"""release-ready gate for public power-claude mirror."""
# Never ALLOW_UNPROVEN. Never fake CERTIFIED.
from __future__ import annotations
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def pass_(m): print("  PASS  " + m, flush=True)
def fail_(m): print("  FAIL  " + m, flush=True)
def run_gate(label, script):
    path = ROOT / script
    print("Gate -- " + label)
    if not path.is_file():
        fail_(label + " missing " + script)
        return False
    r = subprocess.run(["bash", str(path)], cwd=str(ROOT))
    if r.returncode == 0:
        pass_(label)
        return True
    fail_(label)
    return False
def main():
    print("power-claude release-ready")
    print("----------------------------------------")
    print("Policy: never ALLOW_UNPROVEN; never fake CERTIFIED")
    ok = True
    for label, script in [
        ("verify", "scripts/verify/run.sh"),
        ("tidy --full", "scripts/tidy/run.sh"),
        ("enforce", "scripts/enforce/run.sh"),
    ]:
        if not run_gate(label, script):
            ok = False
    print("----------------------------------------")
    if ok:
        print("RELEASE_READY: PASS")
        print("Note: PASS means consumer scripts floor gates green — not a product CERTIFIED claim.")
        return 0
    print("RELEASE_READY: FAIL")
    return 1
if __name__ == "__main__":
    raise SystemExit(main())
