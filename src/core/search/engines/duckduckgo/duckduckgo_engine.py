"""
DuckDuckGo search engine implementation for RivalSearchMCP.
Uses HTML format for most reliable results.
"""

from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, Tag

from src.logging.logger import logger

from ...core.multi_engines import BaseSearchEngine, MultiSearchResult


class DuckDuckGoSearchEngine(BaseSearchEngine):
    """DuckDuckGo search engine implementation - uses lite endpoint."""

    def __init__(self):
        super().__init__("DuckDuckGo", "https://duckduckgo.com")
        # Override session with proper configuration for DuckDuckGo
        import httpx

        self.session = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://duckduckgo.com/",
            },
        )

    async def search(
        self,
        query: str,
        num_results: int = 10,
        extract_content: bool = True,
        follow_links: bool = True,
        max_depth: int = 2,
    ) -> List[MultiSearchResult]:
        """Search DuckDuckGo using HTML format (most reliable)."""
        try:
            logger.info(f"Starting DuckDuckGo search for: {query}")

            # Use only HTML format (most reliable)
            results = await self._search_html(query, num_results)
            logger.info(f"_search_html returned {len(results)} results")

            if extract_content and results:
                # Extract real URLs and fetch content
                for result in results:
                    result.real_url = self._extract_real_url(result.url)

                    # Always fetch content when content extraction is enabled
                    target_url = result.real_url if result.real_url != result.url else result.url
                    if target_url:
                        logger.info(f"Following link to: {target_url}")
                        content = await self._fetch_page_content(target_url)

                        if content:
                            # Extract main content using the enhanced multi-method approach
                            result.full_content = self._extract_main_content(content)
                            result.internal_links = self._extract_internal_links(
                                content, target_url
                            )
                            result.html_structure = self._extract_html_structure(content)

                            if follow_links and result.internal_links and max_depth > 1:
                                result.second_level_content = (
                                    await self._extract_second_level_content(
                                        target_url, result.internal_links
                                    )
                                )

            logger.info(
                f"DuckDuckGo search completed: {len(results)} results with content extraction"
            )
            return results

        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []

    async def _search_html(self, query: str, num_results: int) -> List[MultiSearchResult]:
        """Search using html.duckduckgo.com (lite blocks automated requests)."""
        from src.utils.agents import get_random_user_agent

        search_url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://duckduckgo.com/",
        }
        params = {"q": query}

        try:
            response = await self.session.get(search_url, params=params, headers=headers)
            response.raise_for_status()
            return self._parse_html_results(response.text, num_results)
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []

    def _parse_html_results(self, html: str, num_results: int) -> List[MultiSearchResult]:
        """Parse html.duckduckgo.com HTML results."""
        soup = BeautifulSoup(html, "html.parser")
        results = []
        result_divs = soup.find_all("div", class_="result")

        for i, div in enumerate(result_divs[:num_results]):
            try:
                if isinstance(div, Tag):
                    link = div.find("a", class_="result__a") or div.find("a", href=True)
                    if link and isinstance(link, Tag):
                        title = self._clean_text(link.get_text())
                        url = link.get("href", "")
                        snippet = div.find("a", class_="result__snippet") or div.find(
                            "div", class_="result__snippet"
                        )
                        description = self._clean_text(snippet.get_text()) if snippet else ""
                        if title and url:
                            results.append(
                                MultiSearchResult(
                                    title=title,
                                    url=str(url),
                                    description=description,
                                    engine=self.name,
                                    position=i + 1,
                                    timestamp=datetime.now().isoformat(),
                                    html_structure={},
                                    raw_html="",
                                )
                            )
            except Exception:
                continue
        return results
