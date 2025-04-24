#!/usr/bin/env python3
"""
Script to update all references from ailabkit/AiLabKit to hands-on-ai/Hands-On AI in documentation files.
"""
import re
import os
from pathlib import Path

def update_file(file_path):
    """Update all instances of ailabkit/AiLabKit in a file with hands-on-ai/Hands-On AI."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Keep track if we made changes
    original_content = content
    
    # Common replacements
    replacements = [
        # Import statements
        (r'from ailabkit\.', r'from hands_on_ai.'),
        (r'import ailabkit\.', r'import hands_on_ai.'),
        
        # Pip install
        (r'pip install ailabkit', r'pip install hands-on-ai'),
        (r'uv pip install ailabkit', r'uv pip install hands-on-ai'),
        
        # Configuration paths
        (r'~\.ailabkit', r'~/.hands_on_ai'),
        
        # CLI commands
        (r'ailabkit\s+', r'hands-on-ai '),
        (r'`ailabkit`', r'`hands-on-ai`'),
        
        # Project/module references (text)
        (r'AiLabKit\b', r'Hands-On AI'),
        (r'\bailabkit\b', r'hands-on-ai'),
        
        # Package structure
        (r'ailabkit/', r'hands_on_ai/'),
    ]
    
    # Apply all replacements
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Check if the content was modified
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    # Directory to scan for markdown files
    docs_dir = Path('docs')
    
    # Find all markdown files
    markdown_files = list(docs_dir.glob('**/*.md'))
    
    # Counter for files updated
    updated_files = 0
    
    # Process each file
    for file_path in markdown_files:
        if update_file(file_path):
            print(f"Updated: {file_path}")
            updated_files += 1
    
    # Also update project_browser.html if it exists
    project_browser_paths = [
        Path('docs/project_browser.html'),
        Path('project_browser.html')
    ]
    
    for pb_path in project_browser_paths:
        if pb_path.exists() and update_file(pb_path):
            print(f"Updated: {pb_path}")
            updated_files += 1
    
    print(f"\nTotal files updated: {updated_files}")

if __name__ == "__main__":
    main()