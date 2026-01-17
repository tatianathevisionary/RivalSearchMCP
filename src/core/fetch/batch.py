#!/usr/bin/env python3
"""
Batch retrieval functionality for RivalSearchMCP.
Handles concurrent fetching of multiple URLs.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List

from src.logging.logger import logger

from .base import base_fetch_url


async def batch_rival_retrieve(
    urls: List[str], max_concurrent: int = 10
) -> List[Dict[str, Any]]:
    """
    Batch retrieve content from multiple URLs with concurrency control.

    Args:
        urls: List of URLs to fetch
        max_concurrent: Maximum number of concurrent requests

    Returns:
        List of dictionaries with URL data and content
    """
    from asyncio import Semaphore

    logger.info(f"Starting batch retrieval for {len(urls)} URLs")

    semaphore = Semaphore(max_concurrent)
    tasks = []

    async def fetch_single(url: str) -> Dict[str, Any]:
        async with semaphore:
            try:
                content = await base_fetch_url(url)
                return {
                    "url": url,
                    "content": content,
                    "success": content is not None,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                logger.error(f"Error fetching {url}: {e}")
                return {
                    "url": url,
                    "content": None,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }

    for url in urls:
        tasks.append(fetch_single(url))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions and return successful results
    valid_results = []
    for result in results:
        if isinstance(result, dict):
            valid_results.append(result)
        elif isinstance(result, Exception):
            logger.error(f"Task failed with exception: {result}")

    logger.info(f"Completed batch retrieval: {len(valid_results)} successful, {len(urls) - len(valid_results)} failed")
    return valid_results
