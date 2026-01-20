"""
GitHub repository search tools for FastMCP server.
Searches public GitHub repositories without authentication.
"""

from typing import Optional
from fastmcp import FastMCP

from src.core.github_api import GitHubSearch
from src.logging.logger import logger
from src.utils.markdown_formatter import format_github_markdown


def register_github_tools(mcp: FastMCP):
    """Register GitHub repository search tools."""
    
    github_api = GitHubSearch()
    
    @mcp.tool
    async def github_search(
        query: str,
        language: Optional[str] = None,
        sort: str = "stars",
        max_results: int = 10,
        include_readme: bool = False
    ) -> str:
        """
        Search GitHub repositories without authentication.
        
        Searches public GitHub repositories using the public API.
        No authentication token required.
        
        Args:
            query: Search query (e.g., "web framework", "machine learning")
            language: Filter by programming language (e.g., "Python", "TypeScript")
            sort: Sort by (stars, forks, updated)
            max_results: Maximum results to return (default: 10)
            include_readme: Whether to fetch README content (slower)
        """
        try:
            logger.info(f"GitHub search for: {query}")
            
            repositories = await github_api.search_repositories(
                query=query,
                language=language,
                sort=sort,
                per_page=max_results
            )
            
            # Optionally fetch README for top result
            if include_readme and repositories:
                top_repo = repositories[0]
                owner, repo_name = top_repo['name'].split('/')
                readme = await github_api.get_readme(owner, repo_name)
                if readme:
                    top_repo['readme'] = readme[:1000]  # First 1000 chars
            
            return format_github_markdown(query, repositories)
            
        except Exception as e:
            logger.error(f"GitHub search failed: {e}")
            return f"# 🐙 GitHub Repository Search\n\n❌ **Error:** {str(e)}"
