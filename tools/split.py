#!/usr/bin/env python3

import re
import argparse
from pathlib import Path

def slugify(title):
    return re.sub(r'\W+', '-', title.lower()).strip("-")

def split_markdown(input_file, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    content = input_file.read_text()
    
    # Find all valid project titles (level 2 headers that aren't Table of Contents, Implementation Tips, etc.)
    project_headers = re.findall(r"(?m)^## (?!Table of|Implementation|Assessment)(.+)$", content)
    
    projects = []
    # Extract content for each project
    for i, title in enumerate(project_headers):
        # Find the start position of this project
        header = f"## {title}"
        start_pos = content.find(header)
        
        # Find the end position (either the next project header or the end of the file)
        if i < len(project_headers) - 1:
            next_header = f"## {project_headers[i+1]}"
            end_pos = content.find(next_header, start_pos)
        else:
            # For the last project, go to the end of the file
            end_pos = len(content)
        
        # Extract the full project content
        project_content = content[start_pos:end_pos].strip()
        projects.append((title, project_content))
    
    # Write each project to its own file
    for title, content in projects:
        slug = slugify(title)
        out_path = output_dir / f"{slug}.md"
        out_path.write_text(content)
    
    return len(projects)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split mini-projects.md into individual files")
    parser.add_argument("--input", type=Path, default=Path("docs/mini-projects.md"), 
                        help="Input markdown file (default: docs/mini-projects.md)")
    parser.add_argument("--output-dir", type=Path, default=Path("docs/projects"), 
                        help="Output directory for project files (default: docs/projects)")
    
    args = parser.parse_args()
    
    count = split_markdown(args.input, args.output_dir)
    print(f"✅ Split into {count} project files in {args.output_dir}")