# AI Product Manager Portal
## Implementation Plan

### Executive Summary

A simple, local-first "AI PM" portal for drafting and managing product documentation. A React (shadcn + Tailwind) UI lets a user create and browse product plans and feature docs. A Python backend stores everything as JSON files on disk and integrates with an LLM to generate and expand documentation from prompts. No external services, databases, or auth — runs entirely on localhost.

---

## 1. Goals & Scope

### Goals
- Create, view, edit, and organize product plan / feature documents through a UI.
- Use an LLM to generate a first draft of a document from a short prompt, and to expand/refine existing sections on request.
- Store all product data as JSON on the local filesystem — no database.
- Validate each document against a required-fields schema (also stored as JSON), have an LLM review it against that schema, and block progress until missing/incomplete fields are filled in.
- Once a document validates, use an LLM to generate further downstream artifacts (e.g., user stories, test plans) appropriate to that document's type.

### Non-Goals (for this simple version)
- Multi-user auth, permissions, or hosted deployment.
- Real-time collaboration.
- Integrations with external trackers (Jira, GitHub Issues, etc.) — future enhancement.

---

## 2. Tech Stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite, shadcn/ui, Tailwind CSS |
| Backend | Python (FastAPI) |
| Storage | JSON files on disk (one file per document + an index file) |
| LLM | Provider-agnostic client in backend (Claude by default), called via a `/generate` endpoint |

---

## 3. Data Model

All product data lives under a single `data/` directory as JSON files. No database.

```
data/
  index.json                # list of all documents (id, title, type, status, timestamps)
  documents/
    <doc_id>.json            # full content of one document
  schemas/
    product_plan.schema.json  # required fields/sections for type "product_plan"
    feature.schema.json       # required fields/sections for type "feature"
  artifact_types.json         # artifact_type -> prompt template + target schema mapping
```

**`index.json`**
```json
{
  "documents": [
    {
      "id": "doc_001",
      "title": "Checkout Redesign",
      "type": "feature",        // "product_plan" | "feature"
      "status": "draft",        // "draft" | "in_review" | "approved"
      "created_at": "2026-07-05T10:00:00Z",
      "updated_at": "2026-07-05T10:00:00Z"
    }
  ]
}
```

**`documents/<doc_id>.json`**
```json
{
  "id": "doc_001",
  "title": "Checkout Redesign",
  "type": "feature",
  "status": "draft",
  "sections": [
    { "heading": "Problem", "content": "..." },
    { "heading": "Proposed Solution", "content": "..." },
    { "heading": "Success Metrics", "content": "..." }
  ],
  "prompt_history": [
    { "prompt": "Draft a feature doc for a faster checkout flow", "timestamp": "..." }
  ],
  "validation": {
    "valid": false,
    "checked_at": "2026-07-05T10:05:00Z",
    "missing_fields": ["Success Metrics"],
    "issues": [
      { "field": "Success Metrics", "message": "Section is empty; needs at least one measurable target." }
    ]
  },
  "source_document_id": null,
  "artifact_type": null,
  "linked_artifacts": [],
  "created_at": "2026-07-05T10:00:00Z",
  "updated_at": "2026-07-05T10:00:00Z"
}
```

**`schemas/feature.schema.json`** (required-fields schema, plain JSON Schema)
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
`product_plan.schema.json` follows the same shape with its own `required_sections` list (e.g., `["Overview", "Target Users", "Roadmap", "Success Metrics"]`).

---

## 4. Backend (Python / FastAPI)

### Responsibilities
- Read/write JSON files under `data/` (no ORM, no DB driver).
- Expose a small REST API for the frontend.
- Call the LLM to generate or expand document content, and merge the result back into the document's JSON.
- Validate a document's sections against its type's JSON schema, both structurally and via an LLM review pass, and record the result.
- Generate downstream artifacts from a validated document using per-artifact-type prompt templates.

### API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/documents` | List all documents (from `index.json`) |
| `GET` | `/documents/{id}` | Get full document content |
| `POST` | `/documents` | Create a new document (blank or from a prompt) |
| `PUT` | `/documents/{id}` | Update a document's sections/status/title |
| `DELETE` | `/documents/{id}` | Delete a document |
| `POST` | `/documents/{id}/generate` | Send a prompt + existing content to the LLM, append/update sections with the result |
| `POST` | `/documents/{id}/validate` | Check the document's sections against its type's schema (structurally + LLM review); returns `valid`, `missing_fields`, `issues` |
| `GET` | `/artifact-types` | List available artifact types for a given document type (from `artifact_types.json`) |
| `POST` | `/documents/{id}/artifacts` | Generate a new artifact document (`artifact_type`) from a validated source document |

