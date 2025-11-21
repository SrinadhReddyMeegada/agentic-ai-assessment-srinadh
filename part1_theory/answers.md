
_Agentic AI — Post-Course Assessment Answers_

---

## 1. Agent Architecture

### **1.1 Functional difference between an Agent and a Chatbot**

| Concept | Chatbot | Agent |
|--------|---------|--------|
| Purpose | Respond to user messages | Achieve a goal / complete tasks |
| Intelligence | Pattern-based conversational | Autonomous decision-making |
| Tools | Usually none | Can use tools: search, APIs, DB, functions |
| Memory | Optional, simple | Full-state memory + contextual awareness |
| Execution | One-turn or multi-turn replies | Multi-step planning, acting, reasoning |
| Workflow | Input → Output | Plan → Tools → Reflect → Act → Final output |

**In simple words:**  
A chatbot talks.  
An agent *thinks + decides + uses tools + takes action*.

**Example:**
- Chatbot → “Hi, how can I help?”  
- Agent → Searches the web, summarises, writes a report, saves it to a file.

---

### **1.2 When NOT to use AI (3 scenarios)**

#### **Scenario 1 — Deterministic logic**
If the problem has a fixed, rule-based answer.

Examples:
- Tax calculation  
- OTP generation  
- Interest calculation

Reason:  
LLMs may hallucinate, and deterministic logic is faster, cheaper, safer.

---

#### **Scenario 2 — High-accuracy legal/financial decisions**
Examples:
- Approving loans  
- Diagnosing diseases  
- Background checks  

Reason:  
LLMs are probabilistic. These tasks require guaranteed correctness.

---

#### **Scenario 3 — Sensitive or confidential data processing**
If the input contains:
- Personal identifiable information  
- Company confidential documents  
- Medical reports  

Reason:  
LLM usage creates compliance/security concerns.

---

### **1.3 State Awareness in LLMs via Introspection**

**State awareness** means the LLM knows:
- What it has done  
- What it plans to do  
- What step it's currently on  
- What tools it should use  

LLMs do **introspection** by:
1. Reading their own previous messages  
2. Inspecting the internal state model (like Pydantic state)  
3. Reflecting:  
   > “What is the user asking?”  
   > “What is the system instructing?”  
   > “What information do I currently have?”

**Example:**
An e-commerce UI agent knows:
- Cart items  
- Active filters  
- Current screen (home, cart, product)

So the agent can reason:
> “The user added an item earlier, cart is not empty → show checkout button.”

---

## 2. LLM Mechanics

### **2.1 How an LLM processes a request (developer perspective)**

1. **Prompt construction** → system + user instructions  
2. **Tokenisation** → words → tokens  
3. **Model inference** → transformer layers compute next-token probabilities  
4. **Tool selection** (if applicable)  
5. **Response generation** → streaming output  
6. **State update** → append message to memory / agent state  

Devs mainly control:
- System prompt  
- Tools  
- State model  
- Agent loop logic  

---

### **2.2 Role of tools / function calls**

Tools extend LLM abilities beyond text generation.

Without tools, LLMs can only **talk**.  
With tools, LLMs can **act**.

Examples:
- Web search  
- Database lookup  
- Python execution  
- File creation  
- API calls

Tools turn the model into an **agent**.

---

### **2.3 Purpose of logging in production agent systems**

Logging is critical for:
- Debugging agent failures  
- Monitoring tool usage  
- Observability (trace what the agent decided)  
- Performance measurement  
- Auditing for compliance  
- Tracing hallucinations  
- Understanding state transitions  

Modern agent frameworks rely on:
- Structured logs  
- Traces  
- Step-level histories  
- OpenTelemetry standards  
- Logfire instrumentation  

---

## 3. Retrieval-Augmented Generation (RAGs)

### **3.1 Standard RAG vs Hierarchical RAG**

| Feature | Standard RAG | Hierarchical RAG |
|---------|--------------|------------------|
| Chunking | Flat chunks | Multi-level chunking (sections → sub-sections → paragraphs) |
| Retrieval | Vector search | Tree-based retrieval (top-down) |
| When useful | Small documents | Books, large PDFs, multi-topic content |
| Accuracy | Good | Higher (less noise) |
| Cost | Cheaper | Slightly more expensive |
| Hallucination rate | Medium | Lower |

---

### **3.2 When to use each**

#### **Use Standard RAG when:**
- Your content is small (1–20 pages)
- Retrieval is straightforward
- You need fast, cheap lookups

#### **Use Hierarchical RAG when:**
- Large documents (100+ pages)
- Multi-topic info (manuals, books)
- You need structured contextual retrieval

---

### **3.3 Limitations**

#### **Standard RAG limitation:**  
May retrieve noisy or irrelevant chunks.

#### **Hierarchical RAG limitation:**  
Multiple processing stages → slower & more expensive.

---

## 4. Correct Way to Use Copilot (10 points)

**Copilot is a productivity tool, NOT a brain.**

Proper usage:
1. Give **clear, specific prompts**  
2. Provide **context** → file, function, expected output  
3. Review code line-by-line  
4. Never trust generated code blindly  
5. Ask Copilot to explain changes  
6. Use it as a **pair programmer**, not a code generator  
7. Keep security-sensitive logic manual  
8. Use comments to guide Copilot:  
   ```python
   # Copilot: refactor this function for readability
   ```

Improper usage:
- Asking Copilot to write entire projects
- Blindly pasting generated code  
- Using it without testing  
