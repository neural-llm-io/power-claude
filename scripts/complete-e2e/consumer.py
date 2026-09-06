#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re, subprocess, tempfile, urllib.error, urllib.request
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
    if "install-extension neural-llm.power-claude" in readme:
        pass_("README documents install-extension")
    else:
        fail_("README missing install-extension")
        rc = 1
    if "neural-llm.com/pricing" in readme:
        pass_("README documents pricing")
    else:
        fail_("README missing pricing")
        rc = 1
    lic = (ROOT / "LICENSE").read_text(encoding="utf-8", errors="replace")
    if len(lic.strip()) > 100 and "Neural-LLM" in lic:
        pass_("LICENSE present with Neural-LLM")
    else:
        fail_("LICENSE missing/invalid")
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
        for cmd in ("halt", "doctor", "emergency-off"):
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
        # npm registry metadata identity (consumer install surface)
        try:
            reg_url = "https://registry.npmjs.org/power-claude/latest"
            rreq = urllib.request.Request(reg_url, headers={"User-Agent": "power-claude-consumer-e2e", "Accept": "application/json"})
            with urllib.request.urlopen(rreq, timeout=45) as rresp:
                rraw = rresp.read(500000)
                rcode = getattr(rresp, "status", 200)
            if not (200 <= int(rcode) < 400):
                fail_("registry metadata HTTP " + str(rcode))
                rc = 1
            else:
                rdata = json.loads(rraw.decode("utf-8", errors="replace"))
                rver = str(rdata.get("version") or "")
                if rdata.get("name") != "power-claude":
                    fail_("registry metadata unexpected name")
                    rc = 1
                elif rver != ver:
                    fail_("registry metadata version " + rver + " != packed " + ver)
                    rc = 1
                else:
                    lbin = rdata.get("bin") or {}
                    if not (isinstance(lbin, dict) and "pc" in lbin and "power-claude" in lbin):
                        fail_("registry metadata missing pc/power-claude bin")
                        rc = 1
                    else:
                        pass_("registry metadata name/version/bin " + rver)
                        dist = rdata.get("dist") or {}
                        tb = str(dist.get("tarball") or "")
                        want = "power-claude-" + rver + ".tgz"
                        shasum = str(dist.get("shasum") or "")
                        if want not in tb:
                            fail_("registry tarball URL missing " + want)
                            rc = 1
                        elif len(shasum) != 40:
                            fail_("registry dist.shasum unexpected")
                            rc = 1
                        else:
                            pass_("registry tarball URL+shasum " + rver)
                            try:
                                treq = urllib.request.Request(tb, method="HEAD", headers={"User-Agent": "power-claude-consumer-e2e"})
                                with urllib.request.urlopen(treq, timeout=45) as tresp:
                                    tcode = getattr(tresp, "status", 200)
                                if 200 <= int(tcode) < 400:
                                    pass_("registry tarball HEAD " + str(tcode))
                                else:
                                    fail_("registry tarball HEAD HTTP " + str(tcode))
                                    rc = 1
                            except Exception as te:
                                fail_("registry tarball HEAD " + type(te).__name__)
                                print(str(te)[:300])
                                rc = 1
                            integrity = str(dist.get("integrity") or "")
                            fcount = dist.get("fileCount")
                            if integrity.startswith("sha512-") and len(integrity) > 20:
                                pass_("registry dist.integrity sha512")
                            else:
                                fail_("registry dist.integrity missing/unexpected")
                                rc = 1
                            if isinstance(fcount, int) and fcount > 0:
                                pass_("registry dist.fileCount " + str(fcount))
                            else:
                                fail_("registry dist.fileCount unexpected")
                                rc = 1
                            usize = dist.get("unpackedSize")
                            if isinstance(usize, int) and usize > 1000:
                                pass_("registry dist.unpackedSize " + str(usize))
                            else:
                                fail_("registry dist.unpackedSize unexpected")
                                rc = 1
                            packed_sha = hashlib.sha1(tgz[0].read_bytes()).hexdigest()
                            if packed_sha == shasum:
                                pass_("packed tarball sha1 matches registry")
                            else:
                                fail_("packed tarball sha1 != registry shasum")
                                print("packed=" + packed_sha + " registry=" + shasum)
                                rc = 1
                            packed_files = sum(1 for x in pkg_dir.rglob("*") if x.is_file())
                            if isinstance(fcount, int) and packed_files == fcount:
                                pass_("packed file count matches registry " + str(fcount))
                            else:
                                fail_("packed file count " + str(packed_files) + " != registry " + str(fcount))
                                rc = 1
        except Exception as e:
            fail_("registry metadata " + type(e).__name__)
            print(str(e)[:300])
            rc = 1

        # Public mirror CHANGELOG should not be ahead of published package.
        cl = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8", errors="replace")
        heads = re.findall(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]", cl, flags=re.M)
        if not heads:
            fail_("CHANGELOG missing version headings")
            rc = 1
        else:
            head = heads[0]
            def tup(v):
                return tuple(int(x) for x in v.split("."))
            if tup(head) <= tup(ver):
                pass_("CHANGELOG head " + head + " <= published " + ver)
            else:
                fail_("CHANGELOG head " + head + " ahead of published " + ver)
                rc = 1
        # VS Marketplace gallery API identity (consumer install surface)
        try:
            mq = {
                "filters": [{"criteria": [{"filterType": 7, "value": "neural-llm.power-claude"}], "pageNumber": 1, "pageSize": 1}],
                "flags": 914,
            }
            mreq = urllib.request.Request(
                "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1",
                data=json.dumps(mq).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json;api-version=7.1-preview.1",
                    "User-Agent": "power-claude-consumer-e2e",
                },
                method="POST",
            )
            with urllib.request.urlopen(mreq, timeout=45) as resp:
                mraw = resp.read(500000)
                mcode = getattr(resp, "status", 200)
            if not (200 <= int(mcode) < 400):
                fail_("marketplace api HTTP " + str(mcode))
                rc = 1
            else:
                mdata = json.loads(mraw.decode("utf-8", errors="replace"))
                exts = ((mdata.get("results") or [{}])[0].get("extensions") or [])
                if not exts:
                    fail_("marketplace api empty extensions")
                    rc = 1
                else:
                    e0 = exts[0]
                    pub = (e0.get("publisher") or {}).get("publisherName")
                    name = e0.get("extensionName")
                    ver0 = ((e0.get("versions") or [{}])[0].get("version")) if e0.get("versions") else None
                    if pub != "neural-llm" or name != "power-claude":
                        fail_("marketplace api unexpected identity")
                        rc = 1
                    else:
                        pass_("marketplace api publisher/name " + str(ver0 or ""))
                        disp = str(e0.get("displayName") or "").strip()
                        sdesc = str(e0.get("shortDescription") or "").strip()
                        if disp:
                            pass_("marketplace api displayName " + disp[:40])
                        else:
                            fail_("marketplace api missing displayName")
                            rc = 1
                        if len(sdesc) > 10:
                            pass_("marketplace api shortDescription")
                        else:
                            fail_("marketplace api shortDescription missing/short")
                            rc = 1
                        stats = e0.get("statistics") or []
                        install = next((s.get("value") for s in stats if s.get("statisticName") == "install"), None)
                        if isinstance(install, (int, float)) and install >= 0:
                            pass_("marketplace api install " + str(int(install)))
                        else:
                            fail_("marketplace api install statistic missing")
                            rc = 1
                        files = (e0.get("versions") or [{}])[0].get("files") or []
                        vsix = [f for f in files if f.get("assetType") == "Microsoft.VisualStudio.Services.VSIXPackage"]
                        if not vsix or not vsix[0].get("source"):
                            fail_("marketplace api missing VSIXPackage")
                            rc = 1
                        else:
                            src = vsix[0]["source"]
                            try:
                                vreq = urllib.request.Request(src, method="HEAD", headers={"User-Agent": "power-claude-consumer-e2e"})
                                with urllib.request.urlopen(vreq, timeout=60) as vresp:
                                    vcode = getattr(vresp, "status", 200)
                                    clen = vresp.headers.get("Content-Length")
                                if 200 <= int(vcode) < 400 and clen and int(clen) > 1000:
                                    pass_("marketplace vsix HEAD " + str(clen))
                                else:
                                    fail_("marketplace vsix HEAD")
                                    rc = 1
                            except Exception as ve:
                                fail_("marketplace vsix HEAD " + type(ve).__name__)
                                print(str(ve)[:300])
                                rc = 1
                            for asset_type, label in (
                                ("Microsoft.VisualStudio.Services.Content.License", "license"),
                                ("Microsoft.VisualStudio.Services.Content.Details", "details"),
                                ("Microsoft.VisualStudio.Services.Icons.Default", "icon"),
                            ):
                                hits = [f for f in files if f.get("assetType") == asset_type]
                                if not hits or not hits[0].get("source"):
                                    fail_("marketplace missing " + label)
                                    rc = 1
                                    continue
                                try:
                                    areq = urllib.request.Request(hits[0]["source"], method="HEAD", headers={"User-Agent": "power-claude-consumer-e2e"})
                                    with urllib.request.urlopen(areq, timeout=60) as aresp:
                                        acode = getattr(aresp, "status", 200)
                                    if 200 <= int(acode) < 400:
                                        pass_("marketplace " + label + " HEAD " + str(acode))
                                    else:
                                        fail_("marketplace " + label + " HEAD")
                                        rc = 1
                                except Exception as ae:
                                    fail_("marketplace " + label + " HEAD " + type(ae).__name__)
                                    print(str(ae)[:300])
                                    rc = 1
        except Exception as e:
            fail_("marketplace api " + type(e).__name__)
            print(str(e)[:300])
            rc = 1

        # Marketplace + Open VSX listing reachability (consumer install surfaces)
        urls = [
            ("marketplace listing", "https://marketplace.visualstudio.com/items?itemName=neural-llm.power-claude", "html"),
            ("open-vsx api", "https://open-vsx.org/api/neural-llm/power-claude", "openvsx"),
            ("product site", "https://neural-llm.com/power-claude", "html"),
            ("pricing page", "https://neural-llm.com/pricing", "html"),
        ]
        for label, murl, kind in urls:
            try:
                req = urllib.request.Request(murl, headers={"User-Agent": "power-claude-consumer-e2e", "Accept": "application/json, text/html, */*"})
                with urllib.request.urlopen(req, timeout=45) as resp:
                    code = getattr(resp, "status", 200)
                    raw = resp.read(500000)
                if not (200 <= int(code) < 400):
                    fail_(label + " HTTP " + str(code))
                    rc = 1
                    continue
                if kind == "openvsx":
                    data = json.loads(raw.decode("utf-8", errors="replace"))
                    if data.get("namespace") != "neural-llm" or data.get("name") != "power-claude":
                        fail_(label + " unexpected identity")
                        rc = 1
                    else:
                        pass_(label + " namespace/name " + str(data.get("version", "")))
                        odisp = str(data.get("displayName") or "").strip()
                        odesc = str(data.get("description") or "").strip()
                        if odisp:
                            pass_("open-vsx displayName " + odisp[:40])
                        else:
                            fail_("open-vsx missing displayName")
                            rc = 1
                        if len(odesc) > 10:
                            pass_("open-vsx description")
                        else:
                            fail_("open-vsx description missing/short")
                            rc = 1
                        dlc = data.get("downloadCount")
                        if isinstance(dlc, int) and dlc >= 0:
                            pass_("open-vsx downloadCount " + str(dlc))
                        else:
                            fail_("open-vsx downloadCount unexpected")
                            rc = 1
                        home = str(data.get("homepage") or "")
                        if "neural-llm.com/power-claude" in home:
                            pass_("open-vsx homepage " + home)
                        else:
                            fail_("open-vsx homepage unexpected")
                            rc = 1
                        dl = ((data.get("files") or {}).get("download"))
                        if not dl:
                            fail_("open-vsx missing download")
                            rc = 1
                        else:
                            dreq = urllib.request.Request(dl, method="HEAD", headers={"User-Agent": "power-claude-consumer-e2e"})
                            with urllib.request.urlopen(dreq, timeout=45) as dresp:
                                dcode = getattr(dresp, "status", 200)
                                clen = dresp.headers.get("Content-Length")
                            if 200 <= int(dcode) < 400 and clen and int(clen) > 1000:
                                pass_("open-vsx vsix download HEAD " + str(clen))
                            else:
                                fail_("open-vsx vsix download HEAD")
                                rc = 1
                            for asset, min_len in (("icon", 100), ("license", 100), ("readme", 100), ("sha256", 32)):
                                aurl = (data.get("files") or {}).get(asset)
                                if not aurl:
                                    fail_("open-vsx missing " + asset)
                                    rc = 1
                                    continue
                                try:
                                    areq = urllib.request.Request(aurl, method="HEAD", headers={"User-Agent": "power-claude-consumer-e2e"})
                                    with urllib.request.urlopen(areq, timeout=45) as aresp:
                                        acode = getattr(aresp, "status", 200)
                                        alen = aresp.headers.get("Content-Length")
                                    if 200 <= int(acode) < 400 and alen and int(alen) >= min_len:
                                        pass_("open-vsx " + asset + " HEAD " + str(alen))
                                    else:
                                        fail_("open-vsx " + asset + " HEAD")
                                        rc = 1
                                except Exception as ae:
                                    fail_("open-vsx " + asset + " HEAD " + type(ae).__name__)
                                    print(str(ae)[:300])
                                    rc = 1
                            sha_url = (data.get("files") or {}).get("sha256")
                            if sha_url:
                                try:
                                    sreq = urllib.request.Request(sha_url, headers={"User-Agent": "power-claude-consumer-e2e"})
                                    with urllib.request.urlopen(sreq, timeout=45) as sresp:
                                        sbody = sresp.read(200).decode("utf-8", errors="replace").strip()
                                    if re.fullmatch(r"[a-fA-F0-9]{64}", sbody):
                                        pass_("open-vsx sha256 body " + sbody[:12])
                                    else:
                                        fail_("open-vsx sha256 body unexpected")
                                        rc = 1
                                except Exception as se:
                                    fail_("open-vsx sha256 body " + type(se).__name__)
                                    print(str(se)[:300])
                                    rc = 1
                else:
                    body = raw.decode("utf-8", errors="replace")
                    needle = ("Power Claude" in body) or ("power-claude" in body) or ("neural-llm.power-claude" in body)
                    if needle:
                        pass_(label + " body proves Power Claude")
                    else:
                        fail_(label + " body missing Power Claude")
                        rc = 1
                    if label == "product site":
                        if "/pricing" in body:
                            pass_("product site links pricing")
                        else:
                            fail_("product site missing /pricing link")
                            rc = 1
                    if label == "pricing page":
                        if "/power-claude" in body:
                            pass_("pricing page links product")
                        else:
                            fail_("pricing page missing /power-claude link")
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
