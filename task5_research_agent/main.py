from __future__ import annotations

import argparse
import os
from datetime import datetime
from typing import List

import logfire
from pydantic_ai import Agent, Tool

from logfire_instrumentation import configure_logfire
from models import ResearchContext, ResearchDependencies, ResearchSummary
from tools import summarize_snippets, web_search
os.environ["MODEL"] = "google-gla:gemini-2.5-flash"


def build_model_name() -> str:
    """
    Return the model name for the research agent.

    We use the same configuration that worked in your test chatbot:
    - Provider: google-gla (Google Generative Language API)
    - Model:   gemini-2.5-flash

    You can override this by setting MODEL in .env if needed.
    """
    return os.getenv("MODEL", "google-gla:gemini-2.5-flash")


def build_agent() -> Agent[ResearchDependencies, ResearchSummary]:
    """
    Create the Pydantic-AI research agent.

    The agent:
    - Uses Gemini 2.5 Flash via the Google GLA provider
    - Accepts ResearchDependencies as deps
    - Outputs a validated ResearchSummary
    - Has two tools:
      * web_search
      * summarize_snippets
    """

    model_name = build_model_name()

    tools: List[Tool[ResearchDependencies]] = [
        Tool(web_search),
        Tool(summarize_snippets),
    ]

    instructions = (
        "You are a senior research analyst. Your job is to read search snippets, "
        "synthesize a balanced, non-hallucinated answer, and be explicit about "
        "what is assumption vs fact. Always:\n"
        "1. Use the `web_search` tool to gather context.\n"
        "2. Use `summarize_snippets` to compress the snippets.\n"
        "3. Then write a concise short answer plus bullet-point key findings.\n"
        "4. List the sources you relied on.\n"
        "If information is uncertain or speculative, call it out clearly."
    )

    agent: Agent[ResearchDependencies, ResearchSummary] = Agent(
        model_name,
        deps_type=ResearchDependencies,
        output_type=ResearchSummary,
        instructions=instructions,
        tools=tools,
    )

    return agent


def run_research(question: str) -> ResearchSummary:
    """
    Top-level orchestration for a single research run.

    This function is what you'd typically call from a CLI, scheduled job,
    or web handler.
    """
    configure_logfire()

    ctx = ResearchContext(question=question, started_at=datetime.utcnow())
    logfire.info("research.start", question=question)

    agent = build_agent()

    deps = ResearchDependencies(max_snippets=5)

    # Run synchronously for CLI simplicity.
    result = agent.run_sync(question, deps=deps)

    # Compute how many snippets were used by inspecting tool calls.
    # Universal version — snippet count comes from summarizer tool
    ctx.num_snippets = getattr(result.output, "num_snippets", 0)
    ctx.mark_completed()

    logfire.info(
        "research.completed",
        question=ctx.question,
        num_snippets=ctx.num_snippets,
        started_at=ctx.started_at.isoformat(),
        completed_at=ctx.completed_at.isoformat() if ctx.completed_at else None,
    )

    # Also append a simple text log for the assessment.
    _append_sample_log(ctx, result.output)

    return result.output


def _append_sample_log(ctx: ResearchContext, summary: ResearchSummary) -> None:
    """Append a human-readable log entry to sample_logs.txt."""
    log_path = os.path.join(os.path.dirname(__file__), "sample_logs.txt")

    lines = [
        "==============================",
        f"Run at:        {ctx.started_at.isoformat()}",
        f"Completed at:  {ctx.completed_at.isoformat() if ctx.completed_at else 'N/A'}",
        f"Question:      {ctx.question}",
        f"Snippets used: {ctx.num_snippets}",
        "",
        "Short answer:",
        summary.short_answer,
        "",
        "Key points:",
        *[f"- {p}" for p in summary.key_points],
        "",
        "Sources:",
        *[f"- {s}" for s in summary.sources],
        "\n",
    ]

    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _pretty_print(summary: ResearchSummary) -> None:
    """Print the research result in a CLI-friendly format."""
    print("\n" + "=" * 60)
    print("RESEARCH QUESTION")
    print("=" * 60)
    print(summary.question)
    print("\n" + "=" * 60)
    print("SHORT ANSWER")
    print("=" * 60)
    print(summary.short_answer)
    print("\n" + "=" * 60)
    print("KEY POINTS")
    print("=" * 60)
    for point in summary.key_points:
        print(f"- {point}")
    print("\n" + "=" * 60)
    print("ASSUMPTIONS & CAVEATS")
    print("=" * 60)
    for a in summary.assumptions:
        print(f"- {a}")
    print("\n" + "=" * 60)
    print("SOURCES (MOCK)")
    print("=" * 60)
    for s in summary.sources:
        print(f"- {s}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Pydantic-AI Research Agent (Gemini 2.5 Flash)")
    parser.add_argument(
        "question",
        type=str,
        help="Research question to ask the agent",
    )
    args = parser.parse_args()

    summary = run_research(args.question)
    _pretty_print(summary)


if __name__ == "__main__":
    main()
