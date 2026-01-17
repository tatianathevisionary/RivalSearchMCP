# RivalSearchMCP Usage Guide

## Overview

RivalSearchMCP provides 8 powerful tools for web research, content discovery, and analysis. This guide shows you how to use each tool effectively.

## Available Tools

### 1. `multi_search` - Multi-Engine Search

Search across Yahoo and DuckDuckGo engines with intelligent fallbacks and content extraction.

**Parameters:**
- `query`: Search query string
- `num_results`: Number of results per engine (default: 10)
- `extract_content`: Whether to extract full page content (default: True)
- `follow_links`: Whether to follow internal links (default: True)
- `max_depth`: Maximum depth for link following (default: 2)
- `use_fallback`: Whether to use fallback strategy (default: True)

**Examples:**
```python
# Basic multi-engine search
multi_search(query="Python programming", num_results=10)

# Deep content extraction
multi_search(
    query="artificial intelligence trends 2024",
    num_results=15,
    extract_content=True,
    follow_links=True,
    max_depth=3
)
```

### 2. `content_operations` - Content Operations

Consolidated tool for retrieving, streaming, analyzing, and extracting content from URLs.

**Parameters:**
- `operation`: Operation type - "retrieve", "stream", "analyze", "extract"
- `url`: URL for retrieve/stream/extract operations
- `content`: Content for analyze operation
- `extraction_method`: For retrieve - "auto", "html", "text", "markdown"
- `analysis_type`: For analyze - "general", "sentiment", "technical", "business"
- `max_links`: For extract - maximum links to extract
- `link_type`: For extract - "all", "internal", "external", "images", "documents"
- `extract_key_points`: For analyze - extract key points
- `summarize`: For analyze - create summary

**Examples:**
```python
# Retrieve content from URL
content_operations(operation="retrieve", url="https://example.com")

# Analyze content
content_operations(
    operation="analyze",
    content="Your content here",
    analysis_type="sentiment",
    extract_key_points=True
)

# Extract links
content_operations(
    operation="extract",
    url="https://example.com",
    link_type="internal"
)
```

### 3. `traverse_website` - Website Traversal

Intelligent website exploration with research, documentation, and mapping modes.

**Parameters:**
- `url`: Website URL to traverse
- `mode`: Traversal mode - "research", "docs", "map" (default: "research")
- `max_pages`: Maximum number of pages to traverse (default: 5)
- `max_depth`: Maximum depth for link following (default: 2)
- `generate_llms_txt`: Whether to generate LLMs.txt documentation (default: False)

**Examples:**
```python
# Research mode exploration
traverse_website(url="https://blog.example.com", mode="research", max_pages=10)

# Documentation exploration
traverse_website(url="https://docs.example.com", mode="docs", max_pages=20)

# Website structure mapping
traverse_website(url="https://competitor.com", mode="map", max_depth=3)
```

### 4. `trends_core` - Google Trends Analysis

Analyze Google Trends data with search, related queries, regional data, and comparisons.

**Parameters:**
- `operation`: Operation type - "search", "related", "interest_over_time", "regional", "compare"
- `keywords`: List of keywords to analyze
- `timeframe`: Time range (default: "today 7-d")
- `geo`: Geographic region code
- `gprop`: Google property
- `resolution`: For regional operations (default: "COUNTRY")

**Examples:**
```python
# Search trends
trends_core(operation="search", keywords=["AI", "machine learning"])

# Get related queries
trends_core(operation="related", keywords=["Python"], timeframe="today 12-m")

# Regional interest analysis
trends_core(operation="regional", keywords=["electric cars"], geo="US")

# Compare multiple keywords
trends_core(operation="compare", keywords=["Python", "JavaScript", "Java"])
```

### 5. `trends_export` - Trends Data Export

Export Google Trends data in CSV, JSON, and SQL formats.

**Parameters:**
- `keywords`: Keywords to export data for
- `timeframe`: Time range (default: "today 7-d")
- `geo`: Geographic region
- `format`: Export format - "csv", "json", "sql" (default: "csv")
- `filename`: Output filename (auto-generated if None)

**Examples:**
```python
# Export to CSV
trends_export(keywords=["AI trends"], format="csv")

# Export to JSON
trends_export(keywords=["Python"], timeframe="today 12-m", format="json")

# Export to SQLite database
trends_export(keywords=["machine learning"], format="sql", filename="ml_trends.db")
```

