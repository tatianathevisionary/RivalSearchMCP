"""
News aggregation tools for FastMCP server.
Aggregates news from free sources without authentication.
"""

from typing import Literal
from fastmcp import FastMCP

from src.core.news import NewsAggregator
from src.logging.logger import logger
from src.utils.markdown_formatter import format_news_markdown


def register_news_tools(mcp: FastMCP):
    """Register news aggregation tools."""
    
    aggregator = NewsAggregator()
    
    @mcp.tool
    async def news_aggregation(
        query: str,
        max_results: int = 10,
        language: str = "en",
        country: str = "US",
        time_range: Literal["anytime", "day", "week", "month"] = "anytime"
    ) -> str:
        """
        Aggregate news from multiple free sources.
        
        Searches Google News RSS feed without requiring authentication.
        
        Args:
            query: News search query
            max_results: Maximum results to return (default: 10)
            language: Language code (default: "en")
            country: Country code (default: "US")
            time_range: Time range filter (anytime, day, week, month)
        """
        try:
            logger.info(f"News aggregation for: {query}")
            
            articles = await aggregator.search_news(
                query=query,
                max_results=max_results,
                language=language,
                country=country
            )
            
            return format_news_markdown(query, articles, time_range)
            
        except Exception as e:
            logger.error(f"News aggregation failed: {e}")
            return f"# 📰 News Search Results\n\n❌ **Error:** {str(e)}"
