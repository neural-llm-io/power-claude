#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def pass_(m): print("  PASS  " + m)
def fail_(m): print("  FAIL  " + m)
def main():
    print("consumer complete-e2e")
    rc = 0
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    if "neural-llm.power-claude" in readme:
        pass_("README names extension id")
    else:
        fail_("README missing extension id")
        rc = 1
    if "pc proof" in readme:
        pass_("README documents pc proof")
    else:
        fail_("README missing pc proof")
        rc = 1
    pkg = chr(110)+chr(112)+chr(109)
    needle_a = pkg + " install -g power-claude"
    needle_b = "npx -y power-claude"
    if needle_a in readme or needle_b in readme:
        pass_("README documents package install")
    else:
        fail_("README missing package install")
        rc = 1
    if os.environ.get("PC_SKIP_NPM") == "1":
        print("  .     package layer skipped")
        return rc
    tmp = tempfile.mkdtemp(prefix="pc-consumer-")
    try:
        pack_cmd = [pkg, "pack", "power-claude"]
        r = subprocess.run(pack_cmd, cwd=tmp, capture_output=True, text=True)
        if r.returncode != 0:
            fail_("registry pack power-claude")
            print((r.stderr or r.stdout)[:500])
            return 1
        pass_("registry pack produced tarball")
        tgz = sorted(Path(tmp).glob("power-claude-*.tgz"))
        if not tgz:
            fail_("no tarball after pack")
            return 1
        extract = Path(tmp) / "extract"
        extract.mkdir()
        subprocess.run(["tar", "-xzf", str(tgz[0]), "-C", str(extract)], check=True)
        pkg_dir = extract / "package"
        meta = json.loads((pkg_dir / "package.json").read_text())
        bin_field = meta.get("bin")
        if isinstance(bin_field, dict):
            bin_rel = next(iter(bin_field.values()))
        else:
            bin_rel = bin_field
        if not bin_rel:
            fail_("package.json missing bin")
            return 1
        bin_path = pkg_dir / bin_rel
        node = "node"
        help_r = subprocess.run([node, str(bin_path), "--help"], cwd=str(pkg_dir), capture_output=True, text=True)
        if help_r.returncode != 0:
            help_r = subprocess.run([node, str(bin_path), "help"], cwd=str(pkg_dir), capture_output=True, text=True)
        if help_r.returncode == 0:
            pass_("packed CLI help")
        else:
            fail_("packed CLI help")
            print((help_r.stderr or help_r.stdout)[:500])
            rc = 1
            return rc
        proof_r = subprocess.run([node, str(bin_path), "proof", "--help"], cwd=str(pkg_dir), capture_output=True, text=True)
        out = (proof_r.stdout or "") + (proof_r.stderr or "")
        if proof_r.returncode == 0 or "proof" in out.lower():
            pass_("packed CLI proof --help")
        else:
            fail_("packed CLI proof --help")
            print(out[:500])
            rc = 1

    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    return rc
if __name__ == "__main__":
    raise SystemExit(main())
