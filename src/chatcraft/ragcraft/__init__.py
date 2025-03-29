from pathlib import Path
from typing import Union
from chatcraft.get_response import get_response
from chatcraft.rag.rag_utils import get_top_k

DEFAULT_INDEX_PATH = Path.home() / ".chatcraft" / ".rag_index" / "default.npz"

def rag_bot(prompt: str, index_path: Union[str, Path] = DEFAULT_INDEX_PATH, top_k: int = 3) -> str:
    """
    A context-aware chatbot using local file-based RAG.
    Returns a plain string, aligned with other _bot() functions.
    """
    index_path = Path(index_path)

    if not index_path.exists():
        raise FileNotFoundError(
            f"❌ RAG index not found: {index_path}\n"
            "💡 Tip: Run `build_index.py` or use `rag interactive` to create one."
        )

    chunk_source_pairs = get_top_k(prompt, index_path, k=top_k)
    chunks_only = [chunk for chunk, _ in chunk_source_pairs]
    context = "\n\n".join(chunks_only)

    system = "Use the provided context to answer the question. If unsure, say you don't know."
    return get_response(prompt, system=system, context=context)
