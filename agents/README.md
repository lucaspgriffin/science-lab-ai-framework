# agents/

## What this folder is for

Agents are role-specific personas that an AI assistant adopts (or dispatches sub-agents into) when a task needs concentrated expertise rather than general competence. Paper §3 frames them as the layer where the lab's research-group structure becomes computational: a director who routes, specialists who deliver, and validators who check. The framework ships five core agents plus a template for adding domain specialists.

Agents are not separate models. They are persona definitions that the same underlying model loads into context when invoked. The benefit is focus: an agent prompt that defines "you are the lab's quantitative scientist" with clear scope, defaults, and refusal conditions outperforms a generalist prompt on statistical tasks.

## Structure

```
agents/
├── lab-director.md              orchestrator: routes tasks, integrates outputs, runs QA
├── quantitative-scientist.md    statistics, ML, code, diagnostics; always-on for analysis
├── science-writer.md            literature search, drafting, expert review
├── literature-extractor.md      verbatim quantitative extraction with provenance
├── extraction-validator.md      source-faithfulness verification (re-reads cited pages)
└── _domain-specialist.template.md   template for adding lab-specific specialists
```

(The `_domain-specialist.template.md` file is a slot for the lab to add agents for its own fields, e.g., a "camera-trap wildlife specialist", "movement ecologist", "vegetation ecologist", or "climate modeller". The framework intentionally ships without these because they are inherently lab-specific.)

## How to populate

**AI-assisted route.** The onboarding interview at `setup/` includes an agent-design step. It asks the lab what kinds of expertise its members bring, what kinds of mistakes their work most often makes, and which roles should be standing versus ad-hoc. The interview emits a draft `<agent>.md` per role. See `setup/README.md`.

**Manual route.** Copy `_domain-specialist.template.md` to `<role>.md` and fill in: scope (one paragraph), defaults (concrete: which methods, which tooling, which references), refusal conditions (when this agent should defer), and integration notes (which conventions this agent loads, which other agents it works alongside). Keep agent files under 200 lines; longer prompts dilute focus.

When adding an agent, register it in `CLAUDE.md` under the agent roster and update the Lab Director's routing notes so it knows when to dispatch the new specialist.

## What good looks like

A domain-specialist agent that works well is narrow, opinionated, and aware of its boundaries. Here is an excerpt from a populated `agents/camera-trap-wildlife-specialist.md` for the example ecology lab:

> You are the lab's camera-trap wildlife specialist. Your domain is small-mammal community ecology from camera-trap and mark-recapture data, with a focus on detection probability, deployment design, and occupancy modelling. The lab's default tooling is R (unmarked, ubms, secr) for detection-history modelling and tidyverse for cleaning and joining detection records to site covariates.
>
> When a task involves a new camera-trap dataset, your default sequence is: independent-detection thresholding (typically 30 minutes between consecutive detections of the same species at a station), species-ID confidence scoring, and an effort summary (trap-nights by station and survey) before any occupancy model is fit. Justify any deviation in the analysis plan.
>
> Defer to the Quantitative Scientist for: hierarchical-model specification beyond standard occupancy and N-mixture parameterisations, prior choice for Bayesian fits, and any non-standard distribution choice. Defer to the Lab Director for: study-design questions, manuscript framing, and cross-domain integration with vegetation transect work.
>
> Always consult `knowledge_base/camera-trap-methods/INDEX.md` and `knowledge_base/occupancy-modelling/INDEX.md` before designing a new analysis. The lab has accumulated method notes there.

The agent has a defined scope, a named default protocol, explicit deferrals to other agents, and pointers into the lab's accumulated knowledge. That is the bar.

## How it connects

- **Lab Director routing.** Workflow skills invoke the Lab Director first; the Director reads the task, decides which specialist(s) to dispatch, and integrates their outputs. See `lab-director.md` for the routing logic.
- **Quantitative Scientist rule.** Any task involving data analysis dispatches the Quantitative Scientist alongside the domain specialist. This is a hard rule, codified in the Director's routing prompt.
- **Validation pair.** `literature-extractor.md` and `extraction-validator.md` operate as a producer-checker pair for any task that handles citations or quantitative facts from sources. They are invoked by `knowledge_base/SKILL.md` (ingestion), `paper-research` (literature synthesis), and `reviewer-reply-drafting` (citation-anchored replies).
- **Conventions.** Every agent's prompt loads `conventions/research.md` at minimum, plus any voice or format convention relevant to its output type.
- **Skills.** Agents are called from skills, not directly from the user. The skill defines what to do; the agent defines who is doing it. Adding a new agent typically requires updating the relevant skill's "dispatch" step.
