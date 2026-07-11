from pathlib import Path
import tempfile
import os

from dotenv import load_dotenv

# Load ANTHROPIC_API_KEY (and any other vars) from config/.env before the
# agents module constructs its Agent objects, which read the key at import time.
load_dotenv(Path(__file__).resolve().parent.parent / "config" / ".env")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_ai.exceptions import ModelHTTPError

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

def _agent_error_detail(exc: Exception) -> str:
    if isinstance(exc, ModelHTTPError):
        return f"Claude API error ({exc.status_code}): {exc.body}"
    return f"Agent call failed: {exc}"

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

    try:
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
    except ModelHTTPError as e:
        raise HTTPException(status_code=502, detail=_agent_error_detail(e))

    artifact_id = save_artifact(project_id, prd)
    return {"artifact_id": artifact_id, "prd": prd}

@app.post("/projects/{project_id}/artifacts/{artifact_id}/regenerate-section")
def api_regenerate_section(project_id: str, artifact_id: str, req: RegenerateSectionRequest):
    prd = load_artifact(project_id, artifact_id)

    try:
        result = generation_agent.run_sync(
            f"Regenerate ONLY the {req.section} section. "
            f"Current PRD context: {req.context}. "
            f"Return the full PRD structure but only change {req.section}."
        )
        updated_prd = result.output
    except ModelHTTPError as e:
        raise HTTPException(status_code=502, detail=_agent_error_detail(e))

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
