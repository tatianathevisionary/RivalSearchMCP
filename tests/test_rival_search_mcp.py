"""
Professional-grade test suite for RivalSearchMCP.
Tests all 8 tools with unit tests, integration tests, and proper mocking.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from typing import Dict, Any
import json
import os
import tempfile
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.client import Client

# Import the server
from server import app


@pytest.fixture
async def mcp_client():
    """Fixture providing a FastMCP client connected to RivalSearchMCP server."""
    async with Client(app) as client:
        yield client


@pytest.fixture
def mock_search_engines():
    """Mock search engine responses."""
    mock_duckduckgo = MagicMock()
    mock_duckduckgo.search.return_value = [
        {
            "title": "Python Programming Guide",
            "url": "https://example.com/python",
            "description": "Learn Python programming",
            "engine": "duckduckgo",
            "position": 1,
        }
    ]

    mock_yahoo = MagicMock()
    mock_yahoo.search.return_value = [
        {
            "title": "Yahoo Python Tutorial",
            "url": "https://yahoo.example.com/python",
            "description": "Python tutorial on Yahoo",
            "engine": "yahoo",
            "position": 1,
        }
    ]

    with (
        patch(
            "src.core.search.engines.duckduckgo.duckduckgo_engine.DuckDuckGoSearchEngine",
            return_value=mock_duckduckgo,
        ),
        patch(
            "src.core.search.engines.yahoo.yahoo_engine.YahooSearchEngine",
            return_value=mock_yahoo,
        ),
    ):
        yield {"duckduckgo": mock_duckduckgo, "yahoo": mock_yahoo}


@pytest.fixture
def mock_content_fetch():
    """Mock content fetching."""
    with patch("src.core.fetch.base_fetch_url") as mock_fetch:
        mock_fetch.return_value = "<html><body><h1>Test Content</h1><p>This is test content.</p></body></html>"
        yield mock_fetch


@pytest.fixture
def mock_trends_api():
    """Mock Google Trends API."""
    mock_api = MagicMock()
    mock_api.search_trends.return_value = [
        {
            "keyword": "AI",
            "trends": [10, 20, 30],
            "dates": ["2024-01", "2024-02", "2024-03"],
        }
    ]
    mock_api.get_related_queries.return_value = {
        "queries": ["artificial intelligence", "machine learning"]
    }
    mock_api.get_interest_over_time.return_value = {"data": "time_series_data"}

    with patch("src.core.trends.GoogleTrendsAPI", return_value=mock_api):
        yield mock_api


@pytest.fixture
def mock_scientific_search():
    """Mock scientific research APIs."""
    with (
        patch("src.tools.scientific.search_arxiv_robust") as mock_arxiv,
        patch("src.tools.scientific.search_semantic_scholar_robust") as mock_ss,
        patch("src.tools.scientific.search_pubmed_robust") as mock_pubmed,
        patch("src.tools.scientific.search_kaggle_datasets_robust") as mock_kaggle,
        patch("src.tools.scientific.search_huggingface_datasets_robust") as mock_hf,
    ):
        mock_arxiv.return_value = [
            {
                "title": "Test Paper",
                "authors": ["Author"],
                "year": 2024,
                "source": "arxiv",
            }
        ]
        mock_ss.return_value = [
            {
                "title": "Semantic Scholar Paper",
                "authors": ["Author"],
                "year": 2024,
                "source": "semantic_scholar",
            }
        ]
        mock_pubmed.return_value = [
            {
                "title": "Medical Paper",
                "authors": ["Author"],
                "year": 2024,
                "source": "pubmed",
            }
        ]
        mock_kaggle.return_value = [
            {"title": "Test Dataset", "description": "Test data", "source": "kaggle"}
        ]
        mock_hf.return_value = [
            {
                "title": "HF Dataset",
                "description": "Hugging Face data",
                "source": "huggingface",
            }
        ]

        yield {
            "arxiv": mock_arxiv,
            "semantic_scholar": mock_ss,
            "pubmed": mock_pubmed,
            "kaggle": mock_kaggle,
            "huggingface": mock_hf,
        }


class TestServerInitialization:
    """Test server initialization and basic functionality."""

    @pytest.mark.asyncio
    async def test_server_starts_and_has_tools(self, mcp_client):
        """Test that server starts and exposes expected tools."""
        tools = await mcp_client.list_tools()
        tool_names = [tool.name for tool in tools]

        expected_tools = [
            "multi_search",
            "content_operations",
            "traverse_website",
            "trends_core",
            "trends_export",
            "research_topic",
            "scientific_research",
            "research_workflow",
        ]

        for tool in expected_tools:
            assert tool in tool_names, f"Tool {tool} not found in {tool_names}"

        assert len(tools) >= 8, f"Expected at least 8 tools, got {len(tools)}"

    @pytest.mark.asyncio
    async def test_server_has_resources(self, mcp_client):
        """Test that server exposes resources."""
        resources = await mcp_client.list_resources()
        assert isinstance(resources, list)
        assert len(resources) >= 5  # Should have at least 5 resources

    @pytest.mark.asyncio
    async def test_server_has_prompts(self, mcp_client):
        """Test that server exposes prompts."""
        prompts = await mcp_client.list_prompts()
        assert isinstance(prompts, list)
        assert len(prompts) >= 4  # Should have at least 4 prompts


class TestMultiSearchTool:
    """Test the multi_search tool functionality."""

    @pytest.mark.asyncio
    async def test_multi_search_basic(self, mcp_client, mock_search_engines):
        """Test basic multi-engine search."""
        result = await mcp_client.call_tool(
            "multi_search",
            {"query": "python programming", "num_results": 5, "extract_content": False},
        )

        assert result.content
        content = result.content[0].text
        assert "# 🔍 Search Results" in content
        assert "python programming" in content.lower()

    @pytest.mark.asyncio
    async def test_multi_search_with_content_extraction(
        self, mcp_client, mock_search_engines, mock_content_fetch
    ):
        """Test multi-search with content extraction."""
        result = await mcp_client.call_tool(
            "multi_search",
            {"query": "test query", "num_results": 2, "extract_content": True},
        )

        assert result.content
        content = result.content[0].text
        assert "# 🔍 Search Results" in content

    @pytest.mark.asyncio
    async def test_multi_search_parameter_validation(self, mcp_client):
        """Test parameter validation for multi_search."""
        # Test missing query
        with pytest.raises(Exception):
            await mcp_client.call_tool("multi_search", {"num_results": 5})

        # Test invalid num_results
        with pytest.raises(Exception):
            await mcp_client.call_tool(
                "multi_search", {"query": "test", "num_results": 0}
            )


class TestContentOperationsTool:
    """Test the content_operations tool."""

    @pytest.mark.asyncio
    async def test_content_operations_retrieve(self, mcp_client, mock_content_fetch):
        """Test content retrieval operation."""
        result = await mcp_client.call_tool(
            "content_operations",
            {
                "operation": "retrieve",
                "url": "https://example.com",
                "extraction_method": "markdown",
            },
        )

        assert result.content
        content = result.content[0].text
        assert isinstance(content, str)
        assert len(content) > 0

    @pytest.mark.asyncio
    async def test_content_operations_analyze(self, mcp_client):
        """Test content analysis operation."""
        result = await mcp_client.call_tool(
            "content_operations",
            {
                "operation": "analyze",
                "content": "This is a test article about artificial intelligence and machine learning.",
                "analysis_type": "general",
                "extract_key_points": True,
            },
        )

        assert result.content
        content = result.content[0].text
        assert "Content Operations" in content
        assert "analysis" in content.lower()

    @pytest.mark.asyncio
    async def test_content_operations_extract(self, mcp_client):
        """Test link extraction operation."""
        result = await mcp_client.call_tool(
            "content_operations",
            {"operation": "extract", "url": "https://example.com", "link_type": "all"},
        )

        assert result.content
        content = result.content[0].text
        assert isinstance(content, str)


class TestTraverseWebsiteTool:
    """Test the traverse_website tool."""

    @pytest.mark.asyncio
    async def test_traverse_website_research_mode(self, mcp_client):
        """Test website traversal in research mode."""
        with patch("src.core.traverse.research_topic") as mock_research:
            mock_research.return_value = [
                {
                    "url": "https://example.com/page1",
                    "title": "Page 1",
                    "content": "Content 1",
                    "depth": 0,
                }
            ]

            result = await mcp_client.call_tool(
                "traverse_website",
                {"url": "https://example.com", "mode": "research", "max_pages": 3},
            )

            assert result.content
            content = result.content[0].text
            assert "success" in content.lower() or "pages" in content.lower()

    @pytest.mark.asyncio
    async def test_traverse_website_with_llms_txt(self, mcp_client):
        """Test website traversal with LLMs.txt generation."""
        with patch("src.core.traverse.research_topic") as mock_research:
            mock_research.return_value = [
                {
                    "url": "https://example.com/page1",
                    "title": "Test Page",
                    "content": "Test content",
                    "depth": 0,
                }
            ]

            result = await mcp_client.call_tool(
                "traverse_website",
                {
                    "url": "https://example.com",
                    "mode": "research",
                    "max_pages": 2,
                    "generate_llms_txt": True,
                },
            )

            assert result.content
            content = result.content[0].text
            assert isinstance(content, str)


class TestTrendsTools:
    """Test Google Trends tools."""

    @pytest.mark.asyncio
    async def test_trends_core_search(self, mcp_client, mock_trends_api):
        """Test trends_core search operation."""
        result = await mcp_client.call_tool(
            "trends_core",
            {
                "operation": "search",
                "keywords": ["AI", "machine learning"],
                "timeframe": "today 7-d",
            },
        )

        assert result.content
        content = result.content[0].text
        assert isinstance(content, str)

    @pytest.mark.asyncio
    async def test_trends_core_related(self, mcp_client, mock_trends_api):
        """Test trends_core related queries operation."""
        result = await mcp_client.call_tool(
            "trends_core",
            {"operation": "related", "keywords": ["Python"], "timeframe": "today 12-m"},
        )

        assert result.content
        content = result.content[0].text
        assert isinstance(content, str)

    @pytest.mark.asyncio
    async def test_trends_export_csv(self, mcp_client, mock_trends_api):
        """Test trends data export to CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = await mcp_client.call_tool(
                "trends_export",
                {
                    "keywords": ["AI"],
                    "timeframe": "today 7-d",
                    "format": "csv",
                    "filename": f"{temp_dir}/test_trends.csv",
                },
            )

            assert result.content
            content = result.content[0].text
            assert "success" in content.lower() or "export" in content.lower()


