"""
Utility functions for RivalSearchMCP.
"""

# Import only the utilities that are actually used
from .content import clean_html_to_markdown
from .agents import get_random_user_agent, get_enhanced_ua_list
from .clients import get_http_client

# Re-export BeautifulSoup utilities
from bs4 import BeautifulSoup

def create_soup(html: str):
    """Create BeautifulSoup object."""
    return BeautifulSoup(html, 'html.parser')

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    import re
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

__all__ = [
    "clean_html_to_markdown",
    "create_soup",
    "clean_text",
    "get_random_user_agent",
    "get_enhanced_ua_list",
    "get_http_client",
]
