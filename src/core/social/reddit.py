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
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
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
        try:
            # Use Reddit's public JSON API
            url = f"{self.base_url}/r/{subreddit}/search.json"
            params = {
                "q": query,
                "sort": sort,
                "t": time_filter,
                "limit": limit,
                "restrict_sr": "on" if subreddit != "all" else "off",
            }

            async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()

                data = response.json()
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
                            "selftext": post.get("selftext", "")[:500],  # First 500 chars
                            "source": "reddit",
                        }
                    )

                logger.info(f"Found {len(posts)} Reddit posts for: {query}")
                return posts

        except Exception as e:
            logger.error(f"Reddit search failed: {e}")
            return []
