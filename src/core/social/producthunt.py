"""
Product Hunt search implementation using public GraphQL API.
No authentication required for reading public posts.
"""

from typing import Any, Dict, List

import httpx

from src.logging.logger import logger


class ProductHuntSearch:
    """Search Product Hunt without authentication."""

    def __init__(self):
        self.api_url = "https://www.producthunt.com/frontend/graphql"
        self.base_url = "https://www.producthunt.com"

    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search Product Hunt posts.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of Product Hunt post dictionaries
        """
        from urllib.parse import quote_plus

        url = f"https://www.producthunt.com/search/posts?q={quote_plus(query)}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
        }

        try:
            async with httpx.AsyncClient(
                headers=headers, timeout=30.0, follow_redirects=True
            ) as client:
                response = await client.get(url)
                if response.status_code != 200:
                    logger.warning(
                        "Product Hunt returned %s for %r (body snippet: %s)",
                        response.status_code,
                        query,
                        response.text[:200],
                    )
                    return []

                from bs4 import BeautifulSoup

                soup = BeautifulSoup(response.text, "html.parser")
                products = []

                # Try the structured selector first, then fall back to any
                # /posts/ link. Product Hunt renders via React so selectors
                # shift — this is best-effort scraping.
                product_elements = soup.find_all("div", attrs={"data-test": "post-item"})
                if not product_elements:
                    links = soup.find_all("a", href=lambda h: h and "/posts/" in h)
                    seen = set()
                    for link in links:
                        if len(products) >= limit:
                            break
                        title = link.get_text(strip=True)
                        href = link.get("href", "")
                        if not title or not href or href in seen:
                            continue
                        seen.add(href)
                        products.append(
                            {
                                "title": title,
                                "url": (
                                    href if href.startswith("http") else f"{self.base_url}{href}"
                                ),
                                "tagline": "",
                                "votes": 0,
                                "source": "producthunt",
                            }
                        )

                if not products:
                    logger.warning(
                        "Product Hunt page parsed but no products extracted "
                        "for %r (selectors may be stale)",
                        query,
                    )
                else:
                    logger.info("Found %d Product Hunt posts for %r", len(products), query)
                return products[:limit]

        except httpx.HTTPError as e:
            logger.warning("Product Hunt search failed (network): %s", e)
            return []
        except Exception:
            logger.exception("Product Hunt search failed (unexpected)")
            return []
