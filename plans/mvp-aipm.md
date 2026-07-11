# AI Product Manager Portal — Phase 1 MVP (Local-First)

This document captures the Phase 1 design and reference code for the AI PM Portal:
requirements documentation, PRD generation, and local export — built with PydanticAI
and FastAPI, no OAuth/JIRA/Confluence integration yet.

## Overview

**Core loop:** Raw notes → AI extraction → AI generation → editable draft → local file export (Markdown / .docx / .csv)

**Stack:**
- Agents: PydanticAI (two-stage: extraction → generation)
- Backend: FastAPI
- Persistence: local JSON files (no database)
- Frontend: React (editable form over typed PRD schema)
- Export: Markdown, .docx (python-docx), .csv (JIRA-importable)

---

## 1. Agents (`agents.py`)

```python
from pydantic import BaseModel
from pydantic_ai import Agent

# ---------- Stage 1: Extraction ----------

class ExtractedRequirements(BaseModel):
    problem_statement: str
    goals: list[str]
    target_users: list[str]
    open_questions: list[str]

agent = Agent(
    'anthropic:claude-sonnet-4-5',
    output_type=ExtractedRequirements,
    system_prompt=(
        "You extract structured product requirements from raw notes. "
        "Only include information present in the notes. "
        "Flag anything ambiguous as an open question rather than guessing."
    ),
)

# ---------- Stage 2: Generation ----------

class UserStory(BaseModel):
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: list[str]

class GeneratedPRD(BaseModel):
    title: str
    problem_statement: str
    goals: list[str]
    user_stories: list[UserStory]
    success_metrics: list[str]
    assumptions: list[str]

generation_agent = Agent(
    'anthropic:claude-sonnet-4-5',
    output_type=GeneratedPRD,
    system_prompt=(
        "You are a senior PM writing a PRD. Given extracted requirements, "
        "generate user stories following INVEST principles (Independent, "
        "Negotiable, Valuable, Estimable, Small, Testable). Each story needs "
        "clear, testable acceptance criteria. Do not invent goals not implied "
        "by the input."
    ),
)

# ---------- Chaining ----------

def generate_prd(raw_notes: str) -> GeneratedPRD:
    extraction_result = agent.run_sync(raw_notes)
    extracted = extraction_result.output

    prompt = f"""
    Problem: {extracted.problem_statement}
    Goals: {extracted.goals}
    Target users: {extracted.target_users}
    Open questions to keep in mind: {extracted.open_questions}
    """
    generation_result = generation_agent.run_sync(prompt)
    return generation_result.output
```

Optional tool example (agent can call this mid-run to stay consistent with existing terminology):

```python
@agent.tool
async def get_project_glossary(ctx, project_key: str) -> str:
    """Fetch existing product terminology for a project."""
    return "Terms: 'export' means download-only, not email delivery."
```

Per-section regeneration (avoids redoing the whole doc when only one part is off):

```python
def regenerate_user_stories(extracted: ExtractedRequirements) -> list[UserStory]:
    result = generation_agent.run_sync(
        f"Regenerate only user stories for: {extracted.problem_statement}"
    )
    return result.output.user_stories
```

---

## 2. Export Layer (`export.py`)

```python
from docx import Document
import csv

def export_to_markdown(prd) -> str:
    lines = [f"# {prd.title}\n"]
    lines.append("## Problem Statement")
    lines.append(f"{prd.problem_statement}\n")

    lines.append("## Goals")
    for goal in prd.goals:
        lines.append(f"- {goal}")
    lines.append("")

    lines.append("## User Stories")
    for i, story in enumerate(prd.user_stories, 1):
        lines.append(f"### Story {i}")
        lines.append(f"**As a** {story.as_a}, **I want** {story.i_want}, "
                      f"**so that** {story.so_that}\n")
        lines.append("**Acceptance Criteria:**")
        for ac in story.acceptance_criteria:
            lines.append(f"- [ ] {ac}")
        lines.append("")

    lines.append("## Success Metrics")
    for metric in prd.success_metrics:
        lines.append(f"- {metric}")
    lines.append("")

    lines.append("## Assumptions")
    for a in prd.assumptions:
        lines.append(f"- {a}")

    return "\n".join(lines)


def export_to_docx(prd, path: str):
    doc = Document()
    doc.add_heading(prd.title, level=0)

    doc.add_heading("Problem Statement", level=1)
    doc.add_paragraph(prd.problem_statement)

    doc.add_heading("Goals", level=1)
    for goal in prd.goals:
        doc.add_paragraph(goal, style="List Bullet")

    doc.add_heading("User Stories", level=1)
    for i, story in enumerate(prd.user_stories, 1):
        doc.add_heading(f"Story {i}", level=2)
        p = doc.add_paragraph()
        p.add_run(f"As a {story.as_a}, I want {story.i_want}, "
                   f"so that {story.so_that}").italic = True

        doc.add_paragraph("Acceptance Criteria:", style="Intense Quote")
        for ac in story.acceptance_criteria:
            doc.add_paragraph(ac, style="List Bullet")

    doc.add_heading("Success Metrics", level=1)
    for m in prd.success_metrics:
        doc.add_paragraph(m, style="List Bullet")

    doc.add_heading("Assumptions", level=1)
    for a in prd.assumptions:
        doc.add_paragraph(a, style="List Bullet")

    doc.save(path)


def export_stories_to_csv(prd, path: str):
    """JIRA-importable CSV bridge (no API integration needed yet)."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Summary", "Description", "Acceptance Criteria"])
        for story in prd.user_stories:
            summary = f"As a {story.as_a}, I want {story.i_want}"
            description = f"So that {story.so_that}"
            criteria = "; ".join(story.acceptance_criteria)
            writer.writerow([summary, description, criteria])
```

