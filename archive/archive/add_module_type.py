#!/usr/bin/env python3
"""
Add module type (chat, rag, agent) metadata to all mini-project files.

This script scans markdown files in the docs/projects directory and adds a
module type field after the difficulty and time fields.
"""

import os
import re
from pathlib import Path

# Define the projects directory
PROJECTS_DIR = Path("docs/projects")

def add_module_type(file_path, module_type="chat"):
    """Add module type to a markdown file if it doesn't already have it."""
    print(f"Processing {file_path}...")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if module type is already present
    if re.search(r'\*\*Module\*\*:', content):
        print(f"  Module type already exists in {file_path}")
        return False
    
    # Find the position to insert the module type
    # Look for the Learning Focus line which comes after Difficulty and Time
    match = re.search(r'(\*\*Learning Focus\*\*:.*?)(\n+)', content, re.DOTALL)
    
    if match:
        # Insert the module type line after Learning Focus
        insert_position = match.end(1)
        new_content = (
            content[:insert_position] + 
            f"  \n**Module**: {module_type}" +
            content[insert_position:]
        )
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  Added module type '{module_type}' to {file_path}")
        return True
    else:
        print(f"  Could not find insertion point in {file_path}")
        return False

def main():
    """Add module type to all mini-project files."""
    # Ensure the directory exists
    if not PROJECTS_DIR.exists():
        print(f"Error: Directory '{PROJECTS_DIR}' not found.")
        return
    
    # Get all markdown files
    project_files = list(PROJECTS_DIR.glob('*.md'))
    
    if not project_files:
        print(f"No markdown files found in {PROJECTS_DIR}")
        return
    
    # Process each file
    updated_count = 0
    
    for file_path in project_files:
        # Right now all existing projects are chat-based
        # You can customize this logic to determine different module types
        if add_module_type(file_path, "chat"):
            updated_count += 1
    
    print(f"\nDone! Added module type to {updated_count} of {len(project_files)} project files.")

if __name__ == "__main__":
    main()