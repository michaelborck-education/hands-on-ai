"""
Therapeutic bot personalities for support and reflection.
"""

# To implement:
# from .bots.therapist_bot import therapist_bot

# Placeholder implementation until individual bot is created
from ..get_response import get_response

def therapist_bot(prompt):
    """
    Provide empathetic and reflective support.

    **Educational Uses:**
    - Mental health awareness
    - Roleplaying and support
    """
    return get_response(prompt, system="You are a calm, empathetic therapist who asks reflective questions and offers support without judgment.", personality="therapist")

__all__ = ["therapist_bot"]