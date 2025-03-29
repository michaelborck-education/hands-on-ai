from pathlib import Path
import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests


# --- CONFIG LOADING ---
def load_config():
    config_file = Path.home() / ".chatcraft" / "config.json"
    file_config = {}
    if config_file.exists():
        try:
            with config_file.open("r") as f:
                file_config = json.load(f)
        except Exception:
            print("⚠️ Warning: Couldn't read config file")

    model = os.getenv("EMBEDDING_MODEL", file_config.get("embedding_model", file_config.get("model", "nomic-embed-text")))
    ollama_url = os.getenv("OLLAMA_URL", file_config.get("ollama_host", "http://localhost:11434"))

    return model, ollama_url


EMBEDDING_MODEL, OLLAMA_URL = load_config()


# --- TEXT LOADING ---
def load_text_file(path: Path) -> str:
    ext = path.suffix.lower()

    if ext in [".txt", ".md"]:
        return path.read_text(encoding="utf-8")

    elif ext == ".docx":
        try:
            import docx
        except ImportError:
            raise ImportError("Please install `python-docx` to use .docx files. Try: pip install .[rag]")
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    elif ext == ".pdf":
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError("Please install `pymupdf` to use .pdf files. Try: pip install .[rag]")
        with fitz.open(path) as doc:
            return "\n".join(page.get_text() for page in doc)

    else:
        raise ValueError(f"❌ Unsupported file type: {ext}. Supported: .txt, .md, .docx, .pdf")


# --- CHUNKING ---
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


# --- EMBEDDING ---
def get_embeddings(chunks):
    url = f"{OLLAMA_URL}/api/embeddings"
    headers = {"Content-Type": "application/json"}
    vectors = []

    for chunk in chunks:
        response = requests.post(url, headers=headers, json={"model": EMBEDDING_MODEL, "prompt": chunk})
        response.raise_for_status()
        vectors.append(response.json()["embedding"])

    return np.array(vectors)


# --- SAVE/LOAD INDEX (with sources) ---
def save_index_with_sources(vectors, chunks, sources, path):
    np.savez(path, vectors=vectors, chunks=np.array(chunks), sources=np.array(sources))


def load_index_with_sources(path):
    data = np.load(path, allow_pickle=True)
    return data["vectors"], data["chunks"], data["sources"]


# --- RAG RETRIEVAL ---
def get_top_k(query, index_path, k=3, return_scores=False):
    vectors, chunks, sources = load_index_with_sources(index_path)
    query_vector = get_embeddings([query])[0].reshape(1, -1)
    sims = cosine_similarity(query_vector, vectors)[0]
    top_indices = sims.argsort()[-k:][::-1]

    top_chunks = [chunks[i] for i in top_indices]
    top_sources = [sources[i] for i in top_indices]
    top_scores = [sims[i] for i in top_indices]

    if return_scores:
        return list(zip(top_chunks, top_sources)), top_scores
    return list(zip(top_chunks, top_sources))
