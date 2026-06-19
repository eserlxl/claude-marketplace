#!/usr/bin/env python3
"""Tests for scripts/validate-marketplace.py.

Standard library only. Mirrors the files the validator reads into a tempdir and
runs the validator via subprocess against the pristine copy and against seeded
defects, asserting its accept/reject contract. Exits 0 only if every case behaves.

This exists because CI always runs the validator against the *valid* manifest, so
it never exercises the failure paths; a regression that weakened the validator
(e.g. a broken sync regex, or an early `sys.exit(0)`) would ship green. These
cases fail loudly if the validator stops rejecting bad input.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_REL = ".claude-plugin/marketplace.json"
README_REL = "README.md"
VALIDATOR_REL = "scripts/validate-marketplace.py"


def make_workdir(tmp, mutate_manifest=None, mutate_readme=None):
    """Mirror the three files the validator reads into tmp, optionally mutating the
    manifest dict and/or the README text. The real repo files are never touched."""
    work = Path(tmp)
    (work / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (work / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / VALIDATOR_REL, work / VALIDATOR_REL)

    manifest = json.loads((ROOT / MANIFEST_REL).read_text())
    if mutate_manifest:
        mutate_manifest(manifest)
    (work / MANIFEST_REL).write_text(json.dumps(manifest, indent=2))

    readme = (ROOT / README_REL).read_text()
    if mutate_readme:
        readme = mutate_readme(readme)
    (work / README_REL).write_text(readme)
    return work


def run_validator(work):
    return subprocess.run(
        [sys.executable, str(work / VALIDATOR_REL)],
        capture_output=True, text=True,
    )


# --- seeded defects -------------------------------------------------------
def dup_name(m):
    m["plugins"].append(dict(m["plugins"][0]))


def bad_source_type(m):
    m["plugins"][0]["source"]["source"] = "ftp"


def drop_source_field(m):
    # planwright's url source -> remove its required 'url'
    m["plugins"][1]["source"].pop("url", None)


def readme_drift(r):
    return r.replace("/plugin install qb@eserlxl", "/plugin install gone@eserlxl")


# (name, expect_ok, mutate_manifest, mutate_readme)
CASES = [
    ("pristine copy accepted", True, None, None),
    ("duplicate plugin name rejected", False, dup_name, None),
    ("README install drift rejected", False, None, readme_drift),
    ("invalid source type rejected", False, bad_source_type, None),
    ("missing source field rejected", False, drop_source_field, None),
]


def main():
    failures = []
    for name, expect_ok, mm, mr in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            work = make_workdir(tmp, mm, mr)
            res = run_validator(work)
        ok = res.returncode == 0
        passed = ok == expect_ok
        print(f"{'PASS' if passed else 'FAIL'}: {name} "
              f"(exit={res.returncode}, expected {'0' if expect_ok else 'non-0'})")
        if not passed:
            failures.append(name)
            if res.stderr.strip():
                print("    stderr:", res.stderr.strip())

    if failures:
        print(f"\n{len(failures)} case(s) misbehaved: {failures}")
        sys.exit(1)
    print(f"\nAll {len(CASES)} case(s) passed.")


if __name__ == "__main__":
    main()
