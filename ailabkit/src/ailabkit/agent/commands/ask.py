"""
Ask command for the agent CLI - runs an agent with tools.
"""

import typer
from rich import print
from rich.panel import Panel
from rich.console import Console
from ..core import run_agent, list_tools
from ...config import get_model

app = typer.Typer(help="Ask a question using agent tools")


@app.callback(invoke_without_command=True)
def ask(
    prompt: str = typer.Argument(..., help="Question or instruction for the agent"),
    model: str = typer.Option(None, help="LLM model to use (default: from config)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """Ask a question or give an instruction to the agent."""
    # Register tools if not already done
    from ..tools import register_calculator_tool, register_weather_tool, register_search_tool
    register_calculator_tool()
    register_weather_tool()
    register_search_tool()
    
    console = Console()
    
    # Show available tools
    if verbose:
        console.print("[bold]Available tools:[/bold]")
        for tool in list_tools():
            console.print(f"- [cyan]{tool['name']}[/cyan]: {tool['description']}")
        console.print()
    
    # Get model from config if not specified
    if model is None:
        model = get_model()
    
    # Run the agent
    console.print(f"🤖 [bold]Running agent with prompt:[/bold] {prompt}")
    
    try:
        response = run_agent(prompt, model=model)
        console.print(Panel(response, title="Agent Response", border_style="green"))
    except Exception as e:
        console.print(f"[red]❌ Error running agent: {e}[/red]")
        raise typer.Exit(1)