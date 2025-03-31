"""
Teacher personality bot.
"""

from ...get_response import get_response

def teacher_bot(prompt):
    """
    Generate structured explanations like a calm teacher.

    **Educational Uses:**
    - Step-by-step tutorials
    - Clarifying concepts
    """
    return get_response(prompt, system="You are a calm and clear teacher. You explain concepts step by step.", personality="teacher")