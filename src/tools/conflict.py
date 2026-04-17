"""
Source-conflict detection MCP tool.

`find_conflicts` takes 2+ source URLs (fetched + extracted to text) or
pre-supplied snippets and returns a structured report of disagreements
-- numeric, date, and polarity conflicts -- with auditable
(source-quoted) context. Rule-based only, no LLM.

Use it whenever the caller notices two or more sources that seem to
make claims about the same referent. The tool never "smooths over"
disagreement; when conflicts exist, they are surfaced as a first-class
output the caller's model can cite directly.
"""

from typing import Annotated, Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP
from pydantic import Field
from scrapling.fetchers import AsyncFetcher

from src.core.conflict import find_conflicts as _find_conflicts
from src.core.content.extractors import UnifiedContentExtractor
from src.logging.logger import logger

_MAX_SOURCES = 10
_MAX_SNIPPET_CHARS = 8000


async def _fetch_snippet(url: str) -> str:
    """Fetch a URL and return clean extracted text (truncated).

    Routes through Scrapling for TLS-fingerprint resistance, falls back
    to plain httpx if Scrapling misbehaves on a given URL.
    """
    try:
        page = await AsyncFetcher.get(url, stealthy_headers=True, timeout=20)
        if page.status == 200 and page.body:
            extractor = UnifiedContentExtractor()
            return extractor.extract(page.text or page.body.decode("utf-8", "replace"))[
                :_MAX_SNIPPET_CHARS
            ]
    except Exception as e:
        logger.debug("find_conflicts Scrapling fetch failed for %s: %s", url, e)

    try:
        async with httpx.AsyncClient(
            timeout=20.0,
            follow_redirects=True,
            headers={"User-Agent": "rivalsearchmcp/1.0"},
        ) as client:
            r = await client.get(url)
            if r.status_code == 200:
                extractor = UnifiedContentExtractor()
                return extractor.extract(r.text)[:_MAX_SNIPPET_CHARS]
    except Exception as e:
        logger.warning("find_conflicts fallback fetch failed for %s: %s", url, e)

    return ""


def register_conflict_tools(mcp: FastMCP) -> None:
    """Register the find_conflicts tool."""

    @mcp.tool
    async def find_conflicts(
        sources: Annotated[
            List[str],
            Field(
                description=(
                    "List of sources to compare. Each entry is either a URL "
                    "(which will be fetched and extracted to text) or a "
                    "pre-extracted text snippet. A minimum of 2 sources is "
                    "required for any comparison to happen."
                ),
                min_length=2,
                max_length=_MAX_SOURCES,
            ),
        ],
        claim: Annotated[
            Optional[str],
            Field(
                description=(
                    "Optional claim to check polarity on. If set, the tool "
                    "reports which sources support the claim and which "
                    "contradict it (e.g., 'the vaccine is safe'). When "
                    "omitted, only numeric and date conflicts are surfaced."
                ),
                default=None,
            ),
        ] = None,
    ) -> Dict[str, Any]:
        """
        Find numeric, date, and polarity disagreements across 2+ sources.

        Detection strategy (rule-based, deterministic):

          * Numeric: extract (value, unit) pairs and their ~50-char
            topic context; a pair where different values share ≥2
            topic tokens and are in the same unit family (currency,
            percent, storage, headcount, …) is reported as a numeric
            conflict. Confidence scales with topic overlap.

          * Date: extract absolute dates (ISO, Month-Day-Year, or bare
            year); pairs that share ≥2 topic tokens but differ on the
            year or full date are reported as date conflicts.

          * Polarity (only when `claim` is set): check each source for
            support / contradiction of the claim. Detects inserted
            negation ("X is safe" vs "X is not safe") via
            subject + copula + tail matching.

        Returns a structured report; no free-form narrative. The caller's
        LLM (or a human reader) should decide what to do with each
        conflict -- e.g., weight by source quality, prefer the more
        recent, call out the disagreement in a final answer.
        """
        logger.info("find_conflicts: %d source(s) claim=%r", len(sources), claim)

        snippets: List[Dict[str, Any]] = []
        for i, entry in enumerate(sources):
            if entry.startswith(("http://", "https://")):
                text = await _fetch_snippet(entry)
                snippets.append({"index": i, "input": entry, "text": text, "source_kind": "url"})
            else:
                snippets.append(
                    {
                        "index": i,
                        "input": f"(inline source {i})",
                        "text": entry[:_MAX_SNIPPET_CHARS],
                        "source_kind": "inline",
                    }
                )

        report = _find_conflicts([s["text"] for s in snippets], claim=claim)

        return {
            "status": "success",
            "claim": claim,
            "source_count": len(snippets),
            "sources": [
                {"index": s["index"], "input": s["input"], "kind": s["source_kind"]}
                for s in snippets
            ],
            "conflict_count": len(report.conflicts),
            "conflicts": [c.as_dict() for c in report.conflicts],
            "agreements": report.agreements,
        }
