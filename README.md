# Eser KUBALI's Claude Code plugin marketplace

A [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
that aggregates Eser KUBALI's plugins. The plugins themselves live in their own
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

`eserlxl/qb` and `eserlxl/planwright` are plugin repositories. Earlier, each one
*also* declared its own marketplace named `eserlxl`, so adding both as
marketplaces made the second overwrite the first (a marketplace is keyed by its
`name`, not by the repo it came from). This repo is the single canonical
`eserlxl` marketplace; add **only this repo** and it offers every plugin.

> Do not run `/plugin marketplace add eserlxl/qb` or `eserlxl/planwright` as
> marketplaces — those repos still declare an `eserlxl` marketplace internally
> and would clobber this aggregator's registration.
