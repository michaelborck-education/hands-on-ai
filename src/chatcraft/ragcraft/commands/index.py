import typer
from chatcraft.ragcraft.rag_utils import chunk_text, get_embeddings, save_index_with_sources, load_text_file
from pathlib import Path

app = typer.Typer()
DEFAULT_INDEX_PATH = Path.home() / ".chatcraft" / ".rag_index" / "default.npz"

@app.command()
def index(
    input_path: Path = typer.Argument(..., help="File or folder to index (.md, .txt, .docx, .pdf)"),
    output_file: Path = typer.Option(None, help="Optional: output index path"),
    chunk_size: int = typer.Option(500, help="Words per chunk"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing index file")
):
    """Index a file or folder of notes using RagCraft."""
    if not input_path.exists():
        typer.secho(f"❌ Path not found: {input_path}", fg=typer.colors.RED)
        raise typer.Exit(1)

    index_path = output_file or DEFAULT_INDEX_PATH
    index_path.parent.mkdir(parents=True, exist_ok=True)

    if index_path.exists() and not force:
        typer.secho(f"⚠️ Index exists: {index_path}", fg=typer.colors.YELLOW)
        typer.echo("Use --force to overwrite.")
        raise typer.Exit(1)

    def collect_chunks(path: Path):
        chunks, sources = [], []
        if path.is_file():
            try:
                text = load_text_file(path)
                chunks_ = chunk_text(text, chunk_size)
                chunks.extend(chunks_)
                sources.extend([str(path.name)] * len(chunks_))
            except Exception as e:
                typer.secho(f"⚠️ Skipped {path}: {e}", fg=typer.colors.YELLOW)
        else:
            for file in sorted(path.rglob("*")):
                if file.is_file():
                    try:
                        text = load_text_file(file)
                        chunks_ = chunk_text(text, chunk_size)
                        chunks.extend(chunks_)
                        sources.extend([str(file.relative_to(path))] * len(chunks_))
                        typer.echo(f"📄 Indexed {file}")
                    except Exception as e:
                        typer.secho(f"⚠️ Skipped {file}: {e}", fg=typer.colors.YELLOW)
        return chunks, sources

    chunks, sources = collect_chunks(input_path)

    if not chunks:
        typer.secho("❌ No valid content found to index.", fg=typer.colors.RED)
        raise typer.Exit(1)

    vectors = get_embeddings(chunks)
    save_index_with_sources(vectors, chunks, sources, index_path)
    typer.secho(f"✅ RagCraft index saved to {index_path}", fg=typer.colors.GREEN)
