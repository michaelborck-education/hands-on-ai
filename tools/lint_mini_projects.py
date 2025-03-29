# tools/lint_mini_projects.py

import re
from pathlib import Path

MINI_PROJECTS_PATH = Path("docs/mini-projects.md")
# Match actual project headers (level 2, not in TOC or implementation sections)
PROJECT_REGEX = re.compile(r"^## (?!Table of|Implementation|Assessment)(.+)$", re.MULTILINE)
REQUIRED_FIELDS = ["**Difficulty**", "**Time**", "**Learning Focus**"]

def extract_projects(md_path):
    content = md_path.read_text()
    
    # Find all project headers
    project_headers = PROJECT_REGEX.findall(content)
    projects = []
    
    # Get content for each project
    for i, header in enumerate(project_headers):
        # Find the start of this project
        header_with_prefix = f"## {header}"
        start_pos = content.find(header_with_prefix)
        
        # Find the end (either next project or end of file)
        if i < len(project_headers) - 1:
            next_header = f"## {project_headers[i+1]}"
            end_pos = content.find(next_header, start_pos)
        else:
            end_pos = len(content)
        
        # Extract project content
        project_content = content[start_pos:end_pos].strip()
        
        # Remove the header from the body for checking
        body = project_content[len(header_with_prefix):].strip()
        projects.append((header, body))
    
    return projects

def lint_project(title, body):
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in body:
            errors.append(f"  ❌ Missing {field}")
    return errors

def main():
    if not MINI_PROJECTS_PATH.exists():
        print(f"❌ Could not find {MINI_PROJECTS_PATH}")
        return

    projects = extract_projects(MINI_PROJECTS_PATH)
    valid_count = 0

    for title, body in projects:
        print(f"🔍 Checking: {title}")
        errors = lint_project(title, body)
        if errors:
            for err in errors:
                print(err)
        else:
            print("  ✅ OK")
            valid_count += 1

    print("\n✅ Finished linting.")
    print(f"✅ {valid_count}/{len(projects)} projects have all required fields.")

if __name__ == "__main__":
    main()