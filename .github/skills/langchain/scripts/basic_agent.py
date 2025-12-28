"""
basic_agent.py

Minimal but production-oriented example of a LangChain tool-using agent.

Features:
- Modern tool-calling agent pattern.
- Typed tools with clear docstrings.
- Simple CLI entrypoint.
"""

import os
from typing import Any, Dict

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

@tool
def calculator(expression: str) -> float:
    """Evaluate basic arithmetic expressions like '2 + 2 * 5'."""
    try:
        # In production, consider using a safe math parser instead of eval.
        return float(eval(expression))
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Invalid expression '{expression}': {exc}") from exc


@tool
def fake_search(query: str) -> str:
    """
    Simulate a search tool.

    In production, replace with a real search implementation that calls an API
    such as a web search provider or an internal knowledge service.
    """
    # This is intentionally a stub.
    return (
        "Search results for query: "
        f"'{query}'. Replace fake_search with a real integration."
    )


TOOLS = [calculator, fake_search]


# ---------------------------------------------------------------------------
# Agent construction
# ---------------------------------------------------------------------------

def build_llm() -> ChatOpenAI:
    """
    Build a chat model instance.

    Expects OPENAI_API_KEY (or compatible) to be set in the environment.
    """
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.0")),
    )


def build_agent() -> AgentExecutor:
    """
    Create a tool-calling agent wrapped in an AgentExecutor.

    The agent:
    - Receives a user input.
    - Decides whether to call tools.
    - Returns a final natural-language answer.
    """
    llm = build_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "Act as a helpful assistant. "
                    "Use tools when necessary to perform accurate calculations "
                    "or retrieve factual information."
                ),
            ),
            ("human", "{input}"),
        ]
    )

    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
    )
    return executor


def run_agent(input_text: str) -> Dict[str, Any]:
    """Run the agent on a single input string and return the full result dict."""
    executor = build_agent()
    return executor.invoke({"input": input_text})


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Simple CLI entrypoint.

    Example:
        export OPENAI_API_KEY="sk-..."
        python -m scripts.basic_agent "What is (3 + 5) * 2?"
    """
    import argparse

    parser = argparse.ArgumentParser(description="Run the basic LangChain agent.")
    parser.add_argument(
        "input",
        type=str,
        nargs="*",
        help="User query for the agent.",
    )
    args = parser.parse_args()

    if not args.input:
        parser.error("Provide an input string, e.g. `basic_agent.py '2 + 2'`")

    query = " ".join(args.input)
    result = run_agent(query)
    print("\n=== Agent Output ===")
    print(result.get("output", ""))


if __name__ == "__main__":
    main()
