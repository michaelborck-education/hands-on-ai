"""
Friendly assistant bot.
"""

from ...get_response import get_response

def friendly_bot(prompt):
    """
    Generate a friendly and helpful response to the given prompt.

    **Educational Uses:**
    - General question answering
    - Student support
    - Introductory AI interactions
    """
    return get_response(prompt, system="You are a friendly and helpful assistant.", personality="friendly")