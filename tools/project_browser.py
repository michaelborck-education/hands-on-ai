import datetime
import argparse
from pathlib import Path
import markdown
import re
import json

PROJECTS_DIR = Path("docs/projects")
VERSION_FILE = Path("version.json")
OUTPUT_HTML = Path("tools/project_browser.html")

def read_markdown_files(projects_dir):
    projects = []

    for md_file in projects_dir.glob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        
        # Updated regex to match h1 titles instead of h2
        title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
        difficulty_match = re.search(r'\*\*Difficulty\*\*:\s*(.*)', content)
        focus_match = re.search(r'\*\*Learning Focus\*\*:\s*(.*)', content)

        title = title_match.group(1).strip() if title_match else md_file.stem.replace('_', ' ').title()
        difficulty = difficulty_match.group(1).strip() if difficulty_match else 'Medium'
        focus = focus_match.group(1).strip() if focus_match else 'General'

        # Updated line with extensions for syntax highlighting
        html_content = markdown.markdown(
            content, extensions=['fenced_code', 'codehilite']
        )

        projects.append({
            'title': title,
            'focus': focus,
            'difficulty': difficulty,
            'content': html_content
        })

    return projects

def read_local_version():
    if VERSION_FILE.exists():
        data = json.loads(VERSION_FILE.read_text())
        return data.get("version", "0.0.0")
    return "unknown"

def generate_html(projects):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    focuses = sorted(set(p['focus'] for p in projects))
    difficulties = sorted(set(p['difficulty'] for p in projects))

    html = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Project Browser</title>
    <script src='https://cdn.tailwindcss.com'></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</head>
<body class='bg-gray-50 p-6'>
    <h1 class='text-2xl font-bold mb-4'>AiLabKit Project Browser</h1>
    <p class='mb-4'>Generated: {date_str} v{local_version} <span id="latest-version">  <span id="latest-version">📁 Offline version. Visit <a href="https://github.com/teaching-repositories/ailabkit" target="_blank">AiLabKit GitHub</a> to check for updates.</span>
</span></p>

    <div class='mb-4 flex flex-col md:flex-row gap-4'>
        <input type='text' id='search' placeholder='Search projects...' class='border p-2 rounded w-full md:w-1/3'>

        <select id='focusFilter' class='border p-2 rounded'>
            <option value='all'>All Focus Areas</option>
            {''.join(f'<option value="{f}">{f}</option>' for f in focuses)}
        </select>

        <select id='difficultyFilter' class='border p-2 rounded'>
            <option value='all'>All Difficulties</option>
            {''.join(f'<option value="{d}">{d}</option>' for d in difficulties)}
        </select>
    </div>

    <div id='projects' class='space-y-4'>
        {''.join(generate_accordion_item(p, idx) for idx, p in enumerate(projects))}
    </div>

<script>
function toggleAccordion(idx) {{
    document.getElementById(`content-${{idx}}`).classList.toggle('hidden');
}}

const search = document.getElementById('search');
const focusFilter = document.getElementById('focusFilter');
const difficultyFilter = document.getElementById('difficultyFilter');
const items = document.querySelectorAll('.project');

search.addEventListener('input', applyFilters);
focusFilter.addEventListener('change', applyFilters);
difficultyFilter.addEventListener('change', applyFilters);

function applyFilters() {{
    const searchVal = search.value.toLowerCase();
    const focusVal = focusFilter.value;
    const difficultyVal = difficultyFilter.value;

    items.forEach(item => {{
        const matchesSearch = item.dataset.title.includes(searchVal);
        const matchesFocus = focusVal === 'all' || item.dataset.focus === focusVal;
        const matchesDifficulty = difficultyVal === 'all' || item.dataset.difficulty === difficultyVal;

        item.style.display = (matchesSearch && matchesFocus && matchesDifficulty) ? '' : 'none';
    }});
}}
</script>
</body>
</html>
"""
    return html


def generate_accordion_item(project, idx):
    return f"""
    <div class='project border rounded shadow-sm bg-white' data-title='{project['title'].lower()}' data-focus='{project['focus']}' data-difficulty='{project['difficulty']}'>
        <button onclick='toggleAccordion({idx})' class='w-full text-left p-4 font-semibold'>
            {project['title']} <span class='text-sm text-gray-500'>({project['focus']} - {project['difficulty']})</span>
        </button>
        <div id='content-{idx}' class='hidden p-4 border-t'>
            {project['content']}
        </div>
    </div>
"""


def build_html(projects_dir, output_path):
    projects = read_markdown_files(projects_dir)
    html = generate_html(projects)
    output_path.write_text(html, encoding='utf-8')
    return len(projects)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML browser for mini-projects")
    parser.add_argument("--projects-dir", type=Path, default=Path("docs/projects"), 
                        help="Directory containing markdown project files (default: docs/projects)")
    parser.add_argument("--output", type=Path, default=Path("tools/project_browser.html"), 
                        help="Output HTML file path (default: tools/project_browser.html)")

    args = parser.parse_args()

    local_version = read_local_version()
    count = build_html(args.projects_dir, args.output)
    print(f"✅ Generated browser with {count} projects: {args.output}")