import type { ExportFormat, GeneratedPRD, GenerateResponse, ProjectMeta } from "./types"

export const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000"

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  })
  if (!res.ok) {
    const body = await res.text().catch(() => "")
    throw new Error(`${res.status} ${res.statusText}: ${body}`)
  }
  return res.json() as Promise<T>
}

export const api = {
  listProjects: () => request<ProjectMeta[]>("/projects"),

  createProject: (name: string) =>
    request<ProjectMeta>("/projects", {
      method: "POST",
      body: JSON.stringify({ name }),
    }),

  getProject: (projectId: string) =>
    request<ProjectMeta>(`/projects/${projectId}`),

  generate: (projectId: string, rawNotes: string) =>
    request<GenerateResponse>(`/projects/${projectId}/generate`, {
      method: "POST",
      body: JSON.stringify({ raw_notes: rawNotes }),
    }),

  regenerateSection: (projectId: string, artifactId: string, section: string, context: string) =>
    request<{ prd: GeneratedPRD }>(
      `/projects/${projectId}/artifacts/${artifactId}/regenerate-section`,
      { method: "POST", body: JSON.stringify({ section, context }) }
    ),

  listArtifacts: (projectId: string) =>
    request<{ artifact_ids: string[] }>(`/projects/${projectId}/artifacts`),

  getArtifact: (projectId: string, artifactId: string) =>
    request<GeneratedPRD>(`/projects/${projectId}/artifacts/${artifactId}`),

  updateArtifact: (projectId: string, artifactId: string, prd: GeneratedPRD) =>
    request<{ status: string }>(`/projects/${projectId}/artifacts/${artifactId}`, {
      method: "PUT",
      body: JSON.stringify(prd),
    }),

  deleteArtifact: (projectId: string, artifactId: string) =>
    request<{ status: string }>(`/projects/${projectId}/artifacts/${artifactId}`, {
      method: "DELETE",
    }),

  exportUrl: (projectId: string, artifactId: string, format: ExportFormat) =>
    `${API_BASE}/projects/${projectId}/artifacts/${artifactId}/export/${format}`,
}
