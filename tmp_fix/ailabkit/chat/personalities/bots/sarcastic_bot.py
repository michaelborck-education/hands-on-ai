"""
Sarcastic assistant bot.
"""

from ...get_response import get_response

def sarcastic_bot(prompt):
    """
    Generate a sarcastic response with dry humor to the given prompt.

    **Educational Uses:**
    - Humor-based feedback
    - Personality contrast exercises
    """
    return get_response(prompt, system="You are a sarcastic assistant who always responds with dry humor.", personality="sarcastic")