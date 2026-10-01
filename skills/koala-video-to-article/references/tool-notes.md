# Tool notes — Rights-aware video-to-article preparation

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `search_youtube`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.1", "kind": "fixed"}`.

Required fields: `query`.

Exposed fields: `query`, `limit`.

Search results do not contain the full video. Inspect captions and usage rights separately.

## `get_youtube_captions`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `videoId`.

Exposed fields: `videoId`, `maxLength`.

Caption text can be automatic and incomplete. Verify exact names and factual claims; captions are not reuse rights.

## `get_page_content`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 100,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Extracted text can omit important markup; not finding a fact does not prove absence.

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

