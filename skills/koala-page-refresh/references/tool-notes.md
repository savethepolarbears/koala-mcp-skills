# Tool notes — Existing-page rescue and refresh brief

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_gsc_page_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `pageUrl`.

Exposed fields: `days`, `startDate`, `endDate`, `pageUrl`, `limit`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_gsc_query_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `query`.

Exposed fields: `days`, `startDate`, `endDate`, `query`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_gsc_indexing_status`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `urls`.

Exposed fields: `urls`, `brandId`.

Max 10 URLs belonging to the connected property. A sitemap entry is not indexation evidence.

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

## `search_google_serp`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.5", "kind": "fixed"}`.

Required fields: `keyword`.

Exposed fields: `keyword`, `location`, `include`, `raw`, `limit`, `language`, `freshData`.

Use keyword, not query. Locality uses location; there is no country input here. Fetch sources to verify precise claims; snippets are discovery evidence.

## `check_keyword_coverage`

Effect: `read`. Scope: `public`. Cost: `{"credits": "3", "kind": "fixed"}`.

Required fields: `keywords`, `domain`.

Exposed fields: `keywords`, `domain`, `country`, `language`.

Max 30. Model judgments from sitemap/ranking evidence; not planned tasks and not proof of absence. Inspect matched URL and intent before replacement.

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

## `edit_article`

Effect: `edit`. Scope: `article`. Cost: `{"credits": "1", "kind": "fixed"}`.

Required fields: `articleId`, `instruction`.

Exposed fields: `articleId`, `instruction`, `brandId`.

One platform credit, no writer words. Instructions are self-contained. Previous content is saved and concurrent edits rejected; do not assume a restore or CMS publish tool exists.

