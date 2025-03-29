import typer
from chatcraft.get_response import get_response
from chatcraft.rag.rag_utils import get_top_k, load_config
from pathlib import Path
import textwrap

app = typer.Typer(help="Ask questions using a local RAG index.")

DEFAULT_INDEX_PATH = Path.home() / ".chatcraft" / ".rag_index" / "default.npz"

def display_context(chunk_source_pairs, scores=None):
    print("📚 Top Context Chunks:")
    for i, (chunk, source) in enumerate(chunk_source_pairs):
        score_info = f" (score: {scores[i]:.4f})" if scores else ""
        print(f"\n{i + 1}. [{source}]{score_info}")
        print(textwrap.fill(chunk.strip(), width=80))

@app.command()
def ask(
    query: str = typer.Argument(..., help="Question to ask"),
    index_path: Path = typer.Option(DEFAULT_INDEX_PATH, help="Path to .npz index file"),
    show_context: bool = typer.Option(False, "--show-context", help="Display retrieved context"),
    show_scores: bool = typer.Option(False, "--show-scores", help="Display similarity scores")
):
    model, _ = load_config()
    chunk_source_pairs, scores = get_top_k(query, index_path, return_scores=True)

    if show_context:
        display_context(chunk_source_pairs, scores if show_scores else None)

    chunks_only = [chunk for chunk, _ in chunk_source_pairs]
    context = "\n\n".join(chunks_only)
    system = "You are an assistant answering using the provided context. If unsure, say you don't know."

    print("\n💬 Response:")
    print(get_response(query, system=system, context=context))

@app.command()
def interactive(
    index_path: Path = typer.Option(DEFAULT_INDEX_PATH, help="Path to .npz index file"),
    show_context: bool = typer.Option(False, "--show-context", help="Display retrieved context"),
    show_scores: bool = typer.Option(False, "--show-scores", help="Display similarity scores")
):
    if not index_path.exists():
        typer.secho(f"❌ Index file not found: {index_path}", fg=typer.colors.RED)
        build = input("📚 Would you like to build a new index from a file or folder? (y/n): ").strip().lower()
        if build not in {"y", "yes"}:
            typer.echo("❌ No index loaded. Exiting.")
            raise typer.Exit(1)

        input_path = input("📝 Enter path to your .md, .pdf, .docx or folder: ").strip()
        input_file = Path(input_path)
        if not input_file.exists():
            typer.secho(f"❌ File or folder not found: {input_file}", fg=typer.colors.RED)
            raise typer.Exit(1)

        from chatcraft.rag.build_index import collect_chunks_from_path
        from chatcraft.rag.rag_utils import get_embeddings, save_index_with_sources

        typer.echo(f"📖 Reading and chunking: {input_path}")
        chunks, sources = collect_chunks_from_path(input_file, chunk_size=500)
        vectors = get_embeddings(chunks)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        save_index_with_sources(vectors, chunks, sources, index_path)
        typer.secho("✅ Index built successfully!\n", fg=typer.colors.GREEN)

    print(f"🧠 Entering Interactive RAG Chat (Index: {index_path})")
    print("Type your question, or 'exit' to quit.\n")

    while True:
        try:
            query = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break

        if query.lower() in {"exit", "quit"}:
            break

        ask(query=query, index_path=index_path, show_context=show_context, show_scores=show_scores)
        print("-" * 80)

if __name__ == "__main__":
    app()
