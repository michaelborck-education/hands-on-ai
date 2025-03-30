# Makefile for common development tasks

.PHONY: install-dev test test-basic lint format ci sync-version requirements build bundle docs deploy-docs chat-repl rag-repl agent-repl chat-web rag-web doctor build-mini-projects update-mini-projects spelling-au build-project-browser build-all release release-test help clean lint-mini-projects

# 🧪 Run and check
test:
	pytest

test-basic:
	python test_ailabkit.py

lint:
	ruff src/ailabkit tests tools

format:
	ruff format src/ailabkit tests tools

ci: lint test

# 🔧 Project setup
install-dev:
	pip install -r requirements-dev.txt

sync-version:
	python tools/inject_version.py --all
	@echo "✅ Synced version across pyproject.toml and version.json"

requirements:
	uv pip compile pyproject.toml --output-file=requirements.txt
	uv pip compile pyproject.toml --extra=dev --output-file=requirements-dev.txt
	@echo "✅ Regenerated requirements.txt and requirements-dev.txt"

# 🏗️ Build and distribute
build:
	python -m build

bundle:
	python tools/build_zip.py

# 📚 Documentation
docs:
	mkdocs build --clean

deploy-docs:
	mkdocs gh-deploy --force

# 🧪 Run CLI modules in interactive mode
chat-repl:
	ailabkit chat interactive

rag-repl:
	ailabkit rag interactive

agent-repl:
	ailabkit agent interactive

# 🌐 Run web interfaces
chat-web:
	ailabkit chat web

rag-web:
	ailabkit rag web

# 🩺 Run diagnostic check
doctor:
	ailabkit doctor

# 🔧 Rebuild mini-projects markdown from individual project files
build-mini-projects:
	python tools/build_mini_projects.py

# 🔄 Update mini-projects code examples to use ailabkit.chat
update-mini-projects:
	python tools/scripts/update_mini_projects.py

# 🇦🇺 Convert American spelling to Australian/British spelling in docs
spelling-au:
	python tools/scripts/convert_spelling.py --verbose

# 🌐 Regenerate HTML-based project browser
build-project-browser:
	python tools/project_browser.py

# Lint mini-projects markdown files
lint-mini-projects:
	python tools/lint_mini_projects.py

# 🛠️ Rebuild everything: sync version, docs, browser, mini-projects
build-all: sync-version update-mini-projects build-mini-projects build-project-browser docs

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
	@echo "  test                  Run all tests with pytest"
	@echo "  test-basic            Run basic imports test directly"
	@echo "  lint                  Run Ruff linter"
	@echo "  format                Auto-format code with Ruff"
	@echo "  build                 Build package with python -m build"
	@echo "  bundle                Create offline zip"
	@echo "  sync-version          Sync version across files"
	@echo "  requirements          Regenerate requirements.txt and requirements-dev.txt"
	@echo "  docs                  Build MkDocs site"
	@echo "  deploy-docs           Deploy site to GitHub Pages"
	@echo "  chat-repl             Start AiLabKit chat interactive mode"
	@echo "  rag-repl              Start AiLabKit RAG interactive mode"
	@echo "  agent-repl            Start AiLabKit agent interactive mode"
	@echo "  chat-web              Start AiLabKit chat web interface"
	@echo "  rag-web               Start AiLabKit RAG web interface"
	@echo "  doctor                Run system diagnostic for AiLabKit"
	@echo "  build-mini-projects   Rebuild mini-projects.md from /docs/projects"
	@echo "  update-mini-projects  Update code in mini-projects to use ailabkit.chat"
	@echo "  spelling-au           Convert American spelling to Australian/British spelling"
	@echo "  lint-mini-projects    Lint mini-projects.md files"
	@echo "  build-project-browser Generate the project_browser.html"
	@echo "  build-all             Sync version, rebuild docs and project browser"
	@echo "  release               Tag, build, and publish to PyPI"
	@echo "  release-test          Publish to TestPyPI"
	@echo "  clean                 Remove temporary build/test artifacts"
	@echo "  help                  Show this help message"