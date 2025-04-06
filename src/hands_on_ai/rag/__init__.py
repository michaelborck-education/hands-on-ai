"""
RAG module - Retrieval-Augmented Generation for document Q&A.
"""

from .utils import (
    load_text_file,
    chunk_text,
    get_embeddings,
    save_index_with_sources,
    load_index_with_sources,
    get_top_k,
    get_sample_docs_path,
    list_sample_docs,
    copy_sample_docs
)

# Core RAG functions
__all__ = [
    "load_text_file",
    "chunk_text",
    "get_embeddings",
    "save_index_with_sources",
    "load_index_with_sources",
    "get_top_k",
    # Sample document utilities
    "get_sample_docs_path",
    "list_sample_docs",
    "copy_sample_docs"
]