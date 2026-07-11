import { useState } from "react"
import { ProjectList } from "@/pages/ProjectList"
import { NewProject } from "@/pages/NewProject"
import { ProjectDetail } from "@/pages/ProjectDetail"
import type { GeneratedPRD, ProjectMeta } from "@/lib/types"

type View =
  | { name: "list" }
  | { name: "new" }
  | { name: "detail"; projectId: string; projectName: string; artifactId?: string; prd?: GeneratedPRD }

function App() {
  const [view, setView] = useState<View>({ name: "list" })

  return (
    <div className="min-h-svh bg-background text-foreground">
      <header className="border-b">
        <div className="mx-auto max-w-3xl px-6 py-4">
          <h1 className="text-sm font-semibold tracking-wide text-muted-foreground uppercase">
            AI PM Portal
          </h1>
        </div>
      </header>

      <main>
        {view.name === "list" && (
          <ProjectList
            onSelectProject={(project: ProjectMeta) =>
              setView({ name: "detail", projectId: project.id, projectName: project.name })
            }
            onNewProject={() => setView({ name: "new" })}
          />
        )}

        {view.name === "new" && (
          <NewProject
            onCancel={() => setView({ name: "list" })}
            onGenerated={(projectId, artifactId, prd) =>
              setView({ name: "detail", projectId, projectName: prd.title, artifactId, prd })
            }
          />
        )}

        {view.name === "detail" && (
          <ProjectDetail
            projectId={view.projectId}
            projectName={view.projectName}
            initialArtifactId={view.artifactId}
            initialPrd={view.prd}
            onBack={() => setView({ name: "list" })}
          />
        )}
      </main>
    </div>
  )
}

export default App
