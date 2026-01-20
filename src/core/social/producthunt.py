"""
Product Hunt search implementation using public GraphQL API.
No authentication required for reading public posts.
"""

import httpx
from typing import List, Dict, Any

from src.logging.logger import logger


class ProductHuntSearch:
    """Search Product Hunt without authentication."""
    
    def __init__(self):
        self.api_url = "https://www.producthunt.com/frontend/graphql"
        self.base_url = "https://www.producthunt.com"
    
    async def search(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search Product Hunt posts.
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of Product Hunt post dictionaries
        """
        try:
            # Use Product Hunt's search endpoint (simplified approach)
            # Since GraphQL requires more setup, we'll use RSS feed
            url = f"https://www.producthunt.com/search/posts?q={query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse HTML for product information
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                products = []
                # Product Hunt uses complex structure, extract what we can
                product_elements = soup.find_all('div', attrs={'data-test': 'post-item'})
                
                if not product_elements:
                    # Fallback: look for links to posts
                    links = soup.find_all('a', href=lambda h: h and '/posts/' in h)
                    for link in links[:limit]:
                        title = link.get_text(strip=True)
                        href = link.get('href', '')
                        if title and href:
                            products.append({
                                'title': title,
                                'url': f"{self.base_url}{href}" if not href.startswith('http') else href,
                                'tagline': '',
                                'votes': 0,
                                'source': 'producthunt'
                            })
                
                logger.info(f"Found {len(products)} Product Hunt posts for: {query}")
                return products[:limit]
                
        except Exception as e:
            logger.error(f"Product Hunt search failed: {e}")
            return []
