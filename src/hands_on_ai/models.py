"""
Core model utilities for Hands-on AI.

This module provides centralized functionality for working with LLM models:
- Listing available models
- Checking if a model exists
- Getting model information
- Normalizing model names
- Detecting model capabilities
"""

import requests
import re
from typing import Dict, List, Any, Optional, Tuple
from .config import get_server_url, get_api_key, log

def normalize_model_name(model_name: str) -> str:
    """
    Normalize the model name to the format expected by Ollama.
    
    Args:
        model_name: Original model name
        
    Returns:
        str: Normalized model name
    """
    # If model name already has a tag (contains a colon), use it as is
    if ":" in model_name:
        return model_name
    
    # Otherwise append :latest tag
    return f"{model_name}:latest"

def get_model_info(model_name: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific model.
    
    Args:
        model_name: Name of the model
        
    Returns:
        Optional[Dict]: Model information or None if not found
    """
    # Get server URL and prepare for API call
    server_url = get_server_url()
    
    # Try variations of the model name
    original_name = model_name
    normalized_name = normalize_model_name(model_name)
    
    model_variations = [original_name]
    if normalized_name != original_name:
        model_variations.append(normalized_name)
    
    # Prepare headers with API key if available
    headers = {}
    api_key = get_api_key()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        log.debug("Using API key for authentication")
    
    # Try each variation
    for model_variant in model_variations:
        log.debug(f"Checking model: {model_variant}")
        
        try:
            # Call the Ollama API to check if the model exists and get its metadata
            response = requests.post(
                f"{server_url}/api/show",
                json={"name": model_variant},
                headers=headers,
                timeout=5
            )
            
            # If we found a matching model
            if response.status_code == 200:
                model_info = response.json()
                log.debug(f"Found model: {model_variant}")
                return model_info
            
        except Exception as e:
            log.debug(f"Error accessing model API for {model_variant}: {e}")
            continue
    
    # No matching model found
    log.debug(f"Model not found: {model_name}")
    return None

def check_model_exists(model_name: str) -> bool:
    """
    Check if a model exists on the server.
    
    Args:
        model_name: Name of the model
        
    Returns:
        bool: True if the model exists, False otherwise
    """
    return get_model_info(model_name) is not None

def list_models() -> List[Dict[str, Any]]:
    """
    List all available models.
    
    Returns:
        List[Dict]: List of model information dictionaries
    """
    server_url = get_server_url()
    
    # Prepare headers with API key if available
    headers = {}
    api_key = get_api_key()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        log.debug("Using API key for authentication")
    
    try:
        # Call the Ollama API to list all models
        response = requests.get(
            f"{server_url}/api/tags",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            models_data = response.json()
            # The API returns a dict with 'models' key containing the list
            if "models" in models_data:
                return models_data["models"]
            return []
        
        log.warning(f"Failed to list models: {response.status_code}")
        return []
        
    except Exception as e:
        log.warning(f"Error listing models: {e}")
        return []

def get_model_capabilities(model_name: str) -> Dict[str, bool]:
    """
    Determine the capabilities of a given model.
    
    Args:
        model_name: Name of the model
        
    Returns:
        Dict[str, bool]: Dictionary of capability flags
    """
    # Initialize with default capabilities (conservative)
    capabilities = {
        "react_format": False,
        "json_format": True,
        "function_calling": False,
        "tool_use": False,
        "vision": False
    }
    
    # Get model info
    model_info = get_model_info(model_name)
    if not model_info:
        return capabilities
    
    # Check parameters field for model size
    if "parameters" in model_info:
        parameters = model_info.get("parameters", {})
        
        # Extract model size info
        model_size = 0
        if "num_params" in parameters:
            model_size = parameters["num_params"]
        elif "parameter_count" in parameters:
            model_size = parameters["parameter_count"]
        
        # Models with at least 30B parameters can likely handle ReAct format
        if model_size >= 30_000_000_000:  # 30B or larger
            capabilities["react_format"] = True
            capabilities["function_calling"] = True
            capabilities["tool_use"] = True
    
    # Check template/system prompt for function calling capabilities
    template = model_info.get("template", "")
    if "function" in template.lower() or "tool" in template.lower():
        capabilities["react_format"] = True
        capabilities["function_calling"] = True
        capabilities["tool_use"] = True
    
    # Check model families based on name
    model_name_lower = model_name.lower()
    
    # Models known to support vision
    vision_models = ["llava", "bakllava", "moondream", "cogvlm"]
    if any(vision_model in model_name_lower for vision_model in vision_models):
        capabilities["vision"] = True
    
    # Models known to support function calling / tool use
    function_models = [
        "gpt-4", "gpt4", "claude-2", "claude-3", "claude3",
        "llama3-70b", "llama-70b", "mixtral-8x7b"
    ]
    
    if any(pattern.lower() in model_name_lower for pattern in function_models):
        capabilities["react_format"] = True
        capabilities["function_calling"] = True
        capabilities["tool_use"] = True
    
    return capabilities

def detect_best_format(model_name: str) -> str:
    """
    Determine the best format for the given model based on its capabilities.
    
    Args:
        model_name: Name of the model
        
    Returns:
        str: "react" or "json" (default)
    """
    capabilities = get_model_capabilities(model_name)
    
    if capabilities["react_format"]:
        return "react"
    return "json"