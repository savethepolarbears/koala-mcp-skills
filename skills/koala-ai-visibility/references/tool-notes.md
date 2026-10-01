# Tool notes — Sampled Google AI Overview visibility

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `get_google_ai_overview_presence`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`, `keywords`.

Exposed fields: `domain`, `keywords`, `urls`.

Sampled Google AI Overviews only, not ChatGPT/Claude/all AI. This exposed schema has no country/language input; disclose unknown provider market. Absent citation is sample absence.

## `compare_google_ai_overview_citations`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`, `competitors`, `keywords`.

Exposed fields: `domain`, `competitors`, `keywords`.

Up to 3 competitors and 5 queries. Preserve the sampled query set; no market argument exposed. Do not broaden findings to all AI engines.

## `get_ai_search_opportunities`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `domain`, `keywords`.

Exposed fields: `domain`, `keywords`, `country`, `language`.

Max 3 seeds. Opportunity hypotheses, not observed all-engine visibility.

## `audit_page_citation_readiness`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `urls`.

Exposed fields: `urls`.

Heuristic 0–100 readiness score, not an observed citation rate or guarantee. Use a nonempty set of max 3 URLs.

## `check_ai_crawler_robots_rules`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`.

Declared crawler-specific robots rules, not a network/firewall test or an AI-engine visibility measurement.

## `search_brand_mentions`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`, `brandName`.

Exposed fields: `domain`, `brandName`, `competitors`.

Web search mentions, not AI-chat mentions or an exhaustive count. Inspect source pages before assigning sentiment.

## `get_page_content`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 100,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Extracted text can omit important markup; not finding a fact does not prove absence.

