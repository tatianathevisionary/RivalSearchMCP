"""
Hacker News search implementation using Algolia HN Search API.
No authentication required.
"""

import httpx
from typing import List, Dict, Any
from datetime import datetime

from src.logging.logger import logger


class HackerNewsSearch:
    """Search Hacker News using Algolia API (no auth needed)."""
    
    def __init__(self):
        self.api_url = "https://hn.algolia.com/api/v1"
        self.base_url = "https://news.ycombinator.com"
    
    async def search(
        self,
        query: str,
        tags: str = "story",
        sort_by: str = "relevance",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search Hacker News stories.
        
        Args:
            query: Search query
            tags: Filter by type (story, comment, poll, etc.)
            sort_by: Sort by relevance or date
            limit: Maximum results
            
        Returns:
            List of HN story dictionaries
        """
        try:
            endpoint = f"{self.api_url}/search"
            params = {
                'query': query,
                'tags': tags,
                'hitsPerPage': limit
            }
            
            if sort_by == "date":
                endpoint = f"{self.api_url}/search_by_date"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(endpoint, params=params)
                response.raise_for_status()
                
                data = response.json()
                stories = []
                
                for hit in data.get('hits', []):
                    stories.append({
                        'title': hit.get('title', ''),
                        'author': hit.get('author', ''),
                        'points': hit.get('points', 0),
                        'url': hit.get('url', ''),
                        'hn_url': f"{self.base_url}/item?id={hit.get('objectID', '')}",
                        'num_comments': hit.get('num_comments', 0),
                        'created_at': hit.get('created_at', ''),
                        'story_text': hit.get('story_text', '')[:500],
                        'source': 'hackernews'
                    })
                
                logger.info(f"Found {len(stories)} Hacker News stories for: {query}")
                return stories
                
        except Exception as e:
            logger.error(f"Hacker News search failed: {e}")
            return []
