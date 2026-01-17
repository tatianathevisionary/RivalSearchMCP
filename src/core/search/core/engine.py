#!/usr/bin/env python3
"""
Multi-engine search core functionality for RivalSearchMCP.
Supports multiple search engines with DuckDuckGo and Yahoo.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, cast
from urllib.parse import quote_plus

from bs4 import BeautifulSoup, Tag

from src.logging.logger import logger
from src.utils import get_enhanced_ua_list, get_http_client


# Additional search engine configurations
ADDITIONAL_ENGINES = {
    "duckduckgo": {
        "url": "https://html.duckduckgo.com/html/",
        "params": {"q": "{query}"},
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    },
    "yahoo": {
        "url": "https://search.yahoo.com/search",
        "params": {"p": "{query}", "n": "{num}"},
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    },
}


class MultiEngineSearch:
    """Multi-engine search with DuckDuckGo and Yahoo as primary engines."""

    def __init__(self):
        """Initialize the multi-engine search."""
        self.results = {}
        self.failed_engines = []
        self.user_agents = get_enhanced_ua_list()

    async def search_all_engines(
        self,
        query: str,
        num_results: int = 10,
        engines: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        self.query = query  # Store query for results
        """
        Search across DuckDuckGo and Yahoo simultaneously with deduplication.

        Args:
            query: Search query
            num_results: Number of results per engine
            engines: List of engines to use (default: duckduckgo, yahoo)

        Returns:
            Dictionary with deduplicated results from both engines
        """
        if engines is None:
            engines = ["duckduckgo", "yahoo"]  # Only DuckDuckGo and Yahoo

        logger.info(f"🔍 Multi-engine search for: {query}")
        logger.info(f"🚀 Using engines: {', '.join(engines)}")

        # Filter to only available engines
        available_engines = [e for e in engines if e in ADDITIONAL_ENGINES]

        if available_engines:
            logger.info(f"🔄 Searching {len(available_engines)} engines...")

            # Search all engines concurrently
            tasks = []
            for engine in available_engines:
                task = asyncio.create_task(
                    self.search_single_engine(engine, query, num_results)
                )
                tasks.append(task)

            # Wait for all searches to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results and handle exceptions
            for engine, result in zip(available_engines, results):
                if isinstance(result, Exception):
                    logger.error(f"❌ {engine} search failed: {result}")
                    self.failed_engines.append(engine)
                elif isinstance(result, list) and result:
                    self.results[engine] = result
                    logger.info(f"✅ {engine}: {len(result)} results")
                else:
                    logger.warning(f"⚠️ {engine}: No results")
                    self.failed_engines.append(engine)

        return self._aggregate_results(num_results)

    async def search_single_engine(
        self, engine: str, query: str, num_results: int
    ) -> List[Dict[str, Any]]:
        """Search a single engine (excluding Google)."""
        config = ADDITIONAL_ENGINES[engine]

        # Prepare request
        params = config["params"].copy()
        params = {
            k: v.format(query=quote_plus(query), num=num_results)
            for k, v in params.items()
        }

        headers = config["headers"].copy()
        headers["User-Agent"] = self._get_random_ua()

        try:
            client = await get_http_client()
            response = await client.get(
                config["url"], params=params, headers=headers, timeout=30.0
            )
            response.raise_for_status()

            # Parse results based on engine
            if engine == "duckduckgo":
                return self._parse_duckduckgo_results(response.text, num_results)
            elif engine == "yahoo":
                return self._parse_yahoo_results(response.text, num_results)
            else:
                return self._parse_generic_results(response.text, num_results)

        except Exception as e:
            logger.error(f"Error searching {engine}: {e}")
            raise

    def _get_random_ua(self) -> str:
        """Get a random user agent."""
        import random

        return random.choice(self.user_agents)

    def _parse_duckduckgo_results(
        self, html: str, num_results: int
    ) -> List[Dict[str, Any]]:
        """Parse DuckDuckGo search results."""
        results = []
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Find search result containers
            result_containers = soup.find_all("div", class_="result")

            for i, container in enumerate(result_containers[:num_results]):
                try:
                    # Cast to Tag for proper type checking
                    container_tag = cast(Tag, container)

                    # Extract title and link
                    title_elem = container_tag.find("a", class_="result__a")
                    snippet_elem = container_tag.find("a", class_="result__snippet")

                    if title_elem:
                        # Cast title_elem to Tag for get operation
                        title_tag = cast(Tag, title_elem)
                        result = {
                            "title": title_tag.get_text(strip=True),
                            "url": title_tag.get("href", ""),
                            "snippet": (
                                snippet_elem.get_text(strip=True)
                                if snippet_elem
                                else ""
                            ),
                            "position": i + 1,
                            "engine": "duckduckgo",
                        }
                        results.append(result)
                except Exception as e:
                    logger.debug(f"Error parsing DuckDuckGo result: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing DuckDuckGo results: {e}")

        return results

    def _parse_yahoo_results(self, html: str, num_results: int) -> List[Dict[str, Any]]:
        """Parse Yahoo search results."""
        results = []
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Find search result containers
            result_containers = soup.find_all("div", class_="dd")

            for i, container in enumerate(result_containers[:num_results]):
                try:
                    # Cast to Tag for proper type checking
                    container_tag = cast(Tag, container)

                    # Extract title and link
                    title_elem = container_tag.find("h3")
                    if title_elem:
                        title_tag = cast(Tag, title_elem)
                        link_elem = title_tag.find("a")
                    else:
                        link_elem = None
                    snippet_elem = container_tag.find("div", class_="compText")

                    if title_elem and link_elem:
                        # Cast elements to Tag for proper type checking
                        title_tag = cast(Tag, title_elem)
                        link_tag = cast(Tag, link_elem)
                        snippet_tag = cast(Tag, snippet_elem) if snippet_elem else None
                        result = {
                            "title": title_tag.get_text(strip=True),
                            "url": link_tag.get("href", ""),
                            "snippet": (
                                snippet_tag.get_text(strip=True) if snippet_tag else ""
                            ),
                            "position": i + 1,
                            "engine": "yahoo",
                        }
                        results.append(result)
                except Exception as e:
                    logger.debug(f"Error parsing Yahoo result: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing Yahoo results: {e}")

        return results

    def _parse_generic_results(
        self, html: str, num_results: int
    ) -> List[Dict[str, Any]]:
        """Parse generic search results."""
        results = []
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Find all links
            links = soup.find_all("a", href=True)

            for i, link in enumerate(links[:num_results]):
                try:
                    # Cast to Tag for proper type checking
                    link_tag = cast(Tag, link)

                    href = link_tag.get("href", "")
                    if isinstance(href, str) and href.startswith("http"):
                        result = {
                            "title": link_tag.get_text(strip=True) or href,
                            "url": href,
                            "snippet": "",
                            "position": i + 1,
                            "engine": "generic",
                        }
                        results.append(result)
                except Exception as e:
                    logger.debug(f"Error parsing generic result: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing generic results: {e}")

        return results

    def _aggregate_results(self, num_results: int = 10) -> Dict[str, Any]:
        """
        Aggregate and deduplicate results from all engines.

        Args:
            num_results: Maximum number of deduplicated results to return

        Returns:
            Dictionary with aggregated results and metadata
        """
        total_results = sum(len(results) for results in self.results.values())
        successful_engines = len(self.results)

        # Create aggregated results list with deduplication
        seen_urls = set()
        all_results = []

        # Sort results by engine priority: DuckDuckGo first, then Yahoo
        engine_priority = {"duckduckgo": 0, "yahoo": 1}

        for engine in sorted(
            self.results.keys(), key=lambda x: engine_priority.get(x, 999)
        ):
            results = self.results[engine]
            for result in results:
                url = result.get("url", "").lower().rstrip("/")

                # Skip duplicates based on URL
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    result_copy = result.copy()
                    result_copy["source_engine"] = engine
                    all_results.append(result_copy)

                    # Limit to prevent too many results
                    if (
                        len(all_results) >= num_results * 2
                    ):  # Allow some buffer for quality
                        break

        # Sort by position within each engine, then take top results
        all_results.sort(
            key=lambda x: (
                engine_priority.get(x.get("source_engine", ""), 999),
                x.get("position", 999),
            )
        )

        final_results = all_results[:num_results]

        return {
            "query": getattr(self, "query", ""),
            "total_raw_results": total_results,
            "deduplicated_results": len(final_results),
            "successful_engines": successful_engines,
            "failed_engines": self.failed_engines.copy(),
            "results": final_results,
            "engines_used": list(self.results.keys()),
            "timestamp": datetime.now().isoformat(),
        }

    def save_results(self, filename: Optional[str] = None) -> str:
        """Save aggregated results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"debug/multi_engine_search_{timestamp}.json"

        aggregated = self._aggregate_results()

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(aggregated, file, indent=2)

        logger.info(f"📄 Multi-engine search results saved to {filename}")
        return filename


# Multi-engine convenience function
async def multi_engine_search(
    query: str, num_results: int = 10, engines: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convenience function for multi-engine search.

    Args:
        query: Search query
        num_results: Number of results per engine
        engines: List of engines to use

    Returns:
        Aggregated results from all engines
    """
    searcher = MultiEngineSearch()
    return await searcher.search_all_engines(query, num_results, engines)
