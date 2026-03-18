# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RivalSearchMCP is an MCP server providing 10 specialized tools for web research, content discovery, and analysis. Built on FastMCP, it offers multi-engine search (Yahoo/DuckDuckGo), website traversal, scientific research, and AI-enhanced research workflows. Ships with Claude Code Agent Skills for standalone CLI usage.

- **100% free**: No API keys required for core functionality
- **Dual deployment**: Hosted service at `https://RivalSearchMCP.fastmcp.app/mcp` or local development
- **Transport modes**: stdio (default, for CLI/IDE) or HTTP (production via `ENVIRONMENT=production`)

## Development Commands

### Setup & Running
```bash
# Install dependencies
pip install -r requirements.txt

# Install with dev dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install

# Run server (stdio mode - default for MCP clients)
python server.py

# Run in production mode (HTTP transport)
ENVIRONMENT=production python server.py

# Custom port
PORT=8080 ENVIRONMENT=production python server.py
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run specific test function
pytest tests/test_client.py::test_function_name

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Filter by markers
pytest -m unit           # Only unit tests
pytest -m integration    # Only integration tests
pytest -m "not slow"     # Skip slow tests

# Verbose with short traceback
pytest -v --tb=short
```

### Code Quality
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint with auto-fix
ruff check --fix src/ tests/

# Type checking
mypy src/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Documentation
```bash
# Serve locally at http://127.0.0.1:8000
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Architecture

### High-Level Structure

RivalSearchMCP uses a **modular tool-based architecture** where each tool category registers MCP tools with the FastMCP app in `server.py`. The architecture separates tool interfaces from core business logic:

```
src/
├── tools/          # MCP tool implementations (10 tools)
│   ├── analysis.py       # content_operations tool
│   ├── multi_search.py   # multi_search tool
│   ├── research.py       # research_topic tool
│   ├── scientific.py     # scientific_research tool
│   ├── search.py         # Tool registration orchestration
│   ├── traversal.py      # traverse_website tool
│   ├── trends.py         # trends_core, trends_export tools
│   └── research_modules/ # AI-enhanced research (OpenRouter integration)
├── core/           # Core business logic (reusable, not MCP-specific)
│   ├── search/     # Multi-engine search orchestration
│   ├── content/    # Extraction, parsing, cleaning (6-tier fallback)
│   ├── trends/     # Google Trends API wrapper
│   ├── scientific/ # Academic search (arXiv, PubMed, Semantic Scholar, etc.)
│   ├── traverse/   # Website crawling logic
│   ├── bypass/     # Anti-detection, proxy handling
│   └── security/   # Rate limiting, IP filtering
├── middleware/     # FastMCP middleware (timing, security, metrics)
├── schemas/        # Pydantic validation schemas
└── utils/          # Shared utilities (content, parsing, headers, etc.)
```

### Key Architectural Patterns

**Tool Registration Pattern:**
Each `src/tools/<category>.py` exports a `register_<category>_tools(app: FastMCP)` function that decorates tool implementations and registers them with the FastMCP app. All registration functions are called in `server.py` (lines 109-116).

Example pattern:
```python
def register_search_tools(app: FastMCP):
    @app.tool(name="multi_search", description="...")
    async def multi_search(query: str, ...) -> SearchResults:
        # Uses core modules from src/core/search/
        pass
