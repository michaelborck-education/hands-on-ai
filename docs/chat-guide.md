# ChatCraft CLI Guide

This guide explains how to use the ChatCraft command-line interface (CLI) to interact with educational chatbot personalities powered by Ollama.

## 📦 Installation

Once ChatCraft is installed with pip:

```bash
uv pip install -e '.[dev]'
```

You’ll have access to a CLI tool:

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

Performs a diagnostic to check if the Ollama server is reachable and responding.

---

## 🖥️ Interactive Mode (REPL)

Run:

```bash
chat interactive
```

This opens a text-based, stateless REPL (Read-Eval-Print Loop).

### REPL Commands

Use commands prefixed with `/` inside the REPL:

| Command               | Description |
|-----------------------|-------------|
| `/help`              | Show help menu |
| `/exit`              | Exit the REPL |
| `/bots`              | List available bot personalities |
| `/personality NAME`  | Switch to a different bot |
| `/doctor`            | Check Ollama server status |

> ❗ This REPL is stateless: it does not retain memory or chat history between turns.

---

## 🧠 Custom Personalities

ChatCraft bots are defined as simple Python functions using `get_response()`. You can create your own bots or extend existing ones.

All built-in bots are available via:

```python
from chat import friendly_bot, pirate_bot, coder_bot, ...
```

---

## 🧪 Troubleshooting

- If you see `❌ Ollama server not reachable`, ensure Ollama is running on your machine.
- Use `chat doctor` for diagnostics.
- To change the server URL, set the `OLLAMA_HOST` environment variable.

```bash
export OLLAMA_HOST=http://remote-server:11434
```

---

## 📚 Related Docs

- [Ollama Setup Guide](./ollama-guide.md)
- [Mini Projects](./mini-projects.md)
- [Education Guide](./education-guide.md)

---

*ChatCraft CLI is designed for educational use, rapid prototyping, and personality-driven chatbot interaction.*

For more advanced usage, consider integrating ChatCraft into your Python projects using the `chat` library.