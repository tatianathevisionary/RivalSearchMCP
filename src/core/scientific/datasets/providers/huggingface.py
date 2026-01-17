"""
HuggingFace dataset search provider.
Handles searching and retrieving datasets from HuggingFace Hub.
"""

import asyncio
import requests
from typing import List, Dict, Optional, Any

from src.logging.logger import logger


class HuggingFaceDatasetProvider:
    """Provider for searching HuggingFace datasets."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "RivalSearchMCP/1.0"})

    async def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search datasets on Hugging Face.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of dataset dictionaries
        """
        try:
            params = {
                "search": query,
                "limit": min(limit, 100),
            }

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(
                    "https://huggingface.co/api/datasets", params=params, timeout=30
                ),
            )

            if response.status_code == 200:
                datasets = response.json()
                logger.info(
                    f"Found {len(datasets)} datasets from HuggingFace for query: {query}"
                )

                # Normalize and optimize HuggingFace dataset structure
                normalized_datasets = []
                for dataset in datasets[:limit]:
                    normalized = {
                        "id": dataset.get("id"),
                        "title": dataset.get("id", "").split("/")[
                            -1
                        ],  # Extract dataset name
                        "description": dataset.get("description", "")[:200]
                        if dataset.get("description")
                        else "",
                        "author": dataset.get("author"),
                        "url": f"https://huggingface.co/datasets/{dataset.get('id', '')}",
                        "downloads": dataset.get("downloads", 0),
                        "likes": dataset.get("likes", 0),
                        "last_modified": dataset.get("lastModified"),
                        "tags": dataset.get("tags", []),
                        "source": "huggingface",
                    }
                    # Remove None/empty values
                    normalized = {
                        k: v for k, v in normalized.items() if v is not None and v != ""
                    }
                    normalized_datasets.append(normalized)

                return normalized_datasets
            else:
                logger.warning(f"HuggingFace API error: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error searching HuggingFace datasets: {e}")
            return []

    async def get_dataset_details(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific HuggingFace dataset.

        Args:
            dataset_id: HuggingFace dataset identifier (e.g., "username/dataset-name")

        Returns:
            Dataset details or None if not found
        """
        try:
            url = f"https://huggingface.co/api/datasets/{dataset_id}"

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(url, timeout=30),
            )

            if response.status_code == 200:
                dataset = response.json()
                return {
                    "id": dataset_id,
                    "title": dataset.get("id", "").split("/")[-1],
                    "description": dataset.get("description", ""),
                    "author": dataset.get("author"),
                    "url": f"https://huggingface.co/datasets/{dataset_id}",
                    "downloads": dataset.get("downloads", 0),
                    "likes": dataset.get("likes", 0),
                    "last_modified": dataset.get("lastModified"),
                    "tags": dataset.get("tags", []),
                    "card_data": dataset.get("cardData"),
                    "source": "huggingface",
                }
            else:
                logger.warning(f"Failed to get HuggingFace dataset details: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting HuggingFace dataset details: {e}")
            return None

    def close(self):
        """Close the session."""
        self.session.close()