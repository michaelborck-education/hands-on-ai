"""
Bot personality discovery and retrieval.
"""

import inspect
from . import personalities


def list_available_bots():
    """
    Discover available bot functions defined in personalities module.
    Bots must accept a single 'prompt' argument and not be private.
    
    Returns:
        dict: Dictionary of bot names and functions
    """
    bots = {}
    for name, obj in inspect.getmembers(personalities):
        if (
            callable(obj)
            and not name.startswith("_")
            and name.endswith("_bot")  # Enforce _bot suffix
        ):
            sig = inspect.signature(obj)
            params = list(sig.parameters.values())
            if len(params) == 1 and params[0].name == "prompt":
                bots[name] = obj
    return bots


def get_bot(name):
    """
    Retrieve a specific bot by name.
    
    Args:
        name (str): Bot name
        
    Returns:
        function: Bot function or None if not found
    """
    return list_available_bots().get(name)


def get_bot_description(bot_func):
    """
    Get the first non-empty line of a bot's docstring.
    
    Args:
        bot_func (function): Bot function
        
    Returns:
        str: Bot description
    """
    if not bot_func.__doc__:
        return "No description."
    return next((line.strip() for line in bot_func.__doc__.splitlines() if line.strip()), "No description.")