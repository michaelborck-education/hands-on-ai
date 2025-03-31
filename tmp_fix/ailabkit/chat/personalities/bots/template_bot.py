"""
Template for creating a new bot personality.

Copy this file to a new file named <your_bot_name>_bot.py.
"""

from ...get_response import get_response

def template_bot(prompt):
    """
    Short description of what this bot does.

    **Educational Uses:**
    - Use case 1
    - Use case 2
    """
    return get_response(
        prompt,
        system="You are an example bot. Describe your personality here.",
        personality="default"  # Match with fallbacks.json entry if possible
    )


"""
INSTRUCTIONS FOR CONTRIBUTING A NEW PERSONALITY:

1. Create a copy of this file with a descriptive name (must end with _bot.py)
2. Update the bot function name (must match filename and end with _bot)
3. Write a clear docstring with educational uses
4. Set appropriate system prompt and personality
5. If creating a new category of bots:
   - Add a new category file in the personalities directory
   - Import your bot in that file
   - Add your category to __init__.py
6. If adding to an existing category:
   - Add your bot to the appropriate category file
7. Update personalities/__init__.py to import your bot
8. OPTIONAL: Add fallback messages for your personality in 
   chat/data/fallbacks.json

Submit a pull request with your changes!
"""