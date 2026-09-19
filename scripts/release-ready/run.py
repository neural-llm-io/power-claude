#!/usr/bin/env python3
"""release-ready gate for public power-claude mirror."""
# Never ALLOW_UNPROVEN. Never fake CERTIFIED.
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
import tempfile
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
    env.pop("PC_SKIP_NPM", None)
    cmd = ["bash", str(path)] + (extra_args or [])
    r = subprocess.run(cmd, cwd=str(ROOT), env=env)
    if r.returncode == 0:
        pass_(label)
        return True
    fail_(label)
    return False

def refuse_skip_flags() -> bool:
    """Fail closed if skip / unproven bypass flags are present."""
    print("Gate -- refuse skip / unproven bypass flags")
    bad = []
    skip_key = "PC_SKIP_NPM"
    allow_key = "ALLOW_UNPROVEN"
    if os.environ.get(skip_key) == "1":
        bad.append(skip_key + "=1")
    if os.environ.get(allow_key) == "1":
        bad.append(allow_key + "=1")
    argv = set(sys.argv[1:])
    for flag in (
        "--skip-npm",
        "--skip",
        "--allow-unproven",
        skip_key + "=1",
        allow_key + "=1",
    ):
        if flag in argv:
            bad.append("argv:" + flag)
    if bad:
        fail_("refused skip/bypass: " + ", ".join(bad))
        return False
    pass_("no " + skip_key + " / " + allow_key + " / --skip* bypass")
    return True

def run_prove_receipt() -> bool:
    """Invoke prove --receipt; fail unless ok==true and behavior_proven==true."""
    print("Gate -- prove --receipt (ok + behavior_proven)")
    prove = ROOT / "scripts/complete-e2e/prove.py"
    if not prove.is_file():
        fail_("prove.py missing")
        return False
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Never greenwash a partial prove under release-ready.
    env.pop("PC_SKIP_NPM", None)
    env.pop("ALLOW_UNPROVEN", None)
    with tempfile.TemporaryDirectory(prefix="pc-rr-prove-") as td:
        out = Path(td) / "receipt.json"
        r = subprocess.run(
            [sys.executable, str(prove), "--receipt", "--out", str(out)],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
        )
        if r.stderr:
            sys.stderr.write(r.stderr)
            if not r.stderr.endswith("\n"):
                sys.stderr.write("\n")
        receipt = None
        if out.is_file():
            try:
                receipt = json.loads(out.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                fail_("prove receipt JSON invalid: " + str(e))
                return False
        if receipt is None:
            # Fallback: parse stdout JSON (prove emits receipt on stdout).
            try:
                receipt = json.loads((r.stdout or "").strip() or "{}")
            except json.JSONDecodeError:
                fail_("prove --receipt produced no parseable receipt")
                return False
        ok = receipt.get("ok")
        proven = receipt.get("behavior_proven")
        if ok is not True or proven is not True:
            fail_(
                "prove receipt ok!=true or behavior_proven!=true "
                "(ok={!r} behavior_proven={!r} env={!r})".format(
                    ok, proven, receipt.get("environment_status")
                )
            )
            return False
        if r.returncode != 0:
            fail_("prove --receipt exited " + str(r.returncode) + " despite ok receipt")
            return False
        pass_("prove --receipt ok=true behavior_proven=true")
        return True

def main() -> int:
    print("power-claude release-ready")
    print("----------------------------------------")
    print("Policy: never ALLOW_UNPROVEN; never fake CERTIFIED")
    purge_bytecode()
    ok = True
    if not refuse_skip_flags():
        # Fail closed immediately — do not clear skip and greenwash later gates.
        print("----------------------------------------")
        print("RELEASE_READY: FAIL")
        return 1
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
    # Fail-closed attestation: release-ready must not greenwash without prove receipt.
    if not run_prove_receipt():
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
