#!/usr/bin/env python3
"""
Simple RAG Example - Demonstrates basic usage of hands-on-ai RAG functionality.

This example shows how to:
1. Set up sample documents
2. Create a RAG index
3. Ask questions using the indexed documents
4. Use the CLI commands programmatically

Requirements:
- hands-on-ai package installed
- An LLM server running (Ollama, OpenAI API, etc.)
"""

from pathlib import Path
from hands_on_ai.rag import (
    copy_sample_docs,
    load_text_file,
    chunk_text,
    get_embeddings,
    save_index_with_sources,
    get_top_k
)
from hands_on_ai.chat import get_response
from hands_on_ai.config import get_model


def main():
    """Run the simple RAG example."""
    print("🚀 Simple RAG Example")
    print("=" * 50)
    
    # Step 1: Copy sample documents
    print("\n📁 Step 1: Setting up sample documents...")
    samples_dir = copy_sample_docs("rag_example")
    print(f"✅ Sample documents copied to: {samples_dir}")
    
    # List available files
    sample_files = list(samples_dir.glob("*"))
    print(f"📄 Found {len(sample_files)} sample files:")
    for file in sample_files:
        if file.is_file():
            print(f"  - {file.name}")
    
    # Step 2: Load and process documents
    print("\n🔧 Step 2: Processing documents...")
    all_chunks = []
    all_sources = []
    
    for file_path in sample_files:
        if file_path.is_file() and file_path.suffix in ['.txt', '.md']:
            print(f"  Processing: {file_path.name}")
            try:
                text = load_text_file(file_path)
                chunks = chunk_text(text, chunk_size=100)
                
                # Add source information for each chunk
                sources = [f"{file_path.name}:chunk_{i}" for i in range(len(chunks))]
                
                all_chunks.extend(chunks)
                all_sources.extend(sources)
                print(f"    ✅ Generated {len(chunks)} chunks")
                
            except Exception as e:
                print(f"    ❌ Error processing {file_path.name}: {e}")
    
    print(f"📊 Total chunks processed: {len(all_chunks)}")
    
    # Step 3: Create embeddings and save index
    print("\n🧠 Step 3: Creating embeddings...")
    try:
        vectors = get_embeddings(all_chunks)
        index_path = Path("simple_rag_index.npz")
        save_index_with_sources(vectors, all_chunks, all_sources, index_path)
        print(f"✅ Index saved to: {index_path}")
    except Exception as e:
        print(f"❌ Error creating embeddings: {e}")
        print("Make sure you have an LLM server running (e.g., Ollama)")
        return
    
    # Step 4: Ask questions
    print("\n❓ Step 4: Asking questions...")
    
    questions = [
        "What is TCP?",
        "How does networking work?",
        "What are the main networking protocols?"
    ]
    
    for question in questions:
        print(f"\n🔍 Question: {question}")
        
        try:
            # Retrieve relevant chunks
            results = get_top_k(question, index_path, k=3, return_scores=True)
            context_chunks, scores = results
            
            # Show retrieved context
            print("📄 Retrieved context:")
            for i, ((chunk, source), score) in enumerate(zip(context_chunks, scores)):
                print(f"  {i+1}. {source} (score: {score:.3f})")
                print(f"     {chunk[:100]}...")
            
            # Build prompt with context
            context_text = "\n".join([chunk for chunk, _ in context_chunks])
            prompt = f"""Question: {question}

Context:
{context_text}

Answer the question based on the provided context. If the context doesn't contain enough information, say so."""
            
            # Get AI response
            model = get_model()
            response = get_response(
                prompt,
                system="You are a helpful assistant that answers questions based on the provided context.",
                model=model
            )
            
            print(f"🤖 Answer: {response}")
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
    
    print("\n🎉 Example completed!")
    print(f"\nTo try the CLI commands:")
    print(f"  hands-on-ai rag index {samples_dir}")
    print(f"  hands-on-ai rag ask 'What is TCP?'")
    print(f"  hands-on-ai rag interactive")
    print(f"  hands-on-ai rag web")


if __name__ == "__main__":
    main()