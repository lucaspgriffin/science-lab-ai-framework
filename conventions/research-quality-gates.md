# Research Quality Gates: Convergence Criteria for Publication-Ready Work

## Purpose

Defines the checklist the Lab Director evaluates each round of `conventions/iteration-workflow.md` to decide whether work is publication-ready. Each project's goal spec (`.iterate/project-goal-spec.md`) selects which gates apply; waived gates must carry written justification.

A gate is **passed** only when the written justification exists in `decision-log.md`. Ticking a box is not enough.

## The Five Gate Families

### 1. Analytic Gate

Purpose: the statistical work is sound and transparent.

- **Diagnostics run and pass** for every fitted model: residual diagnostics (e.g., DHARMa for GLMM), smooth-term and concurvity checks (for GAM), autocorrelation checks (ACF/PACF for temporal), spatial autocorrelation checks (Moran's I, variogram), collinearity (VIF), Hessian positive-definiteness (mixed-effects).
- **Sensitivity analyses** exist for every consequential ad hoc decision: filtering threshold, bin width, exclusion criterion, smoothing parameter, step interval, etc. Each sensitivity run has a stated finding ("sign/magnitude stable" or "meaningful drift, described in limitations").
- **Model assumptions tested**: distribution family justified by data structure, random-effect structure justified by design, link function and offset justified.
- **Every coefficient interpretable**: no `NaN` SEs in published model, no near-separation estimates dominating pooled results, no extreme outliers in random effects without explanation.
- **Coefficient magnitude sanity**: no main-effect coefficient exceeds 3x the 95th percentile of same-covariate coefficients across study units, OR has |est| > 5 log-odds per 1 SD, without a stated mechanism in `decision-log.md`. This catches near-separation artifacts that pass the NaN-SE bar but reflect numerical instability from low within-stratum covariate variance. The "without a stated mechanism" clause permits legitimate large effects provided the analyst explicitly justifies them.
- **Reproducibility**: seeds set, sessionInfo recorded, relative paths, version-controlled.

### 2. Domain Gate

Purpose: findings make sense in the substantive domain, or the discordance is acknowledged and engaged.

- **Counterintuitive findings** either explained mechanistically (hypothesis offered, citations of precedent or analogy) OR explicitly flagged as real puzzles for the discussion.
- **Literature-discordant results** engaged: what does the prior literature predict? Why might our findings differ (scale, population, methods, real signal)? Not glossed over.
- **System- or unit-specific patterns** checked against established understanding for each focal unit. A unit known to associate with feature X showing null selection for X must be explained (e.g., scale mismatch, season, availability sampling), not silently accepted.
- **Seasonal or temporal structure** considered where it is plausible. Year-round claims require year-round analysis or explicit limitation.
- **Mechanism hypotheses** offered for key findings: what drives the pattern? This is what separates description from science.

### 3. Visual Gate

Purpose: figures communicate their own findings to a reader without requiring the caption to do the work.

- **Every figure passes the five-test rendered-output protocol** per `conventions/visual-review-protocol.md`:
  1. 5-second takeaway clear
  2. 30-second main finding identifiable without caption
  3. Careful-study verification possible (raw data visible, not only the summary)
  4. Resolution and uncertainty rendered (sample size, precision, SE, n)
  5. Physical plausibility check (no out-of-domain data, no constraint violations)
- **Raw data visible** alongside model output wherever practical. Selection surfaces overlay observed positions; model predictions overlay data points.
- **Reference context** on spatial/temporal plots: scale bar, north arrow, time indicator, inset maps where zoomed.
- **Colour is semantic**: time gradients, magnitudes, and categories use appropriate palettes. Default plotting-library palettes are rarely right for a paper figure.
- **Every main-paper figure** has at least one render-iteration cycle (render, read, revise, render again). See `conventions/visual-review-protocol.md` for tier definitions.

### 4. Literature Gate

Purpose: claims are sited in the existing literature, and novelty is clearly earned.

- **Every substantive claim** either cites prior work or is explicitly flagged as novel.
- **Prior conflicting findings engaged**: if three recent studies say X and we say Y, Y is justified (methodological, scale, population, or genuine new finding).
- **Method citations** current (within roughly five years for canonical methods; older is fine for foundational references).
- **Stakeholder-relevant context** included where applicable (e.g., management or policy relevance, jurisdictional context).

### 5. Framing Gate

Purpose: the paper has a defensible narrative structure before writing begins in earnest.

- **Main paper and appendix structure drafted** with figure list, table list, and section headings.
- **Figure-to-claim evidence map exists**: each main-paper figure is tied to a specific claim it supports; each appendix figure is tied to a robustness check, diagnostic, or secondary finding.
- **Opening hook** (what's the story?) and **closing implication** (what does this mean?) articulated.
- **Target journal** identified, even tentatively, with reasoning (scope fit, audience, IF considerations).

## Goal-Spec Governs Applicability

Every project's `project-goal-spec.md` enumerates which gates are **applicable** for this run. Gates may be:

- **Applied**: must pass before loop terminates
- **Waived**: justified in the goal spec (for example, "this is a methods paper; Framing Gate deferred to downstream companion paper")
- **Partial**: only some criteria apply (for example, Analytic Gate excluding Hessian check for models fit via conditional logistic)

Lab Director cannot pass a gate without either all applicable criteria met or explicit waiver with justification.

## Writing the Justification

Each gate's pass in `decision-log.md` must include:

```
### Round N Gate: Analytic
Status: PASSED
Justification: [specific evidence: which diagnostic, which sensitivity result,
                what coefficient looks stable across model variants, etc.]
Open items rolled forward: [nothing | specific list]
```

Vague justifications ("diagnostics look fine") are not acceptance. The entries need to reference specific files, specific coefficient CIs, specific plots.

## Escalation

If the same gate fails two consecutive rounds, Lab Director escalates to USER CHECKPOINT. Options offered:

- Reduce scope (drop a deliverable so the gate no longer applies)
- Waive the gate with written justification
- Change approach (new method, new model structure)
- Extend round budget
- Halt the loop

## References

- `conventions/iteration-workflow.md`: where these gates are evaluated
- `conventions/visual-review-protocol.md`: Visual Gate detail
- `conventions/goal-spec.template.md`: where applicable gates are declared per project
- `conventions/code-format.template.md`: reproducibility expectations underlying the Analytic Gate
