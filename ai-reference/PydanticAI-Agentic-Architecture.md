# 🤖 PydanticAI Agentic Architecture — Best Practices & Examples

> **Last Updated: July 2026**

A curated reference guide to the best GitHub repositories and resources for building agentic architectures using PydanticAI — the Python agent framework built the Pydantic way.

---

## Table of Contents

1. [What is PydanticAI?](#1-what-is-pydanticai)
2. [Top GitHub Repositories & Resources](#2-top-github-repositories--resources)
3. [Key PydanticAI Architecture Patterns](#3-key-pydanticai-architecture-patterns)
4. [Core Components](#4-core-components)
5. [References & Further Reading](#5-references--further-reading)

---

## 1. What is PydanticAI?

PydanticAI is a Python agent framework designed to help you build **production-grade applications and workflows** with generative AI. It extends the Pydantic ecosystem to bring type safety, validation, and structured outputs to LLM-powered agents.

| Feature | Description |
|---|---|
| **Type Safety** | Full Pydantic validation on all LLM inputs and outputs |
| **Tool Decorators** | Simple Python decorators to expose functions as LLM tools |
| **Dependency Injection** | Clean dependency management for agent context |
| **Multi-Provider** | Supports OpenAI, Gemini, Anthropic, and more |
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
| **Structured Outputs** | Define Pydantic models as the agent's result type for validated responses |
| **Multi-step Workflows** | Chain tool calls and reasoning steps for complex task execution |
| **Provider Flexibility** | Swap LLM providers (OpenAI, Gemini, Claude) without changing agent logic |
| **Streaming Support** | Stream agent responses for real-time, token-by-token output |

---

## 4. Core Components

### 4.1 Agent Class

The central building block of any PydanticAI application.

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ResponseModel(BaseModel):
    answer: str
    confidence: float

agent = Agent(
    model="openai:gpt-4o",
    result_type=ResponseModel,
    system_prompt="You are a helpful research assistant."
)
```

---

### 4.2 Tool Decorators

Expose Python functions as tools the LLM can call during a run.

```python
from pydantic_ai import Agent, RunContext

agent = Agent(model="openai:gpt-4o")

@agent.tool
async def search_database(ctx: RunContext, query: str) -> str:
    """Search the internal database for relevant documents."""
    results = await ctx.deps.db.search(query)
    return results
```

---

### 4.3 Dependency Injection

Pass typed external dependencies (DB connections, API clients, config) into the agent.

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
```

---

### 4.4 Structured Response Validation

Guarantee the shape of every LLM response using Pydantic models.

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
    result_type=AnalysisResult
)

result = await agent.run("Analyze the latest market trends.")
print(result.data.summary)
print(result.data.key_points)
```

---

### 4.5 Multi-Agent (Agentic) Pattern

Compose multiple specialized agents for complex workflows.

```python
from pydantic_ai import Agent

# Specialized sub-agents
research_agent = Agent(model="openai:gpt-4o", system_prompt="You are a research specialist.")
analysis_agent = Agent(model="openai:gpt-4o", system_prompt="You are a data analyst.")
writer_agent   = Agent(model="openai:gpt-4o", system_prompt="You are a report writer.")

# Orchestrator
async def run_pipeline(topic: str):
    raw_data    = await research_agent.run(f"Research: {topic}")
    analysis    = await analysis_agent.run(f"Analyze: {raw_data.data}")
    final_report = await writer_agent.run(f"Write report from: {analysis.data}")
    return final_report.data
```

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
