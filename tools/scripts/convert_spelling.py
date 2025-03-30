#!/usr/bin/env python3
"""
Convert American English spelling to Australian/British English spelling
in documentation files.

This script recursively scans markdown files in the specified directory
and applies common American to Australian/British spelling conversions.
"""

import os
import re
import argparse
from pathlib import Path

# Define common American to Australian/British spelling conversions
# Format: (American spelling, Australian/British spelling)
SPELLING_CONVERSIONS = [
    # -or to -our
    (r'\b(col)or\b', r'\1our'),
    (r'\b(fav)or\b', r'\1our'),
    (r'\b(flav)or\b', r'\1our'),
    (r'\b(hon)or\b', r'\1our'),
    (r'\b(hum)or\b', r'\1our'),
    (r'\b(lab)or\b', r'\1our'),
    (r'\b(neighb)or\b', r'\1our'),
    (r'\b(neighb)ors\b', r'\1ours'),
    (r'\b(rum)or\b', r'\1our'),
    (r'\b(rum)ors\b', r'\1ours'),
    (r'\b(sav)or\b', r'\1our'),
    (r'\b(sav)ors\b', r'\1ours'),
    (r'\b(splend)or\b', r'\1our'),
    (r'\b(vig)or\b', r'\1our'),
    
    # -ize to -ise
    (r'\b(\w+)ize\b', r'\1ise'),
    (r'\b(\w+)ized\b', r'\1ised'),
    (r'\b(\w+)izing\b', r'\1ising'),
    (r'\b(\w+)ization\b', r'\1isation'),
    (r'\b(\w+)izations\b', r'\1isations'),
    
    # -yze to -yse
    (r'\b(anal)yze\b', r'\1yse'),
    (r'\b(anal)yzer\b', r'\1yser'),
    (r'\b(anal)yzed\b', r'\1ysed'),
    (r'\b(anal)yzing\b', r'\1ysing'),
    (r'\b(catal)yze\b', r'\1yse'),
    (r'\b(catal)yzed\b', r'\1ysed'),
    (r'\b(catal)yzing\b', r'\1ysing'),
    (r'\b(paral)yze\b', r'\1yse'),
    (r'\b(paral)yzed\b', r'\1ysed'),
    (r'\b(paral)yzing\b', r'\1ysing'),
    
    # -og to -ogue
    (r'\b(catal)og\b', r'\1ogue'),
    (r'\b(catal)ogs\b', r'\1ogues'),
    (r'\b(dial)og\b', r'\1ogue'),
    (r'\b(dial)ogs\b', r'\1ogues'),
    (r'\b(mon)olog\b', r'\1ologue'),
    (r'\b(mon)ologs\b', r'\1ologues'),
    
    # -am to -amme
    (r'\b(progr)am(?!m)\b', r'\1amme'),
    (r'\b(progr)ams\b', r'\1ammes'),
    
    # -ense to -ence
    (r'\b(def)ense\b', r'\1ence'),
    (r'\b(lic)ense\b', r'\1ence'),  # Noun form
    (r'\b(off)ense\b', r'\1ence'),
    (r'\b(pret)ense\b', r'\1ence'),
    
    # -ter to -tre
    (r'\b(cen)ter\b', r'\1tre'),
    (r'\b(cen)ters\b', r'\1tres'),
    (r'\b(fi)ber\b', r'\1bre'),
    (r'\b(fi)bers\b', r'\1bres'),
    (r'\b(me)ter\b', r'\1tre'),  # As in unit of measurement
    (r'\b(me)ters\b', r'\1tres'),
    (r'\b(thea)ter\b', r'\1tre'),
    (r'\b(thea)ters\b', r'\1tres'),
    
    # Specific words
    (r'\b(plow)\b', r'plough'),
    (r'\b(tire)\b', r'tyre'),  # Car tire
    (r'\b(tires)\b', r'tyres'),
    (r'\b(gray)\b', r'grey'),
    (r'\b(grays)\b', r'greys'),
    (r'\b(math)\b', r'maths'),
    (r'\b(airplane)\b', r'aeroplane'),
    (r'\b(airplanes)\b', r'aeroplanes'),
    (r'\b(aluminum)\b', r'aluminium'),
    (r'\b(jail)\b', r'gaol'),
    (r'\b(jails)\b', r'gaols'),
    (r'\b(dialog box)\b', r'dialogue box'),
    (r'\b(dialog boxes)\b', r'dialogue boxes'),
    
    # Double L in derivatives
    (r'\b(travel)ing\b', r'\1ling'),
    (r'\b(travel)ed\b', r'\1led'),
    (r'\b(cancel)ing\b', r'\1ling'),
    (r'\b(cancel)ed\b', r'\1led'),
]

# Words to explicitly exclude (special cases, technical terms, etc.)
EXCLUDE_WORDS = [
    'advertise', 'authorize', 'characterize', 'customize', 'computerize',
    'memorize', 'minimize', 'normalize', 'organize', 'organization', 
    'organizations', 'recognize', 'summarize', 'visualize', 'visualization',
    'visualizations', 'utilize',
    # Technical programming terms
    'size', 'sizes', 'resize', 'initialize',
    # File extensions/types
    'serialization', 'serializing', 'serialize',
    # Keep American spelling in code-specific text
    'color-picker', 'colors.js',
    # From test case
    'parameter'
]

# Complete words to exclude (words that should never be changed)
EXCLUDE_FULL_WORDS = [
    'color', 'visualization', 'program', 'flavor', 'center', 'analyze',
    'recognize', 'customize'  # Common in code examples and test cases
]

