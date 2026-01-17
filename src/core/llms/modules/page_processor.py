"""
Page processing utilities for LLMs.txt generation.
Handles HTML parsing and content extraction from web pages.
"""

from typing import Optional, List, Dict, Any
from urllib.parse import urljoin, urlparse

from src.logging.logger import logger


class PageProcessor:
    """Handles processing of individual web pages."""

    def __init__(self, session, content_processor):
        self.session = session
        self.content_processor = content_processor

    def process_page(self, url: str, visited_urls: set) -> Optional[Dict[str, Any]]:
        """Process a single page and return structured data."""
        if url in visited_urls:
            return None

        logger.info(f"Processing page: {url}")

        try:
            content = self._get_page_content(url)
            if not content:
                return None

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, "html.parser")

            # Extract title
            title = self._extract_title(soup)

            # Extract main content
            main_content = self._extract_main_content(soup)

            # Clean content
            clean_content = self.content_processor.clean_text_content(main_content)

            # Categorize page
            category = self._categorize_page(title, clean_content, url)

            # Create page data
            page_data = {
                "url": url,
                "title": title,
                "content": clean_content,
                "category": category,
                "description": (
                    clean_content[:200] + "..."
                    if len(clean_content) > 200
                    else clean_content
                ),
            }

            visited_urls.add(url)
            return page_data

        except Exception as e:
            logger.warning(f"Failed to process {url}: {e}")
            return None

    def _get_page_content(self, url: str) -> Optional[str]:
        """Get page content with error handling."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"Failed to get content from {url}: {e}")
            return None

    def _extract_title(self, soup) -> str:
        """Extract page title."""
        title_tag = soup.find("title")
        return title_tag.get_text(strip=True) if title_tag else "Untitled"

    def _extract_main_content(self, soup) -> str:
        """Extract main content from HTML."""
        # Try to find main content areas
        main_selectors = [
            "main", '[role="main"]', ".main-content", ".content",
            ".post-content", ".article-content", "#content", "#main",
        ]

        for selector in main_selectors:
            main_element = soup.select_one(selector)
            if main_element:
                return str(main_element)

        # Fallback: remove navigation and get body content
        self._remove_unwanted_elements(soup)
        body = soup.find("body")
        return str(body) if body else str(soup)

    def _remove_unwanted_elements(self, soup):
        """Remove unwanted HTML elements."""
        import re

        # Remove script and style elements
        for element in soup(["script", "style", "noscript", "iframe", "embed", "object"]):
            element.decompose()

        # Remove navigation, footer, header elements
        for element in soup(["nav", "footer", "header", "aside", "menu"]):
            element.decompose()

        # Remove common ad and tracking elements
        for element in soup.find_all(
            class_=re.compile(
                r"(ad|ads|advertisement|banner|tracking|analytics|cookie|popup|modal|overlay)",
                re.I,
            )
        ):
            element.decompose()

    def _categorize_page(self, title: str, content: str, url: str) -> str:
        """Categorize page based on content and URL."""
        title_lower = title.lower()
        url_lower = url.lower()

        # Documentation categories
        if any(word in title_lower for word in ["api", "reference", "docs", "documentation"]):
            return "API Reference"
        elif any(word in title_lower for word in ["guide", "tutorial", "how-to", "getting started"]):
            return "Guides & Tutorials"
        elif any(word in title_lower for word in ["example", "sample", "demo"]):
            return "Examples & Demos"
        elif any(word in title_lower for word in ["install", "setup", "configuration"]):
            return "Installation & Setup"
        elif any(word in title_lower for word in ["faq", "help", "support", "troubleshooting"]):
            return "Help & Support"
        elif any(word in url_lower for word in ["blog", "news", "announcement"]):
            return "Blog & News"
        else:
            return "Other"


class PageDiscoverer:
    """Handles discovery of pages from base URLs."""

    def __init__(self, session):
        self.session = session

    def discover_pages(self, base_urls: List[str], max_pages: int) -> List[Dict[str, str]]:
        """Discover pages from base URLs."""
        discovered_pages = []

        logger.info("Using simple page discovery")
        logger.info(f"Base URLs: {base_urls}")

        for base_url in base_urls:
            logger.info(f"Processing base URL: {base_url}")

            # Use simple link discovery to find pages
            discovered_urls = self._simple_link_discovery(base_url, max_pages)

            # Add the base URL itself if not already found
            if base_url not in discovered_urls:
                discovered_urls.insert(0, base_url)

            for url in discovered_urls:
                if len(discovered_pages) >= max_pages:
                    break
                if url not in [page["url"] for page in discovered_pages]:
                    discovered_pages.append({"url": url, "source": "link_discovery"})

        logger.info(f"Discovered {len(discovered_pages)} pages using simple discovery")
        return discovered_pages or []

    def _simple_link_discovery(self, base_url: str, max_pages: int) -> List[str]:
        """Simple link discovery as fallback."""
        discovered_urls = []

        try:
            html_content = self._get_page_content(base_url)
            if html_content:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, "html.parser")

                # Find all links
                for link in soup.find_all("a", href=True):
                    try:
                        href_attr = link["href"]
                        if href_attr:
                            full_url = self._resolve_url(base_url, href_attr)

                            if full_url and full_url not in discovered_urls:
                                discovered_urls.append(full_url)
                                if len(discovered_urls) >= max_pages:
                                    break
                    except (KeyError, TypeError):
                        continue
        except Exception as e:
            logger.warning(f"Link discovery failed for {base_url}: {e}")

        return discovered_urls

    def _get_page_content(self, url: str) -> Optional[str]:
        """Get page content."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(f"Failed to get content from {url}: {e}")
            return None

    def _resolve_url(self, base_url: str, href: str) -> Optional[str]:
        """Resolve relative URLs to absolute URLs."""
        try:
            # Skip external links, javascript, mailto, etc.
            if href.startswith(("http://", "https://", "javascript:", "mailto:", "tel:")):
                return None

            # Resolve relative URL
            full_url = urljoin(base_url, href)

            # Only include same-domain URLs
            base_domain = urlparse(base_url).netloc
            full_domain = urlparse(full_url).netloc

            if base_domain == full_domain:
                return full_url

            return None
        except Exception:
            return None