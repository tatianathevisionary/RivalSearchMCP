"""
Research-memory MCP tools (issue #9).

Five tools that let a caller carry context across tool calls and
across MCP sessions:

  research_session_start    Create a new workspace; returns session_id.
  research_session_add      Append findings (url + metadata) and/or a note.
  research_session_get      Read the full current state.
  research_session_list     Enumerate workspaces, optionally by tag.
  research_session_delete   Remove a workspace.

All backed by src.core.memory, whose default in-memory store keeps
sessions alive for the process's lifetime. Set
RESEARCH_MEMORY_DIR=<path> to switch to disk-backed FileTreeStore so
workspaces survive restarts.
"""

from typing import Annotated, Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import Field

from src.core.memory import research_session_add as _add
from src.core.memory import research_session_delete as _delete
from src.core.memory import research_session_get as _get
from src.core.memory import research_session_list as _list
from src.core.memory import research_session_start as _start


def register_memory_tools(mcp: FastMCP) -> None:
    """Register the five research-memory tools."""

    @mcp.tool
    async def research_session_start(
        topic: Annotated[
            str,
            Field(
                description=(
                    "Human-readable subject of this research workspace "
                    "(e.g. 'OpenAI funding history', 'postgres vs mysql "
                    "for OLAP at 10TB')."
                ),
                min_length=2,
                max_length=300,
            ),
        ],
        tags: Annotated[
            Optional[List[str]],
            Field(
                description=(
                    "Optional tags for grouping and filtering with "
                    "research_session_list (e.g. ['vendor-eval', 'q2-2026'])."
                ),
                default=None,
            ),
        ] = None,
    ) -> Dict[str, Any]:
        """
        Create a new research workspace and return its handle.

        The returned `session_id` is the key every subsequent
        research_session_* call takes. Pass it back to
        research_session_add to accumulate findings; the same id works
        across tool calls AND across MCP session reconnects, so
        iterative research carries context forward.
        """
        s = await _start(topic=topic, tags=tags)
        return {"status": "success", **s.as_dict()}

    @mcp.tool
    async def research_session_add(
        session_id: Annotated[
            str,
            Field(description="Session UUID from research_session_start"),
        ],
        findings: Annotated[
            Optional[List[Dict[str, Any]]],
            Field(
                description=(
                    "List of findings to append. Each item is an arbitrary "
                    "dict; typical keys are `url`, `title`, `quality` (from "
                    "score_sources), `source`, `published`. URLs already "
                    "present in the session are silently deduped."
                ),
                default=None,
            ),
        ] = None,
        note: Annotated[
            Optional[str],
            Field(
                description=(
                    "Optional free-text note to append alongside the "
                    "findings. Useful for hypotheses, follow-up items, or "
                    "the caller's own synthesis so far."
                ),
                default=None,
                max_length=4000,
            ),
        ] = None,
    ) -> Dict[str, Any]:
        """
        Append findings and/or a note to an existing workspace.

        Append-only by design: findings are never overwritten, and
        duplicate URLs are silently collapsed rather than creating a
        second entry. Each appended finding gets a monotonic `index`
        and an `added_at` timestamp.
        """
        updated = await _add(session_id, findings=findings, note=note)
        if updated is None:
            return {
                "status": "error",
                "error": f"No research session with id {session_id!r}",
            }
        return {"status": "success", **updated.as_dict()}

    @mcp.tool
    async def research_session_get(
        session_id: Annotated[
            str,
            Field(description="Session UUID from research_session_start"),
        ],
    ) -> Dict[str, Any]:
        """
        Return the full state of a research workspace: topic, tags,
        created/updated timestamps, every finding, and every note.

        The exact dict returned here is what will be persisted across
        restarts when RESEARCH_MEMORY_DIR is configured -- nothing is
        ever dropped or summarised.
        """
        s = await _get(session_id)
        if s is None:
            return {
                "status": "error",
                "error": f"No research session with id {session_id!r}",
            }
        return {"status": "success", **s.as_dict()}

    @mcp.tool
    async def research_session_list(
        tag: Annotated[
            Optional[str],
            Field(
                description="Return only sessions that carry this tag",
                default=None,
            ),
        ] = None,
    ) -> Dict[str, Any]:
        """
        Enumerate research workspaces (most-recently-updated first).

        Returns a light summary per session (id, topic, tags, updated_at)
        -- call research_session_get to pull the full findings.
        """
        entries = await _list(tag=tag)
        return {"status": "success", "count": len(entries), "sessions": entries}

    @mcp.tool
    async def research_session_delete(
        session_id: Annotated[
            str,
            Field(description="Session UUID to delete"),
        ],
    ) -> Dict[str, Any]:
        """
        Remove a research workspace permanently.

        Irreversible. Intended for clearing ephemeral sessions or
        retiring completed ones.
        """
        removed = await _delete(session_id)
        return {
            "status": "success" if removed else "not_found",
            "deleted": removed,
            "session_id": session_id,
        }
