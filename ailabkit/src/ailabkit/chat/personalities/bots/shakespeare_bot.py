"""
Shakespeare personality bot.
"""

from ...get_response import get_response

def shakespeare_bot(prompt):
    """
    Generate responses in Shakespearean English and poetic tone.

    **Educational Uses:**
    - Literature and poetry study
    - Exploring language style
    """
    return get_response(prompt, system="You respond in the style of William Shakespeare.", personality="shakespeare")