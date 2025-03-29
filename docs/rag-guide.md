# 🧠 ChatCraft RAG Guide: Ask Questions About Your Notes

## Overview
ChatCraft now includes a **Simple RAG (Retrieval-Augmented Generation)** system. This lets you ask an LLM questions about your **own notes** (e.g., `.md`, `.txt`, `.pdf`, `.docx`) using a local model like Ollama.

You load your files → build an index → ask questions. That’s it!

---

## 📦 Optional: Install Word and PDF Support

To use `.pdf` and `.docx` files, install the extra RAG dependencies:

```bash
uv pip install .[rag]
```

Or with pip:

```bash
pip install chatcraft[rag]
```

---

## 🔧 Step 1: Build the RAG Index

You need to turn your `.md`, `.txt`, `.docx`, or `.pdf` file into an **indexed format** that the system can search.

### 🔨 Command:
```bash
python -m chatcraft.rag.build_index path/to/notes.pdf
```

- `notes.pdf` = your file (e.g., lecture notes, textbook, etc.)
- `default.npz` will be saved to `~/.chatcraft/.rag_index/` unless you specify a path

This will:
- Read your file
- Chunk the text (~500 words by default)
- Get embeddings via Ollama (`nomic-embed-text` by default)
- Save everything into `.npz` for later

> 💡 You only need to do this **once per file**, unless your notes change!

---

## 🔍 Step 2: Ask a Question (Query the Index)

Now that you’ve built an index, you can ask questions about it.

### 🧪 Command:
```bash
python -m chatcraft.rag.query_rag ask "What are the four layers of a firewall?"
```

This will:
- Embed your query
- Compare it to your notes
- Find the top 3 most relevant chunks
- Send those + your prompt to the LLM

You can also show the retrieved context:

```bash
python -m chatcraft.rag.query_rag ask "Explain DNS" --show-context --show-scores
```

---

## 🗨️ Step 2b: Use Interactive Mode

Use a simple REPL-style chat with your notes:

```bash
python -m chatcraft.rag.query_rag interactive
```

If no index exists, it will guide you through building one interactively!

---

## 🤖 Step 3: Use RAG in Code (like a bot)

You can use `rag_bot()` in your Python scripts, just like other ChatCraft bots:

```python
from chatcraft.rag import rag_bot

response = rag_bot("Summarize quantum entanglement")
print(response)
```

---

## ⚙️ Optional Settings

### 🔁 Change Model or Host (via config or env)

ChatCraft supports config priority:

1. Environment variables
2. `~/.chatcraft/config.json`
3. Defaults

### 🧪 Example: Environment Variables

```bash
export EMBEDDING_MODEL=nomic-embed-text
export OLLAMA_URL=http://localhost:11434
```

### ⚙️ Or: Config File (`~/.chatcraft/config.json`)
```json
{
  "embedding_model": "nomic-embed-text",
  "ollama_host": "http://localhost:11434"
}
```

---

## 🛠️ Developer Tips

- Adjust chunk size (`--chunk-size` flag or modify `chunk_text()` in `rag_utils.py`)
- Change number of context chunks (e.g., `top_k=5` in `rag_bot()`)
- Use `get_top_k()` + `get_response()` directly for advanced workflows

---

## 🏁 Coming Soon (Ideas)
- ✅ Multi-file indexing
- ✅ Source tags
- ✅ Web interface for visual exploration
- 🧠 Syntax-aware RAG for code
- 🗃️ CSV/table flattening for structured data

---

Made for students. Built for educators. Powered by open LLMs.  
Happy RAG-ing! 🚀
