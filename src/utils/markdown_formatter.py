"""
Utilities for formatting tool outputs as clean markdown.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


def format_academic_search_markdown(results: Dict[str, Any]) -> str:
    """Format academic search results as clean markdown."""
    if results.get("status") != "success":
        return f"❌ **Error:** {results.get('error', 'Unknown error occurred')}"

    query = results.get("query", "")
    papers = results.get("results", [])
    metadata = results.get("metadata", {})

    # Header
    output = f"# 🔬 Academic Search Results for: *{query}*\n\n"
    output += f"**Found {len(papers)} papers** from {', '.join(metadata.get('sources_searched', []))}\n\n"
    output += "---\n\n"

    # Papers
    for i, paper in enumerate(papers, 1):
        output += f"## {i}. {paper.get('title', 'Untitled')}\n\n"

        # Authors
        authors = paper.get("authors", [])
        if authors:
            if len(authors) <= 3:
                author_str = ", ".join(authors)
            else:
                author_str = ", ".join(authors[:3]) + " et al."
            output += f"**Authors:** {author_str}\n\n"

        # Basic info
        info_parts = []
        if paper.get("year"):
            info_parts.append(f"**Year:** {paper.get('year')}")
        if paper.get("venue"):
            info_parts.append(f"**Venue:** {paper.get('venue')}")
        if paper.get("citation_count"):
            info_parts.append(f"**Citations:** {paper.get('citation_count')}")

        if info_parts:
            output += " | ".join(info_parts) + "\n\n"

        # Abstract (truncated if too long)
        abstract = paper.get("abstract", "")
        if abstract:
            if len(abstract) > 500:
                abstract = abstract[:500] + "..."
            output += f"**Abstract:** {abstract}\n\n"

        # Links
        links = []
        if paper.get("url"):
            links.append(f"[📄 Paper]({paper.get('url')})")
        if paper.get("pdf_url"):
            links.append(f"[📕 PDF]({paper.get('pdf_url')})")

        if links:
            output += " | ".join(links) + "\n\n"

        # Citations if available
        citations = paper.get("citations", {})
        if citations:
            output += "**Citations:**\n\n"
            if citations.get("bibtex"):
                output += f"```\n{citations['bibtex']}\n```\n\n"
            if citations.get("apa"):
                output += f"*{citations['apa']}*\n\n"

        output += "---\n\n"

    # Footer
    output += f"*Search completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"

    return output.strip()


def format_dataset_discovery_markdown(results: Dict[str, Any]) -> str:
    """Format dataset discovery results as clean markdown."""
    if results.get("status") != "success":
        return f"❌ **Error:** {results.get('error', 'Unknown error occurred')}"

    query = results.get("query", "")
    datasets = results.get("datasets", [])
    metadata = results.get("metadata", {})

    # Header
    output = f"# 📊 Dataset Discovery Results for: *{query}*\n\n"
    output += f"**Found {len(datasets)} datasets** from {', '.join(metadata.get('sources_searched', []))}\n\n"
    output += "---\n\n"

    # Datasets
    for i, dataset in enumerate(datasets, 1):
        output += f"## {i}. {dataset.get('title', 'Untitled Dataset')}\n\n"

        # Owner/Source
        owner = dataset.get("owner", "")
        source = dataset.get("source", "")
        if owner:
            output += f"**Owner:** {owner} ({source})\n\n"

        # Description
        description = dataset.get("description", "")
        if description:
            if len(description) > 300:
                description = description[:300] + "..."
            output += f"**Description:** {description}\n\n"

        # Basic info
        info_parts = []
        if dataset.get("file_formats"):
            formats = [fmt for fmt in dataset.get("file_formats", []) if fmt]
            if formats:
                info_parts.append(f"**Formats:** {', '.join(formats[:3])}")
        if dataset.get("size"):
            info_parts.append(f"**Size:** {dataset.get('size')}")
        if dataset.get("license"):
            info_parts.append(f"**License:** {dataset.get('license')}")

        if info_parts:
            output += " | ".join(info_parts) + "\n\n"

        # Stats
        stats_parts = []
        if dataset.get("download_count") is not None:
            stats_parts.append(f"📥 {dataset.get('download_count')} downloads")
        if dataset.get("upvote_count") is not None:
            stats_parts.append(f"👍 {dataset.get('upvote_count')} upvotes")

        if stats_parts:
            output += " | ".join(stats_parts) + "\n\n"

        # Links
        links = []
        if dataset.get("url"):
            links.append(f"[🔗 View Dataset]({dataset.get('url')})")
        if dataset.get("download_url"):
            links.append(f"[⬇️ Download]({dataset.get('download_url')})")

        if links:
            output += " | ".join(links) + "\n\n"

        # Tags
        tags = dataset.get("tags", [])
        if tags:
            tag_str = " ".join(f"`{tag}`" for tag in tags[:5])
            output += f"**Tags:** {tag_str}\n\n"

        # Metadata if available
        dataset_metadata = dataset.get("metadata", {})
        if dataset_metadata and dataset_metadata.get("columns"):
            columns = dataset_metadata.get("columns", [])
            if columns:
                output += f"**Columns:** {', '.join(columns[:10])}{'...' if len(columns) > 10 else ''}\n\n"

        output += "---\n\n"

    # Footer
    output += f"*Search completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"

    return output.strip()


def format_multi_search_markdown(results: Dict[str, Any]) -> str:
    """Format multi-search results as clean markdown."""
    # Check for error status
    if results.get("status") == "error" or "error" in results:
        return f"❌ **Error:** {results.get('error', 'Unknown error occurred')}"

    query = results.get("query", results.get("summary", {}).get("query", ""))
    results_data = results.get("results", {})

    # Header
    output = f"# 🔍 Search Results for: *{query}*\n\n"

    total_results = 0
    successful_engines = 0
    for engine, engine_data in results_data.items():
        if engine_data.get("status") == "success":
            count = engine_data.get("count", 0)
            total_results += count
            successful_engines += 1
            output += f"**{engine.title()}:** {count} results\n"

    output += (
        f"\n**Total Results:** {total_results} from {successful_engines} engines\n\n"
    )
    output += "---\n\n"

    # Results by engine
    for engine, engine_data in results_data.items():
        if engine_data.get("status") == "success" and engine_data.get("results"):
            output += f"## {engine.title()} Results\n\n"

            for i, result in enumerate(engine_data["results"], 1):
                title = result.get("title", "Untitled")
                url = result.get("url", "")
                description = result.get("description", "")

                output += f"### {i}. {title}\n\n"

                if description:
                    # Truncate description if too long
                    if len(description) > 200:
                        description = description[:200] + "..."
                    output += f"{description}\n\n"

                if url:
                    output += f"[🔗 Visit Page]({url})\n\n"

                output += "---\n\n"

    # Footer
    output += f"*Search completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"

    return output.strip()


def format_research_analysis_markdown(
    results: Dict[str, Any], tool_name: str = "Research"
) -> str:
    """Format research/analysis results as clean markdown."""
    if results.get("status") != "success":
        return f"❌ **Error:** {results.get('error', 'Unknown error occurred')}"

    topic = results.get("topic", "")
    output = f"# 📋 {tool_name} Analysis: *{topic}*\n\n"

    # Summary
    summary = results.get("summary", "")
    if summary:
        output += f"## Summary\n\n{summary}\n\n"

    # Key findings
    findings = results.get("key_findings", [])
    if findings:
        output += "## Key Findings\n\n"
        for i, finding in enumerate(findings, 1):
            output += f"{i}. {finding}\n"
        output += "\n"

    # Sources
    sources = results.get("sources", [])
    if sources:
        output += "## Sources\n\n"
        for i, source in enumerate(sources, 1):
            title = source.get("title", "Untitled")
            url = source.get("url", "")
            if url:
                output += f"{i}. [{title}]({url})\n"
            else:
                output += f"{i}. {title}\n"
        output += "\n"

    # AI Insights (special handling)
    ai_insights = results.get("ai_insights")
    if ai_insights:
        output += "## 🤖 AI Insights\n\n"
        output += f"{ai_insights}\n\n"

    # Additional sections
    for section_name, section_data in results.items():
        if section_name not in [
            "status",
            "topic",
            "summary",
            "key_findings",
            "sources",
            "timestamp",
            "ai_insights",  # Already handled above
        ]:
            if isinstance(section_data, list) and section_data:
                output += f"## {section_name.replace('_', ' ').title()}\n\n"
                for item in section_data:
                    output += f"- {item}\n"
                output += "\n"
            elif isinstance(section_data, str) and section_data:
                output += (
                    f"## {section_name.replace('_', ' ').title()}\n\n{section_data}\n\n"
                )

    # Footer
    output += f"*Analysis completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"

    return output.strip()
