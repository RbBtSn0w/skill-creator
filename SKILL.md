---
name: skill-creator
description: Create, update, evaluate, and optimize AI agent skills. Synthesizes lean principles with robust evaluation loops for universal skill development.
---

# Unified Skill Creator

A universal skill for creating new agent skills, refining existing skills, and measuring skill performance. This workflow combines lean, principle-driven instruction design with robust, subagent-driven evaluation and description optimization loops.

## Core Principles

1. **Assume the Agent is Capable.** Include only information that changes decisions or improves work. Strip out generic advice, conversational filler, repetitive instructions, and speculative edge cases. Explain the *why* behind non-obvious rules rather than relying on oppressive MUSTs; modern models generalize better from rationale than arbitrary constraints.
2. **Preserve User Intent and Scope.** A skill must support the requested task without expanding its scope, replacing chosen tools, or modifying unrelated configuration. Never generalize an isolated failure into an absolute universal rule (avoid speculative generalization). Define clear stopping conditions proportional to risk.
3. **Match Specificity to Risk.** Give the agent room to choose appropriate approaches when multiple paths are valid. Reserve deterministic scripts, rigid sequences, and absolute language for operations where deviation leads to safety, security, data loss, or correctness failures.
4. **Keep Discovery Cheap and Precise.** Skill descriptions determine when a skill triggers during tool/skill routing. Make descriptions discriminating: state what the skill does and the specific contexts where it applies. Avoid bloated capability catalogs or broad catchall phrases that accidentally intercept unrelated user queries.
5. **Disclose Detail Progressively.** Organize skill content into three distinct tiers:
   - **Level 1 (Metadata):** Frontmatter `name` and `description` (always in context for routing; keep concise).
   - **Level 2 (SKILL.md body):** Shared purpose, core constraints, workflow steps, and routing links (loaded when triggered; keep under 500 lines).
   - **Level 3 (Supporting resources):** Detailed schemas, mode-specific reference guides, scripts, and asset templates (loaded or executed on demand).

## Anatomy of a Skill

```text
skill-name/
├── SKILL.md                 # Required: YAML frontmatter + core markdown instructions
├── scripts/                 # Optional: Executable helpers for deterministic tasks
├── references/              # Optional: Documentation, schemas, and domain knowledge
└── assets/                  # Optional: Output templates, icons, sample data
```

### Component Roles
- **`SKILL.md` (Required):** The single entry point loaded into context when the skill triggers. Contains frontmatter, high-level guidance, critical invariants, and reference links.
- **`scripts/` (Optional):** Executable code (e.g., Python, Bash) for deterministic transformations, heavy parsing, or complex API calls. Scripts run via shell; their source code is not loaded into prompt context unless actively debugging.
- **`references/` (Optional):** On-demand documentation files (e.g., schemas, format specifications, platform guides). Loaded into context only when referenced via markdown links.
- **`assets/` (Optional):** Static artifacts (templates, boilerplate code, images) copied or adapted into output deliverables. Assets are never directly injected into agent context.

### Progressive Disclosure in Practice

Structure complex skills with mode-specific references rather than inlining everything into `SKILL.md`:

```text
cloud-deploy/
├── SKILL.md                 # Workflow router and shared deployment safety checks
└── references/
    ├── aws.md               # AWS ECS/Lambda deployment steps and parameters
    ├── gcp.md               # GCP Cloud Run deployment steps and parameters
    └── azure.md             # Azure Container Apps deployment steps and parameters
```

In `SKILL.md`, route the agent conditionally:
```markdown
## Deployment Providers
- When deploying to AWS, read [references/aws.md](references/aws.md).
- When deploying to GCP, read [references/gcp.md](references/gcp.md).
- When deploying to Azure, read [references/azure.md](references/azure.md).
```

A short skill can route to details only when an advanced operation demands them:
```markdown
## Document Operations
Handle ordinary text edits directly.
- For tracked changes, read [references/redlining.md](references/redlining.md).
- For document internals and packaging, read [references/ooxml.md](references/ooxml.md).
```

Only create supporting resources when their concrete benefit justifies them:
- Repeated complex transforms justify a script (e.g., `scripts/rotate_pdf.py`).
- Domain-specific structures justify a reference (e.g., `references/schema.md`).
- Project scaffolds or templates justify an asset (e.g., `assets/frontend-template/`).

