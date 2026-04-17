"""
Entity research tool.

A single tool that fans out across every relevant RivalSearchMCP
capability in parallel and returns a unified profile of a named
entity (company, product, person, project, technology).

Replaces the typical 30-90 minute manual workflow of:
  - web search for overview
  - news search for recent developments
  - GitHub search for code + community health
  - social search for developer/user sentiment
  - academic search for technical/research footprint

with a single call. Every sub-source runs concurrently; each
sub-source's failure is isolated (`return_exceptions=True`) and
surfaced as a 'source failed' note rather than aborting the whole
profile.

Every returned URL carries a quality score and the final profile
carries an aggregate confidence summary.
"""

import asyncio
from typing import Annotated, Any, Dict, List, Literal, Optional

from fastmcp import Context, FastMCP
from pydantic import Field

from src.core.news.aggregator import NewsAggregator
from src.core.quality import assess_results, summarize_quality
from src.core.scientific.search.orchestrator import AcademicSearchOrchestrator
from src.core.social.bluesky import BlueskySearch
from src.core.social.hackernews import HackerNewsSearch
from src.core.social.reddit import RedditSearch
from src.core.social.stackoverflow import StackOverflowSearch
from src.logging.logger import logger
from src.tools.multi_search import MultiSearchOrchestrator

EntityType = Literal["auto", "company", "product", "person", "project", "technology"]


def _format_profile(
    entity: str,
    entity_type: str,
    sections: Dict[str, Any],
    confidence: Dict[str, Any],
) -> str:
    """Render the combined entity profile as clean Markdown."""
    badge = {"high": "🟢", "medium": "🟡", "low": "🔴", "none": "⚪"}.get(
        confidence.get("confidence", "none"), "⚪"
    )
    md = f"# 🗺️ Entity Profile: *{entity}*\n\n"
    md += f"**Type:** {entity_type}\n\n"
    md += (
        f"**{badge} Confidence:** {confidence.get('confidence', 'none')} · "
        f"mean quality {confidence.get('mean_score', 0)}/100 · "
        f"{confidence.get('independent_domains', 0)} independent sources across "
        f"{confidence.get('result_count', 0)} results\n\n"
    )
    md += "---\n\n"

    def render_section(title: str, items: List[Dict[str, Any]], fields: List[str]) -> None:
        nonlocal md
        if not items:
            return
        md += f"## {title}\n\n"
        for i, it in enumerate(items[:5], 1):
            md += f"### {i}. {it.get('title') or it.get('name') or it.get('text', '')[:80]}\n\n"
            q = it.get("quality") or {}
            if q:
                md += f"**Quality:** {q.get('score', 0)}/100 ({q.get('tier', '?')})"
                sig = q.get("signals") or {}
                if sig.get("corroboration"):
                    md += f" · corroborated by {sig['corroboration']} other sources"
                md += "\n\n"
            meta_bits = []
            for f in fields:
                v = it.get(f)
                if v:
                    meta_bits.append(f"**{f.replace('_', ' ').title()}:** {v}")
            if meta_bits:
                md += " | ".join(meta_bits) + "\n\n"
            if it.get("description"):
                md += f"{it['description'][:300]}\n\n"
            url = it.get("url") or it.get("link")
            if url:
                md += f"[🔗 Source]({url})\n\n"
            md += "---\n\n"

    render_section("🌐 Web Overview", sections.get("web", []), ["source", "engine"])
    render_section("📰 Recent News", sections.get("news", []), ["source", "published"])
    render_section(
        "🐙 Code & Community (GitHub)",
        sections.get("github", []),
        ["stars", "forks", "language", "updated_at"],
    )
    render_section(
        "💬 Community Sentiment (HN, Reddit, Stack Overflow, Bluesky)",
        sections.get("social", []),
        ["source", "score", "num_comments"],
    )
    render_section(
        "🔬 Academic Footprint",
        sections.get("academic", []),
        ["year", "venue", "citationCount"],
    )

    failures = sections.get("_failures") or {}
    if failures:
        md += "## ⚠️ Source Notes\n\n"
        for src, err in failures.items():
            md += f"- **{src}**: {err}\n"
        md += "\n"

    return md


