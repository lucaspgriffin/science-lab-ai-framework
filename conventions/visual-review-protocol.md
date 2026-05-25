# Visual Review Protocol: Render-and-Read

## Purpose

Figures that "work" in code often fail to communicate to a human reader. This protocol enforces a review step where the agent actually reads the rendered image (not just the code) and judges it by what a reader sees.

This protocol is invoked in Phase 3 of `conventions/iteration-workflow.md` by the Quantitative Scientist, and is a prerequisite for the Visual Gate in `conventions/research-quality-gates.md`.

## Core Principle

Code-mode review ("did we set the minimal theme, right colorscale, correct facets") is necessary but insufficient. Reader-mode review ("what does a human learn in 5 seconds, 30 seconds, careful study") is mandatory for any figure that will be cited in a decision or included in a paper.

The mechanism is simple: **render the figure, open the PNG, describe what is actually visible.**

## The Five-Test Checklist

Applied to every full-tier figure:

### Test 1: 5-Second Takeaway
Open the PNG, look for 5 seconds, look away. What is the immediate impression? If the figure's main finding is not clear in 5 seconds, the figure fails.

### Test 2: 30-Second Main Finding
Return to the figure for 30 seconds. Can the main finding be stated without reading the caption? If the caption is the only path to interpretation, the figure fails.

### Test 3: Careful-Study Verification
Study the figure carefully. Can the finding be verified from the data shown (not just from the summary)? If raw data is hidden behind a model or summary-only plot, the figure fails.

### Test 4: Resolution and Uncertainty Visibility
Is the data resolution (sample size, uncertainty, confidence, standard error) rendered somewhere in the figure? If resolution is hidden, the figure fails. A tight-looking curve that masks huge SE is misleading.

### Test 5: Physical Plausibility
Does any data element shown in the figure violate a known physical, biological, or logical constraint? For spatial data: do any points fall outside the valid study extent, or cross known barriers? For time series: do any values exceed physically impossible bounds (e.g., proportions > 1, negative counts, temperatures above boiling)? For unit-level trajectories: do any paths connect implausibly? If any data element is physically implausible, the figure fails AND the underlying data pipeline has a bug that must be fixed before re-rendering.

**This test is the reviewer's firewall against silent pipeline failures.** A figure can pass tests 1 to 4 while still being wrong: tests 1 to 4 check communication quality; test 5 checks whether the thing being communicated is physically real. An impossible trajectory is a pipeline bug masquerading as a legible figure.

For spatial data specifically, the reviewer should:
- Overlay the valid-study-area boundary (region polygon, study-extent shapefile, mask) if not already visible
- Inspect every track or point for out-of-bounds placement
- Check any projected or smoothed data against a sample of raw data to catch smoothing artifacts that cross barriers
- Verify that any post-hoc correction (snapping, projection, masking) was actually applied to the displayed data

## The Protocol Steps

For every full-tier figure:

1. **Render** the figure from the current code.
2. **Read the PNG** via the Read tool. Do not rely on the code alone.
3. **Describe what is visible** in 2 to 4 sentences, as if to a blind reviewer. Include things like: "this is a whole-extent view with three trajectories, mostly overlapping, with no visible indication of the refinement effect." Be specific about what a reader sees, not what the code was meant to produce.
4. **Score the five tests**. For each failure, state why. Test 5 (physical plausibility) is mandatory for any figure showing data in a constrained domain (spatial, temporal, compositional).
5. **Propose the next render** with specific changes: zoom to smaller extent, facet into panels, add overlay of raw data, add scale bar, switch palette, add inset map, add uncertainty band, overlay valid-domain boundary for plausibility check.
6. **Re-render and re-read**. Iterate at least twice per full-tier figure before marking it done.
7. **Record** the final figure's status in the round's critique file, with a one-paragraph note on what was visible before vs after the revision.

## Two Tiers

### Lightweight tier (in-analysis diagnostics)
- Applied to: residual plots, exploratory density plots, per-unit diagnostic grids, raster sanity checks.
- Protocol: Test 1 only, no iteration required.
- Purpose: keep analysis moving; a rough figure is fine for a rough decision.

