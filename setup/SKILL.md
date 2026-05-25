---
name: lab-onboarding
description: Onboards a new lab into the science-lab-AI-framework by interviewing the adopter and populating template files in conventions/, agents/, and knowledge_base/. Use when the adopter says "set up the framework", "onboard my lab", "populate the templates", "run the lab interview", "configure science-lab-AI-framework for my group", or pastes an export from setup/lab-onboarding.html. Has two entry modes: ingest the HTML export text, or run a chat-driven interview that asks the same questions phase by phase.
---

# Lab onboarding: populating the science-lab-AI-framework for a new adopter

> The headline adopter feature. Takes a freshly forked copy of `science-lab-AI-framework` and turns it into a lab-specific working framework by filling in every `[adopter: ...]` slot across `conventions/`, seeding `agents/` with domain specialists, and scaffolding the first three `knowledge_base/` topics.

## When to trigger

Trigger this skill when the adopter says any of:
- "set up the framework"
- "onboard my lab"
- "populate the templates"
- "run the lab interview"
- "configure the framework for my group"
- "I forked science-lab-AI-framework, what now"

Also trigger automatically when the adopter pastes a text block whose first line reads `SCIENCE-LAB-AI-FRAMEWORK ONBOARDING` (the standard header emitted by `setup/lab-onboarding.html`).

## Inputs

One of:
1. **HTML export text.** The adopter has filled in `setup/lab-onboarding.html` and pasted the export. Skip to Phase 8 and just write files.
2. **Nothing.** Run Phases 1 through 7 as a chat-driven interview, ask one phase at a time, accumulate answers in working memory, then run Phase 8.

If the adopter is partway through (some answers in the export, some missing), fill what is present and run the chat-driven interview only for the missing phases.

## Outputs

The skill writes or updates these files in the adopter's fork of `science-lab-AI-framework/`:

| Target path | Source template | Phase that drives it |
|---|---|---|
| `conventions/voice.md` | `conventions/voice.template.md` | Phase 2 |
| `conventions/manuscript-format.md` | `conventions/manuscript-format.template.md` (or scaffold if absent) | Phase 3 |
| `conventions/code-format.md` | `conventions/code-format.template.md` (or scaffold if absent) | Phase 4 |
| `conventions/figure-format.md` | `conventions/figure-format.template.md` (or scaffold if absent) | Phase 4 |
| `conventions/research.md` | already populated; leave as-is unless adopter overrides | Phase 3 |
| `agents/<specialist>.md` | one file per Phase 5 specialist; scaffolded from `agents/quantitative-scientist.md` as a structural model | Phase 5 |
| `knowledge_base/<topic>/INDEX.md` | `knowledge_base/_topic.template/INDEX.md` (or scaffold if absent) | Phase 6 |
| `knowledge_base/<topic>/<seed-article>.md` | scaffolded placeholder | Phase 6 |
| `setup/onboarding-record.md` | new file, full transcript of adopter answers, for audit and re-run | Phase 8 |

All `.template` suffixes are dropped on save. The skill never overwrites a populated convention file without explicit confirmation.

## Phase 1: Lab identity

Ask for or extract:

- **Lab name** (short, used in headers and citations).
- **Principal investigator** (name and institution).
- **Domain** (e.g. terrestrial ecology; physical oceanography; behavioural neuroscience).
- **Subfield emphasis** (one or two sentences).
- **Methods stack** (e.g. camera traps + mark-recapture + occupancy modelling; multi-electrode arrays + spike sorting + manifold methods).
- **Primary outputs** (manuscripts, software releases, datasets, reports, all of the above).
- **Target journals** (top three to five).

These values populate the header block of every generated convention file and the YAML frontmatter of any new agent.

**Worked example (the example ecology lab).** Lab name: "Forest Small-Mammal Lab". PI: "Dr. Y, University of Z". Domain: "terrestrial ecology". Methods: "camera traps, live-trapping with mark-recapture, vegetation transects, occupancy modelling". Primary outputs: "primary research manuscripts, open-source R packages, field-method protocols". Target journals: "*Journal of Animal Ecology*, *Ecography*, *Methods in Ecology and Evolution*".

## Phase 2: Voice elicitation

The highest-leverage section. Two parts:

**Part A: paste 2 to 3 sample paragraphs** from the lab's recent published papers (intro, discussion, abstract). These are the primary signal.

