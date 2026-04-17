"""
Bluesky search via the AT Protocol public endpoint.

Uses api.bsky.app/xrpc/app.bsky.feed.searchPosts which does real
full-text search over public posts, requires no authentication, and
returns posts with author, text, engagement counts, and timestamps.

Note: `public.api.bsky.app` (the historically-documented host) now
returns 403 for this method; `api.bsky.app` is the working endpoint
as of late 2025.
"""

from typing import Any, Dict, List, Optional

import httpx

from src.logging.logger import logger

_API_BASE = "https://api.bsky.app/xrpc"


class BlueskySearch:
    """Search Bluesky public posts via the AT Protocol."""

    def __init__(self):
        self.api_url = _API_BASE
        self.headers = {
            "User-Agent": (
                "rivalsearchmcp/1.0 (+https://github.com/damionrashford/RivalSearchMCP)"
            ),
            "Accept": "application/json",
        }

    async def search(
        self,
        query: str,
        limit: int = 10,
        sort: str = "top",
        lang: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search Bluesky posts.

        Args:
            query: Search query
            limit: Max results (1..100)
            sort: "top" or "latest"
            lang: Optional ISO 639-1 language filter (e.g., "en")
        """
        params: Dict[str, Any] = {
            "q": query,
            "limit": max(1, min(limit, 100)),
            "sort": sort,
        }
        if lang:
            params["lang"] = lang

        try:
            async with httpx.AsyncClient(
                headers=self.headers, timeout=30.0, follow_redirects=True
            ) as client:
                response = await client.get(
                    f"{self.api_url}/app.bsky.feed.searchPosts", params=params
                )
                if response.status_code != 200:
                    logger.warning(
                        "Bluesky returned %s for %r (body: %s)",
                        response.status_code,
                        query,
                        response.text[:200],
                    )
                    return []

                data = response.json()
                posts = data.get("posts", [])
                results: List[Dict[str, Any]] = []
                for p in posts:
                    author = p.get("author") or {}
                    record = p.get("record") or {}
                    # Convert AT URI (at://did/collection/rkey) to a bsky.app URL.
                    uri = p.get("uri", "")
                    bsky_url = ""
                    if uri.startswith("at://"):
                        parts = uri[len("at://") :].split("/")
                        if len(parts) >= 3:
                            did = parts[0]
                            rkey = parts[2]
                            handle = author.get("handle") or did
                            bsky_url = f"https://bsky.app/profile/{handle}/post/{rkey}"
                    results.append(
                        {
                            "text": record.get("text", ""),
                            "url": bsky_url,
                            "author_handle": author.get("handle", ""),
                            "author_display_name": author.get("displayName", ""),
                            "created_at": record.get("createdAt", ""),
                            "like_count": p.get("likeCount", 0),
                            "repost_count": p.get("repostCount", 0),
                            "reply_count": p.get("replyCount", 0),
                            "uri": uri,
                            "source": "bluesky",
                        }
                    )

                logger.info("Found %d Bluesky posts for %r", len(results), query)
                return results

        except httpx.HTTPError as e:
            logger.warning("Bluesky search failed (network): %s", e)
            return []
        except Exception:
            logger.exception("Bluesky search failed (unexpected)")
            return []