### Full tier (publication / convergence-gate figures)
- Applied to: every figure referenced in `round-N-decision.md`, every figure destined for the main paper or appendix, every figure cited in `decision-log.md` as evidence for a gate pass.
- Protocol: all five tests plus a minimum of two render-iteration cycles.
- Purpose: protect the Visual Gate from silent failure.

Promotion rule: any figure a critic cites as evidence in a critique file is automatically promoted to full-tier for the next round.

## Style Rules

Apply these in parallel with the five-test protocol. Specific platform conventions live in `conventions/figure-format.template.md`; the rules below are the protocol-level baseline.

- **No Unicode characters in rendered figure text**: garbled labels (for example, degree symbols rendering as `..C`) are one of the most common silent failures in batch or non-interactive runs. Two acceptable approaches, in preference order:
  1. **Plotmath expressions** (preferred when supported): renders correctly across locales and looks best.
  2. **Plain ASCII fallback** (safe everywhere): `C`, `deg C`, `R2`, `m2`, `+/-`, `->`, `x`, `mg O2 kg^-1 h^-1`.
  Never put a bare Unicode degree, superscript, micro, plus-minus, or comparison symbol into rendered text without confirming locale handling.
- **PNG by default**, no PDF export unless the task explicitly asks for it.
- **Colour-semantic match**: time gradients use a sequential viridis-family palette; signed magnitudes use a diverging palette; categories use a colourblind-safe qualitative palette.
- **Small multiples default** for unit-level data (per-individual, per-site, per-replicate): aim for 8 or more panels, not 3.
- **Always include** a scale bar on spatial plots, a sample-size annotation where the sample is non-obvious, error bars or shading where uncertainty exists.
- **Per-panel scale bars on small multiples**: spatial small-multiples figures with different zoom extents per panel require a scale bar *in each panel* (dynamic length to match zoom), not a single legend-strip scale bar. A single shared scale fails when panels have different extents.
- **Extrapolation-region masking**: when a spatial model is fit on data with geographic coverage smaller than the prediction extent (for example, a sparse observation array smaller than the full study region), mask or dim the extrapolation region on the visualization, OR annotate the coverage boundary. Readers must be able to distinguish "validated" from "extrapolated" regions at a glance.

## Common Failure Patterns to Watch For

- **Whole-extent view when the effect is local**: a small-scale pattern invisible because the plot shows the whole region. Fix: zoom with inset context.
- **Model summary without data overlay**: prediction surfaces with no observed points. Fix: overlay actual data points.
- **Colour palette misused for magnitudes**: default sequential palette on a categorical variable or rainbow on ordered values. Fix: semantic palette.
- **Tight-looking fit masking uncertainty**: model line without CI band, or with CIs clamped for "readability." Fix: show the real uncertainty; if it's too large to interpret, that's the finding.
- **Sample thin**: 3 example units when 20 exist. Fix: small-multiples with 8 to 12 panels.
- **Legend unreadable**: text too small, wrong position, collides with data. Fix: read the rendered PNG to catch.
- **Unicode-garbled labels**: degree, superscript, micro, etc. rendered as placeholder characters under a non-UTF locale. Fix: use plotmath expressions or plain ASCII fallback. See Style Rules above. The render-and-read pass MUST flag any garbled label: if you see `..`, don't silently accept it.

## Writing Up the Review

Critique entries in `round-N-critique-quantitative.md` should include, for each full-tier figure:

```
### Figure: <filename>
Tier: full
Tests passed: [1/2/3/4/5] / [listed failures]
Visible before revision: [2 to 4 sentence description]
Visible after revision: [2 to 4 sentence description]
Iterations: [count]
Final status: PASS / NEEDS-REVISION / BLOCKING
```

## References

- `conventions/research-quality-gates.md`: Visual Gate criteria
- `conventions/iteration-workflow.md`: Phase 3 where this protocol runs
- `conventions/figure-format.template.md`: platform-specific style rules
- `agents/quantitative-scientist.md`: the agent that executes this protocol
- Project CLAUDE.md files: lab-specific style rules per project
