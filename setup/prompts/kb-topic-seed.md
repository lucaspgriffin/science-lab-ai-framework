# Knowledge-base topic seeding

A prompt template invoked by `setup/SKILL.md` Phase 6. Used to scaffold the first three knowledge-base topics for a newly onboarded lab, with research-integrity conventions enforced from the start.

## Inputs

- Three topic names (filesystem-safe, kebab-case) chosen by the adopter.
- For each topic: a one-line scope statement and two or three placeholder article titles.
- Lab identity from Phase 1 (used to tune the scope of the topic to the lab's actual practice).

## Prompt body (run for each of the three topics)

For each topic, build the folder skeleton in `knowledge_base/<topic>/` as follows.

### Step 1: Create the topic folder

Create `knowledge_base/<topic>/` if it does not exist.

### Step 2: Write `INDEX.md`

The index is a short overview that tells future readers (human or model) what the topic covers, where it fits in the lab's domain landscape, and what articles exist or are planned. Structure:

```
# <Topic name in title case>

> Scope: <one-line scope statement from the adopter>

## What this topic covers

<2 to 3 sentences expanding the scope statement. Describe the methods, organisms, systems, or questions that fall inside the topic. Be specific: vague scopes lead to vague articles.>

## Cross-references

<List 1 to 3 sibling topics in this lab's knowledge base, if any, with a short note on how they connect. Leave a placeholder if no siblings exist yet.>

## Articles

- [<article title 1>](./<article-slug-1>.md): <one-line summary>
- [<article title 2>](./<article-slug-2>.md): <one-line summary>
- [<article title 3>](./<article-slug-3>.md): <one-line summary>

## Maintenance notes

- Last updated: <YYYY-MM-DD>
- Source-integrity convention: all cited claims in this topic follow `conventions/research.md`. New articles are drafted using the Literature Extractor and Extraction Validator agents for any quantitative or attributed claim. See `agents/literature-extractor.md` and `agents/extraction-validator.md`.
```

### Step 3: Write one placeholder article per stated title

For each of the 2 to 3 placeholder article titles the adopter named, create `knowledge_base/<topic>/<article-slug>.md` with:

```
# <Article title>

> Status: scaffolded, not yet written. The structure below is a starting point; replace placeholder text with researched content before this article is cited in any deliverable.

## Scope

[adopter: 2 to 3 sentences naming the question, method, or system this article covers]

## Key concepts

[adopter: 3 to 6 bulleted concepts that anchor the article]

## Methods or approaches

[adopter: describe the relevant methods or approaches; include equations or pseudocode where appropriate]

## Open questions and limitations

[adopter: list the known unknowns and the boundaries of current understanding]

## References

[adopter: populate this section using the Literature Extractor agent. Every cited claim must trace to a verifiable source. The Extraction Validator agent should run a final pass on this section before any downstream use.]

## Cross-references

- Parent topic: [<topic name>](./INDEX.md)
- Related articles in this lab's KB: [adopter: add as the KB grows]
- Related conventions: `conventions/research.md`

## Maintenance notes

- Scaffolded on: <YYYY-MM-DD>
- Last reviewed: pending first content pass
```

### Step 4: Source-integrity enforcement

For each article scaffold, the `## References` section explicitly directs the future author (human or model) to use the Literature Extractor and Extraction Validator agents. This is non-negotiable: it is the framework's mechanism for keeping the knowledge base trustworthy.

Do not pre-populate references during scaffolding. The adopter must do the literature pass with the proper agents; pre-populated references would risk hallucinations entering the knowledge base on day one.

## Voice constraints

The generated `INDEX.md` and article scaffolds must comply with the framework voice rules:

- No em-dashes anywhere in the prose (use colons, semicolons, parentheses, or restructure).
- No superlatives in scaffold text.
- Scaffold text should be terse and informative, not chatty.

## Worked example (the example ecology lab)

The example ecology lab seeds three topics:

1. `camera-trap-methods` (scope: deployment design, detection probability, species ID).
2. `occupancy-modelling` (scope: single-season, dynamic, and multi-species occupancy frameworks).
3. `small-mammal-microhabitat` (scope: microhabitat selection, structural drivers, community-level response).

For `camera-trap-methods`, two placeholder articles: `detection-probability.md` and `deployment-design.md`. The `INDEX.md` cross-references `occupancy-modelling` (detection probability is the structural link to occupancy inference) and `small-mammal-microhabitat` (microhabitat covariates often drive detection structure).

This worked example is illustrative only. Strip it from any generated file.

## Output paths

- `knowledge_base/<topic-1>/INDEX.md` and 2 to 3 article scaffolds.
- `knowledge_base/<topic-2>/INDEX.md` and 2 to 3 article scaffolds.
- `knowledge_base/<topic-3>/INDEX.md` and 2 to 3 article scaffolds.
