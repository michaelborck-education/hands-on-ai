# Classroom Setup for ChatCraft

This guide walks educators and students through the technical setup needed to use [ChatCraft](https://github.com/teaching-repositories/chatcraft) in a classroom environment. It assumes basic familiarity with Python and the command line.

---

## 💻 System Requirements

- Operating System: Linux, macOS, or WSL on Windows
- Python: 3.8+
- [Ollama](https://ollama.com) installed and running (for local LLM inference)
- Internet access (for first-time setup or optional remote models)

---

## 🔧 Installation Steps

### 1. Clone the ChatCraft Repository
```bash
git clone https://github.com/teaching-repositories/chatcraft.git
cd chatcraft
```

### 2. Create a Virtual Environment
We recommend `uv` for fast installs, but `venv` or `virtualenv` also works.
```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Install ChatCraft (Editable Mode)
```bash
uv pip install -e '.[dev]'
```
This installs the core package, CLI entry point, and development tools.

---

## 🤖 Run Ollama
ChatCraft expects a local Ollama server by default.

### 1. Install Ollama
Follow instructions at: [https://ollama.com/download](https://ollama.com/download)

### 2. Start the Server
```bash
ollama run llama3
```
Or use a model of your choice (e.g., `codellama`, `mistral`, etc.)

---

## 🚀 Test the Setup

### CLI Check:
```bash
chatcraft doctor
```
Should report that Ollama is reachable.

### Interactive Mode:
```bash
chatcraft interactive
```
Chat with any of the built-in personalities.

---

## 🧪 Classroom Preparation

- ✅ Ensure all students have Python and Ollama installed
- ✅ Pre-install the models if bandwidth is limited
- ✅ Use `just doctor` or `chatcraft doctor` to verify working setup
- ✅ Optionally, preload `.venv` and models on lab machines
- ✅ Use offline bundle (`just bundle`) if internet is restricted

---

## 📦 Optional: Offline Setup
Use the offline zip bundle:
```bash
just bundle
```
Distribute `ChatCraft_Offline_Bundle.zip` to students for isolated environments.

---

## 🌐 Remote Ollama (Advanced)
You can point ChatCraft to a remote Ollama server by setting the environment variable:
```bash
export CHATCRAFT_SERVER_URL=http://your-ollama-server:11434
```
Useful for running a central server in class.

---

## 🧰 Related Tools
- `just doctor` - Check environment
- `just repl` or `chatcraft interactive` - Start REPL
- `just build-all` - Build docs and mini-projects
- `mkdocs serve` - Live preview of documentation site

---

## 📘 See Also
- [CLI Guide](cli-guide.md)
- [Ollama Setup](ollama-guide.md)
- [Education Guide](education-guide.md)