**Part B: explicit preferences:**
- Default register (technical, methods-heavy / accessible / formal / informal).
- Hedging stance (aggressive / moderate / minimal).
- Banned words (the lab's signature anti-patterns; LLM tells they find grating).
- Signature phrases (verbs and constructions that recur in their papers).
- Em-dash policy (the framework default is hard-ban; adopter can override).

The skill loads `setup/prompts/voice-from-samples.md` and runs the embedded prompt against the pasted samples to infer hedging patterns, sentence rhythm, and vocabulary. Inferred rules are merged with the adopter's explicit preferences (explicit wins on conflict).

Output: a fully populated `conventions/voice.md` with every `[adopter: ...]` slot in `voice.template.md` resolved. Worked example blocks from the template are removed.

## Phase 3: Manuscript norms

Ask for or extract:

- Citation style (numeric, author-year, journal-specific).
- Reference manager (Zotero, EndNote, Paperpile, manual).
- Methods-section convention (deferred-to-supplementary vs in-text-detailed).
- Figure caption length (terse / standard / verbose).
- Abstract structure (structured headings vs single paragraph).
- Any journal-specific quirks (e.g. *Methods in Ecology and Evolution* application-paper conventions, BES journal preprint-first norms).
- Source-integrity stance (does the lab require verbatim quotation provenance for every cited claim, or accept paraphrase). This drives whether `conventions/research.md` needs softening or stays at the strict default.

Populates `conventions/manuscript-format.md`. If no template file exists, the skill writes a minimal scaffold matching the structure described in `CLAUDE.md`'s always-load conventions table.

## Phase 4: Code stack

Ask for or extract:

- **Primary language**: R, Python, both, other.
- **Conditional follow-ups:**
  - If R: tidyverse vs base vs data.table; preferred plotting (ggplot2 / lattice / base); package management (renv / pak / none).
  - If Python: scientific stack (numpy + pandas + scipy / polars / jax); plotting (matplotlib / seaborn / plotnine / plotly); environment management (uv / poetry / conda / pip + venv).
  - If both: which is dominant for analysis vs scripting.
- Project layout convention (e.g. `data/`, `R/`, `scripts/`, `outputs/`).
- Naming style (snake_case / camelCase / mixed).
- Version control (git only / git + GitHub / GitHub Actions / Zenodo deposits).
- Reproducibility expectations (containerised, lockfile, README-only, none).

Populates `conventions/code-format.md` and `conventions/figure-format.md`.

The skill loads `setup/prompts/code-format-from-repo.md` and offers to scan a sample script if the adopter wants the inferred conventions to come from real code rather than self-report.

## Phase 5: Agent roster

The framework ships with five general-purpose agents (Lab Director, Quantitative Scientist, Science Writer, Literature Extractor, Extraction Validator). Phase 5 asks which domain specialists the lab needs beyond these.

Suggest based on Phase 1 domain. For the example ecology lab, candidates are:
- `camera-trap-wildlife-specialist.md` (camera-trap deployment, detection probability, species ID)
- `small-mammal-population-ecologist.md` (mark-recapture, demographic rates, population dynamics)
- `vegetation-ecologist.md` (transect design, community composition, climate response)

Ask the adopter to:
1. Confirm or revise the suggested list.
2. For each chosen specialist, name two or three core sub-topics and two or three signature methods.

For each confirmed specialist, scaffold an agent file at `agents/<specialist>.md` using `agents/quantitative-scientist.md` as the structural model. The skill fills in: persona block, knowledge-base read-list, core methods, default deliverables. Leave the rest as scaffolding the adopter can elaborate on later.

## Phase 6: Knowledge-base seed

Ask the adopter to name three topics to seed first. These should be high-traffic concepts the lab will return to repeatedly (methods areas, organism systems, key questions). For each topic:

- Topic name (filesystem-safe, kebab-case).
- One-line scope statement.
- Two or three placeholder article titles (the actual articles will be filled in over time).

The skill loads `setup/prompts/kb-topic-seed.md` and runs the embedded scaffolding prompt. For each topic, it creates:

- `knowledge_base/<topic>/INDEX.md` (folder-level overview, scope, article list).
- `knowledge_base/<topic>/<placeholder-article>.md` (skeleton with section headers and a `[adopter: write this]` placeholder).

Research-integrity conventions are honoured: every article scaffold includes a top note pointing at `conventions/research.md` and instructing future contributors to use the Literature Extractor and Extraction Validator agents for any cited claims.

## Phase 7: Quality preferences

The `research-iterate` workflow runs an analysis through five quality gates (Analytic, Ecological/Domain, Visual, Literature, Framing). Ask the adopter which gates apply to their work and what convergence threshold each gate requires.

- **Analytic gate**: always on. Confirm thresholds (e.g. residual diagnostics pass, posterior predictive checks pass).
- **Domain gate**: rename to match the lab's field (e.g. "Ecological" for the example ecology lab; "Oceanographic" for a physical-oceanography lab; "Ethological" for a behavioural lab). Confirm the criteria.
- **Visual gate**: confirm the render-and-read protocol applies.
- **Literature gate**: confirm whether the lab requires literature contextualisation before publication-ready (some labs leave this for the manuscript phase).
- **Framing gate**: confirm whether the lab uses framing review (advocacy vs descriptive scoping).

Phase 7 outputs a short addendum file at `conventions/research-quality-gates-lab-overrides.md` (only created if any gate is renamed or has lab-specific thresholds). The base file is left untouched.

## Phase 8: File generation

Once all phases are answered, the skill writes everything in one pass and reports.

For each target file:
1. Read the corresponding `.template.md` (if present) or the structural model file.
2. Substitute every `[adopter: ...]` slot with the adopter's answer.
3. Remove worked-example blocks (these were instructional only).
4. Write to the target path with the `.template` suffix removed.
5. Set the YAML frontmatter (where applicable) with lab name, PI, generated-on date.

The skill also writes `setup/onboarding-record.md`: the full transcript of adopter answers across all phases, for audit, version control, and re-running the onboarding if templates evolve.

### Generation rules

- **Never overwrite a non-template file silently.** If `conventions/voice.md` already exists (not `voice.template.md`), pause and ask whether to overwrite, write to `voice.lab-onboarding.md` as a sibling, or skip.
- **Preserve template comments.** Any HTML-style comment in a template that begins with `<!-- keep -->` is copied verbatim.
- **Strip worked examples.** Every `> **Example: ...** ... ` block in a template is removed on generation (these are instructional only).
- **Apply voice constraints.** No em-dashes anywhere in generated text (use colons, semicolons, parentheses, or restructure). No superlatives in scaffold text.

## Verification step

After Phase 8, the skill reports a summary table:

```
Generated files:
  conventions/voice.md                                   (Phase 2)
  conventions/manuscript-format.md                       (Phase 3)
  conventions/code-format.md                             (Phase 4)
  conventions/figure-format.md                           (Phase 4)
  agents/camera-trap-wildlife-specialist.md              (Phase 5)
  agents/small-mammal-population-ecologist.md            (Phase 5)
  knowledge_base/camera-trap-methods/INDEX.md            (Phase 6)
  knowledge_base/camera-trap-methods/detection-probability.md   (Phase 6)
  knowledge_base/occupancy-modelling/INDEX.md            (Phase 6)
  knowledge_base/occupancy-modelling/multi-species-occupancy.md (Phase 6)
  knowledge_base/small-mammal-microhabitat/INDEX.md      (Phase 6)
  setup/onboarding-record.md                             (audit trail)
```

The skill then prompts the adopter to:

1. Open each generated file and read it end to end.
2. Edit anything that does not match the lab's actual practice (the skill's inferences are starting points, not contracts).
3. Commit the populated files to version control with a clear message ("Onboarded science-lab-AI-framework for [Lab Name]").
4. Optionally re-run the onboarding skill later if any phase needs to be revisited (the onboarding record makes this cheap).

