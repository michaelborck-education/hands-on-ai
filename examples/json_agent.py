#!/usr/bin/env python
"""
JSON-based Agent: A simplified agent pattern for smaller models
that uses structured JSON output for more reliable tool calling.
"""

# Define our tool functions
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

def run_json_agent(user_question, max_iterations=3):
    """
    Run an agent that uses JSON for tool calling with smaller models.
    
    Args:
        user_question: The question from the user
        max_iterations: Maximum number of tool calls
        
    Returns:
        Final answer from the agent
    """
    from hands_on_ai.chat import get_response
    
    # Register our tools in a dictionary
    tools = {
        "weather_data": {
            "name": "weather_data",
            "description": "Get the weather for a location",
            "function": weather_data
        },
        "temperature_graph": {
            "name": "temperature_graph",
            "description": "Generate a graph with temperature",
            "function": temperature_graph
        },
        "precipitation_graph": {
            "name": "precipitation_graph",
            "description": "Generate a graph with precipitation",
            "function": precipitation_graph
        },
        "rain_chance_graph": {
            "name": "rain_chance_graph",
            "description": "Generate a graph with chance of rain",
            "function": rain_chance_graph
        }
    }
    
    # Construct the system prompt with JSON format instructions
    system_prompt = """You are an intelligent agent that can analyze questions and call tools.

AVAILABLE TOOLS:
"""
    
    # Add tool descriptions
    for tool in tools.values():
        system_prompt += f"- {tool['name']}: {tool['description']}\n"
    
    system_prompt += """
To call a tool, respond with VALID JSON in this format:
```json
{
  "thought": "Your reasoning about what tool to use",
  "tool": "tool_name",
  "input": "location or other input parameter"
}
```

If you don't need to call a tool, or after you've gathered all necessary information, respond with:
```json
{
  "thought": "Your reasoning about the answer",
  "answer": "Your final answer to the user's question"
}
```

IMPORTANT: 
1. Your response MUST be valid JSON wrapped in ```json and ``` markers
2. Use ONLY the exact tool names provided above
3. Each tool takes a location parameter (like "New York")
4. Only call tools that are relevant to the user's question

EXAMPLE:
User: What's the weather like in Chicago and should I bring an umbrella?

Your response:
```json
{
  "thought": "I need to check the current weather in Chicago",
  "tool": "weather_data",
  "input": "Chicago"
}
```

After receiving weather data:
```json
{
  "thought": "I should check if there's a chance of rain",
  "tool": "rain_chance_graph",
  "input": "Chicago"
}
```

After receiving rain chance data:
```json
{
  "thought": "Now I have all the information I need",
  "answer": "The weather in Chicago is sunny and 25°C. There's only a 20% chance of rain, but you might want to bring a small umbrella just in case."
}
```
"""
    
    # Initialize conversation state
    conversation_history = [user_question]
    
    # Main agent loop
    for iteration in range(max_iterations):
        # Get the response from the LLM
        llm_response = get_response(
            prompt="\n".join(conversation_history),
            system=system_prompt
        )
        
        print(f"\nLLM Response (iteration {iteration+1}):")
        print(llm_response)
        
        # Extract JSON from the response
        json_match = re.search(r"```json\s*(.*?)\s*```", llm_response, re.DOTALL)
        
        if not json_match:
            print("Warning: No JSON found in the response. Using the full response.")
            json_text = llm_response
        else:
            json_text = json_match.group(1)
        
        try:
            # Parse the JSON response
            response_data = json.loads(json_text)
            
            # Check if we have a final answer
            if "answer" in response_data:
                return response_data["answer"]
            
            # Check if we need to call a tool
            if "tool" in response_data and "input" in response_data:
                tool_name = response_data["tool"]
                tool_input = response_data["input"]
                
                # Check if the tool exists
                if tool_name not in tools:
                    error_message = f"Error: Tool '{tool_name}' not found. Available tools: {', '.join(tools.keys())}"
                    print(error_message)
                    conversation_history.append(error_message)
                    continue
                
                # Call the tool
                tool_result = tools[tool_name]["function"](tool_input)
                print(f"Tool result: {tool_result}")
                
                # Add the tool result to the conversation
                conversation_history.append(f"Tool result: {tool_result}")
            else:
                # No tool call, treat as final answer
                if "thought" in response_data:
                    return response_data.get("thought", "No final answer provided.")
                else:
                    return "No final answer or tool call found in the response."
                
        except json.JSONDecodeError as e:
            error_message = f"Error: Failed to parse JSON response: {e}"
            print(error_message)
            conversation_history.append(error_message)
    
    # If we reach max iterations without a final answer
    return "Reached maximum number of iterations without a final answer."

def main():
    # Introduction
    print("=== JSON-based Agent Demo ===")
    print("This approach uses structured JSON output for more reliable tool calling with smaller models.\n")
    
    # List available tools
    print("Available tools:")
    print("- weather_data: Get the weather for a location")
    print("- temperature_graph: Generate a graph with temperature")
    print("- precipitation_graph: Generate a graph with precipitation")
    print("- rain_chance_graph: Generate a graph with chance of rain")
    
    # User question
    user_question = """I need to see the current temperature in New York. 
    Can you generate a temperature graph for New York and tell me if it's going to rain?"""
    
    print("\nUser question:")
    print(user_question)
    print("\nProcessing...")
    
    # Run the JSON agent
    final_answer = run_json_agent(user_question)
    
    print("\nFinal answer:")
    print(final_answer)

if __name__ == "__main__":
    main()
