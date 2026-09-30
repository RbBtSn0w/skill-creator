# Skill Creator

<p align="center">
  <img src="skills/skill-creator/assets/skill-creator-small.svg" alt="Skill Creator Logo" width="96" height="96" />
</p>

<p align="center">
  <strong>Universal, platform-neutral AI agent skill creator, evaluator, and description optimizer.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache 2.0" /></a>
  <a href="skills/skill-creator/SKILL.md"><img src="https://img.shields.io/badge/Standard-Universal_Skill_Spec-green.svg" alt="Standard: Universal Skill Spec" /></a>
</p>

---

## Overview

**Skill Creator** is a comprehensive, vendor-agnostic framework for building, testing, refining, and packaging AI agent skills. Synthesizing lean instruction design with robust subagent evaluation loops, it ensures skills trigger with high precision, provide non-obvious guidance, and avoid over-constraining models.

### Key Capabilities

- **Lean Scaffolding (`init_skill.py`):** Bootstrap standard skills with appropriate resource structures (`scripts/`, `references/`, `assets/`).
- **Static Schema & Quality Linter (`quick_validate.py`):** Catch unescaped placeholders, regex naming violations, and schema anomalies before deployment.
- **Dual-Tier Validation Workflow:**
  - **Tier A (Fast):** Subagent blind forward-testing in isolated scratchpads.
  - **Tier B (Rigorous):** Concurrent with-skill vs. baseline benchmarking, assertion grading, and browser-based qualitative review (`generate_review.py`).
- **Trigger Rate Optimization Loop (`run_loop.py`):** Automatically refine frontmatter descriptions using stratified train/test query sets with blinded history to prevent overfitting.
- **Clean Packaging (`package_skill.py`):** Bundle production-ready `.skill` zip archives with automated exclusion of VCS, test artifacts, and caches.

---

## Installation

### Recommended: Via `adg skills`

The recommended way to install and manage `skill-creator` across your local projects and agents is using `adg skills`:

```bash
# Install to the current project
adg skills add RbBtSn0w/skill-creator

# Install globally across all supported agents
adg skills add RbBtSn0w/skill-creator -g

# Install globally and automatically apply to all agents without prompt
adg skills add RbBtSn0w/skill-creator --all
```

### Alternative: Via `skills` CLI / `npx`

You can also install via the standard `skills` package manager:

```bash
npx skills add RbBtSn0w/skill-creator -g
```

### Manual Installation

Clone the repository directly into your agent's skills directory:

```bash
git clone https://github.com/RbBtSn0w/skill-creator.git
```

---

## Standard Skill Architecture

Every skill managed or produced by `skill-creator` strictly adheres to the 4-part modular anatomy:

```text
skill-name/
├── SKILL.md                 # Required: Entrypoint containing YAML frontmatter + core guidance
├── scripts/                 # Optional: Deterministic code executed directly via shell
├── references/              # Optional: On-demand documentation, schemas, and subagent rubrics
└── assets/                  # Optional: Templates, starter code, and visual assets
```

### Progressive Disclosure

- **Level 1 (Metadata):** `name` and `description` in YAML frontmatter. Always resident in context for skill routing.
- **Level 2 (SKILL.md body):** Core constraints, workflow routing, and deliverable format templates. Loaded only when the skill triggers (kept under 500 lines).
- **Level 3 (Supporting Resources):** In-depth guides (`references/`), specialized scripts (`scripts/`), and templates (`assets/`). Read or executed on demand.

### Repository Layout

For skills containing supporting resources, `skill-creator` follows the standard nested sub-directory layout under `skills/`:

```text
skill-creator/
├── README.md
├── LICENSE
└── skills/
    └── skill-creator/
        ├── SKILL.md
        ├── assets/
        ├── references/
        └── scripts/
```

When installed via package managers (such as `adg skills add https://github.com/RbBtSn0w/skill-creator -g`), subdirectories under `skills/` are automatically detected, triggering a recursive installation of the entire directory (`skill.path` resolves to `tempDir/skills/skill-creator`).

---

## Quick Start

### 1. Initialize a New Skill

```bash
python skills/skill-creator/scripts/init_skill.py my-helper --path skills/ --resources scripts,references,assets --examples
```

### 2. Validate Skill Structure

```bash
python skills/skill-creator/scripts/quick_validate.py skills/my-helper
```

### 3. Run Benchmark Evaluation (Tier B)

1. Author test cases in `evals/evals.json` using the schema defined in `skills/skill-creator/references/schemas.md`.
2. Spawn concurrent with-skill and baseline runs into `<workspace>/iteration-1/`.
3. Grade runs and aggregate statistical benchmarks:
   ```bash
   python skills/skill-creator/scripts/aggregate_benchmark.py <workspace>/iteration-1 --skill-name "my-helper"
   ```
4. Review results and leave feedback using the visual reviewer:
   ```bash
   python skills/skill-creator/scripts/generate_review.py <workspace>/iteration-1 --skill-name "my-helper" --benchmark <workspace>/iteration-1/benchmark.json
   ```

### 4. Optimize the Skill Description

Automatically maximize triggering accuracy while minimizing false positives on near-miss queries:

```bash
python skills/skill-creator/scripts/run_loop.py \
  --eval-set evals/trigger_eval.json \
  --skill-path skills/my-helper \
  --model <model-identifier> \
  --max-iterations 5
```

### 5. Package for Distribution

```bash
python skills/skill-creator/scripts/package_skill.py skills/my-helper dist/
```

---

## Tooling Suite

| Tool | Path | Description |
| :--- | :--- | :--- |
| **Initializer** | `skills/skill-creator/scripts/init_skill.py` | Scaffolds directory, `SKILL.md`, and sample resources with executable permissions. |
| **Validator** | `skills/skill-creator/scripts/quick_validate.py` | Validates frontmatter attributes, kebab-case naming, and unfinished `[TODO:]` blocks. |
| **Packager** | `skills/skill-creator/scripts/package_skill.py` | Compiles `.skill` archive with customizable exclusion rules (`--exclude`). |
| **Eval Runner** | `skills/skill-creator/scripts/run_eval.py` | Evaluates query triggering against `AGENT_CLI` with stream interception. |
| **Loop Controller** | `skills/skill-creator/scripts/run_loop.py` | Multi-iteration description optimizer with 60/40 stratified holdout. |
| **Description Improver** | `skills/skill-creator/scripts/improve_description.py` | Generates discriminating descriptions driven by eval failure analysis. |
| **Benchmark Aggregator** | `skills/skill-creator/scripts/aggregate_benchmark.py` | Aggregates pass rates, wall-clock duration, and token usage into `benchmark.json`. |
| **Review Server** | `skills/skill-creator/scripts/generate_review.py` | Serves interactive evaluation viewer (`skills/skill-creator/assets/viewer.html`) or exports `--static` HTML. |

---

## Subagent Reference Protocols

Pre-configured subagent protocols for automated evaluation are located in `skills/skill-creator/references/agents/`:

- [skills/skill-creator/references/agents/grader.md](skills/skill-creator/references/agents/grader.md): Evaluates transcripts and outputs against quantitative assertions, audits eval quality, and captures execution metrics.
- [skills/skill-creator/references/agents/comparator.md](skills/skill-creator/references/agents/comparator.md): Performs blind A/B quality adjudication across two anonymous outputs using dynamic content and structure rubrics.
- [skills/skill-creator/references/agents/analyzer.md](skills/skill-creator/references/agents/analyzer.md): Analyzes unblinded transcripts post-comparison and surfaces macro-level anomalies across multi-run benchmark datasets.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
