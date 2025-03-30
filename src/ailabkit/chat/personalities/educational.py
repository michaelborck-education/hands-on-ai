"""
Educational bot personalities for teaching and learning.
"""

from .bots.teacher_bot import teacher_bot
# To implement:
# from .bots.coach_bot import coach_bot
# from .bots.grumpy_professor_bot import grumpy_professor_bot

# Placeholder implementations until all individual bots are created
from ..get_response import get_response

def coach_bot(prompt):
    """
    Motivate and encourage like a personal coach.

    **Educational Uses:**
    - Confidence building
    - Encouraging self-direction
    """
    return get_response(prompt, system="You are an enthusiastic motivational coach who encourages and supports students.", personality="coach")


def grumpy_professor_bot(prompt):
    """
    Respond with brilliance and mild academic impatience.

    **Educational Uses:**
    - Humorous contrast
    - Critical thinking prompts
    """
    return get_response(prompt, system="You are a grumpy but brilliant professor. You're annoyed by simple questions but still explain things correctly, often with a sarcastic tone.", personality="grumpy")

__all__ = ["teacher_bot", "coach_bot", "grumpy_professor_bot"]