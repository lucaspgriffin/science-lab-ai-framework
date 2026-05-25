# Manuscript format template: Lab manuscript conventions

> **This is a scaffold, not a finished file.** Copy it to `conventions/manuscript-format.md` in your lab's working framework and fill in every `[adopter: ...]` slot. The worked examples use a running adopter scenario (a fictional terrestrial ecology lab targeting *Journal of Animal Ecology*, *Ecography*, and *Methods in Ecology and Evolution*). Delete the examples once you have written your own.

A manuscript-format file encodes the conventions that operate ABOVE voice: section structure, citation density, length targets, figure/table conventions, and journal-specific defaults. Voice (`conventions/voice.template.md`) handles sentence-level register; this file handles document-level architecture.

---

## 1. Default journal and architecture

The lab's default target journal sets most downstream conventions (reference style, figure count, section ordering, length limits). Name the default, name two or three runners-up, and note when each is appropriate.

`[adopter: name your default journal and the alternates. Include reference style, typical figure/word counts, and submission-format quirks for each.]`

> **Example: the ecology lab targets these journals.**
> - **Default**: *Journal of Animal Ecology* (author-year references; ~4 to 6 main figures; ~7,000-word body including methods; unstructured abstract 350 words; methods integrated).
> - **Alternate 1**: *Ecography* (author-year; ~6 to 8 main figures; ~8,000 words; methods integrated).
> - **Alternate 2**: *Functional Ecology* (author-year; ~5 figures; ~7,500 words; methods integrated).
> - **Methods papers** route to *Methods in Ecology and Evolution*; applied work routes to *Journal of Applied Ecology*; broader-scope syntheses go to *Oikos* or *Ecology Letters*.

---

## 2. IMRAD skeleton

The default section structure for a primary research manuscript. Most field-ecology and quantitative-ecology papers fit this; named-section variants belong here too.

`[adopter: list your default section order, with brief notes on what belongs in each. Include any house variants (e.g., "Results and Discussion combined" for short-format papers).]`

> **Example: the ecology lab uses this skeleton.**
> 1. **Title** (under 15 words, no jargon abbreviations)
> 2. **Abstract** (350 words unstructured; or structured with Background, Methods, Results, Conclusion for some journals)
> 3. **Introduction** (4 to 6 paragraphs)
> 4. **Methods** (integrated; subsections per analytical step)
> 5. **Results** (5 to 8 subsections, each tied to a figure)
> 6. **Discussion** (4 to 6 paragraphs)
> 7. **References**
> 8. **Figure legends**
> 9. **Tables** (inline or separate file per journal)
> 10. **Supplementary materials** (separate document)

---

## 3. Section-by-section conventions

For each section, name: opening-sentence style, citation density, length target, and one structural rule the lab cares about.

### 3.1 Abstract

`[adopter: state the abstract structure, length, and any required components (background, methods one-liner, key result with statistic, conclusion).]`

> **Example: the ecology lab uses this abstract pattern.** 350 words unstructured. Sentence 1 = problem framing in the field. Sentence 2 = the specific gap. Sentences 3 to 5 = approach (one-paragraph methods summary, including study system, field methods, and modelling). Sentences 6 to 9 = key results, including at least two quantitative statistics with confidence intervals. Final 1 to 2 sentences = the takeaway, framed as a generalisable ecological principle or a methodological contribution.

### 3.2 Introduction

`[adopter: state opening-sentence style, citation density (citations per paragraph), length target, and the narrative arc.]`

> **Example: the ecology lab uses this introduction pattern.** 4 to 6 paragraphs, ~1,000 to 1,500 words. Opening sentence is a one-line statement of why the ecological question matters (not "Recent advances have ..."). Citation density is high: 6 to 12 citations per paragraph, balanced between foundational (pre-2015) and recent (last 5 years). The arc moves from broad ecological question, to the specific study system, to the methodological or knowledge gap, to the present study's contribution. Last paragraph ends with a one-sentence summary of the main finding.

### 3.3 Results

`[adopter: state structure (subsections, figure pairing), opening-sentence convention, and citation density.]`

> **Example: the ecology lab uses this results pattern.** 5 to 8 subsections, each ~250 to 400 words and each paired to exactly one main figure. Subsection opening sentence names the analytical question, not the result ("We asked whether ...", "To assess ..."). Citation density is low: only methodological references and direct comparisons to specific prior values. No interpretation or speculation in Results; that belongs in Discussion. Each subsection ends with a one-sentence transition to the next question.

### 3.4 Discussion

`[adopter: state structure, citation density, and rules for hedging.]`

