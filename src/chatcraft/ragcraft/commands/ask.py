import typer
from chatcraft.get_response import get_response
from chatcraft.ragcraft.rag_utils import get_top_k
from pathlib import Path

app = typer.Typer()
DEFAULT_INDEX_PATH = Path.home() / ".chatcraft" / ".rag_index" / "default.npz"

@app.command()
def ask(
    query: str = typer.Argument(..., help="Your question"),
    index_path: Path = typer.Option(DEFAULT_INDEX_PATH, help="Path to .npz index"),
    show_context: bool = typer.Option(False, help="Show matched chunks"),
    show_scores: bool = typer.Option(False, help="Show similarity scores")
):
    """Ask a question using your indexed notes."""
    chunk_sources, scores = get_top_k(query, index_path, return_scores=True)

    if show_context:
        for i, (chunk, source) in enumerate(chunk_sources):
            score = f" (score: {scores[i]:.4f})" if show_scores else ""
            print(f"\n{i+1}. [{source}]{score}")
            print(chunk.strip())

    context = "\n\n".join(chunk for chunk, _ in chunk_sources)
    system = "Use the provided context to answer the question. If unsure, say you don't know."
    print("\n💬 Response:")
    print(get_response(query, system=system, context=context))
