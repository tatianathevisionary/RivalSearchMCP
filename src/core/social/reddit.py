"""
Reddit search implementation using public JSON API.
No authentication required.

Falls back to Scrapling-based HTML parsing when the JSON API is
blocked (common from cloud IPs where Reddit's Cloudflare frontend
rejects bare httpx TLS fingerprints).
"""

import asyncio
import re
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

        Tries the JSON API first (fastest, structured data). If that fails
        (403/429/empty from Cloudflare), falls back to Scrapling-based HTML
        parsing which spoofs a real browser TLS fingerprint.

        Args:
            query: Search query
            subreddit: Subreddit to search (default: "all")
            sort: Sort by (relevance, hot, top, new)
            time_filter: Time filter (all, day, week, month, year)
            limit: Maximum results

        Returns:
            List of Reddit post dictionaries
        """
        # --- Attempt 1: JSON API via httpx (fast path) ---
        posts = await self._search_json(query, subreddit, sort, time_filter, limit)
        if posts:
            return posts

        # --- Attempt 2: Retry JSON API after brief delay (transient blocks) ---
        logger.info("Reddit JSON API returned empty; retrying after 2s delay")
        await asyncio.sleep(2)
        posts = await self._search_json(query, subreddit, sort, time_filter, limit)
        if posts:
            return posts

        # --- Attempt 3: Scrapling HTML fallback (bypasses TLS fingerprinting) ---
        logger.info("Reddit JSON API failed twice; falling back to Scrapling HTML parser")
        posts = await self._search_html_fallback(query, subreddit, sort, time_filter, limit)
        if posts:
            return posts

        logger.error("All Reddit search methods failed for query %r", query)
        return []

    async def _search_json(
        self,
        query: str,
        subreddit: str,
        sort: str,
        time_filter: str,
        limit: int,
    ) -> List[Dict[str, Any]]:
        """Try the Reddit JSON API via httpx."""
        params = {
            "q": query,
            "sort": sort,
            "t": time_filter,
            "limit": limit,
            "restrict_sr": "on" if subreddit != "all" else "off",
        }

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
                            "Reddit JSON %s returned HTTP %s for %r",
                            url,
                            response.status_code,
                            query,
                        )
                        continue
                    data = response.json()
                    posts = self._parse_json_posts(data)
                    if posts:
                        logger.info(
                            "Found %d Reddit posts for %r via JSON API (%s)",
                            len(posts),
                            query,
                            url,
                        )
                        return posts
                except httpx.HTTPError as e:
                    logger.warning("Reddit JSON %s HTTP error: %s", url, e)
                    continue
                except ValueError as e:
                    logger.warning("Reddit JSON %s non-JSON response: %s", url, e)
                    continue
        return []

    async def _search_html_fallback(
        self,
        query: str,
        subreddit: str,
        sort: str,
        time_filter: str,
        limit: int,
    ) -> List[Dict[str, Any]]:
        """
        Fallback: fetch Reddit search results as HTML via Scrapling.

        Scrapling's AsyncFetcher uses tls_client with a real browser
        fingerprint, bypassing Cloudflare's TLS-based bot detection
        that blocks plain httpx from cloud IPs.
        """
        try:
            from scrapling.fetchers import AsyncFetcher
        except ImportError:
            logger.warning("Scrapling not available for Reddit HTML fallback")
            return []

        url = f"{self.base_url}/r/{subreddit}/search"
        params = {
            "q": query,
            "sort": sort,
            "t": time_filter,
            "restrict_sr": "on" if subreddit != "all" else "off",
        }

        try:
            page = await AsyncFetcher.get(
                url,
                params=params,
                stealthy_headers=True,
                timeout=30,
            )
        except Exception as e:
            logger.error("Reddit Scrapling fallback fetch failed: %s", e)
            return []

        if page.status != 200:
            logger.warning(
                "Reddit Scrapling fallback returned HTTP %s for %r",
                page.status,
                query,
            )
            return []

        return self._parse_html_results(page, limit)

    def _parse_json_posts(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract posts from Reddit's JSON listing response."""
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

    def _parse_html_results(self, page: Any, limit: int) -> List[Dict[str, Any]]:
        """Parse Reddit search results from HTML response."""
        posts: List[Dict[str, Any]] = []

        # Reddit's search HTML uses different structures depending on
        # whether the new or old design is served. Try multiple selectors.
        # New Reddit: search-post elements or divs with data-testid
        # Old Reddit: div.search-result with a.search-title
        selectors = [
            "a[data-testid='post-title']",  # New Reddit
            "a.search-title",  # Old Reddit
            "div.search-result a.search-link",  # Old Reddit variant
            "faceplate-tracker[source='search'] a",  # Shreddit components
        ]

        links = []
        for sel in selectors:
            try:
                links = page.css(sel)
                if links:
                    break
            except Exception:
                continue

        if not links:
            # Last resort: find all links that look like Reddit post URLs
            try:
                all_links = page.css("a[href]")
                post_pattern = re.compile(r"/r/\w+/comments/\w+/")
                for link in all_links:
                    href = link.attrib.get("href", "")
                    if post_pattern.search(href):
                        links.append(link)
            except Exception:
                pass

        seen_urls: set = set()
        for link in links[:limit * 2]:
            try:
                title = link.get_all_text() or ""
                title = title.strip()
                if not title or len(title) < 5:
                    continue

                href = link.attrib.get("href", "")
                if not href:
                    continue
                if href.startswith("/"):
                    href = f"{self.base_url}{href}"
                if href in seen_urls:
                    continue
                seen_urls.add(href)

                # Try to extract subreddit from URL
                sub_match = re.search(r"/r/(\w+)/", href)
                subreddit_name = sub_match.group(1) if sub_match else ""

                posts.append(
                    {
                        "title": title[:300],
                        "subreddit": subreddit_name,
                        "author": "",
                        "score": 0,
                        "url": href,
                        "num_comments": 0,
                        "created_utc": 0,
                        "selftext": "",
                        "source": "reddit",
                    }
                )

                if len(posts) >= limit:
                    break
            except Exception:
                continue

        logger.info(
            "Reddit Scrapling HTML fallback found %d posts for query", len(posts)
        )
        return posts
