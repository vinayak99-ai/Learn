# AI Product Manager Portal
## Implementation Plan — MVP 1 of 3

### Executive Summary

A deliberately small first build, staged as three milestones instead of one big release: **MVP 1** (this build) is a product manager logging in, creating a product, and describing it through a chat-style interface. An **Analysis Agent** reads the conversation and asks a short, capped round of clarifying questions in the chat (or none, if the input is already solid). The PM replies in the same thread, and a **Documentation Agent** turns the whole conversation into a finished product document. It's conversational in presentation, but still just one capped round under the hood — no open-ended multi-turn refinement, no feature breakdown, no validation schemas, no downstream artifacts. Those bigger ideas are staged into **MVP 2** and **MVP 3**, detailed in §8 as a broader framework of 8 function-based agents (plus a 9th held for later adoption beyond all three). Stack stays React (shadcn + Tailwind) + Python (FastAPI) + JSON files on disk, with each agent built as a PydanticAI `Agent`.

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
4. **Analysis Agent replies in the thread.** It reads the message and decides: is this enough to write a solid product brief, or not? If not, it posts one assistant message in the chat containing a short, capped list of clarifying questions (e.g., up to 3, asked together in one message — not one at a time).
5. **PM replies, once.** The PM types one reply covering the question(s) in the same thread — still a chat, but capped to this single round; there's no follow-up round of questions after that reply.
6. **Documentation Agent runs automatically after the reply** (or immediately after Analysis, if it asked nothing). It takes the full conversation and produces the finished product document as a set of sections, and posts a short confirmation message in the thread.
7. **PM sees the result.** The synthesized document is shown alongside the chat thread and can be edited by hand. Done — that's the full MVP 1 loop.

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

`conversation` is the entire chat thread rendered in the UI — it starts with the PM's first message, gets one assistant message for the (possibly empty) clarifying-questions round, one more PM message replying, and a final short assistant confirmation once `sections` are synthesized. If the Analysis Agent asks nothing, the thread is just two messages: the PM's description and the assistant's confirmation.

---

## 4. Backend (Python / FastAPI)

### Agents (PydanticAI)

| Agent | Module | `output_type` | Runs when |
|---|---|---|---|
| **Analysis Agent** (intake sub-capability) | `agents/analysis.py` | `AnalysisResult{questions: list[str]}` (empty = no follow-up needed) | Right after the PM's first chat message, on the conversation so far |
| **Documentation Agent** (synthesis sub-capability) | `agents/documentation.py` | `DocumentationDraft{sections: list[Section]}` where `Section{heading: str, content: str}` | Right after the PM's reply to the questions (or immediately after Analysis, if it asked nothing) |

These are the MVP 1-relevant slices of two of the framework's 8 broad agents (§8) — Analysis and Documentation each gain more sub-capabilities in MVP 2 and MVP 3, but MVP 1 only needs intake and synthesis. No shared orchestrator, no dependency-injected context beyond what's passed directly into the call — with only two agents and one linear path, the FastAPI routes just call them in sequence. Both agents read the full `conversation` array rather than a single flat field, but MVP 1 still caps the exchange to one clarifying round — the routes never call Analysis a second time on the same product.

### Conversation State vs. Agent Message History

PydanticAI tracks conversation as a list of typed `ModelMessage` objects (accumulated via `result.new_messages()` / `result.all_messages()`, and passed back in on the next call as `message_history=`) — not the simple role/content records our app stores. For a stateless FastAPI process, that `message_history` has to be serialized between requests too, via `ModelMessagesTypeAdapter.dump_python(...)` / `.validate_python(...)`.

MVP 1 deliberately doesn't use this: Analysis runs at most once per product (on the first message) and Documentation runs at most once (on the reply), so there's no multi-turn *within* either agent's own history to continue — each agent gets a single `.run()` call built from the app's `conversation` array as plain text context, not a chain of prior `.run()` calls. `message_history` only earns its place once a single agent needs to remember its own prior structured turns across multiple calls (e.g., a future uncapped, multi-round Analysis Agent — see §8, "Beyond MVP 1").

This also sets a boundary worth keeping deliberately, not just for MVP 1: the app's `conversation` array is the shared, PM-facing log that can cross agent boundaries (both Analysis and Documentation read it), while each agent's own internal `message_history` — if and when one is used — should stay scoped to that one agent. Analysis and Documentation have different system prompts and output types; feeding one agent's raw message history into another would hand it a "conversation" framed by an agent it isn't, rather than the plain facts the PM actually said.

### API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/products` | List all products |
| `GET` | `/products/{id}` | Get full product content, including `conversation` |
| `POST` | `/products` | Create a product (`title` only); starts with `status: "input"` and an empty `conversation` |
| `POST` | `/products/{id}/messages` | Submit the PM's next chat message (`message`); appends it to `conversation`, then: if this is the **first** user message, runs the Analysis Agent (questions → append as one assistant message, `status: "questions_pending"`; no questions → run Documentation immediately); if `status` was already `questions_pending`, this is the capped reply — always runs the Documentation Agent, appends a confirmation message, and sets `status: "synthesized"` |
| `PUT` | `/products/{id}` | Manual edits to `title`/`sections` after synthesis |

### File Layout
```
backend/
  main.py            # FastAPI app, route definitions
  storage.py          # read/write helpers for index.json and products/*.json
  agents/
    analysis.py         # Analysis Agent (intake sub-capability) + AnalysisResult model
    documentation.py     # Documentation Agent (synthesis sub-capability) + DocumentationDraft/Section models
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
  - While `status` is `input`/`questions_pending`: a `Textarea` + `Button` at the bottom of the thread to send the next message — first the initial description, then (if the Analysis Agent asked something) the one capped reply. Every send posts to the same `POST /products/{id}/messages`.
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
| 2 | Build the Analysis Agent and Documentation Agent (PydanticAI) — the MVP 1-relevant sub-capabilities of two of the 8 broad agents |
| 3 | Implement `POST /products` (create, empty conversation) and `POST /products/{id}/messages` (first message → Analysis, and Documentation if no questions; capped reply → Documentation) |
| 4 | Implement `GET /products`, `GET /products/{id}`, `PUT /products/{id}` |
| 5 | Scaffold frontend: Vite + React + Tailwind + shadcn, `api.ts` client |
| 6 | Build Login screen (local-storage-only) and Product List |
| 7 | Build New Product Dialog, the ChatThread component, and the synthesized Section Editor view |

---

## 7. Open Questions

- Cap on the number of clarifying questions the Analysis Agent can ask (plan assumes ~3, asked together in one chat message) — worth confirming.
- What happens if the PM's reply doesn't clearly address every question asked — does the Documentation Agent just work with whatever's in the conversation, or is there a re-prompt (MVP 1 assumption: it just proceeds; true multi-turn follow-up is deferred beyond MVP 3, see §8)?
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

**Function:** Reads whatever raw input the PM gives it and decides what's missing before anything gets drafted. This is the system's "listener" — it doesn't write documentation itself, it decides whether there's enough to write from.

| Sub-capability | MVP | Input | Output | Triggered by |
|---|---|---|---|---|
| Intake review *(MVP 1 name: Review Agent)* | MVP 1 | Chat `conversation` so far | `AnalysisResult{questions: list[str]}` (empty = proceed straight to documentation) | PM's first chat message on a product |
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
