---
name: site-audit
description: Comprehensive website audit that maps site structure, extracts content, analyzes pages, and checks link health. Produces a detailed site analysis report.
---

# Site Audit

Perform a comprehensive audit of: **$ARGUMENTS**

If a domain name is given without a protocol, prepend "https://". Follow these steps precisely.

## Step 1: Site Mapping

Use `map_website`:
- url: "$ARGUMENTS", mode: "map", max_pages: 15, max_depth: 2

Record all discovered pages, titles, and hierarchy.

## Step 2: Research Mode Traversal

Use `map_website`:
- url: "$ARGUMENTS", mode: "research", max_pages: 10, max_depth: 2

## Step 3: Documentation Check

If the site has docs, explore them:
- `map_website` with url: "$ARGUMENTS", mode: "docs", max_pages: 10

## Step 4: Homepage Analysis

Use `content_operations`:
- operation: "retrieve", url: "$ARGUMENTS", extraction_method: "markdown"

Then analyze with both lenses:
- operation: "analyze", analysis_type: "business", extract_key_points: true, summarize: true
- operation: "analyze", analysis_type: "technical", extract_key_points: true, summarize: true

## Step 5: Link Extraction

Use `content_operations` three times:
- operation: "extract", url: "$ARGUMENTS", link_type: "all", max_links: 100
- operation: "extract", url: "$ARGUMENTS", link_type: "internal", max_links: 100
- operation: "extract", url: "$ARGUMENTS", link_type: "external", max_links: 50

## Step 6: Key Page Analysis

For 3-5 important internal pages (about, pricing, product, blog), use `content_operations`:
- operation: "retrieve", url: <page_url>, extraction_method: "markdown"

## Step 7: External Reputation

Use `web_search`:
- query: "$ARGUMENTS review OR opinion OR analysis", num_results: 10

Use `social_search`:
- query: "$ARGUMENTS", platforms: ["reddit", "hackernews"], max_results_per_platform: 5

## Step 8: Compile Audit Report

1. **Site Overview** -- Purpose and primary audience
2. **Site Structure** -- Page hierarchy, navigation patterns, depth
3. **Content Assessment** -- Homepage effectiveness, key page quality, content volume
4. **Technical Observations** -- Technology signals, frameworks detected
5. **Link Analysis** -- Internal structure, external connections, documents, images
6. **External Reputation** -- Social media and review site mentions
7. **Strengths** -- What the site does well
8. **Issues & Recommendations** -- Problems and suggested improvements
9. **Summary Statistics** -- Table: total pages, links, content length, etc.

Use tables for statistics and link summaries.
