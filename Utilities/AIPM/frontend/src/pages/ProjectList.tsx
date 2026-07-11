import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import type { ProjectMeta } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"

interface ProjectListProps {
  onSelectProject: (project: ProjectMeta) => void
  onNewProject: () => void
}

export function ProjectList({ onSelectProject, onNewProject }: ProjectListProps) {
  const [projects, setProjects] = useState<ProjectMeta[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .listProjects()
      .then(setProjects)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="mx-auto max-w-2xl px-6 py-10">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Projects</h1>
        <Button onClick={onNewProject}>New Project</Button>
      </div>

      {error && (
        <p className="mb-4 text-sm text-destructive">
          Couldn't reach the backend ({error}). Is it running on {import.meta.env.VITE_API_BASE ?? "http://localhost:8000"}?
        </p>
      )}

      {loading ? (
        <p className="text-sm text-muted-foreground">Loading…</p>
      ) : projects.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          No projects yet. Click "New Project" to generate your first PRD.
        </p>
      ) : (
        <div className="flex flex-col gap-3">
          {projects.map((project) => (
            <Card
              key={project.id}
              className="cursor-pointer transition-colors hover:bg-accent/50"
              onClick={() => onSelectProject(project)}
            >
              <CardHeader>
                <CardTitle>{project.name}</CardTitle>
                <CardDescription>
                  Updated {new Date(project.updated_at).toLocaleString()}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
