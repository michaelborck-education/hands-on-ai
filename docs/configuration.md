# Hands-On AI Configuration Guide

This document outlines how to configure Hands-On AI for different environments and usage needs. Hands-On AI is designed to be flexible and educator-friendly, supporting both local development and classroom deployment.

---

## 🔧 Configuration Priorities

Hands-On AI supports configuration via the following priority order:

1. **Environment Variables** (highest priority)
2. **User Configuration File** (`~/.hands-on-ai/config.json`)
3. **Built-in Defaults** (fallback if no config found)

---

## 🧩 Configuration Options

The following options can be configured:

### `OLLAMA_HOST`
- **Description**: URL of the Ollama server to use
- **Default**: `http://localhost:11434`
- **Set via**:
  - Environment: `HANDS_ON_AI_SERVER=http://remote-server:11434`
  - Config File: `{ "server": "http://remote-server:11434" }`

### `API_KEY`
- **Description**: API key for authenticating with the Ollama server
- **Default**: None
- **Set via**:
  - Environment: `HANDS_ON_AI_API_KEY=your-api-key`
  - Config File: `{ "api_key": "your-api-key" }`

### `DEFAULT_MODEL`
- **Description**: Default model to use (e.g., `llama3`, `codellama`)
- **Default**: `llama3`
- **Set via**:
  - Environment: `HANDS_ON_AI_MODEL=codellama`
  - Config File: `{ "model": "codellama" }`

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

By default, Hands-On AI looks for a JSON config file at:
```
~/.hands-on-ai/config.json
```
Example:
```json
{
  "server": "http://192.168.1.42:11434",
  "model": "llama3",
  "default_personality": "coder",
  "timeout": 12,
  "api_key": "your-api-key"
}
```

---

## ⚙️ Developer Overrides

For local development or advanced use, Hands-On AI also supports fallback personality message overrides:

- `~/.hands-on-ai/chat_fallbacks.json` – user-specific overrides
- `hands_on_ai/chat/data/fallbacks.local.json` – local project overrides
- `hands_on_ai/chat/data/fallbacks.json` – default bundled fallback messages

---

## 🧪 Verifying Configuration

Run the built-in diagnostic command:
```
handsonai doctor
```
This will:
- Check the Ollama server connection
- Display the resolved configuration
- List available models (if reachable)

---

## 💡 Tips for Educators

- Create a shared classroom config file and distribute it to students (e.g., via `curl` script)
- Use environment variables to avoid hardcoding URLs into student projects
- Customise fallback personality messages for your learning context

---

## 🛠️ Related Commands

- `just doctor` – Run diagnostics
- `just repl` – Start CLI REPL
- `handsonai --help` – View CLI options

---

For advanced configuration of Ollama itself, refer to the [Ollama Guide](ollama-guide.md).

