"""
Interactive command for the agent CLI - provides a REPL interface.
"""

import typer
from rich import print
from rich.panel import Panel
from rich.console import Console
from ..core import run_agent
from ...config import get_model

app = typer.Typer(help="Run interactive agent chat")


@app.callback(invoke_without_command=True)
def interactive(
    model: str = typer.Option(None, help="LLM model to use (default: from config)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """Run interactive agent chat."""
    # Register tools if not already done
    from ..tools import register_simple_tools
    register_simple_tools()
    
    console = Console()
    
    # Get model from config if not specified
    if model is None:
        model = get_model()
    
    print("\n🤖 [bold]Agent Interactive Mode[/bold] - Ask questions using AI tools")
    print("Type 'exit' to quit.\n")
    
    if verbose:
        from .tools import list_available_tools
        list_available_tools()
        console.print()
    
    while True:
        try:
            user_input = input("💬 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Exiting Agent Interactive Mode.")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        
        # Run the agent
        try:
            response = run_agent(user_input, model=model)
            console.print(Panel(response, title="Agent", border_style="green"))
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")