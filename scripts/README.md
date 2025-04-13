# Hands-On AI Project Tools

This directory contains utility scripts used for development, maintenance, and building Hands-On AI documentation and resources.

## Mini-Projects Tools

- **`build_mini_projects.py`**: Compiles all individual project files into a single mini-projects.md file
  - Usage: `python scripts/build_mini_projects.py`
  - Run with `just build-mini-projects`

- **`split_mini_projects.py`**: Splits a markdown file with level-1 headers into individual project files
  - Usage: `python scripts/split_mini_projects.py --input docs/mini-projects.md --output-dir docs/projects/`
  - Used to create individual project files from the main mini-projects document

- **`lint_mini_projects.py`**: Checks mini-project files for correct formatting and structure
  - Usage: `python scripts/lint_mini_projects.py [--dir DIRECTORY]`
  - Validates project files against the expected format

- **`project_browser.py`**: Creates an interactive HTML browser for navigating mini-projects
  - Usage: `python scripts/project_browser.py`
  - Run with `just build-browser`

## Documentation Tools

- **`generate_bot_gallery.py`**: Generates the bot gallery markdown page from bot source files
  - Usage: `python scripts/generate_bot_gallery.py`
  - Run with `just build-gallery`

- **`convert_spelling.py`**: Converts American English spelling to Australian/British English
  - Usage: `python scripts/convert_spelling.py [--dir DIRECTORY]`
  - Useful for standardizing documentation

## Build Tools

- **`build_zip.py`**: Creates a ZIP file of the project for distribution
  - Usage: `python scripts/build_zip.py`
  - Run with `just build-zip`

- **`inject_version.py`**: Updates version information in package files
  - Usage: `python scripts/inject_version.py [VERSION]`
  - Used during the release process

## Using the Tools

Most of these tools can be run using the `just` command, which is a command runner defined in the project's `justfile`. For example:

```bash
just build-mini-projects  # Builds mini-projects.md
just build-gallery        # Generates the bot gallery
just build-browser        # Builds the project browser
just deploy-docs          # Deploys documentation to GitHub Pages
```

These tools are primarily intended for maintainers and contributors. Users of Hands-On AI generally do not need to run these scripts directly.

For more information on using Hands-On AI, please refer to the [official documentation](https://teaching-repositories.github.io/hands-on-ai/).