### File Layout
```
backend/
  main.py            # FastAPI app, route definitions
  storage.py          # read/write helpers for index.json and documents/*.json
  llm.py              # LLM client wrapper (prompt templates, calls out to model)
  validation.py        # loads schemas/*.json, runs structural + LLM-based validation
  models.py            # Pydantic schemas for request/response validation
data/
  index.json
  documents/
  schemas/
  artifact_types.json
```

---

## 5. Frontend (React + shadcn + Tailwind)

### Pages / Views
- **Document List** — table/grid of all documents (title, type, status, last updated), with a "New Document" button.
- **Document Editor** — section-by-section editor (shadcn `Card`/`Textarea` per section), title + status controls, save button.
- **Generate Panel** — a prompt input (shadcn `Textarea` + `Button`) docked in the editor that sends the prompt to `/documents/{id}/generate` and inserts the returned content into the document.
- **New Document Dialog** — shadcn `Dialog` to pick type (`product_plan` / `feature`) and optionally provide an initial prompt to generate the first draft immediately.
- **Validation Panel** — a "Review" button that calls `/documents/{id}/validate` and renders the result: a shadcn `Alert` summarizing missing fields, plus a red outline/`Badge` on any `SectionEditor` card named in `issues`.
- **Artifacts Panel** — once a document is valid, a "Generate Artifacts" button opens a shadcn `Dialog` listing artifact types (from `/artifact-types`); selecting one calls `/documents/{id}/artifacts` and the resulting artifact appears as a linked document.

### Component Structure
```
frontend/
  src/
    pages/
      DocumentList.tsx
      DocumentEditor.tsx
    components/
      NewDocumentDialog.tsx
      GeneratePanel.tsx
      SectionEditor.tsx
      ValidationPanel.tsx
      ArtifactsPanel.tsx
    lib/
      api.ts           # thin fetch wrapper for backend endpoints
```

### How a Document Gets Added to the Screen

1. User clicks **"New Document"** on the Document List page, which opens the New Document Dialog (shadcn `Dialog`).
2. In the dialog, the user:
   - Enters a **title**.
   - Picks a **type** (`product_plan` / `feature`) via shadcn `Select`.
   - Optionally enters an **initial prompt** (e.g., "Draft a feature doc for a faster checkout flow").
3. On submit:
   - If no prompt was given, the frontend calls `POST /documents` with just title/type. The backend creates a document with empty sections, assigns an `id`, writes `documents/<id>.json`, and appends an entry to `index.json`.
   - If a prompt was given, the frontend calls `POST /documents` with title/type/prompt in one request; the backend creates the document, immediately calls the LLM (same path as `/generate`) to produce the first draft, and saves the populated document.
4. The API response (the new document, including its `id`) is used to:
   - Optimistically prepend a row to the Document List table (title, type, status "draft", "just now") without waiting for a full refetch.
   - Navigate the user straight to `/documents/{id}` (the Document Editor), so the newly created — and possibly LLM-drafted — content is visible immediately.
