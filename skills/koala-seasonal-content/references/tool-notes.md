# Tool notes — Seasonal demand and publishing lead time

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `get_google_trends`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `keywords`.

Exposed fields: `keywords`, `timeRange`, `country`, `type`.

Relative 0–100 interest, not monthly volume. Cross-call normalization can differ. Preserve market and search surface.

## `get_pinterest_trends`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.1", "kind": "fixed"}`.

Required fields: none exposed.

Exposed fields: `category`, `country`, `trendsPreset`, `endDate`, `keywordsToInclude`, `limit`.

Pinterest interest is not Google volume. Seasonal future dates are planning signals, not observed future demand.

## `get_keyword_volume`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `keywords`.

Exposed fields: `keywords`, `country`, `language`, `freshData`.

Max 20 per market. Provider estimates. Advertising competition/CPC are not organic difficulty or affiliate earnings.

## `get_related_keywords`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "per_unique_seed"}`.

Required fields: `keywords`.

Exposed fields: `keywords`, `minVolume`, `country`, `language`, `freshData`.

Max 5 seeds. Bills per successful unique trimmed seed; reserve all unique seeds conservatively. Related terms are not automatically new content intents.

## `check_keyword_coverage`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `keywords`, `domain`.

Exposed fields: `keywords`, `domain`, `country`, `language`.

Max 30. Model judgments from sitemap/ranking evidence; not planned tasks and not proof of absence. Inspect matched URL and intent before replacement.

## `list_article_tasks`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `status`, `startDate`, `endDate`, `dateScope`, `sortBy`, `limit`, `initiativeId`, `brandId`.

One status array is preferable to repeated one-status calls. Calendar coverage is separate from published coverage.

## `get_gsc_query_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `query`.

Exposed fields: `days`, `startDate`, `endDate`, `query`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

