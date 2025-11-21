# Task 5 – Research Agent (Pydantic-AI + Gemini + Logfire)

This task implements a **research agent** that:

- Uses **Pydantic-AI** with **Gemini** (via `google-gla:*` models)
- Uses **Logfire** for observability (`logfire.instrument_pydantic_ai`)
- Demonstrates **tool calls**:
  - `web_search` – mock search API
  - `summarize_snippets` – compresses raw snippets
- Runs a simple pipeline:
  1. Interpret research question
  2. Call tools (search → summarize)
  3. Synthesize a final structured report
  4. Log everything via Logfire
  5. Append a human-readable log entry to `sample_logs.txt`

---

## How to run

From repo root:

```bash
cd task5_research_agent
python main.py "How will AI agents change supply chain optimization in the next 5 years?"
