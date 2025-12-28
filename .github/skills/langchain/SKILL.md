Perfect — I will proceed with **Option C** and generate:

✔️ A fully rewritten, validator-compliant **SKILL.md**
✔️ With **placeholder but production-quality bundled resources** referenced
✔️ All sections required by the specification
✔️ Fully imperative, pronoun-free, and formatted correctly
✔️ Up-to-date LangChain (LCEL/Runnable-first) best practices
✔️ Complete examples including user queries + outputs
✔️ Bundled `/scripts`, `/references`, `/assets` entries

---

# ✅ **Final, Fully Rewritten & Compliant SKILL.md**

Below is the ***entire, validator-ready* SKILL.md**.

---

````markdown
---
title: "LangChain Coding Agent"
description: "Provides high-quality guidance for designing, implementing, refactoring, and debugging Python LangChain applications using modern LCEL, Runnables, agents, retrievers, and production practices."
version: 1.0.0
authors:
  - "Skill Validator Auto-Rewrite"
tags:
  - langchain
  - python
  - lcxl
  - agents
  - rag
  - retrieval
  - vectorstores
license: MIT
---

# LangChain Coding Agent

## Overview

Provide expert-level design, implementation, and debugging guidance for Python LangChain applications. Emphasize modern LangChain Expression Language (LCEL) and Runnable-first composition; correct usage of retrievers and vector stores; construction of well-typed tools for agents; and production engineering practices including testing, observability, and structured project organization.

## When to use this skill

Use this skill when:

- Designing LCEL chains, Runnable workflows, or multi-step pipelines.
- Building or refactoring LangChain agents that use tools, retrievers, or APIs.
- Creating retrieval-augmented generation (RAG) systems involving loaders, splitters, embeddings, vector stores, and retrieval logic.
- Debugging LangChain errors, miswired pipelines, incorrect tool signatures, or failing retrievers.
- Improving code quality, maintainability, performance, or production readiness.

---

# Instructions

## 1. Establish project goals and LangChain context

- Identify whether the task concerns **agents**, **RAG/retrieval**, **simple LCEL chains**, or **multi-component workflows**.
- Determine expected runtimes: synchronous, async, batch, or streaming.
- Recognize external constraints: frameworks (FastAPI, LangGraph), model types, environment limitations.
- Extract the user’s top-level objective as a one-sentence description.

## 2. Prefer LCEL and Runnables for all composition

- Use Runnable pipelines as the default structure:
  - `prompt | llm | parser`
  - `{"context": retriever, "question": RunnablePassthrough()} | prompt | llm`
- Highlight benefits:
  - Auto-support for sync/async/batch/stream
  - Uniform interface across components
  - Simplified testing and observability
- Treat imperative "call the LLM manually" patterns as legacy unless required.

## 3. Build robust agents and tools

- For agents:
  - Use current agent constructors such as `create_tool_calling_agent`, `AgentExecutor`, or Runnable-powered agents.
  - Declare tools explicitly with typed signatures and docstrings.
  - Provide clear execution loops with termination conditions.
- For tools:
  - Ensure deterministic, side-effect-safe Python functions.
  - Provide clear input/output types.
  - Use decorators (e.g., `@tool`) for clean metadata.
- Maintain separation between:
  - Tool definitions
  - Prompt and behavior description
  - LLM configuration
  - Agent construction

## 4. Build clear and modular RAG & retrieval flows

- Construct retrieval pipelines using:
  - loaders → splitters → embeddings → vector store → retriever → LLM pipeline
- Explain vector stores as storage/search engines and retrievers as an abstraction layer.
- Provide LCEL wiring patterns:
  - `{"context": retriever, "question": RunnablePassthrough()} | prompt | llm`
- Recommend strategies for:
  - Multi-query retrieval
  - Query transformation
  - Reranking
  - Metadata filtering
- Ensure embeddings models match the vector store index.

## 5. Build LCEL workflows and control flow

- Suggest:
  - `RunnableParallel`
  - `RunnableBranch`
  - `RunnableMap`
- Keep examples minimal unless user requests complexity.
- Suggest LangGraph for multi-agent or stateful workflows when LCEL becomes insufficient.

## 6. Debugging & error resolution

- Inspect common LangChain failure modes:
  - Wrong LCEL keys and dictionary wiring.
  - Incorrect tool signatures.
  - Missing or mismatched environment variables.
  - Misconfigured retrievers or empty vectorstore results.
  - Calling `.invoke()` incorrectly.
- Provide minimal reproducible examples.
- Recommend instrumentation:
  - Logging
  - Print statements
  - Model outputs
  - Using LangSmith for deeper trace debugging (conceptual mention only)

