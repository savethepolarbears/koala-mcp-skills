# Tool notes — Bounded multi-brand content operations loop

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `list_brands`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Resolve the brand deliberately. Do not copy account results into the public repository.

## `get_brand_profile`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `brandId`.

Inspect integration and effective post status before generation; presets or project overrides can change them.

## `get_brand_knowledge`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `brandId`.

Saved business facts are context, not independent verification of every claim. No knowledge-update tool is exposed.

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

## `get_gsc_search_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `days`, `startDate`, `endDate`, `country`, `device`, `pageContains`, `queryContains`, `compare`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_ga4_top_pages`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `dateRange`, `compareRange`, `brandId`, `limit`.

Measured connected GA4 data. dateRange/compareRange are not GSC startDate/endDate. Page performance takes a path, not a URL. Sessions and GSC clicks are different measures.

