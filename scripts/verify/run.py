#!/usr/bin/env python3
"""Consumer verify floor for public power-claude."""
from __future__ import annotations
import os, subprocess, sys
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
    print("Layer 2 -- README media refs")
    media_py = ROOT / "scripts/complete-e2e/check_readme_media.py"
    r = subprocess.run([sys.executable, str(media_py)], cwd=str(ROOT))
    if r.returncode == 0:
        pass_("readme media refs")
    else:
        fail_("readme media refs")
        rc = 1
    print("Layer 3 -- consumer complete-e2e")
    consumer = ROOT / "scripts/complete-e2e/consumer.py"
    env = os.environ.copy()
    if os.environ.get("PC_SKIP_NPM") == "1":
        env["PC_SKIP_NPM"] = "1"
    r = subprocess.run([sys.executable, str(consumer)], cwd=str(ROOT), env=env)
    if r.returncode == 0:
        pass_("consumer complete-e2e")
    else:
        fail_("consumer complete-e2e")
        rc = 1
    print("----------------------------------------")
    if rc == 0:
        print("VERIFY: PASS")
    else:
        print("VERIFY: FAIL")
    return rc
if __name__ == "__main__":
    raise SystemExit(main())
