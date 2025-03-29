# chatcraft/config.py - Load fallback messages and server settings

import json
import logging
import os
from pathlib import Path
from importlib.resources import files
import importlib.resources


DEFAULT_SERVER = "http://localhost:11434"
DEFAULT_FALLBACKS = {"friendly": ["Retrying..."]}
CONFIG_PATH = Path.home() / ".chatcraft" / "config.json"

log = logging.getLogger("chatcraft")
log.setLevel(logging.WARNING)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
log.addHandler(handler)

if os.environ.get("CHATCRAFT_LOG") == "debug":
    log.setLevel(logging.DEBUG)


def load_fallbacks():
    """
    Load fallback personality messages from user, local, or default locations.

    Priority:
    1. ~/.chatcraft/fallbacks.json
    2. ./chatcraft/data/fallbacks.local.json
    3. packaged fallback (chatcraft/data/fallbacks.json)
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


def get_server_url():
    # Priority: env > config file > default
    if "CHATCRAFT_SERVER" in os.environ:
        return os.environ["CHATCRAFT_SERVER"]
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                cfg = json.load(f)
                return cfg.get("server", DEFAULT_SERVER)
        except Exception as e:
            log.warning(f"Failed to read config.json: {e}")
    return DEFAULT_SERVER
