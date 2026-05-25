# System Improvement Protocol: Self-Update Mechanism

## Purpose

As the research-iterate loop runs, agents encounter system gaps: a missing knowledge base article, an unclear skill step, a routing error, a visualization rule that should be in the protocol, a quality gate that needs tightening. This protocol channels those observations into system updates without interrupting the analysis.

Two queues drive the mechanism: `improvement-queue.md` (agents append; append-only during rounds) and `system-change-proposals.md` (Lab Director triages; decisions logged).

## When Agents Append

Any agent, specialist or Lab Director, may append to `improvement-queue.md` at any point during Phases 1 to 4 when they notice:

- **KB gap**: a domain article is missing, thin, or out of date; a stub is referenced but not written.
- **Skill gap**: a workflow skill is missing a step, a step is unclear, or a task skill lacks coverage for a technique actually needed.
- **Routing error**: Lab Director dispatched to the wrong agent (scope mismatch), or the wrong skill was invoked.
- **Viz rule missing**: a figure failure pattern not yet captured in `conventions/visual-review-protocol.md` or the visualization knowledge-base article.
- **Quality-gate revision**: a gate criterion is too strict (rejects legitimate work), too loose (misses real failures), or missing a criterion (for example, "Analytic Gate should include posterior-predictive check for Bayesian models").
- **Agent-scope issue**: a specialist's persona or competencies section doesn't cover a technique they were asked to critique, or their scope overlaps ambiguously with another specialist.

## Queue Entry Format

Each entry in `improvement-queue.md` uses this structure:

```markdown
### [YYYY-MM-DD, round N] <category>: <short title>
- Source agent: <agent name>
- Context: <what was happening when noticed>
- Observation: <the gap itself>
- Proposed response: <mechanical|structural> on <what would fix it>
- Impact: <blocking|high|medium|low>
```

Category must be one of: `kb-gap`, `skill-gap`, `routing-error`, `viz-rule`, `gate-revision`, `agent-scope`, `dashboard`, `other`.

## Mechanical vs Structural

### Mechanical (auto-apply)
The fix is constrained to content changes inside existing files:
- Fill an existing stub (knowledge-base article written by Science Writer)
- Add cross-links between existing knowledge-base articles
- Update a knowledge-base article with a new citation or new finding
- Tighten an existing step in a skill (clarify wording, add missing sub-step)
- Add a missing alias to an article's frontmatter
- Add a missing figure-failure pattern to the visualization protocol

Auto-apply path:
1. Lab Director moves the item from `improvement-queue.md` to `system-change-proposals.md` with status `mechanical-auto`.
2. The relevant agent (usually Science Writer or the originating specialist) is dispatched to implement, via the framework's skill-update mechanism for skill changes, or direct file edit for knowledge-base articles.
3. Change is applied within the round it is triaged (or at round-boundary for skill changes).
4. Result logged in `decision-log.md` under Round-N Self-Update.

### Structural (user review)
The fix would create or re-organise system components:
- New knowledge-base article on a topic with no existing coverage
- New skill file (workflow or task)
- New agent definition or agent-scope expansion
- New core doc
- New quality gate or significant revision to an existing gate
- Changes to routing tables in CLAUDE.md that affect how requests are dispatched

Structural path:
1. Lab Director moves the item from `improvement-queue.md` to `system-change-proposals.md` with status `structural-pending`.
2. Proposal written up as a brief: rationale, proposed change, affected files, risks.
3. USER CHECKPOINT: user decides build-now, defer, reject, or modify-then-build.
4. If build-now: the appropriate agent is dispatched with the approved brief; the framework's skill-update mechanism is invoked for any skill rebuild needed.
5. Status updated to `structural-applied`, `structural-deferred`, or `structural-rejected` in `system-change-proposals.md` with rationale.

## Triage Cadence

Lab Director triages `improvement-queue.md` at the end of each round (Phase 5). No item is left in `improvement-queue.md` across two rounds without a triage decision.

Triage decisions:
- **Auto-apply now** (mechanical, low-risk): move to `system-change-proposals.md` with status `mechanical-auto`, dispatch implementation.
- **Queue for user review** (structural): move to `system-change-proposals.md` with status `structural-pending`, include in round's escalation set.
- **Defer**: stay on queue with explicit "re-check in round N+K" note; becomes due if the gap re-surfaces.
- **Reject**: move to `system-change-proposals.md` with status `rejected`, with justification (for example, "out of current project scope; not generalizable").

