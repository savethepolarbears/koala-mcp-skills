# Tool notes — Public-domain prospect audit

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `get_traffic_overview`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `country`, `language`, `freshData`.

Directional provider estimates, not connected first-party metrics.

## `get_historical_traffic`

Effect: `read`. Scope: `public`. Cost: `{"credits": "4", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `months`, `country`, `language`, `freshData`.

Higher-cost monthly estimates. Use only when a time-series question changes the decision; align markets and periods.

## `get_domain_authority`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`.

Moz Domain Authority, not a Google metric and not the backlink provider rank.

## `get_ranking_keywords`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `target`.

Exposed fields: `target`, `minPosition`, `maxPosition`, `minVolume`, `keywordContains`, `keywordMatchType`, `limit`, `country`, `language`, `freshData`.

Provider-observed rankings are separate from GSC. Exact keywordContains is whole-word; broad is substring.

## `get_estimated_top_pages`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `limit`, `country`, `language`, `freshData`.

Estimated organic traffic/value, not measured visits or revenue. Confirm page intent with a fetch.

## `get_competitor_domains`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `limit`, `country`, `language`, `freshData`.

Search competitors may have different business models. Validate relevance before a teardown.

## `get_google_ai_overview_presence`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`, `keywords`.

Exposed fields: `domain`, `keywords`, `urls`.

Sampled Google AI Overviews only, not ChatGPT/Claude/all AI. This exposed schema has no country/language input; disclose unknown provider market. Absent citation is sample absence.

## `get_page_content`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 100,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Extracted text can omit important markup; not finding a fact does not prove absence.

