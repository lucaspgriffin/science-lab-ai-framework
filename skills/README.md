# skills/

## What this folder is for

The skills folder holds the executable instructions that an AI assistant loads when it takes on a substantive task. Each skill is a self-contained Markdown specification (a `SKILL.md`) plus optional reference files, describing how to plan, do, and check a piece of scientific work. Skills are the operational unit of the framework: paper §3 names them as the layer that turns a generic model into a lab-specific collaborator.

The folder splits into two routes: **simple skills** (a single phase of work the lab does daily) and **workflows** (multi-phase orchestrators that chain simple skills with state, checkpoints, and quality gates). Both run on the same model; the split is about scope and orchestration, not capability.

## Structure

```
skills/
├── simple/                          (9 single-phase skills for daily work)
│   ├── analysis-planning/           plan the statistical or computational approach
│   ├── code-writing/                produce code from a plan
│   ├── code-review/                 review code for correctness and diagnostics
│   ├── manuscript-writing/          draft or refine manuscript prose
│   ├── manuscript-builder/          render Markdown manuscript to .docx
│   ├── reply-writing/               draft a single reviewer-comment reply
│   ├── reviewer-reply-planning/     triage all reviewer comments
│   ├── reviewer-reply-drafting/     draft replies and tracked-changes manuscript
│   └── topic-writing/               synthesis, perspective, brief, blog post
└── workflows/                       (6 multi-phase orchestrated pipelines)
    ├── analysis-pipeline/           plan, code, review, finalise an analysis
    ├── research-iterate/            six-phase loop to publication-ready outputs
    ├── paper-research/              findings to manuscript reference document
    ├── expert-review/               simulated peer-review panel for a draft
    ├── manuscript-pipeline/         research, review, build the final .docx
    └── reviewer-reply-pipeline/     triage, draft, render tracked-changes .docx
```

Each skill directory contains at minimum a `SKILL.md`. Workflow skills also include phase-specific reference files (e.g., per-sub-agent prompts, state schemas).

## How to populate

There are two routes for installing or replacing skills:

**AI-assisted route (recommended).** Use the onboarding interview at `setup/`. The interview walks through each skill, asks how the lab works in that area, and produces a draft `SKILL.md` tuned to the lab's tooling and voice. See `setup/README.md`.

**Manual route.** Edit `SKILL.md` files directly. The shipped versions are vendor-neutral defaults; the structure is sound, but the example tooling (R, ggplot, *Nature* family targets) reflects one specific lab's setup. Find-and-replace is enough to retarget most skills; substantive changes (different language, different statistical defaults) require editing the phase descriptions.

When adding a new skill: create a folder under `simple/` or `workflows/`, write a `SKILL.md` following the conventions in `conventions/research.md` and any voice convention the lab maintains, then register it in `CLAUDE.md` and (if relevant) `tools/generate-state.js`.

## What good looks like

A skill that works well is short, opinionated, and grounded in lab specifics. Here is an excerpt from a populated `simple/analysis-planning/SKILL.md` for the example ecology lab:

> When planning a multi-species occupancy analysis on camera-trap data, default to a single-season community occupancy model (e.g., `ubms::stan_occu_community` or a hand-coded JAGS / Stan implementation) before any dynamic or N-mixture extension. The lab's prior projects (Project 2024-03, Project 2024-09) found that dynamic-occupancy fits inflated parameter uncertainty when fewer than three field seasons were available. If repeat seasons are unavailable, document the constraint in the plan and consult the Quantitative Scientist agent before proceeding.
>
> Pre-registration: the lab's default is to write the analysis plan as a Markdown document under `plans/<project>/analysis-plan.md`, commit it to the project repository before fitting any model, and reference it in the manuscript Methods section.

The skill stays under 300 lines, names concrete defaults, points at the agents and conventions it depends on, and tells the model what to do when its defaults do not apply. That is the bar.

## How it connects

- **Conventions.** Every skill loads the relevant convention files at session start. The "Required references" block at the top of each `SKILL.md` names exactly which files. See `conventions/README.md`.
- **Agents.** Workflow skills invoke specialist agents for parallel critique or domain expertise. See `agents/README.md` for the roster and the Lab Director routing pattern.
- **Knowledge base.** Skills that involve literature (paper-research, topic-writing, reply-writing) query the KB first via `knowledge_base/SKILL.md` before searching externally.
- **Tools.** The dashboard generator (`tools/generate-state.js`) scans this folder to report which skills are active and which still hold scaffolded defaults.
- **Setup.** New labs populate this folder via the interview at `setup/`; the interview reads the shipped `SKILL.md` files as templates and emits lab-specific replacements.
