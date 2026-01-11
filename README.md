# RivalSearchMCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![MCP Server](https://img.shields.io/badge/MCP-Server-blue?style=for-the-badge)](https://modelcontextprotocol.io)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white&style=for-the-badge)
![FastMCP](https://img.shields.io/badge/FastMCP-Powered-green?style=for-the-badge)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/damion-rashford)

![GitHub Stars](https://img.shields.io/github/stars/damionrashford/RivalSearchMCP?style=social)
![GitHub Forks](https://img.shields.io/github/forks/damionrashford/RivalSearchMCP?style=social)
![GitHub Issues](https://img.shields.io/github/issues/damionrashford/RivalSearchMCP?style=social)
![Last Commit](https://img.shields.io/github/last-commit/damionrashford/RivalSearchMCP?style=social)
![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=damionrashford.RivalSearchMCP)

**Advanced MCP server for web research, content discovery, and trends analysis.**

> 🆓 **100% Free & Open Source** — No API keys, no subscriptions, no rate limits. Just add one URL and go.

## What It Does

RivalSearchMCP provides comprehensive tools for accessing web content, performing multi-engine searches, analyzing websites, conducting research workflows, and analyzing trends data. It includes 6 core tool categories for comprehensive web research capabilities.

## ✅ Why It's Useful

- Access web content and perform searches with anti-detection measures
- Analyze website content and structure with intelligent crawling
- Conduct end-to-end research workflows with progress tracking
- Analyze trends data with comprehensive export options
- Generate LLMs.txt documentation files for websites
- Integrate with AI assistants for enhanced web research

---

## 💡 Example Query

Once connected, try asking your AI assistant:

> "Use rival-search-mcp to research trends for AI agents and automation workflows in 2026. Search for the latest developments, analyze how interest has changed over time, compare regional adoption, find related emerging topics, and export the findings to a report."

---

## 📦 How to Get Started

RivalSearchMCP runs as a **remote MCP server** hosted on FastMCP. Just follow the steps below to install, and go.

### Connect to Live Server

<a href="cursor://anysphere.cursor-deeplink/mcp/install?name=RivalSearchMCP&config=eyJ1cmwiOiJodHRwczovL1JpdmFsU2VhcmNoTUNQLmZhc3RtY3AuYXBwL21jcCJ9"><img src="https://cursor.com/deeplink/mcp-install-dark.png" alt="Install in Cursor" height="32"></a>

Or add this configuration manually:

**For Cursor:**
```json
{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}
```

**For Claude Desktop:**
- Go to Settings → Add Remote Server
- Enter URL: `https://RivalSearchMCP.fastmcp.app/mcp`

**For VS Code:**
- Add the above JSON to your `.vscode/mcp.json` file

**For Claude Code:**
- Use the built-in MCP management: `claude mcp add RivalSearchMCP --url https://RivalSearchMCP.fastmcp.app/mcp`

### Local Development

If you want to run the server locally or contribute:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/damionrashford/RivalSearchMCP.git
   cd RivalSearchMCP
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   # Runs in stdio mode by default (compatible with Claude/IDE MCP clients)
   python server.py
   ```

   To connect your local instance to Claude Desktop, add this to your `claude_desktop_config.json`:
   ```json
   "RivalSearchMCP-local": {
     "command": "python",
     "args": ["/absolute/path/to/RivalSearchMCP/server.py"]
   }
   ```

---

## 🛠 Available Tools

### Search & Discovery (1 tool)
- `web_search` — Advanced web search with Cloudflare bypass, rich snippets detection, and multi-engine fallback

### Content Retrieval (2 tools)
- `retrieve_content` — Enhanced content retrieval from URLs with multiple extraction methods
- `stream_content` — Real-time streaming content processing from WebSocket URLs

### Website Analysis (1 tool)
- `traverse_website` — Intelligent website exploration with different modes (research, docs, map)

### Content Analysis (2 tools)
- `analyze_content` — AI-powered content analysis and insights extraction
- `extract_links` — Link extraction and analysis from web pages

### Trends Analysis (10 tools)
- `search_trends` — Search for trends data for given keywords
- `get_related_queries` — Get related queries for a keyword with interest values
- `get_interest_by_region` — Get interest by geographic region for a keyword
- `get_trending_searches` — Get trending searches for a location
- `export_trends_to_csv` — Export trends data to CSV file
- `export_trends_to_json` — Export trends data to JSON file
- `create_sql_table` — Create SQLite table with trends data
- `compare_keywords_comprehensive` — Comprehensive comparison of multiple keywords
- `get_interest_over_time` — Get interest over time for keywords
- `get_related_topics` — Get related topics for a keyword

### Research Workflows (1 tool)
- `research_topic` — End-to-end research workflow for comprehensive topic analysis

### Documentation Generation (1 tool)
- `generate_llms_txt` — Generate LLMs.txt files for websites following the llmstxt.org specification

---

## ⚡ Key Features

- **Anti-Detection**: Cloudflare bypass and rate limiting for reliable scraping
- **Rich Snippets**: Advanced detection of featured snippets and rich results
- **Multi-Engine Fallback**: Automatic fallback to alternative search engines
- **Progress Tracking**: Real-time progress reporting for long-running operations
- **Data Export**: Multiple format support (CSV, JSON, SQL) for trends data
- **Intelligent Crawling**: Smart website traversal with configurable depth and modes

---

## 🏆 Why RivalSearchMCP?

See how RivalSearchMCP compares to popular alternatives:

| Feature | RivalSearchMCP | Tavily | Perplexity API |
|---------|----------------|--------|----------------|
| **Price** | Free | Paid | Paid |
| **Open Source** | ✅ Yes | ❌ No | ❌ No |
| **Self-Hostable** | ✅ Yes | ❌ No | ❌ No |
| **API Key Required** | ❌ No | ✅ Yes | ✅ Yes |
| **Google Trends** | ✅ Yes | ❌ No | ❌ No |
| **Website Crawling** | ✅ Yes | Limited | ❌ No |
| **Data Export** | CSV, JSON, SQL | JSON | JSON |

---

## 💬 FAQ

<details>
<summary><strong>Is RivalSearchMCP really free?</strong></summary>

Yes! RivalSearchMCP is 100% free and open source under the MIT License. There are no API costs, no subscriptions, and no rate limits. You can use the hosted server or run it locally.
</details>

<details>
<summary><strong>Do I need API keys?</strong></summary>

No. RivalSearchMCP works out of the box without any API keys. Just add the server URL to your MCP client and you're ready to go.
</details>

<details>
<summary><strong>How is this different from Tavily or Perplexity?</strong></summary>

Unlike Tavily and other research APIs that require paid subscriptions, RivalSearchMCP is completely free and open source. You can inspect the code, self-host, and customize it to your needs.
</details>

<details>
<summary><strong>What MCP clients are supported?</strong></summary>

RivalSearchMCP works with any MCP-compatible client including Claude Desktop, Cursor, VS Code, and Claude Code.
</details>

<details>
<summary><strong>Can I self-host this?</strong></summary>

Absolutely! Clone the repo, install dependencies, and run `python server.py`. Full instructions are in the Getting Started section above.
</details>

---

## 📚 Documentation

📖 **[Documentation](https://damionrashford.github.io/RivalSearchMCP)** - Full documentation

**Local Documentation:**
- [User Guide](docs/user-guide/overview.md) - Complete guide to using all tools
- [Examples](docs/examples/basic-usage.md) - Real-world usage examples
- [Installation](docs/getting-started/installation.md) - Setup instructions
- [Quick Start](docs/getting-started/quick-start.md) - Get running in 5 minutes
- [Troubleshooting](docs/getting-started/troubleshooting.md) - Solve common issues

---

## 🤝 Contributing

Contributions are welcome! Whether it's fixing bugs, adding new research tools, or improving documentation, your help is appreciated.

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

Please make sure to update tests as appropriate.

---

## 💡 Issues, Feedback & Support

Found a bug, have a feature request, or want to share how you're using RivalSearchMCP? We'd love to hear from you!

- **Report a bug** — Help us improve by reporting issues
- **Request a feature** — Suggest new capabilities you'd find useful
- **Share your use case** — Tell us how you're using RivalSearchMCP

👉 **[Open an Issue](https://github.com/damionrashford/RivalSearchMCP/issues)**



## Attribution & License

This is an open source project under the **MIT License**. If you use RivalSearchMCP, please credit it by linking back to [RivalSearchMCP](https://github.com/damionrashford/RivalSearchMCP). See [LICENSE](LICENSE) file for details.

---

## ⭐ Like this project? Give it a star!

If you find RivalSearchMCP useful, please consider giving it a star. It helps others discover the project and motivates continued development!

[![Star this repo](https://img.shields.io/github/stars/damionrashford/RivalSearchMCP?style=social)](https://github.com/damionrashford/RivalSearchMCP)

