"""
Research workflow execution engine.
Handles the main research workflow logic and orchestration.
"""

import asyncio
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastmcp import Context
from fastmcp.server.context import Context
from pydantic import Field
from typing_extensions import Annotated
from openrouter import OpenRouter

from src.core.trends import GoogleTrendsAPI
from src.logging.logger import logger
from src.utils.markdown_formatter import format_research_analysis_markdown
from .ai_model_selector import get_best_free_model_with_tools
from .research_synthesis import generate_research_synthesis


class ResearchWorkflowExecutor:
    """Executes comprehensive research workflows with AI assistance."""

    def __init__(self):
        self.trends_api = GoogleTrendsAPI()

    async def execute_research_workflow(
        self,
        topic: str,
        max_sources: int = 15,
        include_trends: bool = True,
        include_website_analysis: bool = True,
        research_depth: str = "comprehensive",
        ai_model: str = "meta-llama/llama-3.1-8b-instruct:free",
        enable_ai_insights: bool = True,
        ctx: Context = None,
    ) -> str:
        """
        Execute a comprehensive research workflow.

        Args:
            topic: Research topic
            max_sources: Maximum sources to analyze
            include_trends: Whether to include trends analysis
            include_website_analysis: Whether to include website analysis
            research_depth: Depth of research (basic, comprehensive, expert)
            ai_model: AI model for insights
            enable_ai_insights: Whether to generate AI insights
            ctx: FastMCP context

        Returns:
            Formatted research results
        """
        research_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Store research state
        if ctx:
            ctx.set_state("research_id", research_id)
            ctx.set_state("research_topic", topic)
            ctx.set_state("research_start_time", datetime.now().isoformat())
            ctx.set_state("ai_model", ai_model)
            ctx.set_state("ai_insights_enabled", enable_ai_insights)

        # Initialize AI client
        ai_client = None
        selected_model = None

        if enable_ai_insights:
            try:
                ai_client = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"))
                selected_model = get_best_free_model_with_tools()

                if ctx:
                    await ctx.info(f"🤖 AI research assistant initialized with {selected_model}")
                    await ctx.info("🔄 OpenRouter provider routing ensures automatic fallbacks and reliability")
            except Exception as e:
                logger.error(f"AI client initialization failed: {e}")
                if ctx:
                    await ctx.warning(f"⚠️ AI client initialization failed: {e}. Continuing without AI assistance.")
                ai_client = None
                enable_ai_insights = False

        if ctx:
            await ctx.info(f"🔬 Starting AI-enhanced research on: {topic}")
            await ctx.info(f"📊 Research ID: {research_id}")
            if enable_ai_insights:
                await ctx.info(f"🧠 AI Model: {ai_model}")
            await ctx.info(f"🎯 Target sources: {max_sources}")
            await ctx.report_progress(0.0)

        # Initialize research results structure
        research_results = self._initialize_research_results(
            research_id, topic, max_sources, include_trends,
            include_website_analysis, research_depth
        )

        try:
            # Execute research phases
            await self._execute_research_phases(
                research_results, topic, max_sources,
                include_trends, include_website_analysis, ctx
            )

            # Generate synthesis and AI insights
            await self._generate_synthesis_and_insights(
                research_results, research_depth,
                ai_client, selected_model, ctx
            )

            # Finalize results
            research_results["status"] = "success"
            research_results["completion_time"] = datetime.now().isoformat()

            logger.info(f"Research workflow completed: {topic} (ID: {research_id})")

            if ctx:
                await ctx.info(f"🎯 AI-enhanced research completed successfully! Research ID: {research_id}")
                await ctx.report_progress(1.0)

            return format_research_analysis_markdown(research_results, "Research")

        except Exception as e:
            error_msg = f"Research workflow failed for '{topic}': {str(e)}"
            if ctx:
                await ctx.error(f"❌ {error_msg}")

            logger.error(error_msg)
            return format_research_analysis_markdown(
                {
                    "topic": topic,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                },
                "Research",
            )

    def _initialize_research_results(
        self, research_id: str, topic: str, max_sources: int,
        include_trends: bool, include_website_analysis: bool, research_depth: str
    ) -> Dict[str, Any]:
        """Initialize the research results structure."""
        return {
            "research_id": research_id,
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "max_sources": max_sources,
                "include_trends": include_trends,
                "include_website_analysis": include_website_analysis,
                "research_depth": research_depth,
            },
            "phases": {},
            "synthesis": {},
            "metadata": {},
        }

    async def _execute_research_phases(
        self, research_results: Dict[str, Any], topic: str, max_sources: int,
        include_trends: bool, include_website_analysis: bool, ctx: Context = None
    ) -> None:
        """Execute the research phases: source discovery, trends, website analysis."""

        # Phase 1: Source Discovery
        if ctx:
            await ctx.info("🔄 Phase 1: Initial search and source discovery")
            await ctx.report_progress(0.1)

        await self._execute_source_discovery(research_results, topic, max_sources)

        if ctx:
            await ctx.report_progress(0.3)

        # Phase 2: Trends Analysis
        if include_trends:
            if ctx:
                await ctx.info("📈 Phase 2: Trends analysis")
                await ctx.report_progress(0.35)

            await self._execute_trends_analysis(research_results, topic)

            if ctx:
                await ctx.report_progress(0.6)
        else:
            if ctx:
                await ctx.info("⏭️ Phase 2 skipped: Trends analysis disabled")
                await ctx.report_progress(0.6)

            research_results["phases"]["trends_analysis"] = {
                "status": "skipped",
                "reason": "Trends analysis disabled by user",
            }

        # Phase 3: Website Analysis
        if include_website_analysis:
            if ctx:
                await ctx.info("🌐 Phase 3: Website analysis and content extraction")
                await ctx.report_progress(0.65)

            await self._execute_website_analysis(research_results, topic)

            if ctx:
                await ctx.report_progress(0.85)
        else:
            if ctx:
                await ctx.info("⏭️ Phase 3 skipped: Website analysis disabled")
                await ctx.report_progress(0.85)

            research_results["phases"]["website_analysis"] = {
                "status": "skipped",
                "reason": "Website analysis disabled by user",
            }

    async def _execute_source_discovery(
        self, research_results: Dict[str, Any], topic: str, max_sources: int
    ) -> None:
        """Execute source discovery phase."""
        try:
            # Use DuckDuckGo Search for initial discovery
            from src.core.search.engines.duckduckgo.duckduckgo_engine import DuckDuckGoSearchEngine

            duckduckgo_engine = DuckDuckGoSearchEngine()
            search_results = await duckduckgo_engine.search(
                query=topic,
                num_results=max_sources,
                extract_content=True,
                follow_links=False,
                max_depth=1,
            )

            if search_results:
                # Extract key information from search results
                sources = []
                for result in search_results:
                    source_info = {
                        "title": result.title,
                        "url": result.url,
                        "description": result.description,
                        "engine": result.engine,
                        "position": result.position,
                        "timestamp": result.timestamp,
                    }
                    sources.append(source_info)

                research_results["phases"]["source_discovery"] = {
                    "status": "success",
                    "sources_found": len(sources),
                    "sources": sources[:max_sources],
                    "search_method": "direct_duckduckgo",
                }
            else:
                research_results["phases"]["source_discovery"] = {
                    "status": "partial",
                    "sources_found": 0,
                    "error": "No search results found",
                }

        except Exception as e:
            research_results["phases"]["source_discovery"] = {
                "status": "error",
                "error": str(e),
            }

    async def _execute_trends_analysis(self, research_results: Dict[str, Any], topic: str) -> None:
        """Execute trends analysis phase."""
        try:
            # Call trends analysis
            trends_data = self.trends_api.search_trends(
                keywords=[topic], timeframe="today 12-m", geo="US"
            )

            if trends_data is not None and not trends_data.empty:
                research_results["phases"]["trends_analysis"] = {
                    "status": "success",
                    "data": trends_data,
                    "keywords_analyzed": [topic],
                    "timeframe": "today 12-m",
                    "geo": "US",
                }
            else:
                research_results["phases"]["trends_analysis"] = {
                    "status": "partial",
                    "data": trends_data,
                    "warning": "Trends analysis returned no data or empty DataFrame",
                }

        except Exception as e:
            research_results["phases"]["trends_analysis"] = {
                "status": "error",
                "error": str(e),
            }

    async def _execute_website_analysis(self, research_results: Dict[str, Any], topic: str) -> None:
        """Execute website analysis phase."""
        try:
            # Analyze top sources from search results
            website_analysis = []
            sources_to_analyze = research_results["phases"].get("source_discovery", {}).get("sources", [])[:5]

            for source in sources_to_analyze:
                try:
                    # Use website traversal for analysis
                    from src.core.traverse import traverse_website

                    traversal_result = await traverse_website(
                        url=source["url"], max_depth=2, max_pages=10
                    )

                    if traversal_result and isinstance(traversal_result, dict):
                        content_to_analyze = str(traversal_result)[:2000]

                        website_analysis.append({
                            "url": source["url"],
                            "engine": source.get("engine", "unknown"),
                            "traversal_result": traversal_result,
                            "content_analysis": {
                                "status": "completed",
                                "content_preview": content_to_analyze[:500],
                            },
                            "status": "success",
                        })
                    else:
                        website_analysis.append({
                            "url": source["url"],
                            "engine": source.get("engine", "unknown"),
                            "error": "No traversal data returned",
                            "status": "partial",
                        })

                except Exception as e:
                    website_analysis.append({
                        "url": source["url"],
                        "error": str(e),
                        "status": "error",
                    })

            research_results["phases"]["website_analysis"] = {
                "status": "success",
                "websites_analyzed": len(website_analysis),
                "analysis_results": website_analysis,
            }

        except Exception as e:
            research_results["phases"]["website_analysis"] = {
                "status": "error",
                "error": str(e),
            }

    async def _generate_synthesis_and_insights(
        self, research_results: Dict[str, Any], research_depth: str,
        ai_client: Optional[OpenRouter], selected_model: Optional[str], ctx: Context = None
    ) -> None:
        """Generate synthesis and AI insights."""
        if ctx:
            await ctx.info("🧠 Phase 4: Synthesizing findings and generating insights")
            await ctx.report_progress(0.9)

        try:
            # Generate synthesis
            synthesis = generate_research_synthesis(research_results, research_depth)
            research_results["synthesis"] = synthesis

            research_results["metadata"]["total_phases"] = 4
            research_results["metadata"]["successful_phases"] = sum(
                1 for phase in research_results["phases"].values()
                if phase.get("status") == "success"
            )
            research_results["metadata"]["research_depth"] = research_depth

            # Generate AI insights
            if ai_client and selected_model:
                await self._generate_ai_insights(
                    research_results, ai_client, selected_model, ctx
                )

            if ctx:
                await ctx.report_progress(1.0)

        except Exception as e:
            research_results["synthesis"] = {"status": "error", "error": str(e)}

    async def _generate_ai_insights(
        self, research_results: Dict[str, Any],
        ai_client: OpenRouter, selected_model: str, ctx: Context = None
    ) -> None:
        """Generate AI-powered insights using OpenRouter."""
        try:
            if ctx:
                await ctx.info("🤖 Generating AI-powered insights...")

            # Compile research summary for AI analysis
            phases = research_results.get("phases", {})
            synthesis = research_results.get("synthesis", {})

            sources_count = len(phases.get("source_discovery", {}).get("sources", []))
            trends_status = phases.get("trends_analysis", {}).get("status")
            website_status = phases.get("website_analysis", {}).get("status")

            research_summary = f"""
Research Topic: {research_results['topic']}

Key Findings:
- Sources Discovered: {sources_count}
- Trends Analysis: {"Completed" if trends_status == "success" else "Not Available"}
- Website Analysis: {"Completed" if website_status == "success" else "Not Available"}

Synthesis: {synthesis.get("summary", "No synthesis available")}
"""

            insight_prompt = f"""Based on this research summary, generate 3-5 strategic insights that would be valuable for stakeholders. Focus on:

1. **Key Patterns & Trends**: What important patterns emerge from the data?
2. **Strategic Implications**: What do these findings mean for decision-making?
3. **Actionable Recommendations**: What specific actions should be taken?
4. **Future Considerations**: What should be monitored or researched further?

Research Summary:
{research_summary}

Provide insights that are specific, evidence-based, and practically valuable."""

            # Generate AI insights
            response = await ai_client.chat.send_async(
                messages=[{"role": "user", "content": insight_prompt}],
                model=selected_model,
                temperature=0.7,
                max_tokens=800,
            )

            if response.choices and response.choices[0].message:
                ai_insights = response.choices[0].message.content
                research_results["ai_insights"] = ai_insights

                if ctx:
                    await ctx.info("✅ AI insights generated successfully")
            else:
                if ctx:
                    await ctx.warning("⚠️ Could not generate AI insights")

        except Exception as e:
            if ctx:
                await ctx.warning(f"⚠️ AI insights generation failed: {e}")