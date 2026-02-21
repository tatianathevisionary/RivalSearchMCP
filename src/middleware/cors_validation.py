"""
CORS Origin validation middleware for MCP HTTP transport.

The MCP server must not reflect arbitrary Origin headers in
Access-Control-Allow-Origin responses. Doing so allows any website
to make cross-origin requests to the server, which is a security
misconfiguration.

This HTTP-level middleware intercepts requests before they reach
FastMCP/Starlette's default CORS handling and enforces a strict
allowlist of trusted origins.
"""

import logging
import os
from typing import Callable, FrozenSet

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger("cors_validation")

# Default allowed origins - configurable via ALLOWED_ORIGINS env var (comma-separated)
_DEFAULT_ALLOWED_ORIGINS: FrozenSet[str] = frozenset(
    {
        "https://rivalsearchmcp.fastmcp.app",
        "https://RivalSearchMCP.fastmcp.app",
        "https://rivalsearchmcp.com",
        "https://www.rivalsearchmcp.com",
    }
)


def _get_allowed_origins() -> FrozenSet[str]:
    """Load allowed origins from environment or use defaults."""
    env_origins = os.getenv("ALLOWED_ORIGINS", "")
    if env_origins.strip():
        custom = frozenset(o.strip() for o in env_origins.split(",") if o.strip())
        return _DEFAULT_ALLOWED_ORIGINS | custom
    return _DEFAULT_ALLOWED_ORIGINS


class CORSOriginValidationMiddleware(BaseHTTPMiddleware):
    """
    Validates the Origin header on incoming requests and sets
    Access-Control-Allow-Origin only for trusted origins.

    Rejects preflight (OPTIONS) and actual requests from untrusted
    origins with a 403 Forbidden response instead of reflecting the
    Origin header back.
    """

    def __init__(self, app, allowed_origins: FrozenSet[str] | None = None):
        super().__init__(app)
        self.allowed_origins = allowed_origins or _get_allowed_origins()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        origin = request.headers.get("origin")

        # No Origin header → not a cross-origin request, pass through
        if not origin:
            return await call_next(request)

        # Check if origin is allowed
        if origin not in self.allowed_origins:
            logger.warning(
                "Blocked request from untrusted origin: %s (method=%s path=%s)",
                origin,
                request.method,
                request.url.path,
            )
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Forbidden",
                    "detail": "Origin not allowed",
                },
            )

        # Allowed origin → handle preflight or pass through with CORS headers
        if request.method == "OPTIONS":
            return Response(
                status_code=204,
                headers={
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": (
                        "Content-Type, Mcp-Protocol-Version, Mcp-Session-Id"
                    ),
                    "Access-Control-Max-Age": "86400",
                },
            )

        # Actual request from allowed origin
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        return response
