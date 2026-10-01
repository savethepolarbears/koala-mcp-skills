# Tool notes — Competitor advantage and gap analysis

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_competitor_domains`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `limit`, `country`, `language`, `freshData`.

Search competitors may have different business models. Validate relevance before a teardown.

## `get_ranking_keywords`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `target`.

Exposed fields: `target`, `minPosition`, `maxPosition`, `minVolume`, `keywordContains`, `keywordMatchType`, `limit`, `country`, `language`, `freshData`.

Provider-observed rankings are separate from GSC. Exact keywordContains is whole-word; broad is substring.

## `get_keyword_gap`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `competitor`, `yourDomain`.

Exposed fields: `competitor`, `yourDomain`, `limit`, `minVolume`, `country`, `language`, `freshData`.

Ranking gap does not establish a content gap. Check the target site and its calendar.

## `get_estimated_top_pages`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `limit`, `country`, `language`, `freshData`.

Estimated organic traffic/value, not measured visits or revenue. Confirm page intent with a fetch.

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

## `get_backlink_gap`

Effect: `read`. Scope: `public`. Cost: `{"credits": "2", "kind": "fixed"}`.

Required fields: `competitor`, `yourDomain`.

Exposed fields: `competitor`, `yourDomain`, `limit`, `freshData`.

One competitor per call. Candidates are not endorsements or guaranteed placements; no outreach-sending tool is included.

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

