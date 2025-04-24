# HandsOnAI RAG Sample Documents

This directory contains sample documents for testing and learning the RAG (Retrieval-Augmented Generation) capabilities of HandsOnAI.

## Available Files

- **tcp_protocol.md**: A Markdown file containing information about TCP and networking concepts
- **networking_basics.txt**: A plaintext document with basic networking reference information
- **tcp_handshake.docx**: A Microsoft Word document explaining the TCP three-way handshake
- **mobile_game_protocols.pdf**: A PDF document about multiplayer mobile games protocols

## Using the Sample Files

These sample files are included in the HandsOnAI package and can be accessed programmatically:

```python
from hands_on_ai.rag import list_sample_docs, get_sample_docs_path, copy_sample_docs

# List all available sample files
print(list_sample_docs())

# Get the path to the sample directory
samples_path = get_sample_docs_path()
print(f"Sample documents are located at: {samples_path}")

# Copy sample files to a local directory for experimentation
local_path = copy_sample_docs("my_samples")
print(f"Copied sample documents to: {local_path}")
```

## Example RAG Usage

Here's a complete example of using the sample files with RAG:

```python
import os
from pathlib import Path
from hands_on_ai.rag import (
    load_text_file, 
    chunk_text, 
    get_embeddings, 
    save_index_with_sources,
    get_top_k,
    copy_sample_docs
)

# Copy sample files to a working directory
samples_dir = copy_sample_docs("rag_demo")

# Process a sample file
sample_file = samples_dir / "tcp_protocol.md"
text = load_text_file(sample_file)

# Chunk the text
chunks = chunk_text(text, chunk_size=50)

# Track the source of each chunk
sources = [f"{sample_file.name}:{i}" for i in range(len(chunks))]

# Get embeddings
vectors = get_embeddings(chunks)

# Save the index
index_path = Path("sample_index.npz")
save_index_with_sources(vectors, chunks, sources, index_path)

# Query the index
query = "What is RAG?"
results = get_top_k(query, index_path, k=2)

print("Query:", query)
print("\nResults:")
for chunk, source in results:
    print(f"\nSource: {source}")
    print(f"Content: {chunk[:100]}...")
```

## Creating Your Own Documents

Once you're familiar with how RAG works using these samples, you can create your own document collections for more sophisticated applications.