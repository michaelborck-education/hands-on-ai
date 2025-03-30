"""
Web command for the agent CLI - runs a web interface for the agent.
"""

import typer
from rich import print
from ..web import run_web_server

app = typer.Typer(help="Start web interface for the agent")

@app.callback(invoke_without_command=True)
def web(
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to"),
    port: int = typer.Option(8002, "--port", "-p", help="Port to bind to"),
):
    """
    Launch a web interface for the agent.
    """
    print(f"\n🌐 [bold]Starting Agent Web Interface[/bold] at http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")
    
    try:
        run_web_server(host=host, port=port)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Agent Web Interface.")
    except Exception as e:
        print(f"\n[red]❌ Error starting web server: {e}[/red]")
        raise typer.Exit(1)