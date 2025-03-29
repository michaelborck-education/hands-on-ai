import typer
from chatcraft.ragcraft.commands.ask import ask
from pathlib import Path

app = typer.Typer()
DEFAULT_INDEX_PATH = Path.home() / ".chatcraft" / ".rag_index" / "default.npz"

@app.command()
def interactive(
    index_path: Path = typer.Option(DEFAULT_INDEX_PATH, help="Path to your RAG index"),
    show_context: bool = typer.Option(False, help="Show matched chunks"),
    show_scores: bool = typer.Option(False, help="Show similarity scores")
):
    """Interactive RAG chatbot session."""
    if not index_path.exists():
        typer.secho("❌ No index found. Run `ragcraft index` first.", fg=typer.colors.RED)
        raise typer.Exit(1)

    print("💬 Enter your questions below. Type 'exit' to quit.")
    while True:
        try:
            query = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break
        if query.lower() in {"exit", "quit"}:
            break
        ask(
            query=query,
            index_path=index_path,
            show_context=show_context,
            show_scores=show_scores
        )
