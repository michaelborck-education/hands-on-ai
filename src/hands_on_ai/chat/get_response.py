"""
Core response functionality for the chat module.
"""

import requests
import random
import time
from ..config import get_server_url, get_api_key, load_fallbacks, log

# Global model cache
_last_model: str | None = None
# Load fallbacks from the chat module
_fallbacks = load_fallbacks(module="chat")


def get_response(
    prompt: str,
    model: str = None,
    system: str = "You are a helpful assistant.",
    personality: str = "friendly",
    stream: bool = False,
    retries: int = 2
) -> str:
    """
    Send a prompt to the LLM and retrieve the model's response.

    This function manages the connection to a local Ollama server, sends the user's
    prompt along with system instructions, and handles retries and warm-up if needed.

    Args:
        prompt (str): The text prompt to send to the model
        model (str): LLM model to use (defaults to config setting)
        system (str): System message defining bot behavior
        personality (str): Used for fallback character during retries
        stream (bool): Whether to request streaming output (default False)
        retries (int): Number of times to retry on error

    Returns:
        str: AI response or error message
    """
    global _last_model
    
    # Get model from config if not specified
    if model is None:
        from ..config import get_model
        model = get_model()

    # Handle model switching
    if model != _last_model:
        warmups = [
            f"🧠 Loading model '{model}' into RAM... give me a sec...",
            f"💾 Spinning up the AI core for '{model}'...",
            f"⏳ Summoning the knowledge spirits... '{model}' booting...",
            f"🤖 Thinking really hard with '{model}'...",
            f"⚙️ Switching to model: {model} ... (may take a few seconds)"
        ]
        msg = random.choice(warmups)
        print(msg)
        log.debug(f"Model switch: {msg}")
        time.sleep(1.2)
        _last_model = model

    # Check for empty prompt
    if not prompt.strip():
        return "⚠️ Empty prompt."

    # Get server URL from config
    url = get_server_url()
    log.debug(f"Using server URL: {url}")

    # Try to get a response
    for attempt in range(1, retries + 1):
        try:
            # Prepare headers with API key if available
            headers = {}
            api_key = get_api_key()
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
                log.debug("Using API key for authentication")
            
            response = requests.post(
                f"{url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "system": system,
                    "stream": stream
                },
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "⚠️ No response from model.")
        except Exception as e:
            log.warning(f"Error during request (attempt {attempt}): {e}")
            if attempt < retries:
                fallback = _fallbacks.get(personality, _fallbacks.get("default", ["Retrying..."]))
                msg = random.choice(fallback)
                print(msg)
                time.sleep(1.0)
            else:
                return f"❌ Error: {str(e)}"