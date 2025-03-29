# tools/build_mini_projects.py

from pathlib import Path

PROJECTS_DIR = Path("docs/projects")
OUTPUT_FILE = Path("docs/mini-projects.md")
HEADER = """# Mini Project Examples

This document contains ready-to-use mini-projects and activities for using ChatCraft in educational settings. Each project includes learning objectives, difficulty level, estimated time, and complete code examples.

## Table of Contents
"""

FOOTER = """
---

<!-- All mini-projects are now included and conform to the standard format.
For additions or edits, update the corresponding files in docs/projects/ and regenerate this document. -->

_For implementation strategies and assessment ideas, see the [ChatCraft Education Guide](education-guide.md)._
"""

def extract_title(md):
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None

def main():
    if not PROJECTS_DIR.exists():
        print(f"❌ Missing directory: {PROJECTS_DIR}")
        return

    projects = []

    for md_file in sorted(PROJECTS_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        title = extract_title(content)

        if not title:
            print(f"⚠️ Skipping {md_file.name}: missing '# Title'")
            continue

        anchor = title.lower().replace(" ", "-")
        projects.append((title, anchor, content))

    if not projects:
        print("⚠️ No valid mini-projects found.")
        return

    toc = "\n".join(
        f"{i+1}. [{title}](#{anchor})" for i, (title, anchor, _) in enumerate(projects)
    )

    body = "\n\n---\n\n".join(content for _, _, content in projects)

    final_output = f"{HEADER}\n{toc}\n\n---\n\n{body}\n{FOOTER}"
    OUTPUT_FILE.write_text(final_output, encoding="utf-8")
    print(f"✅ Wrote {len(projects)} projects to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
