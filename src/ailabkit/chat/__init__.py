"""
Chat module - Simple chatbot with system prompts.
"""

from .get_response import get_response
from .personalities import (
    friendly_bot,
    sarcastic_bot,
    pirate_bot,
    shakespeare_bot,
    teacher_bot,
    coach_bot,
    caveman_bot,
    hacker_bot,
    therapist_bot,
    grumpy_professor_bot,
    alien_bot,
    emoji_bot,
    coder_bot
)

# 🧠 Core interface
__all__ = [
    "get_response",
    "friendly_bot",
    "sarcastic_bot",
    "pirate_bot",
    "shakespeare_bot",
    "teacher_bot",
    "coach_bot",
    "caveman_bot",
    "hacker_bot",
    "therapist_bot",
    "grumpy_professor_bot",
    "alien_bot",
    "emoji_bot",
    "coder_bot"
]