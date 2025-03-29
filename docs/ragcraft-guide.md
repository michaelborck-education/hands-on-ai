# 🧠 RagCraft Guide: Ask Questions About Your Notes

[![](https://img.shields.io/badge/CLI-RagCraft-blue)](#💬-cli-usage)

RagCraft is a lightweight tool to turn your documents into an AI-powered knowledge base using Retrieval-Augmented Generation (RAG). It’s part of the ChatCraft ecosystem.

---

![RagCraft Web Interface](assets/ragcraft-web-preview.png)

---

## 🚀 How to Use

### ✅ Install ChatCraft with RAG support

```bash
pip install chatcraft[rag]
```

Or with `uv`:

```bash
uv pip install chatcraft[rag]
```

---

## 💬 CLI Usage

```bash
ragcraft index notes/            # Build index from folder or file
ragcraft ask "What is TCP?"     # Ask a question
ragcraft interactive             # Start interactive Q&A mode
ragcraft web                     # Launch the FastHTML visual explorer
```

---

## 📁 Where Indexes Are Stored

- CLI default: `~/.chatcraft/.rag_index/default.npz`
- Web UI default: `~/.chatcraft/.rag_index/web_index.npz`

You can override using `--output-file` or `--index-path`.

---

## 🧪 Try It Without Indexing

Use this prebuilt example:

```bash
ragcraft ask "What is TCP?" --index-path chatcraft/testdata/sample_index.npz
```

---

## 📂 Test Data (for Students or Demos)

Use the built-in files in `chatcraft/testdata/demo_notes/`:

```bash
ragcraft index chatcraft/testdata/demo_notes/
```

Includes:

- `sample.md` – Markdown format
- `reference.txt` – Plain text
- `demo.docx` – [Download](../demo.docx)
- `demo.pdf` – [Download](../demo.pdf)

---

## 🛠️ Justfile (Optional Shortcuts)

```make
just rag-index file=notes.md:
    ragcraft index $file

just rag-web:
    ragcraft web
```

---

## 🧠 Example Workflow

```bash
ragcraft index lectures/
ragcraft ask "What are the core steps in DNS resolution?" --show-context
ragcraft web
```

---

Designed for educators. Built for learners. Powered by open models.
