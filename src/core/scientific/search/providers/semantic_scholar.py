"""
Semantic Scholar academic search provider.
Handles searching and retrieving papers from Semantic Scholar API.
"""

import asyncio
import requests
from typing import List, Dict, Optional, Any

from src.logging.logger import logger


class SemanticScholarProvider:
    """Provider for searching Semantic Scholar academic papers."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "RivalSearchMCP/1.0"})

    async def search(
        self,
        query: str,
        limit: int = 20,
        fields: Optional[List[str]] = None,
        year: Optional[str] = None,
        venue: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search papers using Semantic Scholar API.

        Args:
            query: Search query
            limit: Maximum number of results
            fields: Fields to retrieve
            year: Publication year filter
            venue: Venue filter

        Returns:
            List of paper dictionaries
        """
        if fields is None:
            fields = [
                "title",
                "abstract",
                "authors",
                "year",
                "venue",
                "citationCount",
                "openAccessPdf",
                "url",
                "paperId",
                "publicationDate",
                "fieldsOfStudy",
            ]

        params = {
            "query": query,
            "limit": min(limit, 100),  # API limit
            "fields": ",".join(fields),
        }

        if year:
            params["year"] = year
        if venue:
            params["venue"] = venue

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(
                    "https://api.semanticscholar.org/graph/v1/paper/search",
                    params=params,
                    timeout=30,
                ),
            )

            if response.status_code == 200:
                data = response.json()
                papers = data.get("data", [])
                logger.info(
                    f"Found {len(papers)} papers from Semantic Scholar for query: {query}"
                )
                return papers
            else:
                logger.warning(
                    f"Semantic Scholar API error: {response.status_code} - {response.text}"
                )
                return []

        except Exception as e:
            logger.error(f"Error searching Semantic Scholar: {e}")
            return []

    async def get_paper_details(self, paper_id: str, fields: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific paper.

        Args:
            paper_id: Semantic Scholar paper ID
            fields: Fields to retrieve

        Returns:
            Paper details or None if not found
        """
        if fields is None:
            fields = ["title", "abstract", "authors", "year", "venue", "citationCount", "references", "citations"]

        params = {"fields": ",".join(fields)}

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(
                    f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}",
                    params=params,
                    timeout=30,
                ),
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Failed to get paper details: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting paper details: {e}")
            return None

    def close(self):
        """Close the session."""
        self.session.close()