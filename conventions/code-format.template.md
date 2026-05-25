# Code format template: Project structure and coding conventions

> **This is a scaffold, not a finished file.** Copy it to `conventions/code-format.md` in your lab's working framework and fill in every `[adopter: ...]` slot. The worked examples use a running adopter scenario (a fictional terrestrial ecology lab using R + tidyverse for camera-trap, mark-recapture, and vegetation analyses). Delete the examples once you have written your own.

This file specifies how analysis code is organised, named, versioned, documented, and tested. It is the substrate for every analysis the lab produces; the code-implementation and code-review skills rely on it.

---

## 1. Default project structure

The directory layout the lab uses for any new analysis project. The model should create new projects following this template unless explicitly overridden.

`[adopter: state your default project directory tree. Include rules for what goes in each directory and which directories are gitignored.]`

> **Example: the ecology lab uses this structure.**
> ```
> project_name/
> ├── README.md                  # one-page project overview, primary contact, status
> ├── renv.lock                  # R environment lockfile
> ├── project_name.Rproj         # RStudio project file
> ├── config/
> │   └── config.yaml            # all run parameters; never hardcoded in scripts
> ├── data/
> │   ├── raw/                   # immutable, never modified after deposit; gitignored
> │   ├── processed/             # outputs of cleaning and joining; gitignored
> │   └── external/              # third-party reference data (climate rasters, range maps)
> ├── code/
> │   ├── 01_clean/              # data cleaning and joining
> │   ├── 02_model/              # model fitting (occupancy, GLMM, GAM)
> │   ├── 03_predict/            # prediction grids, marginal effects
> │   ├── figures/               # one script per main/supplementary figure
> │   └── exploratory/           # exploratory scripts (not used in final results)
> ├── results/
> │   ├── tables/                # final output tables (.csv, .xlsx)
> │   ├── figures/               # rendered figures (.pdf, .png)
> │   └── models/                # serialised model objects, with version pinning
> ├── manuscript/
> │   ├── main/                  # main-text markdown source
> │   ├── supplementary/         # supplementary documents
> │   └── refs/                  # .bib files
> └── tests/                     # unit tests for any reusable function (via testthat)
> ```
> The `data/raw/` and `data/processed/` directories are gitignored; everything else is version-controlled. A `data/raw/MANIFEST.md` lists the expected files and their source DOIs.

---

## 2. Naming conventions

`[adopter: state your conventions for file naming, variable naming, function naming, and any language-specific style (snake_case vs camelCase, etc.).]`

> **Example: the ecology lab uses these names.**
> - **Files**: `snake_case.R`. Scripts that produce a numbered figure: `fig_NN_short_descriptor.R` (e.g., `fig_03_occupancy_by_canopy.R`).
> - **Variables**: `snake_case` for new code; existing dot-naming in older code is grandfathered.
> - **Constants**: `UPPER_SNAKE_CASE`.
> - **Functions**: verb-first (`fit_occupancy_model`, `summarise_captures`). Avoid one-letter names except for trivial loop counters.
> - **DataFrames / tibbles**: suffix with their structure (`captures_df`, `sites_df`, `transects_df`).
> - **Files that are NOT reproducible** (one-off exploratory work): prefix with `scratch_` and place under `code/exploratory/`.

---

## 3. Version control

`[adopter: state your git conventions: branching, commit message style, what is committed, what is gitignored, and any pre-commit hooks.]`

> **Example: the ecology lab uses these git conventions.**
> - **Repository**: GitHub, public for published projects, private for in-progress.
> - **Branching**: `main` for the publication-ready state; feature branches for new analyses (e.g., `feature/occupancy-canopy`). Merge to main via pull request after code review.
> - **Commit messages**: imperative mood, under 72 characters for the subject line. Body explains the *why*. Reference issue numbers when relevant.
> - **Pre-commit hooks**: `styler` (R format), `lintr` (R lint).
> - **Gitignored**: `data/raw/`, `data/processed/`, large geospatial files (`*.tif`, `*.gpkg`), `.Rproj.user/`, `.Rhistory`, `.RData`, `renv/library/`, IDE settings.
> - **Release tagging**: at manuscript submission, tag `submission-vN`. At acceptance, tag `published-vN`. The published tag's commit hash is the code citation in the manuscript.

---

## 4. Documentation

`[adopter: state your conventions for docstrings, inline comments, READMEs, and any auto-generated documentation.]`

> **Example: the ecology lab uses these documentation conventions.**
> - **Functions**: roxygen2-style docstrings on every reusable function. Include parameter types, return types, and one example call.
> - **Scripts**: each script's first 20 lines are a header block: purpose, inputs, outputs, dependencies, author, last-modified date.
> - **Inline comments**: explain *why*, not *what*. The code is the *what*. Density: one comment per analytical step, not per line.
> - **README**: every project has a top-level README with the one-page project summary, how to set up the environment, how to run the workflow, and contact information.
> - **Methods generation**: the methods section of the manuscript is generated from the docstrings and config.yaml; the lab does not write methods text twice.

