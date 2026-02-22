"""
Fetch module for RivalSearchMCP.
Handles URL fetching and batch retrieval.
"""

from .base import (
    BaseFetcher,
    BatchFetcher,
    EnhancedFetcher,
    UnifiedFetcher,
    URLFetcher,
    base_fetch_url,
    stream_fetch,
)
from .batch import batch_rival_retrieve
from .enhanced import google_search_fetch, rival_retrieve

__all__ = [
    "base_fetch_url",
    "stream_fetch",
    "batch_rival_retrieve",
    "rival_retrieve",
    "google_search_fetch",
    "BaseFetcher",
    "URLFetcher",
    "BatchFetcher",
    "EnhancedFetcher",
    "UnifiedFetcher",
]
