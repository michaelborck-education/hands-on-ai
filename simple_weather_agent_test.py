#!/usr/bin/env python
"""
Simple Weather Agent Test

This is a fixed version of the original code to test the agent functionality.
"""

import os

# Set environment variables for API access
os.environ['HANDS_ON_AI_SERVER'] = 'http://ollama.serveur.au'
os.environ['HANDS_ON_AI_MODEL'] = 'granite3.2'
os.environ['HANDS_ON_AI_API_KEY'] = 'student-api-key-123'

def the_main_one():
    return "Weather data for your location."

def graph2():
    return "Graph with temperature generated."

def graph3():
    return "Graph with precipitation generated."

def graph4():
    return "Graph with chance of rain generated."

def main():
    from hands_on_ai.agent import run_agent, register_tool

    # Clear any existing tools to start fresh
    from hands_on_ai.agent.core import _tools
    _tools.clear()

    # Register our tools
    register_tool("the_main_one", "get the weather for that location", the_main_one)
    register_tool("graph2", "generate a graph with temperature", graph2)
    register_tool("graph3", "generate a graph with precipitation", graph3)
    register_tool("graph4", "generate a graph with chance of rain", graph4)

    # Run the agent with the original prompt
    prompt = "Based on the below conversation decide whether the user wants to get weather data or generate one of the 3 graphs \n\nWeatherWise: would you like a graph with temperature? You: yes"
    
    try:
        response = run_agent(prompt, verbose=True)
        print(f"\nFinal response: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()