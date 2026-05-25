# Readiness Assessment: Phase 0 System-Fitness Check

## Purpose

Before the iteration loop starts, Lab Director confirms that the system (knowledge base, agents, skills) has the expertise required for the project. Gaps are proposed as fills BEFORE Phase 1. This prevents the loop from running in circles on work the system is not equipped to do.

Runs once per iteration invocation; re-triggers if the user substantively changes the goal mid-loop.

## The Four Questions

Applied to the user's goal statement and project directory:

1. **What analytical techniques are required?** (for example, state-space models, mixed-effects meta-analysis, hidden Markov models, spatial GLMM, occupancy, Bayesian state-space.)
2. **What focal study units and relevant domain attributes?** (the specific organisms, sites, populations, or systems under study, along with whatever attributes drive the analysis: traits, history, environmental setting.)
3. **What spatial, temporal, or environmental covariates are involved?** (terrain, vegetation, temperature, season, time-of-day, weather, exposure, and so on.)
4. **What statistical frameworks underlie the choices?** (conditional logistic, Poisson GLM with offset, zero-inflated hurdle, INLA-SPDE, capture-recapture, etc.)

## Querying the Knowledge Base

For each requirement identified in the four questions, query the knowledge base:

1. **Exact slug match**: is there a dedicated article (`knowledge_base/<domain>/articles/<slug>.md`) on this topic?
2. **Alias match**: check article frontmatter `aliases:` fields for synonyms.
3. **Adjacent-article match**: is there an article that covers this as a sub-section but not as primary topic?
4. **Agent-scope match**: is an existing agent's persona or competencies section an explicit match (for example, a domain specialist whose role covers a technique even if no single article is titled with its exact name)?

Coverage is classified as:

- **Present**: dedicated article OR explicit agent-scope coverage. Proceed without flag.
- **Partial**: adjacent article covers it, or stub exists, or alias-match exists but thin. Proceed with caveat logged to `readiness-assessment.md`.
- **Gap**: no match. Propose a fill.

## Gap-Fill Decision Rules

For each gap, Lab Director decides one of:

- **Mechanical fill (auto-apply before loop starts)**: the gap is fillable by literature review, stub completion, or adding cross-links between existing articles. Queue to `improvement-queue.md` with category `kb-gap-mechanical` and dispatch the Science Writer (or relevant specialist) to populate. This runs in a blocking pre-Phase-1 pass.
- **Structural fill (escalate to user)**: the gap requires a new skill file, a new agent definition, an agent-scope expansion, or a new core doc. Queue to `system-change-proposals.md` and USER CHECKPOINT. The loop does not enter Phase 1 until the user decides: build now, defer with caveat, or reduce scope.
- **Proceed with caveat**: the gap is minor or out-of-scope for the current project. Log in `readiness-assessment.md` under "Known limitations of this run," noted for the discussion section.

## The Output Document (`readiness-assessment.md`)

Template:

```markdown
# Readiness Assessment: <project>

## Goal statement
<user's goal, verbatim>

## Required expertise

### Analytical techniques
| Technique | Coverage | Source | Action |
|---|---|---|---|
| <Technique A> | Present | knowledge_base/<domain>/articles/<slug>.md | proceed |
| <Technique B> | Partial | adjacent in <related article> | proceed + stub queued |
| <Technique C> | Gap | --- | mechanical-fill: Science Writer to add KB article |

### Focal study units
| Unit | Attribute coverage | Action |
|---|---|---|
| <Unit X> | Present (attributes A, B, C) | proceed |
| <Unit Y> | Partial (no dedicated profile) | stub queued |
| <Unit Z> | Gap (no profile) | mechanical-fill |

### Covariates
| Covariate | Coverage | Action |
|---|---|---|
| <Covariate 1> | Present | proceed |
| <Covariate 2> | Gap | structural-fill? (new article needed; escalate if large) |

### Statistical frameworks
(as above)

## Gap-fill plan

### Mechanical (auto-apply before Phase 1)
- [...]

### Structural (user review required)
- [...]

### Proceed-with-caveat
- [...]

## Blockers
<structural items that must be resolved before the loop enters Phase 1>
```

## Reassessment

Re-run Phase 0 when:
- The user substantively changes the goal statement (new deliverable, new focal unit, new technique).
- The loop surfaces a required technique not in the original assessment (Lab Director logs this, halts, re-assesses).

## References

- `conventions/iteration-workflow.md`: Phase 0 where this protocol runs
- `conventions/goal-spec.template.md`: the companion document produced in Phase 0
- `conventions/system-improvement-protocol.md`: where gap fills are processed
- `agents/lab-director.md`: agent that runs this assessment with specialist input
- `knowledge_base/*/INDEX.md`: canonical sources for knowledge-base coverage queries
