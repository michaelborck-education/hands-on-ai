"""
Coder personality bot.
"""

from ...get_response import get_response

def coder_bot(prompt):
    """
    Give programming help with code examples and explanations.

    **Educational Uses:**
    - Debugging and code reviews
    - Code literacy and syntax help
    """
    return get_response(prompt, system="You are a skilled coding assistant who explains and writes code clearly and concisely.", personality="coder", model="codellama")