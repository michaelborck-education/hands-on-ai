#!/usr/bin/env python
"""
Test script for the agent functionality in hands-on-ai.
This example demonstrates how the agent calls tools with different formats.
"""

import os

# Set environment variables for API access
os.environ['HANDS_ON_AI_SERVER'] = 'http://localhost:11434'  # Default Ollama server
os.environ['HANDS_ON_AI_MODEL'] = 'llama3'     # Default model
os.environ['HANDS_ON_AI_LOG'] = 'debug'        # Enable debug logging

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

def custom_run_agent(prompt):
    """
    A custom run_agent function that bypasses the LLM and directly calls tools.
    This demonstrates the expected tool calling behavior.
    """
    from hands_on_ai.agent.core import _tools
    
    print("\n--- Direct Tool Execution Demo ---")
    print("This shows what should happen when tools are called correctly:")
    
    # For our test, let's decide which tools to call based on the prompt
    if "temperature" in prompt.lower():
        tool_name = "temperature_graph"
        tool_input = "New York"
        print(f"Calling: {tool_name} with input: {tool_input}")
        result = _tools[tool_name]["function"](tool_input)
        print(f"Tool result: {result}")
    
    if "rain" in prompt.lower() or "umbrella" in prompt.lower():
        tool_name = "rain_chance_graph" 
        tool_input = "New York"
        print(f"Calling: {tool_name} with input: {tool_input}")
        result = _tools[tool_name]["function"](tool_input)
        print(f"Tool result: {result}")
    
    # Return a sample final answer
    return "Here's the information about New York weather based on the tools I used."

def main():
    from hands_on_ai.agent import run_agent, register_tool, list_tools
    from hands_on_ai.agent.core import _tools
    from hands_on_ai.models import check_model_exists, detect_best_format, get_model_capabilities
    from hands_on_ai.config import get_model
    
    # Clear any existing tools to start fresh
    _tools.clear()

    # Register tools
    register_tool("weather_data", "Get the weather for a location", weather_data)
    register_tool("temperature_graph", "Generate a graph with temperature", temperature_graph)
    register_tool("precipitation_graph", "Generate a graph with precipitation", precipitation_graph)
    register_tool("rain_chance_graph", "Generate a graph with chance of rain", rain_chance_graph)
    
    # Print header
    print("=" * 70)
    print("ENHANCED AGENT TEST")
    print("=" * 70)
    print("This test demonstrates the improved agent that works with smaller models.")
    print("The agent now supports both ReAct and JSON formats, with automatic detection.")
    
    # Check model availability
    model = get_model()
    if not check_model_exists(model):
        print(f"\nWARNING: Default model '{model}' not found. Please ensure it's available.")
    else:
        print(f"\nUsing model: {model}")
        format = detect_best_format(model)
        capabilities = get_model_capabilities(model)
        print(f"Detected format: {format}")
        print("Model capabilities:")
        for capability, supported in capabilities.items():
            print(f"  • {capability}: {'✓' if supported else '✗'}")
    
    # List available tools
    print("\nAvailable tools:")
    tools = list_tools()
    for tool in tools:
        print(f"- {tool['name']}: {tool['description']}")
    
    # Test with both formats
    formats = ["json", "auto"]
    
    for format in formats:
        print("\n" + "=" * 70)
        print(f"RUNNING AGENT WITH FORMAT: {format}")
        print("=" * 70)
        
        # Test with a prompt that should make the agent call tools
        prompt = """I'm going to New York tomorrow. Can you tell me the weather 
        and if I should pack an umbrella? Also, I'd like to see a temperature graph."""
    
        print(f"User prompt: {prompt}")
        print(f"Processing with format={format}...")
        
        try:
            # Run the agent with the format
            response = run_agent(
                prompt=prompt, 
                format=format,
                verbose=True, 
                max_iterations=3
            )
            
            print(f"\nFinal response ({format}):")
            print(response)
        except Exception as e:
            print(f"Error: {e}")
    
    # Show the direct tool execution for comparison
    custom_response = custom_run_agent(prompt)
    print("\nFinal response from direct tool execution:")
    print(custom_response)

if __name__ == "__main__":
    main()