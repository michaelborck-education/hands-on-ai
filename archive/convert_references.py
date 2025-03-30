#!/usr/bin/env python3
"""
Script to find and replace ChatCraft references with AiLabKit throughout the documentation.
This script updates both textual references and import statements in code samples.
"""

import os
import re
from pathlib import Path
import fileinput
import sys

# Directory to search
DOCS_DIR = Path("docs")

# Mapping of terms to replace
REPLACEMENTS = [
    # Text replacements (case-sensitive)
    (r'ChatCraft', 'AiLabKit'),
    # Code imports in Python examples
    (r'from chatcraft import', 'from ailabkit.chat import'),
    (r'import chatcraft', 'import ailabkit.chat'),
    # Function calls in Python examples - handle with care to not break other code
    (r'chatcraft\.', 'ailabkit.chat.'),
    # General lowercase references - must come last to avoid breaking code replacements
    (r'chatcraft', 'ailabkit.chat'),
]

# File types to process
FILE_EXTENSIONS = ['.md', '.py', '.txt', '.html']

def should_process_file(file_path):
    """Determine if we should process this file type."""
    ext = file_path.suffix.lower()
    return ext in FILE_EXTENSIONS

def process_file(file_path):
    """Process a single file to replace references."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements_made = 0
        
        for pattern, replacement in REPLACEMENTS:
            # Count the replacements for this pattern
            matches = len(re.findall(pattern, content))
            replacements_made += matches
            
            # Replace the pattern
            content = re.sub(pattern, replacement, content)
        
        # Only write to the file if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements_made
        
        return 0
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    """Main function to traverse directories and process files."""
    if not DOCS_DIR.exists():
        print(f"❌ Directory not found: {DOCS_DIR}")
        return
    
    # Files processed and replacements made
    files_processed = 0
    files_updated = 0
    total_replacements = 0
    
    print(f"🔍 Scanning {DOCS_DIR} for ChatCraft references...")
    
    # Walk through all files in the docs directory
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            file_path = Path(root) / file
            
            if should_process_file(file_path):
                replacements = process_file(file_path)
                files_processed += 1
                
                if replacements > 0:
                    files_updated += 1
                    total_replacements += replacements
                    print(f"✅ Updated {file_path.relative_to(Path.cwd())}: {replacements} replacements")
    
    print("\n📊 Summary:")
    print(f"Files processed: {files_processed}")
    print(f"Files updated: {files_updated}")
    print(f"Total replacements: {total_replacements}")

if __name__ == "__main__":
    main()