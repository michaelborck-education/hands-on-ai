#!/usr/bin/env python
"""
Test Model Detection and Format Selection

This script tests the model detection and format selection capabilities
of the hands-on-ai package. It specifically focuses on how the agent
automatically selects the appropriate format (ReAct or JSON) based on
the model's capabilities.
"""

import os
import sys

# Add parent directory to path to allow importing the module directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def weather_data(location):
    """Get weather data for a location."""
    print(f"✅ Tool called: weather_data with input: {location}")
    return f"Weather data for {location}: Sunny, 25°C, humidity 60%, wind 5mph NE"

def temperature_graph(location):
    """Generate a temperature graph."""
    print(f"✅ Tool called: temperature_graph with input: {location}")
    return f"Graph with temperature for {location} generated. Shows temperature range of 20-30°C."

def main():
    """Test model detection and format selection."""
    from hands_on_ai.agent import register_tool
    from hands_on_ai.agent.core import _tools
    from hands_on_ai.models import get_model_capabilities, detect_best_format
    from hands_on_ai.config import get_model
    
    print("\n===== MODEL DETECTION AND FORMAT SELECTION TEST =====")
    
    # Clear any existing tools
    _tools.clear()
    
    # Register some tools
    register_tool("weather_data", "Get the weather for a location", weather_data)
    register_tool("temperature_graph", "Generate a graph with temperature", temperature_graph)
    
    # Check the current model in config
    current_model = get_model()
    print(f"Current model in config: {current_model}")
    
    # Test a variety of models
    test_models = [
        current_model,         # Current configured model
        "llama3",              # Base small model
        "llama3-70b",          # Large model with 70B parameters
        "mistral-7b",          # Small Mistral model
        "mixtral-8x7b",        # MoE model (likely to support tools)
        "gpt-4",               # Large closed-source model
        "claude-3-haiku",      # Small Claude model
        "nonexistent-model"    # Model that doesn't exist
    ]
    
    print("\n----- Format Detection Test -----")
    print(f"{'Model Name':<20} | {'Best Format':<10} | {'Function Calling':<17} | {'Tool Use':<10}")
    print("-" * 65)
    
    for model in test_models:
        # Get model capabilities
        capabilities = get_model_capabilities(model)
        format_type = detect_best_format(model)
        
        # Create status indicators
        function_status = "✓" if capabilities["function_calling"] else "✗"
        tool_status = "✓" if capabilities["tool_use"] else "✗"
        
        # Print the results
        print(f"{model:<20} | {format_type:<10} | {function_status:<17} | {tool_status:<10}")
    
    print("\n----- Format Auto-Detection -----")
    print("The agent will automatically use the best format for your model.")
    print("  • ReAct format - Used for larger models (30B+) and those with function calling capability")
    print("  • JSON format - Used for smaller models as a more reliable fallback")
    
    print("\nYou can override the auto-detection by specifying a format:")
    print("  agent.run_agent(prompt, format='json')  # Force JSON format")
    print("  agent.run_agent(prompt, format='react') # Force ReAct format")
    print("  agent.run_agent(prompt, format='auto')  # Use auto-detection (default)")
    
    print("\n===== TEST COMPLETE =====")

if __name__ == "__main__":
    main()