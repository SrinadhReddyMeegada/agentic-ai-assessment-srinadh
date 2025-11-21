
---

### 📘 `task6_ui_agent/README.md`

```markdown
# Task 6 – State-Aware UI Agent (E-commerce Assistant)

This task implements a **simple e-commerce assistant** that:

- Maintains a **UI state model** (`UIState`)
- Modifies UI state based on user commands
- Demonstrates **state introspection** ("show state")
- Shows multi-turn conversation across 3+ turns

No external LLM is required here – the agent is **rule-based** so that the logic is easy to explain in an interview, but the same structure can be wired to an LLM later.

---

## Files

- `ui_state.py`  
  Pydantic models for:
  - `FilterState`
  - `CartItem`
  - `UIState`

- `agent.py`  
  Contains `UIAgent`, which:
  - Holds a `UIState` instance
  - Parses user messages
  - Updates UI state (cart, filters, current view)
  - Uses introspection to describe the current state

- `sample_conversation.md`  
  Example 5-turn conversation demonstrating:
  - State changes
  - Cart updates
  - Introspection

---

## How to run

From repo root:

```bash
cd task6_ui_agent
python agent.py
