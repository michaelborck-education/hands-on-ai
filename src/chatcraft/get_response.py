import requests
import random
import time
from chatcraft.config import get_server_url, load_fallbacks, log

_last_model: str | None = None  # global cache
_fallbacks = load_fallbacks()


def get_response(
    prompt: str,
    model: str = "llama3",
    system: str = "You are a helpful assistant.",
    personality: str = "friendly",
    stream: bool = False,
    retries: int = 2
) -> str:
    """
    Send a prompt to the Ollama API and retrieve the model's response.

    This function manages the connection to a local Ollama server, sends the user's
    prompt along with system instructions, and handles retries and warm-up if needed.

    Args:
        prompt (str): The text prompt to send to the model
        model (str): LLM model to use (e.g., "llama3", "codellama")
        system (str): System message defining bot behavior
        personality (str): Used for fallback character during retries
        stream (bool): Whether to request streaming output (default False)
        retries (int): Number of times to retry on error

    Returns:
        str: AI response or error message
    """
    global _last_model

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

    if not prompt.strip():
        return "⚠️ Empty prompt."

    url = get_server_url()
    log.debug(f"Using server URL: {url}")

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(
                f"{url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "system": system,
                    "stream": stream
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "⚠️ No response from model.")
        except Exception as e:
            log.warning(f"Error during request (attempt {attempt}): {e}")
            if attempt < retries:
                fallback = _fallbacks.get(personality, ["Retrying..."])
                msg = random.choice(fallback)
                print(msg)
                time.sleep(1.0)
            else:
                return f"❌ Error: {str(e)}"