```

**Multi-Engine Search Architecture:**
- Core implementation: `src/core/search/core/multi_engines.py`
- Concurrent execution across Yahoo and DuckDuckGo using asyncio
- Automatic fallback when individual engines fail
- Result deduplication by URL via `MultiSearchResult` class
- Intelligent merging of results from multiple sources

**Content Processing Pipeline:**
- 6-tier fallback system in `src/core/content/extractors.py`
- HTML → Markdown conversion via `src/utils/content.py::clean_html_to_markdown()`
- Parser preference: selectolax (fastest) > lxml > html.parser
- BeautifulSoup4 used for robustness with lxml backend

**AI Integration (Optional):**
- OpenRouter integration in `src/tools/research_modules/`
- Used by `research_workflow` tool for AI-enhanced research
- Model selection via `OPENROUTER_MODEL` env var (default: `nvidia/nemotron-3-nano-30b-a3b:free`)
- Requires `OPENROUTER_API_KEY` for AI features
- Graceful degradation when API key not provided

**Middleware Stack:**
Registered in `src/middleware/middleware.py::register_middleware()`:
- `TimingMiddleware` - Logs slow operations (>1000ms threshold)
- `SecurityMiddleware` - Rate limiting and IP filtering
- `MetricsMiddleware` - Usage analytics and performance tracking

### Critical Implementation Details

**FastMCP Configuration (server.py:96-104):**
```python
app = FastMCP(
    name="RivalSearchMCP",
    instructions=SERVER_INSTRUCTIONS,
    include_fastmcp_meta=True,      # Rich metadata enabled
    on_duplicate_tools="error",      # Prevents tool conflicts
    on_duplicate_resources="warn",
    on_duplicate_prompts="replace",
)
```
- stdio transport is default for CLI/IDE compatibility
- HTTP transport enabled when `ENVIRONMENT=production`
- Background tasks started via `start_background_tasks()` at module level

**Dependency Constraints:**
- `urllib3<2.0.0` - Pinned for pytrends compatibility
- `pytrends==4.9.2` - Exact version required for Google Trends
- Use `httpx` for async HTTP requests
- Use `requests` only when synchronous calls required

**Search Engine Compliance:**
- User-agent rotation from `src/config/user_agents.py`
- Rate limiting built into search core
- Anti-detection measures in `src/core/bypass/bypass.py`
- Respects robots.txt and implements delays

**Error Handling Strategy:**
- All tools implement fallback chains (see `src/error/recovery.py`)
- Multi-engine search continues if one engine fails
- Errors logged via `src/logging/logger.py` with context
- Graceful degradation preferred over complete failure

## Environment Variables

All environment variables are optional - the system works without any configuration:

- `OPENROUTER_API_KEY` - Enables AI-enhanced research features
- `OPENROUTER_MODEL` - Override default AI model selection
- `ENVIRONMENT` - Set to `production` for HTTP transport
- `PORT` - Server port for HTTP mode (default: 8000)
- `LOG_LEVEL` - Logging verbosity (default: INFO)

## Testing Configuration

**pytest.ini configuration:**
- Test directory: `tests/`
- Coverage minimum: 80% (`--cov-fail-under=80`)
- Async mode: auto (pytest-asyncio handles async/await)
- Test markers: `unit`, `integration`, `slow`

**Coverage exclusions:**
- Test files (`*/tests/*`, `*/test_*.py`)
- Package `__init__.py` files
- Abstract methods and Protocol classes
- Debug statements and `if __name__ == '__main__'` blocks

## Workflow: Adding New Tools

1. **Create tool function** in `src/tools/<category>.py`
   - Use async def for I/O operations
   - Accept Pydantic models for input validation

2. **Define schemas** in `src/schemas/<category>.py`
   - Use Pydantic BaseModel for type safety
   - Include descriptions for MCP metadata

3. **Implement core logic** in `src/core/<category>/`
   - Keep MCP-agnostic (reusable outside MCP context)
   - Implement error handling and fallbacks

4. **Register tool** - Add `register_<category>_tools(app)` call in `server.py`
   - Insert around lines 109-116 with other registrations

5. **Write tests** in `tests/test_<category>.py`
   - Use pytest-asyncio for async tools
   - Aim for 80%+ coverage

6. **Update README** - Increment tool count if adding new tool (currently 10 total)

7. **Update Agent Skill** - If the new tool should be exposed via the CLI, regenerate:
   ```bash
   fastmcp generate-cli https://RivalSearchMCP.fastmcp.app/mcp skills/rival-search-mcp/cli.py -f
   ```
   Then update `skills/rival-search-mcp/SKILL.md` and the relevant resource file in `skills/rival-search-mcp/resources/`.

## Agent Skills

RivalSearchMCP ships with a Claude Code Agent Skill in `skills/rival-search-mcp/`. This packages all 10 tools as a standalone CLI that agents can invoke directly.

### Structure
```
skills/rival-search-mcp/
├── SKILL.md              # Agent instructions (loaded when skill triggers)
├── scripts/
│   └── cli.py            # Self-contained CLI (PEP 723 inline deps, runs with uv)
└── resources/
    ├── search.md         # web_search, social_search, news_aggregation, github_search, map_website
    ├── content.md        # content_operations, document_analysis
    └── research.md       # research_topic, scientific_research, research_agent
```

### How it works
- `SKILL.md` tells the agent what tools exist and how to invoke them via `scripts/cli.py`
- `scripts/cli.py` was generated by `fastmcp generate-cli` and connects to the live server at `https://RivalSearchMCP.fastmcp.app/mcp`
- Resource files in `resources/` provide detailed flag reference (only loaded when the agent needs specifics)
- The CLI is self-contained with PEP 723 inline dependencies — `uv run scripts/cli.py` just works

### Regenerating the CLI
```bash
fastmcp generate-cli https://RivalSearchMCP.fastmcp.app/mcp skills/rival-search-mcp/cli.py -f
```

## Code Style Standards

Enforced via pre-commit hooks:

- **Line length:** 100 characters (black)
- **Type hints:** Required for all function signatures (mypy with strict flags)
- **Import sorting:** isort with black profile
- **Linting:** ruff with E, W, F, I, B, C4, UP rules
- **Security:** bandit for security checks (excluding tests/)
- **Python version:** 3.9+ (target-version in pyproject.toml)

## Performance Considerations

- **Async/await required** for all I/O operations (HTTP, file I/O)
- **Connection pooling** via httpx for HTTP requests
- **Timing middleware** automatically logs operations >1000ms
- **Cache manager** in `src/core/cache/` for repeated requests
- **Fast parsers** used when available (selectolax > lxml > html.parser)
- **Concurrent execution** in multi-engine search via asyncio.gather()
