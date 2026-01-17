"""
arXiv academic search provider.
Handles searching and retrieving papers from arXiv API.
"""

import asyncio
import requests
from typing import List, Dict, Optional, Any
from urllib.parse import quote

from src.logging.logger import logger


class ArXivProvider:
    """Provider for searching arXiv academic papers."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "RivalSearchMCP/1.0"})

    async def search(
        self,
        query: str,
        limit: int = 20,
        sort_by: str = "relevance",
        sort_order: str = "descending",
    ) -> List[Dict[str, Any]]:
        """
        Search papers using arXiv API.

        Args:
            query: Search query
            limit: Maximum number of results
            sort_by: Sort field (relevance, submittedDate, etc.)
            sort_order: Sort order (ascending, descending)

        Returns:
            List of paper dictionaries
        """
        try:
            base_url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": query,
                "start": 0,
                "max_results": min(limit, 200),  # API limit
                "sortBy": sort_by,
                "sortOrder": sort_order,
            }

            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.session.get(base_url, params=params, timeout=30)
            )

            if response.status_code == 200:
                papers = self._parse_arxiv_response(response.text, limit)
                logger.info(f"Found {len(papers)} papers from arXiv for query: {query}")
                return papers
            else:
                logger.warning(f"arXiv API error: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error searching arXiv: {e}")
            return []

    def _parse_arxiv_response(self, xml_content: str, limit: int) -> List[Dict[str, Any]]:
        """Parse arXiv XML response."""
        try:
            import xml.etree.ElementTree as ET

            # arXiv uses Atom XML format
            root = ET.fromstring(xml_content)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}

            papers = []
            entries = root.findall('atom:entry', namespace)

            for entry in entries[:limit]:
                try:
                    # Extract basic information
                    title_elem = entry.find('atom:title', namespace)
                    title = title_elem.text.strip() if title_elem is not None else "Unknown Title"

                    id_elem = entry.find('atom:id', namespace)
                    url = id_elem.text.strip() if id_elem is not None else ""

                    # Extract authors
                    authors = []
                    author_elems = entry.findall('atom:author', namespace)
                    for author_elem in author_elems:
                        name_elem = author_elem.find('atom:name', namespace)
                        if name_elem is not None:
                            authors.append({"name": name_elem.text.strip()})

                    # Extract publication date
                    published_elem = entry.find('atom:published', namespace)
                    published_date = published_elem.text.strip() if published_elem is not None else ""
                    year = published_date[:4] if published_date else None

                    # Extract abstract (summary)
                    summary_elem = entry.find('atom:summary', namespace)
                    abstract = summary_elem.text.strip() if summary_elem is not None else ""

                    paper = {
                        "title": title,
                        "authors": authors,
                        "abstract": abstract,
                        "url": url,
                        "year": year,
                        "source": "arxiv",
                        "paperId": url.split('/')[-1] if url else None,
                    }

                    papers.append(paper)

                except Exception as parse_error:
                    logger.warning(f"Error parsing arXiv entry: {parse_error}")
                    continue

            return papers

        except Exception as e:
            logger.error(f"Error parsing arXiv XML response: {e}")
            # Fallback: return basic result
            return [{
                "title": f"arXiv search results for: {query}",
                "url": f"https://arxiv.org/search/?query={quote(query)}",
                "source": "arxiv",
            }]

    async def get_paper_details(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific arXiv paper.

        Args:
            paper_id: arXiv paper ID (e.g., "2101.12345")

        Returns:
            Paper details or None if not found
        """
        try:
            url = f"http://export.arxiv.org/api/query?id_list={paper_id}"

            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.session.get(url, timeout=30)
            )

            if response.status_code == 200:
                papers = self._parse_arxiv_response(response.text, 1)
                return papers[0] if papers else None
            else:
                logger.warning(f"Failed to get arXiv paper details: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting arXiv paper details: {e}")
            return None

    def close(self):
        """Close the session."""
        self.session.close()