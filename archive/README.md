# AiLabKit Archive

This directory contains archived scripts and utilities that were used during the development and migration from ChatCraft to AiLabKit. These files are kept for historical reference but are not typically needed for regular development.

## Migration Scripts

Scripts used during the ChatCraft to AiLabKit transition:

- **`add_module_type.py`**: Adds or updates module type (chat, rag, agent) in mini-projects
- **`check_imports.py`**: Helps find and fix outdated import paths (from chatcraft to ailabkit)
- **`convert_references.py`**: Replaces all references to "ChatCraft" with "AiLabKit" in documentation
- **`convert_spelling_migration.py`**: Converts American spelling to Australian/British spelling in documentation
- **`markdown_converter.py`**: Utility for converting between markdown formats
- **`split.py`**: Splits the combined mini-projects.md file into individual project files
- **`update_mini_projects.py`**: Updates code examples to use ailabkit.chat instead of chatcraft

## Previous Versions of Current Scripts

Older versions of scripts that have been replaced by improved versions in the scripts/ directory:

- **`build_mini_projects_old.py`**: Previous version of the mini-projects builder
- **`build_zip_old.py`**: Previous version of the ZIP bundle builder
- **`convert_spelling_old.py`**: Previous version of the spelling converter
- **`generate_bot_gallery_old.py`**: Previous version of the bot gallery generator
- **`inject_version_old.py`**: Previous version of the version injector
- **`lint_mini_projects_old.py`**: Previous version of the mini-projects linter
- **`project_browser_old.py`**: Previous version of the project browser generator

## Notes

These scripts are not maintained and may not work with the current project structure. They are provided for reference only.

For current development tools, please use the scripts in the `scripts/` directory instead.