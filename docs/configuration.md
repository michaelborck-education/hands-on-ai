# Hands-On AI Configuration Guide

This document outlines how to configure Hands-On AI for different environments and usage needs. Hands-On AI is designed to be flexible and educator-friendly, supporting both local development and classroom deployment with any OpenAI-compatible provider.

---

## 🌍 Provider-Agnostic Configuration

HandsOnAI works with **any OpenAI-compatible LLM provider**. The system uses standard OpenAI API endpoints making it compatible with Ollama, OpenAI, OpenRouter, Together AI, and many other providers.

---

## 🔧 Configuration Priorities

Hands-On AI supports configuration via the following priority order:

1. **Environment Variables** (highest priority)
2. **User Configuration File** (`~/.hands-on-ai/config.json`)
3. **Built-in Defaults** (fallback if no config found)

---

## 🧩 Configuration Options

The following options can be configured:

### `HANDS_ON_AI_SERVER`
- **Description**: Base URL of your OpenAI-compatible LLM provider
- **Default**: `http://localhost:11434` (local Ollama)
- **Examples**:
  - Local Ollama: `http://localhost:11434`
  - OpenAI: `https://api.openai.com`
  - OpenRouter: `https://openrouter.ai/api`
  - Together AI: `https://api.together.xyz`
- **Set via**:
  - Environment: `HANDS_ON_AI_SERVER=https://your-provider.com`
  - Config File: `{ "server": "https://your-provider.com" }`

### `HANDS_ON_AI_API_KEY`
- **Description**: API key for authenticating with your provider (Bearer token)
- **Default**: None (not needed for local Ollama)
- **Set via**:
  - Environment: `HANDS_ON_AI_API_KEY=your-api-key`
  - Config File: `{ "api_key": "your-api-key" }`

### `HANDS_ON_AI_MODEL`
- **Description**: Default model to use
- **Default**: `llama3`
- **Examples**:
  - Ollama: `llama3`, `codellama`, `mistral`
  - OpenAI: `gpt-4`, `gpt-3.5-turbo`
  - OpenRouter: `openai/gpt-4`, `anthropic/claude-3-sonnet`
- **Set via**:
  - Environment: `HANDS_ON_AI_MODEL=gpt-4`
  - Config File: `{ "model": "gpt-4" }`

### `HANDS_ON_AI_EMBEDDING_MODEL`
- **Description**: Model to use for embeddings (RAG module)
- **Default**: `nomic-embed-text`
- **Set via**:
  - Environment: `HANDS_ON_AI_EMBEDDING_MODEL=text-embedding-ada-002`
  - Config File: `{ "embedding_model": "text-embedding-ada-002" }`

### `HANDS_ON_AI_LOG`
- **Description**: Enable debug logging
- **Default**: None (warnings only)
- **Set via**:
  - Environment: `HANDS_ON_AI_LOG=debug`

---

## 📁 Configuration File Location

By default, Hands-On AI looks for a JSON config file at:
```
~/.hands-on-ai/config.json
```
## 🎓 Configuration Examples

### For Students (Beginner-Friendly)
Set configuration directly in your Python code:
```python
import os

# Configure your provider  
os.environ['HANDS_ON_AI_SERVER'] = 'https://ollama.serveur.au'
os.environ['HANDS_ON_AI_MODEL'] = 'llama3.2'
os.environ['HANDS_ON_AI_API_KEY'] = input('Enter your API key: ')

# Now use HandsOnAI
from hands_on_ai.chat import get_response
response = get_response("What is machine learning?")
print(response)
```

### Configuration File Example
```json
{
  "server": "https://api.openai.com",
  "model": "gpt-4",
  "embedding_model": "text-embedding-ada-002",
  "api_key": "sk-your-openai-key",
  "chunk_size": 1000
}
```

### Provider-Specific Examples

#### Local Ollama
```json
{
  "server": "http://localhost:11434",
  "model": "llama3"
}
```

#### OpenRouter (Multiple Providers)
```json
{
  "server": "https://openrouter.ai/api",
  "model": "openai/gpt-4",
  "api_key": "sk-or-your-openrouter-key"
}
```

---

## ⚙️ Advanced Features

### Fallback Message Customization
For local development or advanced use, Hands-On AI also supports fallback personality message overrides:

- `~/.hands-on-ai/chat_fallbacks.json` – user-specific overrides
- `hands_on_ai/chat/data/fallbacks.local.json` – local project overrides
- `hands_on_ai/chat/data/fallbacks.json` – default bundled fallback messages

---

## 🧪 Verifying Configuration

Run the built-in diagnostic command:
```bash
handsonai doctor
```
This will:
- Check your provider connection
- Display the resolved configuration  
- List available models (if reachable)
- Verify API key authentication

---

## 💡 Tips for Educators

- **Classroom Setup**: Provide students with your server URL and API keys
- **Environment Variables**: Use environment variables to avoid hardcoding URLs
- **Provider Choice**: Start with local Ollama for privacy, switch to cloud providers for advanced models
- **Configuration Distribution**: Share config files via classroom management tools

### Suggested Classroom Setup
```python
# Add this to the top of all student exercises
import os
os.environ['HANDS_ON_AI_SERVER'] = 'https://your-classroom-server.edu'
os.environ['HANDS_ON_AI_API_KEY'] = 'classroom-api-key'
```

---

## 🛠️ Related Commands

- `handsonai doctor` – Run diagnostics
- `handsonai --help` – View CLI options
- `chat --help` – Chat module help
- `agent --help` – Agent module help
- `rag --help` – RAG module help

---

## 📚 Related Documentation

- [Provider Compatibility](../README.md#provider-compatibility) - Full list of supported providers
- [Classroom Setup](classroom-setup.md) - Setting up HandsOnAI for education
- [Ollama Guide](ollama-guide.md) - Local Ollama installation and setup