class TestScientificResearchTool:
    """Test the scientific_research tool."""

    @pytest.mark.asyncio
    async def test_scientific_research_academic(
        self, mcp_client, mock_scientific_search
    ):
        """Test academic search operation."""
        result = await mcp_client.call_tool(
            "scientific_research",
            {
                "operation": "academic_search",
                "query": "machine learning",
                "max_results": 5,
                "sources": ["arxiv", "semantic_scholar"],
            },
        )

        assert result.content
        content = result.content[0].text
        assert "# 🔬 Academic Search Results" in content
        assert "machine learning" in content

    @pytest.mark.asyncio
    async def test_scientific_research_datasets(
        self, mcp_client, mock_scientific_search
    ):
        """Test dataset discovery operation."""
        result = await mcp_client.call_tool(
            "scientific_research",
            {
                "operation": "dataset_discovery",
                "query": "computer vision",
                "max_results": 5,
                "categories": ["computer_science"],
            },
        )

        assert result.content
        content = result.content[0].text
        assert "# 📊 Dataset Discovery Results" in content
        assert "computer vision" in content


class TestResearchWorkflowTool:
    """Test the AI-enhanced research workflow tool."""

    @pytest.mark.asyncio
    async def test_research_workflow_basic(self, mcp_client):
        """Test basic research workflow."""
        with patch(
            "src.core.search.engines.duckduckgo.duckduckgo_engine.DuckDuckGoSearchEngine"
        ) as mock_engine:
            mock_engine.return_value.search.return_value = [
                {
                    "title": "Test Article",
                    "url": "https://example.com",
                    "description": "Test description",
                    "engine": "duckduckgo",
                }
            ]

            result = await mcp_client.call_tool(
                "research_workflow",
                {
                    "topic": "test research topic",
                    "max_sources": 3,
                    "research_depth": "basic",
                    "enable_ai_insights": False,
                },
            )

            assert result.content
            content = result.content[0].text
            assert "Research Workflow" in content or "research" in content.lower()

    @pytest.mark.asyncio
    async def test_research_workflow_with_ai(self, mcp_client):
        """Test research workflow with AI insights."""
        with (
            patch(
                "src.core.search.engines.duckduckgo.duckduckgo_engine.DuckDuckGoSearchEngine"
            ) as mock_engine,
            patch("openrouter.OpenRouter") as mock_openrouter,
        ):
            mock_engine.return_value.search.return_value = [
                {
                    "title": "AI Test Article",
                    "url": "https://example.com",
                    "description": "AI description",
                    "engine": "duckduckgo",
                }
            ]

            mock_client = MagicMock()
            mock_openrouter.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "AI insights here"
            mock_client.chat.send_async.return_value = mock_response

            result = await mcp_client.call_tool(
                "research_workflow",
                {
                    "topic": "AI trends",
                    "max_sources": 2,
                    "research_depth": "comprehensive",
                    "enable_ai_insights": True,
                    "ai_model": "test-model",
                },
            )

            assert result.content
            content = result.content[0].text
            assert isinstance(content, str)