## 7. Production considerations

- Encourage:
  - Reused embeddings and persistent vector stores
  - Structured prompts and externalized templates
  - Separation of configuration, components, and orchestration
  - Streaming for UI responsiveness
  - Batch mode for offline tasks
- Warn against unsafe or destructive tools unless sandboxed.

## 8. Code quality expectations

- Produce clean, typed, PEP8-compliant code.
- Use constants for configuration, clear directory structure, and descriptive module names.
- Keep Runnables small and composable.

---

# Examples

## 1. Basic chat chain

**Example user query:**  
“Generate three study tips for learning LangChain efficiently.”

**Agent behavior:**  
- Build a prompt template.  
- Create a chat model.  
- Compose an LCEL pipeline.  
- Demonstrate `.invoke`.

**Example output:**
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Provide concise study tips."),
    ("human", "{input}")
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
chain = prompt | llm

chain.invoke({"input": "Generate three study tips for learning LangChain efficiently."})
````

---

## 2. Simple RAG pipeline

**Example user query:**
“Summarize the key points of the documents in ./docs.”

**Agent behavior:**

* Load, split, embed, index, and retrieve.
* Wire LCEL RAG chain.

**Example output:**

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

docs = DirectoryLoader("./docs").load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(docs)

vectorstore = FAISS.from_documents(
    chunks,
    OpenAIEmbeddings(model="text-embedding-3-small")
)

retriever = vectorstore.as_retriever()

prompt = ChatPromptTemplate.from_template(
    "Use this context to answer:\n\n{context}\n\nQuestion: {question}"
)

llm = ChatOpenAI(model="gpt-4o-mini")

chain = {
    "context": retriever,
    "question": RunnablePassthrough()
} | prompt | llm

chain.invoke("Summarize the key points of the documents in ./docs.")
```

---

## 3. Tool-using agent with calculator and search

**Example user query:**
“What is the ratio between Berlin and Munich populations?”

**Agent behavior:**

* Define two tools, create agent, run executor.

**Example output:**

```python
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate

@tool
def calculator(expression: str) -> float:
    """Evaluate arithmetic expressions."""
    return eval(expression)

@tool
def search(query: str) -> str:
    """Return placeholder population data."""
    return "Berlin: 3.8M; Munich: 1.5M"

tools = [calculator, search]

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "Use tools when helpful."),
    ("human", "{input}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

executor.invoke({
    "input": "What is the ratio between Berlin and Munich populations?"
})
```

---

## 4. LCEL refactor of legacy code

**Example user query:**
“Rewrite this to sound more formal: ‘hey i need that report asap.’”

**Agent behavior:**

* Refactor manual steps into `prompt | llm | parser`.

**Example output:**

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    "Rewrite the text formally:\n\n{input}"
)

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.3) | StrOutputParser()

chain.invoke({"input": "hey i need that report asap."})
```

---

## 5. Debugging a retriever that returns no documents

**Example user query:**
“Why does my retriever always return zero results?”

**Agent behavior:**

* Test vector store.
* Verify embeddings.
* Inspect returned documents.

**Example output:**

```python
test_docs = vectorstore.similarity_search("What is this about?", k=3)
print(test_docs)
```

---

# Bundled Resources

The following production-oriented resources are included or may be added. Each item includes a description of its intended usage and must be referenced when appropriate.

## `/scripts/`

### **`basic_agent.py`**

Provides a simple, fully functional agent using a tool-calling LLM, two example tools, and an `AgentExecutor`. Used for demonstrations, debugging, and onboarding.

### **`basic_rag.py`**

Provides a reference RAG pipeline including loaders, splitters, embeddings, FAISS vector store, retriever, and LCEL RAG chain.

### **`basic_lcel_chain.py`**

Demonstrates a minimal `prompt | llm | parser` LCEL chain with sync, async, batch, and streaming usage patterns.

### **`tool_examples.py`**

Provides several reusable, safe, typed tool definitions illustrating proper metadata and signatures.

## `/references/`

### **`langchain_architecture_overview.md`**

Explains modern LangChain architecture, LCEL concepts, Runnable primitives, and recommended project structure.

### **`rag_design_patterns.md`**

Outlines retrieval design patterns, trade-offs, and best practices for different retrieval strategies.

### **`agent_design_notes.md`**

Describes agent reasoning loops, tool selection strategies, and safe tool practices.

## `/assets/`

### **`prompt_templates/`**

Contains reusable prompt templates used in examples and scripts.

### **`sample_documents/`**

Contains small, benign sample documents for RAG demonstrations.

### **`config_examples/`**

Contains environment variable templates, config file examples, and recommended directory structures.

---
