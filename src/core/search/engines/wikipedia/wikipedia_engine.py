"""
Wikipedia search engine implementation using public API.
No authentication required.
"""

from datetime import datetime
from typing import List

import httpx

from src.logging.logger import logger

from ...core.multi_engines import BaseSearchEngine, MultiSearchResult


class WikipediaSearchEngine(BaseSearchEngine):
    """Wikipedia search using public MediaWiki API."""

    def __init__(self):
        super().__init__("Wikipedia", "https://en.wikipedia.org")
        # Override with dedicated session for Wikipedia
        self.session = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; RivalSearchMCP/1.0; +https://github.com/research)",
                "Accept": "application/json",
            },
        )
        self.api_url = "https://en.wikipedia.org/w/api.php"

    async def search(
        self,
        query: str,
        num_results: int = 10,
        extract_content: bool = True,
        follow_links: bool = True,
        max_depth: int = 2,
    ) -> List[MultiSearchResult]:
        """Search Wikipedia articles."""
        try:
            logger.info(f"Starting Wikipedia search for: {query}")

            # Use MediaWiki Search API
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srlimit": num_results,
                "format": "json",
                "utf8": 1,
            }

            response = await self.session.get(self.api_url, params=params)
            response.raise_for_status()

            data = response.json()
            results = []

            for i, item in enumerate(data.get("query", {}).get("search", [])[:num_results]):
                title = item.get("title", "")
                page_id = item.get("pageid", "")
                snippet = (
                    item.get("snippet", "")
                    .replace('<span class="searchmatch">', "")
                    .replace("</span>", "")
                )

                # Build article URL
                url = f"{self.base_url}/wiki/{title.replace(' ', '_')}"

                # Optionally get article extract
                description = snippet
                if extract_content and page_id:
                    extract = await self._get_article_extract(page_id)
                    if extract:
                        description = extract

                results.append(
                    MultiSearchResult(
                        title=title,
                        url=url,
                        description=description,
                        engine=self.name,
                        position=i + 1,
                        timestamp=datetime.now().isoformat(),
                    )
                )

            logger.info(f"Wikipedia search completed: {len(results)} articles")
            return results

        except Exception as e:
            logger.error(f"Wikipedia search failed: {e}")
            return []

    async def _get_article_extract(self, page_id: str) -> str:
        """Get article extract (summary) from Wikipedia."""
        try:
            params = {
                "action": "query",
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
                "pageids": page_id,
                "format": "json",
            }

            response = await self.session.get(self.api_url, params=params)
            response.raise_for_status()

            data = response.json()
            pages = data.get("query", {}).get("pages", {})

            if pages:
                page_data = list(pages.values())[0]
                extract = page_data.get("extract", "")
                # Return first 500 chars
                return extract[:500] + ("..." if len(extract) > 500 else "")

            return ""

        except Exception as e:
            logger.debug(f"Failed to get Wikipedia extract: {e}")
            return ""

    async def close(self):
        """Close the session."""
        await self.session.aclose()