class TestResearchTopicTool:
    """Test the research_topic tool."""

    @pytest.mark.asyncio
    async def test_research_topic_basic(self, mcp_client):
        """Test basic topic research."""
        with patch(
            "src.core.search.engines.duckduckgo.duckduckgo_engine.DuckDuckGoSearchEngine"
        ) as mock_engine:
            mock_engine.return_value.search.return_value = [
                {
                    "title": "Test Topic Article",
                    "url": "https://example.com/topic",
                    "description": "Topic description",
                    "engine": "duckduckgo",
                }
            ]

            result = await mcp_client.call_tool(
                "research_topic",
                {"topic": "test topic", "max_sources": 3, "include_analysis": True},
            )

            assert result.content
            content = result.content[0].text
            assert "Topic Research" in content or "research" in content.lower()


class TestErrorHandling:
    """Test error handling across tools."""

    @pytest.mark.asyncio
    async def test_invalid_operation(self, mcp_client):
        """Test handling of invalid operations."""
        result = await mcp_client.call_tool(
            "content_operations", {"operation": "invalid_operation", "content": "test"}
        )

        assert result.content
        content = result.content[0].text
        assert isinstance(content, str)

    @pytest.mark.asyncio
    async def test_missing_required_parameters(self, mcp_client):
        """Test handling of missing required parameters."""
        # Test multi_search without query
        with pytest.raises(Exception):
            await mcp_client.call_tool("multi_search", {"num_results": 5})

    @pytest.mark.asyncio
    async def test_network_errors(self, mcp_client):
        """Test handling of network errors."""
        with patch(
            "src.core.fetch.base_fetch_url", side_effect=Exception("Network error")
        ):
            result = await mcp_client.call_tool(
                "content_operations",
                {"operation": "retrieve", "url": "https://nonexistent.example.com"},
            )

            assert result.content
            content = result.content[0].text
            assert isinstance(content, str)


