"""
basic_lcel_chain.py

Minimal LCEL chain example showing:
- sync invoke
- async invoke
- batch
- streaming
"""

import asyncio
import os
from typing import Iterable, List, Any

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable


def build_chain() -> Runnable:
    """
    Build a simple LCEL chain that rewrites text in a friendly style.
    """
    prompt = ChatPromptTemplate.from_template(
        "Rewrite the following text in a friendly, clear tone:\n\n{input}"
    )

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
    )

    parser = StrOutputParser()

    chain: Runnable = prompt | llm | parser
    return chain


def run_sync(input_text: str) -> str:
    """Run the chain synchronously."""
    chain = build_chain()
    return chain.invoke({"input": input_text})


async def run_async(input_text: str) -> str:
    """Run the chain asynchronously."""
    chain = build_chain()
    return await chain.ainvoke({"input": input_text})


def run_batch(inputs: Iterable[str]) -> List[Any]:
    """Run the chain in batch mode."""
    chain = build_chain()
    payloads = [{"input": text} for text in inputs]
    return chain.batch(payloads)


def run_stream(input_text: str) -> str:
    """
    Stream tokens for a single input and return the full concatenated result.
    """
    chain = build_chain()
    chunks: List[str] = []
    for chunk in chain.stream({"input": input_text}):
        # chunk is already parsed to a string by StrOutputParser
        print(chunk, end="", flush=True)
        chunks.append(str(chunk))
    print()  # newline
    return "".join(chunks)


def main() -> None:
    """
    Demonstrate sync, async, batch, and streaming usage.

    Example:
        export OPENAI_API_KEY="sk-..."
        python -m scripts.basic_lcel_chain
    """
    text = "I might get this done at some point, not sure when."

    print("=== Sync ===")
    print(run_sync(text))

    print("\n=== Async ===")
    print(asyncio.run(run_async(text)))

    print("\n=== Batch ===")
    batch_res = run_batch(
        [
            "Please rewrite this politely.",
            "Provide a concise reformulation of this message.",
        ]
    )
    for idx, res in enumerate(batch_res, start=1):
        print(f"[{idx}] {res}")

    print("\n=== Streaming ===")
    run_stream("Explain LangChain in one short paragraph.")


if __name__ == "__main__":
    main()
