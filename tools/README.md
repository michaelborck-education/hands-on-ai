# AiLabKit Project Tools

This section documents the utility scripts and tools for AiLabKit development, documentation, and maintenance. These tools can help educators and students extend and customize AiLabKit for their own purposes.

## Overview

The tools in this directory help with tasks such as:

- Building and packaging AiLabKit
- Generating and maintaining documentation
- Converting between American and Australian/British spelling
- Updating module references after code restructuring
- Checking import statements
- Managing mini-projects documentation

## Available Tools

### Documentation Tools

- **`build_mini_projects.py`**: Combines individual mini-project files into a single markdown document.
- **`generate_bot_gallery.py`**: Creates the bot gallery markdown from the available bot personalities.
- **`lint_mini_projects.py`**: Checks mini-project markdown files for formatting issues.
- **`build_project_browser.py`**: Generates an HTML-based browser for mini-projects.
- **`markdown_converter.py`**: Utility for converting between markdown formats.

### Build Tools

- **`build_zip.py`**: Creates an offline zip bundle of the project.
- **`inject_version.py`**: Synchronizes version numbers across project files.
- **`check_imports.py`**: Helps find and fix outdated import paths (from chatcraft to ailabkit).

### Scripts

The `scripts/` directory contains standalone scripts for specific tasks:

- **`update_mini_projects.py`**: Updates code examples to use the new `ailabkit.chat` module instead of the old `chatcraft` module.
- **`convert_spelling.py`**: Converts American English spelling to Australian/British English spelling in documentation files.

See [scripts/README.md](../tools/scripts/README.md) for more details about these scripts.

## Usage

Most tools can be run directly from the command line from the AiLabKit project root:

```bash
python tools/build_mini_projects.py
python tools/scripts/convert_spelling.py --verbose
```

However, it's recommended to use the make or just targets defined in the project:

```bash
# Using make
make build-mini-projects
make spelling-au

# Using just
just build-mini-projects
just spelling-au
```

These commands help when creating your own mini-projects, converting between regional spellings, or extending AiLabKit for classroom use.

## Tool Development Guidelines

When creating new tools for this directory:

1. **Proper Documentation**: Include docstrings and helpful comments.
2. **CLI Arguments**: Use argparse for command-line arguments.
3. **Error Handling**: Provide clear error messages.
4. **Make Integration**: Add commands to the Makefile and justfile.
5. **README Updates**: Document the tool in this README and any relevant subdirectory READMEs.
6. **Dry Run**: When possible, include a `--dry-run` option for tools that modify files.

## Configuration

Tool configuration can be found in:

- **`config.json`**: Contains shared configuration for tools.

## Getting Help

Run tools with `--help` flag to see available options:

```bash
python tools/scripts/convert_spelling.py --help
```