## Modes

### Mode A: ingest HTML export

If the adopter pastes an export block from `setup/lab-onboarding.html`:

1. Parse the export (sections delimited by `## <phase name>`).
2. Validate that all required phases are present. If any are missing, switch to Mode B for those phases only.
3. Skip the interview, go straight to Phase 8.

### Mode B: chat-driven interview

If no export is provided:

1. Show the adopter the phase list and offer to start at Phase 1 or jump to a specific phase.
2. Ask one phase at a time. Confirm understanding before moving to the next.
3. For Phase 2, accept pasted sample paragraphs as input. Run `setup/prompts/voice-from-samples.md` to extract inferred rules.
4. For Phase 4, optionally accept a path to a sample script. Run `setup/prompts/code-format-from-repo.md` to extract inferred conventions.
5. After Phase 7, summarise everything back to the adopter for confirmation, then run Phase 8.

## Cross-references

- The HTML form: `setup/lab-onboarding.html`. Self-contained, runs in any modern browser, saves to localStorage, exports as plain text.
- Voice-inference prompt: `setup/prompts/voice-from-samples.md`.
- Code-inference prompt: `setup/prompts/code-format-from-repo.md`.
- Knowledge-base seeding prompt: `setup/prompts/kb-topic-seed.md`.
- The companion paper (Brownscombe et al., in preparation) for the framework architecture and rationale.