5. The Document Editor fetches `GET /documents/{id}` on mount (confirming what's on disk) and renders one `SectionEditor` per entry in `sections`, so any LLM-generated sections appear as pre-filled, editable cards right away.
6. Any further edits or generate-panel requests call `PUT /documents/{id}` or `POST /documents/{id}/generate`; on success the editor updates in place and the Document List's "last updated" timestamp is refreshed the next time it's viewed (or via the same optimistic-update pattern if the list is kept mounted in a shared state/cache).

### Styling
- Tailwind CSS for layout/utility classes.
- shadcn/ui components (`Button`, `Card`, `Dialog`, `Textarea`, `Badge`, `Table`) for consistent UI primitives — no custom design system needed for v1.

---

## 6. LLM Integration Flow (Draft Generation)

1. User writes a prompt in the Generate Panel (e.g., "Draft the Problem and Success Metrics sections for a faster checkout flow").
2. Frontend calls `POST /documents/{id}/generate` with `{ prompt }`.
3. Backend (`llm.py`) builds a request combining: the prompt, the document's current sections (for context), and a system instruction to return structured section output.
4. LLM response is parsed into `{ heading, content }` sections and merged into the document JSON (new sections appended, matching headings updated).
5. Backend writes the updated document to `documents/<doc_id>.json`, updates `updated_at` in both the document and `index.json`, and returns the updated document to the frontend.
6. Frontend re-renders the editor with the new content; user can keep editing manually or issue another prompt.

---

## 7. Schema Validation & Forced Completion

Each document `type` has a required-fields schema stored as JSON under `schemas/` (see §3). Validation happens in two passes, both triggered by the same `/documents/{id}/validate` call:

1. **Structural check** (`validation.py`, no LLM call): confirms every heading in the type's `required_sections` exists in the document's `sections` array and has non-empty `content`. Anything missing or blank is immediately listed in `missing_fields` — this pass is fast and deterministic.
2. **LLM review pass**: for sections that are structurally present, the backend sends the schema's `required_sections` plus each section's content to the LLM with an instruction to judge whether the content actually satisfies that field's intent (e.g., "Success Metrics" must contain a measurable target, not just prose). The LLM returns `{ field, ok, message }` per section; any `ok: false` entries are appended to `issues`.
3. Backend combines both passes into one result — `{ valid, missing_fields, issues }` — writes it to the document's `validation` object, and returns it to the frontend.
4. **Enforcement in the UI**: the Validation Panel renders `missing_fields`/`issues` inline on the relevant `SectionEditor` cards. The "Generate Artifacts" action (see §8) and the "Mark as In Review/Approved" status transition are disabled in the UI while `validation.valid` is `false`, and the backend independently rejects those two operations with `422` if attempted on an unvalidated/invalid document — so the check can't be bypassed by calling the API directly.
5. The user edits the flagged sections (manually or via another Generate Panel prompt) and re-runs Review until `valid` is `true`.

---

## 8. Artifact Generation Flow

Once a document passes validation, the user can generate further artifacts appropriate to that document's type. Available artifact types per source type are defined in `artifact_types.json` (also plain JSON on disk, editable without code changes), e.g.:

```json
{
  "feature": [
    { "type": "user_stories", "label": "User Stories", "prompt_template": "user_stories.txt" },
    { "type": "test_plan", "label": "Test Plan", "prompt_template": "test_plan.txt" }
  ],
  "product_plan": [
    { "type": "feature_breakdown", "label": "Feature Breakdown", "prompt_template": "feature_breakdown.txt" }
  ]
}
```

Flow:
1. User clicks **"Generate Artifacts"** in the (now-enabled) Artifacts Panel and picks an artifact type from the list returned by `GET /artifact-types?type={document.type}`.
2. Frontend calls `POST /documents/{id}/artifacts` with `{ artifact_type }`.
3. Backend re-checks `validation.valid` is `true` (defense in depth), loads the matching prompt template, and calls the LLM with the source document's full content as context.
4. The LLM's response is saved as a **new** document: `type` set to the artifact type (or a generic `"artifact"` type), `source_document_id` set to the originating doc's `id`, and `artifact_type` set accordingly. It gets its own entry in `index.json` like any other document.
5. The source document's `linked_artifacts` array is updated with the new artifact's `id`, and both files are written back to disk.
6. The frontend adds the new artifact to the Document List and shows it under a "Related Artifacts" list in the source document's editor sidebar, linking to `/documents/{artifact_id}`.

---

## 9. Implementation Steps

| Step | Task |
|---|---|
| 1 | Scaffold backend: FastAPI app, `storage.py` read/write helpers, `data/` directory with empty `index.json` |
| 2 | Implement CRUD endpoints for documents (list, get, create, update, delete) backed by JSON files |
| 3 | Scaffold frontend: Vite + React + Tailwind + shadcn setup, `api.ts` client |
| 4 | Build Document List page wired to `GET /documents` |
| 5 | Build Document Editor page wired to `GET/PUT /documents/{id}` |
| 6 | Add LLM client (`llm.py`) and `/documents/{id}/generate` endpoint |
| 7 | Build Generate Panel + New Document Dialog in the frontend, wired to the generate endpoint |
| 8 | Author `schemas/*.json` for each document type; implement `validation.py` (structural + LLM pass) and `/documents/{id}/validate` |
| 9 | Build Validation Panel in the frontend; wire up enforcement (disable status/artifact actions until valid) |
| 10 | Author `artifact_types.json` and prompt templates; implement `/artifact-types` and `/documents/{id}/artifacts` |
| 11 | Build Artifacts Panel and "Related Artifacts" links in the frontend |
| 12 | Polish: status badges, delete confirmation, basic empty/error states |

---

## 10. Open Questions

- Which LLM provider/model to default to, and how API keys are supplied locally (env var vs. config file).
- Whether documents need a fixed section template per `type` (product_plan vs. feature) or fully freeform sections.
- Whether prompt history per document (already in the data model) should be surfaced in the UI in v1 or just stored for later.
- How strict the LLM review pass should be by default (e.g., a confidence/leniency setting) to avoid blocking users on borderline content.
- Whether artifact documents should be editable/re-validatable like primary documents, or treated as read-only outputs.
