"""
List command for the hands-on-ai CLI.
"""

import typer
from rich import print

app = typer.Typer(help="List available modules")


@app.callback(invoke_without_command=True)
def list_modules():
    """List available modules and their CLIs."""
    print("\n🧠 [bold]hands-on-ai[/bold]: AI Learning Lab Toolkit\n\n")
    print("[bold cyan]Available Modules:[/bold cyan]")
    print("  • [bold]chat[/bold] - Simple chatbot with system prompts")
    print("    Usage: [cyan]chat --help[/cyan]")
    print("  • [bold]rag[/bold] - Retrieval-Augmented Generation")
    print("    Usage: [cyan]rag --help[/cyan]")
    print("  • [bold]agent[/bold] - ReAct-style reasoning with tool use")
    print("    Usage: [cyan]agent --help[/cyan]")