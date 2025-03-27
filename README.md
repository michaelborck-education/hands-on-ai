# ChatCraft

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Classroom Ready](https://img.shields.io/badge/classroom-ready-brightgreen.svg)]()
[![Beginner Friendly](https://img.shields.io/badge/beginner-friendly-orange.svg)]()

> LLMs made simple for students and educators

## What is ChatCraft?

ChatCraft is a lightweight Python wrapper that simplifies interactions with Large Language Models (LLMs) for educational settings. It abstracts away the complexity of API calls, model management, and error handling, allowing students to focus on learning programming concepts through engaging AI interactions.

With just a few lines of code, students can:
- Create personality-based chatbots
- Experiment with different LLM models
- Build creative applications without getting lost in technical details

![ChatCraft Demo](https://via.placeholder.com/800x400?text=ChatCraft+Demo)

## Why ChatCraft?

- **Low barrier to entry** - No API keys or complex setup required
- **Educational focus** - Designed for classrooms and coding workshops
- **Personality customization** - Students can express creativity by designing unique bot personalities
- **Local model support** - Works with Ollama and other local LLM runners
- **Error resilience** - Friendly fallbacks when things go wrong


📚 [Browse the Docs](https://your-org.github.io/chatcraft/)


## Installation

```bash
# Install from PyPI
pip install chatcraft

# Or directly from GitHub
pip install git+https://github.com/yourusername/chatcraft.git
```

### Prerequisites

- Python 3.6 or higher
- For local LLM usage: [Ollama](https://ollama.ai/) or similar local LLM server

## Quick Start

```python
from chatcraft import get_response, friendly_bot, pirate_bot

# Basic usage with default model
response = get_response("Tell me about planets")
print(response)

# Use a personality bot
pirate_response = pirate_bot("Tell me about sailing ships")
print(pirate_response)

# Create your own personality
def wizard_bot(prompt):
    return get_response(
        prompt, 
        system="You are a wise wizard who speaks in riddles and magical references.",
        personality="wizard"
    )

print(wizard_bot("What is the meaning of life?"))
```

## Included Bot Personalities

ChatCraft comes with several ready-to-use personalities:

- `friendly_bot` - A helpful, conversational assistant
- `pirate_bot` - Speaks like a pirate, arr! ☠️
- `emoji_bot` - Communicates primarily through emojis 🤔💭✨
- `teacher_bot` - Patient, educational responses
- `coder_bot` - Coding-focused assistant (uses CodeLlama by default)

## Classroom Examples

See the [mini_project_examples.md](docs/mini_project_examples.md) file for creative ways to use ChatCraft in education, including:

- Building custom personality bots
- Creating quiz systems
- Simulating conversations between different bot personalities
- Journal reflection assistants

## Configuration

ChatCraft looks for a config file at `~/.chatcraft/config.json`. Create this file to customize default settings:

```json
{
  "backend": "ollama",
  "host": "http://localhost:11434",
  "model": "llama3"
}
```

```txt
chatcraft/
├── chatcraft/                ← Source code (bots + get_response.pyx)
│   ├── __init__.py
│   ├── get_response.pyx
│   └── data/
│       └── fallbacks.json
│
├── docs/                     ← MkDocs documentation
│   ├── index.md
│   ├── bots.md
│   ├── ollama-guide.md
│   └── mini-projects.md
│
├── tests/                    ← Pytest tests
│   ├── test_response.py
│   └── test_version_sync.py
│
├── tools/                    ← Build/version utilities
│   ├── build_zip.py
│   ├── bump_version.py
│   ├── inject_version.py
│   └── generate_bot_gallery.py
│
├── .github/                  ← Optional GitHub Actions later
│   └── workflows/
│       └── ci.yml
│
├── justfile
├── Makefile
├── build.py
├── mkdocs.yml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── version.json
├── CONTRIBUTING.md
└── README.md
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get involved.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with education in mind
- Powered by open-source LLM technology
- Inspired by educators who want to bring AI into the classroom responsibly

# 🤝 Credits
# See AUTHORS.md and .mailmap for contributor info
# Co-authored by ChatGPT <chatcraft@openai.com>

---

*ChatCraft is not affiliated with any LLM providers. It's designed as an educational tool to simplify access to LLM technology.*