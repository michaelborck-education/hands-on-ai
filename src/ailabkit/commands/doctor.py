"""
Doctor command for the ailabkit CLI - checks environment and configuration.
"""

import typer
from rich import print
import requests
from .. import config

app = typer.Typer(help="Check environment and configuration")


@app.callback(invoke_without_command=True)
def doctor():
    """Check environment and configuration."""
    print("\n🩺 [bold]ailabkit[/bold] environment check\n")

    # Check configuration
    server_url = config.get_server_url()
    model = config.get_model()
    embedding_model = config.get_embedding_model()
    
    print("[bold]Configuration[/bold]")
    print(f"  • Config file: {config.CONFIG_PATH}")
    print(f"  • Server URL: {server_url}")
    print(f"  • Default model: {model}")
    print(f"  • Embedding model: {embedding_model}")
    
    # Check server connectivity
    try:
        r = requests.get(f"{server_url}/api/tags", timeout=5)
        if r.status_code == 200:
            print("\n✅ Ollama server is reachable")
        else:
            print(f"\n❌ Ollama server returned status code {r.status_code}")
    except Exception as e:
        print(f"\n❌ Could not connect to Ollama server: {e}")