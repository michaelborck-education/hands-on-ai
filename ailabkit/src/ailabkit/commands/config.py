"""
Config command for the ailabkit CLI - view or edit configuration.
"""

import typer
from rich import print
import json
from .. import config

app = typer.Typer(help="View or edit configuration")


@app.callback(invoke_without_command=True)
def show_config():
    """View or edit configuration."""
    config.ensure_config_dir()
    
    if not config.CONFIG_PATH.exists():
        # Create initial config
        print(f"Creating new config at {config.CONFIG_PATH}")
        current_config = config.load_config()  # Will load defaults
        config.save_config(current_config)
    
    # Display current config
    with open(config.CONFIG_PATH, "r") as f:
        config_data = json.load(f)
    
    print("\n[bold]Current Configuration:[/bold]")
    for key, value in config_data.items():
        print(f"  • {key}: {value}")
    
    print("\nTo edit configuration, open:\n" + str(config.CONFIG_PATH))