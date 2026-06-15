# Claude Code plugin marketplace

A [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
that aggregates plugins. The plugins themselves live in their own
repositories; this repo only ships the catalog (`.claude-plugin/marketplace.json`)
and references each plugin via a git source.

## Plugins

| Plugin | Source repo | What it does |
|--------|-------------|--------------|
| `qb` | [`eserlxl/qb`](https://github.com/eserlxl/qb) (`platforms/claude-code`) | Repo-aware, gated, multi-step planning workflow: master plan, autopsy, phase decomposition, coverage/quality audit, gated implementation. |
| `planwright` | [`eserlxl/planwright`](https://github.com/eserlxl/planwright) | Grounded codebase planning that writes a verification-ready checkbox plan. |

## Install

```text
/plugin marketplace add eserlxl/claude-marketplace
/plugin install qb@eserlxl
/plugin install planwright@eserlxl
```

## Why a dedicated marketplace repo?

Individual plugin repositories (like `qb` or `planwright`) may declare their own
marketplace named `eserlxl`. Adding multiple such repositories as marketplaces
makes the later ones overwrite the previous ones (a marketplace is keyed by its
`name`, not by the repo it came from). This repo is the single canonical
`eserlxl` marketplace; add **only this repo** and it offers every plugin in the catalog.

> Do not run `/plugin marketplace add` for individual plugin repositories as
> marketplaces — if those repos declare an `eserlxl` marketplace internally,
> they would clobber this aggregator's registration.
