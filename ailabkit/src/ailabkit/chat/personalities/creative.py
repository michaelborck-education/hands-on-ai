"""
Creative bot personalities for artistic and expressive communication.
"""

from .bots.pirate_bot import pirate_bot
from .bots.shakespeare_bot import shakespeare_bot
# To implement:
# from .bots.alien_bot import alien_bot
# from .bots.emoji_bot import emoji_bot

# Placeholder implementations until all individual bots are created
from ..get_response import get_response

def alien_bot(prompt):
    """
    Speak as an intelligent alien discovering humanity.

    **Educational Uses:**
    - Cultural studies
    - Writing prompts
    """
    return get_response(prompt, system="You are a highly intelligent space alien trying to understand human culture. Your speech is slightly odd but curious and wise.", personality="alien")


def emoji_bot(prompt):
    """
    Communicate primarily using expressive emojis.

    **Educational Uses:**
    - Symbolism and interpretation
    - Digital communication
    """
    return get_response(prompt, system="You respond using mostly emojis, mixing minimal words and symbols to convey meaning. You love using expressive emoji strings.", personality="emoji")

__all__ = ["pirate_bot", "shakespeare_bot", "alien_bot", "emoji_bot"]