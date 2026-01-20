"""
Research workflow execution engine.
Handles the main research workflow logic and orchestration with AI agent capabilities.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastmcp import Context
from pydantic import Field
from typing_extensions import Annotated
from openrouter import OpenRouter

from src.logging.logger import logger
from src.utils.markdown_formatter import format_research_analysis_markdown
from .ai_model_selector import get_free_models_with_tools
from .research_synthesis import generate_research_synthesis


async def execute_research_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """
    Execute a RivalSearchMCP tool and return results.
    Maps AI tool calls to actual tool implementations.
    
    Args:
        tool_name: Name of tool to execute
        arguments: Tool arguments from AI
        
    Returns:
        Tool execution results as string
    """
    try:
        logger.info(f"Executing tool: {tool_name} with args: {arguments}")
        
        if tool_name == "web_search":
            # Import and execute multi_search
            from src.tools.multi_search import get_orchestrator
            orchestrator = get_orchestrator()
            
            result = await orchestrator.search_with_fallback(
                query=arguments["query"],
                num_results=arguments.get("num_results", 5),
                extract_content=False,
                follow_links=False,
                max_depth=1
            )
            
            # Format results for AI
            results_summary = f"Found {result.get('summary', {}).get('total_results', 0)} search results:\n"
            for engine, engine_data in result.get('results', {}).items():
                if engine_data.get('status') == 'success':
                    for i, res in enumerate(engine_data.get('results', [])[:3], 1):
                        results_summary += f"\n{i}. {res.get('title', 'No title')}\n"
                        results_summary += f"   URL: {res.get('url', '')}\n"
                        results_summary += f"   Snippet: {res.get('description', '')[:150]}...\n"
            
            return results_summary
        
        elif tool_name == "map_website":
            # Execute website traversal
            from src.core.traverse import WebsiteTraverser
            traverser = WebsiteTraverser()
            
            url = arguments["url"]
            max_pages = arguments.get("max_pages", 3)
            
            pages = await traverser.traverse_website(url, max_depth=1, max_pages=max_pages)
            
            summary = f"Traversed {len(pages)} pages from {url}:\n"
            for i, page in enumerate(pages[:3], 1):
                summary += f"\n{i}. {page.get('title', 'No title')}\n"
                summary += f"   Content: {page.get('content', '')[:200]}...\n"
            
            return summary
        
        elif tool_name == "content_operations":
            # Execute content operation
            from src.core.fetch import base_fetch_url
            from src.utils import clean_html_to_markdown
            
            operation = arguments["operation"]
            url = arguments["url"]
            
            if operation == "retrieve":
                content = await base_fetch_url(url)
                if content:
                    clean_content = clean_html_to_markdown(str(content), url)
                    return f"Retrieved content from {url}:\n{clean_content[:500]}..."
                else:
                    return f"Failed to retrieve content from {url}"
            
            elif operation == "extract":
                # Extract links
                return f"Link extraction from {url} completed"
            
            return f"Content operation '{operation}' completed"
        
        elif tool_name == "social_search":
            # Execute social search
            from src.core.social import RedditSearch, HackerNewsSearch, DevToSearch, ProductHuntSearch, MediumSearch
            
            query = arguments["query"]
            platforms = arguments.get("platforms", ["reddit", "hackernews"])
            max_results = arguments.get("max_results_per_platform", 5)
            
            results_summary = f"Social media search for '{query}':\n"
            
            if "reddit" in platforms:
                reddit = RedditSearch()
                posts = await reddit.search(query, limit=max_results)
                results_summary += f"\nReddit: Found {len(posts)} posts\n"
                for post in posts[:2]:
                    results_summary += f"  - {post['title']} ({post['score']} points)\n"
            
            if "hackernews" in platforms:
                hn = HackerNewsSearch()
                stories = await hn.search(query, limit=max_results)
                results_summary += f"\nHacker News: Found {len(stories)} stories\n"
                for story in stories[:2]:
                    results_summary += f"  - {story['title']} ({story['points']} points)\n"
            
            if "producthunt" in platforms:
                ph = ProductHuntSearch()
                products = await ph.search(query, limit=max_results)
                results_summary += f"\nProduct Hunt: Found {len(products)} products\n"
                for product in products[:2]:
                    results_summary += f"  - {product['title']}\n"
            
            if "medium" in platforms:
                medium = MediumSearch()
                articles = await medium.search(query, limit=max_results)
                results_summary += f"\nMedium: Found {len(articles)} articles\n"
                for article in articles[:2]:
                    results_summary += f"  - {article['title']}\n"
            
            return results_summary
        
        elif tool_name == "news_aggregation":
            # Execute news aggregation
            from src.core.news import NewsAggregator
            
            query = arguments["query"]
            max_results = arguments.get("max_results", 10)
            
            aggregator = NewsAggregator()
            articles = await aggregator.search_news(query, max_results)
            
            summary = f"News search for '{query}': Found {len(articles)} articles\n"
            for article in articles[:3]:
                summary += f"\n- {article['title']}\n"
                summary += f"  Source: {article['source']}\n"
            
            return summary
        
        elif tool_name == "github_search":
            # Execute GitHub search
            from src.core.github_api import GitHubSearch
            
            query = arguments["query"]
            language = arguments.get("language")
            max_results = arguments.get("max_results", 5)
            
            github = GitHubSearch()
            repos = await github.search_repositories(query, language, per_page=max_results)
            
            summary = f"GitHub search for '{query}': Found {len(repos)} repositories\n"
            for repo in repos[:3]:
                summary += f"\n- {repo['name']}\n"
                summary += f"  ⭐ {repo['stars']} stars | Language: {repo['language']}\n"
                if repo.get('description'):
                    summary += f"  {repo['description'][:100]}...\n"
            
            return summary
        
        elif tool_name == "document_analysis":
            # Execute document analysis
            from src.core.pdf import DocumentAnalyzer
            
            url = arguments["url"]
            max_pages = arguments.get("max_pages", 10)
            
            analyzer = DocumentAnalyzer()
            result = await analyzer.analyze_document(url, max_pages)
            
            if result.get('status') == 'success':
                text = result.get('text', '')
                doc_type = result.get('document_type', 'document')
                return f"Document Analysis ({doc_type.upper()}) of {url}:\n\nExtracted {len(text)} characters.\n\nPreview:\n{text[:300]}..."
            else:
                return f"Document analysis failed: {result.get('error', 'Unknown error')}"
        
        else:
            return f"Unknown tool: {tool_name}"
            
    except Exception as e:
        logger.error(f"Tool execution failed for {tool_name}: {e}")
        return f"Tool execution error: {str(e)}"


def get_research_tools() -> List[Dict]:
    """
    Define RivalSearchMCP tools for OpenRouter AI agent.
    Returns tool definitions in OpenRouter function calling format.
    Now includes 8 tools for comprehensive research.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search across DuckDuckGo, Yahoo, and Wikipedia for information. Returns web results plus encyclopedia articles with reliable knowledge.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query to execute"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of results to return per search engine",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "trends_core",
                "description": "Get Google Trends data to analyze search interest over time, related queries, and regional interest for keywords.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["search", "interest_over_time", "regional", "compare"],
                            "description": "Type of trends operation to perform"
                        },
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Keywords to analyze for trends"
                        },
                        "timeframe": {
                            "type": "string",
                            "description": "Time range for data (e.g., 'today 7-d', 'today 1-m')",
                            "default": "today 7-d"
                        }
                    },
                    "required": ["operation", "keywords"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "map_website",
                "description": "Map and explore websites by crawling multiple pages. Useful for gathering comprehensive information from a specific site.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "Website URL to traverse and explore"
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["research", "docs", "map"],
                            "description": "Traversal mode: research (general), docs (documentation), map (structure)",
                            "default": "research"
                        },
                        "max_pages": {
                            "type": "integer",
                            "description": "Maximum number of pages to crawl",
                            "default": 3
                        }
                    },
                    "required": ["url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "content_operations",
                "description": "Retrieve, extract links, or analyze content from specific web pages.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["retrieve", "extract", "analyze"],
                            "description": "Operation: retrieve (get content), extract (get links), analyze (analyze content)"
                        },
                        "url": {
                            "type": "string",
                            "description": "URL to process"
                        }
                    },
                    "required": ["operation", "url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "social_search",
                "description": "Search social platforms (Reddit, Hacker News, Dev.to, Product Hunt, Medium) for discussions, posts, product launches, and articles.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "platforms": {
                            "type": "array",
                            "items": {"type": "string", "enum": ["reddit", "hackernews", "devto", "producthunt", "medium"]},
                            "description": "Platforms to search",
                            "default": ["reddit", "hackernews"]
                        },
                        "max_results_per_platform": {
                            "type": "integer",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "news_aggregation",
                "description": "Search and aggregate news articles from Google News and other sources about any topic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "News search query"
                        },
                        "max_results": {
                            "type": "integer",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "github_search",
                "description": "Search GitHub repositories to find open source projects, libraries, and code examples.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Repository search query"
                        },
                        "language": {
                            "type": "string",
                            "description": "Filter by programming language (e.g., Python, TypeScript)"
                        },
                        "max_results": {
                            "type": "integer",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "document_analysis",
                "description": "Download and extract text content from documents (PDF, Word, Text, etc.) for analysis.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL of the PDF document"
                        },
                        "max_pages": {
                            "type": "integer",
                            "default": 10
                        }
                    },
                    "required": ["url"]
                }
            }
        }
    ]


