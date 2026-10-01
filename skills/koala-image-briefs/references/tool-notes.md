# Tool notes — Approved image briefs and generation

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

## `generate_image`

Effect: `generate_image`. Scope: `account`. Cost: `{"fast": "1", "kind": "image", "quality": "8"}`.

Required fields: `prompt`.

Exposed fields: `prompt`, `aspect`, `style`, `quality`, `referenceImages`.

Hosted URL can precede completion. This neither inserts images into an article nor publishes a social post. Reference-image rights and privacy need review.

