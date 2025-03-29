# Makefile for common development tasks

.PHONY: install-dev test lint format ci sync-version requirements build bundle docs deploy-docs repl doctor build-mini-projects build-project-browser build-all release release-test help clean

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
build-all: sync-version build-mini-projects build-project-browser docs

# 🚀 Publish a new release
release: build-all
	@echo "🔖 Preparing release..."
	$(eval VERSION := $(shell grep '^version *= *"' pyproject.toml | sed 's/version *= *"\(.*\)"/\1/'))
	@echo "🔖 Version: $(VERSION)"
	git add .
	git commit -m "🔖 Release $(VERSION)"
	git tag v$(VERSION)
	git push
	git push --tags
	@echo "📦 Building and uploading to PyPI..."
	python -m build
	twine upload dist/*
	@echo "✅ Release $(VERSION) published!"

# 🚀 Publish a new release to TestPyPI
release-test: build-all
	python -m build
	twine upload --repository testpypi dist/*

# 🧹 Clean build artifacts
clean:
	rm -rf build dist *.egg-info __pycache__ .pytest_cache .mypy_cache

# 📋 Help menu
help:
	@echo "Make targets:"
	@echo "  install-dev           Install dev dependencies"
	@echo "  test                  Run tests with pytest"
	@echo "  lint                  Run Ruff linter"
	@echo "  format                Auto-format code with Ruff"
	@echo "  build                 Build and optionally upload"
	@echo "  bundle                Create offline zip"
	@echo "  sync-version          Sync version across files"
	@echo "  requirements          Regenerate requirements.txt and requirements-dev.txt"
	@echo "  docs                  Build MkDocs site"
	@echo "  deploy-docs           Deploy site to GitHub Pages"
	@echo "  repl                  Start ChatCraft REPL"
	@echo "  doctor                Run system diagnostic for ChatCraft"
	@echo "  build-mini-projects   Rebuild mini-projects.md from /docs/projects"
	@echo "  build-project-browser Generate the project_browser.html"
	@echo "  build-all             Sync version, rebuild docs and project browser"
	@echo "  release               Tag, build, and publish to PyPI"
	@echo "  release-test          Publish to TestPyPI"
	@echo "  clean                 Remove temporary build/test artifacts"
	@echo "  help                  Show this help message"
