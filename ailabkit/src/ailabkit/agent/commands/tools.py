"""
Tools command for the agent CLI - lists available tools.
"""

import typer
from rich import print
from rich.table import Table
from rich.console import Console
from ..core import list_tools

app = typer.Typer(help="List available agent tools")


@app.callback(invoke_without_command=True)
def list_available_tools():
    """List all available agent tools."""
    # Register tools if not already done
    from ..tools import register_calculator_tool, register_weather_tool, register_search_tool
    register_calculator_tool()
    register_weather_tool()
    register_search_tool()
    
    console = Console()
    
    # Create a table for tools
    table = Table(title="Available Agent Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Description")
    
    # Add tools to the table
    tools = list_tools()
    if not tools:
        console.print("[yellow]No tools are currently registered.[/yellow]")
        return
    
    for tool in tools:
        table.add_row(tool["name"], tool["description"])
    
    console.print(table)