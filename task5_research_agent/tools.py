from __future__ import annotations

from typing import List

from pydantic_ai import RunContext

from models import ResearchDependencies, SearchResult


async def web_search(
    ctx: RunContext[ResearchDependencies],
    query: str,
) -> List[SearchResult]:
    """
    Mock web search tool.
    """
    max_snippets = max(1, min(ctx.deps.max_snippets, 5))

    base_results = [
        SearchResult(
            title="AI Agents: From Chatbots to Autonomous Workflows",
            url="https://example.com/ai-agents-overview",
            snippet=(
                "Explains how modern AI agents combine LLM reasoning with tools, "
                "memory, and state to perform multi-step tasks like research and "
                "planning."
            ),
        ),
        SearchResult(
            title="Domain Report: Trends in AI-driven Research Automation",
            url="https://example.com/research-automation-report",
            snippet=(
                "Survey of companies using LLM agents to automate competitor analysis, "
                "summarize academic papers, and synthesize reports for analysts."
            ),
        ),
        SearchResult(
            title="Best Practices for Using RAG with Gemini",
            url="https://example.com/rag-gemini-best-practices",
            snippet=(
                "Recommends combining retrieval-augmented generation with strong "
                "logging, evaluation, and guardrails when building research tools."
            ),
        ),
        SearchResult(
            title="Observability for AI Agents with Logfire",
            url="https://example.com/logfire-ai-observability",
            snippet=(
                "Shows how Pydantic Logfire can trace agent runs, tool calls, and "
                "latency, enabling safe iteration in production."
            ),
        ),
        SearchResult(
            title="Limitations of LLM-based Research",
            url="https://example.com/llm-research-limitations",
            snippet=(
                "Discusses hallucinations, outdated training data, and the need to "
                "cross-check generated insights against primary sources."
            ),
        ),
    ]

    return base_results[:max_snippets]


async def summarize_snippets(
    ctx: RunContext[ResearchDependencies],
    snippets: List[str],
) -> dict:
    """
    Summarize snippets AND return snippet count.
    """
    unique = []
    for s in snippets:
        norm = " ".join(s.split())
        if norm not in unique:
            unique.append(norm)

    merged = " ".join(unique)

    # trimming
    max_chars = 1200
    if len(merged) > max_chars:
        merged = merged[: max_chars - 3] + "..."

    return {
        "summary": merged,
        "num_snippets": len(snippets),
    }
