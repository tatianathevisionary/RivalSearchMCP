"""
Social search tools for FastMCP server.
Searches Reddit, Hacker News, Dev.to, Product Hunt, and Medium without authentication.
"""

from typing import List, Literal
from fastmcp import FastMCP

from src.core.social import RedditSearch, HackerNewsSearch, DevToSearch, ProductHuntSearch, MediumSearch
from src.logging.logger import logger
from src.utils.markdown_formatter import format_social_media_markdown


def register_social_media_tools(mcp: FastMCP):
    """Register social search tools."""
    
    reddit_search = RedditSearch()
    hn_search = HackerNewsSearch()
    devto_search = DevToSearch()
    producthunt_search = ProductHuntSearch()
    medium_search = MediumSearch()
    
    @mcp.tool
    async def social_search(
        query: str,
        platforms: List[Literal["reddit", "hackernews", "devto", "producthunt", "medium"]] = ["reddit", "hackernews", "devto"],
        max_results_per_platform: int = 10,
        reddit_subreddit: str = "all",
        time_filter: str = "all"
    ) -> str:
        """
        Search across social platforms and communities for discussions and content.
        
        Searches Reddit, Hacker News, Dev.to, Product Hunt, and Medium without authentication.
        
        Args:
            query: Search query
            platforms: List of platforms (reddit, hackernews, devto, producthunt, medium)
            max_results_per_platform: Maximum results per platform (default: 10)
            reddit_subreddit: Reddit subreddit to search (default: "all" for site-wide)
            time_filter: Time filter for Reddit (all, day, week, month, year)
        """
        try:
            logger.info(f"Social search for: {query} on {platforms}")
            
            results = {}
            
            if "reddit" in platforms:
                reddit_results = await reddit_search.search(
                    query=query,
                    subreddit=reddit_subreddit,
                    limit=max_results_per_platform,
                    time_filter=time_filter
                )
                results['reddit'] = {
                    'status': 'success' if reddit_results else 'no_results',
                    'count': len(reddit_results),
                    'results': reddit_results
                }
            
            if "hackernews" in platforms:
                hn_results = await hn_search.search(
                    query=query,
                    limit=max_results_per_platform
                )
                results['hackernews'] = {
                    'status': 'success' if hn_results else 'no_results',
                    'count': len(hn_results),
                    'results': hn_results
                }
            
            if "devto" in platforms:
                devto_results = await devto_search.search(
                    query=query,
                    per_page=max_results_per_platform
                )
                results['devto'] = {
                    'status': 'success' if devto_results else 'no_results',
                    'count': len(devto_results),
                    'results': devto_results
                }
            
            if "producthunt" in platforms:
                ph_results = await producthunt_search.search(
                    query=query,
                    limit=max_results_per_platform
                )
                results['producthunt'] = {
                    'status': 'success' if ph_results else 'no_results',
                    'count': len(ph_results),
                    'results': ph_results
                }
            
            if "medium" in platforms:
                medium_results = await medium_search.search(
                    query=query,
                    limit=max_results_per_platform
                )
                results['medium'] = {
                    'status': 'success' if medium_results else 'no_results',
                    'count': len(medium_results),
                    'results': medium_results
                }
            
            return format_social_media_markdown(query, results)
            
        except Exception as e:
            logger.error(f"Social search failed: {e}")
            return f"# 💬 Social Search Results\n\n❌ **Error:** {str(e)}"
