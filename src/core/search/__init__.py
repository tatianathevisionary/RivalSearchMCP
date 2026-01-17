#!/usr/bin/env python3
"""
Search functionality package for RivalSearchMCP.
Provides multi-engine search capabilities with content extraction.
"""

# Core search functionality
from .core import BaseSearchEngine, MultiSearchResult, MultiEngineSearch

# Search engines
from .engines import DuckDuckGoSearchEngine, YahooSearchEngine

# Parsers and scrapers
# Models

__all__ = [
    # Core
    "BaseSearchEngine",
    "MultiSearchResult",
    "MultiEngineSearch",
    # Engines
    "DuckDuckGoSearchEngine",
    "YahooSearchEngine",
]
