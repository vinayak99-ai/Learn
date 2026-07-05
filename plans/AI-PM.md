# AI Product Manager Portal
## Implementation Plan

### Executive Summary

A simple, local-first "AI PM" portal for drafting and managing product documentation. A product manager opens the app straight to a Product List (no login), creates a Product, and has a short back-and-forth conversation with an LLM to capture high-level details. The LLM then proposes a breakdown of that product into candidate features; each feature gets its own conversational intake, and both products and features end up as structured, schema-validated documents. From there, the LLM can generate further downstream artifacts (user stories, test plans, etc.). A React (shadcn + Tailwind) UI drives all of this against a Python backend that stores everything as JSON files on disk — no database, no external services.

---

## 1. User Journey

This is the concrete, end-to-end story the rest of this plan implements:

1. **Open the app.** No login — it opens directly to the Product List (single local user).
2. **Create a Product.** PM clicks "New Product," gives it a name, and lands on the new product's page in **intake** mode.
3. **Describe it at a high level.** PM types a free-form description of the product idea into a chat-style intake panel (e.g., "We want to speed up our checkout flow, it currently takes too long and we're losing customers at payment").
4. **LLM asks follow-up questions.** The LLM reads what's been said so far and asks a clarifying question (e.g., "Who are the primary users affected, and do you have a current baseline checkout time?"). This repeats turn by turn — a real conversation, not a fixed form.
5. **LLM drafts the product overview.** Once the LLM decides it has enough information, it stops asking questions and instead drafts the product's structured sections (Overview, Target Users, Success Metrics, etc.), and the product moves from **intake** to **draft**.
6. **PM reviews/edits, then validates.** PM can edit the drafted sections directly, then clicks "Review" to validate the product doc against its schema (§7). Any missing/weak sections are flagged and must be fixed before continuing.
7. **LLM splits the product into candidate features.** Once the product overview is valid, PM clicks "Generate Features." The LLM proposes a list of candidate features (name + one-line rationale) based on the product conversation and overview.
8. **PM confirms which features to create.** PM reviews the proposed list (checkboxes, all selected by default), deselects any it doesn't want, and confirms. A real feature document is created for each selected item, linked back to the product, each starting in its own **intake** state.
9. **Per-feature conversation.** For each feature, the PM goes through the same conversational intake as step 3-5, but scoped to that feature (the LLM already has the parent product's context, so it asks feature-specific follow-ups, e.g., "What's the proposed UX change for one-click checkout?").
10. **Feature drafted, validated, and extended.** Each feature reaches **draft**, gets validated the same way as the product (§7), and once valid the PM can generate downstream artifacts for it — user stories, a test plan, etc. (§8).
11. **Back on the Product page**, the PM sees the full breakdown: product overview + a list of its features, each showing status (intake / draft / in_review / approved) and its own generated artifacts.

---

## 2. Goals & Scope

### Goals
- Create a Product and capture its high-level details through an LLM-led conversation, not a blank form.
- Let the LLM split a validated product into candidate features, and turn confirmed candidates into their own documents with their own conversational intake.
- Validate every document (product or feature) against a required-fields schema (stored as JSON), with an LLM review pass, and block progress until issues are resolved.
- Once a document validates, use an LLM to generate further downstream artifacts appropriate to its type.
- Store all product data as JSON on the local filesystem — no database.

### Non-Goals (for this simple version)
- Login/auth of any kind — single local user, opens straight to the Product List.
- Multi-user permissions or hosted deployment.
- Real-time collaboration.
- Integrations with external trackers (Jira, GitHub Issues, etc.) — future enhancement.

---

## 3. Tech Stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite, shadcn/ui, Tailwind CSS |
| Backend | Python (FastAPI) |
| Storage | JSON files on disk (one file per document + an index file) |
| Agent Framework | [PydanticAI](https://ai.pydantic.dev/) — one typed `Agent` per responsibility, each with a Pydantic `output_type` (Claude as the default model) |

---

## 4. Data Model

All product data lives under a single `data/` directory as JSON files. No database. A "document" is either a `product` (top-level) or a `feature` (child of a product, via `product_id`).

```
data/
  index.json                  # list of all documents (id, title, type, status, product_id, timestamps)
  documents/
    <doc_id>.json               # full content of one document (product or feature)
  schemas/
    product.schema.json          # required sections for type "product"
    feature.schema.json          # required sections for type "feature"
  artifact_types.json           # artifact_type -> prompt template + target schema mapping
```

**`index.json`**
```json
{
  "documents": [
    {
      "id": "prod_001",
      "title": "Checkout Redesign",
      "type": "product",         // "product" | "feature"
      "status": "draft",         // "intake" | "draft" | "in_review" | "approved"
      "product_id": null,        // set on feature docs, points at the parent product
      "created_at": "2026-07-05T10:00:00Z",
      "updated_at": "2026-07-05T10:00:00Z"
    }
  ]
}
```

**`documents/<doc_id>.json`**
```json
{
  "id": "prod_001",
  "title": "Checkout Redesign",
  "type": "product",
  "status": "draft",
  "product_id": null,
  "feature_ids": ["doc_010", "doc_011"],
  "conversation": [
    { "role": "user", "content": "We want to speed up checkout, it's too slow today.", "timestamp": "..." },
    { "role": "assistant", "content": "What's the current average checkout time, and who's most affected?", "timestamp": "..." },
    { "role": "user", "content": "About 45 seconds average, mostly mobile users.", "timestamp": "..." }
  ],
  "sections": [
    { "heading": "Overview", "content": "..." },
    { "heading": "Target Users", "content": "..." },
    { "heading": "Success Metrics", "content": "..." }
  ],
  "validation": {
    "valid": true,
    "checked_at": "2026-07-05T10:20:00Z",
    "missing_fields": [],
    "issues": []
  },
  "source_document_id": null,
  "artifact_type": null,
  "linked_artifacts": [],
  "created_at": "2026-07-05T10:00:00Z",
  "updated_at": "2026-07-05T10:20:00Z"
}
```

A `feature` document has the same shape, but `type: "feature"`, `product_id` set to its parent's `id`, and no `feature_ids` (features don't have children).

**`schemas/feature.schema.json`** (required-fields schema, plain JSON)
```json
{
  "type": "object",
  "required_sections": ["Problem", "Proposed Solution", "Success Metrics"],
  "properties": {
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "heading": { "type": "string" },
          "content": { "type": "string", "minLength": 1 }
        },
        "required": ["heading", "content"]
      }
    }
  }
}
```
`schemas/product.schema.json` follows the same shape with its own `required_sections` (e.g., `["Overview", "Target Users", "Success Metrics"]`).

---

## 5. Backend (Python / FastAPI)

### Responsibilities
- Read/write JSON files under `data/` (no ORM, no DB driver).
- Expose a small REST API for the frontend.
- Drive the conversational intake, feature breakdown, validation, and artifact generation by delegating to the PydanticAI agents below — routes stay thin and just call an agent, then persist its structured output.

### Agents (PydanticAI)

Each LLM-driven responsibility is its own `Agent` with a Pydantic `output_type`, so the backend never hand-parses free-text LLM output. All agents share one `PMContext` dependency (the current document, its parent product if any, and its schema) via PydanticAI's dependency injection.

| Agent | Module | `output_type` | Used by |
|---|---|---|---|
| **Intake Agent** | `agents/intake.py` | `IntakeResult = NextQuestion \| DraftedSections` — a discriminated union; `NextQuestion{question: str}` or `DraftedSections{sections: list[Section]}` | `/documents/{id}/messages` (§7) |
| **Validation Agent** | `agents/validation.py` | `ValidationResult{valid: bool, checks: list[SectionCheck]}` where `SectionCheck{field: str, ok: bool, message: str}` | `/documents/{id}/validate` (§9) |
| **Breakdown Agent** | `agents/breakdown.py` | `FeatureProposals{items: list[FeatureProposal]}` where `FeatureProposal{title: str, rationale: str}` | `/documents/{id}/features/propose` (§8) |
| **Artifact Agent** | `agents/artifact.py` | `ArtifactDraft{sections: list[Section]}` — same shape as a document's `sections`, templated per `artifact_type` | `/documents/{id}/artifacts` (§10) |

Each agent is a plain, independent `Agent(model, output_type=..., system_prompt=...)` — no shared orchestrator agent for v1; a FastAPI route calls exactly one agent and persists the result. This keeps the mental model simple (routes stay thin, agents stay single-purpose) and leaves room to introduce an orchestrator agent later if flows need to chain agent calls without a round-trip to the frontend in between.

### API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/documents` | List all documents; supports `?type=product` and `?product_id=` filters |
| `GET` | `/documents/{id}` | Get full document content |
| `POST` | `/documents` | Create a new document (`type`, `title`, optional `product_id` for a manually-added feature); starts in `intake` |
| `PUT` | `/documents/{id}` | Update a document's sections/status/title directly |
| `DELETE` | `/documents/{id}` | Delete a document |
| `POST` | `/documents/{id}/messages` | Send the PM's next intake message; returns either the LLM's next question or, once enough is known, drafted `sections` + a status flip to `draft` |
| `POST` | `/documents/{id}/generate` | Ad-hoc prompt to expand/refine sections on an already-drafted document |
| `POST` | `/documents/{id}/validate` | Check sections against the type's schema (structural + LLM review); returns `valid`, `missing_fields`, `issues` |
| `POST` | `/documents/{id}/features/propose` | (Product only, must be valid) LLM proposes candidate features: `[{ title, rationale }]` |
| `POST` | `/documents/{id}/features/confirm` | Create feature documents for the confirmed subset of proposed candidates, each starting in `intake` with a pre-seeded conversation |
| `GET` | `/artifact-types` | List available artifact types for a given document type |
| `POST` | `/documents/{id}/artifacts` | Generate a downstream artifact document from a validated document |

### File Layout
```
backend/
  main.py            # FastAPI app, route definitions
  storage.py          # read/write helpers for index.json and documents/*.json
  agents/
    deps.py            # shared PMContext dependency (document, parent product, schema)
    intake.py           # Intake Agent + IntakeResult/NextQuestion/DraftedSections models
    validation.py        # Validation Agent + ValidationResult/SectionCheck models (wraps the
                         # deterministic structural check + the agent's qualitative pass)
    breakdown.py         # Breakdown Agent + FeatureProposals/FeatureProposal models
    artifact.py           # Artifact Agent + ArtifactDraft model
  models.py            # Pydantic schemas for request/response validation (API layer, not agent output)
data/
  index.json
  documents/
  schemas/
  artifact_types.json
```

---

## 6. Frontend (React + shadcn + Tailwind)

### Pages / Views
- **Product List** (`/`) — the app's home page: table/grid of `type: product` documents only (title, status, feature count, last updated), with a "New Product" button. Feature documents are not shown at this top level.
- **New Product Dialog** — shadcn `Dialog`, just a name field. Submitting calls `POST /documents` (`type: "product"`) and navigates straight to the product's page in `intake` mode.
- **Document Page** (`/documents/{id}`) — used for both products and features; renders one of two states based on `status`:
  - **Intake Chat** (`status === "intake"`): a chat thread (shadcn `Card` + scrollable message list) showing `conversation`, with a `Textarea` + `Button` to send the next message to `POST /documents/{id}/messages`. Each reply either appends an assistant question to the thread, or (when the LLM is done) swaps the view to the Section Editor.
  - **Section Editor** (`status` is `draft`/`in_review`/`approved`): the existing section-by-section editor (shadcn `Card`/`Textarea` per section), plus the Generate Panel, Validation Panel, and Artifacts Panel described below.
- **Generate Panel** — prompt input for ad-hoc refinement of an already-drafted document via `/documents/{id}/generate`.
- **Validation Panel** — "Review" button calling `/documents/{id}/validate`; renders a shadcn `Alert` summarizing missing fields plus inline flags on the relevant section cards.
- **Feature Breakdown Panel** (product pages only) — once the product is valid, a "Generate Features" button calls `/documents/{id}/features/propose` and shows the candidate list as a checklist (shadcn `Checkbox` per item, all checked by default); "Confirm" calls `/documents/{id}/features/confirm`, and the resulting feature documents appear in a "Features" list on the product page, each linking to its own Document Page.
- **Artifacts Panel** — once a document is valid, "Generate Artifacts" lists artifact types (from `/artifact-types`) and creates a linked artifact document via `/documents/{id}/artifacts`.

### Component Structure
```
frontend/
  src/
    pages/
      ProductList.tsx
      DocumentPage.tsx        # renders IntakeChat or SectionEditor based on status
    components/
      NewProductDialog.tsx
      IntakeChat.tsx
      SectionEditor.tsx
      GeneratePanel.tsx
      ValidationPanel.tsx
      FeatureBreakdownPanel.tsx
      FeatureList.tsx          # shown on a product's Document Page
      ArtifactsPanel.tsx
    lib/
      api.ts                  # thin fetch wrapper for backend endpoints
```

### Styling
- Tailwind CSS for layout/utility classes.
- shadcn/ui components (`Button`, `Card`, `Dialog`, `Textarea`, `Checkbox`, `Badge`, `Table`) for consistent UI primitives — no custom design system needed for v1.

---

## 7. Conversational Intake Flow

This is how a document (product or feature) moves from a blank slate to drafted sections, per steps 3-5 and 9 of the User Journey.

1. Document is created with `status: "intake"` and an empty `conversation`. (For a feature created via breakdown confirmation, `conversation` is pre-seeded with an initial assistant message giving the feature's rationale, so the PM's first reply is already in context.)
2. PM sends a message → `POST /documents/{id}/messages` with `{ message }`.
3. Backend appends `{ role: "user", content: message }` to `conversation`, then runs the **Intake Agent** (`agents/intake.py`) with the full conversation, the document's type schema (`required_sections`), and — for a feature — the parent product's drafted sections, all via the shared `PMContext` dependency.
4. Thanks to the agent's `IntakeResult = NextQuestion | DraftedSections` output type, the route gets back one of exactly two shapes — no free-text parsing:
   - **`NextQuestion`**: appended as `{ role: "assistant", content: question }`; status stays `intake`; frontend just renders the new message.
   - **`DraftedSections`**: backend saves `sections` (already validated against the `Section` Pydantic model) to the document, flips `status` to `draft`, and returns the drafted sections.
5. Backend writes the updated document to disk and updates `updated_at` in both the document and `index.json` on every turn.
6. Frontend swaps from Intake Chat to Section Editor the moment `status` comes back as `draft`, showing the drafted sections as pre-filled, editable cards.

---

## 8. Feature Breakdown Flow

Covers steps 7-9 of the User Journey — splitting a validated product into features.

1. PM clicks **"Generate Features"** on a valid (`validation.valid: true`) product page.
2. Frontend calls `POST /documents/{id}/features/propose`. Backend runs the **Breakdown Agent** (`agents/breakdown.py`) with the product's conversation + drafted sections; its `FeatureProposals{items: list[FeatureProposal]}` output type guarantees a clean `[{ title, rationale }]` list back — nothing is written to disk yet.
3. Frontend shows the proposals as a checklist (all checked by default) in the Feature Breakdown Panel.
4. PM deselects any unwanted proposals and clicks **"Confirm."** Frontend calls `POST /documents/{id}/features/confirm` with the confirmed subset.
5. For each confirmed item, the backend creates a new `feature` document: `product_id` set to the parent, `status: "intake"`, and `conversation` pre-seeded with an assistant message stating the feature's rationale (so the PM's first message continues that thread rather than starting cold). Each gets its own entry in `index.json`.
6. The product's `feature_ids` array is updated with the new documents' ids.
7. Frontend adds the new features to the product page's Feature List; each opens into its own Document Page in `intake` mode, ready for the per-feature conversation (§7).