> **Example: the ecology lab uses this discussion pattern.** 4 to 6 paragraphs, ~1,200 to 1,800 words. Paragraph 1 = a non-redundant restatement of the main finding plus its significance. Paragraphs 2 to 4 = mechanistic interpretation, integration with prior literature, alternative explanations. Paragraph 5 = limitations woven in (NOT a separate section). Final paragraph = implications, scoped. Citation density is high: 8 to 15 per paragraph. Each interpretation paragraph cites at least one supporting and one complicating reference where the literature is mixed.

### 3.5 Methods

`[adopter: state voice (active vs passive), structure, length, and the rule for what goes in Methods vs Supplementary.]`

> **Example: the ecology lab uses these methods conventions.** Passive voice, rationale-first paragraph openings. Subsection per analytical step (study area and design, field protocols, data processing, statistical analysis, model selection, code availability). Length flexible (no main-text limit for *Journal of Animal Ecology* methods within the overall word count). R package versions are explicit. Anything that someone else could not reproduce from the Methods alone moves to the supplementary protocol document.

---

## 4. Citation density and integration

Beyond the per-section densities above, name the lab's rules for how citations are integrated into prose.

`[adopter: state your rules for citation placement, multi-citation grouping, self-citation, and what counts as a citation-worthy claim.]`

> **Example: the ecology lab uses these citation rules.** Citations follow the claim they support, not the start of the sentence. Multi-citation groups of 5 or more are flagged for trimming; if 8 papers genuinely support a claim, cite the 3 most directly relevant. Self-citation is included where directly relevant; the lab does not pad references with its own work. Every quantitative claim or comparison to prior work needs a citation; broad framing statements may not. No orphan citations: every citation must connect to a specific argument in the surrounding sentence.

---

## 5. Figure and table conventions

This file handles the document-level rules (count, placement, legend length, integration into prose). The render-time rules (palette, typography, export format) live in `conventions/figure-format.template.md`.

`[adopter: state main-figure count target, figure-to-result pairing rule, legend length, and the convention for multi-panel figures.]`

> **Example: the ecology lab uses these figure conventions.** 4 to 6 main figures, each paired one-to-one with a Results subsection. Figures are multi-panel (2 to 6 panels) with letter labels (A, B, C, ...) in a consistent corner. Legends are 80 to 150 words, structured: one-sentence figure overview, then per-panel descriptions, then statistical-test summaries. Tables: 1 to 2 main, used for model parameter summaries or sample-design tables that do not benefit from visualisation. All supporting plots go to supplementary figures (typically 5 to 15 supp figures for a typical paper).

---

## 6. Supplementary materials

`[adopter: state what goes into supplementary, naming conventions, and any required components (code, data tables, protocols).]`

> **Example: the ecology lab uses these supplementary conventions.** Single PDF for supplementary figures and tables (Supp Fig 1 through N, Supp Table 1 through N), plus a separate supplementary protocol document (Word or PDF) for methods detail. Data tables that are too large for PDF go as `.csv` or `.xlsx`. Code is deposited on GitHub with a commit-pinned release tag; the README cites the release tag in the methods. Field data are archived on Dryad or Figshare with a DOI; sensitive site coordinates are perturbed prior to deposit per the lab's species-protection policy.

---

## 7. Length targets

`[adopter: state typical word counts for each section and total manuscript length.]`

> **Example: the ecology lab targets these lengths.**
> - Abstract: 350 words (unstructured) or 250 words (structured)
> - Introduction: 1,000 to 1,500 words
> - Methods: 1,500 to 2,500 words
> - Results: 2,000 to 3,000 words
> - Discussion: 1,200 to 1,800 words
> - Total body (including Methods): 6,000 to 8,000 words
> - Total references: 60 to 100 for a primary research paper

---

## 8. Reference list conventions

`[adopter: state reference style, ordering, format details, and any rules about reference set composition.]`

> **Example: the ecology lab uses these reference rules.** Author-year references (alphabetical) for *Journal of Animal Ecology*; first author then "et al." for papers with more than two authors in in-text citations. References are checked against the journal's reference template before submission. The reference set should be 70% from the last 10 years; the remaining 30% is the foundational literature that anchors the intellectual lineage. BioRxiv and EcoEvoRxiv preprints are cited with the preprint flag; flagged for replacement when published.

---

## 9. Cover letter and submission

`[adopter: state any cover-letter or submission conventions if your lab has a house template.]`

> **Example: the ecology lab uses this cover-letter pattern.** One page. Paragraph 1 = the problem and why it matters. Paragraph 2 = the approach and the key finding (one sentence with a number). Paragraph 3 = why this journal specifically. Paragraph 4 = suggested reviewers (4 to 6 names) and any reviewers to exclude (with brief justification).

---

## Cross-references

- Voice (sentence-level register): `conventions/voice.template.md`
- Figures and tables (render conventions): `conventions/figure-format.template.md`
- Citation and source-faithfulness rules: `conventions/research.md`
- Reviewer reply (format delta on this file): `conventions/reply-format.template.md`
