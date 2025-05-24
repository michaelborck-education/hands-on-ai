#!/usr/bin/env python
"""
Debug script to check the Ollama API and model detection.
"""

def check_available_models():
    """Get the list of available models from Ollama."""
    try:
        from hands_on_ai.config import get_server_url, get_api_key
        server_url = get_server_url()
        api_key = get_api_key()
        
        # Prepare headers with API key if available
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            print(f"Using API key: {api_key}")
        
        # Try the /api/tags endpoint first (newer Ollama versions)
        tags_url = f"{server_url}/api/tags"
        print(f"Checking for models with tags endpoint: {tags_url}")
        
        response = requests.get(
            tags_url,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"Found {len(models)} models using tags endpoint")
            return models
        else:
            print(f"Tags endpoint returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            
        # Fall back to the list endpoint (older Ollama versions)
        list_url = f"{server_url}/api/list"
        print(f"Checking for models with list endpoint: {list_url}")
        
        response = requests.get(
            list_url,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"Found {len(models)} models using list endpoint")
            return models
        else:
            print(f"List endpoint returned status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"Error listing models: {e}")
    
    return []

def check_model_details(model_name):
    """Try to get details for a specific model."""
    try:
        from hands_on_ai.config import get_server_url, get_api_key
        server_url = get_server_url()
        api_key = get_api_key()
        
        # Prepare headers with API key if available
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        # Use the /api/show endpoint
        print(f"Checking model details for: {model_name}")
        show_url = f"{server_url}/api/show"
        
        response = requests.post(
            show_url,
            json={"name": model_name},
            headers=headers,
            timeout=5
        )
        
        print(f"Show endpoint status code: {response.status_code}")
        
        if response.status_code == 200:
            model_info = response.json()
            print(f"Successfully got model info for {model_name}")
            return model_info
        else:
            print(f"Failed to get model info: {response.text}")
        
    except Exception as e:
        print(f"Error getting model details: {e}")
    
    return None

def try_generate_request(model_name, prompt="Hello, how are you?"):
    """Try a simple generate request to see if the model works."""
    try:
        from hands_on_ai.config import get_server_url, get_api_key
        server_url = get_server_url()
        api_key = get_api_key()
        
        # Prepare headers with API key if available
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        # Use the /api/generate endpoint
        print(f"Testing generation with model: {model_name}")
        generate_url = f"{server_url}/api/generate"
        
        response = requests.post(
            generate_url,
            json={
                "model": model_name,
                "prompt": prompt,
                "system": "You are a helpful assistant.",
            },
            headers=headers,
            timeout=10
        )
        
        print(f"Generate endpoint status code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("Generation successful!")
            return response_data
        else:
            print(f"Generation failed: {response.text}")
        
    except Exception as e:
        print(f"Error during generation: {e}")
    
    return None

def debug_model_format_detection():
    """Test the model format detection logic."""
    from hands_on_ai.agent.formats import detect_best_format
    
    # Try with model name variations
    model_variations = [
        "llama3.2",
        "llama3",
        "llama3:latest",
    ]
    
    print("\nTesting model format detection with variations:")
    for model in model_variations:
        format = detect_best_format(model)
        print(f"Model: {model:<15} -> Format: {format}")

def main():
    print("=" * 70)
    print("OLLAMA API DEBUG")
    print("=" * 70)
    
    # Get server URL
    from hands_on_ai.config import get_server_url
    server_url = get_server_url()
    print(f"Using Ollama server URL: {server_url}")
    
    # Test basic connectivity
    try:
        response = requests.get(server_url, timeout=5)
        print(f"Basic connectivity: {'SUCCESS' if response.status_code == 200 else 'FAILED'}")
        print(f"Status code: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {e}")
    
    # Get available models
    print("\nChecking available models:")
    models = check_available_models()
    
    if models:
        print("\nAvailable models:")
        for model in models:
            if isinstance(model, dict):
                print(f"- {model.get('name', 'Unknown')} (size: {model.get('size', 'Unknown')})")
            else:
                print(f"- {model}")
    else:
        print("No models found or couldn't retrieve model list")
    
    # Check specific model details
    print("\nChecking model details:")
    model_to_check = "llama3.2"
    model_info = check_model_details(model_to_check)
    
    if model_info:
        print("\nModel details:")
        print(f"- Name: {model_info.get('name', 'Unknown')}")
        print(f"- Model format: {model_info.get('modelfile', 'Unknown')}")
        print(f"- Parameters: {model_info.get('parameters', 'Unknown')}")
        
        template = model_info.get('template', '')
        print(f"- Template includes 'function': {'function' in template.lower()}")
        print(f"- Template includes 'tool': {'tool' in template.lower()}")
    else:
        print(f"Couldn't get details for model {model_to_check}")
    
    # Test generation
    print("\nTesting model generation:")
    generation_result = try_generate_request(model_to_check)
    
    if generation_result:
        print("\nGeneration result:")
        if "response" in generation_result:
            print(f"Response: {generation_result['response'][:100]}...")
        else:
            print("No 'response' field in result")
    
    # Test format detection
    debug_model_format_detection()
    
    print("\n" + "=" * 70)
    print("DEBUG COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
