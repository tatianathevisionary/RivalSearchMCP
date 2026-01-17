"""
AI model selection utilities for research workflows.
Handles OpenRouter model selection with fallback logic.
"""

import os
import requests
from typing import Optional

from src.logging.logger import logger


def get_best_free_model_with_tools() -> str:
    """Dynamically fetch the best available free OpenRouter model that supports tool calling."""
    custom_model = os.getenv('OPENROUTER_MODEL', '')
    if custom_model:
        logger.info(f"Using custom OpenRouter model from env: {custom_model}")
        return custom_model

    # Known free models...
    Dynamically fetch the best available free OpenRouter model that supports tool calling.

    Uses OpenRouter API directly to find free models with tool support.
    Prioritizes known good models, then discovers others dynamically.

    Returns:
        Single best model ID that is free and supports tools
    """
    # Known free models that support tool calling (from OpenRouter current list)
    priority_models = [
        "meta-llama/llama-3.3-70b-instruct:free",  # Best performance, large context
        "mistralai/mistral-7b-instruct:free",  # Good performance, confirmed tool support
        "google/gemma-3-27b-it:free",  # Large context, modern architecture
        "meta-llama/llama-3.1-8b-instruct:free",  # Legacy but reliable
        "microsoft/wizardlm-2-8x22b:free",  # Good performance
    ]

    try:
        # Use requests to call OpenRouter API directly
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            logger.warning("No OPENROUTER_API_KEY found, using priority fallback")
            return priority_models[0]

        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(
            "https://openrouter.ai/api/v1/models", headers=headers, timeout=10
        )
        response.raise_for_status()

        data = response.json()
        if "data" not in data:
            logger.warning("Invalid API response, using priority fallback")
            return priority_models[0]

        # Create lookup of available models
        available_models = {model["id"]: model for model in data["data"]}

        # First, try priority models that are available and support tools
        for model_id in priority_models:
            if model_id in available_models:
                model = available_models[model_id]

                # Check if model is free (pricing.prompt == "0" and pricing.completion == "0")
                pricing = model.get("pricing", {})
                is_free = (
                    pricing.get("prompt") == "0" and pricing.get("completion") == "0"
                )

                # Check if model supports tools
                supported_params = model.get("supported_parameters", [])
                supports_tools = "tools" in supported_params

                if is_free and supports_tools:
                    logger.info(f"Selected priority free model with tools: {model_id}")
                    return model_id

        # If no priority models work, search for any free model with tools
        free_tool_models = []
        for model in data["data"]:
            pricing = model.get("pricing", {})
            is_free = pricing.get("prompt") == "0" and pricing.get("completion") == "0"
            supported_params = model.get("supported_parameters", [])
            supports_tools = "tools" in supported_params

            if is_free and supports_tools:
                model_id = model["id"]
                # Try to get throughput info for ranking
                top_provider = model.get("top_provider", {})
                throughput = (
                    top_provider.get("throughput_last_30m", {}).get("p50", 0)
                    if top_provider
                    else 0
                )
                free_tool_models.append((model_id, throughput))

        if free_tool_models:
            # Sort by throughput (highest first), then by model name for consistency
            free_tool_models.sort(key=lambda x: (-x[1], x[0]))
            best_model = free_tool_models[0][0]
            logger.info(f"Selected best available free model with tools: {best_model}")
            return best_model

        # If no models found, use priority fallback
        logger.warning(
            "No free models with tool support found, using priority fallback"
        )
        return priority_models[0]

    except Exception as e:
        logger.warning(f"Could not fetch dynamic models: {e}. Using priority fallback.")
        return priority_models[0]