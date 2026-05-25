# Figure format template: Plotting and visualisation conventions

> **This is a scaffold, not a finished file.** Copy it to `conventions/figure-format.md` in your lab's working framework and fill in every `[adopter: ...]` slot. The worked examples use a running adopter scenario (a fictional terrestrial ecology lab using R + ggplot2 with the Okabe-Ito colourblind-safe palette). Delete the examples once you have written your own.

This file is the render-time companion to `conventions/manuscript-format.template.md`. Manuscript-format specifies how many figures, how they pair to results, and how legends are structured; this file specifies how each figure is actually rendered: tooling, palette, typography, panel labelling, scale bars, and export format.

---

## 1. Plotting tooling

The lab's default plotting library. Different teams will sit at very different points on this spectrum (ggplot2 / matplotlib / plotly / lattice / D3); the model needs to know which one to assume.

`[adopter: name your default library, any alternates, and the situations that trigger each. Include version pinning conventions if any.]`

> **Example: the ecology lab uses these tools.**
> - **Default**: R ggplot2 (3.4+) with patchwork (1.1+) for multi-panel figures and ggspatial (1.1+) for map insets.
> - **Alternates**: leaflet for interactive supplementary HTML maps; base R graphics for occasional diagnostic plots in supplementary scripts.
> - All plotting code lives under `code/figures/`; one script per main figure, named `fig_NN_short_descriptor.R`.
> - Package versions are pinned with `renv`; figures rendered with mismatched versions are flagged in code review.

---

## 2. Colour palette

The lab's default palette for categorical, sequential, and diverging data. Accessibility (colourblind safety) belongs in the palette choice, not as an afterthought.

`[adopter: name your categorical, sequential, and diverging palettes. Note any palette extensions for higher cardinality (more than 8 categories).]`

> **Example: the ecology lab uses these palettes.**
> - **Categorical (default)**: Okabe-Ito 8-colour palette. Hex codes: `#E69F00, #56B4E9, #009E73, #F0E442, #0072B2, #D55E00, #CC79A7, #000000`. Colourblind-safe (deuteranopia, protanopia, tritanopia).
> - **Categorical (overflow, more than 8 categories)**: Tol's `bright` (7-colour) extended with `muted` (9-colour) for a 12-colour set; use sparingly because 12 categorical colours strain reader memory.
> - **Sequential**: viridis (default) for non-cyclic; mako for darker-background plots.
> - **Diverging**: RdBu via `scale_colour_distiller(palette = "RdBu")` (reverse when needed for the direction-of-effect convention).
> - Never use rainbow / jet palettes.

---

## 3. Typography

`[adopter: name the sans-serif and serif fonts, default sizes for labels and ticks, and the minimum readable size at journal-column width.]`

> **Example: the ecology lab uses this typography.**
> - **Default font**: Arial (sans-serif). Serif alternatives are not used because *Journal of Animal Ecology* and *Ecography* both default to sans-serif in production.
> - **Axis labels**: 9 pt at final figure width.
> - **Tick labels**: 8 pt.
> - **Panel labels** (A, B, C, ...): 12 pt bold.
> - **Legend text**: 8 pt.
> - **Minimum size for any printed text**: 7 pt at the final column width. Anything below is rerendered.

---

## 4. Panel labelling

`[adopter: state the convention for multi-panel figures: letter placement, font size, bracket style, and how to handle sub-panels (A1, A2, A3 vs continuing the letter sequence).]`

> **Example: the ecology lab uses these panel conventions.** Top-left corner of each panel, 12 pt bold, no parentheses (just `A`, `B`, `C`), positioned outside the plot area. Sub-panels use letter+number (A1, A2, A3) only when the sub-panel is clearly a subdivision of a single conceptual unit (e.g., an occupancy-by-covariate plot showing the same model across three habitat strata). Otherwise, sub-panels continue the letter sequence.

---

## 5. Axes, ticks, grids

`[adopter: state your conventions for axis lines, tick direction, grid presence, log vs linear, and zero-line emphasis.]`

> **Example: the ecology lab uses these axis conventions.** Axes shown as solid 0.75-pt lines, left and bottom only (no top or right). Ticks outward (`theme(axis.ticks.length = unit(-0.1, "cm"))` flipped for outward in ggplot2). Major ticks at 5 to 7 positions per axis; minor ticks shown only for log-scale axes. No background grid by default; a light grey horizontal grid (alpha 0.2) is acceptable for bar charts. Log axes use base 10 with explicit `10^N` labels. Zero lines are emphasised (1.0 pt black) on diverging-effect plots (e.g., occupancy or abundance response curves crossing zero on the log-odds or log-link scale).

---

## 6. Scale bars and overlays

