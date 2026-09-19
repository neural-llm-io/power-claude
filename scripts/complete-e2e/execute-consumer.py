#!/usr/bin/env python3
"""Live consumer execute adapter: runs consumer.py and emits execute receipt.

behavior_proven=true ONLY when ok=true after a real consumer execute (not inventory,
not skip-npm, not tautology). Named behavior.cases map PASS lines from consumer to
domain outcomes (subprocess CLI help, packed dual-bin --version, npm registry
metadata, marketplace API, marketplace vsix HEAD, marketplace license/details/icon
HEADs, open-vsx vsix download HEAD, open-vsx icon/license/readme/sha256 HEADs,
open-vsx sha256 body + packed icon size integrity, open-vsx downloadCount, open-vsx displayName+description+listing links/timestamp, packed extension.js+bin sha256, packed tarball sha1+file count vs registry, registry dist.integrity+unpackedSize, registry dist.fileCount, registry tarball URL+shasum, registry homepage+repository+engines.node+bugs/description/keywords, marketplace api displayName+install+dates, marketplace api shortDescription, marketplace listing pricing+product links, product/pricing site cross-links, packed prices.default planPricing+apiPricing+claimMapping+communityFallbacks, packed feature-matrix core+extra stamps, packed jq linux-amd64+all-platforms sha256, packed CLI proof/doctor/rotation/resume/emergency/onboard/recommend --help cluster, packed bin ships cli/proxy/rotator/stop-classifier, packed media/walkthrough core guides, packed description+keywords+LICENSE, packed engine.enc size floor, packed media/marketplace assets count, packed media/icon.png+out/extension.js size, packed files[] entries present, packed out/uninstall-hook.js size, packed media/icon.svg+icon-activity.svg+brand badge.svg/css/html size floors, packed package.json bin pc+power-claude paths, packed CLI emergency-on --help, packed prices.default pro/max_* monthly ladder + apiPricing cache rates, packed CLI halt+emergency-off --help, packed prices.default pro yearly 200, registry pack produced tarball).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RECEIPT_DIR = HERE / ".receipts"
RECEIPT_PATH = RECEIPT_DIR / "execute-receipt.json"
SCHEMA = "hurc-complete-e2e-power-claude-execute/v1"

# Domain cases already proven by consumer.py — each requires real PASS markers
# tied to subprocess / network outcomes (not assertTrue(true)).
CASE_MARKERS: dict[str, tuple[str, ...]] = {
    "packed_cli_help": (
        "PASS  packed CLI help",
        "PASS  packed CLI help lists consumer commands",
    ),
    # Packed CLI help cluster: proof/doctor/rotation/resume/emergency/onboard/recommend --help already proven by consumer.py.
    "packed_cli_help_cluster": (
        "PASS  packed CLI proof --help",
        "PASS  packed CLI doctor --help",
        "PASS  packed CLI rotation --help",
        "PASS  packed CLI resume --help",
        "PASS  packed CLI emergency --help",
        "PASS  packed CLI onboard --help",
        "PASS  packed CLI recommend --help",
    ),
    # Dual-bin packed consumer: pc + power-claude --version must both match package version.
    "packed_dual_bin_version": (
        "PASS  packed CLI --version matches ",
        "PASS  packed power-claude --version matches ",
    ),
    # Dual-bin packed paths: package.json bin has pc+power-claude + power-claude bin path present (NOT version identity).
    "packed_dual_bin_paths": (
        "PASS  package.json bin has pc + power-claude",
        "PASS  packed power-claude bin path present",
    ),
    # Packed CLI emergency-on --help already proven by consumer.py (exact PASS substring; NOT cluster emergency --help).
    "packed_cli_emergency_on_help": (
        "PASS  packed CLI emergency-on --help",
    ),
    # Packed CLI halt + emergency-off --help already proven by consumer.py (require BOTH; NOT cluster / NOT emergency-on).
    "packed_cli_halt_emergency_off_help": (
        "PASS  packed CLI halt --help",
        "PASS  packed CLI emergency-off --help",
    ),
    # Packed bin payload: cli/proxy/rotator/stop-classifier already proven by consumer.py.
    "packed_bin_payload": (
        "PASS  packed bin ships cli/proxy/rotator/stop-classifier",
    ),
    # Packed media/walkthrough core guides already proven by consumer.py.
    "packed_media_walkthrough": (
        "PASS  packed media/walkthrough core guides",
    ),
    # Packed pkg meta: description+keywords+LICENSE already proven by consumer.py (require ALL).
    # dual-bin already CASE (packed_dual_bin_version) — do not re-case.
    "packed_pkg_meta": (
        "PASS  packed description value prop",
        "PASS  packed keywords claude-code+vscode-extension",
        "PASS  packed LICENSE present with Neural-LLM",
    ),
    # Packed engine.enc present + size floor already proven by consumer.py (exact PASS substring).
    "packed_engine_enc": (
        "PASS  packed engine.enc ",
    ),
    # Packed media/marketplace assets count floor already proven by consumer.py (exact PASS substring).
    "packed_media_marketplace_assets": (
        "PASS  packed media/marketplace assets ",
    ),
    # Packed media/icon.png + out/extension.js size floors already proven by consumer.py (require BOTH).
    "packed_icon_extension_js": (
        "PASS  packed media/icon.png ",
        "PASS  packed out/extension.js ",
    ),
    # Packed package.json files[] entries present already proven by consumer.py (exact PASS substring).
    "packed_files_contract": (
        "PASS  packed files[] entries present ",
    ),
    # Packed out/uninstall-hook.js size floor already proven by consumer.py (exact PASS substring).
    "packed_uninstall_hook": (
        "PASS  packed out/uninstall-hook.js ",
    ),
    # Packed brand assets (icon.svg + icon-activity.svg + badge.svg/css/html) size floors already proven by consumer.py (require ALL).
    "packed_brand_assets": (
        "PASS  packed media/icon.svg ",
        "PASS  packed media/icon-activity.svg ",
        "PASS  packed media/brand/power-claude/badge.svg ",
        "PASS  packed media/brand/power-claude/badge.css ",
        "PASS  packed media/brand/power-claude/badge-template.html ",
    ),
    # Packed extension.js + bin sha256 already proven by consumer.py (require BOTH).
    "packed_artifact_sha256": (
        "PASS  packed extension.js sha256 matches",
        "PASS  packed bin sha256 matches",
    ),
    # Packed tarball sha1 + file count vs registry already proven by consumer.py (require BOTH).
    "packed_registry_integrity": (
        "PASS  packed tarball sha1 matches registry",
        "PASS  packed file count matches registry",
    ),
    # Packed prices.default contract already proven by consumer.py (plan ladder + api models + claims + 5x/20x).
    "packed_prices_contract": (
        "PASS  packed prices.default planPricing pro/max",
        "PASS  packed prices.default apiPricing models",
        "PASS  packed prices.default claimMapping periods",
        "PASS  packed prices.default communityFallbacks 5x/20x",
    ),
    # Packed prices.default monthly ladder (pro/max_*) + apiPricing cache rates already proven by consumer.py (require ALL; NOT packed_prices_contract).
    "packed_prices_ladder_cache": (
        "PASS  packed prices.default pro monthly 20",
        "PASS  packed prices.default max_5x monthly 100",
        "PASS  packed prices.default max_20x monthly 200",
        "PASS  packed prices.default apiPricing cache rates",
    ),
    # Packed prices.default pro yearly already proven by consumer.py (exact PASS substring; NOT packed_prices_contract / NOT packed_prices_ladder_cache).
    "packed_prices_pro_yearly": (
        "PASS  packed prices.default pro yearly 200",
    ),
    # Packed feature-matrix core+extra stamps already proven by consumer.py (require BOTH).
    "packed_feature_matrix_stamps": (
        "PASS  packed feature-matrix core stamps",
        "PASS  packed feature-matrix extra stamps",
    ),
    # Packed jq linux-amd64 entry + all-platforms sha256 already proven by consumer.py (require BOTH).
    "packed_jq_platform_sha": (
        "PASS  packed jq manifest linux-amd64 entry",
        "PASS  packed jq all platforms sha256 match",
    ),
    # Registry pack produced tarball already proven by consumer.py (exact PASS substring; NOT packed_registry_integrity / NOT registry_tarball_meta / NOT registry_dist_*).
    "registry_pack_produced_tarball": (
        "PASS  registry pack produced tarball",
    ),
    # Registry dist.integrity (sha512) + dist.unpackedSize already proven by consumer.py (require BOTH).
    "registry_dist_extras": (
        "PASS  registry dist.integrity sha512",
        "PASS  registry dist.unpackedSize ",
    ),
    # Registry dist.fileCount already proven by consumer.py (exact substring).
    "registry_dist_file_count": (
        "PASS  registry dist.fileCount ",
    ),
    "registry_metadata": (
        "PASS  registry metadata name/version/bin",
        "PASS  registry tarball HEAD",
    ),
    # Registry tarball URL + shasum already proven by consumer.py (require BOTH via combined PASS).
    "registry_tarball_meta": (
        "PASS  registry tarball URL+shasum ",
    ),
    # Registry listing meta already proven by consumer.py (homepage+repository+engines+bugs/desc/keywords).
    "registry_listing_meta": (
        "PASS  registry homepage ",
        "PASS  registry repository ",
        "PASS  registry engines.node ",
        "PASS  registry bugs URL",
        "PASS  registry bugs email ",
        "PASS  registry description value prop",
        "PASS  registry keywords claude-code+vscode-extension",
    ),
    "marketplace_api": (
        "PASS  marketplace api publisher/name",
        "PASS  marketplace listing body proves Power Claude",
    ),
    # Marketplace API listing meta already proven by consumer.py (displayName+install+dates).
    "marketplace_api_listing_meta": (
        "PASS  marketplace api displayName ",
        "PASS  marketplace api install ",
        "PASS  marketplace api lastUpdated ",
        "PASS  marketplace api publishedDate ",
    ),
    # Marketplace API shortDescription already proven by consumer.py (exact substring).
    "marketplace_api_short_description": (
        "PASS  marketplace api shortDescription",
    ),
    "marketplace_vsix_download": (
        "PASS  marketplace vsix HEAD",
    ),
    # Marketplace listing assets already proven by consumer.py (same gallery files loop).
    "marketplace_asset_heads": (
        "PASS  marketplace license HEAD",
        "PASS  marketplace details HEAD",
        "PASS  marketplace icon HEAD",
    ),
    # Marketplace listing page cross-links already proven by consumer.py (require BOTH).
    "marketplace_listing_links": (
        "PASS  marketplace listing links pricing",
        "PASS  marketplace listing links product",
    ),
    # Live customer surfaces already proven by consumer.py — require named cases.
    "open_vsx_vsix_download": (
        "PASS  open-vsx vsix download HEAD",
    ),
    # Open VSX listing assets already proven by consumer.py (files loop icon/license/readme/sha256).
    "open_vsx_asset_heads": (
        "PASS  open-vsx icon HEAD",
        "PASS  open-vsx license HEAD",
        "PASS  open-vsx readme HEAD",
        "PASS  open-vsx sha256 HEAD",
    ),
    # Open VSX sha256 body + packed icon size already proven by consumer.py (require BOTH).
    "open_vsx_icon_integrity": (
        "PASS  open-vsx sha256 body",
        "PASS  packed icon size matches open-vsx",
    ),
    # Open VSX downloadCount already proven by consumer.py (exact substring).
    "open_vsx_download_count": (
        "PASS  open-vsx downloadCount ",
    ),
    # Open VSX listing meta already proven by consumer.py (displayName+description+links/timestamp).
    "open_vsx_listing_meta": (
        "PASS  open-vsx displayName ",
        "PASS  open-vsx description",
        "PASS  open-vsx homepage ",
        "PASS  open-vsx repository ",
        "PASS  open-vsx bugs URL",
        "PASS  open-vsx timestamp ",
    ),
    "product_site_links": (
        "PASS  product site links pricing",
        "PASS  product site links marketplace",
        "PASS  product site links open-vsx",
    ),
    "pricing_page_links": (
        "PASS  pricing page links product",
        "PASS  pricing page links marketplace",
        "PASS  pricing page links open-vsx",
    ),
}

BLOCK_MARKERS = (
    "URLError",
    "HTTPError",
    "timed out",
    "Temporary failure in name resolution",
    "Network is unreachable",
    "Connection refused",
    "Name or service not known",
    "nodename nor servname",
    "getaddrinfo failed",
    "Failed to connect",
    "network is down",
    "Could not resolve host",
    "ENOTFOUND",
    "ECONNREFUSED",
    "ETIMEDOUT",
)


def _looks_blocked(blob: str) -> bool:
    low = blob.lower()
    for marker in BLOCK_MARKERS:
        if marker.lower() in low:
            return True
    return False


def _case_from_output(case_id: str, markers: tuple[str, ...], output: str) -> dict[str, Any]:
    missing = [m for m in markers if m not in output]
    if missing:
        return {
            "id": case_id,
            "ok": False,
            "detail": "missing markers: " + "; ".join(missing),
        }
    # Surface the last matching PASS line as detail (real consumer evidence).
    last = ""
    for line in output.splitlines():
        for m in markers:
            if m in line:
                last = line.strip()
    return {"id": case_id, "ok": True, "detail": last or markers[0]}


def _build_receipt(
    *,
    consumer_rc: int,
    output: str,
    skipped_npm: bool,
) -> dict[str, Any]:
    cases = [
        _case_from_output(cid, markers, output)
        for cid, markers in CASE_MARKERS.items()
    ]
    cases_ok = bool(cases) and all(c["ok"] for c in cases)
    consumer_ok = consumer_rc == 0
    blocked = (not consumer_ok or not cases_ok) and _looks_blocked(output)

    if skipped_npm:
        env_status = "partial_skip_npm"
        ok = False
        behavior_proven = False
    elif blocked:
        env_status = "BLOCKED_ENVIRONMENT"
        ok = False
        behavior_proven = False
    elif not consumer_ok or not cases_ok:
        env_status = "execute_failed"
        ok = False
        behavior_proven = False
    else:
        env_status = "live"
        ok = True
        # Real execute only: consumer exit 0 + named domain cases from PASS lines.
        behavior_proven = True

    return {
        "schema": SCHEMA,
        "ok": bool(ok),
        "environment_status": env_status,
        "blocked_environment": bool(blocked),
        "behavior_proven": bool(behavior_proven and ok),
        "executor": "scripts/complete-e2e/consumer.py",
        "consumer_returncode": consumer_rc,
        "behavior": {
            "status": "ok" if behavior_proven and ok else ("blocked" if blocked else "fail"),
            "cases": cases,
        },
    }


def _emit_receipt(receipt: dict[str, Any], out_path: Path | None) -> None:
    text = json.dumps(receipt, indent=2) + "\n"
    sys.stdout.write(text)
    sys.stdout.flush()
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(text, encoding="utf-8")
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")


def main() -> int:
    argv = sys.argv[1:]
    a = set(argv)
    if a & {"-h", "--help"}:
        print(
            "power-claude-execute-consumer: runs live consumer.py and emits execute "
            "receipt JSON (stdout + .receipts/); use --out PATH to also write a copy"
        )
        return 0
    if a & {"-V", "--version"}:
        print("power-claude-execute-consumer 1.0.0")
        return 0

    out_path: Path | None = None
    args = list(argv)
    if "--out" in args:
        i = args.index("--out")
        if i + 1 >= len(args):
            print("execute-consumer.py: --out requires a path", file=sys.stderr)
            return 2
        out_path = Path(args[i + 1])
        del args[i : i + 2]
    if args:
        print("usage: execute-consumer.py [--out PATH]", file=sys.stderr)
        return 2

    consumer = HERE / "consumer.py"
    if not consumer.is_file():
        print("execute-consumer: missing consumer.py", file=sys.stderr)
        return 2

    env = os.environ.copy()
    skipped_npm = env.get("PC_SKIP_NPM") == "1"

    print("power-claude complete-e2e (execute-consumer)", file=sys.stderr)
    print("----------------------------------------", file=sys.stderr)
    proc = subprocess.run(
        [sys.executable, str(consumer)],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    # Forward consumer streams to stderr so stdout stays receipt-only.
    if proc.stdout:
        sys.stderr.write(proc.stdout)
        if not proc.stdout.endswith("\n"):
            sys.stderr.write("\n")
    if proc.stderr:
        sys.stderr.write(proc.stderr)
        if not proc.stderr.endswith("\n"):
            sys.stderr.write("\n")

    receipt = _build_receipt(
        consumer_rc=proc.returncode,
        output=output,
        skipped_npm=skipped_npm,
    )
    print("----------------------------------------", file=sys.stderr)
    print(
        "EXECUTE: PASS" if receipt["ok"] and receipt["behavior_proven"] else "EXECUTE: FAIL",
        file=sys.stderr,
    )
    _emit_receipt(receipt, out_path)
    return 0 if (receipt.get("ok") is True and receipt.get("behavior_proven") is True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
