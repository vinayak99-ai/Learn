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
  "created_at": "2026-07-05T10:00:00Z",
  "updated_at": "2026-07-05T10:00:00Z"
}
```

---

## 4. Backend (Python / FastAPI)

### Responsibilities
- Read/write JSON files under `data/` (no ORM, no DB driver).
- Expose a small REST API for the frontend.
- Call the LLM to generate or expand document content, and merge the result back into the document's JSON.

### API Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/documents` | List all documents (from `index.json`) |
| `GET` | `/documents/{id}` | Get full document content |
| `POST` | `/documents` | Create a new document (blank or from a prompt) |
| `PUT` | `/documents/{id}` | Update a document's sections/status/title |
| `DELETE` | `/documents/{id}` | Delete a document |
| `POST` | `/documents/{id}/generate` | Send a prompt + existing content to the LLM, append/update sections with the result |

### File Layout
```
backend/
  main.py            # FastAPI app, route definitions
  storage.py          # read/write helpers for index.json and documents/*.json
  llm.py              # LLM client wrapper (prompt templates, calls out to model)
  models.py            # Pydantic schemas for request/response validation
data/
  index.json
  documents/
```

---

## 5. Frontend (React + shadcn + Tailwind)

### Pages / Views
- **Document List** — table/grid of all documents (title, type, status, last updated), with a "New Document" button.
- **Document Editor** — section-by-section editor (shadcn `Card`/`Textarea` per section), title + status controls, save button.
- **Generate Panel** — a prompt input (shadcn `Textarea` + `Button`) docked in the editor that sends the prompt to `/documents/{id}/generate` and inserts the returned content into the document.
- **New Document Dialog** — shadcn `Dialog` to pick type (`product_plan` / `feature`) and optionally provide an initial prompt to generate the first draft immediately.

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
    lib/
      api.ts           # thin fetch wrapper for backend endpoints
```

### Styling
- Tailwind CSS for layout/utility classes.
- shadcn/ui components (`Button`, `Card`, `Dialog`, `Textarea`, `Badge`, `Table`) for consistent UI primitives — no custom design system needed for v1.

---

## 6. LLM Integration Flow

1. User writes a prompt in the Generate Panel (e.g., "Draft the Problem and Success Metrics sections for a faster checkout flow").
2. Frontend calls `POST /documents/{id}/generate` with `{ prompt }`.
3. Backend (`llm.py`) builds a request combining: the prompt, the document's current sections (for context), and a system instruction to return structured section output.
4. LLM response is parsed into `{ heading, content }` sections and merged into the document JSON (new sections appended, matching headings updated).
5. Backend writes the updated document to `documents/<doc_id>.json`, updates `updated_at` in both the document and `index.json`, and returns the updated document to the frontend.
6. Frontend re-renders the editor with the new content; user can keep editing manually or issue another prompt.

---

## 7. Implementation Steps

| Step | Task |
|---|---|
| 1 | Scaffold backend: FastAPI app, `storage.py` read/write helpers, `data/` directory with empty `index.json` |
| 2 | Implement CRUD endpoints for documents (list, get, create, update, delete) backed by JSON files |
| 3 | Scaffold frontend: Vite + React + Tailwind + shadcn setup, `api.ts` client |
| 4 | Build Document List page wired to `GET /documents` |
| 5 | Build Document Editor page wired to `GET/PUT /documents/{id}` |
| 6 | Add LLM client (`llm.py`) and `/documents/{id}/generate` endpoint |
| 7 | Build Generate Panel + New Document Dialog in the frontend, wired to the generate endpoint |
| 8 | Polish: status badges, delete confirmation, basic empty/error states |

---

## 8. Open Questions

- Which LLM provider/model to default to, and how API keys are supplied locally (env var vs. config file).
- Whether documents need a fixed section template per `type` (product_plan vs. feature) or fully freeform sections.
- Whether prompt history per document (already in the data model) should be surfaced in the UI in v1 or just stored for later.
