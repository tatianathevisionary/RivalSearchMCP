"""
Dev.to search implementation using public API.
No authentication required for reading public articles.
"""

import httpx
from typing import List, Dict, Any

from src.logging.logger import logger


class DevToSearch:
    """Search Dev.to articles using public API (no auth needed)."""
    
    def __init__(self):
        self.api_url = "https://dev.to/api"
        self.base_url = "https://dev.to"
    
    async def search(
        self,
        query: str,
        tag: str = None,
        per_page: int = 10,
        sort: str = "relevant"
    ) -> List[Dict[str, Any]]:
        """
        Search Dev.to articles.
        
        Args:
            query: Search query
            tag: Filter by tag (optional)
            per_page: Results per page
            sort: Sort by (relevant, latest, top)
            
        Returns:
            List of Dev.to article dictionaries
        """
        try:
            # Dev.to doesn't have direct search API, so we'll get articles by tag
            # or latest articles, then filter client-side
            if tag:
                url = f"{self.api_url}/articles?tag={tag}&per_page={per_page}"
            else:
                url = f"{self.api_url}/articles?per_page=30"  # Get more to filter
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                data = response.json()
                articles = []
                
                # Filter by query if provided
                for article in data:
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    tags = ' '.join(article.get('tag_list', [])).lower()
                    
                    # Simple keyword matching
                    if not query or query.lower() in title or query.lower() in description or query.lower() in tags:
                        articles.append({
                            'title': article.get('title', ''),
                            'description': article.get('description', ''),
                            'url': article.get('url', ''),
                            'published_at': article.get('published_at', ''),
                            'tag_list': article.get('tag_list', []),
                            'reading_time_minutes': article.get('reading_time_minutes', 0),
                            'public_reactions_count': article.get('public_reactions_count', 0),
                            'comments_count': article.get('comments_count', 0),
                            'user': article.get('user', {}).get('name', ''),
                            'source': 'devto'
                        })
                        
                        if len(articles) >= per_page:
                            break
                
                logger.info(f"Found {len(articles)} Dev.to articles for: {query}")
                return articles
                
        except Exception as e:
            logger.error(f"Dev.to search failed: {e}")
            return []
