"""
Reddit search implementation using public JSON API.
No authentication required.
"""

from typing import Any, Dict, List

import httpx

from src.logging.logger import logger


class RedditSearch:
    """Search Reddit without authentication using public JSON API."""

    def __init__(self):
        self.base_url = "https://www.reddit.com"
        # Reddit's API guidelines explicitly ask for an identifying UA of the
        # form <platform>:<app-id>:<version> (by u/<user>). Generic browser UAs
        # are aggressively rate-limited or blocked on cloud IPs.
        # Do NOT set an Accept header: Cloudflare in front of Reddit
        # returns 403 when Accept is explicitly set from a non-browser
        # client, even when the UA is valid. Leaving it unset (default
        # */*) avoids the fingerprint check while still letting Reddit
        # serve JSON from the .json endpoint.
        self.headers = {
            "User-Agent": "python:com.rivalsearchmcp:1.0.0 (by u/rivalsearchmcp)",
        }

    async def search(
        self,
        query: str,
        subreddit: str = "all",
        sort: str = "relevance",
        time_filter: str = "all",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search Reddit posts.

        Args:
            query: Search query
            subreddit: Subreddit to search (default: "all")
            sort: Sort by (relevance, hot, top, new)
            time_filter: Time filter (all, day, week, month, year)
            limit: Maximum results

        Returns:
            List of Reddit post dictionaries
        """
        params = {
            "q": query,
            "sort": sort,
            "t": time_filter,
            "limit": limit,
            "restrict_sr": "on" if subreddit != "all" else "off",
        }

        # Try www.reddit.com first; fall back to old.reddit.com which is
        # typically more lenient about unauthenticated traffic from cloud IPs.
        endpoints = [
            f"{self.base_url}/r/{subreddit}/search.json",
            f"https://old.reddit.com/r/{subreddit}/search.json",
        ]

        async with httpx.AsyncClient(
            headers=self.headers, timeout=30.0, follow_redirects=True
        ) as client:
            for url in endpoints:
                try:
                    response = await client.get(url, params=params)
                    if response.status_code != 200:
                        logger.warning(
                            "Reddit search %s returned %s for %r (body: %s)",
                            url,
                            response.status_code,
                            query,
                            response.text[:200],
                        )
                        continue
                    data = response.json()
                    posts = self._parse_posts(data)
                    logger.info("Found %d Reddit posts for %r via %s", len(posts), query, url)
                    return posts
                except httpx.HTTPError as e:
                    logger.warning("Reddit search %s failed: %s", url, e)
                    continue
                except ValueError as e:
                    logger.warning(
                        "Reddit search %s returned non-JSON: %s (body: %s)",
                        url,
                        e,
                        response.text[:200],
                    )
                    continue

        logger.error("All Reddit endpoints failed for query %r", query)
        return []

    def _parse_posts(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract posts from Reddit's listing response."""
        posts = []
        for post_data in data.get("data", {}).get("children", []):
            post = post_data.get("data", {})
            posts.append(
                {
                    "title": post.get("title", ""),
                    "subreddit": post.get("subreddit", ""),
                    "author": post.get("author", ""),
                    "score": post.get("score", 0),
                    "url": f"{self.base_url}{post.get('permalink', '')}",
                    "num_comments": post.get("num_comments", 0),
                    "created_utc": post.get("created_utc", 0),
                    "selftext": post.get("selftext", "")[:500],
                    "source": "reddit",
                }
            )
        return posts
