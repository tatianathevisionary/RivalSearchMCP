"""
Core module for RivalSearchMCP.
Main functionality for search, fetch, bypass, and content processing.
"""

from .bypass import (
    detect_paywall,
    get_archive_url,
    get_proxies,
    refresh_proxies,
    select_proxy,
    test_proxy,
)



from .fetch import (
    base_fetch_url,
    stream_fetch,
    batch_rival_retrieve,
    rival_retrieve,
    google_search_fetch,
)




from .search import (
    BaseSearchEngine,
    MultiSearchResult,
    DuckDuckGoSearchEngine,
    YahooSearchEngine,
)

from .traverse import (
    traverse_website,
    get_sitemap,
    extract_links,
    analyze_structure,
)

# Removed unused imports:
# from .trends import GoogleTrendsAPI  # Trends tools removed
# from .llms import ContentProcessor, LLMsTxtGenerator  # Module doesn't exist

__all__ = [
    # Bypass
    "detect_paywall",
    "get_archive_url",
    "get_proxies",
    "refresh_proxies",
    "select_proxy",
    "test_proxy",
    # Extract


    # Fetch
    "base_fetch_url",
    "stream_fetch",
    "batch_rival_retrieve",
    "rival_retrieve",
    "google_search_fetch",
    # Search
    "BaseSearchEngine",
    "MultiSearchResult",
    "DuckDuckGoSearchEngine",
    "YahooSearchEngine",
    # Traverse
    "traverse_website",
    "get_sitemap",
    "extract_links",
    "analyze_structure",
    # Trends
    "GoogleTrendsAPI",
    # LLMs
    "ContentProcessor",
    "LLMsTxtGenerator",
]
