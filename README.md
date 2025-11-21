<!-- README.md -->

# Agentic AI – Post-Course Assessment

This repo contains your full **Post-Course Assessment** implementation:

- **Part 1 – Conceptual Understanding (40 pts)**
- **Part 2 – Task 5: Research Agent (30 pts)**
- **Part 2 – Task 6: State-Aware UI Agent (30 pts)**
  - CLI version
  - Web UI with FastAPI

Everything is wired to use:

- **Pydantic-AI** for agents
- **Gemini (via Generative Language API)** as the LLM
- **Pydantic Logfire** for observability

---

## 1. Project Structure

```text
agentic-ai/
├── README.md
├── part1_theory/
│   └── answers.md
├── task5_research_agent/
│   ├── README.md
│   ├── requirements.txt
│   ├── main.py
│   ├── models.py
│   ├── tools.py
│   ├── logfire_instrumentation.py
│   └── sample_logs.txt
├── task6_ui_agent/
│   ├── README.md
│   ├── ui_state.py
│   ├── agent.py
│   └── sample_conversation.md
└── task6_ui_agent_web/
    ├── README.md
    ├── backend.py
    ├── ui_state.py
    ├── requirements.txt
    └── index.html
