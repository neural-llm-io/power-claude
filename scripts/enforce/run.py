#!/usr/bin/env python3
"""enforce --fix floor for public power-claude mirror."""
from __future__ import annotations
import os, shutil, stat, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def pass_(m): print("  PASS  " + m, flush=True)
def fail_(m): print("  FAIL  " + m, flush=True)
def info_(m): print("  FIX   " + m, flush=True)
def main():
    do_fix = "--fix" in sys.argv
    print("power-claude enforce" + (" --fix" if do_fix else ""))
    print("----------------------------------------")
    rc = 0
    scripts_root = ROOT / "scripts"
    print("Layer 1 -- shell scripts executable + shebang")
    for sh in sorted(scripts_root.rglob("*.sh")):
        rel = str(sh.relative_to(ROOT))
        text = sh.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("#!"):
            fail_("missing shebang " + rel); rc = 1; continue
        mode = sh.stat().st_mode
        if mode & stat.S_IXUSR:
            pass_("exec+shebang " + rel)
        elif do_fix:
            sh.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            info_("chmod +x " + rel)
        else:
            fail_("not executable " + rel); rc = 1
    print("Layer 2 -- purge bytecode")
    junk = [p for p in ROOT.rglob("*") if ".git" not in p.parts and (p.name == "__pycache__" or p.suffix == ".pyc")]
    if not junk: pass_("no bytecode")
    elif do_fix:
        for p in junk:
            if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
            elif p.exists(): p.unlink()
            info_("removed " + str(p.relative_to(ROOT)))
    else:
        fail_("bytecode present"); rc = 1
    print("Layer 3 -- required prove entrypoints")
    required = ["scripts/verify/run.sh", "scripts/verify/run.py", "scripts/complete-e2e/consumer.py", "scripts/complete-e2e/consumer.sh", "scripts/complete-e2e/check_readme_media.py", "scripts/complete-e2e/run.py", "scripts/complete-e2e/run.sh", "scripts/complete-e2e/prove.py", "scripts/complete-e2e/prove.sh", "scripts/complete-e2e/list-surfaces.py", "configs/complete-e2e/runtime.json", "tests/regression/complete-e2e-prove-receipt.test.sh", "scripts/tidy/run.sh", "scripts/tidy/run.py", "scripts/enforce/run.sh", "scripts/enforce/run.py", "scripts/release-ready/run.sh", "scripts/release-ready/run.py"]
    for rel in required:
        if (ROOT / rel).is_file(): pass_("present " + rel)
        else: fail_("missing " + rel); rc = 1
    print("Layer 4 -- gitignore bytecode rules")
    gi_path = ROOT / ".gitignore"
    gi = gi_path.read_text(encoding="utf-8", errors="replace") if gi_path.is_file() else ""
    if "__pycache__" in gi or "*.pyc" in gi: pass_(".gitignore covers bytecode")
    elif do_fix:
        with gi_path.open("a", encoding="utf-8") as f: f.write("\\n# Python bytecode\\n__pycache__/\\n*.pyc\\n")
        info_("appended bytecode rules to .gitignore")
    else: fail_(".gitignore missing bytecode rules"); rc = 1
    print("Layer 5 -- policy scan (no ALLOW_UNPROVEN / fake CERTIFIED)")
    banned = []
    for path in sorted(scripts_root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in {".py", ".sh", ".md", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(ROOT))
        allow_a = "ALLOW_UNPROVEN" + "=1"
        allow_b = "ALLOW_UNPROVEN" + " = 1"
        if allow_a in text or allow_b in text:
            banned.append(rel + ": " + allow_a)
        cert_a = "CERTIFIED" + "=1"
        cert_b = "certified" + " = true"
        if cert_a in text or cert_b in text.lower():
            banned.append(rel + ": fake CERTIFIED enable")
    if not banned:
        pass_("no ALLOW_UNPROVEN/fake CERTIFIED enables in scripts")
    else:
        fail_("policy violations: " + "; ".join(banned[:5])); rc = 1
    print("Layer 6 -- tidy --full after enforce")

    tidy = ROOT / "scripts/tidy/run.sh"
    if tidy.is_file():
        r = subprocess.run(["bash", str(tidy)], cwd=str(ROOT))
        if r.returncode == 0: pass_("tidy --full")
        else: fail_("tidy --full"); rc = 1
    else: fail_("tidy missing"); rc = 1
    print("----------------------------------------")
    print("ENFORCE: PASS" if rc == 0 else "ENFORCE: FAIL")
    return rc
if __name__ == "__main__":
    raise SystemExit(main())
