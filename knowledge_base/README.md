# knowledge_base/

## What this folder is for

The knowledge base is the lab's accumulated thinking, organised by topic and held in Markdown files that an AI assistant can read, query, and update. Paper §3 frames it as the long-term memory layer: skills supply procedural knowledge ("how to plan an analysis"), agents supply role-specific judgement ("how a quantitative scientist would frame this"), and the knowledge base supplies the lab's *content* (what the lab has read, what it has decided, what it has concluded). All three layers are needed for the model to act as a real collaborator rather than a generic assistant.

The KB is inspired by the LLM-compiled-wiki pattern: raw sources land in `raw/` directories, an AI assistant compiles them into encyclopedic articles in `articles/`, and indices and concept maps are maintained as the corpus grows.

## Structure

```
knowledge_base/
├── SKILL.md                     workflow definitions: ingest, compile, query, maintain
├── GLOBAL-CONCEPTS.template.md  template for the cross-topic concept map
├── README.md                    this file
├── _topic.template/             scaffold for a new topic
│   ├── INDEX.md                 topic overview, articles list, cross-references
│   └── example-article.md       template for an individual article
└── <topic-name>/                one directory per topic the lab works on
    ├── INDEX.md
    ├── CONCEPTS.md
    ├── raw/
    └── articles/
```

The framework ships without any populated topics. The `_topic.template/` directory is the scaffold; copy it to start a new topic.

## How to populate

**AI-assisted route.** The onboarding interview at `setup/` asks the lab to name three to five topics it cares about most, then walks through one topic in depth: the foundational papers the lab would seed it with, the concept vocabulary that recurs in lab discussions, and the recurring debates. The interview emits a populated `INDEX.md` plus two or three stub articles for that topic. The remaining topics are seeded as stubs for later filling. See `setup/README.md`.

**Manual route.** Copy `_topic.template/` to `<topic-name>/`. Fill in `INDEX.md` (topic overview, key concepts, expected articles, cross-references). Ingest two or three foundational sources into `raw/` using the format in `_topic.template/example-article.md`. Run the **Compile** workflow defined in `SKILL.md` to generate initial articles.

When adding a new topic, also update `GLOBAL-CONCEPTS.md` to register it in the domain hierarchy and define at least one cross-topic bridge.

## What good looks like

A topic that works well has between five and twenty articles, an `INDEX.md` that a new lab member can skim in three minutes to orient, and a `CONCEPTS.md` that shows how the topic connects outward. Here is an excerpt from a populated `camera-trap-methods/INDEX.md` for the example ecology lab:

> ## Topic overview
> Camera-trap methods for small-mammal community studies. Covers deployment design (station spacing, lure protocols, camera-model selection), detection-probability modelling, species-identification protocols, and effort accounting (trap-night summaries). Does not cover downstream community-level inference (see `occupancy-modelling`) or mark-recapture (see `mark-recapture`).
>
> ## Articles in this topic
> | Article | Summary |
> |---------|---------|
> | detection-probability | `unmarked` single-season occupancy is the lab default; covariate-driven detection structure |
> | species-id-confidence | AI-assisted classification vs. expert review; inter-observer agreement |
> | deployment-design | Station spacing, lure protocols, and array geometry |
>
> ## Cross-references
> - occupancy-modelling: detection probability is the structural link from histories to inference
> - mixed-models: random-site effects partition station-level heterogeneity

The index is short, opinionated (it names a lab default), and shows the boundaries of the topic. That is the bar.

## How it connects

- **research.md is the source-faithfulness contract.** Every ingestion, every article update, every citation must comply with `conventions/research.md`. The KB is the most citation-heavy artefact the lab produces; a single fabricated citation undermines the lab's manuscripts that draw from it.
- **literature-extractor and extraction-validator agents are the validation pair.** All quantitative extraction from sources runs through `agents/literature-extractor.md` (producer) and `agents/extraction-validator.md` (checker). The checker re-reads cited pages and confirms every number, date, and named claim matches the source. This is not optional.
- **paper-research, topic-writing, reply-writing skills query the KB first.** Before searching externally, these skills check whether the lab has already compiled relevant material. The KB-first pattern keeps the lab's distinctive perspective in the foreground.
- **The Maintain workflow runs periodically.** Monthly, or after a major ingestion batch, run **Maintain** (defined in `SKILL.md`) to find broken cross-references, missing connections, and stale articles. The dashboard at `tools/` flags health metrics.
- **GLOBAL-CONCEPTS.md is the cross-topic map.** When two topics share a concept (e.g., "noise modelling" appears in QC and in network inference), name the bridge in `GLOBAL-CONCEPTS.md`. Articles that participate in a named bridge reference it in their Connections section.
