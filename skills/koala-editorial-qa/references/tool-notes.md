# Tool notes — Evidence-first editorial acceptance loop

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_article_status`

Effect: `read`. Scope: `article`. Cost: `{"kind": "free"}`.

Required fields: `articleId`.

Exposed fields: `articleId`, `brandId`.

Resume the same article ID. No tight polling loop and no replacement job after a timeout.

## `get_article_content`

Effect: `read`. Scope: `article`. Cost: `{"kind": "free"}`.

Required fields: `articleId`.

Exposed fields: `articleId`, `variant`, `brandId`.

Polished falls back to original when no edited version exists. Read only account-owned articles; validate identity when no brand filter is used.

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

## `edit_article`

Effect: `edit`. Scope: `article`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `articleId`, `instruction`.

Exposed fields: `articleId`, `instruction`, `brandId`.

One platform credit, no writer words. Instructions are self-contained. Previous content is saved and concurrent edits rejected; do not assume a restore or CMS publish tool exists.

