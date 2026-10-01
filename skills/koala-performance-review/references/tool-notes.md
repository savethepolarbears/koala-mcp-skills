# Tool notes — Measured performance and experiment review

Reviewed 2026-10-01. Runtime definitions win. These are conservative transcriptions; inspect exact live inputs, especially opaque fields. Costs are reviewed planning estimates, not a real-time billing guarantee. Full workflows may use a subset of the tools listed.

## `get_usage`

Effect: `read`. Scope: `account`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: none; call without arguments.

Check platform credits and writer words separately. Reading a balance does not reserve it.

## `get_gsc_search_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `days`, `startDate`, `endDate`, `country`, `device`, `pageContains`, `queryContains`, `compare`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_gsc_top_queries`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `days`, `startDate`, `endDate`, `country`, `device`, `pageContains`, `queryContains`, `limit`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_gsc_top_pages`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `days`, `startDate`, `endDate`, `country`, `device`, `pageContains`, `queryContains`, `limit`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_gsc_query_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `query`.

Exposed fields: `days`, `startDate`, `endDate`, `query`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_gsc_page_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `pageUrl`.

Exposed fields: `days`, `startDate`, `endDate`, `pageUrl`, `limit`, `brandId`.

Measured connected-property data. Explicit inclusive date pairs; equal periods and same filters. GSC country filters use alpha-3. Missing or truncated rows are not zero. compare=true is supported only on aggregate search performance.

## `get_ga4_top_pages`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `dateRange`, `compareRange`, `brandId`, `limit`.

Measured connected GA4 data. dateRange/compareRange are not GSC startDate/endDate. Page performance takes a path, not a URL. Sessions and GSC clicks are different measures.

## `get_ga4_traffic_sources`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `dateRange`, `compareRange`, `brandId`.

Measured connected GA4 data. dateRange/compareRange are not GSC startDate/endDate. Page performance takes a path, not a URL. Sessions and GSC clicks are different measures.

## `get_ga4_audience_overview`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: none exposed.

Exposed fields: `dateRange`, `compareRange`, `brandId`.

Measured connected GA4 data. dateRange/compareRange are not GSC startDate/endDate. Page performance takes a path, not a URL. Sessions and GSC clicks are different measures.

## `get_ga4_page_performance`

Effect: `read`. Scope: `brand`. Cost: `{"kind": "free"}`.

Required fields: `pagePath`.

Exposed fields: `dateRange`, `compareRange`, `brandId`, `pagePath`.

Measured connected GA4 data. dateRange/compareRange are not GSC startDate/endDate. Page performance takes a path, not a URL. Sessions and GSC clicks are different measures.