### 6. `research_topic` - Topic Research

End-to-end research workflow for comprehensive topic analysis.

**Parameters:**
- `topic`: Research topic to investigate
- `sources`: Optional list of specific sources to use
- `max_sources`: Maximum number of sources to research (default: 5)
- `include_analysis`: Whether to include content analysis (default: True)

**Examples:**
```python
# Basic topic research
research_topic(topic="renewable energy trends")

# Research with specific sources
research_topic(
    topic="quantum computing",
    sources=["https://arxiv.org", "https://nature.com"],
    max_sources=10
)
```

### 7. `scientific_research` - Scientific Research

Academic paper search and dataset discovery across multiple repositories.

**Parameters:**
- `operation`: Operation type - "academic_search", "dataset_discovery"
- `query`: Search query
- `max_results`: Maximum number of results (default: 10)
- `sources`: For academic_search - list of sources (default: ["arxiv"])
- `categories`: For dataset_discovery - list of categories

**Examples:**
```python
# Academic paper search
scientific_research(
    operation="academic_search",
    query="machine learning",
    sources=["arxiv", "semantic_scholar"],
    max_results=15
)

# Dataset discovery
scientific_research(
    operation="dataset_discovery",
    query="computer vision",
    categories=["computer_science"],
    max_results=20
)
```

### 8. `research_workflow` - AI-Enhanced Research

Comprehensive AI-powered research workflow with OpenRouter integration.

**Parameters:**
- `topic`: Research topic to investigate
- `max_sources`: Maximum number of sources to analyze (default: 15)
- `include_trends`: Whether to include trends analysis (default: True)
- `include_website_analysis`: Whether to include website traversal (default: True)
- `research_depth`: Depth of research - "basic", "comprehensive", "expert" (default: "comprehensive")
- `ai_model`: OpenRouter AI model (default: "meta-llama/llama-3.1-8b-instruct:free")
- `enable_ai_insights`: Whether to generate AI-powered insights (default: True)

**Examples:**
```python
# Comprehensive AI research
research_workflow(
    topic="AI automation trends 2024",
    research_depth="comprehensive",
    include_trends=True,
    enable_ai_insights=True
)

# Expert-level research
research_workflow(
    topic="quantum computing applications",
    research_depth="expert",
    max_sources=25,
    ai_model="meta-llama/llama-3.3-70b-instruct:free"
)
```



## Common Workflows

### Basic Web Research
```python
# 1. Search for information
results = multi_search(query="your topic", num_results=10)

# 2. Get content from top results
content = content_operations(operation="retrieve", url="https://top-result.com")

# 3. Analyze the content
analysis = content_operations(
    operation="analyze",
    content=content,
    analysis_type="general"
)
```

### Comprehensive Topic Research
```python
# Use the research workflow
research = research_topic(topic="your research topic", max_sources=10)

# Or use AI-enhanced research
ai_research = research_workflow(
    topic="your research topic",
    research_depth="comprehensive",
    enable_ai_insights=True
)
```

### Website Analysis
```python
# Explore a website thoroughly
site_data = traverse_website(url="https://target-site.com", mode="research", max_pages=15)

# Analyze content from the site
analysis = content_operations(
    operation="analyze",
    content="extracted content from site",
    analysis_type="business"
)
```

## Tips for Best Results

1. **Use appropriate tools for your needs:**
    - `multi_search` for web searches across Yahoo and DuckDuckGo
    - `content_operations` for retrieving, analyzing, or extracting content
    - `traverse_website` for exploring entire websites
    - `trends_core` and `trends_export` for Google Trends analysis
    - `research_workflow` for comprehensive AI-enhanced research
    - `scientific_research` for academic papers and datasets

2. **Optimize parameters:**
    - Start with smaller `max_pages` and `max_sources` values and increase as needed
    - Use `extract_content=True` in searches for deeper analysis
    - Enable `use_fallback=True` for more reliable multi-engine searches
    - Choose appropriate `research_depth` for AI research workflows

3. **Combine tools effectively:**
    - Use `multi_search` to find sources, then `content_operations` for details
    - Use `traverse_website` to explore sites, then `content_operations` for insights
    - Use `research_workflow` for comprehensive research projects with AI assistance