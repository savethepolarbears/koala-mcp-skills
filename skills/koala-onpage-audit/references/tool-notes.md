# Tool notes — Evidence-first on-page audit

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

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

## `analyze_page`

Effect: `read`. Scope: `public`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `url`, `prompt`.

Exposed fields: `url`, `prompt`.

Source-derived analyst answer, not a complete deterministic SEO audit. Analyst sees up to 24,000 extracted characters; verify critical facts against source text/HTML.

## `screenshot_page`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `url`, `fullPage`, `mobile`, `width`, `height`.

Visual inspection only. Does not prove full markup or crawler access; mobile overrides desktop dimensions.

## `get_sitemap`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `domain`.

Exposed fields: `domain`, `limit`.

Default 1,000, up to 50,000 slugs; 90-second/200-child bounds. returnedSlugCount is returned inventory, not site total. No proof of indexation or orphan status.

