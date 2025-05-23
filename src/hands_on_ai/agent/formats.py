"""
Agent format handlers for different types of model responses.
"""

import re
import json
import requests
from typing import Dict, List, Callable, Any, Tuple
from ..config import get_server_url, get_api_key, log

# JSON prompt template
JSON_SYSTEM_PROMPT = """You are an intelligent agent that can analyze questions and call tools.

AVAILABLE TOOLS:
{tool_list}

To call a tool, respond with VALID JSON in this format:
```json
{{
  "thought": "Your reasoning about what tool to use",
  "tool": "tool_name",
  "input": "parameter for the tool"
}}
```

If you don't need to call a tool, or after you've gathered all necessary information, respond with:
```json
{{
  "thought": "Your reasoning about the answer",
  "answer": "Your final answer to the user's question"
}}
```

IMPORTANT: 
1. Your response MUST be valid JSON wrapped in ```json and ``` markers
2. Use ONLY the exact tool names provided above
3. Only call tools that are relevant to the user's question
4. Think step by step about what information you need to answer the question

EXAMPLE:
User: What's the weather like in Chicago and should I bring an umbrella?

Your response:
```json
{{
  "thought": "I need to check the current weather in Chicago",
  "tool": "weather_data",
  "input": "Chicago"
}}
```

After receiving tool results:
```json
{{
  "thought": "I should check if there's a chance of rain",
  "tool": "rain_chance_graph",
  "input": "Chicago"
}}
```

After receiving all needed information:
```json
{{
  "thought": "Now I have all the information I need",
  "answer": "The weather in Chicago is sunny and 25°C. There's only a 20% chance of rain, but you might want to bring a small umbrella just in case."
}}
```
"""

def normalize_model_name(model_name: str) -> str:
    """
    Normalize the model name to the format expected by Ollama.
    
    Args:
        model_name: Original model name
        
    Returns:
        str: Normalized model name
    """
    # If model name already has a tag (contains a colon), use it as is
    if ":" in model_name:
        return model_name
    
    # Otherwise append :latest tag
    return f"{model_name}:latest"

def detect_best_format(model_name: str) -> str:
    """
    Determine the best format for the given model based on API capabilities.
    
    Args:
        model_name: Name of the model
        
    Returns:
        str: "react" or "json" (default)
    """
    # Default format for safety
    DEFAULT_FORMAT = "json"
    
    try:
        server_url = get_server_url()
        
        # Try only two variations:
        # 1. The original name exactly as provided
        # 2. The normalized name with :latest appended (if needed)
        original_name = model_name
        normalized_name = normalize_model_name(model_name)
        
        model_variations = [original_name]
        if normalized_name != original_name:
            model_variations.append(normalized_name)
        
        # Prepare headers with API key if available
        headers = {}
        api_key = get_api_key()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            log.debug("Using API key for authentication")
        
        # Try each variation
        for model_variant in model_variations:
            log.debug(f"Checking model capabilities for: {model_variant}")
            
            # Call the Ollama API to check if the model exists and get its metadata
            response = requests.post(
                f"{server_url}/api/show",
                json={"name": model_variant},
                headers=headers,
                timeout=5
            )
            
            # If we found a matching model
            if response.status_code == 200:
                log.debug(f"Found model: {model_variant}")
                
                # Parse the model info
                model_info = response.json()
                
                # Check if model has parameters field
                if "parameters" in model_info:
                    # Extract parameters that might indicate model capability
                    parameters = model_info.get("parameters", {})
                    
                    # Look for model size info
                    model_size = 0
                    if "num_params" in parameters:
                        model_size = parameters["num_params"]
                    elif "parameter_count" in parameters:
                        model_size = parameters["parameter_count"]
                    
                    # Models with at least 30B parameters can likely handle ReAct format
                    if model_size >= 30_000_000_000:  # 30B or larger
                        log.debug(f"Model {model_variant} has {model_size} parameters, using ReAct format")
                        return "react"
                    
                    log.debug(f"Model {model_variant} has {model_size} parameters, using JSON format")
                
                # Also check template/system prompt for function calling capabilities
                template = model_info.get("template", "")
                if "function" in template.lower() or "tool" in template.lower():
                    log.debug(f"Model {model_variant} mentions functions/tools in template, using ReAct format")
                    return "react"
                
                # Fall back to name-based detection as a secondary method
                if _model_name_suggests_large_model(model_variant):
                    log.debug(f"Model name '{model_variant}' suggests a large model, using ReAct format")
                    return "react"
                
                # Default to JSON format for models we found but can't determine capabilities
                log.debug(f"Using JSON format for model {model_variant}")
                return DEFAULT_FORMAT
        
        # If API call fails, fall back to name-based detection
        model_format = _name_based_format_detection(model_name)
        if model_format != DEFAULT_FORMAT:
            return model_format
            
        # If we tried all variations and none worked, log a debug message
        model_list = ", ".join(model_variations)
        log.debug(f"Could not determine model capabilities. Tried: {model_list}. Using default format: {DEFAULT_FORMAT}")
        return DEFAULT_FORMAT
    
    except Exception as e:
        # If there's any error, fall back to name-based detection
        log.debug(f"Error accessing model API: {e}. Falling back to name-based detection.")
        return _name_based_format_detection(model_name)

def _model_name_suggests_large_model(model_name: str) -> bool:
    """Check if the model name suggests it's a large model based on patterns."""
    large_model_patterns = [
        "gpt-4", "gpt4", 
        "claude-2", "claude-3", "claude3",
        "llama3-70b", "llama-70b", 
        "mixtral-8x7b"
    ]
    
    return any(pattern.lower() in model_name.lower() for pattern in large_model_patterns)

