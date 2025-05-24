#!/usr/bin/env python
"""
Weather Graph Agent Example

This script demonstrates how to use the hands-on-ai agent module to create
an agent that can decide between fetching weather data or generating different
types of weather graphs based on a conversation.
"""

def get_weather_data(location="current location"):
    """Get weather data for a location."""
    return f"Weather data for {location}: Sunny, 25°C, humidity 60%, wind 5mph NE"

def generate_temperature_graph(location="current location"):
    """Generate a temperature graph for a location."""
    return f"Graph with temperature data for {location} generated. Shows temperature range of 20-30°C."

def generate_precipitation_graph(location="current location"):
    """Generate a precipitation graph for a location."""
    return f"Graph with precipitation data for {location} generated. Shows 5mm rainfall expected."

def generate_rain_chance_graph(location="current location"):
    """Generate a graph showing chance of rain for a location."""
    return f"Graph with chance of rain for {location} generated. Shows 20% chance of rain."

def main():
    from hands_on_ai.agent import run_agent, register_tool, list_tools
    
    # Clear any existing tools to start fresh
    from hands_on_ai.agent.core import _tools
    _tools.clear()
    
    # Register our weather tools
    register_tool(
        "get_weather_data", 
        "Get current weather data for a location", 
        get_weather_data
    )
    
    register_tool(
        "generate_temperature_graph", 
        "Generate a graph showing temperature data for a location", 
        generate_temperature_graph
    )
    
    register_tool(
        "generate_precipitation_graph", 
        "Generate a graph showing precipitation data for a location", 
        generate_precipitation_graph
    )
    
    register_tool(
        "generate_rain_chance_graph", 
        "Generate a graph showing chance of rain for a location", 
        generate_rain_chance_graph
    )
    
    # List available tools
    print("Available tools:")
    tools = list_tools()
    for tool in tools:
        print(f"- {tool['name']}: {tool['description']}")
    
    # Example 1: User wants a temperature graph
    print("\n--- Example 1: User wants a temperature graph ---")
    conversation1 = """
    WeatherWise: Would you like to see the current weather or a weather graph?
    User: I'd like to see a temperature graph please.
    """
    
    prompt1 = f"Based on the following conversation, decide whether the user wants current weather data or to generate one of the weather graphs:\n\n{conversation1}"
    
    print(f"Prompt: {prompt1}")
    print("Processing...")
    
    try:
        response1 = run_agent(prompt1, verbose=True, max_iterations=3)
        print(f"\nFinal response: {response1}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Example 2: User wants current weather data
    print("\n--- Example 2: User wants current weather data ---")
    conversation2 = """
    WeatherWise: Would you like to see the current weather or a weather graph?
    User: Just give me the current weather for now.
    """
    
    prompt2 = f"Based on the following conversation, decide whether the user wants current weather data or to generate one of the weather graphs:\n\n{conversation2}"
    
    print(f"Prompt: {prompt2}")
    print("Processing...")
    
    try:
        response2 = run_agent(prompt2, verbose=True, max_iterations=3)
        print(f"\nFinal response: {response2}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Example 3: User wants precipitation data
    print("\n--- Example 3: User wants precipitation data ---")
    conversation3 = """
    WeatherWise: What kind of weather information would you like today?
    User: Is it going to rain? Can you show me precipitation data?
    """
    
    prompt3 = f"Based on the following conversation, decide whether the user wants current weather data or to generate one of the weather graphs:\n\n{conversation3}"
    
    print(f"Prompt: {prompt3}")
    print("Processing...")
    
    try:
        response3 = run_agent(prompt3, verbose=True, max_iterations=3)
        print(f"\nFinal response: {response3}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
