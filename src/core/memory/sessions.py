"""
Append-only research workspaces backed by a py-key-value-aio store.

Design:

  A "research session" is a named workspace identified by a UUID. It
  owns a list of `findings` (URL + quality + inline metadata) and a
  list of `notes` (free text the caller wants to remember). Each add
  is append-only: nothing is ever silently overwritten, which is the
  right default for research continuity where a stale fact is data,
  not noise.

  Storage is pluggable. The default store is MemoryStore (single-
  process, non-persistent). Setting the env var
  RESEARCH_MEMORY_DIR=<path> switches to FileTreeStore (disk-backed,
  survives restarts on single-server FastMCP deployments). For
  distributed deployments, wire in RedisStore / DynamoDBStore the
  same way and pass it as `override_store`.

  All entries carry an `index` that's monotonically increasing per
  session so callers can query "show me findings added after index N"
  to implement pagination / streaming updates cheaply.
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from key_value.aio.protocols.key_value import AsyncKeyValue
from key_value.aio.stores.memory import MemoryStore

from src.logging.logger import logger

_COLLECTION = "research_sessions"
_INDEX_COLLECTION = "research_sessions_index"


@dataclass
class ResearchSession:
    """One research workspace. Persisted as a single dict per session_id."""

    session_id: str
    topic: str
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    findings: List[Dict[str, Any]] = field(default_factory=list)
    notes: List[Dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "topic": self.topic,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "findings": self.findings,
            "notes": self.notes,
            "finding_count": len(self.findings),
            "note_count": len(self.notes),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResearchSession":
        return cls(
            session_id=d["session_id"],
            topic=d.get("topic", ""),
            tags=list(d.get("tags") or []),
            created_at=d.get("created_at", ""),
            updated_at=d.get("updated_at", ""),
            findings=list(d.get("findings") or []),
            notes=list(d.get("notes") or []),
        )


# ---------------------------------------------------------------------------
# Store lifecycle
# ---------------------------------------------------------------------------

_store_singleton: Optional[AsyncKeyValue] = None


def get_store() -> AsyncKeyValue:
    """Return the process-wide research memory store.

    Resolved once per process from RESEARCH_MEMORY_DIR. Pass an
    explicit backend via `set_store()` for tests or alternative
    backends (Redis, DynamoDB, ...).
    """
    global _store_singleton
    if _store_singleton is not None:
        return _store_singleton

    memdir = os.getenv("RESEARCH_MEMORY_DIR", "").strip()
    if memdir:
        try:
            from pathlib import Path

            # FileTreeStore pulls in `aiofile`; import lazily so the
            # default MemoryStore path doesn't require it.
            from key_value.aio.stores.filetree import (
                FileTreeStore,
                FileTreeV1CollectionSanitizationStrategy,
                FileTreeV1KeySanitizationStrategy,
            )

            path = Path(memdir).expanduser().resolve()
            path.mkdir(parents=True, exist_ok=True)
            _store_singleton = FileTreeStore(
                data_directory=path,
                key_sanitization_strategy=FileTreeV1KeySanitizationStrategy(path),
                collection_sanitization_strategy=FileTreeV1CollectionSanitizationStrategy(path),
            )
            logger.info("research memory: using FileTreeStore at %s", path)
        except ImportError as e:
            logger.warning(
                "research memory: RESEARCH_MEMORY_DIR set but FileTreeStore "
                "unavailable (%s); falling back to in-memory store. Install "
                "`aiofile` to enable disk persistence.",
                e,
            )
            _store_singleton = MemoryStore()
    else:
        _store_singleton = MemoryStore()
        logger.info("research memory: using MemoryStore (set RESEARCH_MEMORY_DIR for persistence)")
    return _store_singleton


def set_store(store: AsyncKeyValue) -> None:
    """Override the process-wide store. Primarily for tests."""
    global _store_singleton
    _store_singleton = store


# ---------------------------------------------------------------------------
# Session operations
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


async def _load(store: AsyncKeyValue, session_id: str) -> Optional[ResearchSession]:
    raw = await store.get(collection=_COLLECTION, key=session_id)
    if not raw:
        return None
    return ResearchSession.from_dict(raw)


async def _save(store: AsyncKeyValue, session: ResearchSession) -> None:
    session.updated_at = _now_iso()
    await store.put(collection=_COLLECTION, key=session.session_id, value=session.as_dict())


async def _index_add(store: AsyncKeyValue, session_id: str, topic: str, tags: List[str]) -> None:
    """Maintain a light-weight index for listing."""
    idx = await store.get(collection=_INDEX_COLLECTION, key="_all") or {"ids": {}}
    idx.setdefault("ids", {})
    idx["ids"][session_id] = {
        "topic": topic,
        "tags": tags,
        "updated_at": _now_iso(),
    }
    await store.put(collection=_INDEX_COLLECTION, key="_all", value=idx)


async def _index_touch(store: AsyncKeyValue, session_id: str) -> None:
    idx = await store.get(collection=_INDEX_COLLECTION, key="_all") or {"ids": {}}
    if session_id in idx.get("ids", {}):
        idx["ids"][session_id]["updated_at"] = _now_iso()
        await store.put(collection=_INDEX_COLLECTION, key="_all", value=idx)


async def _index_remove(store: AsyncKeyValue, session_id: str) -> None:
    idx = await store.get(collection=_INDEX_COLLECTION, key="_all") or {"ids": {}}
    if session_id in idx.get("ids", {}):
        idx["ids"].pop(session_id)
        await store.put(collection=_INDEX_COLLECTION, key="_all", value=idx)


async def research_session_start(
    topic: str,
    tags: Optional[List[str]] = None,
    *,
    store: Optional[AsyncKeyValue] = None,
) -> ResearchSession:
    """Create a new workspace and return its ResearchSession."""
    s = store or get_store()
    session = ResearchSession(
        session_id=str(uuid.uuid4()),
        topic=topic.strip(),
        tags=[t.strip() for t in (tags or []) if t and t.strip()],
        created_at=_now_iso(),
        updated_at=_now_iso(),
    )
    await _save(s, session)
    await _index_add(s, session.session_id, session.topic, session.tags)
    logger.info("research memory: started session %s (topic=%r)", session.session_id, topic)
    return session


async def research_session_get(
    session_id: str,
    *,
    store: Optional[AsyncKeyValue] = None,
) -> Optional[ResearchSession]:
    """Load a session by id, or None if no such session."""
    s = store or get_store()
    return await _load(s, session_id)


async def research_session_list(
    *,
    tag: Optional[str] = None,
    store: Optional[AsyncKeyValue] = None,
) -> List[Dict[str, Any]]:
    """Return a list of {session_id, topic, tags, updated_at} entries,
    optionally filtered to sessions that carry `tag`."""
    s = store or get_store()
    idx = await s.get(collection=_INDEX_COLLECTION, key="_all") or {"ids": {}}
    out: List[Dict[str, Any]] = []
    for sid, meta in idx.get("ids", {}).items():
        if tag and tag not in (meta.get("tags") or []):
            continue
        out.append(
            {
                "session_id": sid,
                "topic": meta.get("topic", ""),
                "tags": meta.get("tags") or [],
                "updated_at": meta.get("updated_at", ""),
            }
        )
    out.sort(key=lambda r: r.get("updated_at", ""), reverse=True)
    return out


async def research_session_add(
    session_id: str,
    *,
    findings: Optional[List[Dict[str, Any]]] = None,
    note: Optional[str] = None,
    store: Optional[AsyncKeyValue] = None,
) -> Optional[ResearchSession]:
    """Append findings and/or a free-text note.

    `findings` entries are deduped against what's already in the
    session by URL (same URL twice is silently collapsed). Each added
    entry gets a monotonically-increasing `index` field plus an
    `added_at` timestamp.

    Returns the updated session, or None if `session_id` doesn't exist.
    """
    s = store or get_store()
    session = await _load(s, session_id)
    if session is None:
        return None

    existing_urls = {f.get("url") for f in session.findings if f.get("url")}
    next_index = max((f.get("index", -1) for f in session.findings), default=-1) + 1

    if findings:
        for f in findings:
            url = f.get("url")
            if url and url in existing_urls:
                continue
            entry = dict(f)
            entry["index"] = next_index
            entry["added_at"] = _now_iso()
            session.findings.append(entry)
            if url:
                existing_urls.add(url)
            next_index += 1

    if note:
        note_index = max((n.get("index", -1) for n in session.notes), default=-1) + 1
        session.notes.append({"index": note_index, "text": note, "added_at": _now_iso()})

    await _save(s, session)
    await _index_touch(s, session_id)
    return session


async def research_session_delete(
    session_id: str,
    *,
    store: Optional[AsyncKeyValue] = None,
) -> bool:
    """Delete a session; returns True if one was actually removed."""
    s = store or get_store()
    session = await _load(s, session_id)
    if session is None:
        return False
    await s.delete(collection=_COLLECTION, key=session_id)
    await _index_remove(s, session_id)
    logger.info("research memory: deleted session %s", session_id)
    return True
