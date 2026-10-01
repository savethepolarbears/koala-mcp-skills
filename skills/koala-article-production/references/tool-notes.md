# Tool notes — Approved brief to verified Koala article

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

## `list_writer_presets`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `brandId`.

Named preset settings replace defaults as a snapshot, not a shallow overlay. Use exact discovered names only.

## `list_article_tasks`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `status`, `startDate`, `endDate`, `dateScope`, `sortBy`, `limit`, `initiativeId`, `brandId`.

One status array is preferable to repeated one-status calls. Calendar coverage is separate from published coverage.

## `list_recent_articles`

Effect: `read`. Scope: `article`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `limit`, `brandId`.

Bounded recent results are not a complete article inventory. Ambiguous matches require disambiguation, not a guessed ID.

## `check_keyword_coverage`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `keywords`, `domain`.

Exposed fields: `keywords`, `domain`, `country`, `language`.

Max 30. Model judgments from sitemap/ranking evidence; not planned tasks and not proof of absence. Inspect matched URL and intent before replacement.

## `create_article_in_koala_writer`

Effect: `generate`. Scope: `article`. Cost: `{"kind": "words"}`.

Required fields: none exposed.

Exposed fields: `presetName`, `articleType`, `articleInstructions`, `includeCta`, `ctaPrompt`, `articleLength`, `numberOfSections`, `includeFaq`, `projectId`, `asin`, `articleUrl`, `youTubeVideoUrl`, `serviceArea`, `numberOfItems`, `multimediaOption`, `targetKeyword`, `title`, `toneOfVoiceProfile`, `pointOfView`, `includeConclusion`, `includeKeyTakeaways`, `imageStyle`, `maxImages`, `maxVideos`, `realTimeData`, `realTimeDataSource`, `shouldCiteSources`, `enableDeepResearch`, `extendedResearch`, `brandMentionLevel`, `language`, `country`, `allowDuplicate`, `brandId`, `waitForCompletion`.

Creation can upload or publish via brand/project integration. Omit both for standalone output. Never enable allowDuplicate without explicit authorization for another article. Persist articleId before waiting. Prompts cannot enable image pipeline settings.

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

