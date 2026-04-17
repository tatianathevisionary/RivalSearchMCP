"""
Mojeek web search engine via www.mojeek.com/search.

Mojeek operates its own independent index (not a Google/Bing wrapper)
and exposes real full-text search through a plain HTML SERP. Accepts
standard requests fine, but we still route through Scrapling for
consistency with the other engines and because its header defaults
match what Mojeek expects.

Result cards are `ul.results-standard > li`; title link is `h2 a`
(direct link, no redirector unlike Bing); snippet is `p.s`.
"""

from datetime import datetime
from typing import List

from scrapling.fetchers import AsyncFetcher

from src.logging.logger import logger

from ...core.multi_engines import BaseSearchEngine, MultiSearchResult


class MojeekSearchEngine(BaseSearchEngine):
    """Mojeek independent web search (Scrapling-powered)."""

    def __init__(self):
        super().__init__("Mojeek", "https://www.mojeek.com")
        self.search_url = f"{self.base_url}/search"

    async def search(
        self,
        query: str,
        num_results: int = 10,
        extract_content: bool = True,
        follow_links: bool = True,
        max_depth: int = 2,
    ) -> List[MultiSearchResult]:
        logger.info("Starting Mojeek search for: %s", query)

        results = await self._search_html(query, num_results)
        logger.info("Mojeek returned %d results", len(results))

        if extract_content and results:
            for result in results:
                result.real_url = self._extract_real_url(result.url)
                target_url = result.real_url if result.real_url != result.url else result.url
                if not target_url:
                    continue

                content = await self._fetch_page_content(target_url)
                if not content:
                    continue

                result.full_content = self._extract_main_content(content)
                result.internal_links = self._extract_internal_links(content, target_url)
                result.html_structure = self._extract_html_structure(content)

                if follow_links and result.internal_links and max_depth > 1:
                    result.second_level_content = await self._extract_second_level_content(
                        target_url, result.internal_links
                    )

        return results

    async def _search_html(self, query: str, num_results: int) -> List[MultiSearchResult]:
        try:
            page = await AsyncFetcher.get(
                self.search_url,
                params={"q": query, "fmt": "html"},
                stealthy_headers=True,
                timeout=30,
            )
        except Exception as e:
            logger.error("Mojeek fetch failed: %s", e)
            return []

        if page.status != 200:
            logger.warning(
                "Mojeek returned %s for %r (body snippet: %s)",
                page.status,
                query,
                (page.body or b"")[:200],
            )
            return []

        results: List[MultiSearchResult] = []
        cards = page.css("ul.results-standard > li")
        for i, card in enumerate(cards[:num_results]):
            title_links = card.css("h2 a")
            if not title_links:
                continue
            title = self._clean_text(title_links[0].get_all_text() or "")
            url = title_links[0].attrib.get("href", "")
            if not title or not url:
                continue

            snippet_nodes = card.css("p.s")
            description = (
                self._clean_text(snippet_nodes[0].get_all_text() or "") if snippet_nodes else ""
            )

            results.append(
                MultiSearchResult(
                    title=title,
                    url=url,
                    description=description,
                    engine=self.name,
                    position=i + 1,
                    timestamp=datetime.now().isoformat(),
                    html_structure={},
                    raw_html="",
                )
            )
        return results