### What NOT to Include & Anti-Patterns
- **No Auxiliary Documentation:** Do NOT create `README.md`, installation guides, changelogs, or auxiliary tutorials inside the skill directory. The skill is an agent instruction set, not a software project.
- **No Empty Boilerplate:** Do NOT leave empty folders, stub files, or unused `[TODO: ...]` placeholders.
- **No Over-Constraining:** Avoid rigid step-by-step algorithms when the agent could solve the task flexibly.
- **No Catchall Descriptions:** Avoid phrases like "Handles all developer tasks" or "Use for anything related to coding".
- **No Fragile Assertions:** Avoid testing skills by matching exact wording, formatting whitespace, or markdown headings. Verify observable invariants (created files, exit codes, parsed AST, valid schema outputs).

## Writing Patterns & Templates

### 1. Output Format Template
When an agent's output must adhere to a strict structure, define it with a fenced template block:
```markdown
## Deliverable Format
Generate the audit report using this exact structure:
# Security Audit: [Target System]
## Executive Summary
[High-level risk posture and critical findings]
## Vulnerability Matrix
| ID | Severity | Component | Description | Remediation |
|---|---|---|---|---|
## Actionable Next Steps
```

### 2. Input / Output Examples Pattern
Demonstrate transformations with concrete before/after pairs:
```markdown
## Commit Message Generation
**Example 1:**
Input: Added token validation middleware to protect /api/v1/user endpoints
Output: feat(auth): validate JWT tokens on user endpoints
```

## Creating or Updating a Skill

### Step 1: Capture Intent & Design
Identify the user's core requirements:
- What should this skill enable the agent to do?
- When should it trigger? (key trigger phrases and operational contexts)
- What is the expected output structure and format?
- What are the safety, permission, or correctness invariants?
- *Tip: Inspect conversation history to observe real user workflows and error recovery patterns.*

### Step 2: Initialize and Author Instructions
Use the bootstrapping script to scaffold the skill directory:
```bash
python scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets]
```
Author `SKILL.md`:
- **`name`**: Action-oriented, lowercase alphanumeric with hyphens (`^[a-z0-9-]+$`, max 64 chars).
- **`description`**: Pushy but precise. Combine what it does with explicit trigger triggers:
  *Weak:* "Create deployment pipelines."
  *Strong:* "Configure and deploy CI/CD pipelines. Use whenever the user mentions setting up automated builds, release workflows, or pipeline configs."
- **Body**: Use imperative tone, structured headings, explicit output templates, and clear input/output examples.

### Step 3: Validate and Iterate

Select the validation tier based on skill complexity:

#### Tier A: Quick Validation (Simple or low-risk skills)
1. **Static Validation:** Run `python scripts/quick_validate.py <path/to/skill>` to verify frontmatter schema, naming constraints, and ensure no lingering `[TODO: ...]` placeholders remain.
2. **Blind Forward-Testing:** Spawn an independent subagent to execute a realistic task using the skill:
   - Provide only: the realistic user prompt, the skill path, and raw input files.
   - Strictly withhold: expected outputs, suspected failure modes, or proposed fixes.
   - Isolate execution: run in a dedicated temporary workspace.
   - Authorization gates: confirm with the user before executing external API mutations or fee-incurring tasks.
3. **Inspect Output & Refine:** Review the generated deliverables and adjust instructions where needed.

#### Tier B: Rigorous Evaluation Loop (Complex, high-risk, or multi-step skills)
Follow the systematic benchmark workflow:
```text
<skill-name>-workspace/
└── iteration-1/
    ├── eval-1/
    │   ├── with_skill/outputs/      # New skill outputs
    │   ├── baseline/outputs/        # Control group outputs (without_skill or old_skill)
    │   └── eval_metadata.json       # Prompt and assertions
    ├── benchmark.json               # Aggregated metrics (pass rates, tokens, time)
    └── feedback.json                # User review feedback
```

1. **Define Test Cases:** Author 2–3 realistic test cases in `evals/evals.json` using the schema in `references/schemas.md`.
2. **Snapshot Existing Skills:** When modifying an existing skill, snapshot the current version before editing:
   ```bash
   cp -r <skill-path> <workspace>/skill-snapshot/
   ```
