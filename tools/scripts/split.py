#!/usr/bin/env python3

import re
import typer
from pathlib import Path
from typing import Optional

def slugify(title):
    """Convert a title to a slug format (lowercase, hyphens instead of spaces and special chars)."""
    return re.sub(r'\W+', '-', title.lower()).strip("-")

def split_markdown(input_file, output_dir):
    """Split a markdown file with level-1 headers into individual files."""
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read the content of the input file
    content = input_file.read_text()
    
    # Find all level-1 headers (# Project Title)
    project_headers = re.findall(r"(?m)^# (.+)$", content)
    
    if not project_headers:
        typer.echo(f"⚠️ No level-1 headers found in {input_file}")
        return 0
    
    projects = []
    # Extract content for each project
    for i, title in enumerate(project_headers):
        # Find the start position of this project
        header = f"# {title}"
        start_pos = content.find(header)
        
        # Find the end position (either the next project header or the end of the file)
        if i < len(project_headers) - 1:
            next_header = f"# {project_headers[i+1]}"
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
        typer.echo(f"Creating file: {out_path}")
        out_path.write_text(content)
    
    return len(projects)

app = typer.Typer(help="Split markdown files with level-1 headers into individual files")

@app.command()
def split(
    input_file: Path = typer.Option(
        Path("docs/projects/agent/mini-projects.md"),
        "--input",
        "-i",
        help="Input markdown file"
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Output directory for project files (default: same directory as input file)"
    ),
):
    """Split markdown files with level-1 headers into individual project files."""
    # If no output directory is specified, use the same directory as the input file
    if output_dir is None:
        output_dir = input_file.parent
    
    count = split_markdown(input_file, output_dir)
    typer.echo(f"✅ Split into {count} project files in {output_dir}")

if __name__ == "__main__":
    app()