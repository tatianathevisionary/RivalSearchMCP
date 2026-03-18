# Research & Scientific Tools

## research_topic

End-to-end research workflow for a topic. Combines search, content retrieval, and analysis into a single operation.

```bash
uv run --with fastmcp python cli.py call-tool research_topic --topic <value> --sources <value> --max-sources <value> --include-analysis
```

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--topic` | string | yes | — | Research topic |
| `--sources` | JSON string | no | null | List of specific sources to use |
| `--max-sources` | integer | no | 5 | Maximum number of sources to research |
| `--include-analysis` | boolean | no | true | Include content analysis |

**Example:**
```bash
python cli.py call-tool research_topic --topic "LLM agent frameworks comparison" --max-sources 10
```

---

## scientific_research

Academic paper and dataset discovery across multiple sources. No authentication required.

```bash
uv run --with fastmcp python cli.py call-tool scientific_research --operation <value> --query <value> --max-results <value> --sources <value> --categories <value>
```

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--operation` | string | yes | — | "academic_search" or "dataset_discovery" |
| `--query` | string | yes | — | Search query |
| `--max-results` | integer | no | 10 | Maximum results to return |
| `--sources` | JSON string | no | null | Specific sources to search |
| `--categories` | JSON string | no | null | Categories for dataset discovery |

### Operations

**academic_search** — Search papers across Semantic Scholar, arXiv, PubMed:
```bash
python cli.py call-tool scientific_research --operation academic_search --query "transformer attention mechanisms" --sources '["arxiv", "semantic_scholar"]'
```

**dataset_discovery** — Find datasets on Kaggle, HuggingFace:
```bash
python cli.py call-tool scientific_research --operation dataset_discovery --query "sentiment analysis" --sources '["huggingface", "kaggle"]'
```

---

## research_agent

AI research agent using OpenRouter with autonomous tool calling. Orchestrates multiple tools to generate comprehensive reports. Requires `OPENROUTER_API_KEY` environment variable.

```bash
uv run --with fastmcp python cli.py call-tool research_agent --topic <value> --max-sources <value> --research-depth <value> --ai-model <value>
```

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--topic` | string | yes | — | Research topic to investigate |
| `--max-sources` | integer | no | 15 | Maximum sources to analyze |
| `--include-trends` | boolean | no | true | Include trends analysis |
| `--include-website-analysis` | boolean | no | true | Include website traversal |
| `--research-depth` | string | no | comprehensive | Depth: "quick", "standard", "comprehensive" |
| `--ai-model` | string | no | meta-llama/llama-3.1-8b-instruct:free | OpenRouter model (auto-fallback to 4+ free models) |
| `--enable-ai-insights` | boolean | no | true | Generate AI-powered insights |

**Example:**
```bash
python cli.py call-tool research_agent --topic "competitive analysis of MCP servers" --research-depth comprehensive --max-sources 20
```

**Note:** This is the only tool that requires an API key. Set `OPENROUTER_API_KEY` in your environment. Without it, the tool gracefully degrades.
