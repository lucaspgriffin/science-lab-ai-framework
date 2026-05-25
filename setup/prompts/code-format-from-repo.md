# Code-format inference from a sample script

A prompt template invoked by `setup/SKILL.md` Phase 4. Used to infer code-format rules from a representative script the adopter provides, then populate `conventions/code-format.md` from `conventions/code-format.template.md`.

## Inputs

- A path (or pasted content) of one representative script from the lab's recent work. Ideally an analysis script (200 to 600 lines) rather than a small utility.
- The adopter's explicit Phase 4 answers (primary language, plotting library, project layout, naming style, version-control practice, reproducibility expectations).

## Prompt body (run against the script)

Read the script end to end. Treat it as the canonical reference for the lab's style. Identify:

1. **Language and dialect.** R (tidyverse vs base vs data.table) or Python (numpy + pandas + scipy / polars / jax). Record library imports verbatim at the top of the file.

2. **Naming conventions.** Are variables snake_case, camelCase, or mixed. Are functions named with verbs (e.g. `fit_model`) or nouns. Are constants ALL_CAPS or lower. Are file names dated (e.g. `2026-05_analysis.R`) or descriptive (e.g. `fit-models.R`).

3. **Project structure cues.** Are there relative paths that imply a project layout (e.g. `read_csv("data/raw/cells.csv")` implies `data/raw/`). List every directory referenced.

4. **Section organisation.** How is the script broken up. Numbered headers (`# 1. Load data`), markdown-style (`## Load data`), or unstructured. Average size of each section.

5. **Comment density.** Comments per 50 lines of code. Are comments terse (one-liners labelling sections) or expository (multi-line rationale).

6. **Function patterns.** Are functions defined inline (closures) or in a `R/` or `src/` folder. Are they documented (roxygen, docstrings, none). Are arguments typed (Python type hints, R `checkmate` or no checks).

7. **Plotting style.** ggplot2 with a custom theme (find and record the theme function); matplotlib with rcParams; seaborn defaults; plotnine; plotly. If a theme function is defined, copy its signature.

8. **Reproducibility cues.** `set.seed()` calls; `sessionInfo()` or `pip freeze` at end; environment file references (`renv.lock`, `pyproject.toml`, `requirements.txt`); container references (`Dockerfile`, `.devcontainer`).

9. **Output handling.** Where do figures and tables get written. Are filenames timestamped, numbered, or descriptive. Are outputs git-tracked or gitignored.

10. **Error and edge-case handling.** Are there `tryCatch` / `try-except` blocks. Are NAs handled explicitly or assumed handled by upstream cleaning.

## Merging with explicit preferences

The adopter's explicit Phase 4 answers always win on conflict. The inference fills gaps the adopter did not explicitly cover.

If the explicit answer was "tidyverse" but the script uses base R, ask the adopter whether the script is representative or whether the lab is mid-transition. Record the resolution.

## Output

Populate every `[adopter: ...]` slot in `conventions/code-format.template.md` with content derived from the inference and the explicit preferences. Sections to fill typically include:

- Language and stack (with library list).
- Naming conventions.
- Project layout (with directory tree).
- Section headers and comment density.
- Function organisation.
- Plotting (with the lab's theme function, if found).
- Reproducibility expectations.
- Output handling.

Remove every worked-example block from the template before saving. The generated file should describe the adopter's lab, not a fictional example.

## Voice constraints

The generated `conventions/code-format.md` must comply with the framework voice rules:

- No em-dashes (use colons, semicolons, parentheses).
- No superlatives.
- Code samples may use whatever syntax the language requires; prose around the samples follows the voice rules.

## Output paths

- `conventions/code-format.md`
- `conventions/figure-format.md` (the plotting findings are extracted into a separate file because figures are referenced by multiple workflows).
