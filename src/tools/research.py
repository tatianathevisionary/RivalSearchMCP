"""
Research tools registration for FastMCP server.
Provides AI-enhanced research workflow tools.
"""

from typing import Literal
from fastmcp import FastMCP, Context
from pydantic import Field
from typing_extensions import Annotated

from src.logging.logger import logger
from .research_modules.research_workflow import ResearchWorkflowExecutor


def register_research_tools(mcp: FastMCP):
    """Register comprehensive research tools."""

    executor = ResearchWorkflowExecutor()

    @mcp.tool(
        name="research_agent",
        description="AI research agent using OpenRouter with autonomous tool calling capabilities",
        tags={"research", "workflow", "ai", "openrouter", "tool_calling"},
        meta={
            "version": "3.0",
            "category": "Research",
            "ai_enhanced": True,
            "tool_calling": True,
            "performance": "high",
            "workflow": True,
            "multi_tool": True,
        },
        annotations={
            "title": "AI Research Workflow",
            "readOnlyHint": True,
            "openWorldHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
        },
    )
    async def research_agent(
        ctx: Context,
        topic: Annotated[
            str,
            Field(
                description="Research topic to investigate",
                min_length=3,
                max_length=500,
            ),
        ],
        max_sources: Annotated[
            int,
            Field(
                description="Maximum number of sources to analyze",
                ge=5,
                le=50,
                default=15,
            ),
        ] = 15,
        include_trends: Annotated[
            bool, Field(description="Whether to include trends analysis")
        ] = True,
        include_website_analysis: Annotated[
            bool, Field(description="Whether to include website traversal and analysis")
        ] = True,
        research_depth: Annotated[
            Literal["basic", "comprehensive", "expert"],
            Field(description="Depth of research to perform"),
        ] = "comprehensive",
        ai_model: Annotated[
            str,
            Field(
                description="Primary OpenRouter AI model (automatic fallbacks to 4+ free models with tool calling)",
                default="meta-llama/llama-3.1-8b-instruct:free",
            ),
        ] = "meta-llama/llama-3.1-8b-instruct:free",
        enable_ai_insights: Annotated[
            bool,
            Field(
                description="Whether to generate AI-powered insights and recommendations"
            ),
        ] = True,
    ) -> str:
        """
        AI-enhanced research workflow using OpenRouter with multi-model fallbacks and tool calling.

        This tool combines human expertise with AI assistance to perform comprehensive research:
        - AI-powered query generation and research planning using multiple fallback models
        - Automated tool calling to gather data from multiple sources
        - AI analysis and synthesis of research findings with provider optimization
        - Intelligent insights and recommendations generation
        - Progress tracking with AI-guided workflow optimization

        Features robust AI integration:
        - Automatic fallback to 4+ free models with tool calling support
        - Performance optimization prioritizing throughput and low latency
        - Privacy-focused routing (data_collection: deny)
        - Tool calling capabilities for intelligent research orchestration

        Uses OpenRouter's best available free model with tool calling support,
        leveraging OpenRouter's automatic provider routing and fallbacks for reliability.

        Returns structured research findings with AI-generated insights and metadata.
        """
        return await executor.execute_research_workflow(
            topic=topic,
            max_sources=max_sources,
            include_trends=include_trends,
            include_website_analysis=include_website_analysis,
            research_depth=research_depth,
            ai_model=ai_model,
            enable_ai_insights=enable_ai_insights,
            ctx=ctx,
        )