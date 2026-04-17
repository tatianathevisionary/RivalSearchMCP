"""
Research memory.

Persistent, append-only workspaces keyed by a caller-supplied
`session_id`. Each workspace accumulates findings (URLs with
quality scores + notes) across tool calls and across MCP sessions,
letting iterative research carry context forward instead of
starting from zero every time (issue #9).

Storage is pluggable via py-key-value-aio. Default backend is an
in-memory store; set `RESEARCH_MEMORY_DIR` to any writable path to
persist workspaces to disk (FileTreeStore). For multi-server cloud
deployments, swap in a Redis / DynamoDB store via the same protocol.
"""

from .sessions import (
    ResearchSession,
    get_store,
    research_session_add,
    research_session_delete,
    research_session_get,
    research_session_list,
    research_session_start,
)

__all__ = [
    "ResearchSession",
    "get_store",
    "research_session_add",
    "research_session_delete",
    "research_session_get",
    "research_session_list",
    "research_session_start",
]
