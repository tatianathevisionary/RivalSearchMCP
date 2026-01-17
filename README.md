# RivalSearchMCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
![MCP Server](https://img.shields.io/badge/MCP-Server-blue?style=for-the-badge)
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

RivalSearchMCP provides comprehensive tools for accessing web content, performing multi-engine searches across Yahoo and DuckDuckGo, analyzing websites, conducting research workflows, and analyzing trends data. It includes 8 specialized tools organized into key categories for comprehensive web research capabilities.

## ✅ Why It's Useful

- Access web content and perform searches with anti-detection measures
- Analyze website content and structure with intelligent crawling
- Conduct end-to-end research workflows with progress tracking
- Analyze trends data with comprehensive export options
- Generate LLMs.txt documentation files for websites
- Integrate with AI assistants for enhanced web research

## 💡 Example Query

Once connected, try asking your AI assistant:

> "Use rival-search-mcp to research trends for AI agents and automation workflows in 2026. Search for the latest developments, analyze how interest has changed over time, compare regional adoption, find related emerging topics, and export the findings to a report."

## 📦 How to Get Started

RivalSearchMCP runs as a **remote MCP server** hosted on FastMCP. Just follow the steps below to install, and go.

### Connect to Live Server

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en-US/install-mcp?name=RivalSearchMCP&config=eyJ1cmwiOiJodHRwczovL1JpdmFsU2VhcmNoTUNQLmZhc3RtY3AuYXBwL21jcCJ9)

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

## 🛠 Available Tools (8 Total)

### Search & Discovery
- `multi_search` — Multi-engine search across Yahoo and DuckDuckGo with content extraction and intelligent fallbacks

### Content Operations
- `content_operations` — Consolidated tool for retrieving, streaming, analyzing, and extracting content from URLs

### Website Analysis
- `traverse_website` — Intelligent website exploration with research, documentation, and mapping modes

### Trends Analysis (2 tools)
- `trends_core` — Google Trends analysis with search, related queries, regional data, and comparisons
- `trends_export` — Export trends data in CSV, JSON, and SQL formats

### Research Workflows (2 tools)
- `research_topic` — End-to-end research workflow for comprehensive topic analysis
- `research_workflow` — AI-enhanced research with OpenRouter integration and progress tracking

### Scientific Research
- `scientific_research` — Academic paper search and dataset discovery across arXiv, Semantic Scholar, PubMed, Kaggle, and Hugging Face

## ⚡ Key Features

- **Multi-Engine Search**: Intelligent search across Yahoo and DuckDuckGo with automatic fallbacks
- **Content Processing**: Advanced content extraction and analysis with OCR support
- **AI-Enhanced Research**: OpenRouter integration for AI-powered insights and research assistance
- **Scientific Discovery**: Academic paper and dataset search across major repositories
- **Progress Tracking**: Real-time progress reporting for long-running operations
- **Data Export**: Multiple format support (CSV, JSON, SQL) for trends data
- **Intelligent Crawling**: Smart website traversal with configurable depth and modes

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
<summary><strong>What MCP clients are supported?</strong></summary>

RivalSearchMCP works with any MCP-compatible client including Claude Desktop, Cursor, VS Code, and Claude Code.
</details>

<details>
<summary><strong>Can I self-host this?</strong></summary>

Absolutely! Clone the repo, install dependencies, and run `python server.py`. Full instructions are in the Getting Started section above.
</details>

## 📚 Documentation

For detailed guides and examples, visit the **[Full Documentation](https://damionrashford.github.io/RivalSearchMCP)**.

## 🤝 Contributing

Contributions are welcome! Whether it's fixing bugs, adding new research tools, or improving documentation, your help is appreciated.

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

## 💡 Issues, Feedback & Support

Found a bug, have a feature request, or want to share how you're using RivalSearchMCP? We'd love to hear from you!

- **Report a bug** — Help us improve by reporting issues
- **Request a feature** — Suggest new capabilities you'd find useful
- **Share your use case** — Tell us how you're using RivalSearchMCP

👉 **[Open an Issue](https://github.com/damionrashford/RivalSearchMCP/issues)**

## Attribution & License

This is an open source project under the **MIT License**. If you use RivalSearchMCP, please credit it by linking back to [RivalSearchMCP](https://github.com/damionrashford/RivalSearchMCP). See [LICENSE](LICENSE) file for details.

## ⭐ Like this project? Give it a star!

If you find RivalSearchMCP useful, please consider giving it a star. It helps others discover the project and motivates continued development!

[![Star this repo](https://img.shields.io/github/stars/damionrashford/RivalSearchMCP?style=social)](https://github.com/damionrashford/RivalSearchMCP)
