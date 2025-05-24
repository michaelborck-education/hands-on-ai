#!/usr/bin/env python
"""
Direct Model Utilities Test

This script tests the model utilities module directly through the Python API
rather than using the CLI commands. This is useful for testing and demonstration.
"""

import os
import sys
from rich import print
from rich.table import Table

# Add parent directory to path to allow importing the module directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_list_models():
    """Test listing all available models."""
    from hands_on_ai.models import list_models
    
    print("\n[bold cyan]Testing list_models()[/bold cyan]")
    print("This function returns a list of all available models from the server.")
    
    models = list_models()
    
    if not models:
        print("[yellow]No models found. Make sure Ollama is running.[/yellow]")
        return None
    
    # Create and display a table of models
    table = Table(title=f"Found {len(models)} Models")
    table.add_column("Name", style="cyan")
    table.add_column("Size", style="green")
    table.add_column("Modified", style="blue")
    
    for model in models:
        name = model.get("name", "Unknown")
        size_bytes = model.get("size", 0)
        size = format_size(size_bytes)
        modified = model.get("modified", "Unknown")
        
        table.add_row(name, size, modified)
    
    print(table)
    
    # Return first model for further tests
    return models[0]["name"] if models else None

def test_check_model_exists(model_name):
    """Test checking if a model exists."""
    from hands_on_ai.models import check_model_exists
    
    if not model_name:
        print("[yellow]No model name provided for existence check.[/yellow]")
        return
    
    print(f"\n[bold cyan]Testing check_model_exists('{model_name}')[/bold cyan]")
    print("This function checks if a specific model exists on the server.")
    
    exists = check_model_exists(model_name)
    
    if exists:
        print(f"[green]✓ Model '{model_name}' exists[/green]")
    else:
        print(f"[red]✗ Model '{model_name}' does not exist[/red]")
    
    # Also test a non-existent model
    fake_model = "this-model-does-not-exist-12345"
    fake_exists = check_model_exists(fake_model)
    
    if fake_exists:
        print(f"[yellow]? Model '{fake_model}' exists (unexpected)[/yellow]")
    else:
        print(f"[green]✓ Model '{fake_model}' correctly reported as non-existent[/green]")

def test_get_model_info(model_name):
    """Test getting detailed model information."""
    from hands_on_ai.models import get_model_info
    
    if not model_name:
        print("[yellow]No model name provided for model info test.[/yellow]")
        return
    
    print(f"\n[bold cyan]Testing get_model_info('{model_name}')[/bold cyan]")
    print("This function retrieves detailed information about a model.")
    
    model_info = get_model_info(model_name)
    
    if not model_info:
        print(f"[red]Could not retrieve information for model '{model_name}'[/red]")
        return
    
    # Print basic info
    print(f"[bold]Model Name:[/bold] {model_name}")
    
    # Display size if available
    if "size" in model_info:
        size = format_size(model_info["size"])
        print(f"[bold]Size:[/bold] {size}")
    
    # Display parameter count if available
    if "parameters" in model_info:
        params = model_info["parameters"]
        if "num_params" in params:
            param_count = format_params(params["num_params"])
            print(f"[bold]Parameters:[/bold] {param_count}")
        elif "parameter_count" in params:
            param_count = format_params(params["parameter_count"])
            print(f"[bold]Parameters:[/bold] {param_count}")
    
    # Display base model if available from modelfile
    if "modelfile" in model_info:
        modelfile = model_info["modelfile"]
        if "FROM" in modelfile:
            base_model = modelfile.split("FROM")[1].strip().split("\n")[0]
            print(f"[bold]Base Model:[/bold] {base_model}")

def test_model_capabilities(model_name):
    """Test model capability detection."""
    from hands_on_ai.models import get_model_capabilities, detect_best_format
    
    if not model_name:
        print("[yellow]No model name provided for capabilities test.[/yellow]")
        return
    
    print(f"\n[bold cyan]Testing get_model_capabilities('{model_name}')[/bold cyan]")
    print("This function detects what features a model supports.")
    
    capabilities = get_model_capabilities(model_name)
    
    # Create a table for the capabilities
    table = Table(title=f"Capabilities for {model_name}")
    table.add_column("Capability", style="cyan")
    table.add_column("Supported", style="green")
    
    for capability, supported in capabilities.items():
        icon = "✓" if supported else "✗"
        color = "green" if supported else "red"
        capability_name = capability.replace('_', ' ').title()
        table.add_row(capability_name, f"[{color}]{icon}[/{color}]")
    
    print(table)
    
    # Also test format detection
    print(f"\n[bold cyan]Testing detect_best_format('{model_name}')[/bold cyan]")
    print("This function determines the best format to use with the model.")
    
    format_type = detect_best_format(model_name)
    print(f"[bold]Best Format:[/bold] {format_type}")
    
    if format_type == "react":
        print("[green]This model can use the more advanced ReAct format for better reasoning.[/green]")
    else:
        print("[yellow]This model will use the simpler JSON format for better compatibility.[/yellow]")

def format_size(size_bytes):
    """Format size in bytes to a human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0 or unit == "TB":
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def format_params(params):
    """Format parameter count to a human-readable format."""
    if params >= 1_000_000_000:
        return f"{params / 1_000_000_000:.1f}B"
    elif params >= 1_000_000:
        return f"{params / 1_000_000:.1f}M"
    elif params >= 1_000:
        return f"{params / 1_000:.1f}K"
    return str(params)

def test_normalize_model_name():
    """Test model name normalization."""
    from hands_on_ai.models import normalize_model_name
    
    print("\n[bold cyan]Testing normalize_model_name()[/bold cyan]")
    print("This function normalizes model names to include the tag if missing.")
    
    test_names = [
        "llama3",
        "llama3:latest",
        "mistral:7b",
        "mpt-7b:v1.0",
    ]
    
    # Create a table for the results
    table = Table(title="Model Name Normalization")
    table.add_column("Original Name", style="cyan")
    table.add_column("Normalized Name", style="green")
    
    for name in test_names:
        normalized = normalize_model_name(name)
        table.add_row(name, normalized)
    
    print(table)

def main():
    """Run all the model utility tests."""
    print("\n[bold]DIRECT MODEL UTILITIES TEST[/bold]")
    print("=" * 60)
    print("This script tests the model utilities module directly via the Python API.")
    
    # Test listing models
    first_model = test_list_models()
    
    # Test model existence checking
    test_check_model_exists(first_model)
    
    # Test getting model info
    test_get_model_info(first_model)
    
    # Test model capabilities
    test_model_capabilities(first_model)
    
    # Test model name normalization
    test_normalize_model_name()
    
    print("\n[bold green]Testing Complete![/bold green]")

if __name__ == "__main__":
    main()