3. **Spawn All Runs Concurrently:** Launch subagents for all test cases—both `with_skill` and control group (`without_skill` for greenfield, `old_skill` snapshot for updates)—in the **same turn**. Concurrent execution ensures consistent testing conditions and minimal iteration latency.
4. **Draft Assertions During Execution:** While subagent runs are in progress, draft objective, quantitative assertions checking observable outcomes. For complex textual or semantic outputs, use `agents/grader.md`.
5. **Capture Ephemeral Timing Data:** Task completion notifications contain ephemeral metrics (`total_tokens`, `duration_ms`). Immediately record these into each run's `timing.json` upon completion (this data cannot be recovered after the turn).
6. **Grade, Aggregate, and Analyze:**
   - Execute grading against assertions. Ensure `grading.json` expectations array strictly uses the fields `text`, `passed`, and `evidence` (the review viewer requires these exact keys).
   - Aggregate statistics:
     ```bash
     python scripts/aggregate_benchmark.py <workspace>/iteration-<N> --skill-name <name>
     ```
   - Diagnose anomalies with `agents/analyzer.md` (flag non-discriminating assertions, high variance, or token bloat).
   - For blind quality evaluation, adjudicate outputs with `agents/comparator.md`.
7. **Launch Reviewer & Incorporate Feedback:**
   - Start local review server:
     ```bash
     python scripts/generate_review.py <workspace>/iteration-<N> --skill-name "<name>" --benchmark <workspace>/iteration-<N>/benchmark.json
     ```
     *(For iteration 2+, pass `--previous-workspace <workspace>/iteration-<N-1>` to view historical diffs. In headless or CI environments, pass `--static /tmp/review.html` to export a standalone HTML artifact).*
   - The user reviews outputs and formal grades in the browser and submits. Read `<workspace>/feedback.json`, generalize findings, keep instructions lean, and iterate into `iteration-<N+1>/`.

#### Practical Evaluation Guidelines
- **Single-Agent Fallback:** When running in environments without subagents, execute test cases sequentially in-session. Skip quantitative baselines and focus on direct qualitative inspection of output files with the user.
- **Mine Transcripts for Reusable Scripts:** Inspect execution transcripts across test runs. If subagents independently write similar ad-hoc scripts (e.g., `create_docx.py` or `extract_table.py`), extract and bundle them directly into `scripts/` to prevent future invocations from reinventing the wheel.
- **Preserve Identity on Updates:** When modifying an existing skill, maintain the canonical `name` and directory path (do not append `-v2`). If the installed skill resides in a read-only location, copy it to `/tmp/<skill-name>/` to edit, test, and package.

### Step 4: Description Optimization (Advanced)
A skill's description controls whether an agent selects it during tool routing. To systematically maximize triggering accuracy:
1. **Curate Trigger Evaluation Set:** Prepare ~20 realistic user queries:
   - 8–10 **Positive queries** (should trigger the skill across varying phrasing).
   - 8–10 **Challenging near-miss negative queries** (adjacent domains or related tools that should NOT trigger this skill, e.g. querying Docker container status vs editing a Dockerfile). *Do not use trivially irrelevant queries like "tell a joke".*
   - *Query Quality:* Avoid abstract queries like `"Format this data"` or `"Extract text from PDF"`. Author rich queries with natural language, file paths, and context: e.g., `"My manager just sent me ~/Downloads/Q4_sales_final.xlsx and wants a profit margin column added based on revenue in Col C and costs in Col D"`.
2. **Review Query Set:** Present queries for inspection using the `assets/eval_review.html` template:
   - Read `assets/eval_review.html` and replace placeholders:
     - `__EVAL_DATA_PLACEHOLDER__` → JSON array of eval queries (raw JS variable assignment, unquoted).
     - `__SKILL_NAME_PLACEHOLDER__` → Skill name.
     - `__SKILL_DESCRIPTION_PLACEHOLDER__` → Current description.
   - Save to `/tmp/eval_review_<skill-name>.html` and open it. The user can toggle polarities, tweak phrasing, add/remove queries, and export to `~/Downloads/eval_set.json`.
3. **Run Optimization Loop:** Execute the automated optimizer:
   ```bash
   python scripts/run_loop.py --eval-set <path-to-eval-set.json> --skill-path <path-to-skill> --model <model-name> --max-iterations 5
   ```
   - **Anti-Overfitting Design:** The loop performs a 60/40 stratified train/test split. History provided to the description generator blinds held-out test scores.
   - **Selection:** The optimizer selects the `best_description` based on the held-out test set score rather than the training score.
4. **Apply Result:** Write the winning description back into `SKILL.md` frontmatter.

### Step 5: Package and Distribute
Once validated, package the skill into a portable `.skill` archive:
```bash
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```
The packaging script validates the skill structure, verifies frontmatter, and strips VCS history, caches, and test artifacts (`evals/`, `tests/`, `.skills_staging/`). Custom exclusions can be passed via `--exclude` or the `SKILL_PACKAGE_EXCLUDE` environment variable.
