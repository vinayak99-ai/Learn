# AI Product Manager Portal
## Implementation Plan — MVP 1 of 3

### Executive Summary

A deliberately small first build, staged as three milestones instead of one big release: **MVP 1** (this build) is a product manager logging in, creating a product, and describing it through a chat-style interface. An **Analysis Agent** works from a standard product checklist to figure out what's missing, and asks up to 3 clarifying questions per round — often with clickable suggested options, not just free text — looping for further rounds until the checklist is covered or a 30-question cap is reached, whichever comes first. The PM replies each round in the same thread, and once the loop ends, a **Documentation Agent** turns the whole conversation into a finished product document. It's a real back-and-forth, not a single capped exchange — but there's still no feature breakdown, no schema-enforced validation gate, no downstream artifacts; those bigger ideas are staged into **MVP 2** and **MVP 3**, detailed in §8 as a broader framework of 8 function-based agents (plus a 9th held for later adoption beyond all three). Stack stays React (shadcn + Tailwind) + Python (FastAPI) + JSON files on disk, with each agent built as a PydanticAI `Agent`.

### The Three-MVP Roadmap, at a Glance

| Milestone | Adds | Agent count |
|---|---|---|
| **MVP 1** (this build) | Analysis, Documentation | 2 |
| **MVP 2** | Structuring, Architecture Decision (+ Documentation gains validation/refinement) | 4 |
| **MVP 3** | Persona, Planning & Delivery, Prioritization, Communication (+ Analysis gains meeting-notes intake) | 8 (all core agents) |
| *Beyond MVP 3* | Domain Knowledge Agent (9th, optional, later adoption) | — |

---

## 1. MVP 1 User Journey

1. **Log in.** A simple screen asking for a name — no password, nothing persisted server-side. Just enough to feel like "logging in"; gates nothing.
2. **Create a product.** PM clicks "New Product," gives it a title, and lands in a chat thread for that product.
3. **Describe it in the chat.** PM types their first message describing the product — problem, users, goals, whatever they have — same as talking to a person.
4. **Analysis Agent replies in the thread, checking against the standard product checklist** (§4, "Standard Product Checklist"). It figures out which checklist items are still unclear and posts up to 3 questions for this round — several of them with clickable suggested options (e.g., likely user segments) alongside the option to just type a free-text answer.
5. **PM replies to that round.** Either by clicking suggested options, typing free text, or a mix — one reply per round.
6. **The loop continues.** If checklist items are still open and the question cap hasn't been hit, Analysis Agent asks up to 3 more in the next round. This repeats until either the checklist is sufficiently covered, or a hard cap of 30 total questions is reached — whichever happens first.
7. **Documentation Agent runs automatically once the loop ends** (checklist covered, or nothing was needed in the first place). It takes the full conversation and produces the finished product document as a set of sections, and posts a short confirmation message in the thread.
8. **PM sees the result.** The synthesized document is shown alongside the chat thread and can be edited by hand. Done — that's the full MVP 1 loop.

---

