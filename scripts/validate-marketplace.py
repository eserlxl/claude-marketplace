#!/usr/bin/env python3
"""Validate .claude-plugin/marketplace.json for the eserlxl Claude Code marketplace.

Pure standard library, no dependencies. Exits 0 when the manifest is valid and
consistent with README.md, or non-zero with a clear message otherwise.

It mirrors the structural checks the official `claude plugin validate .` performs
(JSON schema, duplicate plugin names, source path traversal) and adds a catalog
sync check: the plugin list in the manifest must match the plugin table and the
`/plugin install` commands documented in README.md, so the two never drift.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
README = ROOT / "README.md"

# Plugin source types accepted by Claude Code (object form); a string source is a
# "./"-relative local path. See the Claude Code marketplace reference.
VALID_SOURCE_TYPES = {"github", "url", "git-subdir", "npm"}
SOURCE_REQUIRED = {
    "github": {"repo"},
    "url": {"url"},
    "git-subdir": {"url", "path"},
    "npm": {"package"},
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")  # kebab-case, no spaces


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def _has_traversal(path):
    return isinstance(path, str) and ".." in path.split("/")


def main():
    if not MANIFEST.exists():
        fail(f"missing manifest: {MANIFEST}")
    try:
        data = json.loads(MANIFEST.read_text())
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {MANIFEST.name}: {exc}")

    if not isinstance(data, dict):
        fail("manifest root must be a JSON object")
    if not data.get("name"):
        fail("manifest missing top-level 'name'")
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("manifest 'plugins' must be a non-empty array")

    names = []
    for i, plugin in enumerate(plugins):
        where = f"plugins[{i}]"
        if not isinstance(plugin, dict):
            fail(f"{where} must be an object")
        name = plugin.get("name")
        if not isinstance(name, str) or not name:
            fail(f"{where} missing a string 'name'")
        if not NAME_RE.match(name):
            fail(f"{where} name '{name}' is not kebab-case (lowercase, hyphen-separated)")
        if not plugin.get("description"):
            fail(f"plugin '{name}' missing a non-empty 'description'")

        src = plugin.get("source")
        if src is None:
            fail(f"plugin '{name}' missing 'source'")
        if isinstance(src, str):
            if not src.startswith("./"):
                fail(f"plugin '{name}' string source must be a './'-relative path, got '{src}'")
            if _has_traversal(src):
                fail(f"plugin '{name}' source path contains '..'")
        elif isinstance(src, dict):
            stype = src.get("source")
            if stype not in VALID_SOURCE_TYPES:
                fail(f"plugin '{name}' source.source '{stype}' "
                     f"is not one of {sorted(VALID_SOURCE_TYPES)}")
            missing = SOURCE_REQUIRED[stype] - set(src)
            if missing:
                fail(f"plugin '{name}' {stype} source missing field(s): {sorted(missing)}")
            if _has_traversal(src.get("path", "")):
                fail(f"plugin '{name}' source path contains '..'")
        else:
            fail(f"plugin '{name}' source must be an object or a './'-relative string")
        names.append(name)

    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        fail(f"duplicate plugin name(s): {dupes}")

    if not README.exists():
        fail("README.md is missing")
    readme = README.read_text()
    table_names = set(re.findall(r"^\|\s*`([a-z0-9][a-z0-9-]*)`\s*\|", readme, re.MULTILINE))
    install_names = set(re.findall(r"/plugin install\s+([a-z0-9][a-z0-9-]*)@", readme))
    manifest_names = set(names)
    if table_names != manifest_names:
        fail(f"README plugin table {sorted(table_names)} "
             f"does not match manifest {sorted(manifest_names)}")
    if install_names != manifest_names:
        fail(f"README '/plugin install' commands {sorted(install_names)} "
             f"do not match manifest {sorted(manifest_names)}")

    print(f"OK: {len(names)} plugin(s) valid and in sync with README: {', '.join(names)}")


if __name__ == "__main__":
    main()