def _name_based_format_detection(model_name: str) -> str:
    """Detect format based on model name patterns."""
    DEFAULT_FORMAT = "json"
    
    if _model_name_suggests_large_model(model_name):
        log.debug(f"Model name '{model_name}' suggests a large model, using ReAct format")
        return "react"
    
    log.debug(f"Using default JSON format for model {model_name}")
    return DEFAULT_FORMAT

def parse_json_response(text: str) -> Dict[str, Any]:
    """
    Parse a JSON response from the model.
    
    Args:
        text: Response text from the model
        
    Returns:
        Dict with parsed JSON data or error information
    """
    # Extract JSON from the response (if wrapped in code blocks)
    json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    
    if json_match:
        json_text = json_match.group(1)
    else:
        # Try to find anything that looks like JSON object (starts with { and ends with })
        json_pattern = r"\s*({.*})\s*"
        object_match = re.search(json_pattern, text, re.DOTALL)
        
        if object_match:
            json_text = object_match.group(1)
        else:
            # Fallback to using the whole text
            json_text = text
    
    try:
        # Parse the JSON response
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        log.warning(f"Failed to parse JSON from model response: {e}")
        
        # Try to fix common JSON errors
        try:
            # Try to fix missing quotes around keys
            fixed_json = re.sub(r'(\s*)(\w+)(\s*):', r'\1"\2"\3:', json_text)
            return json.loads(fixed_json)
        except json.JSONDecodeError:
            pass
            
        try:
            # Try to fix missing commas between elements
            fixed_json = re.sub(r'(\s*"\w+"\s*:\s*"[^"]*")\s*(")', r'\1,\2', json_text)
            return json.loads(fixed_json)
        except json.JSONDecodeError:
            pass
        
        # If all attempts fail, extract anything useful from the response
        # Look for thought patterns
        thought_match = re.search(r'"?thought"?\s*:\s*"([^"]*)"', text, re.IGNORECASE)
        answer_match = re.search(r'"?answer"?\s*:\s*"([^"]*)"', text, re.IGNORECASE)
        tool_match = re.search(r'"?tool"?\s*:\s*"([^"]*)"', text, re.IGNORECASE)
        input_match = re.search(r'"?input"?\s*:\s*"([^"]*)"', text, re.IGNORECASE)
        
        result = {"error": str(e)}
        
        if thought_match:
            result["thought"] = thought_match.group(1)
        if answer_match:
            result["answer"] = answer_match.group(1)
        if tool_match and input_match:
            result["tool"] = tool_match.group(1)
            result["input"] = input_match.group(1)
        
        # If we've extracted something useful, return it
        if len(result) > 1:
            log.info("Extracted partial JSON data using regex fallbacks")
            return result
            
        # Complete failure, return the error with the text
        return {"error": str(e), "text": text}

def format_tools_for_json_prompt(tools: Dict[str, Dict[str, Any]]) -> str:
    """
    Format tools list for inclusion in JSON prompt.
    
    Args:
        tools: Dictionary of tool information
        
    Returns:
        str: Formatted tool list for the prompt
    """
    if not tools:
        return "No tools are available."
    
    tool_texts = []
    for name, info in tools.items():
        tool_texts.append(f"- {name}: {info['description']}")
    
    return "\n".join(tool_texts)

def run_json_agent(
    prompt: str, 
    tools: Dict[str, Dict[str, Any]], 
    model: str = None,
    max_iterations: int = 5,
    verbose: bool = False
) -> str:
    """
    Run an agent that uses JSON for tool calling with smaller models.
    
    Args:
        prompt: User question
        tools: Dictionary of tools
        model: LLM model to use
        max_iterations: Maximum number of tool calls
        verbose: Whether to print intermediate steps
        
    Returns:
        str: Final agent response
    """
    from ..chat import get_response
    
    # Format the system prompt with tools
    system_prompt = JSON_SYSTEM_PROMPT.format(
        tool_list=format_tools_for_json_prompt(tools)
    )
    
    # Initialize conversation state
    conversation_history = [prompt]
    
    # Main agent loop
    for iteration in range(max_iterations):
        # Get the response from the LLM
        llm_response = get_response(
            prompt="\n".join(conversation_history),
            system=system_prompt,
            model=model
        )
        
        if verbose:
            log.info(f"LLM Response (iteration {iteration+1}):\n{llm_response}")
        
        # Parse the JSON response
        response_data = parse_json_response(llm_response)
        
        # Check if parsing failed completely
        if "error" in response_data and len(response_data) == 2 and "text" in response_data:
            # Completely failed to parse anything useful
            error_message = f"Error parsing response: {response_data['error']}"
            if verbose:
                log.warning(error_message)
            
            # Add the error to the conversation and ask for a proper JSON response
            conversation_history.append(
                error_message + "\nPlease provide a valid JSON response following the format in the instructions."
            )
            continue
        
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
                if verbose:
                    log.warning(error_message)
                conversation_history.append(error_message)
                continue
            
            # Call the tool
            try:
                tool_result = tools[tool_name]["function"](tool_input)
                if verbose:
                    log.info(f"Tool result: {tool_result}")
                
                # Add the tool result to the conversation
                conversation_history.append(f"Tool result: {tool_result}")
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {str(e)}"
                if verbose:
                    log.exception(f"Error executing tool {tool_name}")
                conversation_history.append(error_message)
        else:
            # No tool call or answer, see if we can extract something useful
            if "thought" in response_data:
                return f"No clear answer, but here's what I was thinking: {response_data['thought']}"
            else:
                # Try one more time with a clearer instruction
                conversation_history.append(
                    "I need a valid JSON response. Please provide either a tool call or a final answer."
                )
                continue
    
    # If we reach max iterations without a final answer
    return "I've reached the maximum number of steps without finding a complete answer."