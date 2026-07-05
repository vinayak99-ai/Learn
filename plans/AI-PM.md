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

## 8. Beyond the MVP (Later Phases, Not This Build)

Ideas from earlier planning that are explicitly out of scope for this MVP, kept here so they aren't lost:

- **Multi-turn conversational intake** instead of one-shot input + one round of questions.
- **Feature breakdown**: splitting a product into child feature documents, each with their own intake.
- **Schema-driven validation**: required-fields JSON schemas per document type, with a dedicated Validation Agent and enforcement gates.
- **Downstream artifact generation**: user stories, test plans, etc. generated from a validated document.
- **Business "value" section** on feature docs, distinct from success metrics.
- **Real login/auth** if this ever needs more than one user.
