# Build Your Own Q&A CLI

**Difficulty**: Intermediate  
**Time**: 45 minutes  
**Learning Focus**: RAG, Embeddings, Vector Search, CLI Development  
**Module**: RAG

## Overview
Create a command-line interface (CLI) tool that implements Retrieval-Augmented Generation (RAG) to answer questions based on your own knowledge index. This project will teach you how to programmatically load vector embeddings, perform similarity searches, and generate contextually relevant responses.

## Instructions

1. **Setup Your Environment**
   - Ensure you have Python 3.7+ installed
   - Install the required libraries: `ailabkit` and `numpy`

2. **Understanding the Components**
   - Learn how RAG combines retrieval and generation
   - Understand embeddings and cosine similarity for semantic search
   - Explore the provided `rag_utils` functions: `embed_query()` and `get_top_k()`

3. **Build Your CLI Script**
   - Create a Python script with the following functions:
     - `load_index()`: Load document chunks and embeddings from an .npz file
     - `query_index()`: Embed a query and find the most similar chunks
     - `generate_answer()`: Create a response using retrieved context
     - `main()`: Handle CLI arguments and orchestrate the workflow

4. **Sample Implementation**
   ```python
   #!/usr/bin/env python3
   """
   Simple Q&A CLI using RAG (Retrieval-Augmented Generation)
   This script loads an index, embeds queries, retrieves relevant chunks, and generates answers.
   """

   import argparse
   import numpy as np
   from ailabkit.chat import get_response
   from ailabkit.rag.utils import embed_query, get_top_k

   def load_index(index_path):
       """Load chunked documents and their embeddings from an .npz file"""
       print(f"Loading index from {index_path}...")
       try:
           data = np.load(index_path, allow_pickle=True)
           chunks = data['chunks']
           embeddings = data['embeddings']
           metadata = data.get('metadata', None)
           print(f"Loaded {len(chunks)} chunks from index.")
           return chunks, embeddings, metadata
       except Exception as e:
           print(f"Error loading index: {e}")
           exit(1)

   def query_index(query, chunks, embeddings, metadata=None, top_k=3, show_scores=False):
       """Embed the query and retrieve the top K most relevant chunks"""
       print(f"Processing query: '{query}'")
       
       # Embed the query
       query_embedding = embed_query(query)
       
       # Get the top k chunks and their similarity scores
       top_chunks, top_scores, top_indices = get_top_k(
           query_embedding, embeddings, chunks, k=top_k, return_indices=True
       )
       
       # Prepare context from top chunks
       context = "\n\n---\n\n".join(top_chunks)
       
       # Show scores and sources if requested
       if show_scores:
           print("\n=== Top Chunks ===")
           for i, (chunk, score) in enumerate(zip(top_chunks, top_scores)):
               source_info = ""
               if metadata is not None and len(metadata) > top_indices[i]:
                   source_info = f" Source: {metadata[top_indices[i]].get('source', 'unknown')}"
               print(f"[{i+1}] Score: {score:.4f}{source_info}")
               print(f"Preview: {chunk[:100]}...\n")
       
       return context, top_chunks, top_scores

   def generate_answer(query, context):
       """Generate a response using the provided context"""
       prompt = f"""
   Based on the following context, please answer the question. If the context doesn't contain 
   relevant information to answer the question fully, say what you can based on the context 
   and indicate what information is missing.

   Context:
   {context}

   Question: {query}

   Answer:
   """
       return get_response(prompt, personality="helpful")

   def main():
       parser = argparse.ArgumentParser(description="Query a RAG index and get answers.")
       parser.add_argument("query", help="The question to ask")
       parser.add_argument("--index", "-i", default="sample_index.npz", help="Path to the .npz index file")
       parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of chunks to retrieve")
       parser.add_argument("--show-scores", "-s", action="store_true", help="Show similarity scores and chunk previews")
       parser.add_argument("--show-context", "-c", action="store_true", help="Show full context used for generation")
       args = parser.parse_args()
       
       # Load the index
       chunks, embeddings, metadata = load_index(args.index)
       
       # Query the index
       context, top_chunks, top_scores = query_index(
           args.query, chunks, embeddings, metadata, 
           top_k=args.top_k, show_scores=args.show_scores
       )
       
       # Show full context if requested
       if args.show_context:
           print("\n=== Full Context ===")
           print(context)
           print("\n")
       
       # Generate and print the answer
       print("\n=== Answer ===")
       answer = generate_answer(args.query, context)
       print(answer)
       
       # Log source information if metadata is available
       if metadata is not None and not args.show_scores:
           print("\n=== Sources ===")
           used_sources = set()
           for idx in range(min(args.top_k, len(top_chunks))):
               if idx < len(top_scores):
                   source = metadata[idx].get('source', 'unknown')
                   used_sources.add(source)
           
           for source in used_sources:
               print(f"- {source}")

   if __name__ == "__main__":
       main()
   ```

5. **Test Your Implementation**
   - Use the provided `sample_index.npz` file
   - Run your script with various queries
   - Experiment with different `top_k` values to see how it affects answers

## Extension Ideas

1. **Add More CLI Options**
   - Implement a `--temperature` flag to control response randomness
   - Add a `--model` option to select different LLMs for response generation
   - Create a `--format` flag to return responses as JSON or markdown

2. **Enhance Result Quality**
   - Implement re-ranking of retrieved chunks using cross-encoders
   - Add chunk summarization before combining context
   - Create a custom scoring mechanism that considers both relevance and recency

3. **Build a Web Interface**
   - Create a simple Flask or Streamlit app that uses your RAG engine
   - Add visualization of similarity scores or chunk relationships
   - Implement user feedback collection to improve retrieval quality

4. **Performance Optimizations**
   - Add caching for query embeddings and responses
   - Implement batched query processing for multiple questions
   - Explore approximate nearest neighbor algorithms for faster retrieval on large indices