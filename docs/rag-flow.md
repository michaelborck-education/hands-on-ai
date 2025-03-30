# RAG Flow with Index Creation

The diagram now shows two main processes:

1. **RAG Index Creation Process** (top flow):
   - Start with a document collection
   - Split documents into smaller chunks
   - Generate embeddings for each chunk using an embedding model
   - Store these vectors in a vector database
   - Create the RAG index from these vectors

2. **Query Processing Flow** (bottom flow):
   - User submits a query ("What is TCP?")
   - The query is embedded using the same embedding model
   - The system performs vector similarity search using the pre-created RAG index
   - Retrieves the top-K most similar chunks
   - Feeds these chunks along with the original query into the LLM's prompt
   - LLM generates the final response

The critical connection between these processes is shown by the dotted line from "RAG Index Creation" to "Vector Similarity Search," indicating that the index created in the first process is used during the retrieval step of the second process.  This diagram provides a more complete view of the RAG architecture, showing both how the knowledge base is prepared and how it's used at query time.

```text
## 1. RAG Index Creation Process
+----------------------+     +----------------------+     +----------------------+
|                      |     |                      |     |                      |
| Document Collection  +---->+  Document Chunking   +---->+   Chunk Embedding   |
|                      |     |                      |     |                      |
+----------------------+     +----------------------+     +-----------+----------+
                                                                     |
                                                                     |
+----------------------+     +----------------------+                |
|                      |     |                      |                |
|  RAG Index Creation  +<----+   Vector Storage     +<---------------+    
|                      |     |                      |     
+----------+-----------+     +----------------------+     
           |
           |
           |  Index is used for
           |
           v
## 2. Query Processing Flow
+----------------------+     +----------------------+     +----------------------+
|                      |     |                      |     |                      |
|     User Query       +---->+   Embed the Query    +---->+ Vector Similarity    |
|   "What is TCP?"     |     |                      |     |       Search         |
|                      |     |                      |     |                      |
+----------------------+     +----------------------+     +-----------+----------+
                                                                     |
                                                                     v
+----------------------+     +----------------------+     +----------------------+
|                      |     |                      |     |                      |
|  Generate Response   |<----+  Feed Chunks+Query   |<----+  Retrieve Top-K      |
| "TCP is a trans...  "|     |   into LLM Prompt    |     |      Chunks          |
|                      |     |                      |     |                      |
+----------------------+     +----------------------+     +----------------------+
```


