# Goal-spec template: Per-project endpoint definition

> **This is a scaffold, not a finished file.** Copy it to `.iterate/project-goal-spec.md` in each project directory and fill in every `[adopter: ...]` slot. The worked example uses a running adopter scenario (a fictional terrestrial ecology lab's small-mammal occupancy project). Delete the example block once you have written your own.

Every `research-iterate` invocation produces a `project-goal-spec.md` in the project's `.iterate/` directory. This document is the loop's exit condition: the iteration terminates when all applicable acceptance criteria pass. It is read by the Lab Director in Phase 0 (drafted), Phase 4 (evaluated each round), and at loop termination.

Without a concrete goal spec, the loop has no stopping criterion other than the round budget or a user halt. The spec must be specific enough that "done" is testable.

---

## Required sections

### 1. Goal statement (verbatim)

The user's original goal statement, unedited. This anchors the loop against scope drift.

`[adopter: paste the user's verbatim request here.]`

### 2. Concrete deliverables

A bulleted list of specific artifacts the iteration must produce. Each item names a file, figure, table, or text section. No vague items.

`[adopter: list the artefacts. Each item should be specific enough that you can check it off as produced or not produced.]`

### 3. Acceptance criteria

Testable statements. Each is tied to a specific quality gate from `conventions/research-quality-gates.md`. Use measurable language.

`[adopter: write 5 to 12 testable criteria, each tagged with the relevant gate family in brackets.]`

### 4. Applicable gates

Which gate families from `conventions/research-quality-gates.md` apply for this project:

- **Analytic**: APPLIED / WAIVED (justification) / PARTIAL (which criteria)
- **Ecological / Biological / Domain**: APPLIED / WAIVED / PARTIAL
- **Visual**: APPLIED / WAIVED / PARTIAL
- **Literature**: APPLIED / WAIVED / PARTIAL
- **Framing**: APPLIED / WAIVED / PARTIAL

Waivers must include reasoning.

`[adopter: mark each gate's status with a justification for any WAIVED or PARTIAL entries.]`

### 5. Out-of-scope

Explicit non-goals. Things the iteration should not attempt. Prevents scope creep during refinement rounds.

`[adopter: list 3 to 6 specific things the loop will not do, even if the analysis suggests them.]`

### 6. Round budget

Estimated maximum number of refinement rounds. Global default is 5; override here if the project is unusually simple or complex.

`[adopter: state the round budget and any project-specific escalation triggers.]`

### 7. Escalation-requiring decisions

Decisions the Lab Director must escalate to the user rather than resolve autonomously.

`[adopter: list 3 to 6 decisions that the loop must not make on its own.]`

---

## Worked example (the example ecology lab)

> The following block is illustrative. Replace it with your own filled-in spec when you copy this template into a project's `.iterate/project-goal-spec.md`.

```markdown
# Project Goal Spec: Small-mammal occupancy across a canopy-cover gradient

## 1. Goal statement
Quantify how small-mammal occupancy and detection probability respond to a
canopy-cover gradient in a temperate-forest study system, using two years of
camera-trap data alongside vegetation transect covariates; produce a validated
inference set, plus a draft manuscript targeting Journal of Animal Ecology.

## 2. Concrete deliverables
- `results/tables/occupancy_estimates.csv` with species-by-site occupancy posteriors and credible intervals
- `results/models/occupancy_multispecies.rds` with the fitted multi-species occupancy model and held-out predictive performance
- 5 main-paper figures:
  - Fig 1: study area map + site-level sampling design
  - Fig 2: detection histories summary and naive occupancy by species
  - Fig 3: covariate effects on occupancy (partial effects with credible intervals)
  - Fig 4: covariate effects on detection probability
  - Fig 5: predicted occupancy surface across the canopy-cover gradient
- 8 to 12 supplementary figures (QC, sensitivity, alternative model parameterisations)
- Drafted Methods (~2,000 words) and Results (~2,500 words) sections
- `decision-log.md` with justification for every quality gate pass
- `manuscript/main/draft.md` ready for expert-review skill

## 3. Acceptance criteria
- [Analytic] Held-out predictive log-score within 2 SE of cross-validation baseline for occupancy classification
- [Analytic] Sensitivity analysis confirms covariate effects stable across alternative prior choices and across leave-one-site-out folds
- [Analytic] Detection histories handle observer effects (camera type, deployment season) as explicit covariates
- [Ecological] Top covariate effects qualitatively consistent with the published small-mammal microhabitat literature (positive control on three focal species)
- [Ecological] Predicted occupancy surface is biologically plausible at landscape extremes (no implausible extrapolation across the canopy gradient)
- [Visual] Every main figure passes the four-test render-and-read protocol with at least one documented revision cycle
- [Visual] All categorical species colours use Okabe-Ito; partial-effect plots show 95% credible intervals
- [Literature] Every claim in the Discussion cites at least one supporting or contrasting reference
- [Literature] Discussion explicitly engages with at least 3 alternative modelling frameworks (single-species occupancy, hierarchical N-mixture, joint species distribution models)
- [Framing] Abstract draft passes voice check from conventions/voice.md
- [Framing] Figure-to-claim evidence map documented in .iterate/framing/

## 4. Applicable gates
- Analytic: APPLIED
- Ecological: APPLIED
- Visual: APPLIED
- Literature: APPLIED
- Framing: APPLIED

## 5. Out-of-scope
- Adding a third field season: out of round budget
- Cross-region comparison (boreal sites): deferred to follow-up project
- Acoustic or genetic species identification: separate workstream
- Population-dynamics modelling beyond static occupancy: separate manuscript
- Web-portal deployment of the predicted surface: deferred to data-release phase post-acceptance

## 6. Round budget
5 rounds. Escalate if held-out predictive performance stalls below baseline at round 2.

## 7. Escalation-requiring decisions
- Dropping a focal species from the analysis if detection is too sparse for stable inference
- Switching the held-out validation strategy (site-out vs season-out vs random)
- Adding a new co-author for the vegetation analyses
- Changing the target journal
- Any new agent, skill, or KB article (any structural system change)
```

---

## References

- `conventions/iteration-workflow.md`: Phase 0 drafts this, Phase 4 evaluates against it
- `conventions/research-quality-gates.md`: source of the gate families referenced in acceptance criteria
- `conventions/readiness-assessment.md`: companion document from Phase 0
