---
name: market-intel
description: Market intelligence gathering combining news analysis, social trend monitoring, GitHub ecosystem scanning, and web research to produce a market landscape report.
---

# Market Intelligence

Gather market intelligence on: **$ARGUMENTS**

The argument may be a market segment, technology category, industry vertical, or trend. Follow these steps precisely.

## Step 1: Market Landscape Search

Use `web_search` twice:
1. query: "$ARGUMENTS market landscape overview", num_results: 15, extract_content: true
2. query: "$ARGUMENTS market size growth trends", num_results: 10, extract_content: true

## Step 2: News & Industry Developments

Use `news_aggregation` twice:
1. query: "$ARGUMENTS", max_results: 15, time_range: "month"
2. query: "$ARGUMENTS funding acquisition investment", max_results: 10, time_range: "month"

## Step 3: Community & Practitioner Signals

Use `social_search` twice:
1. query: "$ARGUMENTS", platforms: ["reddit", "hackernews", "producthunt"], max_results_per_platform: 15, time_filter: "year"
2. query: "$ARGUMENTS vs OR alternative OR comparison OR best", platforms: ["reddit", "hackernews"], max_results_per_platform: 10

## Step 4: Open Source Ecosystem

Use `github_search` twice:
1. query: "$ARGUMENTS", sort: "stars", max_results: 15
2. query: "$ARGUMENTS", sort: "updated", max_results: 10

## Step 5: Key Player Deep Dives

For the top 3 companies/projects identified, use `content_operations`:
- operation: "retrieve", url: <player_url>, extraction_method: "markdown"
- operation: "analyze", content: <retrieved>, analysis_type: "business", extract_key_points: true

## Step 6: Academic Foundation

Use `scientific_research`:
- operation: "academic_search"
- query: "$ARGUMENTS"
- max_results: 5
- sources: ["semantic_scholar", "arxiv"]

## Step 7: Compile Report

1. **Market Overview** -- Definition, scope, current state
2. **Market Size & Growth** -- Sizing data, growth rates, projections
3. **Key Players** -- Major companies and products with brief profiles
4. **Competitive Landscape** -- How players are positioned
5. **Technology Trends** -- Emerging tech, OSS momentum, developer adoption
6. **Investment & M&A Activity** -- Funding, acquisitions, partnerships
7. **Community Signals** -- Practitioner discussions, sentiment, preferences
8. **Opportunities & Whitespace** -- Underserved segments, unmet needs
9. **Risks & Headwinds** -- Challenges, regulatory concerns, saturation
10. **Outlook** -- 6-12 month forward assessment
11. **Sources** -- All URLs and references

Use tables for player comparisons. Cite sources inline.
