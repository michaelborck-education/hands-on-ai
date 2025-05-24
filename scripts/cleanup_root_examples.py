#!/usr/bin/env python
"""
Cleanup script to remove old example files from the root directory
that have been moved to the examples/ directory.

This script is meant to be run after updating from a version before 0.1.12,
where example scripts were kept in the root directory.
"""

import os
import argparse
from pathlib import Path

# Files that have been moved to examples/
MOVED_FILES = [
    "test_agent.py",
    "simple_weather_agent_test.py",
    "weather_graph_agent_example.py",
    "debug_agent_prompt.py",
    "debug_json_agent.py",
    "enhanced_test_agent.py",
    "json_agent.py",
    "multi_format_agent_test.py",
]

def main():
    parser = argparse.ArgumentParser(
        description="Remove old example files that have been moved to examples/"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually delete files, just show what would be deleted",
    )
    args = parser.parse_args()

    # Get the project root directory
    root_dir = Path(__file__).parent.parent
    
    print(f"Checking for old example files in {root_dir}...")
    
    # Check for each file
    files_to_remove = []
    for filename in MOVED_FILES:
        file_path = root_dir / filename
        if file_path.exists():
            files_to_remove.append(file_path)
    
    # Report findings
    if not files_to_remove:
        print("No old example files found in the root directory.")
        return
    
    print(f"Found {len(files_to_remove)} old example file(s) to remove:")
    for file_path in files_to_remove:
        print(f"  - {file_path.relative_to(root_dir)}")
    
    # Delete files if not in dry-run mode
    if args.dry_run:
        print("\nDry run: No files were deleted.")
        print("Run without --dry-run to actually delete these files.")
    else:
        print("\nDeleting files...")
        for file_path in files_to_remove:
            os.remove(file_path)
            print(f"  ✓ Deleted {file_path.relative_to(root_dir)}")
        print("\nCleanup complete! All example files have been moved to examples/")
        print("You can run 'git status' to verify the changes.")

if __name__ == "__main__":
    main()