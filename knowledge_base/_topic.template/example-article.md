---
title: "Detection probability in camera-trap surveys"
slug: "detection-probability"
domain: "Methods: detection and survey"
domains: []                              # only set if article spans multiple primary domains
aliases: ["imperfect detection", "per-survey detection rate"]
related: [species-id-confidence, deployment-design, occupancy-modelling]
sources:
  - raw/MacKenzie_2002_Occupancy.md
  - raw/Burton_2015_CameraTrappingReview.md
  - raw/Royle_Nichols_2003_HeterogeneityDetection.md
status: published                        # one of: stub | draft | published
origin: manual                           # who/what wrote this article
last_updated: 2026-05-25
---

# Detection probability in camera-trap surveys

> Template article for the topic-scaffold. Replace with the lab's own article. Below is a worked example for the placeholder topic "Camera-Trap Methods".

## Summary

Detection probability is the per-survey, per-station probability that a target species is recorded given that it is present. In camera-trap studies of small mammals, detection probability is typically well below one, and treating raw detection histories as proxies for true occupancy biases inference. Modern occupancy and N-mixture models partition the observation process from the ecological process explicitly, allowing covariates to act on detection and on occupancy independently.

## Key points

### What detection probability is and why it matters

Camera-trap sampling produces a detection history per station per survey: a 1/0 vector indicating whether the focal species was recorded during each repeat survey. The per-survey detection probability p depends on station-level covariates (camera model, lure, microhabitat), survey-level covariates (deployment season, weather), and the species' own behaviour (activity level, body size, habitat use). If p is unmodelled, the naive proportion of stations where the species was detected understates true occupancy by a factor that depends on the number of surveys [MacKenzie et al. 2002, p.2249].

### How detection-probability modelling works

- **Single-season occupancy models** (the MacKenzie et al. 2002 framework) jointly estimate occupancy psi and detection probability p from a station-by-survey detection-history matrix. Likelihood combines a Bernoulli observation process on top of a Bernoulli ecological process.
- **Royle-Nichols heterogeneity models** treat per-station abundance as the latent quantity and let p scale with abundance, useful when sites differ in animal density rather than presence-absence [Royle & Nichols 2003, p.781].
- **Hierarchical N-mixture models** generalise to counts rather than detection-non-detection, parameterising both abundance and detection.

### Benchmark findings

Burton et al. (2015) reviewed 266 camera-trap studies and reported that **fewer than 40 percent reported detection-probability estimates**, even though detection bias is the largest single source of inference error in such studies [Burton et al. 2015, Table 2]. Among studies that did estimate p, per-survey detection probabilities for small carnivores ranged from 0.05 to 0.40 depending on station design and species, illustrating the wide variation that justifies explicit modelling.

### Practical recommendations

Plan a minimum of three to five repeat surveys per station to allow stable detection-probability estimates. Record candidate detection covariates at deployment (camera generation, lure type, microhabitat class, technician). Visualise the per-station detection rate before fitting the occupancy model; stations with zero detections across all surveys can still inform p if they are paired with stations where the species was detected at the same covariate values.

## Methods and approaches

For new datasets, the lab's default sequence is: (1) build a detection history per station, per species, per survey window, (2) fit a single-species occupancy model with detection covariates (camera, lure, season) using `unmarked`, (3) inspect detection-probability residuals against unmodelled covariates to surface missed structure, (4) graduate to multi-species or dynamic models only after the single-species model is well-behaved.

## Open questions

- The interaction between AI-assisted image classification and detection-probability estimation is under-studied: misclassification at the image level propagates into apparent detection structure, but few studies model this jointly.
- Detection-probability transferability across regions remains uncertain; pooled-design analyses across study areas are sparse.
- Continuous-time formulations (time-to-detection models) offer theoretical advantages over fixed-interval surveys but adoption in small-mammal work is limited.

## Connections

- **Related to:** [[species-id-confidence]]. Detection probability is conditional on correct species ID; classification errors at the image level masquerade as detection-probability variation.
- **Depends on:** [[deployment-design]]. Station spacing and lure choice determine the per-station detection ceiling.
- **Informs:** [[occupancy-modelling]]. Detection-probability structure is the bridge from raw histories to occupancy inference.
- **Pattern:** *Detection probability* (see `GLOBAL-CONCEPTS.md`). Imperfect detection is the shared challenge across camera traps, mark-recapture, and acoustic surveys.

## Sources

All claims trace to one of the entries below. Per `conventions/research.md`, every quantitative statement is verifiable from the cited page; the `extraction-validator` agent has confirmed claim-citation alignment.

- **MacKenzie et al. 2002.** "Estimating site occupancy rates when detection probabilities are less than one." *Ecology* 83: 2248-2255. DOI: 10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2. Pages 2249-2250 (likelihood derivation); page 2253 (covariate parameterisation).
- **Burton et al. 2015.** "Wildlife camera trapping: a review and recommendations for linking surveys to ecological processes." *Journal of Applied Ecology* 52: 675-685. DOI: 10.1111/1365-2664.12432. Table 2 (review of detection-probability reporting); pages 678-679 (recommended practice).
- **Royle & Nichols 2003.** "Estimating abundance from repeated presence-absence data or point counts." *Ecology* 84: 777-790. DOI: 10.1890/0012-9658(2003)084[0777:EAFRPA]2.0.CO;2. Page 781 (abundance-mediated detection model); Figure 2 (effect-size simulations).

## Template usage notes (delete in published articles)

- Set `status:` to `stub` for incomplete articles, `draft` for in-progress, `published` for complete.
- Set `origin:` to `manual`, `paper-research`, `kb-maintain`, or whatever workflow produced the article. The Maintain workflow uses this field to identify auto-generated content that may need human review.
- The Sources block is the audit substrate. Every claim must trace to one entry, with page or figure reference. The `extraction-validator` agent re-reads cited pages and verifies alignment before an article moves from `draft` to `published`.
