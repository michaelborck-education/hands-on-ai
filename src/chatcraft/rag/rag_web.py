from fasthtml import html, run, route, Form, File, Redirect, ctx
from chatcraft.rag.rag_utils import (
    chunk_text, get_embeddings, save_index_with_sources,
    get_top_k, load_text_file
)
from chatcraft.get_response import get_response
from pathlib import Path
import tempfile
import shutil

INDEX_PATH = Path.home() / ".chatcraft" / ".rag_index" / "web_index.npz"

@route("/")
def home():
    return html(
        h1("🧠 ChatCraft RAG Visual Explorer"),
        h2("Upload Notes (.md, .pdf, .docx, .txt)"),
        Form("/upload", enctype="multipart/form-data")[
            File("file"),
            " ",
            html.button("Upload and Index", type="submit")
        ],
        h2("Ask a Question"),
        Form("/ask")[
            html.input(name="question", value=ctx.query.get("question", ""), required=True),
            " ",
            html.button("Ask", type="submit")
        ],
        _render_result()
    )

@route("/upload", method="POST")
def upload(file):
    if file.filename.endswith((".md", ".txt", ".pdf", ".docx")):
        tmp_path = Path(tempfile.mktemp(suffix=Path(file.filename).suffix))
        with tmp_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)
        text = load_text_file(tmp_path)
        chunks = chunk_text(text)
        vectors = get_embeddings(chunks)
        sources = [file.filename] * len(chunks)
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        save_index_with_sources(vectors, chunks, sources, INDEX_PATH)
        tmp_path.unlink()
        return Redirect("/")
    return html("❌ Unsupported file type")

@route("/ask", method="POST")
def ask(question):
    ctx.query["question"] = question
    return Redirect("/")

def _render_result():
    question = ctx.query.get("question")
    if not question:
        return ""

    if not INDEX_PATH.exists():
        return html.p("❌ No index found. Please upload a file first.")

    chunk_sources, scores = get_top_k(question, INDEX_PATH, return_scores=True)
    chunks_only = [chunk for chunk, _ in chunk_sources]
    context = "\n\n".join(chunks_only)
    system = "Use the provided context to answer the question. If unsure, say you don't know."
    response = get_response(question, system=system, context=context)

    return html(
        h2("💬 Response"),
        html.p(response),
        h3("📚 Context Used"),
        html.ul([
            html.li(
                html.strong(f"[{source}]"),
                html.br(),
                chunk,
                html.br(),
                html.em(f"Similarity: {scores[i]:.4f}")
            ) for i, (chunk, source) in enumerate(chunk_sources)
        ])
    )

if __name__ == "__main__":
    run()
