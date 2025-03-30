#!/usr/bin/env python3
"""
Update mini-project code examples to use the new ailabkit.chat module
instead of the old chatcraft module.

This script scans all the markdown files in the docs/projects directory
and updates import statements and other references to the chatcraft module.
"""

import os
import re

# Define the projects directory
PROJECTS_DIR = "docs/projects"

# Define replacement patterns
REPLACEMENTS = [
    # Standard import replacements
    (r'from chatcraft import get_response', r'from ailabkit.chat import get_response'),
    (r'from chatcraft import (\w+)', r'from ailabkit.chat import \1'),
    (r'from chatcraft\.(\w+) import', r'from ailabkit.chat.\1 import'),
    (r'import chatcraft', r'import ailabkit.chat'),
    
    # Function call replacements (with proper indentation preserved)
    (r'(\s+)chatcraft\.', r'\1ailabkit.chat.'),
    
    # Advanced pattern for directly referenced modules
    (r'chatcraft\.([\w\.]+)', r'ailabkit.chat.\1'),
    
    # Handle specific cases for personalities
    (r'from chatcraft\.personalities', r'from ailabkit.chat.personalities'),
    
    # Update CLI commands in code or examples
    (r'chatcraft interactive', r'ailabkit chat interactive'),
    (r'chatcraft ask', r'ailabkit chat ask'),
]

def update_file(file_path):
    """Update a single markdown file with the new module references."""
    print(f"Processing {file_path}...")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply all replacements
    original_content = content
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    
    # Check if content was modified
    if content != original_content:
        # Write back to the file if changes were made
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated {file_path}")
        return True
    else:
        print(f"  No changes needed in {file_path}")
        return False

def main():
    """Main function to update all mini-project files."""
    # Get all markdown files in the projects directory
    project_files = []
    for root, _, files in os.walk(PROJECTS_DIR):
        for file in files:
            if file.endswith('.md'):
                project_files.append(os.path.join(root, file))
    
    # Process each file
    updated_count = 0
    for file_path in project_files:
        if update_file(file_path):
            updated_count += 1
    
    print(f"\nDone! Updated {updated_count} of {len(project_files)} project files.")

if __name__ == "__main__":
    main()