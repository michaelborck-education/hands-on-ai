# Justfile for common development tasks

# 🧪 Run and check
test:
  pytest

lint:
  ruff chatcraft tests tools

format:
  ruff format chatcraft tests tools

# 💼 Run linter and tests together
ci: 
  just lint
  just test

# 🔧 Project setup
install-dev:
  pip install -r requirements-dev.txt

sync-version:
  python tools/inject_version.py --all
  echo "✅ Synced version across pyproject.toml and version.json"

requirements:
  uv pip compile pyproject.toml --output-file=requirements.txt
  uv pip compile pyproject.toml --extra=dev --output-file=requirements-dev.txt
  echo "✅ Regenerated requirements.txt and requirements-dev.txt"

# 🏗️ Build and distribute
build args="":
  python build.py {{args}}

bundle:
  python tools/build_zip.py

# 📚 Documentation
docs:
  mkdocs build --clean

deploy-docs:
  mkdocs gh-deploy --force

# 🧪 Run CLI in interactive REPL mode
repl:
  chatcraft interactive

# 🩺 Run diagnostic check
doctor:
  chatcraft doctor

# 🔧 Rebuild mini-projects markdown from individual project files
build-mini-projects:
  python tools/build_mini_projects.py

# 🌐 Regenerate HTML-based project browser
build-project-browser:
  python tools/project_browser.py

# 🛠️ Rebuild everything: sync version, docs, browser, mini-projects
build-all:
  just sync-version
  just build-mini-projects
  just build-project-browser
  just docs

# 🚀 Publish a new release
release:
  just build-all
  echo "🔖 Preparing release..."
  version=$(grep '^version *= *"' pyproject.toml | sed 's/version *= *"\(.*\)"/\1/')
  echo "🔖 Version: $$version"
  git add .
  git commit -m "🔖 Release $$version"
  git tag v$$version
  git push
  git push --tags
  echo "📦 Building and uploading to PyPI..."
  python -m build
  twine upload dist/*
  echo "✅ Release $$version published!"

# 🚀 Publish a new release to TestPyPI
release-test:
  just build-all
  python -m build
  twine upload --repository testpypi dist/*

# Lint mini-projects markdown files
lint-mini-projects:
  python tools/lint_mini_projects.py

clean:
  rm -rf build dist *.egg-info __pycache__ .pytest_cache .mypy_cache

# 📋 Help menu
help:
  @echo "Available commands:"
  @echo "  install-dev           Install dev dependencies"
  @echo "  test                  Run tests with pytest"
  @echo "  lint                  Run Ruff linter"
  @echo "  format                Auto-format code with Ruff"
  @echo "  build                 Build and optionally upload"
  @echo "  bundle                Create offline zip"
  @echo "  sync-version          Sync version across files"
  @echo "  docs                  Build MkDocs site"
  @echo "  deploy-docs           Deploy site to GitHub Pages"
  @echo "  repl                  Start ChatCraft REPL"
  @echo "  doctor                Run system diagnostic for ChatCraft"
  @echo "  build-mini-projects   Rebuild mini-projects.md from /docs/projects"
  @echo "  lint-mini-projects    Lint mini-projects.md files"
  @echo "  build-project-browser Generate the project_browser.html"
  @echo "  build-all             Sync version, rebuild docs and project browser"
  @echo "  release               Build, tag, push and publish to PyPI"
  @echo "  release-test          Publish release to TestPyPI"
  @echo "  clean                 Clean up build artifacts"
  @echo "  help                  Show this help message"
  