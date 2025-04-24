"""
Template for creating new personalities.

Copy this file, rename it, and customize to add your own personality.
"""

from ..get_response import get_response

def example_bot(prompt):
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

1. Create a copy of this file with a descriptive name
2. Create your bot function (must end with _bot)
3. Write a clear docstring with educational uses
4. Set appropriate system prompt and personality
5. Add your bot to __init__.py: 
   - Import it in the appropriate section
   - Add to __all__ list
6. OPTIONAL: Add fallback messages for your personality in 
   hands_on_ai/src/hands_on_ai/chat/data/fallbacks.json

Submit a pull request with your changes!
"""