# eserlxl Claude Code plugin marketplace

This repository is the canonical eserlxl plugin marketplace for
Claude Code plugins.

It is a catalog repository: no plugin source lives here. The plugins live in
their own repositories and are referenced through their git source. Alongside the
catalog (`.claude-plugin/marketplace.json`) it ships only the light tooling that
keeps the catalog valid (see [Validating the marketplace](#validating-the-marketplace)).

## Plugins

| Plugin | Source repo | Description |
|--------|-------------|-------------|
| `qb` | [`eserlxl/qb`](https://github.com/eserlxl/qb) | Repo-aware, gated, multi-step planning workflow for Claude Code. It creates a master plan, assessment, phase decomposition, coverage/quality audit, and gated implementation flow. Outputs English Planner-docs/ files and works in-session with zero setup. |
| `planwright` | [`eserlxl/planwright`](https://github.com/eserlxl/planwright) | Grounded codebase planning for AI coding agents, packaged for Claude Code. It audits your repository and writes a verification-ready checkbox plan where every step is concrete and checkable. |
| `external-agents` | [`eserlxl/external-agents`](https://github.com/eserlxl/external-agents) | Run external coding-agent CLIs — `agy`, `codex`, optionally `claude` — as autonomous sub-agents from inside Claude Code. Dispatch a task to one agent or fan one prompt out to all in parallel and collect every response inline; read-write by default, with a `--read-only` mode available. |

## Install

Add this marketplace once:

```text
/plugin marketplace add eserlxl/claude-marketplace
```

Then install any plugin from the catalog:

```text
/plugin install qb@eserlxl
/plugin install planwright@eserlxl
/plugin install external-agents@eserlxl
```

## Validating the marketplace

The catalog must stay a valid `.claude-plugin/marketplace.json`. Before pushing a
catalog change, validate it with Claude Code:

```text
claude plugin validate .
```

A self-contained check (no Claude Code required) also runs in CI on every push and
pull request, and can be run locally:

```text
python3 scripts/validate-marketplace.py
```

It confirms the manifest is valid JSON, every plugin entry has a well-formed name,
description, and source, there are no duplicate plugin names, and the plugin list stays
in sync with the table and install commands in this README.

## Why this marketplace exists

Claude Code marketplaces are keyed by marketplace name, not by the repository
they came from.

Individual plugin repositories, such as `qb` or `planwright`, may also declare
a marketplace named `eserlxl`. If you add those repositories directly as
marketplaces, the later registration can overwrite the earlier one.

This repository avoids that conflict by acting as the single canonical
`eserlxl` marketplace.

## Important

Add only this repository as the marketplace:

```text
/plugin marketplace add eserlxl/claude-marketplace
```

Do not run `/plugin marketplace add` for individual plugin repositories such as
`eserlxl/qb` or `eserlxl/planwright`. If those repositories declare an internal
`eserlxl` marketplace, they may clobber this aggregator registration.

## License

The MIT license in [LICENSE](LICENSE) covers **only this catalog repository** — its
`marketplace.json`, this README, and the validation tooling here. It does not cover the
plugins themselves.

Each plugin ships from its own repository under its own license, and they are not
uniformly MIT:

- [`qb`](https://github.com/eserlxl/qb) — MIT
- [`planwright`](https://github.com/eserlxl/planwright) — GNU GPL v3.0 or later
- [`external-agents`](https://github.com/eserlxl/external-agents) — GNU GPL v3.0 or later

Check each plugin's repository for the authoritative terms.
