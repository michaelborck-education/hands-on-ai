"""
Version command for the ailabkit CLI.
"""

import typer
from rich import print
from .. import __version__

app = typer.Typer(help="Display version information")


@app.callback(invoke_without_command=True)
def version():
    """Display version information."""
    print(f"ailabkit v{__version__}")
    print("AI Learning Lab Toolkit")