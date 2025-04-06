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
    public: bool = typer.Option(False, "--public", help="Make the interface accessible from other devices (binds to 0.0.0.0)"),
):
    """
    Launch a web interface for the agent.
    """
    # Override host if public flag is set
    if public:
        host = "0.0.0.0"
        print("\n⚠️ [yellow]PUBLIC MODE:[/yellow] Interface will be accessible from other devices on your network.")
    
    # Display appropriate URL
    display_host = "localhost" if host == "127.0.0.1" else host
    print(f"\n🌐 [bold]Starting Agent Web Interface[/bold] at http://{display_host}:{port}")
    print("Press Ctrl+C to stop the server.")
    
    try:
        run_web_server(host=host, port=port)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Agent Web Interface.")
    except Exception as e:
        print(f"\n[red]❌ Error starting web server: {e}[/red]")
        raise typer.Exit(1)