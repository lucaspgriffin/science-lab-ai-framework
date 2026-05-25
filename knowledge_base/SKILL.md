# Knowledge Base Skill: LLM-compiled topic wikis

> Read this file whenever building, updating, querying, or maintaining the lab's knowledge base.

## What this is

A collection of topic-organised Markdown wikis that an AI assistant builds and maintains from raw source material. Each topic is a directory containing:

- `raw/` for source documents (PDFs, clipped articles, notes, dataset summaries)
- `articles/` for AI-compiled wiki articles (one `.md` per concept)
- `INDEX.md` for an auto-maintained list of articles with one-line summaries
- `CONCEPTS.md` for a concept map showing relationships between articles

The knowledge base is not a static reference. It is a living compilation that grows as new sources are ingested and connections are discovered. Treat it as the lab's accumulated thinking, not as a search index.

## Directory structure

```
knowledge_base/
├── SKILL.md                ← this file
├── GLOBAL-CONCEPTS.md      ← domain hierarchy and cross-topic connection map
├── _topic.template/        ← template for new topics
└── <topic-name>/           ← one directory per topic the lab works on
```

Each topic directory contains:

- `INDEX.md` (auto-maintained article index with a `domain:` field in YAML frontmatter)
- `CONCEPTS.md` (concept map covering internal and cross-topic relationships)
- `raw/` (source PDFs, clipped articles, notes)
- `articles/` (compiled wiki articles)

### Domain hierarchy

Topics are organised into broad domains via metadata, not directories. The `domain:` field in each topic's `INDEX.md` frontmatter and each article's frontmatter enables grouping and querying by domain. Articles spanning domains use `domains: [primary, secondary]`. See `GLOBAL-CONCEPTS.md` for the full domain map.

For the example ecology lab, topics might organise as:

| Domain | Topics |
|--------|--------|
| Methods: detection and survey | camera-trap-methods, mark-recapture, vegetation-transects |
| Biology: small-mammal ecology | small-mammal-microhabitat, population-dynamics, community-composition |
| Habitat and climate | vegetation-climate-response, canopy-structure, climate-covariates |
| Statistics and computation | mixed-models, occupancy-modelling, joint-species-distribution |

### Adding a new topic

1. Copy `_topic.template/` to `knowledge_base/<topic-name>/`.
2. Fill in the stub `INDEX.md` (set `topic:` and `domain:`).
3. Fill in the stub `CONCEPTS.md` with cross-topic placeholders.
4. Register the topic in `CLAUDE.md` and in `GLOBAL-CONCEPTS.md`.
5. Run the **Compile** workflow to populate articles from raw sources.

## Workflows

### 1. Ingest: adding raw material

**Trigger:** "add this to the knowledge base", "ingest this paper", "clip this for <topic>".

**Required convention:** Load `conventions/research.md` before ingesting. Source-faithfulness rules apply to every claim that lands in an article.

Two ingestion modes:

#### a) Full raw summary (for foundational papers and reviews)

For papers the lab will reference repeatedly (its own publications, foundational reviews), create a dedicated `raw/` Markdown file:

1. Read the PDF or HTML source.
2. Use the `literature-extractor` agent (see `agents/literature-extractor.md`) for any quantitative facts. Verbatim extraction with page-level provenance is mandatory; the agent does not paraphrase numbers.
3. Save a structured summary to `raw/` as `[Author Year] - [short title].md` with this YAML frontmatter:

```yaml
---
source_type: paper | preprint | dataset | notes
title: "Full title"
authors: "Author list"
year: 2024
journal: "Journal name"
doi: "10.xxxx/yyyy"
date_ingested: 2026-05-25
tags: [concept1, concept2]
---
```

4. Run the `extraction-validator` agent (see `agents/extraction-validator.md`) on the summary before compiling. It performs the source-faithfulness checks defined in `conventions/research.md`.

#### b) Direct compilation (for bulk literature)

For a large reference library, skip the per-paper raw summary:

1. During article compilation, read the relevant source directly.
2. Synthesise findings into the article, citing the source in the article's Sources section.
3. Reference the source by filename plus DOI.
4. The article's Sources section serves as the citation record.

**When to use which:** raw summaries for sources you will reference across multiple articles; direct compilation for sources that contribute to one article only.

#### c) Pending queue from scheduled briefings

If the lab runs a literature-alert task, that task should emit pre-validated candidates into the KB in two forms (without writing articles directly):

- Per-topic pending files at `knowledge_base/<topic>/raw/_pending-YYYY-MM-DD.md` for high-signal candidates.
- A global seen-DOI registry at `knowledge_base/_seen-dois.txt` for deduplication.

The **Maintain** workflow processes these pending entries.

### 2. Compile: building and updating the wiki

**Trigger:** "compile the knowledge base", "update the wiki", "integrate the new sources".

**Required conventions:** `conventions/research.md` (source-faithfulness), plus any writing-voice conventions the lab has set.

