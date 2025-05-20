"""
hands_on_ai: Your Hands-on AI Toolkit

A modular toolkit for learning AI concepts through hands-on experimentation.
"""

__version__ = "0.1.10"

# Import core modules
from . import chat
from . import rag
from . import agent

# Make modules available at top level
__all__ = [
    "chat",
    "rag", 
    "agent"
]