def update_file(file_path, dry_run=False, verbose=False):
    """Update a single file with Australian/British spelling."""
    if verbose:
        print(f"Processing {file_path}...")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip code blocks, HTML blocks, YAML frontmatter, etc. by temporarily storing them
    code_blocks = []
    yaml_blocks = []
    html_blocks = []
    
    def replace_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks) - 1}__"
    
    def replace_yaml_block(match):
        yaml_blocks.append(match.group(0))
        return f"__YAML_BLOCK_{len(yaml_blocks) - 1}__"
    
    def replace_html_block(match):
        html_blocks.append(match.group(0))
        return f"__HTML_BLOCK_{len(html_blocks) - 1}__"
    
    # Temporarily replace special blocks
    # Replace YAML frontmatter
    content = re.sub(r'---\n[\s\S]*?\n---', replace_yaml_block, content)
    
    # Replace code blocks - fenced code blocks and inline code
    content = re.sub(r'```[\s\S]*?```', replace_code_block, content)
    
    # Handle inline code
    # We need to better handle inline code by preserving whole sentences with backticks
    parts = []
    last_end = 0
    
    # Use regex to find all inline code sections
    for match in re.finditer(r'`[^`]+`', content):
        # Add text before the backtick
        if match.start() > last_end:
            parts.append(content[last_end:match.start()])
            
        # Add the backtick content as a code block
        code_blocks.append(match.group(0))
        parts.append(f"__CODE_BLOCK_{len(code_blocks) - 1}__")
        
        last_end = match.end()
    
    # Add any remaining text
    if last_end < len(content):
        parts.append(content[last_end:])
    
    # Rejoin the content
    content = "".join(parts)
    
    # Replace HTML blocks
    content = re.sub(r'<[^>]+>[^<]*</[^>]+>', replace_html_block, content)
    
    # Store original content for comparison
    original_content = content
    
    # Convert spelling patterns
    for am_pattern, au_pattern in SPELLING_CONVERSIONS:
        # Skip if it contains any excluded words
        if any(excl in am_pattern for excl in EXCLUDE_WORDS):
            continue
            
        # For patterns that match full words, check against EXCLUDE_FULL_WORDS
        is_full_word_pattern = '\\b' in am_pattern
        if is_full_word_pattern:
            # Extract the word from the pattern (between capture groups if present)
            pattern_word = re.search(r'\\b\(?(\w+)', am_pattern)
            if pattern_word and pattern_word.group(1) in EXCLUDE_FULL_WORDS:
                continue
                
        content = re.sub(am_pattern, au_pattern, content)
    
    # Restore blocks using direct string replacement
    
    # Restore in reverse order
    for i, block in enumerate(html_blocks):
        content = content.replace(f"__HTML_BLOCK_{i}__", block)
    
    for i, block in enumerate(code_blocks):
        content = content.replace(f"__CODE_BLOCK_{i}__", block)
    
    for i, block in enumerate(yaml_blocks):
        content = content.replace(f"__YAML_BLOCK_{i}__", block)
    
    # Check if content was modified
    if content != original_content:
        if not dry_run:
            # Write back to the file if changes were made
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            if verbose:
                print(f"  Updated {file_path}")
            return True
        else:
            if verbose:
                print(f"  Would update {file_path} (dry run)")
            return True
    else:
        if verbose:
            print(f"  No changes needed in {file_path}")
        return False

def process_directory(directory_path, extensions=None, dry_run=False, verbose=False):
    """Process all files in the specified directory recursively."""
    if extensions is None:
        extensions = ['.md', '.mdx', '.txt', '.html']
    
    # Convert to Path object for consistent handling
    directory = Path(directory_path)
    
    # Ensure the directory exists
    if not directory.is_dir():
        print(f"Error: Directory '{directory}' not found.")
        return 0, 0
    
    # Track statistics
    total_files = 0
    updated_files = 0
    
    # Get all target files in the directory (recursively)
    for ext in extensions:
        for file_path in directory.glob(f'**/*{ext}'):
            # Skip hidden files
            if any(part.startswith('.') for part in file_path.parts):
                continue
                
            total_files += 1
            
            if update_file(file_path, dry_run, verbose):
                updated_files += 1
    
    return total_files, updated_files

def main():
    """Main function to update documentation files."""
    parser = argparse.ArgumentParser(
        description='Convert American spelling to Australian/British spelling in documentation files'
    )
    parser.add_argument('--dir', default='./docs', help='Directory to process (default: ./docs)')
    parser.add_argument('--extensions', default='.md,.mdx,.txt,.html', 
                        help='Comma-separated file extensions to process (default: .md,.mdx,.txt,.html)')
    parser.add_argument('--dry-run', action='store_true', help='Check files without making changes')
    parser.add_argument('--file', help='Process a specific file instead of a directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    # Process extensions
    extensions = args.extensions.split(',')
    
    if args.file:
        # Process just one file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File '{file_path}' not found.")
            return
            
        updated = update_file(file_path, args.dry_run, True)
        if updated:
            print(f"File would be updated" if args.dry_run else f"File updated")
        else:
            print("No changes needed")
    else:
        # Process directory
        total_files, updated_files = process_directory(
            args.dir, extensions, args.dry_run, args.verbose
        )
        
        mode = "would be" if args.dry_run else "were"
        print(f"\nDone! {updated_files} of {total_files} files {mode} updated with Australian/British spelling.")

if __name__ == "__main__":
    main()