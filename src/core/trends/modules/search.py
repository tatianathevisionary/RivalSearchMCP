"""
Google Trends data retrieval methods.
Handles searching, querying, and fetching trends data from Google Trends API.
"""

import pandas as pd
from typing import List, Dict, Optional, Any

from src.logging.logger import logger
from .client import GoogleTrendsClient


class GoogleTrendsSearch:
    """Handles Google Trends data retrieval operations."""

    def __init__(self, client: GoogleTrendsClient):
        self.client = client

    def search_trends(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> pd.DataFrame:
        """
        Search for trends data for given keywords with professional rate limiting.

        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data (e.g., 'today 12-m', 'today 5-y')
            geo (str): Geographic location (e.g., 'US', 'GB')
            cat (int): Category ID (0 for all categories)

        Returns:
            pd.DataFrame: Trends data
        """
        def _execute_search():
            if not self.client.client:
                logger.error("Google Trends client not initialized")
                return pd.DataFrame()

            logger.info(f"🔍 Searching trends for: {keywords}")

            # Build payload (required before any data retrieval per pytrends docs)
            self.client.client.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)

            # Get interest over time
            data = self.client.client.interest_over_time()

            # Ensure we always return a DataFrame
            if data is None:
                logger.warning("PyTrends returned None - creating empty DataFrame")
                return pd.DataFrame()

            # Reset rate limit counter on successful request
            if not data.empty:
                self.client.rate_limit_hits = max(0, self.client.rate_limit_hits - 1)
                logger.info(f"✅ Retrieved trends data with {len(data)} data points")
                return data
            else:
                logger.warning("No trends data found")
                return pd.DataFrame()

        return self.client.execute_with_rate_limit(_execute_search) or pd.DataFrame()

    def get_interest_over_time(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> pd.DataFrame:
        """
        Get interest over time data (alias for search_trends).

        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID

        Returns:
            pd.DataFrame: Interest over time data
        """
        return self.search_trends(keywords, timeframe, geo, cat)

    def get_related_queries(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> Dict:
        """
        Get related queries for given keywords with rate limiting.

        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID

        Returns:
            Dict: Related queries data
        """
        def _execute_related_queries():
            if not self.client.client:
                logger.error("Google Trends client not initialized")
                return {}

            logger.info(f"🔍 Getting related queries for: {keywords}")

            # Build payload
            self.client.client.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)

            # Get related queries
            related = self.client.client.related_queries()

            # Reset rate limit counter on success
            if related:
                self.client.rate_limit_hits = max(0, self.client.rate_limit_hits - 1)

            logger.info("✅ Retrieved related queries data")
            return related or {}

        return self.client.execute_with_rate_limit(_execute_related_queries) or {}

    def get_related_topics(
        self,
        keywords: List[str],
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> Dict:
        """
        Get related topics for given keywords.

        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID

        Returns:
            Dict: Related topics data
        """
        def _execute_related_topics():
            if not self.client.client:
                logger.error("Google Trends client not initialized")
                return {}

            logger.info(f"🔍 Getting related topics for: {keywords}")

            # Build payload
            self.client.client.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)

            # Get related topics
            topics = self.client.client.related_topics()

            # Reset rate limit counter on success
            if topics:
                self.client.rate_limit_hits = max(0, self.client.rate_limit_hits - 1)

            logger.info("✅ Retrieved related topics data")
            return topics or {}

        return self.client.execute_with_rate_limit(_execute_related_topics) or {}

    def get_interest_by_region(
        self,
        keywords: List[str],
        resolution: str = "COUNTRY",
        timeframe: str = "today 12-m",
        geo: str = "",
        cat: int = 0,
    ) -> pd.DataFrame:
        """
        Get interest by region data.

        Args:
            keywords (List[str]): List of search terms
            resolution (str): Geographic resolution ('COUNTRY', 'REGION', 'CITY')
            timeframe (str): Time range for data
            geo (str): Geographic location filter
            cat (int): Category ID

        Returns:
            pd.DataFrame: Interest by region data
        """
        def _execute_region_data():
            if not self.client.client:
                logger.error("Google Trends client not initialized")
                return pd.DataFrame()

            logger.info(f"🔍 Getting interest by region for: {keywords}")

            # Build payload
            self.client.client.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)

            # Get interest by region
            region_data = self.client.client.interest_by_region(
                resolution=resolution, inc_low_vol=True, inc_geo_code=True
            )

            # Reset rate limit counter on success
            if region_data is not None and not region_data.empty:
                self.client.rate_limit_hits = max(0, self.client.rate_limit_hits - 1)

            logger.info("✅ Retrieved regional interest data")
            return region_data if region_data is not None else pd.DataFrame()

        return self.client.execute_with_rate_limit(_execute_region_data) or pd.DataFrame()

    def get_trending_searches(self, geo: str = "US") -> List[str]:
        """
        Get trending searches for a geographic location.

        Args:
            geo (str): Geographic location code

        Returns:
            List[str]: Trending search terms
        """
        def _execute_trending():
            if not self.client.client:
                logger.error("Google Trends client not initialized")
                return []

            logger.info(f"🔍 Getting trending searches for: {geo}")

            # Get trending searches
            trending = self.client.client.trending_searches(pn=geo)

            # Reset rate limit counter on success
            if trending:
                self.client.rate_limit_hits = max(0, self.client.rate_limit_hits - 1)

            logger.info(f"✅ Retrieved {len(trending) if trending else 0} trending searches")
            return trending if trending else []

        return self.client.execute_with_rate_limit(_execute_trending) or []

    def get_realtime_trending_searches(self, geo: str = "US") -> List[str]:
        """
        Get real-time trending searches.

        Args:
            geo (str): Geographic location code

        Returns:
            List[str]: Real-time trending search terms
        """
        def _execute_realtime():
            if not self.client.client:
                logger.error("Google Trends client not initialized")
                return []

            logger.info(f"🔍 Getting real-time trending searches for: {geo}")

            # Get real-time trending searches
            realtime = self.client.client.realtime_trending_searches(pn=geo)

            # Reset rate limit counter on success
            if realtime:
                self.client.rate_limit_hits = max(0, self.client.rate_limit_hits - 1)

            logger.info(f"✅ Retrieved {len(realtime) if realtime else 0} real-time trending searches")
            return realtime if realtime else []

        return self.client.execute_with_rate_limit(_execute_realtime) or []