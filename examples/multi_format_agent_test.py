#!/usr/bin/env python
"""
Test script for the enhanced multi-format agent functionality.

This script demonstrates the new format auto-detection and JSON-based agent
that works with smaller language models.
"""

def weather_data(location):
    """Get weather data for a location."""
    print(f"✅ Tool called: weather_data with input: {location}")
    return f"Weather data for {location}: Sunny, 25°C, humidity 60%, wind 5mph NE"

def temperature_graph(location):
    """Generate a temperature graph."""
    print(f"✅ Tool called: temperature_graph with input: {location}")
    return f"Graph with temperature for {location} generated. Shows temperature range of 20-30°C."

def precipitation_graph(location):
    """Generate a precipitation graph."""
    print(f"✅ Tool called: precipitation_graph with input: {location}")
    return f"Graph with precipitation for {location} generated. Shows 5mm rainfall expected."

def rain_chance_graph(location):
    """Generate a graph showing chance of rain."""
    print(f"✅ Tool called: rain_chance_graph with input: {location}")
    return f"Graph with chance of rain for {location} generated. Shows 20% chance of rain."

def main():
    from hands_on_ai.agent import run_agent, register_tool, list_tools
    from hands_on_ai.agent.core import _tools
    
    # Clear any existing tools to start fresh
    _tools.clear()

    # Register tools
    register_tool("weather_data", "Get the weather for a location", weather_data)
    register_tool("temperature_graph", "Generate a graph with temperature", temperature_graph)
    register_tool("precipitation_graph", "Generate a graph with precipitation", precipitation_graph)
    register_tool("rain_chance_graph", "Generate a graph with chance of rain", rain_chance_graph)
    
    # Print test header
    print("=" * 70)
    print("MULTI-FORMAT AGENT TEST")
    print("=" * 70)
    print("This test demonstrates the enhanced agent with format auto-detection.")
    print("The agent automatically selects the best format based on the model:")
    print("  - JSON format for smaller models (better compatibility)")
    print("  - ReAct format for larger models (more reasoning steps)")
    print("=" * 70)
    
    # List available tools
    print("\nAvailable tools:")
    tools = list_tools()
    for tool in tools:
        print(f"- {tool['name']}: {tool['description']}")
    
    # Test with a prompt that should make the agent call tools
    prompt = """I'm planning a picnic in Chicago tomorrow. Can you tell me the weather 
    and if I should bring an umbrella? Also, I'd like to see the temperature graph."""

    # Test with different formats
    formats = ["auto", "json", "react"]
    
    for format in formats:
        print("\n" + "=" * 70)
        print(f"TEST WITH FORMAT: {format}")
        print("=" * 70)
        
        print(f"User prompt: {prompt}")
        print(f"Processing with format={format}...\n")
        
        try:
            # Run the agent with the specified format
            response = run_agent(
                prompt=prompt,
                format=format,
                verbose=True,
                max_iterations=3
            )
            
            print(f"\nFinal response ({format} format):")
            print(response)
        except Exception as e:
            print(f"Error running agent with {format} format: {e}")
    
    print("\n" + "=" * 70)
    print("FORMAT DETECTION TEST")
    print("=" * 70)
    
    # Test with existing model (actual detection through API)
    print("Testing with model that exists on the server:")
    from hands_on_ai.agent.formats import detect_best_format
    
    actual_model = "llama3.2"
    detected_format = detect_best_format(actual_model)
    print(f"Model: {actual_model:<12} -> Detected format: {detected_format}")
    
    # Test with non-existent models (should fall back to default)
    print("\nTesting with models that don't exist on the server:")
    non_existent_models = ["llama3-70b", "gpt-4", "nonexistent-model"]
    
    for model in non_existent_models:
        detected_format = detect_best_format(model)
        print(f"Model: {model:<16} -> Detected format: {detected_format}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
