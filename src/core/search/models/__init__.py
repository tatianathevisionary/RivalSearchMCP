"""
Models package for search functionality.
"""

# Base models
from .base import BaseSearchResult, BaseSearchMetadata, BaseSearchRequest


# DuckDuckGo models
from .duckduckgo import (
    DuckDuckGoSearchResult,
    DuckDuckGoSearchMetadata,
    DuckDuckGoInstantAnswer,
    DuckDuckGoRelatedTopic,
)

# Yahoo models
from .yahoo import (
    YahooSearchResult,
    YahooSearchMetadata,
    YahooNewsResult,
    YahooVideoResult,
    YahooImageResult,
)

__all__ = [
    # Base models
    "BaseSearchResult",
    "BaseSearchMetadata",
    "BaseSearchRequest",
    # DuckDuckGo models
    "DuckDuckGoSearchResult",
    "DuckDuckGoSearchMetadata",
    "DuckDuckGoInstantAnswer",
    "DuckDuckGoRelatedTopic",
    # Yahoo models
    "YahooSearchResult",
    "YahooSearchMetadata",
    "YahooNewsResult",
    "YahooVideoResult",
    "YahooImageResult",
]
