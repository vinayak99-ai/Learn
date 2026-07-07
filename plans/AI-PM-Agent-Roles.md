# AI PM Portal — Agent Roles (High Level)

A plain-language summary of what each agent does, for a first pass. No technical detail (inputs/outputs/schemas) — see `AI-PM.md` §8 for the full spec behind each one.

There are **8 core agents**, each named for the product-management job it stands in for, plus a **9th agent held for later adoption** rather than built alongside the first 8.

---

## The 8 Core Agents

### 1. Analysis Agent
Reads whatever the PM gives it — a first product description, later a pasted set of meeting notes — and figures out what's already clear versus what still needs to be asked before anything gets written. This is the system's "listener": it doesn't write documentation itself, it decides whether there's enough to write from.

### 2. Documentation Agent
Owns the actual written product and feature documents. It drafts the first version from what the PM has said, rewrites specific sections when asked, and checks its own work is complete enough to move forward. This is the system's primary "writer."

### 3. Persona Agent
Keeps track of who the users actually are, as its own reusable definition instead of something re-typed inside every document. Other documents reference a persona rather than re-describing the same users each time.

### 4. Structuring Agent
Takes one finished product document and breaks it down into a real hierarchy: candidate features, then candidate sub-features underneath each one. The PM reviews and confirms what actually gets created.

### 5. Architecture Decision Agent
Acts as the technical-feasibility checkpoint. Before a feature moves toward being built, this agent gives a feasibility read — risks, dependencies, open technical questions — so nothing moves forward that's obviously going to hit a wall.

### 6. Planning & Delivery Agent
Everything from "approved" to "in the tools the team actually works in." It turns an approved feature into a real implementation plan, generates what engineering needs (user stories, test plans), and publishes the finished work out to Jira and Confluence.

### 7. Prioritization Agent
Looks across the backlog and proposes an order — what to build first — using whatever signal is available (risk, scope, PM input).

### 8. Communication Agent
Keeps everyone outside the core loop informed: rolls current status up into a roadmap view, and drafts status updates tailored to whoever's asking — engineering, leadership, or customers.

---

## The 9th Agent (Later Adoption)

### 9. Domain Knowledge Agent
Not part of the first 8, and not treated as equal to them — this one is explicitly deferred. Its job would be to ground the other agents in knowledge specific to the organization (past decisions, internal systems, internal terminology) that an LLM has no way of knowing on its own. It only gets adopted once there's a real knowledge base to connect it to; until then, the Structuring and Architecture Decision agents work from general knowledge alone.

---

## What's Actually Being Built First

Only two of the above are in the MVP: the **Analysis Agent** (asking clarifying questions) and the **Documentation Agent** (drafting the product document). Everything else on this page is roadmap, not current scope.
