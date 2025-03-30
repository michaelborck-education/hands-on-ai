"""
Pirate personality bot.
"""

from ...get_response import get_response

def pirate_bot(prompt):
    """
    Respond like a witty pirate using nautical slang and playful tone.

    **Educational Uses:**
    - Creative writing
    - Reframing problem-solving
    """
    return get_response(prompt, system="You are a witty pirate. Talk like a pirate from the 1700s.", personality="parrot")