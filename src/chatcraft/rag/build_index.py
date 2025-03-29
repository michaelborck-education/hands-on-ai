import typer
from pathlib import Path
from chatcraft.rag.rag_utils import chunk_text, get_embeddings, save_index_with_sources, load_text_file
import os

app = typer.Typer(help="Build a RAG index from a file or folder of documents.")

DEFAULT_INDEX_PATH = Path.home() / ".chatcraft" / ".rag_index" / "default.npz"

def collect_chunks_from_path(path: Path, chunk_size: int):
    chunks, sources = [], []
    if path.is_file():
        try:
            text = load_text_file(path)
            file_chunks = chunk_text(text, chunk_size=chunk_size)
            chunks.extend(file_chunks)
            sources.extend([str(path.name)] * len(file_chunks))
        except Exception as e:
            typer.secho(f"⚠️ Skipping {path}: {e}", fg=typer.colors.YELLOW)

    elif path.is_dir():
        for file in sorted(path.rglob("*")):
            if file.is_file():
                try:
                    text = load_text_file(file)
                    file_chunks = chunk_text(text, chunk_size=chunk_size)
                    chunks.extend(file_chunks)
                    sources.extend([str(file.relative_to(path))] * len(file_chunks))
                    typer.echo(f"📄 Indexed {file}")
                except Exception as e:
                    typer.secho(f"⚠️ Skipping {file}: {e}", fg=typer.colors.YELLOW)

    return chunks, sources

@app.command()
def build(
    input_path: Path = typer.Argument(..., help="Path to a file or folder to index (.md, .txt, .pdf, .docx)"),
    output_file: Path = typer.Argument(None, help="Optional: path to save the .npz index"),
    chunk_size: int = typer.Option(500, help="Number of words per chunk"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing index file without warning")
):
    if not input_path.exists():
        typer.secho(f"❌ Path not found: {input_path}", fg=typer.colors.RED)
        raise typer.Exit(1)

    index_path = output_file or DEFAULT_INDEX_PATH
    index_path.parent.mkdir(parents=True, exist_ok=True)

    if index_path.exists() and not force:
        typer.secho(f"⚠️ Index file already exists: {index_path}", fg=typer.colors.YELLOW)
        typer.echo("Use --force to overwrite it.")
        raise typer.Exit(1)

    typer.echo(f"📖 Reading from: {input_path}")
    chunks, sources = collect_chunks_from_path(input_path, chunk_size)

    if not chunks:
        typer.secho("❌ No valid files found to index.", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.echo(f"🧠 Generating embeddings for {len(chunks)} chunks...")
    vectors = get_embeddings(chunks)

    typer.echo(f"💾 Saving index to: {index_path}")
    save_index_with_sources(vectors, chunks, sources, index_path)

    typer.secho("✅ Index built successfully!", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
