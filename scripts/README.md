# AiLabKit Scripts

This directory contains scripts and utilities for building, testing, and maintaining the AiLabKit project. These tools are used regularly as part of development and maintenance.

## Core Scripts

- **`build_mini_projects.py`**: Combines individual mini-project files into the combined docs/mini-projects.md
- **`build_zip.py`**: Creates a standalone offline bundle of AiLabKit
- **`convert_spelling.py`**: Converts American spelling to Australian/British spelling in documentation
- **`generate_bot_gallery.py`**: Generates the bot gallery markdown from available personalities
- **`inject_version.py`**: Ensures version consistency across the project
- **`lint_mini_projects.py`**: Lints mini-project files for proper format and required fields
- **`project_browser.py`**: Creates the HTML-based project browser

## Usage with justfile

The recommended way to use these scripts is via the `just` command:

```bash
# Regenerate mini-projects.md from individual files
just build-mini-projects

# Create the project browser HTML
just build-project-browser

# Lint mini-projects for required fields
just lint-mini-projects

# Convert spelling in documentation
just spelling-au

# Build the offline bundle
just bundle
```

## Tool Development Guidelines

When creating new tools for this directory:

1. **Proper Documentation**: Include docstrings and helpful comments.
2. **CLI Arguments**: Use [Typer](https://typer.tiangolo.com/) for command-line interfaces.
3. **Error Handling**: Provide clear error messages.
4. **justfile Integration**: Add commands to the justfile.
5. **README Updates**: Document the tool in this README.
6. **Dry Run**: When possible, include a `--dry-run` option for tools that modify files.

## Additional Resources

Visit the [archive](../archive/) directory for historical scripts used during the migration from ChatCraft to AiLabKit.