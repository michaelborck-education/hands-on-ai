# 🤝 Contributing to ChatCraft

Thanks for your interest in contributing to ChatCraft! Whether you're fixing a typo, writing a bot, improving documentation, or adding a new feature — you're welcome here.


## Ways to Contribute

There are many ways to contribute to ChatCraft:

1. **Add new bot personalities**: Create creative, educational, or specialized bot personalities.
2. **Bug fixes**: Help identify and fix bugs in the existing codebase.
3. **Documentation**: Improve the project documentation, tutorials, or examples.
4. **Feature enhancements**: Add new features or enhance existing ones.
5. **Educational content**: Create classroom activities, lesson plans, or educational guides.

## Getting Started

1. **Fork the repository**: Create your own fork of the ChatCraft repository.
2. **Clone your fork**: `git clone https://github.com/your-username/chatcraft.git`
3. **Create a branch**: `git checkout -b my-contribution`
4. **Make your changes**: Implement your contribution.
5. **Test your changes**: Ensure your code works as expected.
6. **Submit a pull request**: Push your changes to your fork and open a pull request.

## Development Environment

1. Install Python 3.6 or higher.
2. Install the development dependencies:
   ```
   pip install -e ".[dev]"
   ```
3. For testing LLM functionality, install [Ollama](https://ollama.ai/) or configure another LLM backend.

## Code Style Guidelines

- Follow PEP 8 style guidelines for Python code.
- Use clear, descriptive variable and function names.
- Include docstrings for all functions, classes, and modules.
- Add comments for complex or non-obvious code sections.
- Keep lines to a maximum of 88 characters.

## Adding a New Bot Personality

To add a new bot personality:

1. Open `__init__.py` in the main package.
2. Add a new function for your bot, following the existing pattern:
   ```python
   def your_bot_name(prompt):
       return get_response(
           prompt, 
           system="Your system prompt here.", 
           personality="your_personality_name"
       )
   ```
3. Add your bot to the `__all__` list.
4. Add appropriate fallback messages in `data/fallback.jsom`.
5. Document your bot in the README.md and other relevant documentation.

## Adding Documentation

If you're adding documentation:

1. Place general documentation in the `docs/` directory.
2. Ensure educational materials are appropriate for classroom use.
3. Include clear examples and explanations.
4. Specify the target audience (grade level, experience level).

## Testing

Before submitting a pull request:

1. Test your code with multiple inputs.
2. Ensure it works with the default Ollama backend.
3. Check for any error conditions or edge cases.

## Pull Request Process

1. Update the README.md and documentation with details of changes if applicable.
2. Update the version number following [Semantic Versioning](https://semver.org/).
3. Your pull request will be reviewed by maintainers who may request changes.
4. Once approved, your pull request will be merged.


## 🧰 Development Setup

1. **Clone the repository**
2. **Install dev dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```
   Or if you're using Poetry-compatible tools:
   ```bash
   pip install .[dev]
   ```

## 🔧 Common Commands

Use either `just <task>` or `make <task>`:

| Task | Description |
|------|-------------|
| `test` | Run tests using pytest |
| `lint` | Lint code with Ruff |
| `format` | Auto-format with Ruff |
| `build` | Build the Python package |
| `bundle` | Create offline zip of project_browser |
| `sync-version` | Sync version across HTML and TOML |
| `docs` | Build static site with MkDocs |
| `deploy-docs` | Deploy to GitHub Pages |

## 🤖 Bot Contributions

To add a new bot:
1. Define the function in `chatcraft/__init__.py`
2. Follow the pattern: `def <name>_bot(prompt): ...`
3. Include a meaningful docstring with:
   - Usage example
   - Educational uses
   - Example response
4. Add an entry to `fallbacks.json` (optional)

## 🧪 Testing
Add your tests in `tests/`. For bots, test both:
- Basic output (non-empty)
- Empty prompt handling

## 📚 Documentation
Bot docstrings are auto-documented using `mkdocstrings`. Update `docs/bots.md` only if you're changing layout or structure.

## ❤️ Thanks
Thanks for helping make ChatCraft better for educators and students everywhere!

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## Questions?

If you have questions about contributing, open an issue in the repository or contact the maintainers directly.

Thank you for contributing to ChatCraft and helping make AI education more accessible!