"""
Search tools for FastMCP server.
Handles multi-engine search with Yahoo and DuckDuckGo engines.
"""

from typing import Optional, Annotated
from datetime import datetime

from fastmcp import FastMCP
from fastmcp import Context
from fastmcp.server.context import Context
from pydantic import Field

from src.logging.logger import logger

from src.tools.multi_search import multi_search


def register_search_tools(mcp: FastMCP):
    """Register all search-related tools."""

    # No Google search tool - removed as requested

    @mcp.tool(
        name="multi_search",
        description="Search across Yahoo and DuckDuckGo engines with fallback support",
        tags={"search", "web", "yahoo", "duckduckgo", "multi-engine"},
        meta={
            "version": "1.0",
            "category": "Search",
            "engines": ["yahoo", "duckduckgo"],
        },
        annotations={
            "title": "Multi-Engine Search",
            "readOnlyHint": True,
            "openWorldHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
        },
    )
    async def multi_search_tool(
        ctx: Context,
        query: Annotated[
            str, Field(description="Search query string", min_length=2, max_length=500)
        ],
        num_results: Annotated[
            int,
            Field(description="Number of results per engine", ge=1, le=20, default=10),
        ] = 10,
        extract_content: Annotated[
            bool,
            Field(description="Whether to extract full page content", default=True),
        ] = True,
        follow_links: Annotated[
            bool, Field(description="Whether to follow internal links", default=True)
        ] = True,
        max_depth: Annotated[
            int,
            Field(
                description="Maximum depth for link following", ge=1, le=3, default=2
            ),
        ] = 2,
        use_fallback: Annotated[
            bool, Field(description="Whether to use fallback strategy", default=True)
        ] = True,
    ) -> str:
        """
        Multi-engine search across Yahoo and DuckDuckGo with enhanced security validation.

        This tool searches across multiple engines simultaneously with:
        - Input validation and sanitization
        - Rate limiting protection
        - Content security scanning
        - Comprehensive error handling
        """
        # Security validation
        from src.core.security.security import InputValidator

        validator = InputValidator()

        # Validate query
        valid_query, cleaned_query = validator.validate_search_query(query)
        if not valid_query:
            await ctx.error(f"Query validation failed: {cleaned_query}")
            return f"❌ **Error:** Invalid query: {cleaned_query}"

        # Validate numeric parameters
        valid_num, num_result = validator.validate_numeric_param(num_results, "num_results", 1, 20)
        if not valid_num:
            await ctx.error(f"Parameter validation failed: {num_result}")
            return f"❌ **Error:** {num_result}"

        valid_depth, depth_result = validator.validate_numeric_param(max_depth, "max_depth", 1, 3)
        if not valid_depth:
            await ctx.error(f"Parameter validation failed: {depth_result}")
            return f"❌ **Error:** {depth_result}"
        """
        Multi-engine search across Yahoo and DuckDuckGo with comprehensive content extraction.

        This tool searches across multiple engines simultaneously:
        - Yahoo Search: Traditional web search engine
        - DuckDuckGo Search: Privacy-focused search engine

        Features:
        - Parallel searching across engines
        - Intelligent fallback if one engine fails
        - Content extraction and link following
        - Clean markdown-formatted results
        """
        return await multi_search(
            query=query,
            ctx=ctx,
            num_results=num_results,
            extract_content=extract_content,
            follow_links=follow_links,
            max_depth=max_depth,
            use_fallback=use_fallback,
        )
