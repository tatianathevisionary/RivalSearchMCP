"""
Source-quality scoring tool for FastMCP.

Exposes `score_sources` so agents (and humans) can get a calibrated
trust signal for a list of URLs without having to reason about the
underlying heuristics themselves.
"""

from typing import Annotated, Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import Field

from src.core.quality import assess_results, summarize_quality
from src.logging.logger import logger


def register_quality_tools(mcp: FastMCP) -> None:
    """Register source-quality scoring tools."""

    @mcp.tool
    async def score_sources(
        urls: Annotated[
            List[str],
            Field(description="List of URLs to score", min_length=1, max_length=50),
        ],
        metadata: Annotated[
            Optional[List[Dict[str, Any]]],
            Field(
                description=(
                    "Optional per-URL metadata (title, published, citation count, "
                    "etc.) aligned index-wise with `urls`. Used to enrich the "
                    "freshness and corroboration signals."
                ),
                default=None,
            ),
        ] = None,
    ) -> Dict[str, Any]:
        """
        Rate a batch of URLs on four auditable signals:

        - domain_tier: primary / reference / academic / news / community /
          vendor / aggregator / unknown (hand-curated classification)
        - freshness: how recent, from provided publish dates
        - corroboration: how many *independent* other domains in the same
          batch corroborate this one (≥50% title-token overlap or shared DOI)
        - citations: citation count (academic) or score/upvotes (social)

        Returns per-URL `{score, tier, signals}` entries plus an aggregate
        `summary` with mean score, unique-domain count, tier distribution,
        and a coarse confidence level (high / medium / low).

        Use this before acting on search results in high-stakes workflows:
        a high-confidence result set (mean ≥ 65, ≥3 independent domains)
        is very different from a low-confidence one even if both look the
        same at a glance.
        """
        logger.info("score_sources: %d url(s)", len(urls))
        md = list(metadata or [])
        # Pad metadata to urls length so index alignment is tolerant.
        while len(md) < len(urls):
            md.append({})

        results = [{"url": u, **(m or {})} for u, m in zip(urls, md)]
        annotated = assess_results(results)
        summary = summarize_quality(annotated)

        return {
            "status": "success",
            "summary": summary,
            "scores": [
                {
                    "url": r["url"],
                    **r["quality"],
                }
                for r in annotated
            ],
        }
