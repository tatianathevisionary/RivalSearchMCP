"""
PubMed academic search provider.
Handles searching and retrieving papers from PubMed API.
"""

import asyncio
from typing import Any, Dict, List, Optional

import requests

from src.logging.logger import logger


class PubMedProvider:
    """Provider for searching PubMed academic papers."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "RivalSearchMCP/1.0",
                "Email": "research@example.com",  # Required by NCBI
            }
        )

    async def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search papers using PubMed API.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of paper dictionaries
        """
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

            # First, search for IDs
            search_params = {
                "db": "pubmed",
                "term": query,
                "retmax": min(limit, 100),
                "retmode": "json",
                "sort": "relevance",
            }

            search_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(
                    f"{base_url}esearch.fcgi", params=search_params, timeout=30
                ),
            )

            if search_response.status_code != 200:
                logger.warning(f"PubMed search API error: {search_response.status_code}")
                return []

            search_data = search_response.json()
            ids = search_data.get("esearchresult", {}).get("idlist", [])

            if not ids:
                logger.info(f"No PubMed results found for query: {query}")
                return []

            # Fetch details for found IDs (limit to prevent API abuse)
            fetch_limit = min(limit, 20)  # Conservative limit for XML parsing
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(ids[:fetch_limit]),
                "retmode": "xml",
            }

            fetch_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(f"{base_url}efetch.fcgi", params=fetch_params, timeout=30),
            )

            if fetch_response.status_code == 200:
                papers = self._parse_pubmed_response(fetch_response.text)
                logger.info(f"Found {len(papers)} papers from PubMed for query: {query}")
                return papers
            else:
                logger.warning(f"PubMed fetch API error: {fetch_response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error searching PubMed: {e}")
            return []

    def _parse_pubmed_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """Parse PubMed XML response."""
        try:
            import xml.etree.ElementTree as ET

            root = ET.fromstring(xml_content)
            papers = []

            # PubMed XML structure
            articles = root.findall(".//PubmedArticle") or root.findall(".//Article")

            for article in articles:
                try:
                    paper = {}

                    # Extract title
                    title_elem = article.find(".//ArticleTitle")
                    if title_elem is not None and title_elem.text:
                        paper["title"] = title_elem.text.strip()

                    # Extract abstract
                    abstract_elem = article.find(".//AbstractText")
                    if abstract_elem is not None and abstract_elem.text:
                        paper["abstract"] = abstract_elem.text.strip()

                    # Extract authors
                    authors = []
                    author_elems = article.findall(".//Author")
                    for author_elem in author_elems:
                        name_elem = author_elem.find(".//LastName")
                        fore_elem = author_elem.find(".//ForeName")
                        if name_elem is not None:
                            name = name_elem.text or ""
                            if fore_elem is not None and fore_elem.text:
                                name = f"{fore_elem.text} {name}"
                            authors.append({"name": name.strip()})

                    paper["authors"] = authors

                    # Extract publication year
                    year_elem = article.find(".//PubDate/Year")
                    if year_elem is not None and year_elem.text:
                        paper["year"] = int(year_elem.text.strip())

                    # Extract PMID
                    pmid_elem = article.find(".//PMID")
                    if pmid_elem is not None and pmid_elem.text:
                        paper["paperId"] = pmid_elem.text.strip()
                        paper["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid_elem.text.strip()}/"

                    # Extract journal/venue
                    journal_elem = article.find(".//Journal/Title")
                    if journal_elem is not None and journal_elem.text:
                        paper["venue"] = journal_elem.text.strip()

                    paper["source"] = "pubmed"

                    if paper.get("title"):  # Only add if we have at least a title
                        papers.append(paper)

                except Exception as parse_error:
                    logger.warning(f"Error parsing PubMed article: {parse_error}")
                    continue

            return papers

        except Exception as e:
            logger.error(f"Error parsing PubMed XML response: {e}")
            return []

    async def get_paper_details(self, pmid: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific PubMed paper.

        Args:
            pmid: PubMed ID

        Returns:
            Paper details or None if not found
        """
        try:
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
            params = {
                "db": "pubmed",
                "id": pmid,
                "retmode": "xml",
            }

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(f"{base_url}efetch.fcgi", params=params, timeout=30),
            )

            if response.status_code == 200:
                papers = self._parse_pubmed_response(response.text)
                return papers[0] if papers else None
            else:
                logger.warning(f"Failed to get PubMed paper details: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting PubMed paper details: {e}")
            return None

    def close(self):
        """Close the session."""
        self.session.close()