**Process:**

1. Scan `raw/` for unprocessed sources (compare against article `sources:` frontmatter).
2. For each new source:
   a. Extract key concepts, findings, methods, and conclusions via `literature-extractor`.
   b. Determine which existing articles this connects to.
   c. Either update existing articles or create new ones using `_topic.template/example-article.md` as the skeleton.
3. Run `extraction-validator` on any article that gained new quantitative claims. The validator re-reads cited pages and confirms that each claim matches its source.
4. Update `INDEX.md` with the new article list and one-line summaries.
5. Update `CONCEPTS.md` with the new relationships.

Each article follows the structure shown in `_topic.template/example-article.md`. Key requirements:

- Every factual claim traces back to a source listed in the Sources section.
- The Connections section explains *why* concepts relate, not just *that* they do.
- Wiki-link syntax (`[[article-slug]]`) is used for internal cross-references.

### 3. Query: using the knowledge base

**Trigger:** "what does the KB say about <topic>", "summarise what we know about <concept>", "find connections between <A> and <B>".

**Process:**

1. Read the relevant topic's `INDEX.md` to identify which articles to consult.
2. Read those articles.
3. Synthesise an answer that cites specific sources from each article.
4. If the query reveals gaps, flag them and optionally create stub articles.

**Integration points with other skills:**

- **paper-research:** When starting a literature search for a manuscript, query the KB first. Existing articles provide a head start.
- **analysis-planning:** When designing a new analysis, check the KB for methodological articles that document how similar analyses have been run before.
- **topic-writing:** When drafting a synthesis or perspective, the KB is the first source to draw from before further literature search.

### 4. Maintain: health checks and cleanup

**Trigger:** "run a KB health check", "lint the knowledge base", "maintain the wiki".

**Process:**

1. **Process pending queues.** For each entry under `raw/_pending-*.md`, decide one of:
   - **Promote** to a full `raw/` summary.
   - **Cite-only:** add the source to one article's Sources section, then delete the pending file.
   - **Discard:** the briefing signal was a false positive. The DOI stays in `_seen-dois.txt` so it will not re-surface.
2. **Consistency check.** Are all raw sources reflected in at least one article? Are all `[[wiki-links]]` valid?
3. **Gap detection.** Are there concepts mentioned in articles that lack their own entries? Create stubs.
4. **Staleness check.** Are any articles citing outdated material that recent literature has superseded?
5. **Connection discovery.** Read across articles for implicit relationships missing from Connections.
6. **Index refresh.** Rebuild `INDEX.md` and `CONCEPTS.md` for any topic that changed.

Run Maintain periodically (monthly is a sensible cadence) or after a major ingestion batch.

## Conventions

### Article naming

- Kebab-case slugs: `doublet-detection.md`, `regulatory-network-inference.md`.
- Use the concept name, not an author name.
- Keep names concise but specific.

### Cross-references

- Wiki-link syntax (`[[article-slug]]`) for internal references. Compatible with Obsidian and most Markdown editors.
- In the Connections section, explain the relationship, not just its existence.

### Source attribution

- Every factual claim ties back to a source in the Sources section.
- Citation format: `[Author Year]` with a brief note about what that source contributes.
- Follow `conventions/research.md`: never fabricate references, verify claim-citation alignment via `extraction-validator`.

### Scope

- Articles are encyclopedic, not argumentative. Save argumentation for manuscripts.
- Write for a knowledgeable reader (graduate student or collaborator level).
- Include enough methodological detail to inform analysis planning.
- Flag genuine disagreements in the literature rather than picking sides.

### Quality over quantity

- A 20-article wiki where every article is well-sourced and well-connected is more useful than 100 thin stubs.
- Prefer depth in core topics over breadth across peripheral ones.
- Mark stubs explicitly so they can be expanded later.

## Seeding from existing literature

When starting the KB from a sizeable reference library, a sensible sequence is:

1. **Sort sources by topic.** Assign each PDF to one or more candidate topics.
2. **Prioritise reviews and foundational papers first.** They define the concept vocabulary that later papers will slot into.
3. **Batch-process** 8 to 12 sources per session, per topic.
4. **Deduplicate** by DOI before ingesting; the seen-DOI registry handles this if the lab uses scheduled briefings.

For the example ecology lab, a first pass might cover (i) camera-trap methodology reviews, (ii) the foundational papers on occupancy and N-mixture modelling (e.g., MacKenzie et al., Royle), (iii) small-mammal community ecology reference papers, and (iv) vegetation-transect method papers. Each becomes a `raw/` summary; each anchors one or more articles.

## Required references

- `conventions/research.md` (mandatory for any ingestion or citation work)
- `agents/literature-extractor.md` (for quantitative extraction from sources)
- `agents/extraction-validator.md` (for source-faithfulness verification)
- `_topic.template/` (file format for new topics and articles)
- `GLOBAL-CONCEPTS.md` (cross-topic map; update when adding topics)
