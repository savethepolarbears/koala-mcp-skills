# Tool notes — Research worthwhile content opportunities

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

## `get_brand_knowledge`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `brandId`.

Saved business facts are context, not independent verification of every claim. No knowledge-update tool is exposed.

## `list_article_tasks`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `status`, `startDate`, `endDate`, `dateScope`, `sortBy`, `limit`, `initiativeId`, `brandId`.

One status array is preferable to repeated one-status calls. Calendar coverage is separate from published coverage.

## `get_gsc_top_queries`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `days`, `startDate`, `endDate`, `country`, `device`, `pageContains`, `queryContains`, `limit`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_sitemap`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `limit`.

Default 1,000, up to 50,000 slugs; 90-second/200-child bounds. returnedSlugCount is returned inventory, not site total. No proof of indexation or orphan status.

## `discover_domain_keywords`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `limit`, `minVolume`, `competitionLevel`, `country`, `language`, `freshData`.

Ideas related to a niche, not a ranking inventory. Avoid speculative keyword-to-revenue conversion.

## `get_related_keywords`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "per_unique_seed"}`.

Required fields: `keywords`.

Exposed fields: `keywords`, `minVolume`, `country`, `language`, `freshData`.

Max 5 seeds. Bills per successful unique trimmed seed; reserve all unique seeds conservatively. Related terms are not automatically new content intents.

## `get_keyword_variations`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "per_unique_seed"}`.

Required fields: `keywords`.

Exposed fields: `keywords`, `limit`, `minVolume`, `country`, `language`, `freshData`.

Max 5 seeds. Variations contain the seed; do not confuse variants with distinct intents. Paid per successful unique trimmed seed.

## `get_autocomplete`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `query`.

Exposed fields: `query`.

This exposed input surface has no country/language arguments. Record market as provider-default/unknown rather than invent parameters. Suggestions are not volumes.

## `get_keyword_volume`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `keywords`.

Exposed fields: `keywords`, `country`, `language`, `freshData`.

Max 20 per market. Provider estimates. Advertising competition/CPC are not organic difficulty or affiliate earnings.

## `check_keyword_coverage`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `keywords`, `domain`.

Exposed fields: `keywords`, `domain`, `country`, `language`.

Max 30. Model judgments from sitemap/ranking evidence; not planned tasks and not proof of absence. Inspect matched URL and intent before replacement.

## `search_google_serp`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.5", "kind": "fixed"}`.

Required fields: `keyword`.

Exposed fields: `keyword`, `location`, `include`, `raw`, `limit`, `language`, `freshData`.

Use keyword, not query. Locality uses location; there is no country input here. Fetch sources to verify precise claims; snippets are discovery evidence.

## `get_page_content`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 100,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Extracted text can omit important markup; not finding a fact does not prove absence.