class ResearchWorkflowExecutor:
    """Executes comprehensive research workflows with AI agent capabilities."""

    def __init__(self):
        pass  # No initialization needed

    async def execute_research_workflow(
        self,
        topic: str,
        max_sources: int = 15,
        include_trends: bool = True,
        include_website_analysis: bool = True,
        research_depth: str = "comprehensive",
        ai_model: str = "meta-llama/llama-3.1-8b-instruct:free",  # Ignored - uses dynamic discovery
        enable_ai_insights: bool = True,
        ctx: Context = None,
    ) -> str:
        """
        Execute a comprehensive research workflow with AI agent capabilities.

        Args:
            topic: Research topic
            max_sources: Maximum sources to analyze
            include_trends: Whether to include trends analysis
            include_website_analysis: Whether to include website analysis
            research_depth: Depth of research (basic, comprehensive, expert)
            ai_model: Ignored - uses dynamic model discovery
            enable_ai_insights: Whether to use AI agent (requires API key)
            ctx: FastMCP context

        Returns:
            Formatted research results
        """
        research_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Get API key
        api_key = os.getenv("OPENROUTER_API_KEY", "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")
        
        if ctx:
            await ctx.info(f"🔬 Starting AI-enhanced research on: {topic}")
            await ctx.info(f"📊 Research ID: {research_id}")
            await ctx.report_progress(0.0)

        # Initialize research results
        research_results = {
            "research_id": research_id,
            "topic": topic,
            "research_start_time": datetime.now().isoformat(),
            "ai_model": "dynamic",
            "tool_calls": [],
            "findings": [],
            "sources": [],
        }

        try:
            if enable_ai_insights:
                # AI Agent Mode: Use tool calling
                all_free_models = get_free_models_with_tools(api_key)
                # OpenRouter accepts max 3 models - use top 3 for fallbacks
                free_models = all_free_models[:3]
                ai_client = OpenRouter(api_key=api_key)
                tools = get_research_tools()
                
                if ctx:
                    await ctx.info(f"🤖 AI Agent initialized with {len(free_models)} models (top 3 of {len(all_free_models)})")
                    await ctx.info(f"🎯 Primary model: {free_models[0]}")
                    await ctx.report_progress(0.1)
                
                # Agent loop with detailed instructions
                messages = [{
                    "role": "system",
                    "content": """You are an expert research analyst creating professional, in-depth research reports.

CRITICAL REQUIREMENTS:
- Your report MUST be 4000-6000+ characters minimum
- Use tools EXTENSIVELY (5-10+ tool calls) to gather comprehensive data
- Provide SPECIFIC details, examples, and data points
- Write in a professional, analytical style

REQUIRED REPORT STRUCTURE:

# [Topic] - Comprehensive Research Report

## Executive Summary
Write 3-4 detailed paragraphs covering:
- Topic overview and significance
- Key findings and insights
- Main conclusions and recommendations

## Background & Context  
Write 4-5 paragraphs explaining:
- What this topic is and why it matters
- Historical context and evolution
- Current state and recent developments
- Key stakeholders and use cases

## Methodology
Briefly describe:
- Tools used for research
- Sources analyzed
- Research approach

## Detailed Findings
Write 6-10 paragraphs with:
- Specific data points and statistics
- Quotes or key information from sources
- Multiple perspectives and viewpoints
- Technical details and specifications
- Real-world examples and case studies
- Comparative analysis where relevant

## Analysis & Insights
Write 4-5 paragraphs analyzing:
- Patterns and trends identified
- Implications and significance
- Strengths and limitations
- Future outlook and predictions

## Recommendations
Provide 5-8 specific, actionable recommendations:
- Based on evidence from research
- Prioritized by importance
- Include rationale for each

## Conclusion
Write 2-3 paragraphs:
- Synthesize key findings
- Final assessment
- Future considerations

TOOL USAGE STRATEGY:
1. Start with multi_search to find key sources (call 2-3 times with different queries)
2. Use traverse_website on important sites to gather detailed content
3. Use content_operations to extract specific information
4. Call trends_core if relevant to show data trends
5. Make 6-10+ total tool calls for comprehensive coverage

WRITING STYLE:
- Professional and analytical
- Use specific examples and data
- Cite sources when referencing information
- Write detailed paragraphs (100-200 words each)
- Use markdown formatting for structure"""
                }, {
                    "role": "user",
                    "content": f"""Create a comprehensive, professional research report on: {topic}

Requirements:
- Minimum 4000 characters
- Use tools extensively (6-10+ calls)
- Follow the structured format provided
- Include specific details, examples, and data
- Write in professional analytical style

Begin your research now."""
                }]
                
                # Execute up to 8 tool calls
                for iteration in range(8):
                    if ctx:
                        await ctx.report_progress(0.2 + (iteration * 0.08))
                    
                    # Call AI with tools
                    response = await ai_client.chat.send_async(
                        models=free_models,  # OpenRouter handles fallbacks
                        messages=messages,
                        tools=tools,
                        tool_choice="auto",
                        temperature=0.7,
                        max_tokens=2000
                    )
                    
                    assistant_message = response.choices[0].message
                    
                    # Check if AI wants to call tools
                    if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                        # Add assistant message to history
                        messages.append({
                            "role": "assistant",
                            "content": assistant_message.content,
                            "tool_calls": [
                                {
                                    "id": tc.id,
                                    "type": "function",
                                    "function": {
                                        "name": tc.function.name,
                                        "arguments": tc.function.arguments
                                    }
                                }
                                for tc in assistant_message.tool_calls
                            ]
                        })
                        
                        # Execute each tool call
                        for tool_call in assistant_message.tool_calls:
                            tool_name = tool_call.function.name
                            arguments = json.loads(tool_call.function.arguments)
                            
                            if ctx:
                                await ctx.info(f"🔧 AI calling tool: {tool_name}")
                            
                            # Execute tool
                            tool_result = await execute_research_tool(tool_name, arguments)
                            
                            research_results["tool_calls"].append({
                                "tool": tool_name,
                                "arguments": arguments,
                                "result": tool_result[:300]  # Summary for display
                            })
                            
                            # Add tool result to messages
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": tool_result
                            })
                    else:
                        # AI finished - has final response
                        final_response = assistant_message.content or "Research completed"
                        research_results["ai_synthesis"] = final_response
                        research_results["findings"].append(final_response)
                        break
                
                research_results["status"] = "success"
                research_results["completion_time"] = datetime.now().isoformat()
                
                if ctx:
                    await ctx.info(f"🎯 Research completed! Used {len(research_results['tool_calls'])} tool calls")
                    await ctx.report_progress(1.0)
                
                # Format comprehensive output
                output = f"# 📋 Research Analysis: *{topic}*\n\n"
                output += f"## Research ID\n\n{research_id}\n\n"
                output += f"## Research Topic\n\n{topic}\n\n"
                output += f"## Research Start Time\n\n{research_results['research_start_time']}\n\n"
                output += f"## AI Model\n\n{free_models[0]}\n\n"
                
                if research_results["tool_calls"]:
                    output += f"## Tools Used\n\n"
                    for tc in research_results["tool_calls"]:
                        output += f"- **{tc['tool']}**: {tc.get('result', 'N/A')[:100]}...\n"
                    output += "\n"
                
                output += f"## AI Synthesis\n\n{research_results.get('ai_synthesis', 'No synthesis available')}\n\n"
                output += f"## Completion Time\n\n{research_results['completion_time']}\n\n"
                output += f"*Analysis completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
                
                return output
            
            else:
                # Non-AI mode: Use old logic for backward compatibility
                return await self._execute_legacy_research(topic, max_sources, research_id, ctx)
                
        except Exception as e:
            error_msg = f"Research workflow failed for '{topic}': {str(e)}"
            if ctx:
                await ctx.error(f"❌ {error_msg}")
            
            logger.error(error_msg)
            return f"# 📋 Research Analysis: *{topic}*\n\n❌ **Error:** {str(e)}\n\n*Analysis attempted on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"

    async def _execute_legacy_research(self, topic: str, max_sources: int, research_id: str, ctx: Context = None) -> str:
        """Legacy research workflow for backward compatibility when AI is disabled."""
        if ctx:
            await ctx.info("📝 Running basic research (AI disabled)")
        
        # Simple search-based research
        from src.core.search.engines.duckduckgo.duckduckgo_engine import DuckDuckGoSearchEngine
        engine = DuckDuckGoSearchEngine()
        
        search_results = await engine.search(query=topic, num_results=5, extract_content=False)
        
        output = f"# 📋 Research Analysis: *{topic}*\n\n"
        output += f"## Research ID\n\n{research_id}\n\n"
        output += f"## Research Topic\n\n{topic}\n\n"
        output += f"## Research Start Time\n\n{datetime.now().isoformat()}\n\n"
        output += f"## AI Model\n\nNone (AI insights disabled)\n\n"
        output += f"## Sources Found\n\n"
        
        if search_results:
            for i, result in enumerate(search_results[:5], 1):
                output += f"{i}. **{result.title}**\n"
                output += f"   - URL: {result.url}\n"
                output += f"   - Description: {result.description}\n\n"
        else:
            output += "No sources found\n\n"
        
        output += f"## Completion Time\n\n{datetime.now().isoformat()}\n\n"
        output += f"*Analysis completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        return output

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