"""
Medium article search implementation using RSS feeds and public API.
No authentication required for reading public articles.
"""

from typing import Any, Dict, List
from urllib.parse import quote_plus

import feedparser
import httpx

from src.logging.logger import logger


class MediumSearch:
    """Search Medium articles using RSS feeds and public endpoints."""

    def __init__(self):
        self.base_url = "https://medium.com"
        self.feed_url = "https://medium.com/feed"

    async def search(self, query: str, tag: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Medium articles.

        Args:
            query: Search query
            tag: Optional tag to filter by
            limit: Maximum results

        Returns:
            List of Medium article dictionaries
        """
        try:
            articles = []

            # Strategy 1: Use tag-based RSS feeds
            if tag:
                feed_url = f"{self.base_url}/feed/tag/{tag}"
            else:
                feed_url = f"{self.base_url}/feed/tag/{query.lower().replace(' ', '-')}"

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }

            async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
                # Try RSS feed first
                try:
                    response = await client.get(feed_url)

                    if response.status_code == 200:
                        feed = feedparser.parse(response.text)

                        for entry in feed.entries[:limit]:
                            articles.append(
                                {
                                    "title": entry.get("title", ""),
                                    "url": entry.get("link", ""),
                                    "author": entry.get("author", ""),
                                    "published": entry.get("published", ""),
                                    "summary": entry.get("summary", "")[:300],
                                    "source": "medium",
                                }
                            )
                except Exception as rss_error:
                    logger.debug(f"RSS feed failed, trying HTML: {rss_error}")

                # Fallback: Parse search results HTML
                if not articles:
                    search_url = f"{self.base_url}/search?q={quote_plus(query)}"
                    response = await client.get(search_url)

                    from bs4 import BeautifulSoup

                    soup = BeautifulSoup(response.text, "html.parser")

                    # Extract article links and titles
                    article_links = soup.find_all(
                        "a", href=lambda h: h and ("/p/" in h or "/@" in h)
                    )

                    for link in article_links[:limit]:
                        title = link.get_text(strip=True)
                        href = link.get("href", "")

                        if title and href and len(title) > 10:
                            articles.append(
                                {
                                    "title": title,
                                    "url": (
                                        href
                                        if href.startswith("http")
                                        else f"{self.base_url}{href}"
                                    ),
                                    "author": "",
                                    "published": "",
                                    "summary": "",
                                    "source": "medium",
                                }
                            )

                logger.info(f"Found {len(articles)} Medium articles for: {query}")
                return articles[:limit]

        except Exception as e:
            logger.error(f"Medium search failed: {e}")
            return []
