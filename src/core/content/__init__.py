"""
Unified content processing module for RivalSearchMCP.
Consolidates the best content extraction, parsing, and cleaning methods.
"""

from .extractors import (
    UnifiedContentExtractor,
    GoogleSpecificExtractor,
    GenericContentExtractor
)
from .parsers import (
    UnifiedHTMLParser,
    GoogleSearchParser,
    DocumentationParser
)
from .cleaners import (
    UnifiedTextCleaner,
    HTMLToMarkdownConverter
)


__all__ = [
    # Extractors
    'UnifiedContentExtractor',
    'GoogleSpecificExtractor',
    'GenericContentExtractor',

    # Parsers
    'UnifiedHTMLParser',
    'GoogleSearchParser',
    'DocumentationParser',

    # Cleaners
    'UnifiedTextCleaner',
    'HTMLToMarkdownConverter',
]
