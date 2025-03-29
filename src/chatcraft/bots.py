# src/chatcraft/bots.py

import inspect
import chatcraft

def list_available_bots():
    """
    Discover available bot functions defined in chatcraft/__init__.py.
    Bots must accept a single 'prompt' argument and not be private.
    """
    bots = {}
    for name, obj in inspect.getmembers(chatcraft):
        if (
            callable(obj)
            and not name.startswith("_")
            and name.endswith("_bot")  # Optional: enforce _bot suffix
        ):
            sig = inspect.signature(obj)
            params = list(sig.parameters.values())
            if len(params) == 1 and params[0].name == "prompt":
                bots[name] = obj
    return bots

def get_bot(name):
    """Retrieve a specific bot by name."""
    return list_available_bots().get(name)

def get_bot_description(bot_func):
    """Get the first non-empty line of a bot's docstring."""
    if not bot_func.__doc__:
        return "No description."
    return next((line.strip() for line in bot_func.__doc__.splitlines() if line.strip()), "No description.")
