from pydantic import BaseModel
from pydantic_ai import Agent

# ---------- Stage 1: Extraction ----------

class ExtractedRequirements(BaseModel):
    problem_statement: str
    goals: list[str]
    target_users: list[str]
    open_questions: list[str]

agent = Agent(
    'anthropic:claude-sonnet-5',
    output_type=ExtractedRequirements,
    system_prompt=(
        "You extract structured product requirements from raw notes. "
        "Only include information present in the notes. "
        "Flag anything ambiguous as an open question rather than guessing."
    ),
)

# ---------- Stage 2: Generation ----------

class UserStory(BaseModel):
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: list[str]

class GeneratedPRD(BaseModel):
    title: str
    problem_statement: str
    goals: list[str]
    user_stories: list[UserStory]
    success_metrics: list[str]
    assumptions: list[str]

generation_agent = Agent(
    'anthropic:claude-sonnet-5',
    output_type=GeneratedPRD,
    system_prompt=(
        "You are a senior PM writing a PRD. Given extracted requirements, "
        "generate user stories following INVEST principles (Independent, "
        "Negotiable, Valuable, Estimable, Small, Testable). Each story needs "
        "clear, testable acceptance criteria. Do not invent goals not implied "
        "by the input."
    ),
)

# ---------- Chaining ----------

def generate_prd(raw_notes: str) -> GeneratedPRD:
    extraction_result = agent.run_sync(raw_notes)
    extracted = extraction_result.output

    prompt = f"""
    Problem: {extracted.problem_statement}
    Goals: {extracted.goals}
    Target users: {extracted.target_users}
    Open questions to keep in mind: {extracted.open_questions}
    """
    generation_result = generation_agent.run_sync(prompt)
    return generation_result.output


@agent.tool
async def get_project_glossary(ctx, project_key: str) -> str:
    """Fetch existing product terminology for a project."""
    return "Terms: 'export' means download-only, not email delivery."


def regenerate_user_stories(extracted: ExtractedRequirements) -> list[UserStory]:
    result = generation_agent.run_sync(
        f"Regenerate only user stories for: {extracted.problem_statement}"
    )
    return result.output.user_stories
