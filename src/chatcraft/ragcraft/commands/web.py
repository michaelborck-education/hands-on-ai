import tempfile
import shutil
from pathlib import Path
from fasthtml import html, run as run_web, route, Form, File, Redirect, ctx
from chatcraft.get_response import get_response
from chatcraft.ragcraft.rag_utils import (
    chunk_text, get_embeddings, save_index_with_sources,
    get_top_k, load_text_file
)

app = None  # Placeholder if needed for CLI inclusion

def web():
    """Launch RagCraft visual web interface."""
    INDEX_PATH = Path.home() / ".chatcraft" / ".rag_index" / "web_index.npz"

    @route("/")
    def home():
        return html(
            h1("🧠 RagCraft Web Interface"),
            h2("Upload File"),
            Form("/upload", enctype="multipart/form-data")[
                File("file"), html.button("Upload")
            ],
            h2("Ask a Question"),
            Form("/ask")[
                html.input(name="question", value=ctx.query.get("question", ""), required=True),
                html.button("Ask")
            ],
            _render_result()
        )

    @route("/upload", method="POST")
    def upload(file):
        if file.filename.endswith((".md", ".txt", ".pdf", ".docx")):
            tmp = Path(tempfile.mktemp(suffix=Path(file.filename).suffix))
            with tmp.open("wb") as f:
                shutil.copyfileobj(file.file, f)
            text = load_text_file(tmp)
            chunks = chunk_text(text)
            vectors = get_embeddings(chunks)
            sources = [file.filename] * len(chunks)
            save_index_with_sources(vectors, chunks, sources, INDEX_PATH)
            tmp.unlink()
            return Redirect("/")
        return html.p("❌ Unsupported file")

    @route("/ask", method="POST")
    def ask_web(question):
        ctx.query["question"] = question
        return Redirect("/")

    def _render_result():
        question = ctx.query.get("question")
        if not question:
            return ""
        if not INDEX_PATH.exists():
            return html.p("❌ No index found. Upload a file first.")
        chunks_sources, scores = get_top_k(question, INDEX_PATH, return_scores=True)
        chunks = [c for c, _ in chunks_sources]
        context = "\n\n".join(chunks)
        system = "Use the provided context to answer the question. If unsure, say you don't know."
        response = get_response(question, system=system, context=context)
        return html(
            h2("💬 Response"), html.p(response),
            h3("📚 Context"),
            html.ul([
                html.li(
                    html.strong(f"[{source}]"), html.br(),
                    chunk, html.br(),
                    html.em(f"Similarity: {scores[i]:.4f}")
                ) for i, (chunk, source) in enumerate(chunks_sources)
            ])
        )

    run_web()