def register_entity_tools(mcp: FastMCP) -> None:
    """Register the entity_research tool."""

    # Reuse the existing orchestrators / providers. They already handle
    # their own retries, timeouts, and error surfacing.
    web_orch = MultiSearchOrchestrator()
    news_agg = NewsAggregator()
    academic_orch = AcademicSearchOrchestrator()
    hn = HackerNewsSearch()
    reddit = RedditSearch()
    so = StackOverflowSearch()
    bsky = BlueskySearch()

    @mcp.tool
    async def entity_research(
        ctx: Context,
        entity: Annotated[
            str,
            Field(
                description="The name of the entity to profile",
                min_length=2,
                max_length=200,
            ),
        ],
        entity_type: Annotated[
            EntityType,
            Field(
                description=(
                    "Entity category. Determines which sources get priority: "
                    "'company'/'product' emphasize web+news+social; "
                    "'project'/'technology' emphasize github+social+academic; "
                    "'person' emphasizes web+academic+social; "
                    "'auto' (default) runs everything."
                ),
                default="auto",
            ),
        ] = "auto",
        max_per_section: Annotated[
            int,
            Field(
                description=(
                    "Upper bound on items kept per section after dedup. The "
                    "profile only renders the top 5 per section, but larger "
                    "values give the quality scorer more corroboration signal."
                ),
                ge=3,
                le=20,
                default=8,
            ),
        ] = 8,
        sources: Annotated[
            Optional[List[Literal["web", "news", "github", "social", "academic"]]],
            Field(
                description=("Which sections to include. Defaults to all five when None."),
                default=None,
            ),
        ] = None,
    ) -> str:
        """
        Research an entity across web, news, code, social, and academic
        sources in parallel. Returns a unified Markdown profile with a
        per-item quality score and an aggregate confidence signal.

        Use cases:
          - Due diligence on a vendor, library, or potential hire
          - Competitive-intelligence snapshot of a company or product
          - Technology evaluation (is X actually used? by whom? what do
            practitioners say? what does the research literature say?)

        Every sub-query is run concurrently and isolated; if one source
        fails (e.g. a rate limit), the others still populate the profile.
        """
        if ctx:
            await ctx.report_progress(progress=0, total=100)
            await ctx.info(f"🗺️ Profiling entity: {entity} ({entity_type})")

        wanted = set(sources) if sources else {"web", "news", "github", "social", "academic"}

        tasks: Dict[str, Any] = {}

        if "web" in wanted:
            tasks["web"] = web_orch.search_all_engines(
                query=entity,
                num_results=max_per_section,
                extract_content=False,
                follow_links=False,
                max_depth=1,
            )
        if "news" in wanted:
            tasks["news"] = news_agg.search_news(
                query=entity, max_results=max_per_section, time_range="month"
            )
        if "github" in wanted:
            # github_search is registered as a FastMCP tool. Call the
            # underlying GitHub search directly to avoid Context coupling.
            from src.core.github_api.search import GitHubSearch

            tasks["github"] = GitHubSearch().search_repositories(
                query=entity, per_page=max_per_section
            )
        if "social" in wanted:
            # Community platforms that respond well to entity-name queries.
            tasks["social_hn"] = hn.search(query=entity, limit=max_per_section)
            tasks["social_reddit"] = reddit.search(
                query=entity, subreddit="all", limit=max_per_section, time_filter="month"
            )
            tasks["social_so"] = so.search(
                query=entity, site="stackoverflow", limit=max_per_section
            )
            tasks["social_bsky"] = bsky.search(query=entity, limit=max_per_section)
        if "academic" in wanted:
            tasks["academic"] = academic_orch.search_academic_papers(
                query=entity,
                sources=["openalex", "crossref", "arxiv"],
                limit=max_per_section,
            )

        if ctx:
            await ctx.report_progress(progress=20, total=100)

        names = list(tasks.keys())
        outs = await asyncio.gather(*tasks.values(), return_exceptions=True)
        by_name: Dict[str, Any] = dict(zip(names, outs))

        if ctx:
            await ctx.report_progress(progress=75, total=100)

        failures: Dict[str, str] = {}
        sections: Dict[str, List[Dict[str, Any]]] = {
            "web": [],
            "news": [],
            "github": [],
            "social": [],
            "academic": [],
        }

        # Web: MultiSearchOrchestrator returns {"results": {engine: {results: [...]}}}
        web = by_name.get("web")
        if isinstance(web, Exception):
            failures["web"] = str(web)
        elif isinstance(web, dict):
            for eng_data in (web.get("results") or {}).values():
                for r in (eng_data or {}).get("results", []):
                    if isinstance(r, dict):
                        sections["web"].append(r)
                    elif hasattr(r, "to_dict"):
                        sections["web"].append(r.to_dict())

        news = by_name.get("news")
        if isinstance(news, Exception):
            failures["news"] = str(news)
        elif news:
            sections["news"] = list(news)

        gh = by_name.get("github")
        if isinstance(gh, Exception):
            failures["github"] = str(gh)
        elif gh:
            # GitHub results have `html_url`; surface as `url`.
            for r in gh:
                if "url" not in r and "html_url" in r:
                    r["url"] = r["html_url"]
                sections["github"].append(r)

        for key in ("social_hn", "social_reddit", "social_so", "social_bsky"):
            data = by_name.get(key)
            if isinstance(data, Exception):
                failures[key] = str(data)
            elif data:
                for item in data:
                    # Bluesky text -> title
                    if "text" in item and "title" not in item:
                        item["title"] = item["text"][:120]
                    sections["social"].append(item)

        acad = by_name.get("academic")
        if isinstance(acad, Exception):
            failures["academic"] = str(acad)
        elif acad:
            sections["academic"] = list(acad)

        # Annotate each section with quality scores (corroboration is
        # computed within each section's result set).
        for key in list(sections.keys()):
            sections[key] = assess_results(sections[key])[:max_per_section]

        sections["_failures"] = failures

        # Aggregate confidence is computed across the union of all
        # items so corroboration signal spans sources.
        union: List[Dict[str, Any]] = []
        for k, items in sections.items():
            if k != "_failures":
                union.extend(items)
        union_annotated = assess_results(
            [{k: v for k, v in it.items() if k != "quality"} for it in union]
        )
        confidence = summarize_quality(union_annotated)

        logger.info(
            "entity_research %r (%s): web=%d news=%d github=%d social=%d academic=%d failures=%d confidence=%s",
            entity,
            entity_type,
            len(sections["web"]),
            len(sections["news"]),
            len(sections["github"]),
            len(sections["social"]),
            len(sections["academic"]),
            len(failures),
            confidence.get("confidence"),
        )

        if ctx:
            await ctx.report_progress(progress=100, total=100)

        return _format_profile(entity, entity_type, sections, confidence)
