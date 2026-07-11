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
