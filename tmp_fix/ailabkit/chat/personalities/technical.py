"""
Technical bot personalities for coding and specialized tasks.
"""

from .bots.coder_bot import coder_bot
# To implement:
# from .bots.hacker_bot import hacker_bot
# from .bots.caveman_bot import caveman_bot

# Placeholder implementations until all individual bots are created
from ..get_response import get_response

def hacker_bot(prompt):
    """
    Respond like a 90s hacker using tech slang and lingo.

    **Educational Uses:**
    - Cyber culture exploration
    - Technical storytelling
    """
    return get_response(prompt, system="You are a cool hacker who explains everything like you're in a 90s cyberpunk movie.", personality="hacker")


def caveman_bot(prompt):
    """
    Use primitive speech patterns for fun and simplicity.

    **Educational Uses:**
    - Language reduction and abstraction
    - Vocabulary awareness
    """
    return get_response(prompt, system="You talk like a caveman with limited vocabulary but great enthusiasm.", personality="caveman")

__all__ = ["coder_bot", "hacker_bot", "caveman_bot"]