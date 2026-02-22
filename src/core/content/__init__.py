"""
Unified content processing module for RivalSearchMCP.
Consolidates the best content extraction, parsing, and cleaning methods.
"""

from .cleaners import HTMLToMarkdownConverter, UnifiedTextCleaner
from .extractors import GenericContentExtractor, GoogleSpecificExtractor, UnifiedContentExtractor
from .parsers import DocumentationParser, GoogleSearchParser, UnifiedHTMLParser

__all__ = [
    # Extractors
    "UnifiedContentExtractor",
    "GoogleSpecificExtractor",
    "GenericContentExtractor",
    # Parsers
    "UnifiedHTMLParser",
    "GoogleSearchParser",
    "DocumentationParser",
    # Cleaners
    "UnifiedTextCleaner",
    "HTMLToMarkdownConverter",
]
