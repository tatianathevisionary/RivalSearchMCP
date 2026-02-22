"""
Core search functionality package.
"""

from .engine import MultiEngineSearch
from .multi_engines import BaseSearchEngine, MultiSearchResult

__all__ = ["BaseSearchEngine", "MultiSearchResult", "MultiEngineSearch"]
