"""
Analysis tools for FastMCP server.
Handles content analysis and end-to-end research workflows.
"""

import asyncio
import re
from typing import List, Optional

from fastmcp import FastMCP

from src.utils.markdown_formatter import format_research_analysis_markdown
from src.logging.logger import logger


def register_analysis_tools(mcp: FastMCP):
    """Register consolidated content operations tool."""

    @mcp.tool
    async def content_operations(
        operation: str,
        url: Optional[str] = None,
        content: Optional[str] = None,
        extraction_method: str = "auto",
        analysis_type: str = "general",
        max_links: int = 100,
        link_type: str = "all",
        extract_key_points: bool = True,
        summarize: bool = True,
        include_metadata: bool = True,
    ) -> str:
        """
        Consolidated content operations: retrieve, stream, analyze, extract.

        Args:
            operation: Operation type - "retrieve", "stream", "analyze", "extract"
            url: URL for retrieve/stream/extract operations
            content: Content for analyze operation
            extraction_method: For retrieve - "auto", "html", "text", "markdown"
            analysis_type: For analyze - "general", "sentiment", "technical", "business"
            max_links: For extract - maximum links to extract
            link_type: For extract - "all", "internal", "external", "images", "documents"
            extract_key_points: For analyze - extract key points
            summarize: For analyze - create summary
            include_metadata: Include metadata in response
        """
        try:
            logger.info(f"Performing {operation} operation")

            if operation == "retrieve":
                if not url:
                    raise ValueError("URL required for retrieve operation")
                # Real content retrieval implementation with retry logic
                from src.core.fetch import base_fetch_url
                from src.utils import clean_html_to_markdown

                max_retries = 3
                content = None
                for attempt in range(max_retries):
                    try:
                        content = await base_fetch_url(url)
                        if content:
                            break
                    except Exception as e:
                        logger.warning(
                            f"Content retrieval attempt {attempt + 1} failed: {e}"
                        )
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)

                if content:
                    if extraction_method == "html":
                        result = str(content)
                    elif extraction_method == "text":
                        result = clean_html_to_markdown(str(content), url)
                    elif extraction_method == "markdown":
                        result = clean_html_to_markdown(str(content), url)
                    else:  # auto
                        result = clean_html_to_markdown(str(content), url)
                else:
                    result = f"Failed to retrieve content from {url} after {max_retries} attempts"

                return result

            elif operation == "stream":
                if not url:
                    raise ValueError("URL required for stream operation")
                # Real streaming implementation with retry logic
                from src.core.fetch import stream_fetch

                max_retries = 3
                content = None
                for attempt in range(max_retries):
                    try:
                        content = await stream_fetch(url)
                        if content:
                            break
                    except Exception as e:
                        logger.warning(
                            f"Content streaming attempt {attempt + 1} failed: {e}"
                        )
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)

                if content:
                    result = str(content)
                else:
                    result = f"Failed to stream content from {url} after {max_retries} attempts"

                return result

            elif operation == "analyze":
                if not content:
                    raise ValueError("Content required for analyze operation")

                # Basic content analysis
                analysis_result = {
                    "content_length": len(content),
                    "word_count": len(content.split()),
                    "analysis_type": analysis_type,
                    "key_points": [],
                    "summary": "",
                    "insights": {},
                }

                # Extract key points if requested
                if extract_key_points:
                    sentences = re.split(r"[.!?]+", content)
                    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]

                    scored_sentences = []
                    for sentence in sentences:
                        score = len(sentence) * 0.3
                        important_words = [
                            "important",
                            "key",
                            "critical",
                            "essential",
                            "significant",
                            "major",
                            "primary",
                        ]
                        for word in important_words:
                            if word.lower() in sentence.lower():
                                score += 10
                        scored_sentences.append((sentence, score))

                    scored_sentences.sort(key=lambda x: x[1], reverse=True)
                    key_points = [s[0] for s in scored_sentences[:5]]
                    analysis_result["key_points"] = key_points

                # Create summary if requested
                if summarize:
                    sentences = re.split(r"[.!?]+", content)
                    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

                    if len(sentences) > 3:
                        summary_parts = [
                            sentences[0],
                            sentences[len(sentences) // 2]
                            if len(sentences) > 2
                            else "",
                            sentences[-1] if len(sentences) > 1 else "",
                        ]
                        summary = ". ".join([s for s in summary_parts if s])
                    else:
                        summary = content

                    analysis_result["summary"] = summary

                # Type-specific analysis
                if analysis_type == "sentiment":
                    positive_words = [
                        "good",
                        "great",
                        "excellent",
                        "amazing",
                        "wonderful",
                        "positive",
                        "happy",
                        "success",
                    ]
                    negative_words = [
                        "bad",
                        "terrible",
                        "awful",
                        "negative",
                        "sad",
                        "failure",
                        "problem",
                        "issue",
                    ]

                    content_lower = content.lower()
                    positive_count = sum(
                        content_lower.count(word) for word in positive_words
                    )
                    negative_count = sum(
                        content_lower.count(word) for word in negative_words
                    )

                    sentiment = (
                        "positive"
                        if positive_count > negative_count
                        else "negative"
                        if negative_count > positive_count
                        else "neutral"
                    )
                    analysis_result["insights"]["sentiment"] = sentiment

                elif analysis_type == "technical":
                    technical_patterns = [
                        r"\b[A-Z]{2,}\b",
                        r"\b\w+\.\w+\b",
                        r"\b\d+\.\d+\b",
                        r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b",
                    ]
                    technical_terms = set()
                    for pattern in technical_patterns:
                        matches = re.findall(pattern, content)
                        technical_terms.update(matches)
                    analysis_result["insights"]["technical_terms"] = list(
                        technical_terms
                    )[:10]

                elif analysis_type == "business":
                    money_pattern = r"\$[\d,]+(?:\.\d{2})?"
                    percentage_pattern = r"\d+(?:\.\d+)?%"
                    date_pattern = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
                    money_matches = re.findall(money_pattern, content)
                    percentage_matches = re.findall(percentage_pattern, content)
                    date_matches = re.findall(date_pattern, content)
                    analysis_result["insights"]["business_metrics"] = {
                        "monetary_values": money_matches[:5],
                        "percentages": percentage_matches[:5],
                        "dates": date_matches[:5],
                    }

                return format_research_analysis_markdown(
                    {
                        "topic": f"Content Analysis: {content[:50]}{'...' if len(content) > 50 else ''}",
                        "summary": analysis_result.get("summary", ""),
                        "key_findings": analysis_result.get("key_points", []),
                        "status": "success",
                    },
                    "Content Operations",
                )

            elif operation == "extract":
                if not url:
                    raise ValueError("URL required for extract operation")

                # Real link extraction implementation
                from src.core.fetch import base_fetch_url
                from urllib.parse import urljoin, urlparse

                try:
                    content = await base_fetch_url(url)
                    if not content:
                        return format_research_analysis_markdown(
                            {"topic": f"Link Extraction from {url}", "status": "error", "error": "Failed to fetch content"},
                            "Content Operations",
                        )

                    # Parse HTML and extract links
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(str(content), 'html.parser')

                    all_links = []
                    internal_links = []
                    external_links = []
                    image_links = []
                    document_links = []

                    base_domain = urlparse(url).netloc

                    # Extract <a> tags
                    for link in soup.find_all('a', href=True):
                        href = link.get('href', '')
                        if not href or href.startswith('#'):
                            continue

                        absolute_url = urljoin(url, href)
                        link_domain = urlparse(absolute_url).netloc

                        link_info = {
                            "url": absolute_url,
                            "text": link.get_text(strip=True)[:100] or "No text",
                            "type": "internal" if link_domain == base_domain else "external"
                        }

                        all_links.append(link_info)

                        if link_domain == base_domain:
                            internal_links.append(link_info)
                        else:
                            external_links.append(link_info)

                        # Check if it's a document
                        if any(absolute_url.lower().endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip']):
                            document_links.append(link_info)

                    # Extract images
                    for img in soup.find_all('img', src=True):
                        src = img.get('src', '')
                        absolute_url = urljoin(url, src)
                        image_links.append({
                            "url": absolute_url,
                            "alt": img.get('alt', 'No alt text'),
                            "type": "image"
                        })

                    # Select links based on link_type
                    if link_type == "internal":
                        selected_links = internal_links
                    elif link_type == "external":
                        selected_links = external_links
                    elif link_type == "images":
                        selected_links = image_links
                    elif link_type == "documents":
                        selected_links = document_links
                    else:  # "all"
                        selected_links = all_links

                    # Limit to max_links
                    selected_links = selected_links[:max_links]

                    # Format result
                    result_summary = f"Extracted {len(selected_links)} {link_type} links from {url}"
                    key_findings = [f"{link.get('text', link.get('alt', 'Link'))}: {link['url']}" for link in selected_links[:10]]

                    if link_type == "all":
                        result_summary += f" ({len(internal_links)} internal, {len(external_links)} external, {len(image_links)} images, {len(document_links)} documents)"

                    return format_research_analysis_markdown(
                        {
                            "topic": f"Link Extraction: {url}",
                            "summary": result_summary,
                            "key_findings": key_findings,
                            "link_statistics": {
                                "total_links": len(all_links),
                                "internal_links": len(internal_links),
                                "external_links": len(external_links),
                                "image_links": len(image_links),
                                "document_links": len(document_links),
                                "extracted_type": link_type,
                                "extracted_count": len(selected_links),
                            },
                            "status": "success",
                        },
                        "Content Operations",
                    )

                except Exception as extract_error:
                    logger.error(f"Link extraction failed: {extract_error}")
                    return format_research_analysis_markdown(
                        {"topic": f"Link Extraction from {url}", "status": "error", "error": str(extract_error)},
                        "Content Operations",
                    )

            else:
                raise ValueError(f"Unknown operation: {operation}")

        except Exception as e:
            logger.error(f"Content operations failed: {e}")
            return format_research_analysis_markdown(
                {"topic": "Content Operations", "status": "error", "error": str(e)},
                "Content Operations",
            )

        # This should never be reached, but ensures type safety
        return format_research_analysis_markdown(
            {"topic": "Content Operations", "status": "error", "error": "Unexpected execution path"},
            "Content Operations",
        )

    @mcp.tool
    async def research_topic(
        topic: str,
        sources: Optional[List[str]] = None,
        max_sources: int = 5,
        include_analysis: bool = True,
    ) -> str:
        """
        End-to-end research workflow for a topic.

        Args:
            topic: Research topic
            sources: Optional list of specific sources to use
            max_sources: Maximum number of sources to research
            include_analysis: Whether to include content analysis
        """
        try:
            logger.info(f"Starting comprehensive research on: {topic}")

            # Real research workflow implementation
            from src.core.fetch import base_fetch_url

            research_results = {
                "topic": topic,
                "sources_researched": [],
                "key_findings": [],
                "summary": "",
                "recommendations": [],
            }

            # Step 1: Search for relevant sources
            if not sources:
                from src.core.search.engines.duckduckgo.duckduckgo_engine import (
                    DuckDuckGoSearchEngine,
                )

                duckduckgo_engine = DuckDuckGoSearchEngine()
                search_results = await duckduckgo_engine.search(
                    query=topic, num_results=max_sources
                )
                sources = [result.url for result in search_results[:max_sources]]

            # Step 2: Retrieve content from sources
            for i, source_url in enumerate(sources):
                try:
                    content = await base_fetch_url(source_url)
                    if content:
                        # Clean content
                        from src.utils import clean_html_to_markdown

                        clean_content = clean_html_to_markdown(str(content), source_url)

                        research_results["sources_researched"].append(
                            {
                                "url": source_url,
                                "content": clean_content,
                                "content_length": len(clean_content),
                            }
                        )

                        # Extract key findings from this source
                        sentences = re.split(r"[.!?]+", clean_content)
                        key_sentences = [
                            s.strip()
                            for s in sentences
                            if len(s.strip()) > 50
                            and any(
                                word in s.lower()
                                for word in [
                                    "important",
                                    "key",
                                    "critical",
                                    "significant",
                                ]
                            )
                        ]
                        research_results["key_findings"].extend(key_sentences[:3])

                except Exception as e:
                    logger.warning(f"Failed to retrieve content from {source_url}: {e}")

            # Step 3: Generate summary and recommendations
            if research_results["key_findings"]:
                research_results["summary"] = (
                    f"Research on '{topic}' found {len(research_results['sources_researched'])} relevant sources with {len(research_results['key_findings'])} key findings."
                )

                # Generate recommendations based on findings
                if len(research_results["sources_researched"]) > 2:
                    research_results["recommendations"].append(
                        "Multiple sources confirm findings - high confidence"
                    )
                if len(research_results["key_findings"]) > 5:
                    research_results["recommendations"].append(
                        "Rich information available - consider deeper analysis"
                    )
                if include_analysis:
                    research_results["recommendations"].append(
                        "Use content_operations tool for detailed insights"
                    )

            return format_research_analysis_markdown(
                {
                    "topic": topic,
                    "summary": research_results.get("summary", ""),
                    "key_findings": research_results.get("key_findings", []),
                    "sources": research_results.get("sources_researched", []),
                    "status": "success",
                },
                "Topic Research",
            )

        except Exception as e:
            logger.error(f"Research topic failed: {e}")
            return format_research_analysis_markdown(
                {"topic": topic, "status": "error", "error": str(e)}, "Topic Research"
            )
