# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repository.

## What this repository is

`Learn` is a personal knowledge-base and scratch-work repo, not a shippable
application. It's a mix of:

- **Long-form Markdown notes/guides** on disparate topics the owner is
  studying (blockchain, LLM/agent architectures, PDF generation, personal
  philosophy).
- **Educational quiz content** for school-grade subjects (English, Math,
  Kannada) in Markdown and (historically) CSV form.
- **A handful of standalone Python scripts** (image resizing for PDFs, quiz
  rebalancing).
- **One small illustrative Python package**, `llm_research_platform/`, whose
  agent classes are demonstrations/specs, not production or tested code.

There is no single "app" to build or run, no test suite, no linter config,
and no CI pipeline. Treat most of the repo as documentation content rather
than source code — when in doubt, ask what the user actually wants edited
before assuming standard "software project" conventions apply.

## Directory map

```
.
├── README.md                      # Root index/TOC linking to many of the docs below
├── docs/                          # Spec for a (currently unbuilt) "Comprehension
│   │                               # Reading and Quiz Application" (Dash + FastAPI + SQL)
│   ├── README.md                  # Doc suite overview / quick-start guide
│   ├── ARCHITECTURE.md            # System architecture + Mermaid diagrams
│   ├── DATABASE_SCHEMA.md         # ER diagrams, SQLAlchemy models, migrations
│   ├── API_DESIGN.md              # REST endpoint specs, Pydantic models
│   └── commands.md                # Generic git workflow cheat-sheet
│
├── llm_research_platform/         # Illustrative Python package (agent stubs)
│   ├── __init__.py                # Re-exports all 14 agents
│   ├── agents/                    # One file per "feature agent" (see below)
│   ├── models/__init__.py         # Shared dataclasses (Document, Metric, ...)
│   └── utils/__init__.py          # Shared helpers (API key lookup, math utils)
├── examples_llm_platform.py       # Runnable usage examples for the agents above
│
├── langchain_pdf_image_resizer.py       # Standalone CLI: resize images for PDF layout
├── langchain_image_preprocessor/        # Related pipeline: JSON-driven image
│   ├── preprocessing_pipeline.py        #   download → resize → annotate JSON
│   ├── sample_input.json / optimized_output.json
│   └── processed_images/                # Generated output (gitignored)
│
├── rebalance_quiz.py               # CLI to rebalance answer-letter distribution
│                                    # in a quiz CSV (quiz-format.csv — see note below)
│
├── kannada/                        # Kannada-language learning material
│   ├── Kannada_Grammar_Grade5_NCERT.md
│   └── ollama.rar                  # Large binary archive (not source code)
│
├── *.md (root)                     # Independent long-form docs, e.g.:
│   ├── DAP_Agile_plan.md, DAP_Prod_Reqs.md         — "Digital Asset Research
│   │                                                  Platform" product docs
│   ├── LLM_Use_Cases_Research_Platform.md,
│   │   LLM_Research_Enhancements.md,
│   │   LLM_PLATFORM_README.md                      — specs for llm_research_platform
│   ├── Blockchain_Grading_Framework.md,
│   │   DeFi-Protocol-Grading-Framework.md,
│   │   Ethereum_Blockchain_Overview.md,
│   │   Plume_Blockchain_Overview.md                — blockchain research notes
│   ├── Aspose_PDF_Dynamic_Generation_Guide.md,
│   │   LangChain_Image_Resizing_PDF_Workflow.md     — PDF-generation guides
│   ├── *Quiz*.md, grade6-/grade7-comprehensive-quiz.md — school quiz content
│   ├── Life_Philosophy_Five_Pillars.md, drivers_of_life.md — personal essays
│   └── QUIZ_ANALYSIS.md, QUIZ_IMPROVEMENT_SUGGESTIONS.md,
│       SUMMARY.md, IMPLEMENTATION_SUMMARY.md,
│       FINAL_VALIDATION.txt                        — write-ups from past
│                                                      analysis/implementation tasks
└── requirements.txt                 # Union of deps for every Python script/package here
```

## Content categories, in more detail

### 1. `llm_research_platform/` — the closest thing to "real code" here

A package of 14 illustrative agent classes (`SemanticSearchAgent`,
`HypothesisAgent`, `GapFinderAgent`, `RecommendationAgent`,
`ReportGenerationAgent`, `AlertAgent`, `CrossDomainAgent`,
`ForecastingAgent`, `PeerReviewAgent`, `VisualizationAgent`,
`ReportAutomationAgent`, `ExperimentationAgent`, `SentimentAnalysisAgent`,
`ComparativeAnalysisAgent`), built to accompany the design docs
`LLM_Research_Enhancements.md` / `LLM_PLATFORM_README.md` /
`LLM_Use_Cases_Research_Platform.md`. It underpins a fictional "Digital Asset
Research Platform" (DAP) described in `DAP_Agile_plan.md` and
`DAP_Prod_Reqs.md`.

Conventions used throughout this package:
- Every module starts with a module-level docstring explaining the agent's
  purpose.
- Classes use full docstrings including an `Example:` block with a `>>>`
  doctest-style snippet.
- Shared data models live in `models/__init__.py` as `@dataclass`; shared
  helpers live in `utils/__init__.py`. New agents should reuse these rather
  than redefining similar structures.
