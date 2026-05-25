# Voice template: Lab writing conventions

> **This is a scaffold, not a finished file.** Copy it to `conventions/voice.md` in your lab's working framework and fill in every `[adopter: ...]` slot. The worked examples below use a running adopter scenario (a fictional terrestrial ecology lab studying small-mammal population dynamics and vegetation-climate interactions) to show what filled-in content looks like; delete those blocks once you have written your own.

A sharp, recognisable voice is one of the highest-leverage tunings you can make. Two labs in the same subfield will hedge differently, choose different verbs, and structure paragraphs differently. The default style of large language models is unhedged, superlative-prone, and rhythmically flat; without an explicit voice file, that is what you will get. This template names the slots that matter most.

---

## 1. Register

The default register your lab writes in. Affects vocabulary range, sentence complexity, technical density, and how comfortable the writing is with mathematical or computational notation.

`[adopter: describe your lab's default register in 2 to 4 sentences. Cover: technical density, comfort with statistical or mathematical notation, citation density, audience assumption.]`

> **Example: the ecology lab uses these defaults.** Technical, citation-dense, careful with biological interpretation. Comfortable with mixed-model notation, occupancy-model parameters, and effect-size summaries in main text; assumes a reader who can parse a random-effect structure or a marginal R² without explanation. Default audience is field ecologists and quantitative ecologists submitting to *Journal of Animal Ecology*, *Ecography*, or *Methods in Ecology and Evolution*. The lab does not soften jargon for general readers in primary research papers; synthesis pieces and policy briefs relax this rule.

---

## 2. Hedging calibration

How aggressively your lab hedges different categories of claim. The mismatch between unhedged facts and over-hedged interpretations is one of the most common voice failures.

`[adopter: write 3 to 5 calibration rules, one per claim category. Categories worth covering: direct measurements, statistical results, mechanistic interpretations, generalisations beyond the sample, implications.]`

> **Example: the ecology lab uses these rules.**
> - **Direct measurements** (capture counts, transect totals, camera-detection counts) are reported as facts: "We recorded 4,217 independent small-mammal detections across 84 camera-trap stations."
> - **Statistical results** are reported with the test and the effect size, no softening: "Occupancy declined with canopy openness (logit-scale slope = -0.42, 95% CI [-0.71, -0.13], n = 84 sites)."
> - **Mechanistic interpretations** hedge moderately: "These results are consistent with reduced understorey cover constraining *Peromyscus* activity during the early dry season." Avoid "demonstrates" or "proves" outside of mathematical proofs.
> - **Generalisations beyond the sample** hedge clearly: "Whether this pattern extends to mesic forest systems in the eastern range remains untested."
> - **Implications** are confident but scoped: "This framework may transfer to other small-mammal communities where microhabitat structure mediates the response to climatic variation."

---

## 3. Punctuation rules

The framework strongly recommends a hard em-dash ban (no `—`, no `--`, no spaced ` - `). Em-dashes are an LLM tic; banning them outright forces alternative constructions and breaks the cadence drift that makes AI-written prose recognisable. This is the framework's strongest default; adopters can relax it if their lab actively prefers em-dashes, but the recommendation is to keep the ban.

`[adopter: confirm the em-dash policy (keep banned vs allowed with cap) and list any other punctuation conventions your lab enforces (Oxford comma, en-dashes in ranges, hyphenation rules for compounds, etc.).]`

> **Example: the ecology lab uses these rules.** Em-dashes are banned, period. Replace with colons (label : explanation), semicolons (clause ; clause), or parentheticals. The hyphen-minus is fine for compounds (mark-recapture, camera-trap, mixed-effects); the en-dash is fine for numeric ranges (2.1–4.6 captures per 100 trap-nights). The lab uses the Oxford comma. Quote marks are typographic in submitted manuscripts; straight quotes in code comments and supplementary scripts.

| If you would have written | Use instead |
|---|---|
| `label — explanation` | `label: explanation` |
| `clause — aside — clause` | `clause, aside, clause` or `clause (aside) clause` |
| `clause — pivot` | `clause; pivot` or two sentences |
| `noun — qualifier` | `noun, qualifier` or restructure |

---

## 4. Sentence rhythm

The default rhythm of the writing: average sentence length, variation, paragraph length, opening constructions.

`[adopter: describe sentence and paragraph rhythm in 3 to 4 sentences. Include any anti-patterns your lab has identified (e.g., "do not start three consecutive sentences with 'We'").]`

