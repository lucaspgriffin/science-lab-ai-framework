# tools/tracked-changes/

Two Python scripts that produce Word-compatible tracked-changes `.docx` files from inline markup in markdown. Used by the reviewer-reply workflows (`skills/simple/reviewer-reply-drafting/`, `skills/workflows/reviewer-reply-pipeline/`).

## Why these exist

When responding to peer reviewers, you typically submit two artefacts: a reply document explaining each change, and a revised manuscript with tracked changes that the journal editor can step through using Word's "Accept change" / "Reject change" buttons. Generating that second artefact reliably is harder than it looks. Pandoc and `python-docx` can produce changes that *look* right visually but do not register as real Word tracked changes (no accept / reject affordance for the editor). Producing true tracked changes requires manipulating the underlying Office Open XML (OOXML) directly: inserting `<w:ins>` and `<w:del>` elements with author attribution, splitting text runs at edit boundaries, and updating the comments registry.

These two scripts handle that OOXML manipulation. They are designed to be used by the reviewer-reply skills, but they are stand-alone Python and can be used in any pipeline that emits inline-marked markdown.

## Contents

```
tools/tracked-changes/
├── README.md                 this file
├── apply_tracked_changes.py  surgical OOXML edits on an existing .docx
└── render_tracked_docx.py    pandoc-based render of marked-up markdown to .docx
```

### `apply_tracked_changes.py`

Reads a markdown file containing inline markup (`~~deleted~~ ++inserted++ [R1-C3: tag]`) plus a copy of the original manuscript `.docx`, and writes tracked-changes XML directly into the existing `.docx`. Preserves all other formatting (fonts, styles, tables, figures, citations) because it works at the OOXML level on the user's file.

Use when the source manuscript is already a polished `.docx` and you want tracked changes layered on top.

```bash
python tools/tracked-changes/apply_tracked_changes.py \
    --revised /path/to/manuscript_revised.docx \
    --markup  /path/to/workflow_intermediates/manuscript_revised_marked.md \
    --author  "Your Name" \
    --report  /path/to/workflow_intermediates/apply_report.md
```

### `render_tracked_docx.py`

Renders a marked-up markdown file directly to a fresh `.docx` with tracked changes. Uses pandoc plus a small OOXML post-processing pass.

Use when the source is markdown and you want the workflow to produce the `.docx` from scratch.

```bash
python tools/tracked-changes/render_tracked_docx.py INPUT.md OUTPUT.docx \
    --mode tracked --author "Your Name" --title "Manuscript title"
```

## Dependencies

- Python 3.8 or newer
- `lxml` (XML processing)
- `pandoc` (for `render_tracked_docx.py`; not needed for `apply_tracked_changes.py`)

Install:

```bash
pip install lxml
# pandoc: brew install pandoc  /  apt install pandoc  /  see https://pandoc.org
```

No other Python packages are required.

## How the markup works

The scripts expect markdown with inline markup of this form:

```
This is the original sentence. ~~This part is deleted.~~ ++This part is inserted.++ The rest continues.
```

Optional reviewer-comment tags follow each markup pair:

```
~~old wording~~ ++new wording++ [R1-C3: reviewer wanted clarification on methods]
```

Tags in the form `[R{reviewer-number}-C{comment-number}: ...]` are converted to Word comments anchored to the change, with the comment text becoming the body of the Word comment.

This markup convention is shared with the manuscript-builder skill and the report-builder skill; if you use those workflows, the same inline format flows through.

## Customisation

The two scripts are read-only as shipped. If you want to change the markup syntax, the comment-tag format, or the author-attribution behaviour, edit the constants at the top of each file. Both scripts are under 1000 lines and the structure is straightforward (parse markup, locate anchors in OOXML, emit `<w:ins>` / `<w:del>` elements, save).

## Integration with the reviewer-reply skills

`skills/simple/reviewer-reply-drafting/SKILL.md` invokes `apply_tracked_changes.py` after the drafting agent has produced the marked-up markdown. The skill expects the script at `tools/tracked-changes/apply_tracked_changes.py` (this path). If you relocate the scripts, update the path in the skill.

`skills/workflows/reviewer-reply-pipeline/SKILL.md` orchestrates the full reviewer-reply cycle; the drafting step delegates to the script as described above.

## Limitations

- Tested against Microsoft Word 2019, Microsoft 365, and LibreOffice Writer. Other Word-compatible editors may handle the tracked-changes markup differently.
- The scripts assume the manuscript `.docx` uses a single primary text run per paragraph (typical for Word output). Heavily marked-up source documents with many overlapping runs may need manual cleanup before the script runs.
- Comments are attached to the inserted text by default; some editors prefer comments anchored to the deleted text. The behaviour is configurable in the source.

## Licence

MIT (see `LICENSE-CODE` at repo root). Use freely; modify as needed.
