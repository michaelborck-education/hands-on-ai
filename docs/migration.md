# Migration Guide: ChatCraft to ailabkit

This document outlines the migration from the original `chatcraft` package structure to the new modular `ailabkit` package.

## Package Structure Changes

### Before (ChatCraft):
```
chatcraft/
├── src/
│   └── chatcraft/
│       ├── __init__.py      # Bot definitions
│       ├── get_response.py  # Core LLM interaction
│       ├── config.py        # Configuration
│       ├── bots.py          # Bot discovery
│       ├── cli.py           # CLI commands
│       ├── data/            # Fallback data
│       └── ragcraft/        # RAG submodule
```

### After (ailabkit):
```
ailabkit/
├── src/
│   └── ailabkit/
│       ├── __init__.py      # Package exports
│       ├── config.py        # Shared configuration
│       ├── cli.py           # Meta CLI
│       ├── utils/           # Shared utilities
│       ├── chat/            # Chat module
│       │   ├── __init__.py
│       │   ├── get_response.py
│       │   ├── cli.py
│       │   ├── personalities/
│       │   │   ├── __init__.py
│       │   │   ├── friendly.py
│       │   │   ├── creative.py
│       │   │   └── bots/
│       │   │       ├── friendly_bot.py
│       │   │       └── ...
│       │   ├── commands/
│       │   └── data/
│       ├── rag/             # RAG module
│       │   ├── __init__.py
│       │   ├── utils.py
│       │   ├── cli.py
│       │   └── commands/
│       └── agent/           # Agent module
│           ├── __init__.py
│           ├── core.py
│           ├── cli.py
│           ├── commands/
│           └── tools/
```

## Key Changes

1. **Modular Organisation:**
   - Each functionality (chat, rag, agent) is now a separate submodule
   - Each submodule has its own CLI, commands, and functionality
   - Shared configuration in central config.py

2. **Personality Structure:**
   - Individual bot files for easy contribution
   - Category grouping for logical organisation
   - Three ways to import bots:
     - From individual files: `from ailabkit.chat.personalities.bots import friendly_bot`
     - From categories: `from ailabkit.chat.personalities.creative import *`
     - From the main module: `from ailabkit.chat import *`

3. **Command Structure:**
   - Each command is in its own file in a `commands/` directory
   - Main CLI file imports and registers all commands
   - Consistent pattern across all submodules

4. **Configuration:**
   - Centralised configuration in ailabkit/config.py
   - Environment variables renamed from CHATCRAFT_* to AILABKIT_*
   - Configuration directory ~/.chatcraft -> ~/.ailabkit

5. **Entry Points:**
   - Multiple CLI entry points:
     - `ailabkit` - Meta CLI
     - `chat` - Chat functionality
     - `rag` - RAG functionality
     - `agent` - Agent functionality

## Migration Steps for End Users

1. Uninstall old package:
   ```
   pip uninstall chatcraft
   ```

2. Install new package:
   ```
   pip install ailabkit
   ```

3. Update import statements:
   - `from chatcraft import friendly_bot` → `from ailabkit.chat import friendly_bot`
   - `from chatcraft import get_response` → `from ailabkit.chat import get_response`

4. Update CLI commands:
   - `chatcraft bots` → `chat bots`
   - `chatcraft ask` → `chat ask`
   - `ragcraft ask` → `rag ask`

5. Update configuration:
   - Rename ~/.chatcraft to ~/.ailabkit
   - Update environment variables

## Migration Steps for Developers

1. Understand the new module structure
2. Create PRs against the correct submodule
3. Follow the new patterns for commands and functionality
4. Use test_ailabkit.py to verify changes