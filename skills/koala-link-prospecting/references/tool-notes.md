# Tool notes — Qualified backlink prospecting

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `get_backlink_summary`

Effect: `read`. Scope: `public`. Cost: `{"credits": "2", "kind": "fixed"}`.

Required fields: `target`.

Exposed fields: `target`, `includeSubdomains`, `freshData`.

Provider totals and referring domains; avoid conflating domains with individual links.

## `get_referring_domains`

Effect: `read`. Scope: `public`. Cost: `{"credits": "2", "kind": "fixed"}`.

Required fields: `target`.

Exposed fields: `target`, `limit`, `sortBy`, `onlyDofollow`, `onlyBroken`, `linkType`, `domainFrom`, `firstSeenAfter`, `firstSeenBefore`, `freshData`.

A domain includes only a sample backlink, not every link. Provider rank is not Moz DA. Broken links are candidates needing current verification.

## `get_backlink_list`

Effect: `read`. Scope: `public`. Cost: `{"credits": "2", "kind": "fixed"}`.

Required fields: `target`.

Exposed fields: `target`, `limit`, `sortBy`, `onlyDofollow`, `onlyBroken`, `linkType`, `domainFrom`, `firstSeenAfter`, `firstSeenBefore`, `freshData`, `onlyLost`.

Individual link records. First seen is discovery time, not publication time; lost is provider-observed, not independently confirmed.

## `get_anchor_texts`

Effect: `read`. Scope: `public`. Cost: `{"credits": "2", "kind": "fixed"}`.

Required fields: `target`.

Exposed fields: `target`, `limit`, `freshData`.

Do not infer a penalty from an anchor-text ratio alone.

## `get_backlink_gap`

Effect: `read`. Scope: `public`. Cost: `{"credits": "2", "kind": "fixed"}`.

Required fields: `competitor`, `yourDomain`.

Exposed fields: `competitor`, `yourDomain`, `limit`, `freshData`.

One competitor per call. Candidates are not endorsements or guaranteed placements; no outreach-sending tool is included.

## `get_domain_authority`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`.

Moz Domain Authority, not a Google metric and not the backlink provider rank.

## `get_page_content`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 100,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Extracted text can omit important markup; not finding a fact does not prove absence.

