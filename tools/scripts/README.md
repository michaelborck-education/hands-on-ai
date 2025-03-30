# AiLabKit Development Scripts

This directory contains utility scripts for AiLabKit development and maintenance.

## Available Scripts

### `update_mini_projects.py`

Updates the code examples in all mini-project markdown files to use the new `ailabkit.chat` module instead of the old `chatcraft` module.

**Usage:**
```bash
# Run directly
python tools/scripts/update_mini_projects.py

# Or use the make/just targets
make update-mini-projects
just update-mini-projects
```

This script searches for common patterns in the mini-project files such as:
- Import statements: `from chatcraft import...` → `from ailabkit.chat import...`
- Module references: `chatcraft.personalities` → `ailabkit.chat.personalities`
- CLI commands: `chatcraft interactive` → `ailabkit chat interactive`

The script is automatically included in the `build-all` workflow.

### `convert_spelling.py`

Converts American English spelling to Australian/British English spelling in documentation files.

**Usage:**
```bash
# Run on all documentation files
python tools/scripts/convert_spelling.py --verbose

# Or use the make/just targets
make spelling-au
just spelling-au

# Run in dry-run mode to see what would change without making changes
python tools/scripts/convert_spelling.py --dry-run --verbose

# Process a specific file
python tools/scripts/convert_spelling.py --file path/to/file.md --verbose

# Process a different directory
python tools/scripts/convert_spelling.py --dir ./other-docs --verbose

# Specify which file extensions to process
python tools/scripts/convert_spelling.py --extensions .md,.txt --verbose
```

This script converts common American spelling patterns to Australian/British spelling:
- -or → -our (color → colour, flavor → flavour)
- -ize → -ise (organize → organise, recognize → recognise)
- -yze → -yse (analyze → analyse)
- -ense → -ence (defense → defence)
- -ter → -tre (center → centre)
- And many specific word changes (gray → grey, program → programme)

The script intelligently skips code blocks, YAML frontmatter, and HTML blocks to avoid changing code or markup. It also includes an exclusion list for technical terms that should retain American spelling.