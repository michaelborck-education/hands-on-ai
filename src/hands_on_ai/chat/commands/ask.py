"""
Ask command for the chat CLI.
"""

import typer
from rich import print
from ..bots import get_bot

app = typer.Typer(help="Send a single prompt to a bot")


@app.callback(invoke_without_command=True)
def ask(
    prompt: str = typer.Argument(..., help="Prompt to send to the chatbot."),
    personality: str = typer.Option("friendly_bot", help="Bot personality to use")
):
    """Send a single prompt to a bot."""
    bot = get_bot(personality)
    if not bot:
        print(f"[red]❌ Bot '{personality}' not found. Try 'chat bots' for options.[/red]")
        raise typer.Exit(1)
    print(bot(prompt))