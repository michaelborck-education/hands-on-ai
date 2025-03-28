# Justfile for common development tasks

# 🧪 Run and check
test:
  pytest

lint:
  ruff chatcraft tests tools

format:
  ruff format chatcraft tests tools

ci: [lint test]  # 💼 Run linter and tests together

# 🔧 Project setup
install-dev:
  pip install -r requirements-dev.txt

sync-version:
  python tools/inject_version.py --all
  echo "✅ Synced version across pyproject.toml and version.json"

requirements:
  uv pip compile pyproject.toml --extra=none --output=requirements.txt
  uv pip compile pyproject.toml --extra=dev --output=requirements-dev.txt
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

# 📋 Help menu
help:
  @echo "Available commands:"
  @echo "  test            Run tests with pytest"
  @echo "  lint            Run Ruff linter"
  @echo "  format          Auto-format code with Ruff"
  @echo "  ci              Run lint and tests together"
  @echo "  install-dev     Install dev dependencies"
  @echo "  sync-version    Sync version across files"
  @echo "  requirements    Generate requirements.txt and requirements-dev.txt"
  @echo "  build           Build and optionally upload (e.g. just build -- --minor)"
  @echo "  bundle          Create offline .zip distribution"
  @echo "  docs            Build documentation"
  @echo "  deploy-docs     Deploy docs to GitHub Pages"
  @echo "  help            Show this help message"
