# Optional Skill Evaluation

Read this reference for a comparison across realistic tasks or for description optimization.
Choose the cases, iteration limit, and stopping condition before running; use existing cases
and expand only to resolve a demonstrated gap. These workflows are not prerequisites for
ordinary maintenance. Commands below run from the skill directory.

## Behavioral comparison

1. Choose tasks covering the affected failure, normal behavior, and relevant boundaries.
   Use [schemas.md](schemas.md) for `evals/evals.json`, metadata, grading, and benchmark formats.
   Preserve the previous skill version as the update baseline; for a new skill, compare against
   execution without it. Record the versions and execution environment.
2. Give executors the user request, skill, and raw inputs. Withhold the intended answer and
   proposed fix. Use separate temporary workspaces; restrict side effects to authorized actions.
   Independent executors can run concurrently when resources allow. Sequential comparison is
   also valid; disclose any shared-context or environment limitations.
3. Review outputs and execution traces against observable outcomes. Assertions should catch
   incorrect results, not just match headings, exact wording, or file existence. Use
   [agents/grader.md](agents/grader.md) for grading, [agents/comparator.md](agents/comparator.md)
   for blind output comparison, and [agents/analyzer.md](agents/analyzer.md) for anomalies.
4. Save available timing and token measurements using [schemas.md](schemas.md). Obtain them
   from actual logs or executor results; leave unavailable fields absent. Do not invent metrics
   or assume that every platform exposes the same completion notification. Missing costs may
   appear as zero or proxies in aggregate output; do not interpret them as measured savings.
5. Inspect regressions and unnecessary operations before changing instructions. Fix the current
   decision point rather than adding an incident-specific exception. Stop at the chosen bound
   once acceptance criteria hold; report small-sample results as cases, not stable improvements.

Use the existing workspace layout:

```text
<skill-name>-workspace/
└── iteration-1/
    └── eval-1/
        ├── with_skill/outputs/
        ├── old_skill/outputs/
        └── eval_metadata.json
```

For new skills, use `without_skill` instead of `old_skill`. Each run's `grading.json` uses
`expectations` entries with `text`, `passed`, and `evidence`; preserve these field names.

```bash
python scripts/aggregate_benchmark.py <workspace>/iteration-1 --skill-name <name>
python scripts/generate_review.py <workspace>/iteration-1 --skill-name <name> --benchmark <workspace>/iteration-1/benchmark.json
```

For later iterations, the reviewer accepts `--previous-workspace <previous-iteration>`.
For a non-interactive artifact, use `--static /tmp/review.html`. Read the resulting feedback
and rerun affected cases only when the revision or unresolved risk warrants it. Keep the
original failure as a regression case. Repeated ad-hoc code can become a bundled helper when
it has reusable value, rather than creating a script for every observed task.

## Description optimization

Use this workflow when changing selection boundaries or investigating misrouting, rather than
for unrelated body edits. Include realistic positive requests and challenging near misses.
Keep a separate final test set outside the optimization inputs if independent final evidence
is needed; do not tune the candidate after inspecting that set without treating it as validation.

To review queries, populate [../assets/eval_review.html](../assets/eval_review.html) with the
`__EVAL_DATA_PLACEHOLDER__` JSON array, `__SKILL_NAME_PLACEHOLDER__`, and
`__SKILL_DESCRIPTION_PLACEHOLDER__`. The review can export an edited evaluation set.

```bash
python scripts/run_loop.py --eval-set <path-to-eval-set.json> --skill-path <path-to-skill> --model <model-name> --max-iterations 5 --report none
```

This command invokes model-backed tools; run it only within the authorized scope and cost.
The existing default splits queries 60/40 and uses the held-out portion to select the best
candidate. Although script fields call it `test`, it serves as a validation set, not an
independent final test. Blinding these scores from the description improver does not remove
selection bias. Preserve the CLI flags and JSON fields; no script change is implied here.
The tool returns `best_description`; inspect the routing tradeoff and apply it to the source
frontmatter only when supported by the results. Report the skill/model versions and limits.
