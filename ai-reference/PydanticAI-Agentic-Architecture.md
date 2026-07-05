# 🤖 PydanticAI Agentic Architecture — Best Practices & Examples

> **Last Updated: July 2026**
>
> **Note:** Section 4 (Core Components) has been updated to reflect PydanticAI's current API naming (`output_type` / `result.output`, replacing the older `result_type` / `result.data`), plus additional concepts — message history, testing models, output validation, and multi-agent orchestration options. Always cross-check against [ai.pydantic.dev](https://ai.pydantic.dev/) for the exact API of the version you're pinning.

A curated reference guide to the best GitHub repositories and resources for building agentic architectures using PydanticAI — the Python agent framework built the Pydantic way.

---

## Table of Contents

1. [What is PydanticAI?](#1-what-is-pydanticai)
2. [Top GitHub Repositories & Resources](#2-top-github-repositories--resources)
3. [Key PydanticAI Architecture Patterns](#3-key-pydanticai-architecture-patterns)
4. [Core Components](#4-core-components)
   - [4.1 Agent Class](#41-agent-class)
   - [4.2 Tool Decorators](#42-tool-decorators)
   - [4.3 Dependency Injection](#43-dependency-injection)
   - [4.4 Structured Output & Validation](#44-structured-output--validation)
   - [4.5 Message History & Multi-Turn Conversations](#45-message-history--multi-turn-conversations)
   - [4.6 Streaming](#46-streaming)
   - [4.7 Testing Agents](#47-testing-agents)
   - [4.8 Multi-Agent (Agentic) Patterns](#48-multi-agent-agentic-patterns)
5. [References & Further Reading](#5-references--further-reading)

---

## 1. What is PydanticAI?

PydanticAI is a Python agent framework designed to help you build **production-grade applications and workflows** with generative AI. It extends the Pydantic ecosystem to bring type safety, validation, and structured outputs to LLM-powered agents.

| Feature | Description |
|---|---|
| **Type Safety** | Full Pydantic validation on all LLM inputs and outputs |
| **Tool Decorators** | Simple Python decorators to expose functions as LLM tools |
| **Dependency Injection** | Clean dependency management for agent context |
| **Multi-Provider** | Supports OpenAI, Anthropic (Claude), Gemini, Groq, Mistral, Cohere, and more |
| **Structured Outputs** | Guaranteed output shapes via Pydantic models |
| **Production-Ready** | Designed for real-world, multi-step agentic workflows |

---

## 2. Top GitHub Repositories & Resources

### 🥇 Official PydanticAI Repository

| | |
|---|---|
| **GitHub** | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) |
| **Description** | Official repository for PydanticAI — the production-grade AI agent framework |
| **Highlights** | Comprehensive `examples/` folder, tool integration, structured responses, multi-step agents |
| **Best For** | Canonical reference, production patterns, official API usage |

---

### 🥈 PydanticAI Agent Examples (Beginner-Friendly)

| | |
|---|---|
| **GitHub** | [hackrnd/pydanticai-agent-examples](https://github.com/hackrnd/pydanticai-agent-examples) |
| **Description** | Simplified, well-explained examples for getting started with PydanticAI |
| **Highlights** | Creating agents, handling dependencies, response validation, multi-provider support (OpenAI, Gemini) |
| **Best For** | Beginners, quick starts, understanding core primitives |

---

### 🥉 GenAI Agents — Comprehensive Patterns

| | |
|---|---|
| **GitHub** | [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) |
| **DeepWiki Guide** | [PydanticAI Architecture Deep Dive](https://deepwiki.com/NirDiamant/GenAI_Agents/2.2-pydanticai-architecture) |
| **Description** | Comprehensive guide to agent and workflow patterns with PydanticAI |
| **Highlights** | In-depth architecture breakdown, Agent class, Tools with decorators, Dependency Injection system, example notebooks |
| **Best For** | Intermediate to advanced users, architecture comparisons, notebook-based learning |

---

### 🌟 Real-World Document Processing Agent

| | |
|---|---|
| **Article + Code** | [Agentic AI Document Extraction with PydanticAI & Unstract](https://unstract.com/blog/building-real-world-ai-agents-with-pydanticai-and-unstract/) |
| **Description** | End-to-end real-world agent for automated document extraction and processing |
| **Highlights** | Natural language orchestration, Pandas data processing, output validation, PostgreSQL storage |
| **Best For** | Enterprise use cases, document automation, data pipeline integration |

---

### 📘 Official Documentation

| | |
|---|---|
| **Docs** | [ai.pydantic.dev](https://ai.pydantic.dev/) |
| **Overview** | [Pydantic AI Overview](https://pydantic.dev/docs/ai/overview/) |
| **Core Concepts** | [Agent Core Concepts](https://pydantic.dev/docs/ai/core-concepts/agent/) |
| **Best For** | Authoritative reference, minimal working examples, production best practices |

---

## 3. Key PydanticAI Architecture Patterns

These are the dominant patterns found across the best PydanticAI repositories:

| Pattern | Description |
|---|---|
| **Agent Definition** | Create agents using the `Agent` class with a model, system prompt, and tools |
| **Tool Decorators** | Expose Python functions as LLM-callable tools using `@agent.tool` |
| **Dependency Injection** | Pass typed context/dependencies into agents cleanly using `RunContext` |
| **Structured Outputs** | Define Pydantic models as the agent's `output_type` for validated responses |
| **Multi-step Workflows** | Chain tool calls and reasoning steps for complex task execution |
| **Provider Flexibility** | Swap LLM providers (OpenAI, Anthropic, Gemini, etc.) without changing agent logic |
| **Streaming Support** | Stream agent responses for real-time, token-by-token output |
| **Message History** | Carry conversation state across runs via `message_history` |
| **Testability** | Swap in `TestModel` / `FunctionModel` to unit-test agents without real API calls |

---

## 4. Core Components

### 4.1 Agent Class

The central building block of any PydanticAI application. The constructor takes the
model, the expected `output_type` (a Pydantic model, dataclass, or plain type), and
an optional system prompt.

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ResponseModel(BaseModel):
    answer: str
    confidence: float

agent = Agent(
    model="openai:gpt-4o",
    output_type=ResponseModel,
    system_prompt="You are a helpful research assistant."
)
```

> **Naming note:** Older PydanticAI code (and many tutorials) use `result_type=`
> instead of `output_type=`. Both may still appear in the wild — check the version
> pinned in your `pyproject.toml`/`requirements.txt` before copying an example.

---

### 4.2 Tool Decorators

Expose Python functions as tools the LLM can call during a run. Use `@agent.tool`
when the function needs the run context (dependencies, usage, etc.), or
`@agent.tool_plain` when it doesn't.

```python
from pydantic_ai import Agent, RunContext

agent = Agent(model="openai:gpt-4o")

@agent.tool
async def search_database(ctx: RunContext, query: str) -> str:
    """Search the internal database for relevant documents."""
    results = await ctx.deps.db.search(query)
    return results

@agent.tool_plain
def get_current_time() -> str:
    """Return the current UTC time — no dependencies needed."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
```

---

### 4.3 Dependency Injection

Pass typed external dependencies (DB connections, API clients, config) into the agent
via `deps_type`, and access them inside tools through `RunContext[DepsType].deps`.

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class AgentDeps:
    db_client: DatabaseClient
    api_key: str

agent = Agent(model="openai:gpt-4o", deps_type=AgentDeps)

@agent.tool
async def fetch_data(ctx: RunContext[AgentDeps], item_id: str) -> dict:
    return await ctx.deps.db_client.get(item_id)

result = await agent.run(
    "Look up item 42",
    deps=AgentDeps(db_client=my_db_client, api_key="...")
)
```

---

### 4.4 Structured Output & Validation

Guarantee the shape of every LLM response using Pydantic models as `output_type`.
The run result exposes the validated value through `.output` (the current name;
older code/tutorials use `.data`).

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class AnalysisResult(BaseModel):
    summary: str
    key_points: list[str]
    sentiment: str
    confidence_score: float

agent = Agent(
    model="openai:gpt-4o",
    output_type=AnalysisResult
)

result = await agent.run("Analyze the latest market trends.")
print(result.output.summary)
print(result.output.key_points)
```

For validation logic that can't be expressed in the Pydantic model alone (e.g.
cross-field checks, external lookups), register an output validator that can
raise a retryable error:

```python
from pydantic_ai import Agent, ModelRetry

agent = Agent(model="openai:gpt-4o", output_type=AnalysisResult)

@agent.output_validator
async def check_sentiment(ctx, output: AnalysisResult) -> AnalysisResult:
    if output.sentiment not in {"positive", "neutral", "negative"}:
        raise ModelRetry("sentiment must be positive, neutral, or negative")
    return output
```

---

### 4.5 Message History & Multi-Turn Conversations

Every run returns the full message exchange. Pass it back in on the next call to
continue a conversation without re-explaining context.

```python
result1 = await agent.run("What's the capital of France?")
result2 = await agent.run(
    "What's its population?",
    message_history=result1.new_messages()
)
```

`result.all_messages()` returns the complete history (including prior turns);
`result.new_messages()` returns only what this run added.

---

### 4.6 Streaming

Stream partial output as the model generates it, useful for chat UIs and long
responses.

```python
async with agent.run_stream("Write a short poem about the ocean.") as result:
    async for chunk in result.stream_text():
        print(chunk, end="", flush=True)
```

---

### 4.7 Testing Agents

Swap in `TestModel` (or a custom `FunctionModel`) so tests don't make real network
calls to an LLM provider.

```python
from pydantic_ai.models.test import TestModel

test_agent = agent.override(model=TestModel())

def test_agent_returns_structured_output():
    result = test_agent.run_sync("hello")
    assert isinstance(result.output, AnalysisResult)
```

---

### 4.8 Multi-Agent (Agentic) Patterns

PydanticAI documents a few distinct ways to compose multiple agents, in roughly
increasing order of complexity:

| Pattern | Description |
|---|---|
| **Agent delegation** | One agent calls another agent from inside a `@agent.tool`, treating the sub-agent as just another tool call |
| **Programmatic hand-off** | Application code decides which agent to invoke next based on the previous agent's output, rather than an agent calling another agent directly |
| **Graph-based control flow** | Complex, stateful, or branching workflows modeled explicitly with the companion **pydantic-graph** library |

**Simple orchestration example** (programmatic hand-off style — application code
drives the sequence):

```python
from pydantic_ai import Agent

research_agent = Agent(model="openai:gpt-4o", system_prompt="You are a research specialist.")
analysis_agent = Agent(model="openai:gpt-4o", system_prompt="You are a data analyst.")
writer_agent   = Agent(model="openai:gpt-4o", system_prompt="You are a report writer.")

async def run_pipeline(topic: str):
    raw_data     = await research_agent.run(f"Research: {topic}")
    analysis     = await analysis_agent.run(f"Analyze: {raw_data.output}")
    final_report = await writer_agent.run(f"Write report from: {analysis.output}")
    return final_report.output
```

For workflows with branching, retries, or long-running state, PydanticAI's sibling
project **pydantic-graph** lets you define each step as a typed node and the
transitions between them explicitly, instead of hand-writing the control flow.

---

## 5. References & Further Reading

| Resource | Link |
|---|---|
| Official PydanticAI Docs | [ai.pydantic.dev](https://ai.pydantic.dev/) |
| pydantic/pydantic-ai (GitHub) | [github.com/pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) |
| hackrnd/pydanticai-agent-examples | [github.com/hackrnd/pydanticai-agent-examples](https://github.com/hackrnd/pydanticai-agent-examples) |
| NirDiamant/GenAI_Agents | [github.com/NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) |
| GenAI_Agents PydanticAI DeepWiki | [deepwiki.com/NirDiamant/GenAI_Agents](https://deepwiki.com/NirDiamant/GenAI_Agents/2.2-pydanticai-architecture) |
| Agentic Document Extraction Article | [unstract.com/blog](https://unstract.com/blog/building-real-world-ai-agents-with-pydanticai-and-unstract/) |
| GitHub Topics: pydantic-ai | [github.com/topics/pydantic-ai](https://github.com/topics/pydantic-ai) |

---

*This document is intended as a living reference. Contributions and updates are welcome via pull request.*
