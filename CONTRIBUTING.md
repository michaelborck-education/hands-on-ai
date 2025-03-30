# 🤝 Contributing to AiLabKit

Thanks for your interest in contributing to AiLabKit! Whether you're fixing a typo, writing a bot, improving documentation, or adding a new feature — you're welcome here.

## Ways to Contribute

There are many ways to contribute to AiLabKit:

1. **Add new bot personalities**: Create creative, educational, or specialized bot personalities for the chat module.
2. **Enhance RAG capabilities**: Improve document processing, indexing, or retrieval in the RAG module.
3. **Extend agent functionality**: Add new tools or capabilities to the agent module.
4. **Bug fixes**: Help identify and fix bugs in the existing codebase.
5. **Documentation**: Improve the project documentation, tutorials, or examples.
6. **Feature enhancements**: Add new features or enhance existing ones.
7. **Educational content**: Create classroom activities, lesson plans, or educational guides.

## 🧰 Development Setup

1. **Fork the repository**: Create your own fork of the AiLabKit repository.
2. **Clone your fork**: `git clone https://github.com/your-username/ailabkit.git`
3. **Install Python 3.8 or higher**.
4. **Install dev dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```
   Or install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```
5. **For testing LLM functionality**: Install [Ollama](https://ollama.ai/) or configure another LLM backend.

## 🔧 Common Commands

Use either `just <task>` or `make <task>`:

| Task | Description |
|------|-------------|
| `test` | Run all tests using pytest |
| `test-basic` | Run basic imports test |
| `lint` | Lint code with Ruff |
| `format` | Auto-format with Ruff |
| `build` | Build the Python package |
| `bundle` | Create offline zip bundle |
| `sync-version` | Sync version across files |
| `docs` | Build static site with MkDocs |
| `deploy-docs` | Deploy to GitHub Pages |
| `chat-repl` | Start chat module in interactive mode |
| `rag-repl` | Start RAG module in interactive mode |
| `agent-repl` | Start agent module in interactive mode |
| `chat-web` | Start chat web interface |
| `rag-web` | Start RAG web interface |

## Development Workflow

1. **Create a branch**: `git checkout -b my-contribution`
2. **Make your changes**: Implement your contribution.
3. **Test your changes**: Ensure your code works as expected.
4. **Submit a pull request**: Push your changes to your fork and open a pull request.

## Code Style Guidelines

- Follow PEP 8 style guidelines for Python code.
- Use clear, descriptive variable and function names.
- Include docstrings for all functions, classes, and modules.
- Add comments for complex or non-obvious code sections.
- Keep lines to a maximum of 100 characters.

## 🤖 Adding a New Bot Personality

To add a new bot personality to the chat module:

1. Decide whether your bot fits into an existing personality category (educational, creative, technical, etc.)
2. Create a new bot file in the appropriate directory:
   - For a standard category bot: `src/ailabkit/chat/personalities/your_bot.py`
   - For a specialized bot: `src/ailabkit/chat/personalities/bots/your_bot.py`
3. Follow the pattern:
   ```python
   def your_bot_name(prompt):
       """Your bot description.
       
       Usage:
           from ailabkit.chat import your_bot_name
           your_bot_name("Your prompt here")
           
       Educational uses:
           - List educational applications
           
       Example:
           >>> your_bot_name("Hello!")
           "Your example response"
       """
       from ailabkit.chat.get_response import get_response
       return get_response(
           prompt, 
           system="Your system prompt here.", 
           personality="your_personality_name"
       )
   ```
4. Import and expose your bot in the appropriate `__init__.py` files:
   - Add to the category's `__init__.py` 
   - Make sure it's imported in `src/ailabkit/chat/personalities/__init__.py`
   - Include it in `src/ailabkit/chat/__init__.py`
5. Add appropriate fallback messages in `src/ailabkit/chat/data/fallbacks.json`.
6. Document your bot in the appropriate documentation files.

## 📚 Extending RAG Module

To extend the RAG (Retrieval-Augmented Generation) capabilities:

1. Understand the existing components:
   - Document loading and processing in `src/ailabkit/rag/utils.py`
   - Index creation and searching functionality
   - Query processing and response generation
2. Consider adding:
   - New document format support
   - Improved chunking strategies
   - Enhanced embedding techniques
   - Better retrieval algorithms
   - UI/UX improvements for the web interface
3. Ensure your changes:
   - Handle errors gracefully
   - Scale well with larger document collections
   - Maintain or improve search quality

## 🛠️ Extending Agent Module

To extend the agent module with new tools or capabilities:

1. Add new tools to `src/ailabkit/agent/tools/`
2. Follow the existing tool pattern
3. Update the relevant command handlers in `src/ailabkit/agent/commands/`
4. Document your new tools and their capabilities
5. Ensure your tools work well with the agent framework

## Adding Documentation

If you're adding documentation:

1. Place general documentation in the `docs/` directory.
2. Ensure educational materials are appropriate for classroom use.
3. Include clear examples and explanations.
4. Specify the target audience (grade level, experience level).
5. Module documentation should be added to the appropriate section.

## 🧪 Testing

Before submitting a pull request:

1. Add your tests in `tests/`.
2. For bots, test both:
   - Basic output (non-empty)
   - Empty prompt handling
3. For RAG extensions, test:
   - Document processing
   - Search functionality
   - Edge cases with unusual inputs
4. For agent tools, test:
   - Input validation
   - Error handling
   - Expected outputs
5. Test your code with multiple inputs.
6. Ensure it works with the default Ollama backend.
7. Check for any error conditions or edge cases.

## Pull Request Process

1. Update the documentation with details of changes if applicable.
2. Update the version number following [Semantic Versioning](https://semver.org/).
3. Your pull request will be reviewed by maintainers who may request changes.
4. Once approved, your pull request will be merged.

## Code of Conduct

Please note that this project follows standard open-source community guidelines for respectful and inclusive participation. By contributing to this project, you agree to maintain a positive and supportive environment for all participants.

## Questions?

If you have questions about contributing, open an issue in the repository or contact the maintainers directly.

## ❤️ Thanks

Thanks for helping make AiLabKit better for educators and students everywhere!