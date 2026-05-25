# conventions/

## What this folder is for

Conventions are the always-load rules that shape every piece of work the lab's AI assistant produces. Paper §3 names them as the layer that makes outputs feel like the lab rather than the model: a manuscript drafted by the model reads in the lab's voice because the voice convention shaped the prose; a citation appears in the manuscript only because the research-integrity convention forced the assistant to verify it. The conventions are short, opinionated, and loaded at the top of every relevant task.

The folder mixes two kinds of files: **opinionated** ones the framework provides as-is (research integrity, iteration mechanics, quality gates) and **template** ones the lab is expected to replace with its own version (voice, format, code style). The split is deliberate: research integrity is the same across labs; writing voice is not.

## Structure

```
conventions/
├── README.md                              this file
│
├── research.md                            (opinionated) research integrity: claim-citation alignment, no fabricated refs
├── iteration-workflow.md                  (opinionated) six-phase research-iterate loop
├── research-quality-gates.md              (opinionated) analytic, ecological, visual, literature, framing gates
├── visual-review-protocol.md              (opinionated) render-and-read protocol for figures
├── readiness-assessment.md                (opinionated) phase-0 expertise-coverage check
├── system-improvement-protocol.md         (opinionated) mechanical vs. structural change triage
│
├── voice.template.md                      (template) writing voice; replace for the lab
├── manuscript-format.template.md          (template) manuscript structure and section conventions
├── reply-format.template.md               (template) reviewer-reply voice and structure
├── code-format.template.md                (template) language, project structure, performance patterns
└── figure-format.template.md              (template) plotting library, table conventions, plotmath rules
```

The `.template.md` suffix marks files the lab is expected to replace. The plain-`.md` files are framework-level rules that should not be diluted; lab-specific extensions belong in additional files (e.g., `voice-fieldwork-supplement.md`).

## How to populate

**AI-assisted route.** The onboarding interview at `setup/` includes a conventions step that handles the template files in turn:

- For `voice.template.md`, the interview asks the lab to provide three to six recent paper drafts; an AI assistant extracts voice patterns (sentence length, hedging level, em-dash usage, preferred verbs) and produces a draft `voice.md`.
- For `code-format.template.md`, the interview reads the lab's most recent project repository and extracts its current code style; it surfaces conflicts and asks the lab to resolve them.
- For `figure-format.template.md`, the interview asks for three figures from recent papers and extracts plotting defaults.

The opinionated files are left untouched by the interview; they are framework defaults that the lab is expected to follow.

**Manual route.** Edit the `.template.md` files directly. Each file ships with worked-example content the lab can find-and-replace from. Once edited, drop the `.template` suffix so skills and agents can locate the file at its expected path.

When adding a new convention (e.g., a presentation-format convention for talks), name it `<topic>.md`, place it in this folder, and reference it from any skill or agent that should load it.

## What good looks like

A convention file that works well is under 300 lines, names concrete patterns, and includes examples of what *not* to do. Here is an excerpt from a populated `voice.md` for the example ecology lab:

> ## Hedging calibration
>
> Hedge only where the data warrant hedging. Three cases:
>
> - **Direct measurement, n adequate:** state the finding flat. "*Peromyscus maniculatus* occupancy was 0.62 (95% CI 0.54 to 0.69) across the 84-station array." Not: "*Peromyscus maniculatus* occupancy appeared to be moderately high across the array."
> - **Inferred relationship:** name the inference and its limit. "These patterns are consistent with canopy openness driving microhabitat selection; experimental thinning would test causality."
> - **Speculation past the data:** flag explicitly. "We speculate that this reflects a behavioural response to perceived predation risk, though no direct evidence is presented here."
>
> ## Em-dashes
>
> Do not use em-dashes (`—`) or double-hyphens (`--`) or spaced hyphens (` - `). Restructure with colons, semicolons, parentheses, or sentence breaks. The lab's submitted manuscripts have zero em-dashes.

The convention names the patterns, gives examples, and states the rule absolutely. That is the bar.

## How it connects

- **Every skill loads its required conventions at session start.** Each `SKILL.md` has a "Required references" block at the top listing the convention files the skill needs. Manuscript-writing loads voice plus manuscript-format; reply-writing adds reply-format; code-writing loads code-format.
- **Agents load conventions too.** A specialist agent's prompt includes the conventions relevant to its output type.
- **`research.md` is non-negotiable.** Any task that produces citations, ingests sources into the KB, or replies to reviewer comments about literature loads `research.md`. Skills enforce this by failing fast if the convention is not loaded.
- **Quality gates use the conventions as benchmarks.** The five quality gates in `research-quality-gates.md` cite specific conventions (visual gate cites `figure-format` and `visual-review-protocol`; framing gate cites `voice` and `manuscript-format`).
- **The system-improvement protocol updates conventions.** When user feedback reveals that a convention is wrong or incomplete (e.g., "stop using em-dashes"), the protocol in `system-improvement-protocol.md` defines how to update the convention and what to re-render.
