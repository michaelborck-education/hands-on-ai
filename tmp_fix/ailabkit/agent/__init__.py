"""
Agent module - ReAct-style reasoning with tool use.
"""

from .core import run_agent, register_tool, list_tools
# Import from tools.py directly instead of tools/ directory
from .tools.calculator import register_calculator_tool
from .tools.weather import register_weather_tool
from .tools.search import register_search_tool
from .agents import calculator, dictionary, converter

# Core agent functions
__all__ = [
    "run_agent",
    "register_tool",
    "list_tools",
    "register_calculator_tool",
    "register_weather_tool",
    "register_search_tool",
    "calculator",
    "dictionary",
    "converter"
]