## 2. Tech Stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite, shadcn/ui, Tailwind CSS |
| Backend | Python (FastAPI) |
| Storage | JSON files on disk (one file per product + an index file) |
| Agents | PydanticAI — MVP 1 uses two of the framework's 8 broad agents (Analysis, Documentation), each with a Pydantic `output_type` (Claude as the default model) |

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
  "status": "questions_pending",
  "conversation": [
    { "role": "user", "content": "We want to speed up our checkout flow, it's too slow and we're losing customers at payment.", "timestamp": "2026-07-05T10:00:00Z" },
    { "role": "assistant", "content": "1. What's the current average checkout completion time?\n2. Which user segment is most affected?\n3. Is there a target timeline for this?", "timestamp": "2026-07-05T10:01:00Z" },
    { "role": "user", "content": "About 45 seconds average. Mostly mobile users. No hard deadline yet.", "timestamp": "2026-07-05T10:02:00Z" }
  ],
  "checklist_covered": ["problem", "current_pain_points"],
  "questions_asked": 3,
  "pending_questions": [
    {
      "checklist_item": "target_users",
      "text": "Which user segment is most affected?",
      "options": ["Mobile users", "Desktop users", "Enterprise customers"]
    },
    {
      "checklist_item": "success_metrics",
      "text": "How will we know this worked?",
      "options": ["Faster average completion time", "Higher conversion rate", "Fewer support tickets"]
    },
    {
      "checklist_item": "constraints",
      "text": "Is there a target timeline for this?",
      "options": []
    }
  ],
  "sections": [],
  "created_at": "2026-07-05T10:00:00Z",
  "updated_at": "2026-07-05T10:02:00Z"
}
```

`conversation` is the entire chat thread rendered in the UI — the PM's first message, one assistant message per question round (rendered as plain numbered text for the transcript/history), and the PM's reply to each round, repeating until the loop ends, followed by a final short assistant confirmation once `sections` are synthesized. If the Analysis Agent asks nothing at all, the thread is just two messages: the PM's description and the assistant's confirmation.

`checklist_covered` and `questions_asked` are backend-maintained bookkeeping (§4) that drive when the loop ends — not something the LLM is trusted to count on its own across calls. `pending_questions` holds the *current* round's questions in structured form (with optional `options` for clickable suggestions) so the frontend can render interactive chips; it's cleared once the PM replies to that round, and is empty once the product reaches `synthesized`.

---

## 4. Backend (Python / FastAPI)

### Agents (PydanticAI)

| Agent | Module | `output_type` | Runs when |
|---|---|---|---|
| **Analysis Agent** (intake sub-capability) | `agents/analysis.py` | `AnalysisResult{questions: list[Question], done: bool}` where `Question{checklist_item: str, text: str, options: list[str]}` | On the PM's first chat message, and again after each subsequent reply — until `done` or the 30-question cap is hit |
| **Documentation Agent** (synthesis sub-capability) | `agents/documentation.py` | `DocumentationDraft{sections: list[Section]}` where `Section{heading: str, content: str}` | Once the Analysis loop ends — `done: true`, or the cap is reached |

These are the MVP 1-relevant slices of two of the framework's 8 broad agents (§8) — Analysis and Documentation each gain more sub-capabilities in MVP 2 and MVP 3, but MVP 1 only needs intake and synthesis. No shared orchestrator, no dependency-injected context beyond what's passed directly into the call — the FastAPI routes just call an agent and persist the result. Both agents read the full `conversation` array rather than a single flat field. Analysis is **not** capped to one call per product: it may run multiple times, once per round, each time checking `checklist_covered` and `questions_asked` (§3) to decide whether to keep going.

### Standard Product Checklist

The Analysis Agent doesn't decide from scratch what's worth asking about — it works from a fixed, ordered checklist that defines what a complete product intake covers. Stored as plain JSON, editable without touching code:

```json
// checklists/product_checklist.json
[
  { "item": "problem",              "label": "Problem / Opportunity",        "required": true  },
  { "item": "target_users",         "label": "Target Users",                 "required": true  },
  { "item": "current_pain_points",  "label": "Current Pain Points",          "required": true  },
  { "item": "success_metrics",      "label": "Success Metrics",              "required": true  },
  { "item": "constraints",          "label": "Constraints / Timeline",       "required": false },
  { "item": "stakeholders",         "label": "Stakeholders",                 "required": false },
  { "item": "existing_alternatives","label": "Existing/Competitive Options", "required": false }
]
```

Each round, the Analysis Agent is given this checklist plus `checklist_covered` (items already answered) and asks up to 3 questions targeting the highest-priority uncovered items — `required` items first. It marks an item covered in its response once the conversation clearly addresses it; the backend merges that into `checklist_covered` on the product. The loop ends (`done: true`) once every `required` item is covered, even if some `required: false` items are still open — those are nice-to-have, not blocking.

This checklist isn't arbitrary: it's designed to line up with the product document's own `sections` (§8.2's Documentation Agent, and the formal schema `required_sections` that arrives with MVP 2's validation sub-capability) — what Analysis gathers is what Documentation drafts into sections, and later what Validation checks for completeness. Same vocabulary throughout, not three different lists that can drift out of sync.

**The 30-question cap is enforced by the backend, not the LLM.** Before calling the Analysis Agent, the route checks `questions_asked >= 30`; if so, it skips straight to Documentation regardless of what's still uncovered. This is deliberate — an LLM re-reading a growing transcript each round is a reasonable way to decide *what* to ask next, but counting *how many* questions it has asked across calls it doesn't retain memory of (§4, "Conversation State vs. Agent Message History") is not something to trust it to self-police.

### Conversation State vs. Agent Message History

PydanticAI tracks conversation as a list of typed `ModelMessage` objects (accumulated via `result.new_messages()` / `result.all_messages()`, and passed back in on the next call as `message_history=`) — not the simple role/content records our app stores. For a stateless FastAPI process, that `message_history` has to be serialized between requests too, via `ModelMessagesTypeAdapter.dump_python(...)` / `.validate_python(...)`.

MVP 1 deliberately doesn't use this, even though Analysis now runs across multiple rounds (up to 10, at 3 questions each, per the 30-question cap): every round is still a fresh `.run()` call built from the app's `conversation` array as plain text context, plus `checklist_covered` so it knows what not to re-ask — not a chain of `message_history`-linked calls. The backend, not the agent's own memory, tracks how many rounds have happened and what's covered (§4, "Standard Product Checklist"), so there's nothing that actually requires the agent to remember its own prior turns via `message_history` — re-deriving from the transcript each time is simpler and just as correct. `message_history` would only earn its place if a future capability needed the agent to reference its own exact prior reasoning, not just the plain facts already sitting in `conversation`.

This also sets a boundary worth keeping deliberately, not just for MVP 1: the app's `conversation` array is the shared, PM-facing log that can cross agent boundaries (both Analysis and Documentation read it), while each agent's own internal `message_history` — if and when one is used — should stay scoped to that one agent. Analysis and Documentation have different system prompts and output types; feeding one agent's raw message history into another would hand it a "conversation" framed by an agent it isn't, rather than the plain facts the PM actually said.

### API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/products` | List all products |
| `GET` | `/products/{id}` | Get full product content, including `conversation` and `pending_questions` |
| `POST` | `/products` | Create a product (`title` only); starts with `status: "input"`, empty `conversation`, `checklist_covered: []`, `questions_asked: 0` |
| `POST` | `/products/{id}/messages` | Submit the PM's message (`message`) — the first description, or a reply to the current round; appends it to `conversation`. If `questions_asked >= 30`, skips straight to Documentation without calling Analysis again. Otherwise runs the Analysis Agent with `conversation` + the checklist + `checklist_covered`: if it returns `done: true` (empty/no more questions needed), runs the Documentation Agent, appends a confirmation, sets `status: "synthesized"`, and clears `pending_questions`; if `done: false`, merges any newly-covered items into `checklist_covered`, adds the new questions' count to `questions_asked`, stores the round in `pending_questions`, appends it to `conversation` as plain numbered text, and keeps `status: "questions_pending"` |
| `PUT` | `/products/{id}` | Manual edits to `title`/`sections` after synthesis |

