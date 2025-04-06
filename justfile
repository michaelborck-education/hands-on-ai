# Justfile for common development tasks

# 🧪 Run and check
test:
  pytest

test-basic:
  python test_ailabkit.py

lint:
  ruff src/ailabkit tests scripts

format:
  ruff format src/ailabkit tests scripts

# 💼 Run linter and tests together
ci: 
  just lint
  just test

# 🔧 Project setup
install-dev:
  pip install -r requirements-dev.txt

sync-version:
  scripts/inject_version.py --all
  echo "✅ Synced version across pyproject.toml and version.json"

requirements:
  uv pip compile pyproject.toml --output-file=requirements.txt
  uv pip compile pyproject.toml --extra=dev --output-file=requirements-dev.txt
  echo "✅ Regenerated requirements.txt and requirements-dev.txt"

# 🏗️ Build and distribute
build:
  python -m build

bundle:
  scripts/build_zip.py

# 📚 Documentation
docs:
  just generate-bot-gallery
  just generate-project-index
  mkdocs build --clean

deploy-docs:
  just generate-bot-gallery
  just generate-project-index
  mkdocs gh-deploy --force

# 🧪 Run CLI modules in interactive mode
chat-repl:
  ailabkit chat interactive

rag-repl:
  ailabkit rag interactive

agent-repl:
  ailabkit agent interactive

# 🩺 Run diagnostic check
doctor:
  ailabkit doctor

# 🌐 Run web interfaces
chat-web:
  ailabkit chat web

rag-web:
  ailabkit rag web
  
agent-web:
  ailabkit agent web

# Rebuild Bot gallery markdown from doc strings
generate-bot-gallery:
  scripts/generate_bot_gallery.py --flat --out docs/bot-gallery.md

# 🇦🇺 Convert American spelling to Australian/British spelling in docs
spelling-au:
  scripts/convert_spelling.py --verbose

# 🌐 Regenerate HTML-based project browser
build-project-browser:
  scripts/project_browser.py --output docs/project_browser.html
  cp docs/project_browser.html project_browser.html

# 🛠️ Rebuild everything: sync version, docs, browser, mini-projects
build-all:
  just sync-version
  just generate-project-index
  just generate-bot-gallery
  just build-project-browser
  just docs

# Lint mini-projects markdown files
lint-mini-projects:
  scripts/lint_mini_projects.py
  
# Generate the projects index.md file
generate-project-index:
  scripts/generate_project_index.py

# Lint chat mini-projects markdown files
lint-chat-projects:
  scripts/lint_mini_projects.py docs/projects/chat

# Lint rag mini-projects markdown files  
lint-rag-projects:
  scripts/lint_mini_projects.py docs/projects/rag

# Lint agent mini-projects markdown files
lint-agent-projects:
  scripts/lint_mini_projects.py docs/projects/agent

# Lint all module-specific mini-projects
lint-all-projects: lint-chat-projects lint-rag-projects lint-agent-projects

clean:
  rm -rf build dist *.egg-info __pycache__ .pytest_cache .mypy_cache

# 📋 Help menu
help:
  @echo "Available commands:"
  @echo "  install-dev           Install dev dependencies"
  @echo "  test                  Run all tests with pytest"
  @echo "  test-basic            Run basic imports test directly"
  @echo "  lint                  Run Ruff linter"
  @echo "  format                Auto-format code with Ruff"
  @echo "  build                 Build and optionally upload"
  @echo "  bundle                Create offline zip"
  @echo "  sync-version          Sync version across files"
  @echo "  docs                  Build MkDocs site"
  @echo "  deploy-docs           Deploy site to GitHub Pages"
  @echo "  chat-repl             Start AiLabKit chat interactive mode"
  @echo "  rag-repl              Start AiLabKit RAG interactive mode"
  @echo "  agent-repl            Start AiLabKit agent interactive mode"
  @echo "  chat-web              Start AiLabKit chat web interface"
  @echo "  rag-web               Start AiLabKit RAG web interface"
  @echo "  agent-web             Start AiLabKit agent web interface"
  @echo "  doctor                Run system diagnostic for AiLabKit"
  @echo "  build-mini-projects   Rebuild mini-projects.md from /docs/projects"
  @echo "  spelling-au           Convert American spelling to Australian/British spelling"
  @echo "  lint-mini-projects    Lint the combined mini-projects.md file"
  @echo "  generate-project-index  Generate the projects/index.md file"
  @echo "  generate-bot-gallery   Generate the bot gallery markdown"
  @echo "  lint-chat-projects    Lint chat mini-projects"
  @echo "  lint-rag-projects     Lint RAG mini-projects"
  @echo "  lint-agent-projects   Lint agent mini-projects"
  @echo "  lint-all-projects     Lint all module-specific mini-projects"
  @echo "  build-project-browser Generate the project_browser.html"
  @echo "  build-all             Sync version, rebuild docs and project browser"
  @echo "  clean                 Clean up build artifacts"
  @echo "  help                  Show this help message"
  
