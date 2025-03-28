import os
import json
from pathlib import Path
import importlib.resources


def load_fallbacks():
    """
    Load fallback personality messages from user, local, or default locations.

    Priority:
    1. ~/.chatcraft/fallbacks.json
    2. ./chatcraft/data/fallbacks.local.json
    3. packaged fallback (chatcraft/data/fallbacks.json)

    Returns:
        dict: fallback personality responses
    """
    user_file = Path.home() / ".chatcraft" / "fallbacks.json"
    local_file = Path("chatcraft/data/fallbacks.local.json")

    if user_file.exists():
        with user_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    elif local_file.exists():
        with local_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    else:
        with importlib.resources.open_text("chatcraft.data", "fallbacks.json") as f:
            return json.load(f)