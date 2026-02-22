"""
Academic search module for scientific research tools.
Provides unified interface to academic search and dataset discovery.
"""

from typing import Any, Dict, List

from .datasets.orchestrator import DatasetDiscoveryOrchestrator
from .search.orchestrator import AcademicSearchOrchestrator


class AcademicSearch:
    """Unified interface for academic search and dataset discovery."""

    def __init__(self):
        self.academic_orchestrator = AcademicSearchOrchestrator()
        self.dataset_orchestrator = DatasetDiscoveryOrchestrator()

    # Academic search methods - delegate to orchestrator
    async def search_semantic_scholar(
        self, query: str, limit: int = 20, **kwargs
    ) -> List[Dict[str, Any]]:
        """Search Semantic Scholar."""
        return await self.academic_orchestrator.providers["semantic_scholar"].search(
            query, limit, **kwargs
        )

    async def search_arxiv(self, query: str, limit: int = 20, **kwargs) -> List[Dict[str, Any]]:
        """Search arXiv."""
        return await self.academic_orchestrator.providers["arxiv"].search(query, limit, **kwargs)

    async def search_pubmed(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search PubMed."""
        return await self.academic_orchestrator.providers["pubmed"].search(query, limit)

    async def search_combined_academic(
        self, query: str, sources: List[str] = None, max_results: int = 50, **kwargs
    ) -> Dict[str, Any]:
        """Search across multiple academic sources."""
        return await self.academic_orchestrator.search_combined_academic(
            query, sources, max_results, **kwargs
        )


class DatasetDiscovery:
    """Unified interface for dataset discovery."""

    def __init__(self):
        self.orchestrator = DatasetDiscoveryOrchestrator()

    # Dataset search methods - delegate to orchestrator
    async def search_kaggle_datasets(
        self, query: str, limit: int = 20, **kwargs
    ) -> List[Dict[str, Any]]:
        """Search Kaggle datasets."""
        return await self.orchestrator.providers["kaggle"].search(query, limit, **kwargs)

    async def search_huggingface_datasets(
        self, query: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search HuggingFace datasets."""
        return await self.orchestrator.providers["huggingface"].search(query, limit)

    async def search_combined_datasets(
        self, query: str, sources: List[str] = None, max_results: int = 50, **kwargs
    ) -> Dict[str, Any]:
        """Search across multiple dataset sources."""
        return await self.orchestrator.search_combined_datasets(
            query, sources, max_results, **kwargs
        )