- `agents/__init__.py` and the top-level `__init__.py` both re-export every
  agent class and keep `__all__` in sync — update both when adding an agent.
- There is **no test suite** for this package. `examples_llm_platform.py` is
  the de facto smoke test — it's meant to be run directly
  (`python3 examples_llm_platform.py`) and prints example output for manual
  inspection.
- The agents are demonstrations/prototypes: several call out to LLM
  providers (OpenAI/Claude/Gemini) conceptually but don't ship real API
  wiring. Don't assume production-hardening (retries, auth, rate limiting)
  is present unless you see it in the specific file.

### 2. Standalone scripts

- **`langchain_pdf_image_resizer.py`** and
  **`langchain_image_preprocessor/preprocessing_pipeline.py`** are two
  independent (overlapping-purpose) implementations of "resize images so
  they fit cleanly into a generated PDF." Read `LangChain_Image_Resizing_PDF_Workflow.md`
  and `langchain_image_preprocessor/README.md` respectively before changing
  either — they document expected JSON input/output shapes.
- **`rebalance_quiz.py`** shuffles multiple-choice options in a quiz CSV so
  correct-answer letters are evenly distributed (fixes tools built during a
  past task documented in `SUMMARY.md`, `QUIZ_ANALYSIS.md`, and
  `QUIZ_IMPROVEMENT_SUGGESTIONS.md`).
  - **Note:** the `quiz-format.csv` file these docs/scripts reference is
    **not currently present in the repo**. If asked to run or extend this
    tooling, check whether the CSV exists first rather than assuming it does.
  - Scripts default to a `dry_run=True` / preview mode and require an
    explicit `--apply` (or `dry_run=False`) flag to write output — preserve
    that safety pattern in any similar tooling you add.

### 3. Documentation content (the majority of the repo)

Most files are long, self-contained Markdown guides/specs, not code. When
editing or extending them:
- Match the existing structure: a numbered Table of Contents near the top,
  `##`/`###` section headers, and heavy use of Mermaid diagrams and Markdown
  tables (see `docs/ARCHITECTURE.md`, `docs/DATABASE_SCHEMA.md` for the
  house style).
- `README.md` is the root index — if you add a substantial new top-level doc,
  add a corresponding entry to its Table of Contents and a short summary
  section, following the pattern already used there.
- `docs/` specifically documents a **proposed, unbuilt** application (Python
  Dash frontend + FastAPI backend + PostgreSQL/SQLite). There is no
  corresponding implementation in this repo — don't assume the described
  API/DB actually exists in code.
- Quiz Markdown files (`Math_Quiz_Grade7.md`, `English_Grammar_Quiz_Grade7.md`,
  `grade6-comprehensive-quiz.md`, etc.) are graded educational content for
  specific school grades — preserve difficulty level and answer-key
  formatting conventions already present when editing.

### 4. `kannada/ollama.rar`

A large (~9 MB) pre-existing binary archive. Don't attempt to read/extract
it as part of routine work; leave it untouched unless explicitly asked.

## Dependencies

`requirements.txt` is a single flat file covering *all* Python
scripts/packages in the repo cumulatively (LangChain/OpenAI, image
processing, the LLM research platform's NLP/ML/forecasting/viz stack,
FastAPI/Pydantic for the proposed `docs/` app, etc.). There's no per-component
`requirements.txt` or virtual-env setup script — if you add a new Python
dependency, append it to this file under the relevant existing comment
section rather than creating a new manifest.

There is no `setup.py`/`pyproject.toml` — scripts and the
`llm_research_platform` package are used directly via `python3 <script>.py`
or by importing from the repo root, not installed.

## Git / PR workflow

- `docs/commands.md` documents the git conventions in use: branch prefixes
  (`feature/`, `bugfix/`, `hotfix/`, `release/`, `docs/`) and Conventional
  Commit-style messages (`feat:`, `fix:`, `docs:`, `refactor:`, `style:`,
  `test:`).
- History shows most changes land via PRs (including several opened by
  automated Copilot/agent sessions — see `git log`), each typically adding
  or updating one focused Markdown doc or tool at a time. Keep changes
  similarly scoped: one topic/tool per PR rather than sweeping edits across
  unrelated docs.

## Practical notes for AI assistants

- **No build/test/lint commands exist.** Don't invent or assume a `make
  test`, `npm run lint`, etc. — there's nothing to run. If you change a
  Python script, the appropriate verification is running it directly
  (e.g. `python3 rebalance_quiz.py`, `python3 examples_llm_platform.py`)
  and inspecting output.
- **Prefer editing existing docs over creating new ones** for a given topic;
  many topics already have a dedicated file (check the root listing and
  `README.md`'s TOC before adding a new Markdown file).
- **Don't conflate the `docs/` app spec with the `llm_research_platform`
  package** — they're unrelated fictional/prototype systems living in the
  same repo (a reading-comprehension quiz app vs. a crypto research
  platform's LLM agents).
- File names in this repo are inconsistently cased (`snake_case.py`,
  `PascalCase_With_Underscores.md`, `kebab-case.md`) — match the convention
  of the specific file/folder you're editing rather than normalizing it
  repo-wide.
