# AI Product Manager Portal
## MVP Implementation Plan

### Executive Summary

A deliberately small MVP: a product manager logs in, creates a product, and types up everything they know about it in one go. A **Review Agent** reads that input and asks a short, fixed round of clarifying questions (or none, if the input is already solid). The PM answers once, and a **Synthesis Agent** turns the input + answers into a finished product document. That's the whole loop — no multi-turn chat, no feature breakdown, no validation schemas, no downstream artifacts. Those ideas are noted in §8 as later phases, not part of this build. Stack stays React (shadcn + Tailwind) + Python (FastAPI) + JSON files on disk, with the two agents built as PydanticAI `Agent`s.

---

## 1. MVP User Journey

1. **Log in.** A simple screen asking for a name — no password, nothing persisted server-side. Just enough to feel like "logging in"; gates nothing.
2. **Create a product.** PM clicks "New Product," gives it a title, and writes a single free-text description covering everything they know (problem, users, goals, whatever they have).
3. **Review Agent runs automatically on submit.** It reads the description and decides: is this enough to write a solid product brief, or not? If not, it returns a short, capped list of clarifying questions (e.g., up to 3).
4. **PM answers, once.** If there are questions, the PM sees them as a simple form (one field per question) and submits answers in a single round — no back-and-forth, no follow-up questions to the answers.
5. **Synthesis Agent runs automatically on submit.** It takes the original description plus the Q&A pairs (or just the description, if there were no questions) and produces the finished product document as a set of sections.
6. **PM sees the result.** The synthesized document is displayed and can be edited by hand. Done — that's the full MVP loop.

---

## 2. Tech Stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite, shadcn/ui, Tailwind CSS |
| Backend | Python (FastAPI) |
| Storage | JSON files on disk (one file per product + an index file) |
| Agents | PydanticAI — exactly two agents, each with a Pydantic `output_type` (Claude as the default model) |

---

## 3. Data Model

```
data/
  index.json              # list of all products (id, title, status, timestamps)
  products/
    <product_id>.json       # full content of one product
```

**`index.json`**
```json
{
  "products": [
    {
      "id": "prod_001",
      "title": "Checkout Redesign",
      "status": "synthesized",   // "input" | "questions_pending" | "synthesized"
      "created_at": "2026-07-05T10:00:00Z",
      "updated_at": "2026-07-05T10:00:00Z"
    }
  ]
}
```

**`products/<product_id>.json`**
```json
{
  "id": "prod_001",
  "title": "Checkout Redesign",
  "status": "synthesized",
  "raw_input": "We want to speed up our checkout flow, it currently takes too long and we're losing customers at payment...",
  "questions": [
    "What's the current average checkout completion time?",
    "Which user segment is most affected?"
  ],
  "answers": [
    "About 45 seconds average.",
    "Mostly mobile users."
  ],
  "sections": [
    { "heading": "Overview", "content": "..." },
    { "heading": "Target Users", "content": "..." },
    { "heading": "Success Metrics", "content": "..." }
  ],
  "created_at": "2026-07-05T10:00:00Z",
  "updated_at": "2026-07-05T10:05:00Z"
}
```

`questions`/`answers` stay empty arrays if the Review Agent decided no follow-up was needed.

---

## 4. Backend (Python / FastAPI)

### Agents (PydanticAI)

| Agent | Module | `output_type` | Runs when |
|---|---|---|---|
| **Review Agent** | `agents/review.py` | `ReviewResult{questions: list[str]}` (empty = no follow-up needed) | Right after a product is created, on its `raw_input` |
| **Synthesis Agent** | `agents/synthesis.py` | `SynthesizedDoc{sections: list[Section]}` where `Section{heading: str, content: str}` | Right after answers are submitted (or immediately after Review, if it asked nothing) |

No shared orchestrator, no dependency-injected context beyond what's passed directly into the call — with only two agents and one linear path, the FastAPI routes just call them in sequence.

### API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/products` | List all products |
| `GET` | `/products/{id}` | Get full product content |
| `POST` | `/products` | Create a product (`title`, `raw_input`); runs the Review Agent immediately. If it returns questions, saves them and sets `status: "questions_pending"`. If not, runs the Synthesis Agent immediately and returns `status: "synthesized"` |
| `POST` | `/products/{id}/answers` | Submit `answers` (same order as `questions`); runs the Synthesis Agent and sets `status: "synthesized"` |
| `PUT` | `/products/{id}` | Manual edits to `title`/`sections` after synthesis |

