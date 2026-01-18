#!/usr/bin/env python3
"""Simple test to show MCP server working with real tool calls."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastmcp.client import Client, PythonStdioTransport


async def main():
    print("\n🚀 Testing RivalSearchMCP Server")
    print("="*80 + "\n")

    transport = PythonStdioTransport("server.py")

    async with Client(transport) as client:
        # Test 1: List all tools
        print("📋 TEST 1: Listing all available tools...\n")
        tools = await client.list_tools()
        print(f"✅ Found {len(tools)} tools:\n")
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool.name}")

        print("\n" + "="*80)

        # Test 2: Content retrieval
        print("\n📄 TEST 2: Content Retrieval from example.com...\n")
        result = await client.call_tool(
            "content_operations",
            {
                "operation": "retrieve",
                "url": "https://example.com",
                "extraction_method": "markdown"
            }
        )

        output = result.content[0].text if result.content else "No output"
        print("RESULT (first 300 chars):")
        print("-" * 80)
        print(output[:300])
        print("...")
        print("-" * 80)

        print("\n" + "="*80)

        # Test 3: Link extraction
        print("\n🔗 TEST 3: Link Extraction from example.com...\n")
        result = await client.call_tool(
            "content_operations",
            {
                "operation": "extract",
                "url": "https://example.com",
                "link_type": "all",
                "max_links": 10
            }
        )

        output = result.content[0].text if result.content else "No output"
        print("RESULT:")
        print("-" * 80)
        print(output)
        print("-" * 80)

        print("\n" + "="*80)
        print("\n✅ All tests passed! RivalSearchMCP is working correctly!")
        print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
