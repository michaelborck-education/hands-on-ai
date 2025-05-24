#!/usr/bin/env python
"""
Debug script to show the exact prompt being sent to the LLM.
"""

import os
import sys

# Set environment variables for API access
os.environ['HANDS_ON_AI_SERVER'] = 'http://ollama.serveur.au'
os.environ['HANDS_ON_AI_MODEL'] = 'llama3.2'
os.environ['HANDS_ON_AI_API_KEY'] = 'student-api-key-123'

# Add patching for get_response to intercept the prompt
import requests
from unittest.mock import patch

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

def main():
    from hands_on_ai.agent import register_tool, list_tools
    from hands_on_ai.agent.core import _tools
    from improved_react_prompts import ENHANCED_SYSTEM_PROMPT, TOOL_DESCRIPTION_FORMAT
    import hands_on_ai.agent.prompts
    
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
    
    # Replace the system prompt with our enhanced version
    hands_on_ai.agent.prompts.SYSTEM_PROMPT = ENHANCED_SYSTEM_PROMPT
    hands_on_ai.agent.prompts.TOOL_DESCRIPTION_FORMAT = TOOL_DESCRIPTION_FORMAT
    
    # Setup prompt to test
    prompt = """I need to see the current temperature in New York. 
    Can you generate a temperature graph for New York and tell me if it's going to rain?"""
    
    # Mock the requests.post to intercept the API call
    original_post = requests.post
    
    def mock_post(url, **kwargs):
        if '/api/generate' in url:
            print("\n=== REQUEST TO LLM API ===")
            print("URL:", url)
            print("\n--- HEADERS ---")
            print(kwargs.get('headers', {}))
            
            json_data = kwargs.get('json', {})
            print("\n--- SYSTEM PROMPT ---")
            print(json_data.get('system', ''))
            
            print("\n--- USER PROMPT ---")
            print(json_data.get('prompt', ''))
            
            print("\n=== END OF REQUEST ===\n")
        
        # Call the original post method
        return original_post(url, **kwargs)
    
    # Apply the mock
    with patch('requests.post', side_effect=mock_post):
        print("\nInitiating agent with prompt:")
        print(f"User prompt: {prompt}")
        
        # Import and call run_agent with the hook in place
        from hands_on_ai.agent import run_agent
        try:
            response = run_agent(prompt, verbose=True, max_iterations=3)
            print("\nFinal response:")
            print(response)
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()