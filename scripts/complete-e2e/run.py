#!/usr/bin/env python3
"""Canonical complete-e2e entry: README media refs + consumer prove."""
from __future__ import annotations
import os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

def main() -> int:
    print("power-claude complete-e2e")
    print("----------------------------------------")
    rc = 0
    media = HERE / "check_readme_media.py"
    r = subprocess.run([sys.executable, str(media)], cwd=str(ROOT))
    if r.returncode == 0:
        print("  PASS  readme media refs", flush=True)
    else:
        print("  FAIL  readme media refs", flush=True)
        rc = 1
    consumer = HERE / "consumer.py"
    env = os.environ.copy()
    if os.environ.get("PC_SKIP_NPM") == "1":
        env["PC_SKIP_NPM"] = "1"
    r = subprocess.run([sys.executable, str(consumer)], cwd=str(ROOT), env=env)
    if r.returncode == 0:
        print("  PASS  consumer complete-e2e", flush=True)
    else:
        print("  FAIL  consumer complete-e2e", flush=True)
        rc = 1
    print("----------------------------------------")
    print("COMPLETE_E2E: PASS" if rc == 0 else "COMPLETE_E2E: FAIL")
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