### File Layout
```
backend/
  main.py            # FastAPI app, route definitions
  storage.py          # read/write helpers for index.json and products/*.json
  agents/
    analysis.py         # Analysis Agent (intake sub-capability) + AnalysisResult/Question models
    documentation.py     # Documentation Agent (synthesis sub-capability) + DocumentationDraft/Section models
  models.py            # Pydantic schemas for request/response validation (API layer)
checklists/
  product_checklist.json   # standard checklist the Analysis Agent works from
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
  - While `status` is `input`: a plain `Textarea` + `Button` for the PM's first message (no `pending_questions` yet).
  - While `status` is `questions_pending`: `pending_questions` renders as one question card per item (up to 3), each showing its `text` and, if `options` is non-empty, a row of clickable shadcn `Badge`/`Button` chips — clicking one fills that question's answer, free text always still available. A single "Send" composes the answers into one reply and posts to `POST /products/{id}/messages`; the response either brings the next round's `pending_questions` or (once `done`) flips to `synthesized`.
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
      ChatThread.tsx          # renders `conversation`, plus QuestionRound while not yet synthesized
      QuestionRound.tsx        # renders `pending_questions` as cards with optional clickable option chips
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
| 2 | Author `checklists/product_checklist.json` |
| 3 | Build the Analysis Agent (PydanticAI) — checklist-aware, `Question`/`AnalysisResult` models, up to 3 questions with optional options per call |
| 4 | Build the Documentation Agent (PydanticAI) — the MVP 1-relevant synthesis sub-capability |
| 5 | Implement `POST /products` (create, empty conversation/checklist state) and `POST /products/{id}/messages` (the round-by-round loop: Analysis until `done` or the 30-question cap, then Documentation) |
| 6 | Implement `GET /products`, `GET /products/{id}`, `PUT /products/{id}` |
| 7 | Scaffold frontend: Vite + React + Tailwind + shadcn, `api.ts` client |
| 8 | Build Login screen (local-storage-only) and Product List |
| 9 | Build New Product Dialog, the ChatThread + QuestionRound components (with clickable option chips), and the synthesized Section Editor view |

---

## 7. Open Questions

- Whether 30 is a hard stop regardless of how many `required` checklist items remain uncovered (plan assumes yes — Documentation just works with whatever's in the conversation past that point), or whether an unresolved `required` item at the cap should surface differently to the PM than a normal completion.
- What happens if a PM's reply ignores the suggested options and free-types something that doesn't clearly answer the question — same assumption as above, Analysis just re-evaluates the whole conversation next round rather than re-prompting the same question.
- Whether the checklist should ever vary by product (e.g., a lighter checklist for a small feature-sized product vs. a fuller one for a major initiative), or stay one fixed list for all of MVP 1.
- Whether "Login" needs to gate anything at all for a single local user, or is purely cosmetic for now.
- Whether the chat input should stay visible/disabled once `status` is `synthesized` (in case the PM wants to add more context later) or disappear entirely in favor of the Section Editor's manual edits.

---

## 8. Beyond MVP 1: The Broad Agent Framework

Rather than a growing list of implementation-level agents, everything beyond MVP 1 is organized around **8 broad, function-based agents** — named for the PM job each one stands in for, not the technical step it happens to perform — plus a **9th, the Domain Knowledge Agent, called out separately as later adoption beyond all three MVPs** rather than part of the initial 8. Each broad agent can carry more than one sub-capability, and those sub-capabilities land in different MVP milestones as the roadmap builds out; MVP 1 only needs the first sub-capability of two of these eight. The three milestones:

- **MVP 1** (2 agents, this build): Analysis (intake only), Documentation (synthesis only).
- **MVP 2** (+2 agents, 4 total): Structuring, Architecture Decision — the next complete capability unit, taking a validated product to a feasibility-checked feature breakdown. Documentation also gains its validation sub-capability here, since Structuring's input requires "a validated product," plus refinement as a natural companion.
- **MVP 3** (+4 agents, 8 total — every core agent except the 9th): Persona, Planning & Delivery, Prioritization, Communication. Analysis also gains its meeting-notes sub-capability here.

### 8.0 The 8 Broad Agents at a Glance

| # | Agent | Introduced | Purpose |
|---|---|---|---|
| 1 | **Analysis Agent** | MVP 1 | Reads raw input — chat messages, later meeting notes — and figures out what's known, what's missing, and what to ask |
| 2 | **Documentation Agent** | MVP 1 | Drafts, refines, and validates the actual product/feature documents |
| 3 | **Persona Agent** | MVP 3 | Owns who the users are as a standalone, reusable definition, rather than re-derived inside every document |
| 4 | **Structuring Agent** | MVP 2 | Breaks a validated product into features, and features into sub-features |
| 5 | **Architecture Decision Agent** | MVP 2 | Judges technical feasibility, dependencies, and design risk before a feature is buildable |
| 6 | **Planning & Delivery Agent** | MVP 3 | Turns an approved feature into an implementation plan, generates the artifacts engineering needs, and publishes everything to Jira/Confluence |
| 7 | **Prioritization Agent** | MVP 3 | Scores and ranks the backlog |
| 8 | **Communication Agent** | MVP 3 | Rolls state up into a roadmap and drafts stakeholder-specific updates |

**9th, for later adoption — not part of MVP 1, 2, or 3:**

| # | Agent | Introduced | Purpose |
|---|---|---|---|
| 9 | **Domain Knowledge Agent** | Beyond MVP 3 (optional) | Grounds other agents in org-specific knowledge an LLM can't know from training — past decisions, internal terminology, existing systems — instead of only general domain knowledge. Not part of the sequential pipeline; a retrieval service other agents call into. Deferred because it requires a real knowledge store (embeddings/vector search) that nothing else here needs — adopt once that infrastructure is worth building, not by default. Could in principle be connected as early as MVP 2, once Structuring and Architecture Decision exist to consult it, but isn't counted toward any of the three MVP milestones. |

### 8.1 Analysis Agent

**Function:** Reads whatever raw input the PM gives it, checks it against the standard product checklist (§4), and decides what's still missing before anything gets drafted — asking up to 3 questions per round, often with clickable suggested options, across as many rounds as needed up to a 30-question cap. This is the system's "listener" — it doesn't write documentation itself, it decides whether there's enough to write from.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Intake review *(MVP 1 name: Review Agent)* | MVP 1 | Chat `conversation` so far + the product checklist + `checklist_covered` | `AnalysisResult{questions: list[Question], done: bool}` (up to 3 `Question`s per call, each with optional `options`; `done: true` = proceed to documentation) | PM's first chat message, and again after each subsequent reply, until `done` or the 30-question cap |
| Meeting-notes intake *(formerly Meeting Notes Agent)* | MVP 3 | Pasted transcript/notes + the relevant product/feature docs | Proposed action items + suggested section edits (not auto-applied) | PM pastes notes and picks the related doc(s) |

### 8.2 Documentation Agent

**Function:** Owns the actual written artifact — drafts it, rewrites pieces of it on request, and checks it's complete enough to act on. This is the system's primary "writer."

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Synthesis *(MVP 1 name: Synthesis Agent)* | MVP 1 | Full chat `conversation` | `DocumentationDraft{sections: list[Section]}` | PM's reply to Analysis's questions (or immediately, if none were asked) |
| Refinement *(formerly Refinement Agent)* | MVP 2 | A prompt (e.g., "expand Success Metrics") + current `sections` | Updated `sections`, merged back into the document | PM submits a refinement prompt on an already-drafted document |
| Validation *(formerly Validation Agent)* | MVP 2 | Document `sections` + its type's `required_sections` schema | `ValidationResult{valid: bool, checks: list[SectionCheck]}` | PM clicks "Review" on a drafted document |

Validation is a gate, not just a writing task, but it's grouped here because it's the Documentation Agent checking its own output against the schema it was drafting to — the same agent that writes it is the one that judges whether it's done.

### 8.3 Persona Agent — *new*

**Function:** Owns "who the users are" as its own artifact, referenced by the Documentation Agent rather than re-described from scratch inside every product/feature doc.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Persona definition & reuse | MVP 3 | Conversation/document context mentioning users, or a direct PM prompt | A structured persona (needs, context, pain points) linked to the product/feature that referenced it | PM defines a persona, or the Documentation Agent flags an undefined "Target Users" reference |

### 8.4 Structuring Agent

**Function:** Takes one finished product document and breaks it down into a real hierarchy — candidate features, then candidate sub-features underneath each one — for the PM to review and confirm.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Decomposition *(formerly Decomposition Agent)* | MVP 2 | Validated product `sections` (+ conversation for context) | `FeatureProposals{items: list[FeatureProposal]}` — titles + rationale, nothing written to disk yet | PM clicks "Generate Features" on a valid product |

Product → candidate features → (per accepted feature) candidate sub-features, two levels deep. PM confirms/deselects proposals at each level before real documents are created.

### 8.5 Architecture Decision Agent

**Function:** Acts as the technical-feasibility gate between "documented" and "buildable" — gives a feasibility read (risks, dependencies, open technical questions) before a feature moves toward being built.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Feasibility evaluation *(formerly Architecture Evaluator Agent)* | MVP 2 | A validated feature/sub-feature's `sections` | Feasibility verdict + notes (risks, dependencies, open technical questions) | A feature/sub-feature passes the Documentation Agent's validation sub-capability |

A feature that fails this gate goes back to the PM/engineering for rework rather than proceeding. **Optionally grounded by the Domain Knowledge Agent (§8.9)** once that's adopted — this is one of the two consumers of it, since a feasibility call is exactly where "generic best practice" and "what this org's systems can actually support" are most likely to diverge.

### 8.6 Planning & Delivery Agent

**Function:** Everything from "approved" to "in the tools engineering actually executes in" — turns an approved feature into a real implementation plan, generates what engineering needs, and publishes the finished work.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Implementation planning *(formerly Implementation Planning Agent)* | MVP 3 | An architecture-approved feature/sub-feature + the Architecture Decision Agent's notes | A structured implementation plan: ordered steps, dependencies between steps, rough scope per step | A feature/sub-feature passes Architecture Decision |
| Artifact generation *(formerly Artifact Agent)* | MVP 3 | An implementation-planned feature/sub-feature | `ArtifactDraft{sections: list[Section]}` (user stories, test plans, acceptance criteria) | PM requests an artifact type for a planned feature |
| Publishing *(formerly Jira/Confluence Agent)* | MVP 3 | A feature's implementation plan + its artifacts | Jira epic (product) / stories (one per plan step) + Confluence pages; IDs written back to local JSON | PM clicks "Publish" on a planned, artifact-complete feature |

This is the system's first external dependency — real auth credentials, network calls, and error handling that every earlier agent deliberately avoids.

### 8.7 Prioritization Agent

**Function:** Looks across the backlog and proposes an order — what to build first — using whatever signal is available.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Backlog scoring *(unchanged from Prioritization Agent)* | MVP 3 | All features/sub-features + whatever signal exists (architecture risk, plan scope, PM input) | Ranked list with rationale per item | On demand, or after a batch of features clears the pipeline |

Already a function-named agent in the original catalog — kept as-is.

### 8.8 Communication Agent

**Function:** Everything about telling people what's going on, as opposed to moving the work itself forward — rolls status up into a roadmap view, and drafts updates tailored to whoever's asking.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Roadmap synthesis *(formerly Roadmap Synthesis Agent)* | MVP 3 | Product/feature statuses + priority scores | A roadmap view (grouped/sequenced summary) | On demand, or scheduled refresh |
| Stakeholder updates *(formerly Stakeholder Update Agent)* | MVP 3 | Current document/pipeline state + target audience | Drafted update text (eng standup / exec summary / customer changelog) | PM requests an update for a given audience |

This — together with Analysis's meeting-notes sub-capability and Prioritization — is where the very first version of this plan's "autonomous AI PM" vision (intake triage, backlog grooming, stakeholder updates) actually lands, now with real structured documents to operate on.

### 8.9 Domain Knowledge Agent — *for later adoption, not one of the 8*

**Function:** Grounds other agents in knowledge specific to the organization — past decisions, internal systems, internal terminology — that an LLM has no way of knowing on its own. Deliberately kept outside the core 8: it's a cross-cutting retrieval service, not a PM function with its own outputs.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Domain grounding | Beyond MVP 3 (optional) | A query from another agent (e.g., "has checkout latency been addressed before?") + the internal knowledge base | Relevant excerpts/citations from past docs, decisions, or architecture notes | Called mid-task by the Structuring or Architecture Decision Agent (not a standalone pipeline step) |

Consulted by the Structuring Agent (to avoid proposing a feature that was already tried and rejected) and the Architecture Decision Agent (to check a proposal against the org's *actual* existing systems, not just generic best practice). Requires a real knowledge store — embeddings/vector search over internal docs, architecture notes, past decisions — a genuine step up in infrastructure from every other agent here, which only ever reads the current document plus the LLM's own knowledge. That store also needs a source and a way to stay current, or it becomes a source of false confidence rather than grounding. Adopt when that infrastructure is worth building, not by default.

### 8.10 MVP Roadmap at a Glance

| Milestone | Agents active (sub-capability) |
|---|---|
| MVP 1 (this build) | Analysis (intake), Documentation (synthesis) |
| MVP 2 | Documentation (refinement, validation), Structuring, Architecture Decision, *[optionally: Domain Knowledge]* |
| MVP 3 | Persona, Planning & Delivery (planning, artifacts, publishing), Prioritization, Communication (roadmap, stakeholder updates), Analysis (meeting notes) |
| *Beyond MVP 3* | Domain Knowledge *(if not already adopted during MVP 2)* |

### 8.11 Handoff Mechanics (MVP 2 & MVP 3)

From MVP 2 onward, the "one route calls one agent" MVP 1 pattern gives way to agents handing structured output directly to the next agent — via PydanticAI's agent delegation (an agent invoking the next as a tool call) or a thin orchestrator function calling them in sequence. A rejection at any gate (Documentation's validation sub-capability, Architecture Decision) stops the chain there instead of continuing on to planning, artifact generation, or publishing, which means documents need an explicit **per-stage status** (e.g., `decomposed` → `validated` → `architecture-approved` → `implementation-planned` → `artifacts-generated` → `published`) rather than MVP 1's single `status` field, so a PM can see exactly where each feature sits and where it stalled.

The **Domain Knowledge Agent**, if and when adopted, is the one exception to this handoff chain: it doesn't sit at a stage or produce a status transition of its own. The Structuring and Architecture Decision Agents would call it as a tool mid-execution, the way any agent might call a function, and its answer just informs the output those two agents were already going to produce.

### 8.12 Do We Need an Orchestrating Agent?

No — normalizing one agent's JSON output into the next agent's expected input is a deterministic mapping problem, not a judgment call, so it doesn't need an LLM. Each handoff is: take a Pydantic model (e.g., `FeatureProposals` from Structuring) and produce the input another agent's `run()` call expects (e.g., a feature's `sections` for Architecture Decision) — a plain typed Python function does this correctly every time, with no latency, cost, or non-determinism added. Reaching for an agent here would mean paying an LLM call to do something a function already does exactly right.

What actually does the "orchestrating" is two things, both already in this plan and both plain code:
- The **per-stage status field** (§8.11) — the state machine that decides what happens next, based on what a document's status already is.
- Small **typed adapter functions** (living in `storage.py` or a new `agents/adapters.py`) that translate one agent's stored output into the next agent's input shape.

So the "thin orchestrator function" already mentioned in §8.11 is exactly right as stated — a function, not an agent. The one caveat: if a future milestone needs a *judgment call* about sequencing (not just "is this document valid, yes/no" but something genuinely ambiguous), that's a case for extending an existing agent's job, not introducing a new orchestrating agent whose only role is data plumbing.
