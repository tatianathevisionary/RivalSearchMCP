"""
Semantic Scholar academic search provider.

Uses the public Graph API at api.semanticscholar.org/graph/v1. Works
without an API key but is aggressively rate-limited (shared quota
across all anonymous callers, routinely returns 429 during peak
hours). When 429 arrives we log at info level and return an empty
list -- the aggregator catches it and other providers still return
their results.

Set `SEMANTIC_SCHOLAR_API_KEY` in the environment to raise this
caller's quota; the key is forwarded via the `x-api-key` header when
present.
"""

import os
from typing import Any, Dict, List, Optional

import httpx

from src.logging.logger import logger

_API_BASE = "https://api.semanticscholar.org/graph/v1"
_DEFAULT_FIELDS = [
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


class SemanticScholarProvider:
    """Search Semantic Scholar via the public Graph API."""

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "rivalsearchmcp/1.0 " "(+https://github.com/damionrashford/RivalSearchMCP)"
            ),
            "Accept": "application/json",
        }
        api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip()
        if api_key:
            self.headers["x-api-key"] = api_key

    async def search(
        self,
        query: str,
        limit: int = 20,
        fields: Optional[List[str]] = None,
        year: Optional[str] = None,
        venue: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {
            "query": query,
            "limit": min(limit, 100),
            "fields": ",".join(fields or _DEFAULT_FIELDS),
        }
        if year:
            params["year"] = year
        if venue:
            params["venue"] = venue

        try:
            async with httpx.AsyncClient(
                headers=self.headers, timeout=30.0, follow_redirects=True
            ) as client:
                r = await client.get(f"{_API_BASE}/paper/search", params=params)
                if r.status_code == 429:
                    logger.info(
                        "semantic_scholar rate-limited (429); skipping this call "
                        "(set SEMANTIC_SCHOLAR_API_KEY for higher quota)"
                    )
                    return []
                if r.status_code != 200:
                    logger.warning(
                        "semantic_scholar returned %s (body: %s)",
                        r.status_code,
                        r.text[:200],
                    )
                    return []
                papers = r.json().get("data", [])
                for p in papers:
                    p["source"] = "semantic_scholar"
                logger.info("semantic_scholar: %d for %r", len(papers), query)
                return papers
        except httpx.HTTPError as e:
            logger.warning("semantic_scholar network error: %s", e)
            return []
        except Exception:
            logger.exception("semantic_scholar unexpected error")
            return []

    async def get_paper_details(
        self, paper_id: str, fields: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        params = {
            "fields": ",".join(
                fields
                or [
                    "title",
                    "abstract",
                    "authors",
                    "year",
                    "venue",
                    "citationCount",
                    "references",
                    "citations",
                ]
            )
        }
        try:
            async with httpx.AsyncClient(
                headers=self.headers, timeout=30.0, follow_redirects=True
            ) as client:
                r = await client.get(f"{_API_BASE}/paper/{paper_id}", params=params)
                if r.status_code != 200:
                    return None
                return r.json()
        except Exception:
            logger.exception("semantic_scholar get_paper_details failed")
            return None

    def close(self):
        """Nothing to close; AsyncClient is used per-call."""
