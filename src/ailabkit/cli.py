"""
Meta CLI for ailabkit - provides version, configuration and module listing.
"""

import typer
from .commands import version, list, doctor, config

app = typer.Typer(help="AI Learning Lab Toolkit")

# Add command modules
app.add_typer(version.app, name="version", help="Display version information")
app.add_typer(list.app, name="list", help="List available modules")
app.add_typer(doctor.app, name="doctor", help="Check environment and configuration")
app.add_typer(config.app, name="config", help="View or edit configuration")

# Add root command
@app.callback(invoke_without_command=True)
def root():
    """
    AI Learning Lab Toolkit - A modular toolkit for learning AI concepts.
    """
    # If no subcommand is provided, show list of modules
    typer.run(list.list_modules)


if __name__ == "__main__":
    app()