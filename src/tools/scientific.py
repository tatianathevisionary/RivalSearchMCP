"""
Scientific research tools for FastMCP server.
Provides academic paper search and dataset discovery using refactored modules.
"""

from typing import List, Dict, Optional, Any
from fastmcp import FastMCP
from fastmcp import Context
from fastmcp.server.context import Context
from pydantic import Field
from typing_extensions import Annotated

from src.core.scientific.search.orchestrator import AcademicSearchOrchestrator
from src.core.scientific.datasets.orchestrator import DatasetDiscoveryOrchestrator
from src.utils.markdown_formatter import (
    format_academic_search_markdown,
    format_dataset_discovery_markdown,
)
from src.logging.logger import logger


def register_scientific_tools(mcp: FastMCP):
    """Register scientific research tools using refactored orchestrators."""

    academic_orchestrator = AcademicSearchOrchestrator()
    dataset_orchestrator = DatasetDiscoveryOrchestrator()

    @mcp.tool
    async def scientific_research(
        ctx: Context,
        operation: Annotated[
            str,
            Field(description="Operation type: 'academic_search' or 'dataset_discovery'")
        ],
        query: Annotated[
            str,
            Field(description="Search query", min_length=1, max_length=500)
        ],
        max_results: Annotated[
            int,
            Field(description="Maximum results to return", ge=1, le=50, default=10)
        ] = 10,
        sources: Annotated[
            Optional[List[str]],
            Field(description="Specific sources to search (optional)")
        ] = None,
        categories: Annotated[
            Optional[List[str]],
            Field(description="Categories for dataset discovery (optional)")
        ] = None,
    ) -> str:
        """
        Scientific research tool for academic papers and datasets.

        Supports two operations:
        - academic_search: Search for academic papers across multiple sources
        - dataset_discovery: Discover datasets from various repositories

        Sources for academic_search: semantic_scholar, arxiv, pubmed
        Sources for dataset_discovery: kaggle, huggingface
        """
        try:
            if ctx:
                await ctx.report_progress(progress=0, total=100)
                await ctx.info(f"🔬 Performing {operation} for: {query}")

            if operation == "academic_search":
                if sources is None:
                    sources = ["semantic_scholar", "arxiv"]

                result = await academic_orchestrator.search_academic_papers(
                    query=query,
                    sources=sources,
                    limit=max_results
                )

                formatted_result = format_academic_search_markdown({
                    "status": "success",
                    "query": query,
                    "results": result,
                    "metadata": {
                        "total_results": len(result),
                        "sources_used": sources,
                        "timestamp": "now",
                    },
                })

            elif operation == "dataset_discovery":
                if categories is None:
                    categories = ["computer_science"]

                result = await dataset_orchestrator.search_datasets(
                    query=query,
                    sources=sources,
                    limit=max_results
                )

                formatted_result = format_dataset_discovery_markdown({
                    "status": "success",
                    "query": query,
                    "datasets": result,
                    "metadata": {
                        "total_results": len(result),
                        "categories_searched": categories,
                        "timestamp": "now",
                    },
                })

            else:
                formatted_result = format_academic_search_markdown({
                    "status": "error",
                    "error": f"Unknown operation: {operation}",
                    "query": query,
                })

            if ctx:
                await ctx.report_progress(progress=100, total=100)

            return formatted_result

        except Exception as e:
            logger.error(f"Scientific research failed: {e}")
            error_result = {
                "status": "error",
                "error": str(e),
                "query": query,
                "operation": operation,
            }

            if "dataset" in operation:
                return format_dataset_discovery_markdown(error_result)
            else:
                return format_academic_search_markdown(error_result)