"""
Academic search orchestrator.
Coordinates searching across multiple academic paper providers.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.logging.logger import logger

from .providers.arxiv import ArXivProvider
from .providers.pubmed import PubMedProvider
from .providers.semantic_scholar import SemanticScholarProvider


class AcademicSearchOrchestrator:
    """Orchestrates academic paper searches across multiple providers."""

    def __init__(self):
        self.providers = {
            "semantic_scholar": SemanticScholarProvider(),
            "arxiv": ArXivProvider(),
            "pubmed": PubMedProvider(),
        }

    async def search_academic_papers(
        self, query: str, sources: List[str] = None, limit: int = 20, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search for academic papers across multiple sources.

        Args:
            query: Search query
            sources: List of sources to search (default: all)
            limit: Maximum results per source
            **kwargs: Additional parameters for specific providers

        Returns:
            List of paper dictionaries with deduplication
        """
        if sources is None:
            sources = list(self.providers.keys())

        # Validate sources
        valid_sources = [s for s in sources if s in self.providers]
        if not valid_sources:
            logger.warning(f"No valid sources specified: {sources}")
            return []

        # Search all requested sources concurrently
        search_tasks = []
        for source in valid_sources:
            provider = self.providers[source]
            search_method = getattr(provider, "search", None)
            if search_method:
                task = search_method(query, limit, **kwargs)
                search_tasks.append((source, task))
            else:
                logger.warning(f"Provider {source} has no search method")

        # Execute searches concurrently
        results = {}
        if search_tasks:
            try:
                search_results = await asyncio.gather(
                    *[task for _, task in search_tasks], return_exceptions=True
                )

                for i, (source, _) in enumerate(search_tasks):
                    result = search_results[i]
                    if isinstance(result, Exception):
                        logger.error(f"Search failed for {source}: {result}")
                        results[source] = {"status": "error", "error": str(result), "papers": []}
                    else:
                        results[source] = {"status": "success", "papers": result or []}

            except Exception as e:
                logger.error(f"Concurrent search execution failed: {e}")
                for source, _ in search_tasks:
                    results[source] = {"status": "error", "error": str(e), "papers": []}

        # Extract and deduplicate papers
        all_papers = []
        for source_data in results.values():
            papers = source_data.get("papers", [])
            all_papers.extend(papers)

        # Deduplicate by title (case-insensitive)
        seen_titles = set()
        deduplicated_papers = []

        for paper in all_papers:
            title = paper.get("title", "").strip().lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                deduplicated_papers.append(paper)

        # Sort by relevance (sources in priority order)
        source_priority = {source: i for i, source in enumerate(valid_sources)}
        deduplicated_papers.sort(
            key=lambda p: (
                source_priority.get(p.get("source", ""), len(source_priority)),
                -int(p.get("citationCount") or 0),  # Higher citations first
                -int(p.get("year") or 0),  # More recent first
            )
        )

        logger.info(
            f"Academic search completed: {len(deduplicated_papers)} unique papers from {len(valid_sources)} sources"
        )
        return deduplicated_papers[:limit]  # Return only requested limit

    async def get_paper_details(self, paper_id: str, source: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific paper.

        Args:
            paper_id: Paper identifier
            source: Source provider

        Returns:
            Paper details or None
        """
        if source not in self.providers:
            logger.warning(f"Unknown source: {source}")
            return None

        provider = self.providers[source]
        details_method = getattr(provider, "get_paper_details", None)
        if details_method:
            try:
                return await details_method(paper_id)
            except Exception as e:
                logger.error(f"Failed to get paper details from {source}: {e}")
                return None
        else:
            logger.warning(f"Provider {source} has no get_paper_details method")
            return None

    async def search_combined_academic(
        self, query: str, sources: List[str] = None, max_results: int = 50, **kwargs
    ) -> Dict[str, Any]:
        """
        Comprehensive academic search with metadata.

        Args:
            query: Search query
            sources: List of sources to search
            max_results: Maximum total results
            **kwargs: Additional search parameters

        Returns:
            Comprehensive search results with metadata
        """
        start_time = datetime.now()

        papers = await self.search_academic_papers(
            query=query, sources=sources, limit=max_results, **kwargs
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Generate metadata
        sources_used = sources or list(self.providers.keys())
        papers_by_source = {}
        for paper in papers:
            source = paper.get("source", "unknown")
            if source not in papers_by_source:
                papers_by_source[source] = []
            papers_by_source[source].append(paper)

        metadata = {
            "query": query,
            "total_results": len(papers),
            "sources_searched": sources_used,
            "results_by_source": {
                source: len(papers) for source, papers in papers_by_source.items()
            },
            "search_duration_seconds": duration,
            "timestamp": end_time.isoformat(),
        }

        # Sort papers by relevance score (if available) or citation count
        papers.sort(key=lambda p: (-int(p.get("citationCount") or 0), -int(p.get("year") or 0)))

        return {
            "status": "success",
            "metadata": metadata,
            "papers": papers,
        }

    def close(self):
        """Close all provider connections."""
        for provider in self.providers.values():
            try:
                provider.close()
            except Exception as e:
                logger.warning(f"Error closing provider: {e}")
