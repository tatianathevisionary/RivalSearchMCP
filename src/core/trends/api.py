"""
Google Trends API core functionality for RivalSearchMCP.
Provides access to Google Trends data through modular components.
"""

import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from src.logging.logger import logger
from .modules.client import GoogleTrendsClient
from .modules.search import GoogleTrendsSearch


class GoogleTrendsAPI:
    """
    A comprehensive wrapper for Google Trends data using pytrends.
    Provides access to all Google Trends functionality through modular components.
    """

    def __init__(
        self,
        hl="en-US",
        tz=360,
        timeout=(10, 25),
        retries=3,
        backoff_factor=0.3,
        proxies=None,
        requests_args=None,
    ):
        """
        Initialize the Google Trends API wrapper.

        Args:
            hl (str): Language (default: 'en-US')
            tz (int): Timezone offset in minutes (default: 360 for EST)
            timeout (tuple): Request timeout (connect, read)
            retries (int): Number of retries for failed requests
            backoff_factor (float): Backoff factor for retries
            proxies (list): List of HTTPS proxies to rotate through
            requests_args (dict): Additional requests library arguments
        """
        self.client = GoogleTrendsClient(
            hl=hl,
            tz=tz,
            timeout=timeout,
            retries=retries,
            backoff_factor=backoff_factor,
            proxies=proxies,
            requests_args=requests_args,
        )
        self.search = GoogleTrendsSearch(self.client)

    # Delegate search methods to the search module
    def search_trends(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> pd.DataFrame:
        """Search for trends data."""
        return self.search.search_trends(keywords, timeframe, geo, cat)

    def get_interest_over_time(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> pd.DataFrame:
        """Get interest over time data."""
        return self.search.get_interest_over_time(keywords, timeframe, geo, cat)

    def get_related_queries(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> Dict:
        """Get related queries."""
        return self.search.get_related_queries(keywords, timeframe, geo, cat)

    def get_related_topics(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> Dict:
        """Get related topics."""
        return self.search.get_related_topics(keywords, timeframe, geo, cat)

    def get_interest_by_region(
        self,
        keywords: List[str],
        resolution: str = "COUNTRY",
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> pd.DataFrame:
        """Get interest by region data."""
        return self.search.get_interest_by_region(keywords, resolution, timeframe, geo, cat)

    def get_trending_searches(self, geo: str = "US") -> List[str]:
        """Get trending searches."""
        return self.search.get_trending_searches(geo)

    def get_realtime_trending_searches(self, geo: str = "US") -> List[str]:
        """Get real-time trending searches."""
        return self.search.get_realtime_trending_searches(geo)

    # Delegate client management methods
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get rate limiting status."""
        return self.client.get_rate_limit_status()

    def reset_rate_limit_counter(self):
        """Reset rate limiting counters."""
        self.client.reset_rate_limit_counter()

    def set_proxy_list(self, proxies: List[str]):
        """Update proxy list."""
        self.client.set_proxy_list(proxies)

    def is_available(self) -> bool:
        """Check if client is available."""
        return self.client.is_available()

    def close(self):
        """Close client resources."""
        self.client.close()

    # Static utility methods
    @staticmethod
    def get_available_timeframes() -> List[str]:
        """Get available timeframe options."""
        return [
            "now 1-H",      # Last hour
            "now 4-H",      # Last 4 hours
            "now 1-d",      # Last day
            "now 7-d",      # Last 7 days
            "today 1-m",    # Past 30 days
            "today 3-m",    # Past 90 days
            "today 5-y",    # Past 5 years
            "today 12-m",   # Past 12 months
        ]

    @staticmethod
    def get_available_regions() -> List[str]:
        """Get available geographic region codes."""
        return [
            "US", "GB", "CA", "AU", "DE", "FR", "IT", "ES", "NL", "BE",
            "CH", "AT", "SE", "NO", "DK", "FI", "PT", "IE", "GR", "PL",
            "CZ", "HU", "SK", "SI", "HR", "BA", "ME", "MK", "AL", "RS",
            "RO", "BG", "TR", "RU", "UA", "BY", "MD", "GE", "AM", "AZ",
            "JP", "KR", "CN", "HK", "TW", "SG", "MY", "TH", "ID", "PH",
            "VN", "IN", "PK", "BD", "LK", "NP", "MM", "KH", "LA", "BN",
            "TL", "AU", "NZ", "FJ", "PG", "SB", "VU", "NC", "PF", "WS",
            "TO", "TV", "KI", "MH", "FM", "PW", "MP", "GU", "AS", "CK",
            "NU", "TK", "NF", "CX", "CC", "HM", "AQ",
        ]