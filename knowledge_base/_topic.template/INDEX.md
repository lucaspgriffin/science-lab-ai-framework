---
topic: "camera-trap-methods"
domain: "Methods: detection and survey"
description: "Camera-trap deployment, detection probability, species identification, and effort accounting for small-mammal community studies."
last_updated: 2026-05-25
article_count: 0
---

# Topic: <Topic name>

> Replace this file with the lab's own topic index. The block below is a working template plus a worked example for the placeholder topic "Camera-Trap Methods". Delete the worked example once the lab's own articles are in place.

## Topic overview

Two to three sentences describing what this topic covers, why it matters for the lab's research, and where its boundaries sit. The overview should make it clear when a new piece of literature belongs in this topic rather than a neighbouring one.

**Worked example:** Camera-trap methods for small-mammal community studies. Covers deployment design (station spacing, lure protocols, camera-model selection), detection-probability modelling, species-identification protocols, and effort accounting (trap-night summaries). Does not cover downstream community-level inference (see `occupancy-modelling`) or mark-recapture (see `mark-recapture`).

## Key concepts

A short bulleted list of the central concepts in this topic. Each bullet maps to an article (linked once written).

- **Detection probability.** Modelling per-station, per-survey detection rates as a function of camera, observer, and environmental covariates.
- **Independent-detection thresholding.** Setting the minimum interval between consecutive detections of the same species at a station to avoid pseudoreplication.
- **Species-identification confidence.** Confidence-scoring protocols for ambiguous camera-trap images, including AI-assisted classification and inter-observer agreement.
- **Deployment design.** Station spacing, lure choice, and array geometry; trade-offs between extent and density.
- **Effort accounting.** Trap-night summaries, station drop-out handling, and reporting standards.

## Articles in this topic

A list of compiled articles with one-line summaries. Auto-maintained by the **Compile** workflow.

| Article | Summary |
|---------|---------|
| [detection-probability](articles/detection-probability.md) | Modelling detection rates and the covariates that drive them |
| [species-id-confidence](articles/species-id-confidence.md) | Confidence scoring, inter-observer agreement, AI-assisted classification |
| [deployment-design](articles/deployment-design.md) | Station spacing, lure protocols, and array geometry |

When the topic has no articles yet, this table reads:

> *No articles yet. Run the **Compile** workflow once `raw/` contains at least one ingested source.*

## Cross-references to other topics

Connections out from this topic. Mirror the bridges named in `knowledge_base/GLOBAL-CONCEPTS.md`.

- **occupancy-modelling.** Detection probability is the structural link between raw detection histories and occupancy inference. See bridge: *Methods ↔ Statistics*.
- **mark-recapture.** Some studies combine camera detections with live-trap captures; the integration requires careful covariate alignment.
- **small-mammal-microhabitat.** Detection covariates often include vegetation structure, which couples to microhabitat-selection inference.

## Bibliography pointers

Where to find the underlying sources for this topic.

- `raw/` (this directory): per-source structured summaries with full provenance (DOI, page numbers, key claims). One Markdown file per ingested source.
- Lab reference library: `<path-to-library>/<topic-subdirectory>` (if the lab maintains a parallel PDF collection).
- Foundational reviews to ingest first: list two to four canonical reviews that set the topic's vocabulary.

**Worked example (for the placeholder camera-trap topic):**

- MacKenzie et al. 2002, *Ecology*, "Estimating site occupancy rates when detection probabilities are less than one" (DOI: 10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2). The foundational occupancy reference.
- Burton et al. 2015, *J Appl Ecol*, "Wildlife camera trapping: a review and recommendations for linking surveys to ecological processes" (DOI: 10.1111/1365-2664.12432). The standard methodological review.
- Rovero & Zimmermann 2016, *Camera Trapping for Wildlife Research* (Pelagic Publishing). The handbook reference.