For spatial data, maps, or anything else where absolute scale matters.

`[adopter: state your scale-bar conventions: placement, size, label, units, colour for dark vs light backgrounds.]`

> **Example: the ecology lab uses these scale-bar conventions.** Site maps and study-area panels: scale bar in lower-right via `ggspatial::annotation_scale()`, white-on-dark for satellite-imagery basemaps and black-on-light for OpenStreetMap or simple polygon basemaps, 5 to 10% of plot width, with unit label below ("5 km"). North arrows added via `annotation_north_arrow()` on any panel where map orientation matters. No map panel is published without a scale bar and a north arrow.

---

## 7. Statistical annotation

Significance markers, error-bar conventions, sample-size annotation, and the rule for what tests get annotated visually vs only in the legend.

`[adopter: state your conventions for asterisk codes, error-bar choices (SD vs SEM vs 95% CI), n annotation, and which tests get visualised on the figure.]`

> **Example: the ecology lab uses these annotations.** Error bars: 95% confidence intervals by default; SEM only when sample size is explicit on the figure. Asterisk codes: `*` P<0.05, `**` P<0.01, `***` P<0.001, `ns` not significant. The exact test (Wilcoxon rank-sum, likelihood-ratio test, etc.) is named in the legend, not on the figure. Sample size is annotated on the figure as `n = N` near the test statistic when it varies across panels; otherwise placed in the legend. The lab does not use `P<0.05` thresholds for continuous-effect figures; partial effects with credible or confidence intervals are preferred.

---

## 8. Export format

`[adopter: state your default export formats and resolutions for main vs supplementary figures, raster vs vector use, and any compression conventions.]`

> **Example: the ecology lab uses these export conventions.**
> - **Main figures**: vector PDF (preferred) for any plot rendered programmatically; high-resolution PNG (600 dpi) when raster is required (e.g., basemap tiles in study-area maps). Each figure exported in both formats so submission systems can use whichever the journal prefers.
> - **Supplementary figures**: 300 dpi PNG for scanning, PDF for vector content.
> - **File naming**: `fig_NN_short_descriptor.pdf` and `.png` (e.g., `fig_03_occupancy_by_canopy.pdf`).
> - **Compression**: PNGs compressed losslessly; PDFs unmodified. No JPEG for any plot containing text or sharp edges.

---

## 9. Accessibility

`[adopter: state your accessibility floor. Colourblind palette is a baseline; what else does your lab enforce?]`

> **Example: the ecology lab uses these accessibility rules.** All categorical colour choices pass deuteranopia simulation (default Okabe-Ito handles this). Where colour encodes ordinal or quantitative meaning, also encode it with linetype or marker shape so the figure remains readable in grayscale. Critical contrasts (e.g., treatment vs control sites, observed vs predicted) use redundant encoding (colour + shape, or colour + label). Figures intended for talks additionally use larger fonts (12 pt minimum) and high-contrast palette settings.

---

## 10. Tables

Tables follow a different aesthetic from figures but are subject to similar legibility rules.

`[adopter: state your table-rendering conventions: tool, font, line weight, and rules for what becomes a table vs a figure.]`

> **Example: the ecology lab uses these table conventions.** Tables rendered with `gt` or `kableExtra` for HTML reports and `flextable` for Word submission. Arial 9 pt body text; bold headers; horizontal lines only (top, header bottom, table bottom); no vertical lines. Numeric columns right-aligned with a fixed number of decimal places per column; counts as integers; percentages with one decimal place. Tables with more than 8 columns or 20 rows are flagged for figure conversion or supplementary-table relocation.

---

## 11. Render-and-read protocol

When the model produces or modifies a figure, it should render the figure and inspect the rendered output, not just write the code. This is a meta-convention rather than a render rule, but it sits alongside the others.

`[adopter: confirm your render-and-read policy. State whether the model is expected to inspect each rendered figure before declaring the task complete.]`

> **Example: the ecology lab uses this policy.** Every figure script must render successfully and be inspected by the model before the analysis pipeline is considered complete. The model checks: (1) does the figure render without errors? (2) are all axes labelled with units? (3) is the legend readable? (4) does the figure visually communicate what the Results section claims? Any failure on these four checks routes back to the figure script for revision before the manuscript draft proceeds. See `conventions/visual-review-protocol.md` for the full protocol.

---

## Cross-references

- Document-level figure conventions (count, placement, legends): `conventions/manuscript-format.template.md`
- Visual review protocol (the four-test render-and-read): `conventions/visual-review-protocol.md`
- Voice (for legend text style): `conventions/voice.template.md`
- Code conventions (where figure scripts live, naming, version pinning): `conventions/code-format.template.md`