## Pre-Loop Execution

During Phase 0, the readiness assessment may queue items directly to `improvement-queue.md`. These are triaged BEFORE Phase 1 begins:
- Mechanical items auto-apply in a blocking pre-loop pass (readiness fills complete before the loop enters Phase 1).
- Structural items trigger USER CHECKPOINT at the Phase 0 boundary.

This ensures the system is ready for the work before the loop starts.

## User-feedback capture (mandatory trigger)

Substantive user feedback is a top-priority improvement signal and MUST trigger this protocol every time. Do not wait for a round-boundary triage; do not assume the lesson is project-specific without checking.

### What counts as substantive feedback

Any user message that contains one or more of:

- Direct criticism of output ("this is wrong", "you missed", "you've failed to", "this is troubling").
- A statement of systematic preference revealed by the work ("I'd like you to remember this", "going forward, do X", "always do Y", "next time").
- A redirect that reveals the output diverged from the user's intent at the *strategy* level (genre, register, audience, framing), not just typos or word choice.
- An explicit ask to update memory or refine the framework ("save this to memory", "make this a rule", "add to skills").

Routine word-choice edits, factual corrections, and clarifying questions are NOT in scope here unless they reveal a recurring pattern.

### Required response when triggered

1. **Acknowledge the feedback honestly** in the conversation. Name what diverged and why it diverged. Do not be defensive.
2. **Capture the lesson to project memory** at the project's memory directory as a new feedback file, indexed in `MEMORY.md`. Use the format:
   - File name: `feedback_<short-topic>.md`
   - Frontmatter: `name`, `description`, `type: feedback`, `date`
   - Body: what happened, what the user wants instead, how to detect the same situation next time, how to behave instead.
3. **Refine the relevant framework file** when the lesson generalises beyond this project. Candidate targets, in order of preference:
   - `conventions/<file>.md` if the lesson is a voice, format, or methodological rule.
   - `agents/<agent>.md` if the lesson is about a specialist's scope or behaviour.
   - `<workflow>/SKILL.md` if the lesson is about a workflow step.
   - A core doc (this protocol, voice, iteration, quality gates) if it is a meta-rule.
4. **Rebundle the affected `.skill` bundle** via the framework's skill-update mechanism if a packaged workflow was touched, so the change ships with future invocations.
5. **Report what changed** in the same response: which memory file, which convention or skill file, and what the practical effect is.

If the feedback is project-specific (for example, a one-off preference for a single manuscript), still write the memory file under the project; only skip the global framework update.

### Distinguishing surface fixes from systemic lessons

- Surface fix: "use Times New Roman, not Calibri" is already covered by `conventions/manuscript-format.template.md`. No new memory; verify the existing rule was honoured and apologise for the miss.
- Systemic lesson: "you keep softening my pitch language back to your default voice" is not currently covered; needs a new rule in `voice.template.md` and a memory entry. Trigger the full capture.

### Anti-patterns

- Logging the feedback only as a TODO and assuming you'll remember next session: you will not. The memory file is the durable record.
- Updating the framework but not the project memory: the project loses local context.
- Updating the memory but not the framework when the lesson generalises: the next project inherits the same gap.
- Treating every edit as a systemic lesson: not every word-change is a rule. Use the surface-fix test above.

## Interaction with the skill-update mechanism

The framework's skill-update mechanism is responsible for actually modifying skill files (including rebuilding `.skill` bundles for distribution). For mechanical improvements affecting skills:

1. Lab Director dispatches the relevant agent with a clear change brief.
2. The agent invokes the skill-update mechanism with the brief.
3. The mechanism applies source changes and triggers any necessary bundle rebuilds.
4. Changes logged in the agent's critique file and rolled up to `decision-log.md`.

For knowledge-base article changes (non-skill), the agent edits the file directly: the skill-update mechanism is not involved.

## References

- `conventions/iteration-workflow.md`: Phase 5 where this protocol runs
- `conventions/readiness-assessment.md`: Phase 0 queues items via this protocol
- `agents/lab-director.md`: the triager