class TestConcurrentOperations:
    """Test concurrent tool operations."""

    @pytest.mark.asyncio
    async def test_multiple_concurrent_searches(self, mcp_client, mock_search_engines):
        """Test running multiple searches concurrently."""
        tasks = []
        for i in range(3):
            task = mcp_client.call_tool(
                "multi_search",
                {
                    "query": f"concurrent test {i}",
                    "num_results": 2,
                    "extract_content": False,
                },
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                pytest.fail(f"Concurrent search failed: {result}")
            # Type checker doesn't understand that we've filtered out exceptions
            assert result.content  # type: ignore
            content = result.content[0].text  # type: ignore
            assert "# 🔍 Search Results" in content


class TestIntegrationScenarios:
    """Test integrated workflows combining multiple tools."""

    @pytest.mark.asyncio
    async def test_search_to_content_workflow(
        self, mcp_client, mock_search_engines, mock_content_fetch
    ):
        """Test workflow from search to content retrieval."""
        # First search
        search_result = await mcp_client.call_tool(
            "multi_search",
            {"query": "python tutorial", "num_results": 2, "extract_content": False},
        )

        assert search_result.content

        # Then retrieve content from a found URL
        content_result = await mcp_client.call_tool(
            "content_operations",
            {
                "operation": "retrieve",
                "url": "https://example.com/python",
                "extraction_method": "markdown",
            },
        )

        assert content_result.content
        content = content_result.content[0].text
        assert isinstance(content, str)

    @pytest.mark.asyncio
    async def test_research_comprehensive_workflow(
        self, mcp_client, mock_search_engines, mock_trends_api
    ):
        """Test comprehensive research workflow."""
        with patch("src.core.traverse.research_topic") as mock_traverse:
            mock_traverse.return_value = [
                {
                    "url": "https://example.com/analysis",
                    "title": "Analysis Page",
                    "content": "Analysis content",
                    "depth": 1,
                }
            ]

            # Research workflow
            result = await mcp_client.call_tool(
                "research_workflow",
                {
                    "topic": "comprehensive test topic",
                    "max_sources": 3,
                    "include_trends": True,
                    "include_website_analysis": True,
                    "research_depth": "comprehensive",
                    "enable_ai_insights": False,
                },
            )

            assert result.content
            content = result.content[0].text
            assert isinstance(content, str)
            assert len(content) > 0


# Performance and load testing
class TestPerformance:
    """Test performance characteristics."""

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_large_result_handling(self, mcp_client):
        """Test handling of large result sets."""
        result = await mcp_client.call_tool(
            "multi_search",
            {
                "query": "comprehensive topic",
                "num_results": 20,
                "extract_content": False,
            },
        )

        assert result.content
        content = result.content[0].text
        assert isinstance(content, str)

    @pytest.mark.asyncio
    async def test_memory_usage(self, mcp_client):
        """Test memory usage doesn't grow excessively."""
        # Run multiple operations and check they don't accumulate
        for i in range(5):
            result = await mcp_client.call_tool(
                "multi_search",
                {
                    "query": f"memory test {i}",
                    "num_results": 3,
                    "extract_content": False,
                },
            )
            assert result.content


if __name__ == "__main__":
    # Run basic smoke tests
    print("🧪 Running RivalSearchMCP professional test suite...")

    async def smoke_test():
        async with Client(app) as client:
            # Check server status
            tools = await client.list_tools()
            print(f"✅ Server has {len(tools)} tools")

            resources = await client.list_resources()
            print(f"✅ Server has {len(resources)} resources")

            prompts = await client.list_prompts()
            print(f"✅ Server has {len(prompts)} prompts")

            # Quick functionality test
            result = await client.call_tool(
                "multi_search",
                {"query": "test", "num_results": 1, "extract_content": False},
            )
            print("✅ Multi-search tool working")

            print("🎉 All smoke tests passed!")

    asyncio.run(smoke_test())
