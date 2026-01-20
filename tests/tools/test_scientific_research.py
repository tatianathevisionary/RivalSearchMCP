#!/usr/bin/env python3
"""
Test suite for scientific_research tool.
Validates both operations and all parameters, plus type error fix.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.mcp_client import create_client


async def test_academic_no_type_error():
    """Critical test: verify type error fix works (citationCount sorting)."""
    async with create_client() as client:
        result = await client.call_tool(
            "scientific_research",
            {
                "operation": "academic_search",
                "query": "machine learning",
                "max_results": 3
            }
        )
        
        assert result.content, "No content returned"
        output = result.content[0].text
        
        # Most critical: must not have type error
        assert "bad operand type" not in output.lower(), "TYPE ERROR STILL PRESENT!"
        assert "Error" not in output or "paper" in output.lower() or "academic" in output.lower()
        
        print(f"✅ Type error fix verified - No 'bad operand' error")


async def test_academic_search_default():
    """Test academic_search with default parameters."""
    async with create_client() as client:
        result = await client.call_tool(
            "scientific_research",
            {
                "operation": "academic_search",
                "query": "neural networks"
            }
        )
        
        output = result.content[0].text
        assert len(output) > 0, "Empty academic search output"
        
        print(f"✅ Academic search default test passed - {len(output)} chars")


async def test_academic_search_max_results():
    """Test academic_search with different max_results values."""
    async with create_client() as client:
        for max_results in [3, 10]:
            result = await client.call_tool(
                "scientific_research",
                {
                    "operation": "academic_search",
                    "query": "deep learning",
                    "max_results": max_results
                }
            )
            
            output = result.content[0].text
            assert len(output) > 200, f"Output too short for max_results={max_results}"
            print(f"  ✓ max_results={max_results} works")
        
        print(f"✅ max_results parameter test passed")


async def test_academic_search_arxiv_source():
    """Test academic_search with arXiv source."""
    async with create_client() as client:
        result = await client.call_tool(
            "scientific_research",
            {
                "operation": "academic_search",
                "query": "transformer models",
                "max_results": 5,
                "sources": ["arxiv"]
            }
        )
        
        output = result.content[0].text
        assert len(output) > 200, "arXiv search output too minimal"
        
        print(f"✅ arXiv source test passed")


async def test_academic_search_semantic_scholar():
    """Test academic_search with Semantic Scholar source."""
    async with create_client() as client:
        result = await client.call_tool(
            "scientific_research",
            {
                "operation": "academic_search",
                "query": "computer vision",
                "max_results": 5,
                "sources": ["semantic_scholar"]
            }
        )
        
        output = result.content[0].text
        assert len(output) > 100, "Semantic Scholar search output too minimal"
        
        print(f"✅ Semantic Scholar source test passed")


async def test_academic_search_multiple_sources():
    """Test academic_search with multiple sources."""
    async with create_client() as client:
        result = await client.call_tool(
            "scientific_research",
            {
                "operation": "academic_search",
                "query": "reinforcement learning",
                "max_results": 5,
                "sources": ["arxiv", "semantic_scholar"]
            }
        )
        
        output = result.content[0].text
        assert len(output) > 200, "Multiple sources search output too minimal"
        
        print(f"✅ Multiple sources test passed")


async def test_dataset_discovery_default():
    """Test dataset_discovery with default parameters."""
    async with create_client() as client:
        result = await client.call_tool(
            "scientific_research",
            {
                "operation": "dataset_discovery",
                "query": "image classification"
            }
        )
        
        output = result.content[0].text
        assert len(output) > 0, "Empty dataset discovery output"
        
        print(f"✅ Dataset discovery default test passed")


async def test_dataset_discovery_max_results():
    """Test dataset_discovery with specific max_results."""
    async with create_client() as client:
        result = await client.call_tool(
            "scientific_research",
            {
                "operation": "dataset_discovery",
                "query": "natural language processing",
                "max_results": 5
            }
        )
        
        output = result.content[0].text
        assert len(output) > 100, "Dataset discovery output too minimal"
        
        print(f"✅ Dataset discovery max_results test passed")


async def test_dataset_discovery_with_categories():
    """Test dataset_discovery with categories parameter."""
    async with create_client() as client:
        result = await client.call_tool(
            "scientific_research",
            {
                "operation": "dataset_discovery",
                "query": "time series",
                "max_results": 3,
                "categories": ["computer_science"]
            }
        )
        
        output = result.content[0].text
        assert len(output) > 50, "Dataset discovery with categories too minimal"
        
        print(f"✅ Dataset discovery with categories test passed")


if __name__ == "__main__":
    asyncio.run(test_academic_no_type_error())
    asyncio.run(test_academic_search_default())
    asyncio.run(test_academic_search_max_results())
    asyncio.run(test_academic_search_arxiv_source())
    asyncio.run(test_academic_search_semantic_scholar())
    asyncio.run(test_academic_search_multiple_sources())
    asyncio.run(test_dataset_discovery_default())
    asyncio.run(test_dataset_discovery_max_results())
    asyncio.run(test_dataset_discovery_with_categories())
    print("\n✅ All scientific_research tests passed!")
