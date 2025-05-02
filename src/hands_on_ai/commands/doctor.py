"""
Doctor command for the hands-on-ai CLI - checks environment and configuration.
"""

import typer
from rich import print
import requests
from .. import config

app = typer.Typer(help="Check environment and configuration")


@app.callback(invoke_without_command=True)
def doctor():
    """Check environment and configuration."""
    print("\n🩺 [bold]hands-on-ai[/bold] environment check\n")

    # Check configuration
    server_url = config.get_server_url()
    model = config.get_model()
    embedding_model = config.get_embedding_model()
    api_key = config.get_api_key()
    
    print("[bold]Configuration[/bold]")
    print(f"  • Config file: {config.CONFIG_PATH}")
    print(f"  • Server URL: {server_url}")
    print(f"  • Default model: {model}")
    print(f"  • Embedding model: {embedding_model}")
    if api_key:
        masked_key = f"{api_key[:4]}{'*' * (len(api_key) - 8)}{api_key[-4:]}" if len(api_key) > 8 else "****"
        print(f"  • API key: {masked_key} (configured)")
    else:
        print(f"  • API key: Not configured")
    
    # Check server connectivity
    try:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        r = requests.get(f"{server_url}/api/tags", headers=headers, timeout=5)
        if r.status_code == 200:
            print("\n✅ Ollama server is reachable")
        else:
            print(f"\n❌ Ollama server returned status code {r.status_code}")
    except Exception as e:
        print(f"\n❌ Could not connect to Ollama server: {e}")