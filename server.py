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
from src.tools.entity import register_entity_tools
from src.tools.github_tool import register_github_tools
from src.tools.news import register_news_tools
from src.tools.pdf_tool import register_pdf_tools
from src.tools.quality import register_quality_tools

# from src.tools.trends import register_trends_tools  # REMOVED - Google rate limits
from src.tools.research import register_research_tools
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
Professional research and content discovery MCP server with AI agent.

🎯 CORE PURPOSE:
Comprehensive research across 20+ data sources including web search, social media,
news, GitHub, academic papers, and documents with OCR. Features an AI research agent
that autonomously uses 7 tools to generate in-depth reports.

🔗 RESEARCH WORKFLOW:
1. web_search → Find URLs and information
2. content_operations → Retrieve full content from URLs
3. document_analysis → Extract text from PDFs/documents
4. research_agent → AI generates comprehensive reports

💡 TOOL INTEGRATION:
Each search tool provides hints for next steps. Follow the suggested workflows
for best results. The AI agent (research_agent) can orchestrate multi-tool
research automatically.

🛠️  AVAILABLE TOOLS (10 Total):
Search & Discovery:
- web_search: Search across DuckDuckGo, Yahoo, and Wikipedia (3 engines, NO AUTH)
- map_website: Intelligent website exploration and mapping
- social_search: Search Reddit, Hacker News, Dev.to, Product Hunt, Medium (NO AUTH)
- news_aggregation: Aggregate news from Google, DuckDuckGo, Yahoo News (NO AUTH)
- github_search: Search GitHub repositories with rate limiting (NO AUTH)

Content Analysis:
- content_operations: Consolidated retrieve, stream, analyze, and extract operations
- research_topic: End-to-end research workflow for topics
- document_analysis: Extract text from PDF, Word, Text, Images with OCR (NO AUTH, 50MB)

Research & Scientific:
- scientific_research: Academic paper and dataset discovery (NO AUTH)
- research_agent: AI research agent with autonomous tool calling (8 tools available)

📋 USAGE PATTERNS:

1. **Quick Search**: web_search → Get URLs → content_operations → Retrieve content
2. **Social Research**: social_search → Find discussions → research_agent → Synthesize
3. **News Analysis**: news_aggregation → Get articles → content_operations → Full text
4. **Code Research**: github_search → Find repos → map_website → Explore docs
5. **Academic**: scientific_research → Find papers → document_analysis → Extract PDFs
6. **Comprehensive**: research_agent → AI orchestrates all tools automatically

💡 BEST PRACTICES:
- Follow "Next Steps" hints in tool outputs for guided workflows
- Use research_agent for complex multi-source research
- Combine tools: search → retrieve → analyze
- All tools work without authentication (except research_agent needs OpenRouter)

🚀 PERFORMANCE:
- Multi-engine search with automatic fallbacks
- OCR auto-downloads models on first use (~100MB)
- GitHub rate limiting: 60 requests/hour
- EasyOCR for images and scanned documents
- All tools provide progress reporting

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
register_research_tools(app)
register_scientific_tools(app)
register_social_media_tools(app)
register_news_tools(app)
register_github_tools(app)
register_pdf_tools(app)
register_quality_tools(app)
register_entity_tools(app)
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