---

## 3. Persistence Layer (`persistence.py`)

Local-first, filesystem-based — no database required for MVP validation.

```
~/pm-portal-data/
  projects/
    proj_a1b2c3/
      meta.json
      artifacts/
        prd_001.json
      raw_inputs/
        input_001.txt
```

```python
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
from pydantic import BaseModel

DATA_ROOT = Path.home() / "pm-portal-data" / "projects"

class ProjectMeta(BaseModel):
    id: str
    name: str
    created_at: str
    updated_at: str

def _project_dir(project_id: str) -> Path:
    return DATA_ROOT / project_id

def create_project(name: str) -> ProjectMeta:
    project_id = f"proj_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    meta = ProjectMeta(id=project_id, name=name, created_at=now, updated_at=now)

    proj_dir = _project_dir(project_id)
    (proj_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (proj_dir / "raw_inputs").mkdir(exist_ok=True)

    with open(proj_dir / "meta.json", "w") as f:
        f.write(meta.model_dump_json(indent=2))

    return meta

def list_projects() -> list[ProjectMeta]:
    if not DATA_ROOT.exists():
        return []
    projects = []
    for proj_dir in DATA_ROOT.iterdir():
        meta_file = proj_dir / "meta.json"
        if meta_file.exists():
            projects.append(ProjectMeta.model_validate_json(meta_file.read_text()))
    return sorted(projects, key=lambda p: p.updated_at, reverse=True)

def get_project(project_id: str) -> ProjectMeta:
    meta_file = _project_dir(project_id) / "meta.json"
    return ProjectMeta.model_validate_json(meta_file.read_text())

def save_artifact(project_id: str, prd, artifact_id: str = None) -> str:
    artifact_id = artifact_id or f"prd_{uuid.uuid4().hex[:8]}"
    artifacts_dir = _project_dir(project_id) / "artifacts"

    with open(artifacts_dir / f"{artifact_id}.json", "w") as f:
        f.write(prd.model_dump_json(indent=2))

    _touch_project(project_id)
    return artifact_id

def load_artifact(project_id: str, artifact_id: str):
    from agents import GeneratedPRD
    path = _project_dir(project_id) / "artifacts" / f"{artifact_id}.json"
    return GeneratedPRD.model_validate_json(path.read_text())

def list_artifacts(project_id: str) -> list[str]:
    artifacts_dir = _project_dir(project_id) / "artifacts"
    if not artifacts_dir.exists():
        return []
    return [f.stem for f in artifacts_dir.glob("*.json")]

def delete_artifact(project_id: str, artifact_id: str):
    path = _project_dir(project_id) / "artifacts" / f"{artifact_id}.json"
    path.unlink(missing_ok=True)

def save_raw_input(project_id: str, text: str) -> str:
    input_id = f"input_{uuid.uuid4().hex[:8]}"
    path = _project_dir(project_id) / "raw_inputs" / f"{input_id}.txt"
    path.write_text(text)
    return input_id

def _touch_project(project_id: str):
    meta = get_project(project_id)
    meta.updated_at = datetime.now(timezone.utc).isoformat()
    meta_file = _project_dir(project_id) / "meta.json"
    meta_file.write_text(meta.model_dump_json(indent=2))
```

---

## 4. FastAPI Backend (`main.py`)

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os

from persistence import (
    create_project, list_projects, get_project,
    save_artifact, load_artifact, list_artifacts, delete_artifact,
    save_raw_input, ProjectMeta
)
from agents import agent, generation_agent, ExtractedRequirements, GeneratedPRD
from export import export_to_markdown, export_to_docx, export_stories_to_csv

