#!/usr/bin/env python
"""
Test the model CLI commands

This script demonstrates how to use the hands-on-ai CLI commands 
for listing and inspecting models.

For this script to work, you need to have installed the package in 
development mode using:
    uv pip install -e .
    or
    pip install -e .

This will make the 'handsonai' command available in your environment.
"""

import os
import sys
import subprocess
from rich import print
from rich.panel import Panel

# Add parent directory to path to allow importing the module directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_cli_command(command):
    """Run a CLI command and capture the output."""
    print(f"[bold blue]Running command:[/bold blue] {command}")
    print("-" * 60)
    
    # Run the command and capture output
    try:
        # Split the command string into parts
        cmd_parts = command.split()
        result = subprocess.run(cmd_parts, capture_output=True, text=True)
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        
        # Print any errors
        if result.stderr:
            print(f"[red]Error:[/red] {result.stderr}")
            
        # Return the result
        return result.returncode == 0
        
    except Exception as e:
        print(f"[red]Exception running command:[/red] {e}")
        return False

def test_cli_commands():
    """Test various model CLI commands."""
    commands = [
        # List models
        "handsonai models",
        
        # Check doctor functionality
        "handsonai doctor",
        
        # Check a specific model
        "handsonai models check llama3",
        
        # Try with a non-existent model
        "handsonai models check nonexistent-model",
    ]
    
    # Find first available model to test info command
    try:
        from hands_on_ai.models import list_models
        models = list_models()
        if models:
            first_model = models[0]["name"]
            commands.append(f"handsonai models info {first_model}")
    except Exception:
        pass
    
    # Run each command
    for i, command in enumerate(commands, 1):
        print(f"\n[bold green]Test {i}/{len(commands)}[/bold green]")
        success = run_cli_command(command)
        
        if not success:
            print(f"[yellow]Command returned non-zero exit code: {command}[/yellow]")
        
        # Add a separator between commands
        if i < len(commands):
            print("\n" + "=" * 60)
    
    print(Panel("CLI command testing complete", border_style="green"))

def main():
    """Run the CLI command tests."""
    print("\n[bold]MODEL CLI COMMANDS TEST[/bold]")
    print("=" * 60)
    print("This script tests the Hands-On AI CLI commands for model management.\n")
    
    # Run the CLI command tests
    test_cli_commands()

if __name__ == "__main__":
    main()