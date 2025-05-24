#!/usr/bin/env python
"""
Model Capabilities Test

This script tests the model utilities module, specifically focusing on:
1. Listing available models
2. Detecting model capabilities
3. Testing model format compatibility

It provides a comprehensive test of the new centralized model utilities.
"""

import os
import sys
import time
from rich import print
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.panel import Panel

# Add parent directory to path to allow importing the module directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_model_listing():
    """Test the model listing functionality."""
    from hands_on_ai.models import list_models
    
    console = Console()
    
    with console.status("[bold green]Fetching available models...", spinner="dots"):
        models = list_models()
    
    if not models:
        console.print(Panel("[yellow]No models found.[/yellow] Make sure Ollama is running.", 
                     title="Model Listing Test", border_style="red"))
        return None
    
    # Create a table for the models
    table = Table(title=f"[bold]{len(models)} Models Available[/bold]")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Size", style="green")
    table.add_column("Modified", style="blue")
    
    # Add models to the table
    for model in models:
        name = model.get("name", "Unknown")
        size = format_size(model.get("size", 0))
        modified = model.get("modified", "Unknown")
        
        table.add_row(name, size, modified)
    
    console.print(table)
    
    # Return the first model for further testing
    return models[0]["name"] if models else None

def test_model_capabilities(model_name):
    """Test the model capabilities detection."""
    from hands_on_ai.models import get_model_capabilities, detect_best_format, normalize_model_name
    
    if not model_name:
        print("[yellow]No model available for capability testing.[/yellow]")
        return
    
    print(f"\n[bold]Testing Capabilities for Model:[/bold] {model_name}")
    
    # Normalize the model name
    normalized_name = normalize_model_name(model_name)
    print(f"Normalized name: {normalized_name}")
    
    # Get model capabilities
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Analyzing model capabilities..."),
        transient=True,
    ) as progress:
        progress.add_task("analyzing", total=None)
        capabilities = get_model_capabilities(model_name)
        time.sleep(1)  # Just to show the spinner
    
    # Create a table for capabilities
    table = Table(title=f"[bold]Capabilities for {model_name}[/bold]")
    table.add_column("Capability", style="cyan")
    table.add_column("Supported", style="green")
    
    for capability, supported in capabilities.items():
        icon = "✓" if supported else "✗"
        color = "green" if supported else "red"
        capability_name = capability.replace('_', ' ').title()
        table.add_row(capability_name, f"[{color}]{icon}[/{color}]")
    
    print(table)
    
    # Show the best format
    best_format = detect_best_format(model_name)
    print(f"\n[bold]Recommended Format:[/bold] {best_format}")
    
    return capabilities

def test_model_matrix():
    """Test different model names against the capability detection."""
    from hands_on_ai.models import get_model_capabilities, detect_best_format
    
    # List of test models (these don't need to exist)
    test_models = [
        "llama3",
        "llama3:latest",
        "llama3-70b",
        "gpt-4",
        "mistral-7b",
        "mixtral-8x7b",
        "claude-3-haiku",
        "llava",
        "phi3"
    ]
    
    print("\n[bold]Model Compatibility Matrix[/bold]")
    print("This shows format detection based on model name patterns\n")
    
    # Create a table for the matrix
    table = Table(title="Model Format Detection")
    table.add_column("Model", style="cyan")
    table.add_column("Best Format", style="green")
    table.add_column("Function Calling", style="yellow")
    table.add_column("Vision", style="magenta")
    
    for model in test_models:
        capabilities = get_model_capabilities(model)
        format_type = detect_best_format(model)
        
        function_icon = "✓" if capabilities["function_calling"] else "✗"
        function_color = "green" if capabilities["function_calling"] else "red"
        
        vision_icon = "✓" if capabilities["vision"] else "✗"
        vision_color = "green" if capabilities["vision"] else "red"
        
        table.add_row(
            model, 
            format_type,
            f"[{function_color}]{function_icon}[/{function_color}]",
            f"[{vision_color}]{vision_icon}[/{vision_color}]"
        )
    
    print(table)

def format_size(size_bytes):
    """Format size in bytes to a human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0 or unit == "TB":
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def main():
    """Run all the model capability tests."""
    print("\n[bold]MODEL CAPABILITIES TEST[/bold]")
    print("=" * 60)
    print("This script tests the model utilities module with a focus on capabilities detection.\n")
    
    # Test 1: List available models
    print("[bold cyan]Test 1: Model Listing[/bold cyan]")
    first_model = test_model_listing()
    
    # Test 2: Test capabilities of an actual model
    print("\n[bold cyan]Test 2: Model Capabilities Detection[/bold cyan]")
    test_model_capabilities(first_model)
    
    # Test 3: Test format detection matrix
    print("\n[bold cyan]Test 3: Model Format Detection Matrix[/bold cyan]")
    test_model_matrix()
    
    print("\n[bold green]Testing Complete![/bold green]")

if __name__ == "__main__":
    main()