> **Example: the ecology lab uses these rhythms.** Mix longer clause-rich sentences (25 to 40 words) with shorter punchy ones (6 to 12 words). Avoid runs of three or more sentences of similar length. Vary sentence openings: no more than two consecutive sentences should begin with "We" or with a participial phrase. Paragraphs average 4 to 6 sentences; single-sentence paragraphs are reserved for emphatic Discussion claims.

---

## 5. Words to use

Signature phrases and verbs that recur in the lab's published work. This list is what teaches the model the lab's voice fingerprint.

`[adopter: list 10 to 20 phrases and verbs your lab uses repeatedly. Pull these from your group's recent published papers.]`

> **Example: the ecology lab uses these phrases.**
> - "To assess whether [X], we ..."
> - "We reasoned that ..."
> - "Consistent with [prior finding], ..."
> - "These patterns suggest that ..."
> - "One plausible mechanism is ..."
> - "By contrast, ..."
> - Verbs: *assess, characterise, detect, infer, model, partition, quantify, distinguish, surveyed, document*.

---

## 6. Words to avoid

The signature anti-patterns. Often more useful than the use-list, because LLM defaults skew toward these.

`[adopter: list 8 to 15 forbidden words, phrases, or grammatical patterns. Include LLM-default tells your lab finds particularly grating.]`

> **Example: the ecology lab avoids these.**
> - Superlatives: *groundbreaking, unprecedented, revolutionary, transformative, novel* (when overused).
> - Empty intensifiers: *significantly* without a number, *markedly increased*, *highly diverse* without a metric.
> - Apologetic hedging on facts: "It may be possible that the data suggest ..."
> - Causation language for correlational findings: *demonstrates, proves, establishes* (unless mathematical).
> - Dramatic framing: *crisis, dire, catastrophic* in primary research papers (reserved for conservation perspectives where the framing is load-bearing).
> - Em-dashes (per section 3).
> - Run-on use of *however*: at most once per paragraph.

---

## 7. Authoring vs editing

A critical distinction: when the model is authoring fresh prose (drafting from notes, expanding bullets, generating an abstract from scratch), the voice file applies fully. When the model is editing existing human-written prose, the voice file applies narrowly: typos, grammar, factual errors, and explicit voice violations are fair game; sentence restructuring is not. This protects authorial intent.

`[adopter: state your lab's editing scope. What is the model allowed to change in human-written drafts? What is off-limits?]`

> **Example: the ecology lab scopes editing.** When editing the lab head's writing or any submitted manuscript, the model may fix: typos, grammar errors that change meaning, factual errors, citation errors, and explicit voice violations from sections 5 and 6 above. The model may NOT: restructure paragraphs, reorder arguments, soften strongly-stated claims, or substitute verbs for stylistic preference. When asked to "tighten" or "polish," ask which scope is meant before editing.

---

## 8. Writing evolution

How the lab's voice has changed over time and what direction it is heading. Useful for the model when it is reading older papers as exemplars: the older voice may not be the current voice.

`[adopter: briefly describe how the lab's voice has shifted (or note that it is stable). 2 to 4 sentences.]`

> **Example: the ecology lab notes this shift.** Papers published before 2020 use heavier passive voice and longer Methods exposition; the current voice has moved toward more active Results narration and shorter Methods sections that defer to a structured supplementary protocol. When using pre-2020 papers as voice exemplars, weight the more recent ones more heavily.

---

## 9. Voice exemplars

Two or three specific published papers from the lab that exemplify the current voice. The model should re-read these when uncertain about tone.

`[adopter: list 2 to 3 papers from your lab's catalogue, with section-level pointers (e.g., "the discussion of paper X is a clean voice example").]`

> **Example: the ecology lab uses these exemplars.**
> - Paper A (2024 *J. Anim. Ecol.*): Introduction and Discussion. Citation-dense, no superlatives, clean hedging on mechanistic claims.
> - Paper B (2023 *Methods Ecol. Evol.*): Methods. Passive-voice rationale-first paragraph openings.
> - Paper C (2025 *Ecography*): Abstract and final Discussion paragraph. The signature "These patterns suggest ... however, ... " structure used four times across the paper.

---

## Cross-references

- Document structure for manuscripts: `conventions/manuscript-format.template.md`
- Sentence-level patterns: see your fork's sentence-patterns reference if you ship one
- Pre-submission checks: see your fork's checklist reference if you ship one
- Reviewer-reply voice deltas: `conventions/reply-format.template.md`
- Figure and table voice: `conventions/figure-format.template.md`
