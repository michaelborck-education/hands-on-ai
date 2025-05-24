#!/usr/bin/env python
"""
Debug script for the JSON agent to identify and fix parsing issues.
"""

import os
import json
import re

# Set environment variables for API access
os.environ['HANDS_ON_AI_SERVER'] = 'http://ollama.serveur.au'
os.environ['HANDS_ON_AI_MODEL'] = 'llama3.2'
os.environ['HANDS_ON_AI_API_KEY'] = 'student-api-key-123'

def weather_data(location):
    """Get weather data for a location."""
    print(f"Tool called: weather_data with input: {location}")
    return f"Weather data for {location}: Sunny, 25°C, humidity 60%, wind 5mph NE"

def temperature_graph(location):
    """Generate a temperature graph."""
    print(f"Tool called: temperature_graph with input: {location}")
    return f"Graph with temperature for {location} generated. Shows temperature range of 20-30°C."

def run_debug_agent():
    """
    Run a simplified agent that shows the JSON parsing process.
    """
    from hands_on_ai.chat import get_response
    
    # Define a simple system prompt
    system_prompt = """You are an intelligent agent that can analyze questions and call tools.

AVAILABLE TOOLS:
- weather_data: Get the weather for a location
- temperature_graph: Generate a graph with temperature

To call a tool, respond with VALID JSON in this format:
```json
{
  "thought": "Your reasoning about what tool to use",
  "tool": "tool_name",
  "input": "parameter for the tool"
}
```

If you don't need to call a tool, respond with:
```json
{
  "thought": "Your reasoning about the answer",
  "answer": "Your final answer to the user's question"
}
```

IMPORTANT: Your response MUST be valid JSON wrapped in ```json and ``` markers.
"""

    # Simple user question
    prompt = "What's the weather like in New York?"
    
    print("=== JSON AGENT DEBUG ===")
    print(f"Sending prompt: {prompt}")
    
    # Get response from LLM
    llm_response = get_response(
        prompt=prompt,
        system=system_prompt
    )
    
    print("\n=== RAW LLM RESPONSE ===")
    print(llm_response)
    
    # Try different JSON parsing approaches
    print("\n=== JSON PARSING ATTEMPTS ===")
    
    # Method 1: Extract code blocks
    print("\nMethod 1: Extract from code blocks")
    json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", llm_response, re.DOTALL)
    if json_match:
        json_text = json_match.group(1)
        print(f"Found JSON in code block: {json_text}")
        try:
            parsed_json = json.loads(json_text)
            print(f"Successfully parsed: {parsed_json}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
    else:
        print("No JSON code block found")
    
    # Method 2: Look for JSON objects
    print("\nMethod 2: Search for JSON-like objects")
    json_pattern = r"\s*({.*})\s*"
    object_match = re.search(json_pattern, llm_response, re.DOTALL)
    if object_match:
        json_text = object_match.group(1)
        print(f"Found JSON-like object: {json_text}")
        try:
            parsed_json = json.loads(json_text)
            print(f"Successfully parsed: {parsed_json}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
    else:
        print("No JSON-like object found")
    
    # Method 3: Try regex extraction of fields
    print("\nMethod 3: Extract fields with regex")
    thought_match = re.search(r'"?thought"?\s*:\s*"([^"]*)"', llm_response, re.IGNORECASE)
    tool_match = re.search(r'"?tool"?\s*:\s*"([^"]*)"', llm_response, re.IGNORECASE)
    input_match = re.search(r'"?input"?\s*:\s*"([^"]*)"', llm_response, re.IGNORECASE)
    answer_match = re.search(r'"?answer"?\s*:\s*"([^"]*)"', llm_response, re.IGNORECASE)
    
    result = {}
    if thought_match:
        result["thought"] = thought_match.group(1)
    if tool_match:
        result["tool"] = tool_match.group(1)
    if input_match:
        result["input"] = input_match.group(1)
    if answer_match:
        result["answer"] = answer_match.group(1)
    
    if result:
        print(f"Extracted fields with regex: {result}")
    else:
        print("No fields extracted with regex")
    
    # Method 4: Fix common JSON errors
    print("\nMethod 4: Try to fix common JSON errors")
    
    # Get full text to fix
    fix_text = llm_response
    if json_match:
        fix_text = json_match.group(1)
    elif object_match:
        fix_text = object_match.group(1)
    
    # Try to fix missing quotes around keys
    try:
        fixed_json = re.sub(r'(\s*)(\w+)(\s*):', r'\1"\2"\3:', fix_text)
        print(f"Fixed missing quotes: {fixed_json}")
        parsed_json = json.loads(fixed_json)
        print(f"Successfully parsed fixed JSON: {parsed_json}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse after fixing quotes: {e}")
    
    print("\n=== DEBUG COMPLETE ===")

if __name__ == "__main__":
    run_debug_agent()