"""
LLMs.txt file generation utilities.
Handles writing LLMs.txt files and data export.
"""

from pathlib import Path
import json
from typing import Dict, Any, List

from src.logging.logger import logger


class LLMsTxtWriter:
    """Handles writing LLMs.txt files and related data."""

    def __init__(self, pages_data: List[Dict[str, Any]], config: Dict[str, Any]):
        self.pages_data = pages_data
        self.config = config

    def write_llms_txt(self, output_file: Path):
        """Generate llms.txt file following the llmstxt.org specification."""
        logger.info(f"Generating {output_file}...")

        # Group pages by category
        categories = {}
        for page in self.pages_data:
            category = page["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(page)

        with open(output_file, "w", encoding="utf-8") as f:
            # Write H1 title (required)
            f.write(f"# {self.config['name']}\n\n")

            # Write blockquote summary (required)
            f.write(f"> {self.config['description']}\n\n")

            # Write sections with H2 headers and full content
            for category in sorted(categories.keys()):
                if category == "Other":
                    # Use "Optional" for the "Other" category as per spec
                    f.write("## Optional\n\n")
                else:
                    f.write(f"## {category}\n\n")

                for page in sorted(categories[category], key=lambda x: x["title"]):
                    # Write the link first (following llmstxt.org format)
                    description = page["description"] if page["description"] else ""
                    f.write(f"- [{page['title']}]({page['url']})")
                    if description:
                        f.write(f": {description}")
                    f.write("\n\n")

                    # Write the full content
                    f.write(page["content"])
                    f.write("\n\n---\n\n")

        logger.info(
            f"Generated {output_file} with full content from {len(self.pages_data)} pages"
        )

    def write_full_txt(self, output_file: Path):
        """Generate llms-full.txt file with expanded content."""
        logger.info(f"Generating {output_file}...")

        # Group pages by category
        categories = {}
        for page in self.pages_data:
            category = page["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(page)

        with open(output_file, "w", encoding="utf-8") as f:
            # Write H1 title (required)
            f.write(f"# {self.config['name']}\n\n")

            # Write blockquote summary (required)
            f.write(f"> {self.config['description']}\n\n")

            # Write sections with H2 headers and full content
            for category in sorted(categories.keys()):
                if category == "Other":
                    # Use "Optional" for the "Other" category as per spec
                    f.write("## Optional\n\n")
                else:
                    f.write(f"## {category}\n\n")

                for page in sorted(categories[category], key=lambda x: x["title"]):
                    # Write the link first (following llmstxt.org format)
                    description = page["description"] if page["description"] else ""
                    f.write(f"- [{page['title']}]({page['url']})")
                    if description:
                        f.write(f": {description}")
                    f.write("\n\n")

                    # Write the full content
                    f.write(page["content"])
                    f.write("\n\n---\n\n")

        logger.info(
            f"Generated {output_file} with full content from {len(self.pages_data)} pages"
        )

    def write_data_json(self, output_file: Path):
        """Save raw data for debugging."""
        with open(output_file, "w") as f:
            json.dump(self.pages_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved raw data to {output_file}")

    def write_all_formats(self, output_dir: Path):
        """Write all supported formats."""
        self.write_llms_txt(output_dir / "llms.txt")
        self.write_full_txt(output_dir / "llms-full.txt")
        self.write_data_json(output_dir / "documentation_data.json")

        logger.info("Generated files:")
        logger.info("- llms.txt (llmstxt.org format)")
        logger.info("- llms-full.txt (full content with expanded links)")
        logger.info("- documentation_data.json (raw data)")