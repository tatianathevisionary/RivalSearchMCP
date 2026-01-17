"""
Web tools schemas for FastMCP server.
Handles website traversal operations.
"""

from typing import List

from pydantic import BaseModel, Field

from .retrieval import TraversalPage


class WebsiteTraversalResult(BaseModel):
    """Result from website traversal operation."""

    success: bool = Field(description="Whether traversal was successful")
    pages: List[TraversalPage] = Field(description="List of traversed pages")
    summary: str = Field(description="Human-readable summary")
    total_pages: int = Field(description="Total number of pages")
    source: str = Field(description="Source URL")
