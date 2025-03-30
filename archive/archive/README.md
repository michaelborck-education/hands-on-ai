# Migration Scripts Archive

This directory contains scripts that were used during the migration from ChatCraft to AiLabKit. These scripts are kept for historical reference but are not typically needed for regular development.

## Available Scripts

- **`add_module_type.py`**: Adds or updates module type (chat, rag, agent) in mini-projects
- **`check_imports.py`**: Helps find and fix outdated import paths (from chatcraft to ailabkit)
- **`convert_references.py`**: Replaces all references to "ChatCraft" with "AiLabKit" in documentation
- **`convert_spelling.py`**: Converts American spelling to Australian/British spelling in documentation
- **`markdown_converter.py`**: Utility for converting between markdown formats
- **`split.py`**: Splits the combined mini-projects.md file into individual project files
- **`update_mini_projects.py`**: Updates code examples to use ailabkit.chat instead of chatcraft

## Notes

These scripts were primarily used during the transition period and initial structuring of the project. They are not maintained and may not work with the current project structure.

If you need to perform similar tasks, consider adapting these scripts or creating new ones in the main scripts directory.