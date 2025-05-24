#!/usr/bin/env python
"""
Enhanced test script for the agent functionality with improved ReAct prompts.
This example demonstrates how to make the agent properly call tools.
"""

def weather_data(location):
    """Get weather data for a location."""
    print(f"Tool called: weather_data with input: {location}")
    return f"Weather data for {location}: Sunny, 25°C, humidity 60%, wind 5mph NE"

def temperature_graph(location):
    """Generate a temperature graph."""
    print(f"Tool called: temperature_graph with input: {location}")
    return f"Graph with temperature for {location} generated. Shows temperature range of 20-30°C."

def precipitation_graph(location):
    """Generate a precipitation graph."""
    print(f"Tool called: precipitation_graph with input: {location}")
    return f"Graph with precipitation for {location} generated. Shows 5mm rainfall expected."

def rain_chance_graph(location):
    """Generate a graph showing chance of rain."""
    print(f"Tool called: rain_chance_graph with input: {location}")
    return f"Graph with chance of rain for {location} generated. Shows 20% chance of rain."

def enhanced_run_agent(prompt, model=None, max_iterations=5, verbose=False):
    """
    Enhanced run_agent function that uses improved prompts with examples.
    """
    from hands_on_ai.agent.core import run_agent
    from improved_react_prompts import ENHANCED_SYSTEM_PROMPT, TOOL_DESCRIPTION_FORMAT
    from hands_on_ai.agent.core import _format_tools_for_prompt, _tools
    
    # Replace the system prompt with our enhanced version
    import hands_on_ai.agent.prompts
    original_system_prompt = hands_on_ai.agent.prompts.SYSTEM_PROMPT
    original_tool_description_format = hands_on_ai.agent.prompts.TOOL_DESCRIPTION_FORMAT
    
    try:
        # Temporarily replace the prompts
        hands_on_ai.agent.prompts.SYSTEM_PROMPT = ENHANCED_SYSTEM_PROMPT
        hands_on_ai.agent.prompts.TOOL_DESCRIPTION_FORMAT = TOOL_DESCRIPTION_FORMAT
        
        # Run the agent with the enhanced prompts
        return run_agent(prompt, model=model, max_iterations=max_iterations, verbose=verbose)
    finally:
        # Restore the original prompts
        hands_on_ai.agent.prompts.SYSTEM_PROMPT = original_system_prompt
        hands_on_ai.agent.prompts.TOOL_DESCRIPTION_FORMAT = original_tool_description_format

def main():
    from hands_on_ai.agent import register_tool, list_tools
    from hands_on_ai.agent.core import _tools
    
    # Clear any existing tools to start fresh
    _tools.clear()

    # Register tools
    register_tool("weather_data", "Get the weather for a location", weather_data)
    register_tool("temperature_graph", "Generate a graph with temperature", temperature_graph)
    register_tool("precipitation_graph", "Generate a graph with precipitation", precipitation_graph)
    register_tool("rain_chance_graph", "Generate a graph with chance of rain", rain_chance_graph)
    
    # List available tools
    print("Available tools:")
    tools = list_tools()
    for tool in tools:
        print(f"- {tool['name']}: {tool['description']}")
    
    print("\nRunning agent test with enhanced ReAct prompts...")
    
    # Test with a prompt that should make the agent call a tool
    prompt = """I need to see the current temperature in New York. 
    Can you generate a temperature graph for New York and tell me if it's going to rain?"""

    print(f"User prompt: {prompt}")
    print("Processing...")
    
    # Run with the enhanced prompts
    response = enhanced_run_agent(prompt, verbose=True, max_iterations=3)
    
    print("\nFinal response:")
    print(response)
    
    print("\nNote: If the LLM still doesn't use the proper ReAct format with tools,")
    print("you may need to try a different model or implement a function calling API.")

if __name__ == "__main__":
    main()
