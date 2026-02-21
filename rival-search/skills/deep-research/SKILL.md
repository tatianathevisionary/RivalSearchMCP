---
name: deep-research
description: Comprehensive multi-source research on any topic. Searches the web, social platforms, news outlets, and academic databases, then synthesizes findings into a structured research report.
---

# Deep Research

Conduct comprehensive multi-source research on: **$ARGUMENTS**

Follow these steps precisely using the RivalSearchMCP tools. Report progress after each step.

## Step 1: Web Search

Use `web_search` for broad discovery:
- query: "$ARGUMENTS"
- num_results: 15
- extract_content: true
- follow_links: true
- max_depth: 2

Identify the top 3-5 most relevant URLs. Note key themes and recurring sources.

## Step 2: Social Media Pulse

Use `social_search` to gauge community discussions:
- query: "$ARGUMENTS"
- platforms: ["reddit", "hackernews", "devto", "producthunt", "medium"]
- max_results_per_platform: 10
- time_filter: "year"

Analyze what practitioners are saying. Note consensus, debate, and emerging opinions.

## Step 3: News Coverage

Use `news_aggregation` for recent developments:
- query: "$ARGUMENTS"
- max_results: 15
- time_range: "month"

Identify breaking news, announcements, and trend shifts.

## Step 4: Academic Literature

Use `scientific_research` for peer-reviewed sources:
- operation: "academic_search"
- query: "$ARGUMENTS"
- max_results: 10
- sources: ["semantic_scholar", "arxiv"]

Look for foundational research and recent publications.

## Step 5: Deep Content Retrieval

For the 2-3 most important URLs from Steps 1-3, use `content_operations`:
- operation: "retrieve", url: <selected_url>, extraction_method: "markdown"

Then analyze the retrieved content:
- operation: "analyze", content: <retrieved>, analysis_type: "general", extract_key_points: true, summarize: true

## Step 6: Synthesize Report

Compile all findings into a structured report:

1. **Executive Summary** -- 2-3 paragraph overview
2. **Key Findings** -- Numbered list of discoveries, cross-referenced across sources
3. **Web Intelligence** -- Mainstream sources (Step 1)
4. **Community Sentiment** -- Practitioner discussions (Step 2)
5. **Recent Developments** -- News and current events (Step 3)
6. **Academic Foundation** -- Research literature (Step 4)
7. **Deep Dive Insights** -- Detailed analysis (Step 5)
8. **Contradictions & Gaps** -- Where sources disagree or information is missing
9. **Sources** -- Complete list of all URLs consulted

Use clean markdown. Cite sources inline with [Source Name](URL) format.
