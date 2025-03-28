# Makefile for common development tasks

.PHONY: install-dev test lint format ci build bundle sync-version requirements docs deploy-docs help

# 🧪 Run and check
test:
	pytest

lint:
	ruff chatcraft tests tools

format:
	ruff format chatcraft tests tools

ci: lint test

# 🔧 Project setup
install-dev:
	pip install -r requirements-dev.txt

sync-version:
	python tools/inject_version.py --all
	@echo "✅ Synced version across pyproject.toml and version.json"

requirements:
	uv pip compile pyproject.toml --extra=none --output=requirements.txt
	uv pip compile pyproject.toml --extra=dev --output=requirements-dev.txt
	@echo "✅ Regenerated requirements.txt and requirements-dev.txt"

# 🏗️ Build and distribute
build:
	python build.py

bundle:
	python tools/build_zip.py

# 📚 Documentation
docs:
	mkdocs build --clean

deploy-docs:
	mkdocs gh-deploy --force

# 📋 Help menu
help:
	@echo "Make targets:"
	@echo "  test            Run tests with pytest"
	@echo "  lint            Run ruff linter"
	@echo "  format          Auto-format code with ruff"
	@echo "  ci              Run lint and tests together"
	@echo "  install-dev     Install dev dependencies"
	@echo "  sync-version    Sync version across files"
	@echo "  requirements    Generate requirements.txt and requirements-dev.txt"
	@echo "  build           Build and optionally upload"
	@echo "  bundle          Create offline zip"
	@echo "  docs            Build MkDocs site"
	@echo "  deploy-docs     Deploy site to GitHub Pages"
	@echo "  help            Show this help message"