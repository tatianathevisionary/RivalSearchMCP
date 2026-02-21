# rival-search

A Claude Code plugin that connects you to [RivalSearchMCP](https://rivalsearchmcp.com) — 10 free research tools, 5 workflow skills, and 2 specialized agents. Zero API keys required.

## Installation

```bash
claude plugin add /path/to/rival-search
```

Or clone and install from the repo:

```bash
git clone https://github.com/damionrashford/RivalSearchMCP.git
claude plugin add ./RivalSearchMCP/rival-search
```

## What You Get

### 10 Research Tools (via MCP)

The plugin auto-connects to the hosted RivalSearchMCP server. All tools are available immediately — no setup needed.

| Tool | Description |
|------|-------------|
| `web_search` | Search across DuckDuckGo, Yahoo, and Wikipedia |
| `social_search` | Search Reddit, Hacker News, Dev.to, Product Hunt, Medium |
| `news_aggregation` | Aggregate news from Google, DuckDuckGo, Yahoo News |
| `github_search` | Search GitHub repositories |
| `scientific_research` | Academic papers (arXiv, Semantic Scholar) and datasets (Kaggle, HuggingFace) |
| `content_operations` | Retrieve, analyze, and extract content from web pages |
| `map_website` | Map and explore website structure |
| `document_analysis` | Extract text from PDFs, Word docs, and images (OCR) |
| `research_topic` | End-to-end research workflow |
| `research_agent` | AI research agent with autonomous tool calling |

### 5 Slash-Command Skills

Skills are guided, multi-step research workflows. Each one orchestrates multiple tools in sequence and produces a structured report.

| Command | Description |
|---------|-------------|
| `/rival-search:deep-research <topic>` | Comprehensive multi-source research across web, social, news, and academic databases |
| `/rival-search:competitor-analysis <company>` | Competitive intelligence with SWOT analysis |
| `/rival-search:market-intel <market>` | Market landscape, trends, players, and opportunities |
| `/rival-search:academic-research <topic>` | Literature review with paper search, dataset discovery, and implementations |
| `/rival-search:site-audit <url>` | Full website audit — structure, content, links, and reputation |

#### Examples

```
/rival-search:deep-research AI code generation tools 2025
/rival-search:competitor-analysis Cursor
/rival-search:market-intel developer tools market
/rival-search:academic-research retrieval augmented generation
/rival-search:site-audit https://example.com
```

### 2 Specialized Agents

Agents are automatically invoked by Claude when your task matches their expertise.

| Agent | Specialty |
|-------|-----------|
| **research-analyst** | General-purpose deep research across all 10 tools. Follows a structured methodology: scope, collect, validate, deep-dive, synthesize. |
| **competitive-intel** | Competitive intelligence specialist. Phased framework: reconnaissance, market position, technical assessment, SWOT analysis. |

## How It Works

The plugin bundles three things:

1. **`.mcp.json`** — Connects to the hosted RivalSearchMCP server at `https://RivalSearchMCP.fastmcp.app/mcp`. This gives Claude access to all 10 research tools automatically.

2. **`skills/`** — Five SKILL.md files that define step-by-step research workflows. Each skill uses `$ARGUMENTS` to pass your input into tool calls.

3. **`agents/`** — Two agent definitions that Claude can invoke when research tasks match their expertise.

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- No API keys needed — all tools are free

## Links

- [RivalSearchMCP Website](https://rivalsearchmcp.com)
- [GitHub Repository](https://github.com/damionrashford/RivalSearchMCP)
- [MCP Server Documentation](https://rivalsearchmcp.com/docs)

## License

MIT
