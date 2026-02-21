---
name: competitor-analysis
description: Analyze a competitor's web presence, social mentions, news coverage, GitHub repositories, and technical footprint. Produces a structured competitive intelligence report.
---

# Competitor Analysis

Conduct competitive intelligence analysis on: **$ARGUMENTS**

The argument may be a company name, product name, or URL. Follow these steps precisely using RivalSearchMCP tools.

## Step 1: Identify the Competitor

If only a name is given, use `web_search` to find their primary website:
- query: "$ARGUMENTS official website"
- num_results: 5
- extract_content: false

## Step 2: Website & Technical Analysis

Map the competitor's website:
- Use `map_website` with url: <competitor_website>, mode: "research", max_pages: 10, max_depth: 2

Note product pages, pricing, features, blog strategy, and technology signals.

## Step 3: Extract Key Pages

Use `content_operations` to retrieve homepage, pricing, and product pages:
- operation: "retrieve", url: <page_url>, extraction_method: "markdown"

Analyze each with:
- operation: "analyze", content: <retrieved>, analysis_type: "business", extract_key_points: true, summarize: true

## Step 4: Social Media Sentiment

Use `social_search`:
- query: "$ARGUMENTS"
- platforms: ["reddit", "hackernews", "devto", "producthunt", "medium"]
- max_results_per_platform: 10
- time_filter: "year"

What do users praise? Complain about? What alternatives do people mention?

## Step 5: News & PR Coverage

Use `news_aggregation`:
- query: "$ARGUMENTS"
- max_results: 15
- time_range: "month"

Also search for funding/partnerships with `web_search`:
- query: "$ARGUMENTS funding OR launch OR partnership OR acquisition"
- num_results: 10

## Step 6: GitHub & Technical Footprint

Use `github_search`:
- query: "$ARGUMENTS"
- sort: "stars"
- max_results: 10
- include_readme: true

Also search for tech stack:
- `web_search` with query: "$ARGUMENTS tech stack OR technology OR architecture"

## Step 7: Ecosystem Analysis

Use `content_operations` to extract outbound links:
- operation: "extract", url: <competitor_website>, link_type: "external", max_links: 50

## Step 8: Compile Report

1. **Company Overview** -- Who they are, market position
2. **Product & Offering Analysis** -- Products, features, pricing
3. **Technical Assessment** -- Tech stack, open source, engineering culture
4. **Market Perception** -- Community sentiment, praise, complaints
5. **News & Momentum** -- Coverage, funding, partnerships, growth signals
6. **Ecosystem & Partnerships** -- Integrations, partner network
7. **Strengths** -- Competitive advantages
8. **Weaknesses** -- Vulnerabilities and pain points
9. **Opportunities** -- Where they can be outperformed
10. **Threats** -- What makes them dangerous
11. **Sources** -- All URLs consulted

Format as clean markdown with inline citations.
