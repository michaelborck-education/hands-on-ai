"""
Doctor command for the chat CLI.
"""

import typer
from rich import print
import requests
from ...config import get_server_url

app = typer.Typer(help="Run diagnostics")


@app.callback(invoke_without_command=True)
def doctor():
    """Run diagnostics to check Ollama server and model availability."""
    print("🩺 Running Chat environment check...\n")
    
    url = get_server_url()
    print(f"Server URL: {url}")
    
    try:
        r = requests.get(f"{url}/api/tags", timeout=2)
        if r.status_code == 200:
            print("✅ Ollama server is reachable.")
            
            # List available models
            try:
                models = r.json()
                if "models" in models:
                    print("\nAvailable models:")
                    for model in models["models"]:
                        print(f"  • {model['name']}")
            except Exception:
                print("[yellow]⚠️ Could not retrieve model list.[/yellow]")
                
        else:
            print(f"[red]❌ Ollama server returned status code {r.status_code}.[/red]")
    except Exception as e:
        print(f"[red]❌ Ollama server not reachable. Make sure it's running on {url}.[/red]")
        print(f"[red]  Error: {e}[/red]")
        raise typer.Exit(1)