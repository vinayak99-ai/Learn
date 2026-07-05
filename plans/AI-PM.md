# AI Product Manager Portal
## MVP Implementation Plan

### Executive Summary

A deliberately small MVP: a product manager logs in, creates a product, and describes it through a chat-style interface. A **Review Agent** reads the conversation and asks a short, capped round of clarifying questions in the chat (or none, if the input is already solid). The PM replies in the same thread, and a **Synthesis Agent** turns the whole conversation into a finished product document. It's conversational in presentation, but still just one capped round under the hood — no open-ended multi-turn refinement, no feature breakdown, no validation schemas, no downstream artifacts. Those bigger ideas are noted in §8 as later phases, not part of this build. Stack stays React (shadcn + Tailwind) + Python (FastAPI) + JSON files on disk, with the two agents built as PydanticAI `Agent`s.

---

## 1. MVP User Journey

1. **Log in.** A simple screen asking for a name — no password, nothing persisted server-side. Just enough to feel like "logging in"; gates nothing.
2. **Create a product.** PM clicks "New Product," gives it a title, and lands in a chat thread for that product.
3. **Describe it in the chat.** PM types their first message describing the product — problem, users, goals, whatever they have — same as talking to a person.
4. **Review Agent replies in the thread.** It reads the message and decides: is this enough to write a solid product brief, or not? If not, it posts one assistant message in the chat containing a short, capped list of clarifying questions (e.g., up to 3, asked together in one message — not one at a time).
5. **PM replies, once.** The PM types one reply covering the question(s) in the same thread — still a chat, but capped to this single round; there's no follow-up round of questions after that reply.
6. **Synthesis Agent runs automatically after the reply** (or immediately after Review, if it asked nothing). It takes the full conversation and produces the finished product document as a set of sections, and posts a short confirmation message in the thread.
7. **PM sees the result.** The synthesized document is shown alongside the chat thread and can be edited by hand. Done — that's the full MVP loop.

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
  "conversation": [
    { "role": "user", "content": "We want to speed up our checkout flow, it's too slow and we're losing customers at payment.", "timestamp": "2026-07-05T10:00:00Z" },
    { "role": "assistant", "content": "Two quick questions: what's the current average checkout completion time, and which user segment is most affected?", "timestamp": "2026-07-05T10:01:00Z" },
    { "role": "user", "content": "About 45 seconds average, mostly mobile users.", "timestamp": "2026-07-05T10:02:00Z" },
    { "role": "assistant", "content": "Got it — drafted the product brief below.", "timestamp": "2026-07-05T10:02:30Z" }
  ],
  "sections": [
    { "heading": "Overview", "content": "..." },
    { "heading": "Target Users", "content": "..." },
    { "heading": "Success Metrics", "content": "..." }
  ],
  "created_at": "2026-07-05T10:00:00Z",
  "updated_at": "2026-07-05T10:02:30Z"
}
```

`conversation` is the entire chat thread rendered in the UI — it starts with the PM's first message, gets one assistant message for the (possibly empty) clarifying-questions round, one more PM message replying, and a final short assistant confirmation once `sections` are synthesized. If the Review Agent asks nothing, the thread is just two messages: the PM's description and the assistant's confirmation.

---

## 4. Backend (Python / FastAPI)

### Agents (PydanticAI)

| Agent | Module | `output_type` | Runs when |
|---|---|---|---|
| **Review Agent** | `agents/review.py` | `ReviewResult{questions: list[str]}` (empty = no follow-up needed) | Right after the PM's first chat message, on the conversation so far |
| **Synthesis Agent** | `agents/synthesis.py` | `SynthesizedDoc{sections: list[Section]}` where `Section{heading: str, content: str}` | Right after the PM's reply to the questions (or immediately after Review, if it asked nothing) |

No shared orchestrator, no dependency-injected context beyond what's passed directly into the call — with only two agents and one linear path, the FastAPI routes just call them in sequence. Both agents read the full `conversation` array rather than a single flat field, but the MVP still caps the exchange to one clarifying round — the routes never call Review a second time on the same product.

### API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/products` | List all products |
| `GET` | `/products/{id}` | Get full product content, including `conversation` |
| `POST` | `/products` | Create a product (`title` only); starts with `status: "input"` and an empty `conversation` |
| `POST` | `/products/{id}/messages` | Submit the PM's next chat message (`message`); appends it to `conversation`, then: if this is the **first** user message, runs the Review Agent (questions → append as one assistant message, `status: "questions_pending"`; no questions → run Synthesis immediately); if `status` was already `questions_pending`, this is the capped reply — always runs the Synthesis Agent, appends a confirmation message, and sets `status: "synthesized"` |
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
- **New Product Dialog** — shadcn `Dialog`, just a title field. Submitting calls `POST /products` (title only) and navigates straight to the new product's empty chat thread.
- **Product Page** (`/products/{id}`) — a chat thread (shadcn `Card` + scrollable message list rendering `conversation`) always visible, plus:
  - While `status` is `input`/`questions_pending`: a `Textarea` + `Button` at the bottom of the thread to send the next message — first the initial description, then (if the Review Agent asked something) the one capped reply. Every send posts to the same `POST /products/{id}/messages`.
  - Once `status` is `synthesized`: the chat thread stays visible above, and the finished `sections` render below it as editable `Card`/`Textarea` blocks, with a "Save" button calling `PUT /products/{id}`.

