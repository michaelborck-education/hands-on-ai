# ChatCraft Configuration Guide

This document outlines how to configure ChatCraft for different environments and usage needs. ChatCraft is designed to be flexible and educator-friendly, supporting both local development and classroom deployment.

---

## 🔧 Configuration Priorities

ChatCraft supports configuration via the following priority order:

1. **Environment Variables** (highest priority)
2. **User Configuration File** (`~/.chatcraft/config.json`)
3. **Built-in Defaults** (fallback if no config found)

---

## 🧩 Configuration Options

The following options can be configured:

### `OLLAMA_HOST`
- **Description**: URL of the Ollama server to use
- **Default**: `http://localhost:11434`
- **Set via**:
  - Environment: `OLLAMA_HOST=http://remote-server:11434`
  - Config File: `{ "ollama_host": "http://remote-server:11434" }`

### `DEFAULT_MODEL`
- **Description**: Default model to use (e.g., `llama3`, `codellama`)
- **Default**: `llama3`
- **Set via**:
  - Environment: `DEFAULT_MODEL=codellama`
  - Config File: `{ "default_model": "codellama" }`

### `DEFAULT_PERSONALITY`
- **Description**: Default bot personality for REPL and CLI
- **Default**: `friendly`
- **Set via**:
  - Environment: `DEFAULT_PERSONALITY=hacker`
  - Config File: `{ "default_personality": "hacker" }`

### `TIMEOUT`
- **Description**: Request timeout (in seconds)
- **Default**: `10`
- **Set via**:
  - Environment: `CHATCRAFT_TIMEOUT=15`
  - Config File: `{ "timeout": 15 }`

---

## 📁 Configuration File Location

By default, ChatCraft looks for a JSON config file at:
```
~/.chatcraft/config.json
```
Example:
```json
{
  "ollama_host": "http://192.168.1.42:11434",
  "default_model": "llama3",
  "default_personality": "coder",
  "timeout": 12
}
```

---

## ⚙️ Developer Overrides

For local development or advanced use, ChatCraft also supports fallback personality message overrides:

- `~/.chatcraft/fallbacks.json` – user-specific overrides
- `chatcraft/data/fallbacks.local.json` – local project overrides
- `chatcraft/data/fallbacks.json` – default bundled fallback messages

---

## 🧪 Verifying Configuration

Run the built-in diagnostic command:
```
chatcraft doctor
```
This will:
- Check the Ollama server connection
- Display the resolved configuration
- List available models (if reachable)

---

## 💡 Tips for Educators

- Create a shared classroom config file and distribute it to students (e.g., via `curl` script)
- Use environment variables to avoid hardcoding URLs into student projects
- Customize fallback personality messages for your learning context

---

## 🛠️ Related Commands

- `just doctor` – Run diagnostics
- `just repl` – Start CLI REPL
- `chatcraft --help` – View CLI options

---

For advanced configuration of Ollama itself, refer to the [Ollama Guide](ollama-guide.md).