app = FastAPI(title="PM Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateProjectRequest(BaseModel):
    name: str

class GenerateRequest(BaseModel):
    raw_notes: str

class RegenerateSectionRequest(BaseModel):
    section: str
    context: str

@app.post("/projects", response_model=ProjectMeta)
def api_create_project(req: CreateProjectRequest):
    return create_project(req.name)

@app.get("/projects", response_model=list[ProjectMeta])
def api_list_projects():
    return list_projects()

@app.get("/projects/{project_id}", response_model=ProjectMeta)
def api_get_project(project_id: str):
    try:
        return get_project(project_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/projects/{project_id}/generate")
def api_generate(project_id: str, req: GenerateRequest):
    save_raw_input(project_id, req.raw_notes)

    extraction_result = agent.run_sync(req.raw_notes)
    extracted = extraction_result.output

    prompt = f"""
    Problem: {extracted.problem_statement}
    Goals: {extracted.goals}
    Target users: {extracted.target_users}
    Open questions to keep in mind: {extracted.open_questions}
    """
    generation_result = generation_agent.run_sync(prompt)
    prd = generation_result.output

    artifact_id = save_artifact(project_id, prd)
    return {"artifact_id": artifact_id, "prd": prd}

@app.post("/projects/{project_id}/artifacts/{artifact_id}/regenerate-section")
def api_regenerate_section(project_id: str, artifact_id: str, req: RegenerateSectionRequest):
    prd = load_artifact(project_id, artifact_id)

    result = generation_agent.run_sync(
        f"Regenerate ONLY the {req.section} section. "
        f"Current PRD context: {req.context}. "
        f"Return the full PRD structure but only change {req.section}."
    )
    updated_prd = result.output

    save_artifact(project_id, updated_prd, artifact_id)
    return {"prd": updated_prd}

@app.get("/projects/{project_id}/artifacts")
def api_list_artifacts(project_id: str):
    return {"artifact_ids": list_artifacts(project_id)}

@app.get("/projects/{project_id}/artifacts/{artifact_id}", response_model=GeneratedPRD)
def api_get_artifact(project_id: str, artifact_id: str):
    try:
        return load_artifact(project_id, artifact_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Artifact not found")

@app.put("/projects/{project_id}/artifacts/{artifact_id}")
def api_update_artifact(project_id: str, artifact_id: str, prd: GeneratedPRD):
    save_artifact(project_id, prd, artifact_id)
    return {"status": "saved"}

@app.delete("/projects/{project_id}/artifacts/{artifact_id}")
def api_delete_artifact(project_id: str, artifact_id: str):
    delete_artifact(project_id, artifact_id)
    return {"status": "deleted"}

@app.get("/projects/{project_id}/artifacts/{artifact_id}/export/{format}")
def api_export(project_id: str, artifact_id: str, format: str):
    from fastapi.responses import FileResponse

    prd = load_artifact(project_id, artifact_id)

    tmp_dir = tempfile.mkdtemp()
    if format == "md":
        path = os.path.join(tmp_dir, f"{prd.title}.md")
        with open(path, "w") as f:
            f.write(export_to_markdown(prd))
        media_type = "text/markdown"
    elif format == "docx":
        path = os.path.join(tmp_dir, f"{prd.title}.docx")
        export_to_docx(prd, path)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif format == "csv":
        path = os.path.join(tmp_dir, f"{prd.title}_stories.csv")
        export_stories_to_csv(prd, path)
        media_type = "text/csv"
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use md, docx, or csv.")

    return FileResponse(path, media_type=media_type, filename=os.path.basename(path))
```

**Run it locally:**

```bash
pip install fastapi uvicorn pydantic-ai python-docx --break-system-packages
uvicorn main:app --reload --port 8000
```

Interactive API docs available at `http://localhost:8000/docs`.

---

## 5. React Integration Snippets

```javascript
// Generate a new PRD
const res = await fetch(`http://localhost:8000/projects/${projectId}/generate`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ raw_notes: notesText })
});
const { artifact_id, prd } = await res.json();

// Save edits
await fetch(`http://localhost:8000/projects/${projectId}/artifacts/${artifact_id}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(editedPrd)
});

// Export — triggers file download
window.open(`http://localhost:8000/projects/${projectId}/artifacts/${artifact_id}/export/docx`);
```

```jsx
function PRDEditor({ prd }) {
  const [data, setData] = useState(prd);

  const updateStory = (index, field, value) => {
    const stories = [...data.user_stories];
    stories[index] = { ...stories[index], [field]: value };
    setData({ ...data, user_stories: stories });
  };

  return (
    <div>
      <input
        value={data.title}
        onChange={e => setData({ ...data, title: e.target.value })}
      />
      {data.user_stories.map((story, i) => (
        <div key={i}>
          <textarea
            value={story.i_want}
            onChange={e => updateStory(i, 'i_want', e.target.value)}
          />
        </div>
      ))}
      <button onClick={() => exportToMarkdown(data)}>Export</button>
    </div>
  );
}
```

---

## Roadmap (Phases 2+)

1. **JIRA sync** — convert user stories into JIRA epics/tickets; read-only status pull first
2. **Progress reporting** — burndown, blockers, velocity summaries from JIRA data
3. **Business value / ROI docs** — guided template with PM-supplied figures, not AI-invented numbers
4. **Feature engineering** — RICE-style scoring and backlog prioritization assistance

## Framework Notes: PydanticAI vs LangGraph

- PydanticAI treats an agent as a typed Python object with schema-validated output — the right fit for Phase 1's linear extraction → generation flow.
- LangGraph treats an agent as a graph of nodes/edges — better suited for later phases needing approval gates, pause/resume, or multi-agent orchestration (e.g., PM review → stakeholder sign-off → JIRA push).
- Recommended path: start with PydanticAI now, layer in LangGraph only when workflow branching/durability becomes a real requirement.
