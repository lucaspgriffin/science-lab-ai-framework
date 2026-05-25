# Iteration Workflow: Research Loop to Publication Quality

## Purpose

Defines the six-phase orchestration loop invoked by `skills/workflows/research-iterate/SKILL.md`. Any analysis that is to reach publication quality runs through this loop. The loop is owned by the Lab Director agent; specialists are dispatched in parallel per phase.

This document is the source of truth for the phase sequence, agent roles per phase, state files, convergence rules, and escalation. It is referenced by the `research-iterate` skill and Lab Director's Iteration Mode.

## The Six Phases

### Phase 0: Readiness and Goal-Setting (runs ONCE, before the loop)

Purpose: establish what "done" means for this project, and confirm the system has the expertise to deliver it before implementation starts.

Lead: Lab Director, with input from all relevant specialists identified by the goal statement.

Process:
1. Lab Director reads the user's goal statement and the project directory.
2. Identifies required analytical techniques, focal study units (with relevant domain attributes), spatial/temporal covariates, and statistical frameworks. Uses `conventions/readiness-assessment.md` as the interrogation protocol.
3. Queries the knowledge base for coverage of each requirement. Marks each as **present**, **partial**, or **gap**.
4. Drafts `project-goal-spec.md` per `conventions/goal-spec.template.md`: concrete deliverables, acceptance criteria tied to `conventions/research-quality-gates.md` gates, applicable vs waived gates, out-of-scope, round budget.
5. Drafts `readiness-assessment.md`: coverage table and gap-fill plan. Mechanical gaps (fillable by literature review or stub completion) go to `improvement-queue.md` as auto-apply. Structural gaps (require a new skill, new agent scope, or new core doc) block the loop and escalate to the user.
6. Mechanical gap fills run BEFORE Phase 1 begins.

USER CHECKPOINT: approve goal spec and readiness plan before entering the loop. Any structural gap must be resolved (either user decision or explicit defer) before proceeding.

Re-trigger: if the user substantively changes the goal mid-loop, Phase 0 re-runs on the new statement; the existing goal spec is archived.

### Phase 1: Plan

Lead: Lab Director.

Process:
1. Read `iteration-state.json` (round number, open issues, gate status, goal-spec progress).
2. Write `round-N-plan.md` with:
   - Round objectives keyed to the remaining goal-spec acceptance criteria and highest-priority open issues from `issue-queue.md`.
   - Dispatch plan: which specialists run this round, which sub-skills they invoke, which outputs they produce.
   - Expected critics for Phase 3.

### Phase 2: Implement

Lead: dispatched specialists per Lab Director's plan, following existing dispatch patterns in `agents/lab-director.md`.

Process:
1. Each specialist executes their portion of `round-N-plan.md`.
2. For code-heavy work, specialists invoke the `skills/workflows/analysis-pipeline/SKILL.md` workflow as a sub-workflow: the existing pipeline primitive is reused, not duplicated.
3. Each specialist writes their outputs to the project directory and appends a self-critique request to their deliverable (questions they want the critics to examine).

### Phase 3: Refine (parallel critics)

Lead: Lab Director dispatches critics; critics act in parallel.

Critics per round:
- **Quantitative Scientist** (always): statistical review AND visualization review per `conventions/visual-review-protocol.md`. Writes `round-N-critique-quantitative.md`.
- **Relevant domain-specialist sub-agents** (instantiated from `agents/_domain-specialist.template.md` for the lab's focal domains): plausibility review against the domain knowledge base. One critique file per specialist.
- **Science Writer** (rounds at or beyond 2, or whenever framing or literature claims exist): framing, citation, narrative-coherence review. Writes `round-N-critique-writer.md`.

Each critique file contains:
- Issues ordered by priority (HIGH, MEDIUM, LOW).
- For each issue: description, evidence (file, figure, coefficient), suggested fix, whether it blocks a quality gate.

### Phase 4: Arbitrate

Lead: Lab Director.

Process:
1. Read all `round-N-critique-*.md` files.
2. Reconcile conflicts (for example, if the Quantitative Scientist says "covariate X is unestimable at this scale" but the goal spec calls for its inclusion, route to Science Writer or a domain specialist for alternative framing).
3. Update `issue-queue.md`: mark each critique item as **accepted** (queued for next round), **deferred** (with reason and re-check condition), or **rejected** (with reason).
4. Evaluate `conventions/research-quality-gates.md` against the goal spec's applicable gates. Write gate-status section to `round-N-decision.md`.
5. Write `decision-log.md` append: round summary, gate status changes, decisions made, key tradeoffs, next-round focus.
6. Choose one:
   - **Done**: all goal-spec acceptance criteria pass, zero open HIGH-priority issues. Loop terminates.
   - **Continue**: proceed to Phase 5 self-update, then Phase 1 of round N+1.
   - **Escalate**: the same gate has failed two rounds in a row, or a new structural question has emerged. USER CHECKPOINT.

USER CHECKPOINT (lightweight): "continue, pause, or redirect?" after each round.

### Phase 5: Self-Update

Lead: any agent contributes; Lab Director triages.

Process:
1. During Phases 1 to 4, any agent may append to `improvement-queue.md` when they spot a system gap: knowledge base article missing, skill step unclear, routing error, viz rule needed, quality-gate revision warranted.
2. End of round: Lab Director triages new entries per `conventions/system-improvement-protocol.md`. Mechanical entries auto-apply via the framework's update mechanism and are logged. Structural entries are queued to `system-change-proposals.md` for user review.
3. Decision log captures triage outcomes.

Mechanical improvements take effect for the next round (round N+1); the newly filled knowledge base article or tightened skill step is available to specialists.

## Global Defaults

- **Max rounds**: 5 (per-project override via `.iterate/config.yaml`)
- **Escalation trigger**: same quality gate fails 2 rounds in a row, OR any structural change proposal is filed
- **Loop exit**: all applicable goal-spec acceptance criteria pass AND zero open HIGH-priority issues, OR max rounds reached (with an escalation report), OR user halts

## State Files (per project, under `.iterate/`)

- `project-goal-spec.md` (Phase 0)
- `readiness-assessment.md` (Phase 0)
- `iteration-state.json`: round N, open issue counts, gate status, goal-spec progress, history (machine-readable, consumed by tooling)
- `round-N-plan.md`, `round-N-critique-<agent>.md`, `round-N-decision.md`: per round
- `issue-queue.md`: rolling open and resolved issues
- `improvement-queue.md`: system-update suggestions
- `decision-log.md`: permanent, human-readable round-by-round summary

## References

- `conventions/research-quality-gates.md`: the gates evaluated each round
- `conventions/visual-review-protocol.md`: the render-and-read protocol applied in Phase 3
- `conventions/readiness-assessment.md`: the Phase 0 expertise-coverage check
- `conventions/goal-spec.template.md`: the project-goal-spec template
- `conventions/system-improvement-protocol.md`: Phase 5 triage rules
- `skills/workflows/research-iterate/SKILL.md`: the orchestrator that implements this workflow
