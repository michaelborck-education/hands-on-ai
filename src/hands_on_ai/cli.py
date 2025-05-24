"""
Meta CLI for hands-on-ai - provides version, configuration and module listing.
"""

import typer
from .commands import version, list, doctor, config, models

app = typer.Typer(help="AI Learning Lab Toolkit")

# Add command modules
app.add_typer(version.app, name="version", help="Display version information")
app.add_typer(list.app, name="list", help="List available modules")
app.add_typer(doctor.app, name="doctor", help="Check environment and configuration")
app.add_typer(config.app, name="config", help="View or edit configuration")
app.add_typer(models.app, name="models", help="Manage and inspect LLM models")

# Add root command
@app.callback(invoke_without_command=True)
def root(ctx: typer.Context):
    """
    AI Learning Lab Toolkit - A modular toolkit for learning AI concepts.
    """
    # If no subcommand is provided, show list of modules
    if ctx.invoked_subcommand is None:
        list.list_modules()


if __name__ == "__main__":
    app()