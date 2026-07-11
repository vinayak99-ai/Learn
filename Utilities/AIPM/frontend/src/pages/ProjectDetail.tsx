import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import type { GeneratedPRD } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { EditableList } from "@/components/EditableList"
import { UserStoryCard } from "@/components/UserStoryCard"
import { Plus } from "lucide-react"

interface ProjectDetailProps {
  projectId: string
  projectName: string
  initialArtifactId?: string
  initialPrd?: GeneratedPRD
  onBack: () => void
}

const emptyStory = { as_a: "", i_want: "", so_that: "", acceptance_criteria: [] }

export function ProjectDetail({
  projectId,
  projectName,
  initialArtifactId,
  initialPrd,
  onBack,
}: ProjectDetailProps) {
  const [artifactId, setArtifactId] = useState<string | null>(initialArtifactId ?? null)
  const [prd, setPrd] = useState<GeneratedPRD | null>(initialPrd ?? null)
  const [loading, setLoading] = useState(!initialPrd)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [savedAt, setSavedAt] = useState<Date | null>(null)

  useEffect(() => {
    if (initialPrd) return
    setLoading(true)
    api
      .listArtifacts(projectId)
      .then(async ({ artifact_ids }) => {
        if (artifact_ids.length === 0) {
          setPrd(null)
          return
        }
        const id = artifact_ids[0]
        const loaded = await api.getArtifact(projectId, id)
        setArtifactId(id)
        setPrd(loaded)
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false))
  }, [projectId, initialPrd])

  async function handleSave() {
    if (!prd || !artifactId) return
    setSaving(true)
    setError(null)
    try {
      await api.updateArtifact(projectId, artifactId, prd)
      setSavedAt(new Date())
    } catch (e) {
      setError(String(e))
    } finally {
      setSaving(false)
    }
  }

  function update<K extends keyof GeneratedPRD>(key: K, value: GeneratedPRD[K]) {
    if (!prd) return
    setPrd({ ...prd, [key]: value })
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <div className="mb-6 flex items-center justify-between">
        <Button variant="ghost" onClick={onBack}>
          ← Projects
        </Button>
        {artifactId && (
          <div className="flex gap-2">
            <Button variant="outline" size="sm" asChild>
              <a href={api.exportUrl(projectId, artifactId, "md")}>Export .md</a>
            </Button>
            <Button variant="outline" size="sm" asChild>
              <a href={api.exportUrl(projectId, artifactId, "docx")}>Export .docx</a>
            </Button>
            <Button variant="outline" size="sm" asChild>
              <a href={api.exportUrl(projectId, artifactId, "csv")}>Export .csv</a>
            </Button>
            <Button size="sm" onClick={handleSave} disabled={saving}>
              {saving ? "Saving…" : "Save"}
            </Button>
          </div>
        )}
      </div>

      {loading && <p className="text-sm text-muted-foreground">Loading…</p>}
      {error && <p className="mb-4 text-sm text-destructive">{error}</p>}

      {!loading && !prd && (
        <p className="text-sm text-muted-foreground">
          No PRD generated yet for "{projectName}". Go back and use "New Project" to generate one.
        </p>
      )}

      {prd && (
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <Label htmlFor="title">Title</Label>
            <Input
              id="title"
              className="text-lg font-semibold"
              value={prd.title}
              onChange={(e) => update("title", e.target.value)}
            />
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor="problem">Problem statement</Label>
            <Textarea
              id="problem"
              className="min-h-24"
              value={prd.problem_statement}
              onChange={(e) => update("problem_statement", e.target.value)}
            />
          </div>

          <EditableList label="Goals" items={prd.goals} onChange={(goals) => update("goals", goals)} />

          <Separator />

          <div className="flex items-center justify-between">
            <Label>User stories</Label>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => update("user_stories", [...prd.user_stories, { ...emptyStory }])}
            >
              <Plus className="size-4" /> Add story
            </Button>
          </div>
          <div className="flex flex-col gap-4">
            {prd.user_stories.map((story, i) => (
              <UserStoryCard
                key={i}
                index={i}
                story={story}
                onChange={(updated) => {
                  const next = [...prd.user_stories]
                  next[i] = updated
                  update("user_stories", next)
                }}
                onRemove={() =>
                  update(
                    "user_stories",
                    prd.user_stories.filter((_, idx) => idx !== i)
                  )
                }
              />
            ))}
          </div>

          <Separator />

          <EditableList
            label="Success metrics"
            items={prd.success_metrics}
            onChange={(success_metrics) => update("success_metrics", success_metrics)}
          />

          <EditableList
            label="Assumptions"
            items={prd.assumptions}
            onChange={(assumptions) => update("assumptions", assumptions)}
          />

          {savedAt && (
            <p className="text-xs text-muted-foreground">Saved at {savedAt.toLocaleTimeString()}</p>
          )}
        </div>
      )}
    </div>
  )
}
