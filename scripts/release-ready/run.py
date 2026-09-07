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
    print("Gate -- policy scan (no ALLOW_UNPROVEN / fake CERTIFIED)")
    banned = []
    for path in sorted((ROOT / "scripts").rglob("*")):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix not in {".py", ".sh", ".md", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(ROOT))
        # Comments stating the ban are OK; assignments / enables are not.
        # Build needles without embedding banned assignments as contiguous literals.
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
        fail_("policy violations: " + "; ".join(banned[:5]))
        ok = False
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
