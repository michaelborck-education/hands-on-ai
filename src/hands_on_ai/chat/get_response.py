"""
Core response functionality for the chat module.
"""

import requests
import random
import time
from openai import OpenAI
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

    # Get server URL and configure OpenAI client
    server_url = get_server_url()
    
    # Add /v1 suffix for OpenAI-compatible endpoints
    if not server_url.endswith('/v1'):
        server_url = server_url.rstrip('/') + '/v1'
    
    log.debug(f"Using OpenAI-compatible server URL: {server_url}")

    # Try to get a response
    for attempt in range(1, retries + 1):
        try:
            # Create OpenAI client
            client = OpenAI(
                base_url=server_url,
                api_key=get_api_key() or "hands-on-ai"
            )
            
            # Make OpenAI-compatible request
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                stream=stream,
                timeout=10
            )
            
            # Handle streaming vs non-streaming response
            if stream:
                # For streaming, collect all chunks
                content = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content += chunk.choices[0].delta.content
                return content if content else "⚠️ No response from model."
            else:
                # For non-streaming, get the content directly
                return response.choices[0].message.content or "⚠️ No response from model."
                
        except Exception as e:
            log.warning(f"Error during request (attempt {attempt}): {e}")
            if attempt < retries:
                fallback = _fallbacks.get(personality, _fallbacks.get("default", ["Retrying..."]))
                msg = random.choice(fallback)
                print(msg)
                time.sleep(1.0)
            else:
                return f"❌ Error: {str(e)}"