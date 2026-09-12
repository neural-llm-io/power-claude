#!/usr/bin/env python3
"""Fail-closed gate: runtime.json adapter argv script paths must exist.

Closes MISSING_PROVER for phantom runtime adapters — if an adapter argv target
(repo-relative .py/.sh/etc.) is missing on disk, exit non-zero with
error=MISSING_PROVER. Never attests behavior_proven (path occupancy only).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUNTIME = ROOT / "configs/complete-e2e/runtime.json"
SCHEMA = "hurc-complete-e2e-power-claude-adapter-paths/v1"

NON_PATH_TOKENS = {
    "python",
    "python3",
    "python3.11",
    "python3.12",
    "bash",
    "sh",
    "dash",
    "zsh",
    "node",
    "nodejs",
    "deno",
    "bun",
    "env",
    "/usr/bin/env",
    "/bin/sh",
    "/bin/bash",
}


def _is_pathish(token: str) -> bool:
    if not token or token.startswith("-"):
        return False
    if token in NON_PATH_TOKENS:
        return False
    if "/" in token or token.endswith((".py", ".sh", ".js", ".mjs", ".ts", ".json")):
        return True
    return False


def check_runtime(root: Path, runtime_path: Path) -> dict[str, Any]:
    if not runtime_path.is_file():
        return {
            "schema": SCHEMA,
            "ok": False,
            "error": "MISSING_PROVER",
            "detail": f"runtime missing: {runtime_path}",
            "behavior_proven": False,
            "adapters_checked": 0,
            "targets_checked": 0,
            "missing": [str(runtime_path)],
        }
    try:
        data = json.loads(runtime_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return {
            "schema": SCHEMA,
            "ok": False,
            "error": "MISSING_PROVER",
            "detail": f"runtime unreadable/invalid: {e}",
            "behavior_proven": False,
            "adapters_checked": 0,
            "targets_checked": 0,
            "missing": [],
        }

    adapters = data.get("adapters")
    if not isinstance(adapters, list) or not adapters:
        return {
            "schema": SCHEMA,
            "ok": False,
            "error": "MISSING_PROVER",
            "detail": "runtime.adapters empty or missing",
            "behavior_proven": False,
            "adapters_checked": 0,
            "targets_checked": 0,
            "missing": [],
        }

    missing: list[str] = []
    targets = 0
    for a in adapters:
        if not isinstance(a, dict):
            missing.append("non-object adapter entry")
            continue
        aid = str(a.get("id") or "<unknown>")
        argv = a.get("argv")
        if not isinstance(argv, list) or not argv:
            missing.append(f"{aid}: empty argv")
            continue
        path_tokens = [t for t in argv if isinstance(t, str) and _is_pathish(t)]
        if not path_tokens:
            missing.append(f"{aid}: no path-like argv target")
            continue
        for tok in path_tokens:
            targets += 1
            cand = Path(tok) if Path(tok).is_absolute() else (root / tok)
            if not cand.is_file():
                missing.append(f"{aid}: argv target missing: {tok}")

    if missing:
        return {
            "schema": SCHEMA,
            "ok": False,
            "error": "MISSING_PROVER",
            "detail": "; ".join(missing),
            "behavior_proven": False,
            "adapters_checked": len(adapters),
            "targets_checked": targets,
            "missing": missing,
        }

    return {
        "schema": SCHEMA,
        "ok": True,
        "error": None,
        "detail": (
            f"all adapter argv script paths present "
            f"({targets} targets, {len(adapters)} adapters)"
        ),
        # Path occupancy is not a live behavior prove — never greenwash.
        "behavior_proven": False,
        "adapters_checked": len(adapters),
        "targets_checked": targets,
        "missing": [],
    }


def main() -> int:
    argv = sys.argv[1:]
    a = set(argv)
    if a & {"-h", "--help"}:
        print(
            "power-claude-check-adapter-paths: fail-closed runtime.json argv "
            "path existence gate (MISSING_PROVER if target missing); "
            "use --runtime PATH to point at an alternate runtime.json"
        )
        return 0
    if a & {"-V", "--version"}:
        print("power-claude-check-adapter-paths 1.0.0")
        return 0

    runtime_path = DEFAULT_RUNTIME
    args = list(argv)
    if "--runtime" in args:
        i = args.index("--runtime")
        if i + 1 >= len(args):
            print("check-adapter-paths.py: --runtime requires a path", file=sys.stderr)
            return 2
        runtime_path = Path(args[i + 1])
        if not runtime_path.is_absolute():
            runtime_path = (Path.cwd() / runtime_path).resolve()
        del args[i : i + 2]
    if args:
        print("usage: check-adapter-paths.py [--runtime PATH]", file=sys.stderr)
        return 2

    print("power-claude complete-e2e (check-adapter-paths)", file=sys.stderr)
    print("----------------------------------------", file=sys.stderr)
    result = check_runtime(ROOT, runtime_path)
    # stdout = machine receipt; stderr = human progress
    sys.stdout.write(json.dumps(result, indent=2) + "\n")
    sys.stdout.flush()
    if result.get("ok") is True:
        print(f"  PASS  adapter paths: {result.get('detail')}", file=sys.stderr)
        print("ADAPTER_PATHS: PASS", file=sys.stderr)
        # Gate green for path occupancy, but never claim behavior_proven.
        return 0
    detail = result.get("detail") or "MISSING_PROVER"
    print(f"  FAIL  MISSING_PROVER: {detail}", file=sys.stderr)
    print("ADAPTER_PATHS: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
