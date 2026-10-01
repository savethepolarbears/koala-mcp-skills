# Tool notes — First-party content decay investigation

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_gsc_search_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `days`, `startDate`, `endDate`, `country`, `device`, `pageContains`, `queryContains`, `compare`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_gsc_top_pages`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `days`, `startDate`, `endDate`, `country`, `device`, `pageContains`, `queryContains`, `limit`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_gsc_top_queries`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `days`, `startDate`, `endDate`, `country`, `device`, `pageContains`, `queryContains`, `limit`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

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

## `get_ga4_page_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `pagePath`.

Exposed fields: `dateRange`, `compareRange`, `brandId`, `pagePath`.

Measured connected GA4 data. dateRange/compareRange are not GSC startDate/endDate. Page performance takes a path, not a URL. Sessions and GSC clicks are different measures.

## `search_google_serp`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.5", "kind": "fixed"}`.

Required fields: `keyword`.

Exposed fields: `keyword`, `location`, `include`, `raw`, `limit`, `language`, `freshData`.

Use keyword, not query. Locality uses location; there is no country input here. Fetch sources to verify precise claims; snippets are discovery evidence.

## `get_page_content`

Effect: `read`. Scope: `public`. Cost: `{"credits": "0.25", "kind": "fixed"}`.

Required fields: `url`.

Exposed fields: `offset`, `contentHash`, `url`.

Up to 100,000 characters per returned chunk. Continue with returned nextOffset and same contentHash; every chunk costs credits. Changed hash requires restart. Extracted text can omit important markup; not finding a fact does not prove absence.

