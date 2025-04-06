"""
Bot personalities for the chat module.

You can import:
1. Individual bots directly: from hands_on_ai.chat.personalities.bots import friendly_bot
2. Categories of bots: from hands_on_ai.chat.personalities.creative import *
3. All bots (this module): from hands_on_ai.chat.personalities import *
"""

# Import individual bots for direct access
from .bots.friendly_bot import friendly_bot
from .bots.sarcastic_bot import sarcastic_bot
from .bots.pirate_bot import pirate_bot
from .bots.shakespeare_bot import shakespeare_bot
from .bots.teacher_bot import teacher_bot
from .bots.coder_bot import coder_bot

# Import from categories for the rest (placeholders until individual files created)
from .creative import alien_bot, emoji_bot
from .educational import coach_bot, grumpy_professor_bot
from .technical import hacker_bot, caveman_bot
from .therapeutic import therapist_bot

# Export all bots
__all__ = [
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