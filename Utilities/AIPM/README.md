# AI PM Portal — MVP Implementation

A working implementation of [`mvp-aipm.md`](../../plans/mvp-aipm.md)'s single-shot design: paste raw notes, get a structured PRD (problem statement, goals, user stories with acceptance criteria, success metrics, assumptions), edit it, and export to Markdown/.docx/.csv. Local-first — no database, no auth, no JIRA/Confluence integration.

> Note: this is a separate implementation track from the chat-style, checklist-driven design in [`plans/AI-PM.md`](../../plans/AI-PM.md) (the actual product roadmap). See that document's §9 for how the two relate.

## Structure

```
AIPM/
  backend/     FastAPI + PydanticAI (two-stage extraction -> generation agents)
  frontend/    React + Vite + TypeScript + Tailwind CSS + shadcn/ui
  config/      .env.example (copy to config/.env with your ANTHROPIC_API_KEY)
```

## Running it

**1. Set your API key**

```bash
cp config/.env.example config/.env
# edit config/.env and set ANTHROPIC_API_KEY
```

**2. Backend**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate      # .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs at `http://localhost:8000/docs`.

**3. Frontend** (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

App at `http://localhost:5173`.

## What's implemented

- Create a project, paste raw notes, generate a PRD via two chained PydanticAI agents (extraction → generation).
- Edit the generated PRD in the browser: title, problem statement, goals, user stories (with acceptance criteria), success metrics, assumptions — all editable, with add/remove for list items and stories.
- Save edits back to disk (`PUT /projects/{id}/artifacts/{id}`).
- Export the PRD as Markdown, .docx, or a JIRA-importable .csv of the user stories.
- Data persists to `~/pm-portal-data/projects/<project_id>/` as plain JSON — inspect or back it up directly.

## Known gaps (not implemented)

- No UI for `POST /.../regenerate-section` (the endpoint exists in the backend; the frontend doesn't call it yet).
- No delete-project UI (only delete-artifact exists on the backend).
- Single global CORS allowlist (`localhost:3000`/`localhost:5173`) — fine for local use, would need revisiting for anything else.