### File Layout
```
backend/
  main.py            # FastAPI app, route definitions
  storage.py          # read/write helpers for index.json and products/*.json
  agents/
    review.py           # Review Agent + ReviewResult model
    synthesis.py         # Synthesis Agent + SynthesizedDoc/Section models
  models.py            # Pydantic schemas for request/response validation (API layer)
data/
  index.json
  products/
```

---

## 5. Frontend (React + shadcn + Tailwind)

### Pages / Views
- **Login** (`/login`) — a name field and a "Continue" button (shadcn `Input` + `Button`); stores the name in local storage, no server call.
- **Product List** (`/`) — table of products (title, status, last updated) with a "New Product" button.
- **New Product Form** (`/products/new`) — title field + a large `Textarea` for the free-text description. Submitting calls `POST /products` and navigates to the product's page.
- **Product Page** (`/products/{id}`) — renders based on `status`:
  - `questions_pending`: a simple form with one `Textarea` per question in `questions`; submitting calls `POST /products/{id}/answers`.
  - `synthesized`: the finished sections rendered as editable `Card`/`Textarea` blocks, with a "Save" button calling `PUT /products/{id}`.

### Component Structure
```
frontend/
  src/
    pages/
      Login.tsx
      ProductList.tsx
      NewProductForm.tsx
      ProductPage.tsx        # renders QuestionsForm or SectionEditor based on status
    components/
      QuestionsForm.tsx
      SectionEditor.tsx
    lib/
      api.ts               # thin fetch wrapper for backend endpoints
```

---

## 6. Implementation Steps

| Step | Task |
|---|---|
| 1 | Scaffold backend: FastAPI app, `storage.py`, `data/` with empty `index.json` |
| 2 | Build the Review Agent and Synthesis Agent (PydanticAI) |
| 3 | Implement `POST /products` (create + run Review, and Synthesis if no questions) and `POST /products/{id}/answers` (run Synthesis) |
| 4 | Implement `GET /products`, `GET /products/{id}`, `PUT /products/{id}` |
| 5 | Scaffold frontend: Vite + React + Tailwind + shadcn, `api.ts` client |
| 6 | Build Login screen (local-storage-only) and Product List |
| 7 | Build New Product Form, Questions Form, and the synthesized Section Editor view |

---

## 7. Open Questions

- Cap on the number of clarifying questions the Review Agent can ask (plan assumes ~3) — worth confirming.
- What happens if the PM leaves an answer blank — does Synthesis just work with what's given, or is a blank field re-prompted (MVP assumption: it just proceeds)?
- Whether "Login" needs to gate anything at all for a single local user, or is purely cosmetic for now.

---

## 8. Beyond the MVP: Full Agent Catalog & Phase Roadmap

Everything from earlier planning, plus the natural remaining agents from the original "AI PM" vision, laid out as a complete catalog with a phase assigned to each. The MVP (Phase 1) is the only phase actually being built now; everything else is roadmap, sequenced so each phase's agents depend only on documents/data that already exist by the end of the previous phase.

### 8.0 Full Agent Catalog

