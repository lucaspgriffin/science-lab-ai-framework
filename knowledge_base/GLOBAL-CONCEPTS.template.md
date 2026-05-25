# Knowledge Base: Global Concept Map (template)

> Domain taxonomy and cross-topic connections across all knowledge-base topics.
> Replace placeholder content with the lab's own domains, topics, and bridges.
> Last updated: YYYY-MM-DD.

## How to use this file

This file lives at `knowledge_base/GLOBAL-CONCEPTS.md`. It serves three purposes:

1. **Domain taxonomy.** A flat, readable map of which topics belong to which broad domain.
2. **Cross-topic bridges.** Tables of `from → to` connections that show how concepts in one topic inform or constrain concepts in another. These bridges are where most of the lab's distinctive thinking lives.
3. **Research identity statement.** A short closing section that names the conceptual bridges defining the lab's research program.

When a new topic enters the KB, update the domain hierarchy and add at least one bridge entry. When new connections surface during article compilation, add them to the relevant bridge table.

## Domain hierarchy

Replace this block with the lab's own domains and topics. Use a single tree that fits on screen.

```
Domain A (broad area)
├── topic-one              ← one-line topic description
├── topic-two              ← one-line topic description
└── topic-three            ← one-line topic description

Domain B (broad area)
├── topic-four             ← one-line topic description
└── topic-five             ← one-line topic description
```

### Worked example: the example ecology lab

```
Methods: detection and survey
├── camera-trap-methods                 ← deployment design, detection probability, species ID
├── mark-recapture                      ← live-trapping, closed-population, robust-design
└── vegetation-transects                ← line-intercept, point-quadrat, cover-class estimation

Biology: small-mammal ecology
├── small-mammal-microhabitat           ← microhabitat selection, structural drivers
└── population-dynamics                 ← demographic rates, year-to-year variation

Habitat and climate
├── vegetation-climate-response         ← community shifts along climate gradients
└── canopy-structure                    ← canopy openness, vertical structure, LIDAR-derived metrics

Statistics and computation
├── mixed-models                        ← GLMM/GAM for nested designs (lme4, glmmTMB, mgcv)
├── occupancy-modelling                 ← single-season, dynamic, multi-species occupancy
└── joint-species-distribution          ← JSDMs, community-level inference
```

## Cross-topic bridges

For each bridge, name the `from → to` pair, the topics it connects, and the substantive reason the connection matters. Worked example below.

### Example bridge 1: Methods ↔ Biology

The pipeline: camera-trap detection histories adjusted for detection probability provide the clean substrate on which microhabitat-selection inferences rest.

| From | To | Connection |
|------|----|-----------|
| camera-trap-methods/detection-probability | small-mammal-microhabitat/site-selection | Uncorrected detection probability biases inferred microhabitat preferences toward easy-to-detect sites |
| camera-trap-methods/species-id-confidence | population-dynamics/abundance-trends | Misclassification in species ID propagates into apparent trends |
| vegetation-transects/cover-class-estimation | small-mammal-microhabitat/structural-drivers | Cover-class summaries are the substrate for microhabitat-selection covariates |

### Example bridge 2: Statistics ↔ All applied topics

Quantitative methods are cross-cutting tools used throughout. Mixed models, in particular, appear in occupancy fits, abundance estimation, and vegetation analyses.

| From | To | Connection |
|------|----|-----------|
| mixed-models/random-effects | occupancy-modelling/site-level-effects | Random-site intercepts partition site-level heterogeneity from covariate effects |
| mixed-models/random-effects | vegetation-transects/plot-clustering | Plot-within-site random effects handle nested vegetation-survey designs |
| occupancy-modelling/dynamic-models | population-dynamics/colonisation-extinction | Dynamic occupancy parameterises colonisation and extinction directly |

### Example bridge 3: Biology ↔ Joint species distribution

Biological context (community composition, climate covariates, habitat structure) constrains which inferred species-level responses are plausible.

| From | To | Connection |
|------|----|-----------|
| population-dynamics/demographic-rates | joint-species-distribution/community-response | Demographic-rate priors anchor JSDM responses for data-poor species |
| vegetation-climate-response/community-shifts | joint-species-distribution/co-occurrence | Co-occurrence patterns are interpretable against the vegetation-climate substrate |

## Integration patterns

Recurring cross-topic concepts that appear in three or more bridges deserve a named pattern. Worked examples:

- **Detection probability** appears in `camera-trap-methods`, `mark-recapture`, and `occupancy-modelling`. The same imperfect-detection framing applies across detection-history sources.
- **Nested hierarchy** appears in `mixed-models`, `vegetation-transects`, and `occupancy-modelling`. The same plot-within-site or station-within-array structure recurs.
- **Climate covariates** appear in `vegetation-climate-response`, `small-mammal-microhabitat`, and `population-dynamics`. The same gridded-climate substrate is reused across the program.

When a pattern is named here, articles that participate in it should list the pattern in their Connections section.

## The lab's research identity

A two-to-three sentence statement of what the lab does that no other lab does in quite the same way. This is the elevator pitch in a static file. Update it when the program shifts.

### Worked example: the example ecology lab

The lab bridges (1) imperfect-detection field methods (camera traps and mark-recapture) and (2) community-level inference of small-mammal responses to vegetation and climate covariates by treating detection structure as a first-class component of the inference, not a nuisance. The anchor of the program is the long-running mixed camera-trap and live-trapping array applied across a canopy-cover gradient: a single design that simultaneously informs species occupancy, demographic rates, and the vegetation-climate covariates that drive them. Outputs target *Journal of Animal Ecology*, *Ecography*, and *Methods in Ecology and Evolution*.
