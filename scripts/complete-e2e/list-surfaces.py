#!/usr/bin/env python3
"""Inventory-only surface listing for complete-e2e runtime.

Fail-closed attestation guard: this adapter MUST NEVER set behavior_proven true.
Inventory listing is not a prove path — only execute/prove adapters may attest.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

CANDIDATES = (
    ("cli:complete-e2e", "scripts/complete-e2e/run.py"),
    ("cli:consumer", "scripts/complete-e2e/consumer.py"),
    ("cli:execute-consumer", "scripts/complete-e2e/execute-consumer.py"),
    ("cli:verify", "scripts/verify/run.py"),
    ("cli:prove", "scripts/complete-e2e/prove.py"),
    ("cli:clean-room-replay", "scripts/complete-e2e/clean-room-replay.py"),
)


def _surfaces(root: Path):
    out = []
    for sid, rel in CANDIDATES:
        if (root / rel).is_file():
            out.append({"id": sid, "kind": "cli", "path": rel, "origin": "runtime"})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="usage: list-surfaces.py [--project-dir PATH]")
    ap.add_argument("--project-dir", default="")
    args = ap.parse_args()
    root = Path(args.project_dir).resolve() if args.project_dir else Path(__file__).resolve().parents[2]
    if not root.is_dir():
        print("list-surfaces: project-dir not a directory", file=sys.stderr)
        return 2
    # Explicit false: inventory must not self-attest (omit would also be ok; force false is
    # fail-closed and machine-checkable by complete-e2e-list-surfaces-no-attest regression).
    payload = {
        "schema": "hurc-complete-e2e-runtime-surfaces/v1",
        "behavior_proven": False,
        "surfaces": _surfaces(root),
    }
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
