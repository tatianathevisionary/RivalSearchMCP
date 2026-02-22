"""
Kaggle dataset search provider.
Handles searching and retrieving datasets from Kaggle API.
"""

import asyncio
from typing import Any, Dict, List, Optional

import requests

from src.logging.logger import logger


class KaggleDatasetProvider:
    """Provider for searching Kaggle datasets."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "RivalSearchMCP/1.0"})

    async def search(
        self, query: str, limit: int = 20, sort_by: str = "relevance"
    ) -> List[Dict[str, Any]]:
        """
        Search datasets on Kaggle.

        Args:
            query: Search query
            limit: Maximum number of results
            sort_by: Sort criteria (relevance, hotness, votes, updated)

        Returns:
            List of dataset dictionaries
        """
        try:
            params = {"search": query, "size": min(limit, 100)}

            if sort_by == "hotness":
                params["sortBy"] = "hotness"
            elif sort_by == "votes":
                params["sortBy"] = "voteCount"
            elif sort_by == "updated":
                params["sortBy"] = "lastUpdated"

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(
                    "https://www.kaggle.com/api/v1/datasets/list",
                    params=params,
                    timeout=30,
                ),
            )

            if response.status_code == 200:
                datasets = response.json()
                logger.info(f"Found {len(datasets)} datasets from Kaggle for query: {query}")

                # Normalize and optimize Kaggle dataset structure
                normalized_datasets = []
                for dataset in datasets[:limit]:
                    # Extract only essential fields for efficiency
                    normalized = {
                        "id": dataset.get("id"),
                        "title": dataset.get("title", dataset.get("titleNullable", "")),
                        "description": dataset.get("subtitle", dataset.get("subtitleNullable", "")),
                        "owner_name": dataset.get(
                            "ownerName", dataset.get("ownerNameNullable", "")
                        ),
                        "url": dataset.get("url", dataset.get("urlNullable", "")),
                        "license": dataset.get(
                            "licenseName", dataset.get("licenseNameNullable", "")
                        ),
                        "size_bytes": dataset.get("totalBytes", dataset.get("totalBytesNullable")),
                        "download_count": dataset.get("downloadCount", 0),
                        "vote_count": dataset.get("voteCount", 0),
                        "last_updated": dataset.get("lastUpdated"),
                        "tags": [
                            tag.get("name", "")
                            for tag in dataset.get("tags", [])
                            if tag.get("name")
                        ],
                        "source": "kaggle",
                    }
                    # Remove None values to reduce payload size
                    normalized = {k: v for k, v in normalized.items() if v is not None and v != ""}
                    normalized_datasets.append(normalized)

                return normalized_datasets
            elif response.status_code == 400:
                logger.debug(
                    "Kaggle API requires authentication (kaggle.json). Using other sources."
                )
                return []
            else:
                logger.warning(f"Kaggle API error: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error searching Kaggle datasets: {e}")
            return []

    async def get_dataset_details(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific Kaggle dataset.

        Args:
            dataset_id: Kaggle dataset identifier

        Returns:
            Dataset details or None if not found
        """
        try:
            # Kaggle dataset IDs are in format "owner/dataset-name"
            if "/" not in dataset_id:
                logger.warning(f"Invalid Kaggle dataset ID format: {dataset_id}")
                return None

            url = f"https://www.kaggle.com/api/v1/datasets/view/{dataset_id}"

            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(url, timeout=30),
            )

            if response.status_code == 200:
                dataset = response.json()
                return {
                    "id": dataset_id,
                    "title": dataset.get("title", ""),
                    "description": dataset.get("subtitle", ""),
                    "owner_name": dataset.get("ownerName", ""),
                    "url": dataset.get("url", ""),
                    "license": dataset.get("licenseName", ""),
                    "size_bytes": dataset.get("totalBytes"),
                    "download_count": dataset.get("downloadCount", 0),
                    "vote_count": dataset.get("voteCount", 0),
                    "last_updated": dataset.get("lastUpdated"),
                    "tags": [tag.get("name", "") for tag in dataset.get("tags", [])],
                    "source": "kaggle",
                }
            else:
                logger.warning(f"Failed to get Kaggle dataset details: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting Kaggle dataset details: {e}")
            return None

    def close(self):
        """Close the session."""
        self.session.close()
