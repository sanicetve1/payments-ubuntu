# Rebuild Plan (from scratch) — Autonomous Fraud-Analysis Chatbot

## 1) What I understood from your current repo

Based on the current codebase, your earlier implementation already had the **core building blocks** of the system you describe, but with inconsistent maturity and some hardcoded assumptions.

### Architecture already present
- A FastAPI backend exposing customer/payment/risk endpoints (`app/main.py`, routers).
- A Streamlit chat UI (`ui/AgentUI.py`) that routes user prompts into agent code.
- LangGraph-style orchestration in `agents/graph.py` with intent routing and branching.
- Tool wrappers that call backend APIs (`tools/api_tools.py`, `tools/time_tools.py`, `tools/base_tools.py`).
- Optional RAG support through Chroma + sentence-transformers (`tools/rag_tool.py`, vector folders).
- SQLite-based dataset already present (`stripe/stripe_test.db`).

### Gaps/pain points observed
- Some config values are hardcoded (e.g., DB path/API base URL), reducing portability.
- Tool URL configuration is inconsistent across tool modules.
- Import-time model initialization can create fragility in constrained environments.
- Legacy/copy files indicate iterative experiments and unclear source-of-truth modules.
- Agent behavior is close to target but not cleanly packaged as a fresh, explainable demo.

## 2) What you want to build now (target product definition)

From your latest brief, the product intent is:

1. **Autonomous chatbot with tool access**  
   - The assistant should decide which tools to call on its own.

2. **LangGraph-first implementation with context + memory**  
   - Multi-step flow, stateful execution, and conversational continuity.

3. **Customer + payments test database**  
   - Reproducible seed data including fraud/dispute scenarios.

4. **Fraud-focused analyst experience**  
   - User asks questions like: “Which customers had fraudulent transactions in the past?”
   - Agent should surface suspicious/priority transactions and rationale.

5. **Demonstrate autonomous tool choice clearly**  
   - The demo must prove that tool selection is agent-driven (not hardcoded by prompt routing only).

## 3) Proposed rebuild strategy (clean-slate, phased)

## Phase 0 — Define demo success criteria
- Define 8–12 canonical user questions.
- Define what “good answer” means for each (accuracy + explanation + trace).
- Decide scope: payments fraud triage first; RAG optional in v2.

**Deliverable:** `docs/demo_scenarios.md` and acceptance checklist.

## Phase 1 — Create clean project skeleton
- Create a new app structure (do not rely on legacy copy files).
- Separate clearly:
  - `backend/` (FastAPI + DB)
  - `agent/` (LangGraph state, nodes, tools)
  - `ui/` (chat frontend)
  - `infra/` (Docker, env templates)
  - `tests/` (unit/integration/e2e)

**Deliverable:** minimal runnable skeleton with health endpoint.

## Phase 2 — Data model + seeded test dataset
- Define normalized schema:
  - customers
  - payments
  - disputes
  - fraud_flags / risk_signals
- Add deterministic seed script with realistic fraud patterns:
  - chargebacks
  - repeated high-risk merchant categories
  - velocity anomalies
  - cross-border spikes

**Deliverable:** reproducible SQLite (or Postgres) seed process + fixture docs.

## Phase 3 — API layer for analyst-friendly retrieval
- Build explicit query endpoints:
  - list customers
  - payments by filters/date/method/country
  - flagged transactions
  - customer risk summary
- Ensure all endpoints support pagination/filtering and predictable response schemas.

**Deliverable:** OpenAPI-documented backend + smoke tests.

## Phase 4 — Tooling contract for the agent
- Create agent tools that wrap API endpoints with strict input schemas.
- Standardize one `BASE_URL` source from environment.
- Add robust error normalization so the agent can recover from failures.

**Deliverable:** typed tool registry + tool unit tests.

## Phase 5 — LangGraph autonomous workflow
- Build explicit graph state (conversation, tool outputs, risk hypotheses, next action).
- Nodes (example):
  - intent/routing
  - planner
  - tool executor
  - evidence synthesizer
  - response formatter
- Include conditional edges for iterative tool-use loops until confidence threshold.

**Deliverable:** graph that demonstrates autonomous multi-step reasoning with tool calls.

## Phase 6 — Memory and context
- Short-term memory: per-session conversation summary.
- Analytical memory: reusable “risk facts” derived during a session.
- Guardrails to avoid stale/incorrect memory reuse.

**Deliverable:** memory policy + tests for follow-up questions.

## Phase 7 — UX for explainability
- UI should show:
  - final answer
  - transactions/customer IDs cited
  - why they are suspicious
  - optional “trace” panel (tool calls, decisions)

**Deliverable:** simple fraud analyst demo screen with transparent outputs.

## Phase 8 — Evaluation + hardening
- Add eval set from Phase 0 scenarios.
- Measure:
  - tool selection correctness
  - factual correctness
  - missed-risk rate / false positives
- Add Docker/Compose for one-command startup.

**Deliverable:** reproducible demo runbook and scorecard.

## 4) Recommended MVP cut (fastest path to value)

For an MVP demo, implement only:
- One DB (SQLite) with strong seed data.
- FastAPI with 4–6 key endpoints.
- 4 core tools (`get_flagged_transactions`, `get_customer_profile`, `get_customer_payments`, `get_risk_summary`).
- One LangGraph loop demonstrating autonomous selection of these tools.
- Streamlit interface with answer + evidence table + trace.

Defer to v2:
- RAG/legal documents.
- Multi-agent orchestration.
- Advanced anomaly models.

## 5) Key design principles for this rebuild
- **Deterministic demo first, intelligence second.**
- **Single source of truth for config and tool endpoints.**
- **Traceability over “black box” answers.**
- **Every fraud claim must map to explicit records.**
- **No secret keys in repo; runtime-only secret injection.**

## 6) Suggested next step (still planning-only)

If this plan matches your goal, next planning artifact should be:
- `plan-architecture.md` with
  - exact folder structure,
  - DB schema (tables/fields),
  - LangGraph state model,
  - tool signatures,
  - 10 demo questions + expected outputs.

