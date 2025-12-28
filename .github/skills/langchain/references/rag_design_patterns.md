# RAG Design Patterns

This document summarizes design patterns for Retrieval-Augmented Generation (RAG) systems using LangChain.

## 1. Basic pipeline

A minimal RAG setup usually follows:

1. Load raw documents.
2. Split them into manageable chunks.
3. Embed the chunks.
4. Store embeddings in a vector store.
5. Expose a retriever.
6. Build a prompt that injects retrieved context and the user question.
7. Call a chat model to produce the final answer.

## 2. Chunking strategy

Important considerations:

- Chunk size and overlap:
  - Larger chunks capture more context but may exceed model limits.
  - Overlap preserves continuity across boundaries.
- Content-aware splitters:
  - RecursiveCharacterTextSplitter can respect paragraphs and headings.
- Metadata propagation:
  - Keep source metadata to enable filtered retrieval and traceability.

## 3. Retrieval strategy

Patterns:

- Simple similarity search: single query, top-k documents.
- Filtered retrieval: restrict by metadata such as document type or tags.
- Multi-query retrieval:
  - Generate several reformulations of a question.
  - Merge and deduplicate retrieved documents.
- Compression:
  - Apply a second-stage model to summarize or filter retrieved chunks.

## 4. Prompt design

Effective RAG prompts:

- Explicitly reference the context segment.
- Instruct the model to avoid fabricating answers when context is insufficient.
- Encourage quoting or referencing specific evidence when appropriate.

Example structure:

- Task instruction.
- Context section.
- Question.
- Answer guidelines.

## 5. Evaluation and iteration

RAG systems benefit from:

- Spot-checking retrieved documents for representative queries.
- Monitoring answer correctness and hallucination rate.
- Adjusting:
  - Chunking
  - Embedding model
  - Vector store configuration
  - Retrieval parameters (k, filters)
  - Prompt wording and structure

## 6. Performance considerations

For performance:

- Reuse embeddings and vector stores instead of recomputing.
- Use batch operations for index building.
- Add caching layers for recurrent queries when feasible.
- Consider using hybrid or hierarchical search when corpora become large.
