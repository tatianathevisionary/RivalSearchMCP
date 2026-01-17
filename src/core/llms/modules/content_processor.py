"""
Content processing utilities for LLMs.txt generation.
Handles HTML parsing, metadata extraction, and content cleaning.
"""

import re
from typing import Dict, Any, List
from urllib.parse import urljoin


class ContentProcessor:
    """Advanced content processing for LLMs.txt generation."""

    def __init__(self):
        """Initialize the content processor."""

    def extract_metadata(self, soup) -> Dict[str, Any]:
        """Extract metadata from HTML content."""
        metadata = {}

        # Extract meta tags
        meta_tags = soup.find_all("meta")
        for meta in meta_tags:
            name = meta.get("name", meta.get("property", ""))
            content = meta.get("content", "")
            if name and content:
                metadata[name] = content

        # Extract Open Graph tags
        og_tags = soup.find_all("meta", property=re.compile(r"^og:"))
        for og in og_tags:
            property_name = og.get("property", "")
            content = og.get("content", "")
            if property_name and content:
                metadata[property_name] = content

        return metadata

    def extract_links(self, soup, base_url: str) -> List[Dict[str, str]]:
        """Extract and categorize links from HTML content."""
        links = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            text = link.get_text(strip=True)

            if href and text:
                full_url = urljoin(base_url, href)
                link_type = self._categorize_link(href, text)

                links.append({"url": full_url, "text": text, "type": link_type})

        return links

    def _categorize_link(self, href: str, text: str) -> str:
        """Categorize link based on URL and text."""
        href_lower = href.lower()
        text_lower = text.lower()

        if any(word in href_lower for word in ["api", "docs", "reference"]):
            return "documentation"
        elif any(word in href_lower for word in ["guide", "tutorial", "how-to"]):
            return "guide"
        elif any(word in href_lower for word in ["example", "demo", "sample"]):
            return "example"
        elif any(word in href_lower for word in ["install", "setup", "get-started"]):
            return "setup"
        elif any(word in text_lower for word in ["download", "install", "setup"]):
            return "download"
        else:
            return "general"

    def clean_text_content(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove special characters that might interfere with markdown
        text = re.sub(r'[^\w\s\-.,!?;:()[\]{}"\']', "", text)

        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(""", "'").replace(""", "'")

        return text.strip()

    def extract_headings(self, soup) -> List[Dict[str, Any]]:
        """Extract heading structure from HTML content."""
        headings = []

        for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            level = int(heading.name[1])
            text = heading.get_text(strip=True)

            if text:
                headings.append(
                    {"level": level, "text": text, "id": heading.get("id", "")}
                )

        return headings