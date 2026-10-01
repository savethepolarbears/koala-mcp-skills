# Tool notes — Credit and Writer allowance planner

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `get_brand_profile`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `brandId`.

Inspect integration and effective post status before generation; presets or project overrides can change them.

## `list_writer_presets`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `brandId`.

Named preset settings replace defaults as a snapshot, not a shallow overlay. Use exact discovered names only.

## `list_article_tasks`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `status`, `startDate`, `endDate`, `dateScope`, `sortBy`, `limit`, `initiativeId`, `brandId`.

One status array is preferable to repeated one-status calls. Calendar coverage is separate from published coverage.

