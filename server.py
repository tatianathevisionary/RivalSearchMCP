#!/usr/bin/env python3
"""
RivalSearchMCP Server - Advanced Web Research and Content Discovery
"""

import os
from fastmcp import FastMCP

# Import modular tool registration functions

from src.tools.search import register_search_tools
from src.tools.traversal import register_traversal_tools
from src.tools.analysis import register_analysis_tools
from src.tools.trends import register_trends_tools
from src.tools.research import register_research_tools
from src.tools.scientific import register_scientific_tools

# Import prompts
from src.prompts import register_prompts

# Import resources
from src.resources import register_resources

# Import middleware
from src.middleware import register_middleware

# Import custom routes
from src.routes.routes import register_custom_routes

# Import logger
from src.logging.logger import logger

# Environment-based configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Comprehensive server instructions
SERVER_INSTRUCTIONS = """
Advanced web research and content discovery MCP server.

CAPABILITIES:
- Multi-engine search across Yahoo and DuckDuckGo with intelligent fallbacks
- Google Trends analysis with data export (CSV, JSON, SQL)
- Website traversal and structure analysis with intelligent crawling
- Content extraction and processing with OCR support
- Scientific research tools for academic and dataset discovery
- AI-enhanced research workflows with OpenRouter integration

AVAILABLE TOOLS (8 Total):
Search & Discovery:
- multi_search: Multi-engine search across Yahoo and DuckDuckGo with content extraction
- traverse_website: Intelligent website exploration and mapping

Content Analysis:
- content_operations: Consolidated retrieve, stream, analyze, and extract operations
- research_topic: End-to-end research workflow for topics

Trends & Analytics:
- trends_core: Google Trends analysis with search, related queries, and regional data
- trends_export: Export trends data in multiple formats

Research & Scientific:
- scientific_research: Academic paper and dataset discovery
- research_workflow: AI-enhanced comprehensive research with progress tracking

USAGE PATTERNS:
1. Basic Research: Use multi_search for simple queries across Yahoo/DuckDuckGo
2. Trend Analysis: Use trends_core + trends_export for market research
3. Content Discovery: Use traverse_website + content_operations for deep analysis
4. Scientific Research: Use scientific_research for academic papers and datasets
5. Comprehensive Research: Use research_workflow for AI-enhanced multi-phase research

BEST PRACTICES:
- Provide specific, detailed search queries for better results
- Use appropriate result limits (10-20 for search, 100+ for trends)
- Combine multiple tools for comprehensive research workflows
- Use trends tools for market research and content strategy
- Leverage traversal tools for website analysis and mapping

PERFORMANCE NOTES:
- Multi-engine search with automatic fallbacks for reliability
- Trends analysis supports multiple timeframes and geographic regions
- Content analysis includes OCR for image text extraction
- All tools provide progress reporting and detailed logging
- AI-enhanced research tools include multi-phase progress tracking

MONITORING & HEALTH:
- Health check endpoint: /health
- Performance metrics: /metrics
- Server status: /status
- Tools information: /tools
- Performance analysis: /performance
"""

# Create enhanced FastMCP server instance
app = FastMCP(
    name="RivalSearchMCP",
    instructions=SERVER_INSTRUCTIONS,
    include_fastmcp_meta=True,  # Enable rich metadata
    on_duplicate_tools="error",  # Prevent conflicts
    on_duplicate_resources="warn",
    on_duplicate_prompts="replace",
)

# Register middleware for production readiness
register_middleware(app)

# Register all tools using modular approach

register_search_tools(app)
register_traversal_tools(app)
register_analysis_tools(app)
register_trends_tools(app)
register_research_tools(app)
register_scientific_tools(app)
# OCR functionality is integrated into retrieval tools - no separate registration needed

# Register prompts
register_prompts(app)

# Register resources
register_resources(app)

# Register custom routes
register_custom_routes(app)

# Start background tasks that require event loop
from src.middleware.middleware import start_background_tasks
start_background_tasks()

if __name__ == "__main__":
    if ENVIRONMENT == "production":
        logger.info(f"Starting RivalSearchMCP in production mode on port {PORT}")
        app.run(transport="http", host="0.0.0.0", port=PORT, log_level=LOG_LEVEL)
    else:
        logger.info("Starting RivalSearchMCP in development mode (stdio)")
        # For CLI compatibility, run directly with STDIO transport
        app.run()
