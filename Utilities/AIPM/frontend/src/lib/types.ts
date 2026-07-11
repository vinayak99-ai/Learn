export interface ProjectMeta {
  id: string
  name: string
  created_at: string
  updated_at: string
}

export interface UserStory {
  as_a: string
  i_want: string
  so_that: string
  acceptance_criteria: string[]
}

export interface GeneratedPRD {
  title: string
  problem_statement: string
  goals: string[]
  user_stories: UserStory[]
  success_metrics: string[]
  assumptions: string[]
}

export interface GenerateResponse {
  artifact_id: string
  prd: GeneratedPRD
}

export type ExportFormat = "md" | "docx" | "csv"
