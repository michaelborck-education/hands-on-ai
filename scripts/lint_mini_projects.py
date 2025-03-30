# tools/lint_mini_projects.py

import re
import typer
from pathlib import Path
import os

app = typer.Typer(help="Lint mini-projects markdown files for correct format")

# Default is the combined file, but we also support directories
DEFAULT_MINI_PROJECTS_PATH = Path("docs/mini-projects.md")

# Match Python code blocks to exclude them from search
CODE_BLOCK_REGEX = re.compile(r"```python.*?```", re.DOTALL)

# Match actual project headers (level 1, not in TOC or implementation sections)
PROJECT_REGEX = re.compile(r"^# (?!Table of|Implementation|Assessment)(.+)$", re.MULTILINE)

# Define the patterns for required fields - allowing flexible whitespace
REQUIRED_FIELD_PATTERNS = [
    re.compile(r"\*\*Difficulty\*\*\s*:"),
    re.compile(r"\*\*Time\*\*\s*:"),
    re.compile(r"\*\*Learning Focus\*\*\s*:")
]

# Define patterns for required sections
SECTION_PATTERNS = [
    re.compile(r"^## Overview", re.MULTILINE),
    re.compile(r"^## Instructions", re.MULTILINE)
]

def extract_projects(md_path):
    """Extract all projects from the markdown file, skipping code blocks."""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(md_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # First, remove all Python code blocks to avoid false matches
    # Replace them with placeholders
    code_blocks = []
    
    def replace_code_block(match):
        code_blocks.append(match.group(0))
        return f"CODE_BLOCK_PLACEHOLDER_{len(code_blocks) - 1}"
    
    content_without_code = CODE_BLOCK_REGEX.sub(replace_code_block, content)
    
    # Find all project headers in the content without code blocks
    project_headers = PROJECT_REGEX.findall(content_without_code)
    projects = []
    
    # Get content for each project
    for i, header in enumerate(project_headers):
        # Find the start of this project
        header_with_prefix = f"# {header}"
        start_pos = content_without_code.find(header_with_prefix)
        
        # Find the end (either next project or end of file)
        if i < len(project_headers) - 1:
            next_header = f"# {project_headers[i+1]}"
            end_pos = content_without_code.find(next_header, start_pos)
        else:
            end_pos = len(content_without_code)
        
        # Extract project content
        project_content = content_without_code[start_pos:end_pos].strip()
        
        # Remove the header from the body for checking
        body = project_content[len(header_with_prefix):].strip()
        
        # For debugging, print the first few characters
        debug_preview = body[:50].replace('\n', '\\n')
        
        projects.append((header, body, debug_preview))
    
    return projects

def lint_project(title, body, debug_preview):
    """Check a project for required fields and sections."""
    errors = []
    
    # Skip linting for implementation/example sections
    if (title.lower().startswith(("run the", "test", "example")) or 
        "test" in title.lower() or "example" in title.lower() or 
        "choose which" in title.lower()):
        return ["  ⚠️ Skipping implementation/example section"]
    
    # Check for required fields using regex patterns
    for i, pattern in enumerate(REQUIRED_FIELD_PATTERNS):
        field_name = ["**Difficulty**", "**Time**", "**Learning Focus**"][i]
        if not pattern.search(body):
            errors.append(f"  ❌ Missing {field_name}")
    
    # Check for required sections using regex patterns
    for i, pattern in enumerate(SECTION_PATTERNS):
        section_name = ["## Overview", "## Instructions"][i]
        if not pattern.search(body):
            errors.append(f"  ❌ Missing {section_name}")
    
    return errors

def lint_single_file(md_path):
    """Lint a single markdown file for project format."""
    if not md_path.exists():
        print(f"❌ Could not find {md_path}")
        return False
    
    projects = extract_projects(md_path)
    valid_count = 0
    actual_projects = 0

    print(f"Found {len(projects)} sections with level 1 headers in {md_path}")
    
    for title, body, debug_preview in projects:
        print(f"🔍 Checking: {title}")
        
        errors = lint_project(title, body, debug_preview)
        
        # Skip implementation sections in the count
        if len(errors) == 1 and errors[0].startswith("  ⚠️ Skipping"):
            print(errors[0])
            continue
            
        actual_projects += 1
        
        if errors:
            for err in errors:
                print(err)
                
            # Debug output for failing projects
            if "Missing **" in " ".join(errors):
                print(f"  🔍 Debug preview: '{debug_preview}'")
        else:
            print("  ✅ OK")
            valid_count += 1

    if actual_projects == 0:
        return True
        
    print(f"✅ {valid_count}/{actual_projects} projects have all required fields and sections.")
    return valid_count == actual_projects

def lint_directory(directory_path):
    """Lint all markdown files in a directory for project format."""
    directory = Path(directory_path)
    if not directory.exists() or not directory.is_dir():
        print(f"❌ Could not find directory {directory}")
        return False
    
    md_files = list(directory.glob("*.md"))
    if not md_files:
        print(f"❌ No markdown files found in {directory}")
        return False
    
    print(f"Found {len(md_files)} markdown files in {directory}")
    
    all_valid = True
    for md_file in md_files:
        print(f"\n=== Checking {md_file.name} ===")
        file_valid = lint_single_file(md_file)
        all_valid = all_valid and file_valid
    
    return all_valid
    
@app.command()
def lint(
    path: Path = typer.Argument(
        DEFAULT_MINI_PROJECTS_PATH,
        help="Path to markdown file or directory containing project files"
    ),
    save_report: bool = typer.Option(
        False, "--save-report", "-s", 
        help="Save a detailed debug report for failing projects"
    )
):
    """Lint mini-projects markdown files for correct format."""
    path = Path(path)
    
    print(f"Linting mini-projects in {path}")
    
    if path.is_dir():
        all_valid = lint_directory(path)
    else:
        all_valid = lint_single_file(path)
    
    print("\n✅ Finished linting.")
    
    # Offer to save problematic projects to a file for debugging
    if not all_valid and save_report:
        report_path = "lint_debug_report.txt"
        with open(report_path, "w") as f:
            f.write(f"Debug report for {path}\n\n")
            
            if path.is_file():
                projects = extract_projects(path)
                for title, body, preview in projects:
                    errors = lint_project(title, body, preview)
                    if errors and not errors[0].startswith("  ⚠️ Skipping"):
                        f.write(f"=== {title} ===\n")
                        f.write(f"Preview: {preview}\n")
                        f.write("Errors:\n")
                        for err in errors:
                            f.write(f"{err}\n")
                        f.write("\nFull Content:\n")
                        f.write(f"{body[:500]}...\n\n")
            else:
                f.write("Directory scan - see console output for details\n")
                
        print(f"Debug report saved to {report_path}")
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    app()