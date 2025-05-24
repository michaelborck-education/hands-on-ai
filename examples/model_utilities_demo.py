#!/usr/bin/env python
"""
Model Utilities Demo for Hands-On AI

This script demonstrates the new centralized model utilities module
that provides functionality for working with LLM models.
"""

import os
import sys
from rich import print
from rich.table import Table

# Add parent directory to path to allow importing the module directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Demonstrate the model utilities functionality."""
    from hands_on_ai.models import (
        list_models, 
        check_model_exists, 
        get_model_info, 
        get_model_capabilities, 
        detect_best_format,
        normalize_model_name
    )
    
    print("\n[bold]MODEL UTILITIES DEMO[/bold]")
    print("=" * 60)
    print("This script demonstrates the new centralized model utilities module.\n")
    
    # List all available models
    print("[bold cyan]Available Models:[/bold cyan]")
    models = list_models()
    
    if not models:
        print("[yellow]No models found.[/yellow] Make sure Ollama is running.")
        return
    
    # Create a table for models
    table = Table()
    table.add_column("Name", style="cyan")
    table.add_column("Size", style="green")
    table.add_column("Best Format", style="magenta")
    
    for model in models[:5]:  # Limit to first 5 models
        name = model.get("name", "Unknown")
        size = format_size(model.get("size", 0))
        
        # Detect best format for model
        format_type = detect_best_format(name)
        
        table.add_row(name, size, format_type)
    
    print(table)
    
    # Select a model to demonstrate detailed capabilities
    if models:
        demo_model = models[0]["name"]
        print(f"\n[bold cyan]Detailed Capabilities for {demo_model}:[/bold cyan]")
        
        # Demonstrate normalization
        normalized = normalize_model_name(demo_model)
        print(f"Normalized name: {normalized}")
        
        # Get model capabilities
        capabilities = get_model_capabilities(demo_model)
        
        # Print capabilities
        for capability, supported in capabilities.items():
            icon = "✓" if supported else "✗"
            color = "green" if supported else "red"
            print(f"[{color}]{icon}[/{color}] {capability.replace('_', ' ').title()}")
        
        # Get and print model info 
        model_info = get_model_info(demo_model)
        if model_info and "parameters" in model_info:
            params = model_info["parameters"]
            if "num_params" in params:
                print(f"Parameter count: {format_params(params['num_params'])}")
            elif "parameter_count" in params:
                print(f"Parameter count: {format_params(params['parameter_count'])}")

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

if __name__ == "__main__":
    main()
