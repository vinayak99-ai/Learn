import { useState } from "react"
import { api } from "@/lib/api"
import type { GeneratedPRD } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"

interface NewProjectProps {
  onGenerated: (projectId: string, artifactId: string, prd: GeneratedPRD) => void
  onCancel: () => void
}

export function NewProject({ onGenerated, onCancel }: NewProjectProps) {
  const [name, setName] = useState("")
  const [rawNotes, setRawNotes] = useState("")
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const canSubmit = name.trim().length > 0 && rawNotes.trim().length > 0 && !busy

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!canSubmit) return
    setBusy(true)
    setError(null)
    try {
      const project = await api.createProject(name.trim())
      const { artifact_id, prd } = await api.generate(project.id, rawNotes.trim())
      onGenerated(project.id, artifact_id, prd)
    } catch (err) {
      setError(
        `${err}. If this is an authentication error, make sure ANTHROPIC_API_KEY is set in config/.env.`
      )
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-6 py-10">
      <h1 className="mb-6 text-2xl font-semibold">New Project</h1>

      <Card>
        <CardHeader>
          <CardTitle>Raw notes → PRD</CardTitle>
          <CardDescription>
            Paste whatever you have — a Slack thread, meeting notes, a rough
            idea. The extraction and generation agents will turn it into a
            structured PRD.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            <div className="flex flex-col gap-2">
              <Label htmlFor="name">Project name</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Checkout Redesign"
              />
            </div>

            <div className="flex flex-col gap-2">
              <Label htmlFor="notes">Raw notes</Label>
              <Textarea
                id="notes"
                className="min-h-48"
                value={rawNotes}
                onChange={(e) => setRawNotes(e.target.value)}
                placeholder="We want to speed up checkout, it's too slow and we're losing customers at payment..."
              />
            </div>

            {error && <p className="text-sm text-destructive">{error}</p>}

            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={onCancel} disabled={busy}>
                Cancel
              </Button>
              <Button type="submit" disabled={!canSubmit}>
                {busy ? "Generating…" : "Generate PRD"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