| # | Agent | Phase | Role |
|---|---|---|---|
| 1 | **Review Agent** | 1 (MVP) | Reads the one-shot product description, decides if it's enough, returns a capped list of clarifying questions (or none) |
| 2 | **Synthesis Agent** | 1 (MVP) | Turns the description + Q&A answers into the finished product document (`sections`) |
| 3 | **Refinement Agent** | 2 | Ad-hoc, prompt-driven expansion/rewrite of one or more sections after synthesis, without re-running the whole intake |
| 4 | **Validation Agent** | 2 | Checks a document's sections against its type's required-fields schema, structurally and qualitatively |
| 5 | **Decomposition Agent** | 3 | Splits a validated product into candidate features, and each accepted feature into candidate sub-features |
| 6 | **Architecture Evaluator Agent** | 3 | Reviews a validated feature/sub-feature for technical feasibility, dependencies, and design risk before it's considered buildable |
| 7 | **Artifact Agent** | 4 | Generates downstream artifacts (user stories, test plans, acceptance criteria) from an architecture-approved feature/sub-feature |
| 8 | **Jira/Confluence Agent** | 4 | Publishes finished docs/artifacts as Jira epics/stories and Confluence pages; writes the resulting IDs back to local JSON |
| 9 | **Prioritization Agent** | 5 | Scores and ranks features/sub-features (e.g., RICE-style) using whatever signal exists — architecture risk, artifact scope, PM-supplied inputs |
| 10 | **Roadmap Synthesis Agent** | 5 | Rolls up product/feature statuses and priority scores into a readable roadmap view |
| 11 | **Stakeholder Update Agent** | 5 | Drafts audience-specific status updates (eng standup, exec summary, customer changelog) from current document state |
| 12 | **Meeting Notes Agent** | 5 | Converts a pasted meeting transcript/notes into action items and proposed section updates on the relevant product/feature docs |

### 8.1 Phase 2 — Refine & Structure

Builds directly on the MVP's synthesized documents; no new external dependencies.

- **Refinement Agent**: exposed via a `/documents/{id}/refine` endpoint (the old "Generate Panel" idea) — PM gives a prompt like "expand the Success Metrics section," agent returns updated `sections` merged back into the document. This is the natural answer to the MVP open question about editing after synthesis.
- **Validation Agent**: required-fields JSON schema per document type (`schemas/*.json`), two-pass check (structural + LLM judgment on content quality), gating further progress until `valid: true`.

### 8.2 Phase 3 — Decompose & Evaluate

Turns a single validated product document into a real feature hierarchy, and adds a technical-feasibility gate before anything downstream gets built.

- **Decomposition Agent**: product → candidate features → (per accepted feature) candidate sub-features. PM confirms/deselects proposals at each level before real documents are created, same pattern as the earlier Breakdown Agent design, extended one level deeper.
- **Architecture Evaluator Agent**: takes a validated feature/sub-feature and returns a feasibility verdict + notes (dependencies, risks, open technical questions). A feature that fails this gate goes back to the PM/engineering for rework rather than proceeding.

### 8.3 Phase 4 — Produce & Publish

Generates the artifacts engineering actually needs, then pushes everything out to the tools the team already works in.

- **Artifact Agent**: generates user stories, test plans, or acceptance criteria for any feature/sub-feature that clears architecture review.
- **Jira/Confluence Agent**: creates a Jira epic per product and a story per feature/sub-feature, a Confluence page per doc/artifact, and persists the resulting Jira key / Confluence page URL back onto the local JSON record. This is the system's first external dependency — real auth credentials, network calls, and error handling the earlier phases deliberately avoid.

### 8.4 Phase 5 — Ongoing PM Operations

Once documents exist and are flowing through the pipeline, these agents support the PM's day-to-day work rather than moving a single document forward — this is where the very first version of this plan's "autonomous AI PM" vision (intake triage, backlog grooming, stakeholder updates) actually lands, now with real structured documents to operate on.

- **Prioritization Agent**: scores/ranks features and sub-features so the PM has a proposed order, not just a flat backlog.
- **Roadmap Synthesis Agent**: rolls up statuses + priority into a single roadmap view, refreshed as documents move through the pipeline.
- **Stakeholder Update Agent**: drafts status updates tailored to different audiences from current document/pipeline state.
- **Meeting Notes Agent**: turns raw meeting notes into action items and proposed edits to existing docs, rather than starting a new document from scratch.

### 8.5 Handoff Mechanics (Phases 2-4)

From Phase 2 onward, the "one route calls one agent" MVP pattern gives way to agents handing structured output directly to the next agent — via PydanticAI's agent delegation (an agent invoking the next as a tool call) or a thin orchestrator function calling them in sequence. A rejection at any gate (Validation, Architecture Evaluator) stops the chain there instead of continuing on to artifact generation or publishing, which means documents need an explicit **per-stage status** (e.g., `decomposed` → `validated` → `architecture-approved` → `artifacts-generated` → `published`) rather than the MVP's single `status` field, so a PM can see exactly where each feature sits and where it stalled.