### Component Structure
```
frontend/
  src/
    pages/
      Login.tsx
      ProductList.tsx
      ProductPage.tsx        # chat thread + (once synthesized) the section editor below it
    components/
      NewProductDialog.tsx
      ChatThread.tsx          # renders `conversation`, plus the message input while not yet synthesized
      SectionEditor.tsx
    lib/
      api.ts               # thin fetch wrapper for backend endpoints
```

Note: creating a product now takes just a `title` up front (via `NewProductDialog`); the PM's actual product description is typed as the *first chat message* on the resulting Product Page, not in the creation dialog itself — this keeps the whole intake, from first message onward, inside one consistent chat thread rather than splitting it across a form and a chat.

---

## 6. Implementation Steps

| Step | Task |
|---|---|
| 1 | Scaffold backend: FastAPI app, `storage.py`, `data/` with empty `index.json` |
| 2 | Build the Review Agent and Synthesis Agent (PydanticAI) |
| 3 | Implement `POST /products` (create, empty conversation) and `POST /products/{id}/messages` (first message → Review, and Synthesis if no questions; capped reply → Synthesis) |
| 4 | Implement `GET /products`, `GET /products/{id}`, `PUT /products/{id}` |
| 5 | Scaffold frontend: Vite + React + Tailwind + shadcn, `api.ts` client |
| 6 | Build Login screen (local-storage-only) and Product List |
| 7 | Build New Product Dialog, the ChatThread component, and the synthesized Section Editor view |

---

## 7. Open Questions

- Cap on the number of clarifying questions the Review Agent can ask (plan assumes ~3, asked together in one chat message) — worth confirming.
- What happens if the PM's reply doesn't clearly address every question asked — does Synthesis just work with whatever's in the conversation, or is there a re-prompt (MVP assumption: it just proceeds; true multi-turn follow-up is deferred, see §8)?
- Whether "Login" needs to gate anything at all for a single local user, or is purely cosmetic for now.
- Whether the chat input should stay visible/disabled once `status` is `synthesized` (in case the PM wants to add more context later) or disappear entirely in favor of the Section Editor's manual edits.

---

## 8. Beyond the MVP: Full Agent Catalog & Phase Roadmap

Everything from earlier planning, plus the natural remaining agents from the original "AI PM" vision, laid out as a complete catalog with a phase assigned to each. The MVP (Phase 1) is the only phase actually being built now; everything else is roadmap, sequenced so each phase's agents depend only on documents/data that already exist by the end of the previous phase.

### 8.0 Full Agent Catalog

| # | Agent | Phase | Role |
|---|---|---|---|
| 1 | **Review Agent** | 1 (MVP) | Reads the chat conversation, decides if it's enough, returns a capped list of clarifying questions (or none) |
| 2 | **Synthesis Agent** | 1 (MVP) | Turns the full chat conversation into the finished product document (`sections`) |
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
