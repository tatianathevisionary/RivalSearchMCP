"""
News aggregation from multiple free sources.
No authentication required - uses Google News RSS and Bing News.
"""

import httpx
import feedparser
from typing import List, Dict, Any
from datetime import datetime
from urllib.parse import quote_plus

from src.logging.logger import logger


class NewsAggregator:
    """Aggregate news from multiple free sources without authentication."""
    
    def __init__(self):
        self.sources = {
            'google_news': 'https://news.google.com/rss/search',
            'duckduckgo_news': 'https://duckduckgo.com/',
            'yahoo_news': 'https://news.search.yahoo.com/search'
        }
    
    async def search_news(
        self,
        query: str,
        max_results: int = 10,
        language: str = "en",
        country: str = "US"
    ) -> List[Dict[str, Any]]:
        """
        Search news from multiple sources.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            language: Language code (default: en)
            country: Country code (default: US)
            
        Returns:
            List of news article dictionaries
        """
        all_articles = []
        
        # Search all news sources concurrently
        import asyncio
        results = await asyncio.gather(
            self._search_google_news(query, max_results, language, country),
            self._search_duckduckgo_news(query, max_results),
            self._search_yahoo_news(query, max_results),
            return_exceptions=True
        )
        
        # Collect results
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
        
        # Deduplicate by URL and title similarity
        seen_urls = set()
        seen_titles = set()
        unique_articles = []
        
        for article in all_articles:
            url = article['url']
            title_lower = article['title'].lower()[:50]  # First 50 chars for fuzzy match
            
            if url not in seen_urls and title_lower not in seen_titles:
                seen_urls.add(url)
                seen_titles.add(title_lower)
                unique_articles.append(article)
        
        logger.info(f"Aggregated {len(unique_articles)} unique articles from {len(results)} sources")
        return unique_articles[:max_results]
    
    async def _search_google_news(
        self,
        query: str,
        max_results: int,
        language: str,
        country: str
    ) -> List[Dict[str, Any]]:
        """Search Google News RSS feed."""
        try:
            url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl={language}&gl={country}&ceid={country}:{language}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse RSS feed
                feed = feedparser.parse(response.text)
                articles = []
                
                for entry in feed.entries[:max_results]:
                    articles.append({
                        'title': entry.get('title', ''),
                        'url': entry.get('link', ''),
                        'description': entry.get('summary', ''),
                        'published': entry.get('published', ''),
                        'source': entry.get('source', {}).get('title', 'Google News'),
                        'platform': 'google_news'
                    })
                
                logger.info(f"Found {len(articles)} Google News articles for: {query}")
                return articles
                
        except Exception as e:
            logger.error(f"Google News search failed: {e}")
            return []
    
    async def _search_duckduckgo_news(
        self,
        query: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Search DuckDuckGo News."""
        try:
            from bs4 import BeautifulSoup
            
            url = "https://lite.duckduckgo.com/lite/"
            params = {
                'q': query,
                'kn': '1'  # News filter
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = []
                
                # Find news result links
                result_links = soup.find_all('a', class_='result-link')
                
                for link in result_links[:max_results]:
                    title = link.get_text(strip=True)
                    url = link.get('href', '')
                    
                    if title and url:
                        articles.append({
                            'title': title,
                            'url': url,
                            'description': '',
                            'published': '',
                            'source': 'DuckDuckGo News',
                            'platform': 'duckduckgo_news'
                        })
                
                logger.info(f"Found {len(articles)} DuckDuckGo News articles for: {query}")
                return articles
                
        except Exception as e:
            logger.error(f"DuckDuckGo News search failed: {e}")
            return []
    
    async def _search_yahoo_news(
        self,
        query: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Search Yahoo News."""
        try:
            from bs4 import BeautifulSoup, Tag
            
            url = "https://news.search.yahoo.com/search"
            params = {
                'p': query,
                'n': max_results
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = []
                
                # Find news result containers
                result_containers = soup.find_all('div', class_='dd')
                if not result_containers:
                    result_containers = soup.find_all('div', class_='NewsArticle')
                
                for container in result_containers[:max_results]:
                    if isinstance(container, Tag):
                        title_elem = container.find('a')
                        
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            url = title_elem.get('href', '')
                            
                            # Try to find description
                            desc_elem = container.find('p')
                            description = desc_elem.get_text(strip=True) if desc_elem else ''
                            
                            if title and url:
                                articles.append({
                                    'title': title,
                                    'url': url,
                                    'description': description,
                                    'published': '',
                                    'source': 'Yahoo News',
                                    'platform': 'yahoo_news'
                                })
                
                logger.info(f"Found {len(articles)} Yahoo News articles for: {query}")
                return articles
                
        except Exception as e:
            logger.error(f"Yahoo News search failed: {e}")
            return []