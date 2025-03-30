"""
Web command for the rag CLI - provides a web interface using FastHTML.
"""

import typer
import os
import json
import tempfile
from pathlib import Path
from ...config import CONFIG_DIR, log
from ..utils import load_text_file, chunk_text, get_embeddings, save_index_with_sources, get_top_k
from ...chat import get_response

app = typer.Typer(help="Launch web interface for RAG")


@app.callback(invoke_without_command=True)
def web(
    port: int = typer.Option(8000, help="Port to run the web server on"),
    index_path: str = typer.Option(None, help="Path to index file (default: ~/.ailabkit/index.npz)"),
):
    """Launch web interface for RAG using FastHTML."""
    try:
        from fasthtml.common import *
    except ImportError:
        print("❌ FastHTML is required for the web interface.")
        print("Please install it with: pip install python-fasthtml")
        raise typer.Exit(1)

    # Determine the index path
    if index_path is None:
        index_path = str(CONFIG_DIR / "index.npz")
    
    index_dir = Path(index_path).parent
    index_dir.mkdir(exist_ok=True)
    
    # Create FastHTML app
    app, rt = fast_app()
    
    # File upload handling - this uses a temporary file to store the uploaded file
    @rt("/upload")
    async def post(file, request):
        try:
            # Check if the index file can be loaded (or initialize it if it doesn't exist)
            if os.path.exists(index_path):
                try:
                    # Test if the file is valid
                    get_top_k("test", index_path, k=1)
                except Exception:
                    # If invalid, create a new one later
                    pass
            
            # Create a temporary file
            suffix = Path(file.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
                content = await file.read()
                temp.write(content)
                temp_path = temp.name
            
            # Process the file
            text = load_text_file(Path(temp_path))
            chunks = chunk_text(text)
            sources = [file.filename] * len(chunks)
            vectors = get_embeddings(chunks)
            
            # Save or update the index
            save_index_with_sources(vectors, chunks, sources, index_path)
            
            # Clean up
            os.unlink(temp_path)
            
            # Return info about the indexing process
            return Div(
                P(f"File {file.filename} indexed successfully."),
                P(f"Created {len(chunks)} text chunks."),
                P("Your document is now ready for questions!")
            )
        except Exception as e:
            log.exception(f"Error during file upload: {e}")
            return Div(f"Error: {str(e)}", style="color: red;")
    
    # Question answering
    @rt("/ask")
    async def post(question: str):
        try:
            # Get context
            context_items, scores = get_top_k(question, index_path, k=3, return_scores=True)
            
            # Format context for response
            context_sections = []
            for i, (text, source) in enumerate(context_items):
                context_sections.append(Div(
                    Div(f"Source: {source} (Score: {scores[i]:.4f})", cls="source"),
                    Div(text[:300] + ('...' if len(text) > 300 else '')),
                    cls="context"
                ))
            
            # Build prompt with context
            prompt = f"Question: {question}\n\nContext:\n"
            for i, (text, source) in enumerate(context_items):
                prompt += f"- {text}\n"
            prompt += "\nAnswer the question based on the provided context. If the context doesn't contain the answer, say so."
            
            # Get answer
            answer = get_response(
                prompt,
                system="You are a helpful assistant that answers questions based only on the provided context."
            )
            
            # Return the results
            return Div(
                H3("Results"),
                H4("Context Used:"),
                *context_sections,
                H4("Answer:"),
                Div(answer, cls="answer")
            )
        except Exception as e:
            log.exception(f"Error during question answering: {e}")
            return Div(f"Error: {str(e)}", style="color: red;")
    
    # Main page
    @rt("/")
    def get():
        return Titled("RAG Web Interface",
            Article(
                H1("RAG Web Interface"),
                
                # Upload section
                Div(
                    H2("Upload Documents"),
                    Form(
                        Input(type="file", name="file"),
                        Button("Upload & Index", type="submit"),
                        enctype="multipart/form-data",
                        action="/upload",
                        method="post",
                        hx_post="/upload",
                        hx_target="#upload-result",
                        hx_swap="outerHTML"
                    ),
                    Div(id="upload-result"),
                    id="uploadForm"
                ),
                
                Hr(),
                
                # Query section
                Div(
                    H2("Ask a Question"),
                    Form(
                        Input(type="text", id="question", name="question", placeholder="Enter your question here"),
                        Button("Ask", type="submit"),
                        hx_post="/ask",
                        hx_target="#result",
                        hx_swap="innerHTML",
                        hx_trigger="submit"
                    ),
                    id="queryForm"
                ),
                
                # Result area
                Div(id="result"),
                
                # CSS styling
                Style("""
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    h1 { color: #333; }
                    textarea, input[type="text"] { width: 100%; padding: 8px; margin: 8px 0; }
                    button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
                    #result { margin-top: 20px; white-space: pre-wrap; }
                    .context { background-color: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
                    .source { font-size: 0.8em; color: #666; }
                    .answer { background-color: #e6f7e6; padding: 15px; border-radius: 5px; }
                """)
            )
        )
    
    # Run the server
    print(f"🌐 Starting RAG web interface on http://localhost:{port}")
    print(f"Using index: {index_path}")
    print("Press Ctrl+C to stop the server")
    
    # Serve the application
    serve(app=app, port=port)