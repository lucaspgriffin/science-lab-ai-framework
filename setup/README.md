# setup/

## What this folder is for

Setup is the lab's on-ramp into the framework. Paper §3 argues that the value of a lab-specific AI assistant comes from lab-specific configuration: a generic voice convention, a generic agent roster, and an empty knowledge base produce generic outputs. Setup closes that gap by walking the lab through a structured interview that emits populated versions of the template files in `conventions/`, draft domain-specialist agents in `agents/`, and seeded topics in `knowledge_base/`.

Two interview modes are supported: a browser-based HTML form (good for human-first setup, with localStorage so the lab can pause and resume) and a `SKILL.md`-driven conversational interview (good for AI-assisted setup, where the model conducts the interview directly).

## Structure

```
setup/
├── README.md                                  this file
├── SKILL.md                                   conversational interview that an AI assistant runs
├── lab-onboarding.html                        browser form, equivalent in scope, localStorage-backed
└── prompts/                                   focused prompts for individual setup steps
    ├── voice-from-samples.md                  extract voice patterns from 3-6 sample papers
    ├── code-format-from-repo.md               extract code conventions from an existing repo
    └── kb-topic-seed.md                       seed a knowledge-base topic from a starter reading list
```

`SKILL.md` and `lab-onboarding.html` cover the same interview ground in different surfaces. The `prompts/` files are reused by both: each is a focused mini-task that can run inside the interview or be invoked separately when the lab wants to re-do one section.

## How to populate

This folder is itself the entry point, so "how to populate" here means "how to run setup". Two routes:

**HTML form route.** Open `setup/lab-onboarding.html` in a browser. The form walks through:

1. Lab basics (name, field, tooling defaults, target journals).
2. Voice samples (upload three to six recent papers; the form sends them to an AI assistant via the configured backend to extract voice patterns).
3. Format conventions (manuscript structure, figure style, code style).
4. Agent roster (which domain specialists the lab needs).
5. Knowledge-base topics (which three to five topics to seed first).

Form state persists in browser localStorage. At any step, the form can export a JSON answer file that the model uses to populate the framework, or the user can resume later.

**Conversational route.** Run `setup/SKILL.md` in a Claude Code (or compatible) session. The model conducts the same interview in dialogue, asking for sample files when needed and producing the populated convention and agent files directly. Useful when the lab already has an AI assistant configured and prefers a guided conversation.

In both routes, the output is the same: every `*.template.md` file in `conventions/` gets a non-template replacement; the `agents/_domain-specialist.template.md` produces one or more populated `<role>.md` files; the `knowledge_base/_topic.template/` produces one or more populated `<topic>/` directories with seeded `INDEX.md` and starter `raw/` summaries.

## What good looks like

A completed setup leaves the framework with:

- `conventions/voice.md` (replacing `voice.template.md`), populated from the lab's sample papers. The new file states the lab's hedging calibration, sentence-length norms, em-dash policy, and preferred verbs.
- `conventions/code-format.md` (replacing the template), populated from the lab's most recent project repository. The file names the language, project structure, plotting library, and naming conventions.
- `agents/camera-trap-wildlife-specialist.md` (or whichever specialist the lab needs), with defined scope, default protocols, and deferrals.
- `knowledge_base/<topic>/INDEX.md` for two or three topics, each with two to four seeded articles drawn from the lab's foundational reading list.

Here is the kind of question the interview asks, with an example ecology lab's answer:

> **Interview prompt.** Name three to five knowledge-base topics that capture the methods, taxa, and literatures your lab actually works on. For each, give a one-sentence scope statement.
>
> **Example ecology lab answer.**
> 1. *Camera-trap methods.* Deployment design, detection probability, species ID, and effort accounting for small-mammal community studies.
> 2. *Occupancy modelling.* Single-season, dynamic, and multi-species occupancy frameworks for repeat-survey detection histories.
> 3. *Small-mammal microhabitat selection.* Structural and climatic drivers of habitat use in temperate-forest small mammals.
> 4. *Vegetation-climate response.* Community-level vegetation shifts along climate gradients, and how those shifts couple to small-mammal habitat structure.
>
> The interview then asks the lab to name three to six foundational sources per topic and uses `prompts/kb-topic-seed.md` to compile starter articles.

## How it connects

- **Templates throughout the framework.** Setup is the only step that converts `*.template.md` files into non-template lab-specific versions. Skills and agents reference the non-template names; until setup runs, they fall back to the templates.
- **Prompts are reusable.** Each `prompts/<step>.md` is a self-contained mini-task. The lab can re-run any one of them (e.g., re-extract voice from a new batch of papers) without re-doing the full interview.
- **Dashboard reflects setup state.** `tools/generate-state.js` reports which conventions are populated versus still templated. A fresh dashboard after setup should show high coverage; gaps surface what is still missing.
- **Iteration workflow refines setup outputs.** Setup produces a v1. The iteration workflow defined in `conventions/iteration-workflow.md` is how the lab refines the conventions, agents, and KB topics over time as projects surface gaps.
