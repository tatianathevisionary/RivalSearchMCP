#!/usr/bin/env python3
"""
RivalSearchMCP Server - Advanced Web Research and Content Discovery
"""

import os

from fastmcp import FastMCP

# Import logger
from src.logging.logger import logger

# Import middleware
from src.middleware import register_middleware
from src.middleware.cors_validation import CORSOriginValidationMiddleware
from src.middleware.null_id_validation import NullIdValidationMiddleware

# Import prompts
from src.prompts import register_prompts

# Import custom routes
from src.routes.routes import register_custom_routes
from src.tools.analysis import register_analysis_tools
from src.tools.conflict import register_conflict_tools
from src.tools.entity import register_entity_tools
from src.tools.github_tool import register_github_tools
from src.tools.memory import register_memory_tools
from src.tools.news import register_news_tools
from src.tools.pdf_tool import register_pdf_tools
from src.tools.quality import register_quality_tools

# from src.tools.trends import register_trends_tools  # REMOVED - Google rate limits
# research_agent (LLM-driven agent) was removed - RivalSearchMCP ships as
# a deterministic research layer; LLM orchestration belongs in the caller.
from src.tools.scientific import register_scientific_tools
from src.tools.search import register_search_tools
from src.tools.social_media import register_social_media_tools
from src.tools.traversal import register_traversal_tools

# Import modular tool registration functions


# Environment-based configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Comprehensive server instructions
SERVER_INSTRUCTIONS = """
Deterministic research and content-discovery MCP server. No LLM is run
inside the server itself — every tool returns structured, auditable
output that the caller's model (or a human) can reason over.

🎯 CORE PURPOSE:
Fan out across dozens of keyless data sources — web search, social
communities, news, GitHub, academic papers, datasets, PDFs — and
return results with per-item quality scores plus an aggregate
confidence signal so callers can calibrate trust rather than treating
all results as equal.

🛠️  AVAILABLE TOOLS:

Search & Discovery:
- web_search: DuckDuckGo + Bing + Yahoo + Mojeek + Wikipedia (no auth)
- map_website: Structured website crawling (research / docs / map modes)
- social_search: Reddit, Hacker News, Dev.to, Product Hunt, Medium,
                 Stack Overflow, Bluesky, Lobste.rs, Lemmy (no auth)
- news_aggregation: Google News, Bing News, Guardian, GDELT, DuckDuckGo
                    News, with a `time_range` freshness filter (no auth)
- github_search: GitHub repositories via the public search API
- scientific_research: OpenAlex, CrossRef, arXiv, PubMed, Europe PMC for
                       papers; Kaggle, HuggingFace, Zenodo, Harvard
                       Dataverse for datasets (no auth)

Content Analysis:
- content_operations: Retrieve / stream / analyze / extract-links on URLs
- research_topic: End-to-end deterministic research orchestration
- document_analysis: PDF, DOCX, text, images (OCR) — up to 50MB

Trust & Synthesis:
- score_sources: Rate a list of URLs on four auditable signals
                 (domain_tier, freshness, corroboration, citations)
                 with a coarse confidence summary
- entity_research: Unified cross-source profile of a named entity
                   (company, product, person, project, technology)
- find_conflicts: Rule-based detection of numeric, date, and polarity
                  disagreements between source snippets

📋 USAGE PATTERNS:

1. Quick search: web_search → content_operations → document_analysis
2. Entity profile: entity_research (single call fans out everywhere)
3. Trust check: score_sources on a list of URLs before acting
4. Conflict check: find_conflicts when sources appear to disagree
5. Academic: scientific_research → document_analysis on PDF links
6. Topical: research_topic → content_operations on top sources

💡 BEST PRACTICES:
- Follow "Next Steps" hints in tool outputs for guided workflows
- Treat confidence="low" in any output as a cue to cross-check
- Combine tools: search → retrieve → analyze → score

🚀 PERFORMANCE:
- Multi-source tools fan out concurrently (asyncio.gather)
- Per-source failures are isolated; other sources still populate output
- Scrapling-backed search engines resist Cloudflare TLS fingerprinting
- GitHub rate limiting: 60 requests/hour unauthenticated

📊 MONITORING:
- Health: /health
- Metrics: /metrics
- Status: /status
- Tools: /tools
"""

# Create enhanced FastMCP server instance
app = FastMCP(
    name="RivalSearchMCP",
    instructions=SERVER_INSTRUCTIONS,
    include_fastmcp_meta=True,  # Enable rich metadata
    on_duplicate_tools="error",  # Prevent conflicts
)

# Register middleware for production readiness
register_middleware(app)

# Register all tools using modular approach

register_search_tools(app)
register_traversal_tools(app)
register_analysis_tools(app)
# register_trends_tools(app)  # REMOVED - Google rate limits
# register_research_tools(app)  # REMOVED - research_agent was LLM-driven
register_scientific_tools(app)
register_social_media_tools(app)
register_news_tools(app)
register_github_tools(app)
register_pdf_tools(app)
register_quality_tools(app)
register_entity_tools(app)
register_conflict_tools(app)
register_memory_tools(app)
# OCR functionality is integrated into retrieval tools - no separate registration needed

# Register prompts
register_prompts(app)

# Register custom routes
register_custom_routes(app)

# Start background tasks that require event loop
from src.middleware.middleware import start_background_tasks  # noqa: E402

start_background_tasks()


def _wrap_http_app_with_security_middleware():
    """Ensure HTTP-level security middleware is applied for all deployments.

    FastMCP Cloud/Horizon calls app.http_app() directly (ignores __main__),
    so we wrap it to always include our HTTP-level validation middleware.

    Middleware order (outermost → innermost):
      1. CORSOriginValidationMiddleware  – blocks untrusted origins (MUST per spec)
      2. NullIdValidationMiddleware       – rejects id: null requests
      3. … FastMCP / Starlette internals
    """
    from starlette.middleware import Middleware

    _original_http_app = app.http_app

    def _http_app(**kwargs):
        middleware = list(kwargs.pop("middleware", None) or [])
        # Insert in reverse order so the first entry runs outermost
        middleware.insert(0, Middleware(NullIdValidationMiddleware))
        middleware.insert(0, Middleware(CORSOriginValidationMiddleware))
        return _original_http_app(middleware=middleware, **kwargs)

    app.http_app = _http_app


_wrap_http_app_with_security_middleware()

if __name__ == "__main__":
    if ENVIRONMENT == "production":
        logger.info(f"Starting RivalSearchMCP in production mode on port {PORT}")
        app.run(transport="http", host="0.0.0.0", port=PORT, log_level=LOG_LEVEL)
    else:
        logger.info("Starting RivalSearchMCP in development mode (stdio)")
        # For CLI compatibility, run directly with STDIO transport
        app.run()
