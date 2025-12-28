# LangChain Architecture Overview

This document describes a conceptual view of modern LangChain architecture focused on:

- Runnables and the LangChain Expression Language (LCEL)
- Prompt and model abstractions
- Tools and agents
- Retrieval and vector stores
- Orchestration and workflows

## 1. Core concepts

### 1.1 Runnables

Runnables are composable units that support a standard interface:

- `invoke(input)`
- `ainvoke(input)`
- `batch(inputs)`
- `stream(input)`

Most LangChain components (prompts, models, parsers, retrievers, chains) are or can be wrapped as Runnables. LCEL uses operator overloading (`|`) to compose them.

### 1.2 Prompts and models

- Prompt templates parameterize text generation with variables.
- Chat models and LLMs are wrapped to expose a Runnable interface.
- Chains typically connect prompt → model → parser.

## 2. Tools and agents

### 2.1 Tools

Tools are typed functions that expose capabilities which a model cannot perform alone (e.g., math, external APIs, databases). Good tools:

- Have a clear, narrow purpose.
- Provide strict input and output types.
- Include precise docstrings for the model to read.

### 2.2 Agents

Agents combine:

- A tool-capable model.
- A set of tools.
- A loop or policy that decides which tool to call and when to stop.

Modern agents are often implemented with tool-calling models and helper constructors such as `create_tool_calling_agent` and `AgentExecutor`.

## 3. Retrieval and vector stores

### 3.1 Vector stores

Vector stores:

- Index embedding vectors for documents.
- Support similarity search and related operations.
- Often provide persistence and filtering.

### 3.2 Retrievers

Retrievers:

- Provide a high-level `query -> documents` interface.
- Hide the specifics of the underlying vector store or search engine.
- Are the preferred interface for RAG pipelines.

## 4. Workflows and control flow

LCEL supports:

- Sequential composition with `|`.
- Parallel composition with `RunnableParallel`.
- Branching with `RunnableBranch`.
- Mapping over inputs with `RunnableMap`.

For complex, multi-step or multi-agent workflows, LangGraph can be used to model states and transitions explicitly.

## 5. Project structure and configuration

A typical LangChain project separates:

- Configuration (API keys, model names, environment-specific settings)
- Core components (prompts, models, tools, retrievers)
- Application code (APIs, CLIs, orchestration logic)

This separation simplifies testing, observability, and deployment.
