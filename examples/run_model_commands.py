#!/usr/bin/env python
"""
Run Model Commands Directly

This script directly calls the functions in the models CLI command module
rather than using the command-line interface.
"""

import sys
import os
from rich.console import Console

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Run the model commands directly."""
    from hands_on_ai.commands.models import list_available_models, info, check
    
    console = Console()
    
    console.print("\n[bold]MODEL COMMANDS TEST[/bold]")
    console.print("=" * 60)
    console.print("This script runs the model commands directly via the Python API.\n")
    
    # Test list_available_models command
    console.print("[bold cyan]1. Testing list_available_models()[/bold cyan]")
    list_available_models()
    
    # Find an existing model to test with
    from hands_on_ai.models import list_models
    models = list_models()
    
    if models:
        first_model = models[0]["name"]
        
        # Test info command
        console.print(f"\n[bold cyan]2. Testing info('{first_model}')[/bold cyan]")
        info(first_model)
        
        # Test check command
        console.print(f"\n[bold cyan]3. Testing check('{first_model}')[/bold cyan]")
        check(first_model)
        
        # Test check with non-existent model
        console.print("\n[bold cyan]4. Testing check('nonexistent-model')[/bold cyan]")
        check("nonexistent-model")
    else:
        console.print("[yellow]No models found to test commands with.[/yellow]")
    
    console.print("\n[bold green]Testing Complete![/bold green]")

if __name__ == "__main__":
    main()