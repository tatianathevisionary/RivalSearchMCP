"""
Simplified cache manager interface.
Provides unified access to different caching backends.
"""

from typing import Any, Optional
from .cache_manager import get_cache_manager


class CacheManager:
    """Simplified cache manager interface."""

    def __init__(self):
        self._manager = get_cache_manager()

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        return await self._manager.get(key)

    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Set a value in cache."""
        return await self._manager.set(key, value, ttl_seconds)

    async def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        return await self._manager.delete(key)

    async def clear(self) -> bool:
        """Clear all cached values."""
        return await self._manager.clear()

    async def get_stats(self) -> dict:
        """Get cache statistics."""
        return await self._manager.get_stats()