---

## 9. Schema Validation & Forced Completion

Each document `type` has a required-fields schema stored as JSON under `schemas/` (see §4). Validation happens in two passes, both triggered by `/documents/{id}/validate`:

1. **Structural check** (plain Python, no LLM call, run before the agent): confirms every heading in the type's `required_sections` exists in the document's `sections` array and has non-empty `content`. Anything missing/blank goes straight into `missing_fields`.
2. **Validation Agent review pass** (`agents/validation.py`): for structurally-present sections, the agent is given each section's content and asked to judge whether it actually satisfies that field's intent (e.g., "Success Metrics" must contain a measurable target, not just prose). Its `ValidationResult{valid: bool, checks: list[SectionCheck]}` output type guarantees one `SectionCheck{field, ok, message}` per section; `ok: false` entries become `issues`.
3. Backend combines both passes into one result, writes it to the document's `validation` object, and returns it.
4. **Enforcement**: "Generate Features" (product only), "Generate Artifacts," and the "Mark as In Review/Approved" status transition are disabled in the UI while `validation.valid` is `false`, and the backend independently rejects those operations with `422` on an invalid document — so the check can't be bypassed by calling the API directly.
5. PM edits the flagged sections (manually or via the Generate Panel) and re-runs Review until `valid` is `true`.

