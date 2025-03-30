"""
Web command for the rag CLI - provides a web interface.
"""

import typer
import os
import tempfile
from pathlib import Path
from ...config import CONFIG_DIR
from ..utils import load_text_file, chunk_text, get_embeddings, save_index_with_sources, get_top_k
from ...chat import get_response

app = typer.Typer(help="Launch web interface for RAG")


def create_web_app(index_path=None):
    """
    Create a FastAPI web app for RAG.
    
    Args:
        index_path: Path to index file
        
    Returns:
        FastAPI app
    """
    from fastapi import FastAPI, File, UploadFile, Form, HTTPException
    from fastapi.responses import HTMLResponse
    from fastapi.middleware.cors import CORSMiddleware
    
    # If no index path is provided, use default
    if index_path is None:
        index_path = str(CONFIG_DIR / "index.npz")
    
    app = FastAPI(title="RAG Web Interface")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Simple HTML frontend
    @app.get("/", response_class=HTMLResponse)
    async def get_home():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>RAG Web Interface</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                textarea, input[type="text"] { width: 100%; padding: 8px; margin: 8px 0; }
                button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
                #result { margin-top: 20px; white-space: pre-wrap; }
                .context { background-color: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
                .source { font-size: 0.8em; color: #666; }
                .answer { background-color: #e6f7e6; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>RAG Web Interface</h1>
            
            <div id="uploadForm">
                <h2>Upload Documents</h2>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" multiple>
                    <button type="submit">Upload & Index</button>
                </form>
            </div>
            
            <hr>
            
            <div id="queryForm">
                <h2>Ask a Question</h2>
                <input type="text" id="question" placeholder="Enter your question here">
                <button onclick="askQuestion()">Ask</button>
            </div>
            
            <div id="result"></div>
            
            <script>
            async function askQuestion() {
                const question = document.getElementById('question').value;
                if (!question) return;
                
                document.getElementById('result').innerHTML = "Searching...";
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: new URLSearchParams({ 'question': question })
                    });
                    
                    if (!response.ok) throw new Error('Network response was not ok');
                    
                    const data = await response.json();
                    let resultHtml = '<h3>Results</h3>';
                    
                    // Show context
                    resultHtml += '<h4>Context Used:</h4>';
                    data.context.forEach((item, i) => {
                        resultHtml += `<div class="context">
                            <div class="source">Source: ${item.source} (Score: ${item.score.toFixed(4)})</div>
                            <div>${item.text.substring(0, 300)}${item.text.length > 300 ? '...' : ''}</div>
                        </div>`;
                    });
                    
                    // Show answer
                    resultHtml += '<h4>Answer:</h4>';
                    resultHtml += `<div class="answer">${data.answer}</div>`;
                    
                    document.getElementById('result').innerHTML = resultHtml;
                } catch (error) {
                    document.getElementById('result').innerHTML = `Error: ${error.message}`;
                }
            }
            </script>
        </body>
        </html>
        """
    
    # Upload and index documents
    @app.post("/upload")
    async def upload_file(file: UploadFile = File(...)):
        try:
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
            
            return {"message": f"File {file.filename} indexed successfully", "chunks": len(chunks)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # Ask a question
    @app.post("/ask")
    async def ask_question(question: str = Form(...)):
        try:
            # Get context
            context_items, scores = get_top_k(question, index_path, k=3, return_scores=True)
            
            # Format context for response
            context = []
            for i, (text, source) in enumerate(context_items):
                context.append({
                    "text": text,
                    "source": source,
                    "score": scores[i]
                })
            
            # Build prompt with context
            prompt = f"Question: {question}\n\nContext:\n"
            for item in context:
                prompt += f"- {item['text']}\n"
            prompt += "\nAnswer the question based on the provided context. If the context doesn't contain the answer, say so."
            
            # Get answer
            answer = get_response(
                prompt,
                system="You are a helpful assistant that answers questions based only on the provided context."
            )
            
            return {
                "question": question,
                "context": context,
                "answer": answer
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return app


@app.callback(invoke_without_command=True)
def web(
    port: int = typer.Option(8000, help="Port to run the web server on"),
    index_path: str = typer.Option(None, help="Path to index file (default: ~/.ailabkit/index.npz)"),
):
    """Launch web interface for RAG."""
    try:
        import uvicorn
        from fastapi import FastAPI
    except ImportError:
        print("[red]❌ FastAPI and uvicorn are required for the web interface.[/red]")
        print("Please install them with: pip install fastapi uvicorn")
        raise typer.Exit(1)
    
    # Determine the index path
    if index_path is None:
        index_path = str(CONFIG_DIR / "index.npz")
    
    index_dir = Path(index_path).parent
    index_dir.mkdir(exist_ok=True)
    
    print(f"🌐 Starting RAG web interface on http://localhost:{port}")
    print(f"Using index: {index_path}")
    print("Press Ctrl+C to stop the server")
    
    # Create and run the web app
    app = create_web_app(index_path)
    uvicorn.run(app, host="0.0.0.0", port=port)