"""
Traversal tools for FastMCP server.
Handles website research, documentation exploration, and website mapping.
"""

from typing import Literal

from fastmcp import FastMCP

from src.core.traverse import (
    explore_documentation,
    map_website_structure,
    research_topic,
)
from src.logging.logger import logger
from src.utils import clean_html_to_markdown


def register_traversal_tools(mcp: FastMCP):
    """Register all traversal-related tools."""

    @mcp.tool
    async def traverse_website(
        url: str,
        mode: Literal["research", "docs", "map"] = "research",
        max_pages: int = 5,
        max_depth: int = 2,
        generate_llms_txt: bool = False,
    ) -> dict:
        """
        Comprehensive website traversal with different modes for different use cases.

        Args:
            url: Website URL to traverse
            mode: Traversal mode - "research" (general), "docs" (documentation), "map" (structure)
            max_pages: Maximum number of pages to traverse
            max_depth: Maximum depth for mapping mode
        """
        try:
            logger.info(f"Traversing website: {url} in {mode} mode")

            if mode == "research":
                result = await research_topic(url, max_pages=max_pages)
            elif mode == "docs":
                result = await explore_documentation(url, max_pages=max_pages)
            elif mode == "map":
                result = await map_website_structure(url, max_pages=max_pages)
            else:
                return {
                    "success": False,
                    "pages": [],
                    "summary": f"Invalid mode: {mode}. Use 'research', 'docs', or 'map'",
                    "total_pages": 0,
                    "source": url,
                }

            # Convert result to simple dict format with clean content
            pages = []
            for page_dict in result:
                # Clean HTML content
                raw_content = page_dict.get("content", "")
                clean_content = clean_html_to_markdown(
                    str(raw_content), page_dict.get("url", "")
                )

                pages.append(
                    {
                        "url": page_dict.get("url", ""),
                        "title": page_dict.get("title", ""),
                        "content": clean_content,
                        "depth": page_dict.get("depth", 0),
                    }
                )

            response = {
                "success": True,
                "pages": pages,
                "summary": f"Successfully traversed {len(result)} pages in {mode} mode",
                "total_pages": len(result),
                "source": url,
                "mode": mode,
            }

            if generate_llms_txt:
                # Generate LLMs.txt content
                llms_txt_content = f"""# {url}

This file contains information about {url} for Large Language Models.

## Site Information
- URL: {url}
- Traversal Mode: {mode}
- Pages Traversed: {len(pages)}

## Content Summary
{response["summary"]}

## Key Pages
"""
                for page in pages[:10]:  # Include up to 10 key pages
                    llms_txt_content += f"- {page['title']}: {page['url']}\n"

                response["llms_txt"] = llms_txt_content

            return response

        except Exception as e:
            logger.error(f"Website traversal failed for {url}: {e}")
            return {
                "success": False,
                "pages": [],
                "summary": f"Error: {str(e)}",
                "total_pages": 0,
                "source": url,
                "mode": mode,
            }
