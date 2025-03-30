# ailabkit: Your AI Learning Lab

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/licence-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Classroom Ready](https://img.shields.io/badge/classroom-ready-brightgreen.svg)]()
[![Beginner Friendly](https://img.shields.io/badge/beginner-friendly-orange.svg)]()

> AI learning made simple for students and educators

ailabkit is a unified educational toolkit designed to teach students how modern AI systems work — by building and interacting with them directly.

It provides a clean, modular structure that introduces core AI concepts progressively through three tools:

## 🧱 Module Overview

| Module | Purpose | CLI Name |
|--------|---------|----------|
| chat | Simple chatbot with system prompts | chat |
| rag | Retrieval-Augmented Generation (RAG) | rag |
| agent | ReAct-style reasoning with tool use | agent |

Each module is:
- 🔌 Self-contained
- 🧩 Installable via one package: `pip install ailabkit`
- 🧠 Designed for progressive learning

## 🗂 Project Structure

```
ailabkit/
├── chat/           ← A simple prompt/response chatbot
├── rag/            ← Ask questions using your own documents
├── agent/          ← Agent reasoning + tools (ReAct-style)
├── config.py       ← Shared config (model, chunk size, paths)
├── cli.py          ← Meta CLI (list, config, version)
└── utils/          ← Shared tools, prompts, paths, etc.
```

## 🧑‍🏫 Why This Matters for Students

Each tool teaches a different level of modern AI interaction:

- **chat** – Prompt engineering, roles, and LLMs
- **rag** – Document search, embeddings, and grounded answers
- **agent** – Multi-step reasoning, tool use, and planning

## 🚀 Getting Started

### Installation

```bash
# Install from PyPI
pip install ailabkit

# Or directly from GitHub
pip install git+https://github.com/teaching-repositories/ailabkit.git
```

### Prerequisites

- Python 3.6 or higher
- For local LLM usage: [Ollama](https://ollama.ai/) or similar local LLM server

### Quick Start

Run a local Ollama server, then import and start chatting:

```python
from ailabkit.chat import pirate_bot
print(pirate_bot("What is photosynthesis?"))
```

For more options:

```python
from ailabkit.chat import get_response, friendly_bot, pirate_bot

# Basic usage with default model
response = get_response("Tell me about planets")
print(response)

# Use a personality bot
pirate_response = pirate_bot("Tell me about sailing ships")
print(pirate_response)
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get involved.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with education in mind
- Powered by open-source LLM technology
- Inspired by educators who want to bring AI into the classroom responsibly