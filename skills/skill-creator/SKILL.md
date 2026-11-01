---
name: skill-creator
description: Create, update, evaluate, and optimize AI agent skills. Synthesizes lean principles with robust evaluation loops for universal skill development.
---

# Unified Skill Creator

A universal skill for creating new agent skills, refining existing skills, and measuring skill performance. Use focused edits for maintenance and evaluation when the changed behavior warrants it.

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
- **`SKILL.md` (Required):** YAML frontmatter with `name` and `description`, followed by complete task instructions. The name matches its directory and uses lowercase letters, digits, and single hyphens, up to 64 characters. The description states what the skill does and when it applies. The body defines required inputs, the intended output, the workflow and decision points, and relevant correctness or permission boundaries. Preserve supported optional frontmatter on updates.
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

## Create or Update

### Create a new skill

For a new skill, identify its task, trigger boundaries, outputs, and correctness or permission
constraints from realistic requests. Clarify missing information only when it changes the
scope or design. Initialize only the resources it needs:

```bash
python scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets]
```

Complete the generated frontmatter and task instructions before validation. Replace or remove
scaffold placeholders and unused examples. Implement required helpers and supply actual
reference or asset content; link supporting resources with clear conditions for using them.
An initialized template is not a finished skill.

### Update an existing skill

For an existing skill, read its current instructions and affected references, scripts, callers,
and tests before editing. Preserve its canonical name, directory, and supported interfaces;
do not reinitialize it. Prefer the source repository over an installed copy. If the source is
unavailable or read-only, use an isolated copy and identify it clearly at delivery.

Locate the decision that needs to change and edit it in place. Replace conflicting guidance,
delete unsupported paths and redundant explanations, and update affected references together.
Add a rule only for a demonstrated, reusable gap; a transient failure may require no skill edit.
Do not preserve obsolete instructions by appending exceptions or override sections.

Keep supported compatibility paths and safety or authorization boundaries explicit. Check
callers before removing resources or contracts. Move substantial conditional detail into a
reference with a clear reading condition; keep essential boundaries in the entrypoint. Record
historical rationale in the change review or version history, rather than the execution guide.
Judge edits by useful decisions retained, not by a target line count or a mandatory history log.

### Validate the result

Check that the skill meets the `SKILL.md` contract above and that its resource links resolve.
Choose behavioral checks for the work performed, rather than the size of the whole skill:

| Work | Appropriate checks |
| --- | --- |
| New skill | Exercise a representative request from inputs to the requested deliverable, and check a nearby request outside its scope. |
| Wording, links, equivalent deduplication | Review the diff, references, and structure. |
| Local behavior or routing | Add the relevant failure case, normal path, and adjacent negative case. |
| New or changed executable helpers | Execute representative valid and failure inputs; verify the actual output and failure behavior. |
| Workflow or high-impact boundaries | Run affected regressions; compare the old version when needed and verify allowed, denied, and failure paths. |

Run the existing structural validator; it does not prove behavioral improvement:

```bash
python scripts/quick_validate.py <path/to/skill>
```

Reuse evidence for unchanged components. Independent execution is useful when it resolves a
behavioral uncertainty; it is not required for every small update. Keep cases local and bounded
unless external actions are already authorized. When a case fails, repair the relevant guidance
and rerun affected checks; expand evaluation only for a new failure or unresolved risk.

For multi-case comparisons or description optimization, read
[references/evaluation.md](references/evaluation.md). A single executor can run old and new
versions sequentially in separate workspaces; report limitations of shared context.

### Deliver

Finish when current guidance and references agree, the relevant checks pass, and remaining
limitations are stated. Report what changed, which checks ran, and what remains unverified.
Do not add an evaluation project or distribution step solely to complete a routine update.

Only package when distribution is requested:

```bash
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

The packager validates structure and excludes VCS history, caches, and test artifacts. Preserve
its existing `--exclude` and `SKILL_PACKAGE_EXCLUDE` options when custom exclusions are needed.
