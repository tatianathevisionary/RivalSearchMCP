"""
Google Trends client management.
Handles initialization, rate limiting, and connection management for Google Trends API.
"""

import os
import time
from typing import Any, Dict, List, Optional, Tuple

from src.logging.logger import logger


class GoogleTrendsClient:
    """Manages Google Trends API client initialization and rate limiting."""

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
        Initialize the Google Trends client with professional rate limiting.

        Args:
            hl (str): Language (default: 'en-US')
            tz (int): Timezone offset in minutes (default: 360 for EST)
            timeout (tuple): Request timeout (connect, read)
            retries (int): Number of retries for failed requests
            backoff_factor (float): Backoff factor for retries (0.1 recommended)
            proxies (list): List of HTTPS proxies to rotate through
            requests_args (dict): Additional requests library arguments
        """
        self.hl = hl
        self.tz = tz
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.proxies = proxies or []
        self.requests_args = requests_args or {}

        # Rate limiting state
        self.last_request_time = None
        self.request_count = 0
        self.rate_limit_hits = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests
        self.rate_limit_sleep = 60  # 60 seconds sleep when rate limited

        # Initialize pytrends client
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the pytrends client with proper configuration."""
        from pytrends.request import TrendReq

        logger.info("Initializing Google Trends client...")

        # Set up requests args for SSL certificate handling
        requests_args = self.requests_args.copy()
        if "verify" not in requests_args:
            requests_args["verify"] = True  # Default to verify SSL

        # Handle REQUESTS_CA_BUNDLE for SSL certificate issues
        if "REQUESTS_CA_BUNDLE" not in os.environ:
            # Try to set a reasonable default if certifi is available
            try:
                import certifi
                os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
                logger.debug("Set REQUESTS_CA_BUNDLE to certifi location")
            except ImportError:
                logger.warning(
                    "certifi not available - SSL certificate verification may fail"
                )

        try:
            # Initialize with proper parameters per pytrends documentation
            logger.info(f"Creating TrendReq with hl={self.hl}, tz={self.tz}")

            # Prepare parameters, ensuring no None values that pytrends can't handle
            trendreq_kwargs = {
                "hl": self.hl,
                "tz": self.tz,
                "timeout": self.timeout,
                "retries": self.retries,
                "backoff_factor": self.backoff_factor,
                "requests_args": requests_args,
            }

            # Only add proxies if we actually have them
            if self.proxies:
                trendreq_kwargs["proxies"] = self.proxies

            self.client = TrendReq(**trendreq_kwargs)
            logger.info("✅ Google Trends API client initialized successfully")
            logger.info(
                f"🔧 Configuration: retries={self.retries}, backoff_factor={self.backoff_factor}"
            )
            if self.proxies:
                logger.info(f"🌐 Using {len(self.proxies)} proxy servers")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Google Trends client: {e}")
            self.client = None

    def _rate_limit_check(self):
        """Implement professional rate limiting per pytrends documentation."""
        current_time = time.time()

        # Enforce minimum interval between requests
        if self.last_request_time is not None:
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.min_request_interval:
                sleep_time = self.min_request_interval - time_since_last
                logger.debug(f"Rate limiting: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)

        # If we've hit rate limits recently, be more conservative
        if self.rate_limit_hits > 0:
            # Exponential backoff: longer sleep for each consecutive hit
            sleep_time = min(
                self.rate_limit_sleep * (2 ** (self.rate_limit_hits - 1)), 300
            )  # Max 5 minutes
            logger.warning(
                f"Rate limit protection: sleeping {sleep_time}s (hit #{self.rate_limit_hits})"
            )
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_count += 1

    def _handle_rate_limit_error(self, error):
        """Handle rate limit errors with exponential backoff."""
        self.rate_limit_hits += 1
        logger.warning(f"Rate limit hit #{self.rate_limit_hits}: {error}")
        logger.info(f"Rate limit status: {self.request_count} total requests")

        # Reset rate limit hits after successful recovery
        if self.rate_limit_hits > 5:
            logger.error("Too many consecutive rate limit hits, resetting client")
            self._initialize_client()
            self.rate_limit_hits = 0

    def execute_with_rate_limit(self, operation_func, *args, **kwargs):
        """
        Execute an operation with rate limiting and error handling.

        Args:
            operation_func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result of the operation or None on failure
        """
        if self.client is None:
            logger.error("Google Trends client not initialized")
            return None

        try:
            self._rate_limit_check()
            result = operation_func(*args, **kwargs)

            # Reset rate limit hits on success
            if self.rate_limit_hits > 0:
                logger.info("Rate limit recovery successful")
                self.rate_limit_hits = 0

            return result

        except Exception as e:
            error_str = str(e).lower()
            if "rate limit" in error_str or "429" in error_str or "too many requests" in error_str:
                self._handle_rate_limit_error(e)
            else:
                logger.error(f"Google Trends operation failed: {e}")
            return None

    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limiting status."""
        return {
            "request_count": self.request_count,
            "rate_limit_hits": self.rate_limit_hits,
            "last_request_time": self.last_request_time,
            "min_request_interval": self.min_request_interval,
            "rate_limit_sleep": self.rate_limit_sleep,
        }

    def reset_rate_limit_counter(self):
        """Reset rate limiting counters."""
        self.request_count = 0
        self.rate_limit_hits = 0
        self.last_request_time = None
        logger.info("Rate limit counters reset")

    def set_proxy_list(self, proxies: List[str]):
        """Update the proxy list and reinitialize client."""
        self.proxies = proxies
        self._initialize_client()

    def is_available(self) -> bool:
        """Check if the Google Trends client is available."""
        return self.client is not None

    def close(self):
        """Clean up client resources."""
        if self.client:
            # pytrends doesn't have a close method, but we can clean up
            self.client = None
            logger.info("Google Trends client closed")