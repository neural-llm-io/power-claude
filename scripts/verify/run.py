#!/usr/bin/env python3
"""Consumer verify floor for public power-claude."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def pass_(m): print("  PASS  " + m)
def fail_(m): print("  FAIL  " + m)
def main():
    print("power-claude consumer verify")
    print("----------------------------------------")
    rc = 0
    print("Layer 1 -- repo shape")
    required = ["README.md", "LICENSE", "CHANGELOG.md", ".gitignore"]
    for name in required:
        if (ROOT / name).is_file():
            pass_("present " + name)
        else:
            fail_("missing " + name)
            rc = 1
    if (ROOT / "media").is_dir():
        pass_("present media/")
    else:
        fail_("missing media/")
        rc = 1
    print("Layer 2 -- complete-e2e")
    e2e = ROOT / "scripts/complete-e2e/run.py"
    r = subprocess.run([sys.executable, str(e2e)], cwd=str(ROOT))
    if r.returncode == 0:
        pass_("complete-e2e")
    else:
        fail_("complete-e2e")
        rc = 1
    print("----------------------------------------")
    if rc == 0:
        print("VERIFY: PASS")
    else:
        print("VERIFY: FAIL")
    return rc
if __name__ == "__main__":
    raise SystemExit(main())
