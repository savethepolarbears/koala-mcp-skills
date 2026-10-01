# Tool notes — Verified URL indexing inspection and submission

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

## `get_gsc_indexing_status`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `urls`.

Exposed fields: `urls`, `brandId`.

Max 10 URLs belonging to the connected property. A sitemap entry is not indexation evidence.

## `request_indexing`

Effect: `submit`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `urls`.

Exposed fields: `urls`, `brandId`.

Explicit separate submission authorization. Max 20. A successful request is not an indexing guarantee; do not substitute generic Google Indexing API claims.

## `get_page_content`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 100,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Extracted text can omit important markup; not finding a fact does not prove absence.

## `get_page_html`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.1", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 250,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Raw HTML is not JavaScript-rendered.