---

## 10. Artifact Generation Flow

Once a document (typically a feature) passes validation, the PM can generate further downstream artifacts. Available artifact types per document type are defined in `artifact_types.json`, e.g.:

```json
{
  "feature": [
    { "type": "user_stories", "label": "User Stories", "prompt_template": "user_stories.txt" },
    { "type": "test_plan", "label": "Test Plan", "prompt_template": "test_plan.txt" }
  ]
}
```

Flow:
1. PM clicks **"Generate Artifacts"** and picks a type from `GET /artifact-types?type={document.type}`.
2. Frontend calls `POST /documents/{id}/artifacts` with `{ artifact_type }`.
3. Backend re-checks `validation.valid` is `true`, then runs the **Artifact Agent** (`agents/artifact.py`) with the matching prompt template (from `artifact_types.json`) as its system prompt and the source document's full content as context; its `ArtifactDraft{sections: list[Section]}` output type comes back already shaped like a document's `sections`.
4. The response is saved as a new document (`source_document_id` set to the originator, `artifact_type` set), with its own `index.json` entry.
5. The source document's `linked_artifacts` array is updated with the new artifact's id.
6. Frontend shows the new artifact under a "Related Artifacts" list on the source document's page.

---

## 11. Implementation Steps

| Step | Task |
|---|---|
| 1 | Scaffold backend: FastAPI app, `storage.py` read/write helpers, `data/` directory with empty `index.json` |
| 2 | Implement CRUD endpoints for documents (list w/ `type`/`product_id` filters, get, create, update, delete) |
| 3 | Scaffold frontend: Vite + React + Tailwind + shadcn setup, `api.ts` client |
| 4 | Build Product List page (`GET /documents?type=product`) and New Product Dialog |
| 5 | Set up PydanticAI + shared `PMContext` dependency (`agents/deps.py`); build the **Intake Agent** and `/documents/{id}/messages` |
| 6 | Build Intake Chat component; wire Document Page to switch between Intake Chat and Section Editor based on `status` |
| 7 | Build Section Editor + Generate Panel, wired to `GET/PUT /documents/{id}` and `/documents/{id}/generate` |
| 8 | Author `schemas/*.json`; build the **Validation Agent** (plus the plain-Python structural check) and `/documents/{id}/validate`; build Validation Panel with enforcement |
| 9 | Build the **Breakdown Agent** and `/documents/{id}/features/propose` + `/confirm`; build Feature Breakdown Panel and Feature List |
| 10 | Author `artifact_types.json` and prompt templates; build the **Artifact Agent** and `/artifact-types` + `/documents/{id}/artifacts`; build Artifacts Panel |
| 11 | Polish: status badges, delete confirmation, basic empty/error states |

---

## 12. Open Questions

- Which LLM provider/model to default to, and how API keys are supplied locally (env var vs. config file).
- How the LLM decides it "has enough" during intake — a fixed minimum turn count, a confidence signal from the model itself, or letting the PM force it to draft early with a "Draft now" button.
- Whether a PM should be able to manually add a feature to a product outside the breakdown flow (the `POST /documents` endpoint already supports `product_id`, so this is possible — just needs a UI entry point).
- How strict the Validation Agent's review pass should be by default, to avoid blocking users on borderline content.
- Whether artifact documents (user stories, test plans) should be editable/re-validatable like primary documents, or treated as read-only outputs.
- Whether to introduce a single orchestrator agent once flows need to chain multiple agents server-side (e.g., auto-running validation right after intake drafts sections), versus keeping each route call exactly one agent as planned for v1.
