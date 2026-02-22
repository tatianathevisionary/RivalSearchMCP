"""
Research synthesis and analysis utilities.
Handles generating insights and summaries from research data.
"""

from typing import Any, Dict


def generate_research_synthesis(
    research_results: Dict[str, Any], research_depth: str
) -> Dict[str, Any]:
    """Generate research synthesis based on depth and findings."""

    synthesis = {
        "status": "success",
        "depth": research_depth,
        "summary": "",
        "key_findings": [],
        "insights": [],
        "recommendations": [],
        "next_steps": [],
    }

    # Extract key information from research phases
    sources = research_results["phases"].get("source_discovery", {}).get("sources", [])
    trends = research_results["phases"].get("trends_analysis", {})
    websites = research_results["phases"].get("website_analysis", {})

    # Generate summary based on depth
    if research_depth == "basic":
        synthesis["summary"] = (
            f"Basic research on '{research_results['topic']}' completed with {len(sources)} sources."
        )
        synthesis["key_findings"] = [
            f"Found {len(sources)} relevant sources" if sources else "Limited source availability"
        ]

    elif research_depth == "comprehensive":
        synthesis["summary"] = (
            f"Comprehensive research on '{research_results['topic']}' completed with {len(sources)} sources, trends analysis, and website exploration."
        )
        synthesis["key_findings"] = [
            f"Discovered {len(sources)} relevant sources",
            f"Trends analysis: {'Completed' if trends.get('status') == 'success' else 'Not available'}",
            f"Website analysis: {'Completed' if websites.get('status') == 'success' else 'Not available'}",
        ]

    elif research_depth == "expert":
        synthesis["summary"] = (
            f"Expert-level research on '{research_results['topic']}' completed with comprehensive analysis across all dimensions."
        )
        synthesis["key_findings"] = [
            f"Comprehensive source discovery: {len(sources)} sources",
            f"Advanced trends analysis: {'Completed' if trends.get('status') == 'success' else 'Not available'}",
            f"Deep website analysis: {'Completed' if websites.get('status') == 'success' else 'Not available'}",
            "Multi-dimensional insights generated",
        ]

    # Generate insights based on available data
    if sources:
        synthesis["insights"].append(f"Primary sources identified: {len(sources)}")
        if any(s.get("has_rich_snippet") for s in sources):
            synthesis["insights"].append("Rich snippets detected in search results")
        if any(s.get("estimated_traffic") == "high" for s in sources):
            synthesis["insights"].append("High-traffic sources identified")

    if trends.get("status") == "success":
        synthesis["insights"].append("Trends data available for temporal analysis")

    if websites.get("status") == "success":
        synthesis["insights"].append(
            f"Website analysis completed for {websites.get('websites_analyzed', 0)} sites"
        )

    # Generate recommendations
    synthesis["recommendations"] = [
        "Review and validate key sources",
        "Consider trends analysis for temporal insights",
        "Explore website content for deeper understanding",
        "Cross-reference findings across multiple sources",
    ]

    # Generate next steps
    synthesis["next_steps"] = [
        "Validate key findings with additional sources",
        "Perform deeper analysis on high-priority sources",
        "Consider expanding research scope if needed",
        "Document findings and insights for future reference",
    ]

    return synthesis
