"""
basic_rag.py

Reference RAG pipeline using LangChain.

Features:
- DirectoryLoader-based ingestion.
- Chunking, embeddings, FAISS vector store.
- LCEL RAG chain with retriever and chat model.
"""

import os
from pathlib import Path
from typing import Iterable, List

from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.vectorstores import VectorStore


# ---------------------------------------------------------------------------
# Ingestion and indexing
# ---------------------------------------------------------------------------

def load_documents(path: str | Path) -> List[Document]:
    """Load documents from a directory path."""
    loader = DirectoryLoader(str(path))
    return loader.load()


def split_documents(
    docs: Iterable[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> List[Document]:
    """Split documents into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(list(docs))


def build_vectorstore(
    docs: Iterable[Document],
) -> VectorStore:
    """
    Build a FAISS vector store from documents using OpenAI embeddings.

    Expects OPENAI_API_KEY to be set in the environment.
    """
    embeddings = OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    )
    return FAISS.from_documents(list(docs), embeddings)


# ---------------------------------------------------------------------------
# RAG chain
# ---------------------------------------------------------------------------

def build_rag_chain(vectorstore: VectorStore) -> Runnable:
    """
    Build an LCEL RAG chain that:
    - uses a retriever from the vector store,
    - injects context and question into a prompt,
    - calls a chat model.
    """
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": int(os.getenv("RAG_TOP_K", "4"))}
    )

    prompt = ChatPromptTemplate.from_template(
        "Use the context to answer the question.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer in a concise and clear way. If the context does not "
        "contain the answer, say that the answer is not known."
    )

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
    )

    rag_chain: Runnable = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    return rag_chain


def build_default_rag_chain(
    docs_path: str | Path,
) -> Runnable:
    """
    Convenience function to:
    - load documents from docs_path,
    - split them,
    - build a vector store,
    - return a ready RAG chain.
    """
    docs = load_documents(docs_path)
    chunks = split_documents(docs)
    vectorstore = build_vectorstore(chunks)
    return build_rag_chain(vectorstore)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """
    CLI entrypoint.

    Example:
        export OPENAI_API_KEY="sk-..."
        python -m scripts.basic_rag ./assets/sample_documents \
          "What is this corpus about?"
    """
    import argparse

    parser = argparse.ArgumentParser(description="Run RAG over a document folder.")
    parser.add_argument(
        "docs_path",
        type=str,
        help="Path to directory with documents.",
    )
    parser.add_argument(
        "question",
        type=str,
        nargs="*",
        help="Question to ask over the documents.",
    )
    args = parser.parse_args()

    if not args.question:
        parser.error("Provide a question to ask about the documents.")

    question = " ".join(args.question)
    chain = build_default_rag_chain(args.docs_path)

    print(f"\n=== Question ===\n{question}\n")
    result = chain.invoke(question)
    # result is a ChatMessage-like object
    content = getattr(result, "content", result)
    print("=== Answer ===")
    print(content)


if __name__ == "__main__":
    main()
