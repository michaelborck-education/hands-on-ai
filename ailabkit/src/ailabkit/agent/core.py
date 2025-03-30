"""
Core agent functionality for ReAct-style reasoning and tool use.
"""

import re
import json
from typing import Dict, List, Callable, Any
from ..config import get_model, log
from ..chat import get_response

# Global tool registry
_tools: Dict[str, Callable] = {}

# ReAct prompts
AGENT_SYSTEM_PROMPT = """You are a helpful AI assistant with access to tools. 
Follow these steps for using tools:

1. THINK: Analyze what the user is asking
2. PLAN: Decide if you need a tool to help answer
3. ACT: Call a tool using this exact format:
   ```tool
   {
     "tool": "tool_name",
     "input": {"param1": "value1", "param2": "value2"}
   }
   ```
4. OBSERVE: Review the tool's response
5. RESPOND: Answer the user's question using the tool's output when appropriate

Available tools: {tool_list}

If you don't need any tools, just respond directly.
Always be helpful, accurate, and concise.
"""


def register_tool(name: str, description: str, function: Callable):
    """
    Register a tool with the agent.
    
    Args:
        name: Tool name
        description: Tool description
        function: Tool function
    """
    _tools[name] = {
        "name": name,
        "description": description,
        "function": function
    }
    log.debug(f"Registered tool: {name}")


def list_tools():
    """
    List all registered tools.
    
    Returns:
        list: List of tool information dictionaries
    """
    return [
        {"name": info["name"], "description": info["description"]}
        for info in _tools.values()
    ]


def _format_tools_for_prompt():
    """Format tools list for inclusion in prompt."""
    if not _tools:
        return "No tools are available."
    
    tool_texts = []
    for name, info in _tools.items():
        tool_texts.append(f"- {name}: {info['description']}")
    
    return "\n".join(tool_texts)


def _parse_tool_calls(text: str):
    """Parse tool calls from text using regex."""
    pattern = r"```tool\s+({.*?})\s+```"
    matches = re.findall(pattern, text, re.DOTALL)
    
    tool_calls = []
    for match in matches:
        try:
            tool_data = json.loads(match)
            if "tool" in tool_data and "input" in tool_data:
                tool_calls.append(tool_data)
        except json.JSONDecodeError:
            log.warning(f"Failed to parse tool call: {match}")
    
    return tool_calls


def _execute_tool_call(tool_call):
    """Execute a parsed tool call."""
    tool_name = tool_call["tool"]
    tool_input = tool_call["input"]
    
    if tool_name not in _tools:
        return f"Error: Tool '{tool_name}' not found."
    
    try:
        result = _tools[tool_name]["function"](**tool_input)
        return result
    except Exception as e:
        log.exception(f"Error executing tool {tool_name}")
        return f"Error executing tool '{tool_name}': {str(e)}"


def run_agent(prompt, model=None, max_iterations=5):
    """
    Run the agent with the given prompt.
    
    Args:
        prompt: User prompt
        model: LLM model to use
        max_iterations: Maximum number of tool use iterations
        
    Returns:
        str: Agent response
    """
    # Prepare system prompt with tools
    system_prompt = AGENT_SYSTEM_PROMPT.format(
        tool_list=_format_tools_for_prompt()
    )
    
    # Initial response
    if model is None:
        model = get_model()
    
    conversation = [
        {"role": "user", "content": prompt}
    ]
    
    for _ in range(max_iterations):
        # Get model response
        response_text = get_response(
            prompt=json.dumps([msg["content"] for msg in conversation]),
            system=system_prompt,
            model=model
        )
        
        # Check for tool calls
        tool_calls = _parse_tool_calls(response_text)
        
        if not tool_calls:
            # No tools used, we're done
            return response_text
        
        # Execute tools and add to conversation
        for tool_call in tool_calls:
            tool_result = _execute_tool_call(tool_call)
            
            # Add the response and tool result to the conversation
            conversation.append({"role": "assistant", "content": response_text})
            conversation.append({
                "role": "tool", 
                "content": f"Tool result for {tool_call['tool']}:\n{tool_result}"
            })
    
    # If we reach max iterations, return the last response
    return "I've reached the maximum number of tool calls without finding a complete answer."