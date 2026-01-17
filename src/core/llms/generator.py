"""
LLMs.txt generator for FastMCP server.
Generates LLMs.txt documentation files following the llmstxt.org specification.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

from src.logging.logger import logger
from .modules.content_processor import ContentProcessor
from .modules.page_processor import PageDiscoverer, PageProcessor


class LLMsTxtGenerator:
    """
    Generic LLMs.txt generator that can work with any documentation website.
    Follows the llmstxt.org specification for creating AI-readable documentation.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the generator with a configuration.

        Args:
            config: Configuration dictionary containing:
                - name: Project name
                - description: Project description
                - urls: List of URLs to start crawling from
                - max_pages: Maximum number of pages to process
                - max_depth: Maximum crawling depth
                - user_agent: User agent string
                - output_dir: Output directory for generated files
        """
        self.config = config
        self.visited_urls = set()
        self.pages_data = []
        self.content_processor = ContentProcessor()

        # Import here to avoid import issues
        import requests
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": config.get("user_agent", "LLMs.txt Generator/1.0")}
        )

        # Initialize processors
        self.page_discoverer = PageDiscoverer(self.session)
        self.page_processor = PageProcessor(self.session, self.content_processor)

    def discover_pages(self) -> list:
        """Discover pages using the page discoverer."""
        base_urls = self.config.get("urls", [])
        max_pages = self.config.get("max_pages", 100)
        return self.page_discoverer.discover_pages(base_urls, max_pages)



    def run(self):
        """Main execution method."""
        logger.info(f"LLMs.txt Generator for {self.config['name']}")
        logger.info("=" * 50)

        # Discover pages
        logger.info("Starting page discovery...")
        discovered_pages = self.discover_pages()
        logger.info(f"\nDiscovered {len(discovered_pages)} pages")

        # Process pages
        logger.info("Starting page processing...")
        self.process_pages(discovered_pages)

        # Generate output files following llmstxt.org specification
        logger.info("Starting file generation...")
        from .modules.file_writer import LLMsTxtWriter

        output_dir = Path(self.config.get("output_dir", "."))
        writer = LLMsTxtWriter(self.pages_data, self.config)
        writer.write_all_formats(output_dir)

        logger.info("\nGeneration complete!")
        logger.info(f"Processed {len(self.pages_data)} pages")