"""
AI model selection utilities for research workflows.
Handles OpenRouter model selection with dynamic discovery and fallback logic.
"""

import os
import requests
from typing import List

from src.logging.logger import logger


def get_free_models_with_tools(api_key: str) -> List[str]:
    """
    Get free OpenRouter models with tool support.
    Primary model is HARDCODED (meta-llama), fallbacks are dynamically fetched.
    
    Returns list with meta-llama first, then dynamic fallbacks.

    Args:
        api_key: OpenRouter API key

    Returns:
        List of model IDs with primary model first, then fallbacks
        Maximum 3 models (OpenRouter limit)
    """
    # HARDCODED PRIMARY MODEL
    primary_model = "meta-llama/llama-3.3-70b-instruct:free"
    
    try:
        # Step 1: Get all models with tool support from OpenRouter API
        logger.info("Fetching free models with tool support from OpenRouter...")
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(
            "https://openrouter.ai/api/v1/models?supported_parameters=tools",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        if "data" not in data:
            raise ValueError("Invalid API response format")

        # Step 2: Filter for FREE models (pricing.prompt == "0" AND pricing.completion == "0")
        all_models = data["data"]
        free_models = []
        
        for model in all_models:
            pricing = model.get("pricing", {})
            is_free = (
                pricing.get("prompt") == "0" and 
                pricing.get("completion") == "0"
            )
            model_id = model.get("id", "")
            
            # Skip primary model (we'll add it first manually)
            if is_free and model_id != primary_model:
                free_models.append(model)
        
        logger.info(f"Found {len(free_models)} free fallback models with tool support")
        
        # Step 3: Sort by context_length DESC (largest/best first)
        free_models.sort(
            key=lambda m: m.get("context_length", 0) or 0,
            reverse=True
        )
        
        # Step 4: Build final list - primary first, then top 2 fallbacks (OpenRouter max = 3)
        fallback_ids = [model["id"] for model in free_models[:2]]
        final_models = [primary_model] + fallback_ids
        
        logger.info(f"Primary model (hardcoded): {final_models[0]}")
        logger.info(f"Fallback models (dynamic): {fallback_ids}")
        
        return final_models

    except Exception as e:
        logger.error(f"Failed to fetch free models: {e}")
        # Emergency fallback: return only primary
        logger.warning("Using emergency fallback - primary model only")
        return [primary_model]
