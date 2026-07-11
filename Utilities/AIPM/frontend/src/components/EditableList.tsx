import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { X, Plus } from "lucide-react"

interface EditableListProps {
  label: string
  items: string[]
  onChange: (items: string[]) => void
  placeholder?: string
}

export function EditableList({ label, items, onChange, placeholder }: EditableListProps) {
  function updateItem(index: number, value: string) {
    const next = [...items]
    next[index] = value
    onChange(next)
  }

  function removeItem(index: number) {
    onChange(items.filter((_, i) => i !== index))
  }

  function addItem() {
    onChange([...items, ""])
  }

  return (
    <div className="flex flex-col gap-2">
      <Label>{label}</Label>
      {items.map((item, i) => (
        <div key={i} className="flex items-center gap-2">
          <Input
            value={item}
            placeholder={placeholder}
            onChange={(e) => updateItem(i, e.target.value)}
          />
          <Button
            type="button"
            variant="ghost"
            size="icon"
            onClick={() => removeItem(i)}
            aria-label={`Remove ${label} item`}
          >
            <X className="size-4" />
          </Button>
        </div>
      ))}
      <Button type="button" variant="outline" size="sm" className="self-start" onClick={addItem}>
        <Plus className="size-4" /> Add
      </Button>
    </div>
  )
}
