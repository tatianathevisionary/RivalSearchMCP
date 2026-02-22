"""
News aggregation from multiple free sources.
No authentication required - uses Google News RSS and Bing News.
"""

from typing import Any, Dict, List
from urllib.parse import quote_plus

import feedparser
import httpx

from src.logging.logger import logger


class NewsAggregator:
    """Aggregate news from multiple free sources without authentication."""

    def __init__(self):
        self.sources = {
            "google_news": "https://news.google.com/rss/search",
            "duckduckgo_news": "https://html.duckduckgo.com/html/",
        }

    async def search_news(
        self, query: str, max_results: int = 10, language: str = "en", country: str = "US"
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

        # Search news sources (Yahoo News removed - returns 500)
        import asyncio

        results = await asyncio.gather(
            self._search_google_news(query, max_results, language, country),
            self._search_duckduckgo_news(query, max_results),
            return_exceptions=True,
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
            url = article["url"]
            title_lower = article["title"].lower()[:50]  # First 50 chars for fuzzy match

            if url not in seen_urls and title_lower not in seen_titles:
                seen_urls.add(url)
                seen_titles.add(title_lower)
                unique_articles.append(article)

        logger.info(
            f"Aggregated {len(unique_articles)} unique articles from {len(results)} sources"
        )
        return unique_articles[:max_results]

    async def _search_google_news(
        self, query: str, max_results: int, language: str, country: str
    ) -> List[Dict[str, Any]]:
        """Search Google News RSS feed."""
        try:
            url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl={language}&gl={country}&ceid={country}:{language}"

            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()

                # Parse RSS feed
                feed = feedparser.parse(response.text)
                articles = []

                for entry in feed.entries[:max_results]:
                    articles.append(
                        {
                            "title": entry.get("title", ""),
                            "url": entry.get("link", ""),
                            "description": entry.get("summary", ""),
                            "published": entry.get("published", ""),
                            "source": entry.get("source", {}).get("title", "Google News"),
                            "platform": "google_news",
                        }
                    )

                logger.info(f"Found {len(articles)} Google News articles for: {query}")
                return articles

        except Exception as e:
            logger.error(f"Google News search failed: {e}")
            return []

    async def _search_duckduckgo_news(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search DuckDuckGo News via html endpoint."""
        try:
            from bs4 import BeautifulSoup

            from src.utils.agents import get_random_user_agent

            url = "https://html.duckduckgo.com/html/"
            params = {"q": f"{query} news"}
            headers = {"User-Agent": get_random_user_agent(), "Referer": "https://duckduckgo.com/"}

            async with httpx.AsyncClient(
                headers=headers, timeout=30.0, follow_redirects=True
            ) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                articles = []
                result_divs = soup.find_all("div", class_="result")
                if not result_divs:
                    result_links = soup.find_all("a", class_="result-link")
                else:
                    result_links = []
                    for div in result_divs[:max_results]:
                        link = div.find("a", class_="result__a") or div.find("a", href=True)
                        if link:
                            result_links.append(link)

                for link in result_links[:max_results]:
                    if not hasattr(link, "get_text"):
                        continue
                    title = link.get_text(strip=True)
                    url = link.get("href", "")

                    if title and url:
                        articles.append(
                            {
                                "title": title,
                                "url": url,
                                "description": "",
                                "published": "",
                                "source": "DuckDuckGo News",
                                "platform": "duckduckgo_news",
                            }
                        )

                logger.info(f"Found {len(articles)} DuckDuckGo News articles for: {query}")
                return articles

        except Exception as e:
            logger.error(f"DuckDuckGo News search failed: {e}")
            return []
