import typer
from chatcraft.ragcraft.commands import ask, index, interactive, web

app = typer.Typer(help="RagCraft: Ask questions about your own notes using RAG.")

# Subcommands (modular CLI)
app.add_typer(index.app, name="index", help="Build a RAG index from files")
app.add_typer(ask.app, name="ask", help="Ask questions using your indexed notes")
app.add_typer(interactive.app, name="interactive", help="Run interactive RAG chat")
app.command("web")(web.web)  # Web is a function, not a Typer app

if __name__ == "__main__":
    app()
