# Chat Module CLI Guide

This guide explains how to use the Chat module's command-line interface (CLI) to interact with educational chatbot personalities powered by any OpenAI-compatible provider.

## 📦 Installation

Once HandsOnAI is installed with pip:

```bash
pip install hands-on-ai
```

You'll have access to the chat CLI tool:

```bash
chat --help
```

---

## 💬 Basic Commands

### Ask a Single Prompt
Send a question to a selected personality:

```bash
chat ask "What is Python used for?" --personality coder
```

By default, the `friendly` bot is used unless another personality is specified.

### List Available Bots

```bash
chat bots
```

Displays all personality bots with a brief description.

### Check System (Doctor)

```bash
chat doctor
```

Performs a diagnostic to check if your configured LLM provider is reachable and responding.

---

## 🖥️ Interactive Mode (REPL)

Run:

```bash
chat interactive
```

This opens a text-based, stateless REPL (Read-Eval-Print Loop).

## 🌐 Web Interface

Launch a web interface to chat with personality bots:

```bash
chat web
```

By default, the interface is only accessible from your local machine. To make it accessible from other devices on your network:

```bash
chat web --public
```

> ⚠️ When using the `--public` flag, the interface will be accessible to anyone on your network. Use with caution.

You can also specify a custom port (default is 8000):

```bash
chat web --port 8888
```

### REPL Commands

Use commands prefixed with `/` inside the REPL:

| Command               | Description |
|-----------------------|-------------|
| `/help`              | Show help menu |
| `/exit`              | Exit the REPL |
| `/bots`              | List available bot personalities |
| `/personality NAME`  | Switch to a different bot |
| `/doctor`            | Check LLM provider status |

> ❗ This REPL is stateless: it does not retain memory or chat history between turns.

---

## 🧠 Custom Personalities

HandsOnAI chat bots are defined as simple Python functions using `get_response()`. You can create your own bots or extend existing ones.

All built-in bots are available via:

```python
from chat import friendly_bot, pirate_bot, coder_bot, ...
```

---

## 🧪 Troubleshooting

- If you see connection errors, check that your LLM provider is running and accessible.
- For local Ollama: ensure Ollama is running on your machine.
- For cloud providers: verify your API key and server URL are correct.
- Use `chat doctor` for diagnostics.
- To change configuration, set `HANDS_ON_AI_SERVER` and `HANDS_ON_AI_API_KEY` environment variables.

```bash
# For local Ollama
export HANDS_ON_AI_SERVER=http://remote-server:11434

# For cloud providers
export HANDS_ON_AI_SERVER=https://api.openai.com
export HANDS_ON_AI_API_KEY=your-api-key
```

---

## 📚 Related Docs

- [Ollama Setup Guide](./ollama-guide.md) - For local LLM setup
- [Configuration Guide](./configuration.md) - For provider setup
- [Mini Projects](./projects/index.md)
- [Education Guide](./education-guide.md)

---

*The HandsOnAI Chat CLI is designed for educational use, rapid prototyping, and personality-driven chatbot interaction.*

For more advanced usage, consider integrating HandsOnAI directly into your Python projects using the `hands_on_ai.chat` module.