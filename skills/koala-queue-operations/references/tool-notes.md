# Tool notes — Queue recovery and safe resumption

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `list_recent_articles`

Effect: `read`. Scope: `article`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `limit`, `brandId`.

Bounded recent results are not a complete article inventory. Ambiguous matches require disambiguation, not a guessed ID.

## `list_article_tasks`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `status`, `startDate`, `endDate`, `dateScope`, `sortBy`, `limit`, `initiativeId`, `brandId`.

One status array is preferable to repeated one-status calls. Calendar coverage is separate from published coverage.

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

