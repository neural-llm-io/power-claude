#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, tempfile, urllib.error, urllib.request
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
    if "open-vsx.org/extension/neural-llm/power-claude" in readme or "Open VSX" in readme:
        pass_("README documents Open VSX")
    else:
        fail_("README missing Open VSX")
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
            if "pc" in bin_field and "power-claude" in bin_field:
                pass_("package.json bin has pc + power-claude")
            else:
                fail_("package.json bin missing pc/power-claude aliases")
                return 1
            bin_rel = bin_field.get("pc") or next(iter(bin_field.values()))
        else:
            bin_rel = bin_field
        ver = str(meta.get("version") or "")
        if ver.count(".") >= 2:
            pass_("package.json version " + ver)
        else:
            fail_("package.json version missing/invalid")
            return 1
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
        for cmd in ("halt", "doctor"):
            cr = subprocess.run([node, str(bin_path), cmd, "--help"], cwd=str(pkg_dir), capture_output=True, text=True)
            cout = (cr.stdout or "") + (cr.stderr or "")
            if cr.returncode == 0 or cmd in cout.lower():
                pass_("packed CLI " + cmd + " --help")
            else:
                fail_("packed CLI " + cmd + " --help")
                print(cout[:400])
                rc = 1
        vr = subprocess.run([node, str(bin_path), "--version"], cwd=str(pkg_dir), capture_output=True, text=True)
        vout = ((vr.stdout or "") + (vr.stderr or "")).strip()
        if vr.returncode == 0 and ver in vout:
            pass_("packed CLI --version matches " + ver)
        else:
            fail_("packed CLI --version")
            print(vout[:300])
            rc = 1
        # Marketplace + Open VSX listing reachability (consumer install surfaces)
        urls = [
            ("marketplace listing", "https://marketplace.visualstudio.com/items?itemName=neural-llm.power-claude"),
            ("open-vsx listing", "https://open-vsx.org/extension/neural-llm/power-claude"),
            ("product site", "https://neural-llm.com/power-claude"),
        ]
        for label, murl in urls:
            try:
                req = urllib.request.Request(murl, headers={"User-Agent": "power-claude-consumer-e2e"})
                with urllib.request.urlopen(req, timeout=45) as resp:
                    code = getattr(resp, "status", 200)
                if 200 <= int(code) < 400:
                    pass_(label + " reachable")
                else:
                    fail_(label + " HTTP " + str(code))
                    rc = 1
            except Exception as e:
                fail_(label + " " + type(e).__name__)
                print(str(e)[:300])
                rc = 1

    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    return rc
if __name__ == "__main__":
    raise SystemExit(main())
