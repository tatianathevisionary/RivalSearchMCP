#!/usr/bin/env python3
"""
Base HTML parser class for search engines.
Provides common parsing functionality that can be extended.
"""

import re
from typing import List, cast
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup, Tag

from src.logging.logger import logger
from ..models.base import BaseSearchResult


class BaseSearchParser(ABC):
    """Base class for search engine HTML parsers."""

    def __init__(self):
        """Initialize the parser."""

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        cleaned_text = re.sub(r"\s+", " ", text)
        return cleaned_text.strip()

    def estimate_traffic(self, position: int) -> str:
        """Estimate traffic based on search position (rough approximation)."""
        if position <= 3:
            return "high"
        elif position <= 10:
            return "medium"
        else:
            return "low"

    def _extract_clean_url(self, href: str) -> str:
        """Extract clean URL from search engine href attribute."""
        try:
            from urllib.parse import unquote

            # Handle Google-style redirects
            if href.startswith("/url?q="):
                url = href.split("&")[0].replace("/url?q=", "")
                return unquote(url)
            elif href.startswith("http"):
                return href
            else:
                return ""
        except Exception:
            return ""

    @abstractmethod
    def parse_search_results(self, soup: BeautifulSoup) -> List["BaseSearchResult"]:
        """Parse search results from BeautifulSoup object. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def extract_search_features(self, result_block) -> List[str]:
        """Extract additional features from search results. Must be implemented by subclasses."""
        pass
