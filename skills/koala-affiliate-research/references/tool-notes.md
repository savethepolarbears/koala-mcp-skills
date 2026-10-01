# Tool notes — Evidence-backed affiliate product research

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `amazon_search`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `keyword`.

Exposed fields: `keyword`, `amazonDomain`.

Resolve candidate ASINs in the requested marketplace. No guarantee of current price, stock or testing.

## `amazon_product_details`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: none exposed.

Exposed fields: **opaque: inspect the live tool; do not infer arguments**.

Connector exposed an unconstrained argument object. Discover and inspect the live tool before invocation; no ASIN argument name is asserted by this pack. Returned price may be absent; attribute reviewer observations.

## `get_page_content`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 100,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Extracted text can omit important markup; not finding a fact does not prove absence.

## `search_google_serp`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.5", "kind": "fixed"}`.

Required fields: `keyword`.

Exposed fields: `keyword`, `location`, `include`, `raw`, `limit`, `language`, `freshData`.

Use keyword, not query. Locality uses location; there is no country input here. Fetch sources to verify precise claims; snippets are discovery evidence.

## `check_keyword_coverage`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `keywords`, `domain`.

Exposed fields: `keywords`, `domain`, `country`, `language`.

Max 30. Model judgments from sitemap/ranking evidence; not planned tasks and not proof of absence. Inspect matched URL and intent before replacement.

## `get_keyword_volume`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `keywords`.

Exposed fields: `keywords`, `country`, `language`, `freshData`.

Max 20 per market. Provider estimates. Advertising competition/CPC are not organic difficulty or affiliate earnings.

