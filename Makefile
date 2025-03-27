# Makefile for common development tasks

.PHONY: install test build sync-version bundle lint format docs deploy-docs help

install:
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	ruff chatcraft tests tools

format:
	ruff format chatcraft tests tools

build:
	python build.py

bundle:
	python tools/build_zip.py

sync-version:
	python tools/inject_version.py

docs:
	mkdocs build --clean

deploy-docs:
	mkdocs gh-deploy --force

help:
	@echo "Make targets:"
	@echo "  install         Install dev dependencies"
	@echo "  test            Run tests with pytest"
	@echo "  lint            Run ruff linter"
	@echo "  format          Auto-format code with ruff"
	@echo "  build           Build and optionally upload"
	@echo "  bundle          Create offline zip"
	@echo "  sync-version    Sync version across files"
	@echo "  docs            Build MkDocs site"
	@echo "  deploy-docs     Deploy site to GitHub Pages"
	@echo "  help            Show this help message"
