# eserlxl Claude Code plugin marketplace

This repository is the canonical eserlxl plugin marketplace for
Claude Code plugins.

It is a catalog-only repository. The plugins live in their own repositories;
this repo only ships `.claude-plugin/marketplace.json` and references each
plugin through its git source.

## Plugins

| Plugin | Source repo | Description |
|--------|-------------|-------------|
| `qb` | `eserlxl/qb` | Repo-aware, gated, multi-step planning workflow for Claude Code. It creates a master plan, autopsy, phase decomposition, coverage/quality audit, and gated implementation flow. Outputs English Planner-docs/ files and works in-session with zero setup. |
| `planwright` | `eserlxl/planwright` | Grounded codebase planning for AI coding agents, packaged for Claude Code. It audits your repository and writes a verification-ready checkbox plan where every step is concrete and checkable. |

## Install

Add this marketplace once:

```text
/plugin marketplace add eserlxl/claude-marketplace
```

Then install any plugin from the catalog:

```text
/plugin install qb@eserlxl
/plugin install planwright@eserlxl
```

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
