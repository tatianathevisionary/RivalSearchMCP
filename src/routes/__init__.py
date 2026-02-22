#!/usr/bin/env python3
"""
Routes package for RivalSearchMCP.
"""

from .pagination import MCPPaginationManager, PaginatedResponse, PaginationCursor
from .routes import *  # noqa: F403
from .server import *  # noqa: F403

__all__ = [
    # Route handlers and server functionality
    # MCP Pagination Support
    "MCPPaginationManager",
    "PaginationCursor",
    "PaginatedResponse",
]