---

## 5. Testing

`[adopter: state your testing conventions: what gets tested, what does not, the test framework, and the coverage floor.]`

> **Example: the ecology lab uses these testing conventions.**
> - **Tested**: any reusable function (used across more than one script) gets unit tests. Statistical wrapper functions get test cases with known-answer inputs. Data-cleaning and parsing utilities get tests for malformed input (e.g., missing timestamps, duplicate capture records).
> - **Not tested**: one-off analysis scripts, exploratory scripts, figure-rendering scripts.
> - **Framework**: testthat.
> - **Coverage floor**: 80% line coverage for any function in `code/utils.R` or equivalent shared utility files. No coverage requirement for analysis scripts.
> - **CI**: GitHub Actions runs the test suite on every push to a feature branch.

---

## 6. Dependency management

`[adopter: state your dependency management strategy: tool, version pinning, environment recreation.]`

> **Example: the ecology lab uses these dependency conventions.**
> - **R**: `renv` for reproducible R environments. `renv.lock` is committed.
> - **Key packages**: tidyverse (data manipulation, plotting), lme4 / glmmTMB (mixed models), brms (Bayesian models), mgcv (GAMs), unmarked (occupancy and mark-recapture), sf and terra (spatial data).
> - **System tools**: containerised via Docker or Singularity for cluster jobs that depend on geospatial system libraries (GDAL, GEOS, PROJ). Container hash recorded in the methods.
> - **No** `install.packages()` without recording in `renv.lock`. Every project's environment is self-contained.

---

## 7. Performance patterns

`[adopter: state any house rules for performance: when to vectorise, when to parallelise, memory ceiling per process, and any commonly-misused patterns.]`

> **Example: the ecology lab uses these performance conventions.**
> - **Vectorisation**: always prefer vectorised operations (`dplyr`, `data.table`, `purrr::map`) over loops.
> - **Parallelisation**: long-running model fits use `future` + `furrr` with explicit worker counts pulled from `config.yaml`, not hardcoded. `brms` and `cmdstanr` use the chain-level parallelism from their own options.
> - **Memory**: long-running scripts declare their memory budget at the top of the file. The default per-script budget is 16 GB; scripts that exceed this require justification and a separate cluster queue.
> - **Spatial data**: rasters are read with `terra::rast()` and cropped to study-area extent before any operation. Vector data joins happen on simplified geometries when feasible.
> - **Antipatterns**: `for (i in ...) df[i, ] <- ...` (use `dplyr::mutate()` or `purrr::map_dfr()` instead); `rbind()` in a loop (use `dplyr::bind_rows()` on a list).

---

## 8. Logging and provenance

`[adopter: state your logging conventions and how analysis runs are reproducibly tracked.]`

> **Example: the ecology lab uses these provenance conventions.**
> - **Logging**: `futile.logger` or `cli` configured per-script with INFO-level default. Logs written to `results/logs/<script_name>_<timestamp>.log`.
> - **Workflow tracking**: long-running multi-step pipelines use `targets` (the R workflow framework) so each step is cached, parameterised, and re-runnable. The `_targets.R` file lives at the project root.
> - **Run identification**: every analysis run has a `run_id` derived from the git commit hash plus a UTC timestamp. The run_id appears in output filenames and in result-table metadata.
> - **Sessioninfo**: every script that produces a result calls `sessionInfo()` at the end and writes it to the log.

---

## 9. Code review conventions

`[adopter: state your code-review process. Who reviews? What is the checklist? How quickly?]`

> **Example: the ecology lab uses these review conventions.** Any pull request to `main` requires one reviewer who is not the author. Reviewers check: (1) does the code follow the section 2 to 7 conventions? (2) is the analytic step justified? (3) are diagnostics included where relevant? (4) does the README still accurately describe the project? Review turnaround is two business days. The code-review skill in `skills/workflows/code-review/SKILL.md` produces an initial automated review that the human reviewer then refines.

---

## 10. Anti-patterns

`[adopter: list anti-patterns specific to your lab's tooling that you have seen frequently and want flagged on sight.]`

> **Example: the ecology lab flags these.**
> - Hardcoded paths (`/Users/jdoe/project/data/...`); all paths go in `config.yaml` or are resolved via `here::here()`.
> - `library()` calls scattered throughout a script; all package loads happen in the script header.
> - Modifying `data/raw/` (immutable).
> - Reading large raster files without cropping to the study area first.
> - Random seeds not set; any stochastic step (bootstrap, MCMC, cross-validation fold assignment) needs a seed in `config.yaml`.
> - Suppressing warnings without explanation. Warnings exist for reasons; the code should either fix the underlying cause or document why the warning is acceptable.

---

## Cross-references

- Code-implementation skill: `skills/workflows/code-implementation/SKILL.md`
- Code-review skill: `skills/workflows/code-review/SKILL.md`
- Figure rendering conventions: `conventions/figure-format.template.md`
- Project goal specification: `conventions/goal-spec.template.md`
