#!/usr/bin/env python3
"""tidy --full floor for public power-claude mirror."""
from __future__ import annotations
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Generated prove/execute receipts (never product source).
RECEIPT_DIR_NAMES = (".receipts",)
KNOWN_RECEIPT_NAMES = (
    "prove-receipt.json",
    "execute-receipt.json",
    # Browser DOM prove receipts (#101/#103/#104) — same leftover class as
    # prove/execute; catch drops outside .receipts/ and git-tracked basenames.
    "browser-product-prove-receipt.json",
    "browser-pricing-prove-receipt.json",
    "browser-openvsx-prove-receipt.json",
)


def pass_(m): print("  PASS  " + m, flush=True)
def fail_(m): print("  FAIL  " + m, flush=True)
def info_(m): print("  FIX   " + m, flush=True)


def _skip_git(p: Path) -> bool:
    return ".git" in p.parts


def _find_bytecode() -> list[Path]:
    junk: list[Path] = []
    for p in ROOT.rglob("*"):
        if _skip_git(p):
            continue
        if p.name == "__pycache__" or p.suffix == ".pyc":
            junk.append(p)
    return junk


def _iter_receipt_dirs() -> list[Path]:
    dirs: list[Path] = []
    for p in ROOT.rglob("*"):
        if _skip_git(p):
            continue
        if p.is_dir() and p.name in RECEIPT_DIR_NAMES:
            dirs.append(p)
    # Canonical location even if empty/missing (for gitignore messaging).
    canonical = ROOT / "scripts" / "complete-e2e" / ".receipts"
    if canonical not in dirs and canonical.is_dir():
        dirs.append(canonical)
    return dirs


def _find_leftover_receipts() -> list[Path]:
    found: list[Path] = []
    for d in _iter_receipt_dirs():
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file():
                found.append(p)
    # Also catch known receipt filenames dropped outside .receipts/.
    for name in KNOWN_RECEIPT_NAMES:
        for p in ROOT.rglob(name):
            if _skip_git(p):
                continue
            if p.is_file() and p not in found:
                found.append(p)
    return found


def _git_tracked_receipts() -> list[str]:
    """Return paths git tracks under .receipts or known receipt names."""
    try:
        r = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=str(ROOT),
            capture_output=True,
            check=False,
        )
    except OSError:
        return []
    if r.returncode != 0:
        return []
    tracked: list[str] = []
    for raw in (r.stdout or b"").split(b"\0"):
        if not raw:
            continue
        rel = raw.decode("utf-8", errors="replace")
        parts = Path(rel).parts
        base = Path(rel).name
        if ".receipts" in parts or base in KNOWN_RECEIPT_NAMES:
            tracked.append(rel)
    return tracked


def _remove_path(p: Path) -> None:
    if p.is_dir():
        shutil.rmtree(p, ignore_errors=True)
    elif p.exists():
        p.unlink(missing_ok=True)


def main() -> int:
    do_full = "--full" in sys.argv
    print("power-claude tidy" + (" --full" if do_full else ""))
    print("----------------------------------------")
    rc = 0

    print("Layer 1 -- no bytecode junk")
    junk = _find_bytecode()
    if not junk:
        pass_("no __pycache__/.pyc")
    elif do_full:
        for p in junk:
            rel = str(p.relative_to(ROOT))
            _remove_path(p)
            info_("removed " + rel)
        leftover = _find_bytecode()
        if not leftover:
            pass_("bytecode purged")
        else:
            fail_(
                "bytecode remain: "
                + ", ".join(str(x.relative_to(ROOT)) for x in leftover[:8])
            )
            rc = 1
    else:
        fail_(
            "bytecode: "
            + ", ".join(str(x.relative_to(ROOT)) for x in junk[:8])
        )
        rc = 1

    print("Layer 2 -- no leftover prove/execute receipts")
    receipts = _find_leftover_receipts()
    if not receipts:
        pass_("no leftover .receipts/*.json")
    elif do_full:
        for p in receipts:
            rel = str(p.relative_to(ROOT))
            _remove_path(p)
            info_("removed " + rel)
        # Remove empty .receipts dirs after file purge.
        for d in _iter_receipt_dirs():
            if d.is_dir() and not any(d.iterdir()):
                _remove_path(d)
                info_("removed empty " + str(d.relative_to(ROOT)))
        leftover = _find_leftover_receipts()
        if not leftover:
            pass_("leftover receipts purged")
        else:
            fail_(
                "receipts remain: "
                + ", ".join(str(x.relative_to(ROOT)) for x in leftover[:8])
            )
            rc = 1
    else:
        fail_(
            "leftover receipts: "
            + ", ".join(str(x.relative_to(ROOT)) for x in receipts[:8])
        )
        rc = 1

    print("Layer 3 -- git must not track .receipts")
    tracked = _git_tracked_receipts()
    if not tracked:
        pass_("no tracked .receipts / receipt files")
    else:
        fail_("git tracks receipts: " + ", ".join(tracked[:8]))
        rc = 1

    print("Layer 4 -- scripts compile + shebang")
    scripts_root = ROOT / "scripts"
    py_files = sorted(scripts_root.rglob("*.py")) if scripts_root.is_dir() else []
    sh_files = sorted(scripts_root.rglob("*.sh")) if scripts_root.is_dir() else []
    for py in py_files:
        if "__pycache__" in py.parts:
            continue
        try:
            py_compile.compile(str(py), doraise=True)
            pass_("compile " + str(py.relative_to(ROOT)))
        except Exception as e:
            fail_("compile " + str(py.relative_to(ROOT)) + ": " + str(e))
            rc = 1
    for sh in sh_files:
        text = sh.read_text(encoding="utf-8", errors="replace")
        if text.startswith("#!"):
            pass_("shebang " + str(sh.relative_to(ROOT)))
        else:
            fail_("missing shebang " + str(sh.relative_to(ROOT)))
            rc = 1

    print("Layer 5 -- gitignore covers bytecode + .receipts")
    gi_path = ROOT / ".gitignore"
    gi = gi_path.read_text(encoding="utf-8", errors="replace") if gi_path.is_file() else ""
    bc_ok = "__pycache__" in gi or "*.pyc" in gi
    # Accept either scoped or generic .receipts ignore.
    rcpt_ok = ".receipts/" in gi or ".receipts" in gi
    if bc_ok and rcpt_ok:
        pass_(".gitignore covers bytecode + .receipts")
    else:
        missing = []
        if not bc_ok:
            missing.append("__pycache__/*.pyc")
        if not rcpt_ok:
            missing.append(".receipts/")
        fail_(".gitignore missing " + ", ".join(missing))
        rc = 1

    print("----------------------------------------")
    print("TIDY: PASS" if rc == 0 else "TIDY: FAIL")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
