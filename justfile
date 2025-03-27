# Justfile for common development tasks

# ✅ Setup development environment
install-dev:
  pip install -r requirements-dev.txt

# 🧪 Run tests
test:
  pytest

# 🧹 Lint with Ruff
lint:
  ruff chatcraft tests tools

# 🎨 Format with Ruff
format:
  ruff format chatcraft tests tools

# 🏗️ Build and optionally upload
build args="":
  python build.py {{args}}

# 💼 Create offline bundle
bundle:
  python tools/build_zip.py

# 🔄 Sync version across project
sync-version:
  python tools/inject_version.py

# 📚 Build documentation
docs:
  mkdocs build --clean

# 🌍 Deploy documentation to GitHub Pages
deploy-docs:
  mkdocs gh-deploy --force

# 📋 Help menu
help:
  @echo "Available commands:"
  @echo "  install-dev     Install dev dependencies"
  @echo "  test            Run tests with pytest"
  @echo "  lint            Run Ruff linter"
  @echo "  format          Auto-format code with Ruff"
  @echo "  build           Build and optionally upload (use: just build -- --minor)"
  @echo "  bundle          Create offline .zip distribution"
  @echo "  sync-version    Sync version across files"
  @echo "  docs            Build documentation"
  @echo "  deploy-docs     Deploy docs to GitHub Pages"
  @echo "  help            Show this help message"
