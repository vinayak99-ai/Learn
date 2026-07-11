import type { UserStory } from "@/lib/types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { EditableList } from "@/components/EditableList"
import { Trash2 } from "lucide-react"

interface UserStoryCardProps {
  index: number
  story: UserStory
  onChange: (story: UserStory) => void
  onRemove: () => void
}

export function UserStoryCard({ index, story, onChange, onRemove }: UserStoryCardProps) {
  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between">
        <CardTitle className="text-base">Story {index + 1}</CardTitle>
        <Button variant="ghost" size="icon" onClick={onRemove} aria-label="Remove story">
          <Trash2 className="size-4" />
        </Button>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div className="flex flex-col gap-2">
            <Label>As a</Label>
            <Input
              value={story.as_a}
              onChange={(e) => onChange({ ...story, as_a: e.target.value })}
            />
          </div>
          <div className="flex flex-col gap-2">
            <Label>I want</Label>
            <Input
              value={story.i_want}
              onChange={(e) => onChange({ ...story, i_want: e.target.value })}
            />
          </div>
          <div className="flex flex-col gap-2">
            <Label>So that</Label>
            <Input
              value={story.so_that}
              onChange={(e) => onChange({ ...story, so_that: e.target.value })}
            />
          </div>
        </div>

        <EditableList
          label="Acceptance criteria"
          items={story.acceptance_criteria}
          onChange={(acceptance_criteria) => onChange({ ...story, acceptance_criteria })}
        />
      </CardContent>
    </Card>
  )
}
