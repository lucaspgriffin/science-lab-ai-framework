#!/usr/bin/env python3
"""
apply_tracked_changes.py — surgically apply reviewer-reply markup to a
user-supplied copy of an original .docx, preserving all other formatting.

Workflow:
  1. Read a "marked-up" markdown file containing edits in the form
        ~~deleted text~~ ++inserted text++ [R1-C3: brief tag]
     where each ~~/++ pair is paired with surrounding context from the
     original manuscript text.
  2. Open the user-supplied <original>_revised.docx (which is byte-identical
     to the original at this point — only intermediate files exist alongside).
  3. For each edit, locate the anchor text in the body XML by concatenating
     the run text within paragraphs, split runs at the deletion boundaries,
     wrap the deletion in <w:del>, insert <w:ins> with the new text, and
     emit comment markers if a [R#-C#: ...] tag follows.
  4. Register comments in word/comments.xml, update [Content_Types].xml
     and word/_rels/document.xml.xml.rels.
  5. Save back to the same path; emit a per-edit report to stderr / a file.

Usage:
  python apply_tracked_changes.py \\
      --revised /path/to/manuscript_revised.docx \\
      --markup  /path/to/workflow_intermediates/manuscript_revised_marked.md \\
      --author  "Your Name" \\
      [--report /path/to/workflow_intermediates/manuscript_apply_report.md]

Dependencies: lxml.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % W_NS
PKG_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
NSMAP = {"w": W_NS}

# --- Markup parsing ---------------------------------------------------------
# Token types in the markdown:
#  - DEL: ~~text~~
#  - INS: ++text++
#  - TAG: [R1-C3: brief tag] or [EC-N: brief tag]
TOKEN_RE = re.compile(
    r"(?P<del>~~.+?~~)"
    r"|(?P<ins>\+\+.+?\+\+)"
    r"|(?P<tag>\[(?:(?:EC|R\d+)-C?\d+(?:\s*\+\s*(?:EC|R\d+)-C?\d+)*:\s*[^\]]+)\])",
    re.DOTALL,
)


def normalise(s: str) -> str:
    """Normalise whitespace and a few common character pairs to maximise
    cross-format matching. (Markdown round-trips can change smart quotes,
    en/em dashes, soft hyphens, and whitespace.)"""
    s = (
        s.replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace(" ", " ")
        .replace("‐", "-")
        .replace("‑", "-")
        .replace("‒", "-")
        .replace("–", "-")  # en dash
        .replace("—", "-")  # em dash
        .replace("‘", "'")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
    )
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# Stitches — also strip backslash-escapes that pandoc emits ("\>" -> ">")
def md_strip(s: str) -> str:
    s = s.replace("\\>", ">").replace("\\<", "<").replace("\\~", "~").replace("\\_", "_").replace("\\*", "*").replace("\\.", ".").replace("\\#", "#")
    return s


def md_strip_emphasis(s: str) -> str:
    """Strip markdown emphasis syntax (**, *, ~ for subscript, ^ for superscript)
    so the deletion text matches the plain text in the docx body, where
    subscripts/superscripts are styling runs rather than text characters.

    Only strip subscript/superscript ~ and ^ when they wrap a word (no spaces);
    bare ~ (as in "~1 hour" meaning approximately) is preserved."""
    # Strip ** and *
    s = re.sub(r"\*\*", "", s)
    s = re.sub(r"(?<!\w)\*(?!\s)", "", s)  # opening italic
    s = re.sub(r"(?<!\s)\*(?!\w)", "", s)  # closing italic
    # Strip subscript markers: ~word~  (paired around a single word, no spaces)
    s = re.sub(r"~([^~\s]+)~", r"\1", s)
    # Strip superscript markers: ^word^
    s = re.sub(r"\^([^\^\s]+)\^", r"\1", s)
    return s


class Edit:
    __slots__ = ("idx", "kind", "deletion", "insertion", "tag", "left_ctx", "right_ctx")

    def __init__(self, idx, kind, deletion="", insertion="", tag="", left_ctx="", right_ctx=""):
        self.idx = idx
        self.kind = kind  # "modify" (del+ins, possibly with tag) | "comment_only"
        self.deletion = deletion
        self.insertion = insertion
        self.tag = tag
        self.left_ctx = left_ctx
        self.right_ctx = right_ctx


def parse_markup(markup_text: str) -> list[Edit]:
    """Parse the marked-up markdown into a list of Edit objects.

    A logical edit can be:
      - ~~del~~ ++ins++ [tag]      (modify-and-comment)
      - ~~del~~ ++ins++             (modify, no comment)
      - ~~del~~                     (pure deletion)
      - ++ins++                     (pure insertion)
      - [tag] alone                 (rare — comment without text change)
    The tag, if present, follows the del/ins pair within a small window.
    """
    edits: list[Edit] = []
    pos = 0
    n = len(markup_text)
    idx = 0
    while pos < n:
        m = TOKEN_RE.search(markup_text, pos)
        if not m:
            break
        # Snag the next 1-3 tokens to glue del+ins+tag together
        sequence = []
        seq_pos = pos
        while True:
            mm = TOKEN_RE.search(markup_text, seq_pos)
            if not mm:
                break
            # Only glue if the gap is short and whitespace-only
            gap = markup_text[seq_pos:mm.start()] if not sequence else markup_text[sequence[-1].end():mm.start()]
            if sequence and not re.fullmatch(r"\s*", gap):
                break
            sequence.append(mm)
            seq_pos = mm.end()
            # Stop once we have an ins followed by a tag
            kinds = [s.lastgroup for s in sequence]
            if "tag" in kinds:
                break
            if len(sequence) >= 3:
                break
        # Build edit from sequence
        deletion = ""
        insertion = ""
        tag = ""
        for s in sequence:
            if s.lastgroup == "del":
                deletion = s.group("del")[2:-2]
            elif s.lastgroup == "ins":
                insertion = s.group("ins")[2:-2]
            elif s.lastgroup == "tag":
                tag = s.group("tag")[1:-1]
        # Context windows: 80 chars before the first token, 80 after the last
        first = sequence[0]
        last = sequence[-1]
        left = markup_text[max(0, first.start() - 200) : first.start()]
        right = markup_text[last.end() : last.end() + 200]
        # Strip nested markup tokens out of context (we want clean original-text context)
        left_clean = TOKEN_RE.sub("", left)
        right_clean = TOKEN_RE.sub("", right)
        if deletion or insertion:
            kind = "modify"
        elif tag:
            kind = "comment_only"
        else:
            kind = "modify"
        edits.append(
            Edit(
                idx=idx,
                kind=kind,
                deletion=md_strip_emphasis(md_strip(deletion)),
                insertion=md_strip_emphasis(md_strip(insertion)),
                tag=tag,
                left_ctx=md_strip_emphasis(md_strip(left_clean)),
                right_ctx=md_strip_emphasis(md_strip(right_clean)),
            )
        )
        idx += 1
        pos = last.end()
    return edits


# --- DOCX manipulation ------------------------------------------------------
class DocxEditor:
    def __init__(self, docx_path: Path, author: str):
        self.path = docx_path
        self.author = author
        self.when = (
            datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        )
        # Load all parts into memory
        with zipfile.ZipFile(self.path, "r") as z:
            self.files: dict[str, bytes] = {n: z.read(n) for n in z.namelist()}
        self.doc = etree.fromstring(self.files["word/document.xml"])
        self.body = self.doc.find(W + "body")
        # Comments registry
        self.next_comment_id = 0
        if "word/comments.xml" in self.files:
            try:
                cm_root = etree.fromstring(self.files["word/comments.xml"])
                ids = [int(c.get(W + "id") or "-1") for c in cm_root.iter(W + "comment")]
                if ids:
                    self.next_comment_id = max(ids) + 1
                self.comments_root = cm_root
            except Exception:
                self.comments_root = etree.Element(W + "comments", nsmap=NSMAP)
        else:
            self.comments_root = etree.Element(W + "comments", nsmap=NSMAP)
        # Revision id counter — start high to avoid collision with any existing revisions
        existing_ids: set[int] = set()
        for tag in (W + "ins", W + "del"):
            for el in self.doc.iter(tag):
                v = el.get(W + "id")
                if v and v.isdigit():
                    existing_ids.add(int(v))
        self.next_rev_id = max(existing_ids, default=0) + 1
        # Snapshot for fingerprint validation
        self.original_section_count = len(list(self.doc.iter(W + "sectPr")))
        self.original_p_count = len(list(self.body.findall(W + "p")))

    # ---- Paragraph search helpers -----------------------------------------
    def _para_text(self, p) -> str:
        """Concatenate live text of the paragraph — only <w:t>, <w:tab>, <w:br>.
        Skip <w:delText> (deleted text), since later edits should anchor against
        the post-deletion live text. This must stay in sync with
        _enumerate_run_texts which also iterates <w:t> only, so character
        offsets returned to the splitter are valid."""
        out = []
        for el in p.iter():
            if el.tag == W + "t":
                out.append(el.text or "")
            elif el.tag == W + "tab":
                out.append("\t")
            elif el.tag == W + "br":
                out.append("\n")
        return "".join(out)

    def _all_paragraphs(self):
        return list(self.doc.iter(W + "p"))

    # ---- Run splitting ----------------------------------------------------
    def _enumerate_run_texts(self, p):
        """Return a list of (run_element, text_element, text, start_offset, end_offset)
        tuples covering every <w:t> child within the paragraph, in document order."""
        result = []
        offset = 0
        for r in p.iter(W + "r"):
            for t in r.findall(W + "t"):
                txt = t.text or ""
                result.append((r, t, txt, offset, offset + len(txt)))
                offset += len(txt)
        return result

    def _split_run_at(self, run_el, t_el, local_offset):
        """Split a <w:r> at character `local_offset` within a child <w:t>.
        Returns (left_run, right_run). The original run is replaced in its parent
        by left_run; right_run is inserted immediately after."""
        parent = run_el.getparent()
        idx = list(parent).index(run_el)
        rpr = run_el.find(W + "rPr")
        text = t_el.text or ""
        left_text = text[:local_offset]
        right_text = text[local_offset:]
        # Build left run
        left_run = etree.Element(W + "r")
        if rpr is not None:
            left_run.append(_clone(rpr))
        lt = etree.SubElement(left_run, W + "t")
        lt.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        lt.text = left_text
        # Build right run
        right_run = etree.Element(W + "r")
        if rpr is not None:
            right_run.append(_clone(rpr))
        rt = etree.SubElement(right_run, W + "t")
        rt.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        rt.text = right_text
        # Replace
        parent.remove(run_el)
        parent.insert(idx, left_run)
        parent.insert(idx + 1, right_run)
        return left_run, right_run

    def _split_at_offset(self, p, char_offset):
        """Split the paragraph's runs so a clean cut exists at `char_offset`.
        Returns the run-index just *after* the split point (i.e., the first
        run whose text starts at >= char_offset)."""
        runs = self._enumerate_run_texts(p)
        for idx, (r, t, txt, start, end) in enumerate(runs):
            if start <= char_offset <= end:
                local = char_offset - start
                if local == 0:
                    # Cut is at start of this run; nothing to split
                    return r
                if local == len(txt):
                    # Cut is at end of this run; return next run if any
                    return runs[idx + 1][0] if idx + 1 < len(runs) else None
                left, right = self._split_run_at(r, t, local)
                return right
        return None

    # ---- Edit application -------------------------------------------------
    def apply_edit(self, edit: Edit) -> dict:
        """Try to apply the edit; return a result dict for the report."""
        result = {
            "idx": edit.idx,
            "deletion": edit.deletion[:80],
            "insertion": edit.insertion[:80],
            "tag": edit.tag[:80],
            "status": "pending",
            "para_idx": None,
        }
        # Skip pure markdown-only constructs (image links etc.)
        if edit.insertion.startswith("![") or edit.deletion.startswith("!["):
            result["status"] = "skipped_markdown_only"
            return result

        # Score every paragraph by how well its text matches the (left + del + right) context
        candidates = self._find_candidate_paragraphs(edit)
        if not candidates:
            result["status"] = "no_match"
            return result
        if len(candidates) > 1:
            # Use stricter scoring (longer ctx) to disambiguate
            candidates = self._tiebreak(candidates, edit)
        if not candidates:
            result["status"] = "ambiguous"
            return result

        para, char_offset, end_offset = candidates[0]
        para_idx = self._all_paragraphs().index(para)
        result["para_idx"] = para_idx

        # Special-case: pure insertion at a location where deletion is empty.
        if edit.deletion == "" and edit.insertion:
            # Insert new run + ins-wrapper at char_offset in this paragraph.
            anchor = self._split_at_offset(para, char_offset)
            ins_el = self._build_ins_element(edit.insertion)
            if anchor is not None:
                anchor.addprevious(ins_el)
            else:
                para.append(ins_el)
            if edit.tag:
                self._wrap_with_comment(para, ins_el, ins_el, edit.tag)
            result["status"] = "applied"
            return result

        # Pure tag-only — comment without text change. Anchor near the left context end.
        if edit.kind == "comment_only" or (edit.deletion == "" and edit.insertion == ""):
            # Place comment markers at char_offset (no text change)
            anchor = self._split_at_offset(para, char_offset) if char_offset else None
            self._insert_orphan_comment(para, anchor, edit.tag)
            result["status"] = "applied"
            return result

        # Standard modify path: del + ins (possibly with tag).
        # Split at start and end of deletion
        right_after_del = self._split_at_offset(para, end_offset)
        anchor_after_split = self._split_at_offset(para, char_offset)
        # After the second split, find every run whose offset lies in [char_offset, end_offset)
        runs = self._enumerate_run_texts(para)
        del_runs = [r for (r, t, txt, start, end) in runs if start >= char_offset and end <= end_offset]
        if not del_runs:
            # Can happen if the deletion is empty after splitting — fall back to no-match
            result["status"] = "no_runs_for_deletion"
            return result
        # Wrap del_runs in a single <w:del>
        del_el = self._wrap_runs_in_del(del_runs)
        # Insert ins immediately after the del element
        ins_el = self._build_ins_element(edit.insertion) if edit.insertion else None
        if ins_el is not None:
            del_el.addnext(ins_el)
        if edit.tag:
            anchor_start = del_el
            anchor_end = ins_el if ins_el is not None else del_el
            self._wrap_with_comment(para, anchor_start, anchor_end, edit.tag)
        result["status"] = "applied"
        return result

    def _find_candidate_paragraphs(self, edit: Edit) -> list[tuple]:
        """Find paragraphs containing the deletion text (or insertion-context)
        with surrounding context matching. Returns list of (paragraph, start_offset, end_offset)
        where the offsets are RAW character offsets in the paragraph text."""
        left_keep = 80
        right_keep = 80
        norm_del = normalise(edit.deletion) if edit.deletion else ""
        norm_left = normalise(edit.left_ctx[-left_keep:]) if edit.left_ctx else ""
        norm_right = normalise(edit.right_ctx[:right_keep]) if edit.right_ctx else ""

        candidates = []
        for p in self._all_paragraphs():
            ptxt = self._para_text(p)
            if not ptxt.strip():
                continue
            norm_ptxt, raw_offsets = _normalise_with_offsets(ptxt)

            if norm_del:
                # Find all occurrences of the normalised deletion in the normalised paragraph
                positions = _find_all_occurrences(norm_ptxt, norm_del)
                for npos in positions:
                    nend = npos + len(norm_del)
                    raw_start = raw_offsets[npos]
                    raw_end = raw_offsets[nend - 1] + 1 if nend > 0 else raw_start
                    # Validate context if available
                    para_left_norm = norm_ptxt[max(0, npos - left_keep):npos]
                    para_right_norm = norm_ptxt[nend:nend + right_keep]
                    score = 0
                    if norm_left:
                        score += _common_suffix(para_left_norm, norm_left)
                    if norm_right:
                        score += _common_prefix(para_right_norm, norm_right)
                    candidates.append((p, raw_start, raw_end, score))
            else:
                # Pure insertion / comment-only: anchor at end of left_ctx (or start of right_ctx)
                if norm_left and len(norm_left) >= 8:
                    needle = norm_left[-min(60, len(norm_left)):]
                    npos = norm_ptxt.rfind(needle)
                    if npos != -1:
                        # Anchor at end of needle
                        nend = npos + len(needle)
                        raw_anchor = raw_offsets[nend - 1] + 1 if nend > 0 else 0
                        # Score: confidence is the needle length
                        candidates.append((p, raw_anchor, raw_anchor, len(needle)))
                if not candidates and norm_right and len(norm_right) >= 8:
                    needle = norm_right[:min(60, len(norm_right))]
                    npos = norm_ptxt.find(needle)
                    if npos != -1:
                        raw_anchor = raw_offsets[npos]
                        candidates.append((p, raw_anchor, raw_anchor, len(needle)))

        # Deduplicate
        seen = set()
        unique = []
        for c in candidates:
            key = (id(c[0]), c[1], c[2])
            if key not in seen:
                seen.add(key)
                unique.append((c[0], c[1], c[2]))
        return unique

    def _find_candidate_paragraphs_scored(self, edit: Edit):
        """Variant that retains scores for tiebreaking."""
        # Re-run with scores; reuse logic but keep scores in tuple
        left_keep = 80
        right_keep = 80
        norm_del = normalise(edit.deletion) if edit.deletion else ""
        norm_left = normalise(edit.left_ctx[-left_keep:]) if edit.left_ctx else ""
        norm_right = normalise(edit.right_ctx[:right_keep]) if edit.right_ctx else ""
        scored = []
        for p in self._all_paragraphs():
            ptxt = self._para_text(p)
            if not ptxt.strip():
                continue
            norm_ptxt, raw_offsets = _normalise_with_offsets(ptxt)
            if norm_del:
                positions = _find_all_occurrences(norm_ptxt, norm_del)
                for npos in positions:
                    nend = npos + len(norm_del)
                    raw_start = raw_offsets[npos]
                    raw_end = raw_offsets[nend - 1] + 1 if nend > 0 else raw_start
                    para_left_norm = norm_ptxt[max(0, npos - left_keep):npos]
                    para_right_norm = norm_ptxt[nend:nend + right_keep]
                    score = 0
                    if norm_left:
                        score += _common_suffix(para_left_norm, norm_left)
                    if norm_right:
                        score += _common_prefix(para_right_norm, norm_right)
                    scored.append((score, p, raw_start, raw_end))
        return scored

    def _tiebreak(self, candidates, edit):
        """When multiple candidates match, score by longer context overlap."""
        scored = self._find_candidate_paragraphs_scored(edit)
        if not scored:
            return []
        scored.sort(reverse=True, key=lambda x: x[0])
        top_score = scored[0][0]
        best = [(p, s, e) for sc, p, s, e in scored if sc == top_score]
        if len(best) == 1:
            return best
        # Still tied — return the first occurrence (paragraph-order preference);
        # also surfaces a warning via the caller.
        return [best[0]]

    # ---- Element builders -------------------------------------------------
    def _new_rev_id(self) -> int:
        v = self.next_rev_id
        self.next_rev_id += 1
        return v

    def _build_ins_element(self, text: str):
        ins = etree.Element(W + "ins")
        ins.set(W + "id", str(self._new_rev_id()))
        ins.set(W + "author", self.author)
        ins.set(W + "date", self.when)
        run = etree.SubElement(ins, W + "r")
        # Explicit Times New Roman 12pt rPr on every inserted run. Inheriting
        # the paragraph's default font is unreliable — Word may render the
        # insertion in a theme font that differs from the surrounding body text.
        # Forcing TNR 24 half-points (12pt) keeps insertions visually consistent.
        rpr = etree.SubElement(run, W + "rPr")
        rfonts = etree.SubElement(rpr, W + "rFonts")
        rfonts.set(W + "ascii", "Times New Roman")
        rfonts.set(W + "hAnsi", "Times New Roman")
        rfonts.set(W + "cs", "Times New Roman")
        sz = etree.SubElement(rpr, W + "sz")
        sz.set(W + "val", "24")
        szcs = etree.SubElement(rpr, W + "szCs")
        szcs.set(W + "val", "24")
        t = etree.SubElement(run, W + "t")
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = text
        return ins

    def _wrap_runs_in_del(self, runs: list):
        """Wrap a contiguous list of <w:r> elements in a <w:del> element.
        Convert <w:t> children to <w:delText>."""
        first = runs[0]
        parent = first.getparent()
        idx = list(parent).index(first)
        del_el = etree.Element(W + "del")
        del_el.set(W + "id", str(self._new_rev_id()))
        del_el.set(W + "author", self.author)
        del_el.set(W + "date", self.when)
        for r in runs:
            # Convert <w:t> to <w:delText> on this run
            for t in r.findall(W + "t"):
                deltext = etree.Element(W + "delText")
                deltext.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                deltext.text = t.text or ""
                t.getparent().replace(t, deltext)
            parent.remove(r)
            del_el.append(r)
        parent.insert(idx, del_el)
        return del_el

    def _wrap_with_comment(self, para, start_anchor, end_anchor, comment_text):
        """Insert <w:commentRangeStart> before start_anchor and
        <w:commentRangeEnd> + <w:r><w:commentReference/></w:r> after end_anchor.
        Register the comment text in word/comments.xml."""
        cid = self.next_comment_id
        self.next_comment_id += 1
        # Body markers
        crs = etree.Element(W + "commentRangeStart")
        crs.set(W + "id", str(cid))
        cre = etree.Element(W + "commentRangeEnd")
        cre.set(W + "id", str(cid))
        cref_run = etree.Element(W + "r")
        cref = etree.SubElement(cref_run, W + "commentReference")
        cref.set(W + "id", str(cid))
        start_anchor.addprevious(crs)
        end_anchor.addnext(cre)
        cre.addnext(cref_run)
        # Register comment
        c = etree.SubElement(self.comments_root, W + "comment")
        c.set(W + "id", str(cid))
        c.set(W + "author", self.author)
        c.set(W + "date", self.when)
        c.set(W + "initials", _initials(self.author))
        cp = etree.SubElement(c, W + "p")
        cr = etree.SubElement(cp, W + "r")
        ct = etree.SubElement(cr, W + "t")
        ct.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        ct.text = comment_text

    def _insert_orphan_comment(self, para, anchor, comment_text):
        """Insert a comment with no text-change anchor — markers placed at offset."""
        cid = self.next_comment_id
        self.next_comment_id += 1
        crs = etree.Element(W + "commentRangeStart")
        crs.set(W + "id", str(cid))
        cre = etree.Element(W + "commentRangeEnd")
        cre.set(W + "id", str(cid))
        cref_run = etree.Element(W + "r")
        cref = etree.SubElement(cref_run, W + "commentReference")
        cref.set(W + "id", str(cid))
        if anchor is not None:
            anchor.addprevious(crs)
            anchor.addprevious(cre)
            anchor.addprevious(cref_run)
        else:
            para.append(crs)
            para.append(cre)
            para.append(cref_run)
        c = etree.SubElement(self.comments_root, W + "comment")
        c.set(W + "id", str(cid))
        c.set(W + "author", self.author)
        c.set(W + "date", self.when)
        c.set(W + "initials", _initials(self.author))
        cp = etree.SubElement(c, W + "p")
        cr = etree.SubElement(cp, W + "r")
        ct = etree.SubElement(cr, W + "t")
        ct.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        ct.text = comment_text

    # ---- Save -------------------------------------------------------------
    def save(self):
        # Update word/document.xml
        self.files["word/document.xml"] = etree.tostring(
            self.doc, xml_declaration=True, encoding="UTF-8", standalone=True
        )
        # Update word/comments.xml if any
        if list(self.comments_root):
            self.files["word/comments.xml"] = etree.tostring(
                self.comments_root, xml_declaration=True, encoding="UTF-8", standalone=True
            )
            # Ensure Content_Types and rels include comments
            self._ensure_comments_relationship()
        # Write
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for name, data in self.files.items():
                z.writestr(name, data)
        shutil.move(str(tmp), str(self.path))

    def _ensure_comments_relationship(self):
        # Content_Types
        ct_xml = self.files["[Content_Types].xml"]
        ct_root = etree.fromstring(ct_xml)
        has_ct = any(
            ov.get("PartName") == "/word/comments.xml"
            for ov in ct_root.findall(f"{{{CT_NS}}}Override")
        )
        if not has_ct:
            ov = etree.SubElement(ct_root, f"{{{CT_NS}}}Override")
            ov.set("PartName", "/word/comments.xml")
            ov.set(
                "ContentType",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml",
            )
            self.files["[Content_Types].xml"] = etree.tostring(
                ct_root, xml_declaration=True, encoding="UTF-8", standalone=True
            )
        # Rels
        rels_path = "word/_rels/document.xml.rels"
        rels_root = etree.fromstring(self.files[rels_path])
        has_rel = any(
            r.get("Type")
            == "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
            for r in rels_root.findall(f"{{{PKG_NS}}}Relationship")
        )
        if not has_rel:
            existing = {r.get("Id") for r in rels_root.findall(f"{{{PKG_NS}}}Relationship")}
            i = 1
            while f"rId{i}" in existing:
                i += 1
            rel = etree.SubElement(rels_root, f"{{{PKG_NS}}}Relationship")
            rel.set("Id", f"rId{i}")
            rel.set(
                "Type",
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments",
            )
            rel.set("Target", "comments.xml")
            self.files[rels_path] = etree.tostring(
                rels_root, xml_declaration=True, encoding="UTF-8", standalone=True
            )


def _clone(el):
    """Deep-clone an etree element."""
    return etree.fromstring(etree.tostring(el))


def _initials(name: str) -> str:
    parts = [p for p in name.replace("-", " ").split() if p]
    return "".join(p[0].upper() for p in parts[:3])


def _find_all_occurrences(haystack: str, needle: str) -> list[int]:
    if not needle:
        return []
    out = []
    pos = 0
    while True:
        idx = haystack.find(needle, pos)
        if idx == -1:
            break
        out.append(idx)
        pos = idx + 1
    return out


def _normalise_with_offsets(s: str):
    """Return (normalised_string, offsets_list) where offsets_list[i] is the
    raw offset in the original `s` corresponding to character i in the
    normalised string. Normalisation collapses runs of whitespace to a single
    space and strips leading/trailing whitespace (anchoring offsets to the
    raw character that produced each normalised character)."""
    out_chars = []
    out_offsets = []
    in_ws = True  # treat leading as already-collapsed
    for raw_idx, ch in enumerate(s):
        # Apply the same character substitutions as normalise()
        if ch in (" ", "‐", "‑", "‒", "–", "—"):
            mapped = "-" if ch in ("‐", "‑", "‒", "–", "—") else " "
        elif ch in ("‘", "’"):
            mapped = "'"
        elif ch in ("“", "”"):
            mapped = '"'
        elif ch in ("\r", "\n", "\t"):
            mapped = " "
        else:
            mapped = ch
        if mapped == " ":
            if in_ws:
                continue
            out_chars.append(" ")
            out_offsets.append(raw_idx)
            in_ws = True
        else:
            out_chars.append(mapped)
            out_offsets.append(raw_idx)
            in_ws = False
    # Strip trailing whitespace from normalised
    while out_chars and out_chars[-1] == " ":
        out_chars.pop()
        out_offsets.pop()
    return "".join(out_chars), out_offsets


def _common_suffix(a: str, b: str) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[-1 - i] == b[-1 - i]:
        i += 1
    return i


def _common_prefix(a: str, b: str) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


# --- Validation -------------------------------------------------------------
def validate(docx_path: Path, original_section_count: int) -> list[str]:
    issues = []
    with zipfile.ZipFile(docx_path, "r") as z:
        body = z.read("word/document.xml")
        root = etree.fromstring(body)
        ins_count = len(list(root.iter(W + "ins")))
        del_count = len(list(root.iter(W + "del")))
        sect_count = len(list(root.iter(W + "sectPr")))
        if sect_count != original_section_count:
            issues.append(
                f"section count changed: original {original_section_count} -> now {sect_count}"
            )
        print(f"  applied: {ins_count} ins, {del_count} del", file=sys.stderr)
        if "word/comments.xml" in z.namelist():
            cm = etree.fromstring(z.read("word/comments.xml"))
            print(f"  comments registered: {len(list(cm.iter(W + 'comment')))}", file=sys.stderr)
    return issues


def qa_scan(docx_path: Path) -> list[str]:
    """Post-render QA scan for common renderer artefacts.

    Catches issues that have shipped in past runs:
    - Doubled adjacent letters at insertion boundaries (e.g., 'OOn', 'FFig', 'CC').
    - Stranded lowercase letters before insertions ('cfood', 'cwas') — leftovers
      from a partial deletion where the first character of the deleted word
      stayed live.
    - Missing spaces between word-and-paren (`capacity(`) or word-and-capital
      (`capacitywas`) at run boundaries.
    - Repeated tokens at insertion sites (e.g., 'food food food').
    - Font drift on <w:ins> runs: any insertion run whose rPr does not force
      Times New Roman 12pt is flagged.

    Returns a list of issue strings (empty if clean).
    """
    issues: list[str] = []
    with zipfile.ZipFile(docx_path, "r") as z:
        doc = etree.fromstring(z.read("word/document.xml"))

    body = doc.find(W + "body")
    if body is None:
        return issues
    paragraphs = list(body.iter(W + "p"))

    # Build visible-text per paragraph (live + ins, exclude del)
    def visible_text(p):
        out = []
        for t in p.iter(W + "t"):
            cur = t.getparent()
            in_del = False
            while cur is not None and cur.tag != W + "p":
                if cur.tag == W + "del":
                    in_del = True
                    break
                cur = cur.getparent()
            if not in_del:
                out.append(t.text or "")
        return "".join(out)

    # Patterns to scan (regex)
    doubled_letter_re = re.compile(r"\b([A-Z])\1(?=[a-z])")  # e.g., OOn, FFig
    stranded_lc_c_re = re.compile(r"\bc(?=food|consumption|was|year)")
    missing_space_re = re.compile(r"\b(capacity|consumption|metabolism)(?=[A-Za-z(])")
    repeated_token_re = re.compile(r"\b(\w+)( \1){2,}\b")

    for p_idx, p in enumerate(paragraphs):
        vt = visible_text(p)
        if not vt:
            continue
        for m in doubled_letter_re.finditer(vt):
            ctx = vt[max(0, m.start() - 20): m.end() + 20]
            issues.append(f"QA(doubled letter): P{p_idx} ...{ctx}...")
        for m in stranded_lc_c_re.finditer(vt):
            ctx = vt[max(0, m.start() - 20): m.end() + 30]
            issues.append(f"QA(stranded letter): P{p_idx} ...{ctx}...")
        for m in missing_space_re.finditer(vt):
            ctx = vt[max(0, m.start() - 10): m.end() + 30]
            issues.append(f"QA(missing space): P{p_idx} ...{ctx}...")
        for m in repeated_token_re.finditer(vt):
            ctx = vt[max(0, m.start() - 10): m.end() + 10]
            issues.append(f"QA(repeated token): P{p_idx} ...{ctx}...")

    # Font drift on insertions
    bad_font_runs = 0
    for ins in doc.iter(W + "ins"):
        for r in ins.findall(W + "r"):
            rpr = r.find(W + "rPr")
            ok = False
            if rpr is not None:
                rfonts = rpr.find(W + "rFonts")
                sz = rpr.find(W + "sz")
                if (
                    rfonts is not None
                    and rfonts.get(W + "ascii") == "Times New Roman"
                    and sz is not None
                    and sz.get(W + "val") == "24"
                ):
                    ok = True
            if not ok:
                bad_font_runs += 1
    if bad_font_runs:
        issues.append(
            f"QA(font drift): {bad_font_runs} <w:ins> runs lack explicit TNR 12pt rPr"
        )

    return issues


# --- CLI --------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--revised", required=True, help="user-supplied <original>_revised.docx (gets tracked changes)")
    ap.add_argument("--markup", required=True, help="<title>_revised_marked.md from drafting Phase 2")
    ap.add_argument("--author", default="Author")
    ap.add_argument("--report", default=None, help="write per-edit report markdown here")
    args = ap.parse_args()

    revised = Path(args.revised)
    markup_path = Path(args.markup)
    if not revised.exists():
        print(f"ERROR: {revised} not found", file=sys.stderr)
        sys.exit(2)
    if not markup_path.exists():
        print(f"ERROR: {markup_path} not found", file=sys.stderr)
        sys.exit(2)

    markup_text = markup_path.read_text(encoding="utf-8")
    edits = parse_markup(markup_text)
    print(f"Parsed {len(edits)} edits from {markup_path.name}", file=sys.stderr)

    editor = DocxEditor(revised, author=args.author)
    original_sect_count = editor.original_section_count

    results = []
    for edit in edits:
        try:
            r = editor.apply_edit(edit)
        except Exception as e:
            r = {"idx": edit.idx, "status": f"error: {e!r}", "deletion": edit.deletion[:80], "insertion": edit.insertion[:80], "tag": edit.tag[:80], "para_idx": None}
        results.append(r)

    editor.save()

    # Validate
    issues = validate(revised, original_sect_count)
    if issues:
        for i in issues:
            print(f"  WARN: {i}", file=sys.stderr)

    # Post-render QA scan
    qa_issues = qa_scan(revised)
    if qa_issues:
        print(f"  QA SCAN: {len(qa_issues)} potential issues — review before declaring complete:", file=sys.stderr)
        for q in qa_issues[:50]:
            print(f"    {q}", file=sys.stderr)
        if len(qa_issues) > 50:
            print(f"    ... and {len(qa_issues) - 50} more", file=sys.stderr)
    else:
        print(f"  QA SCAN: clean", file=sys.stderr)

    # Summary
    statuses = {}
    for r in results:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    print("Summary by status:", file=sys.stderr)
    for s, n in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {s}: {n}", file=sys.stderr)

    if args.report:
        report_path = Path(args.report)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# apply_tracked_changes.py report — {revised.name}\n\n")
            f.write(f"- Markup source: `{markup_path}`\n")
            f.write(f"- Author: {args.author}\n")
            f.write(f"- Edits parsed: {len(edits)}\n\n")
            f.write("## Status counts\n\n")
            for s, n in sorted(statuses.items(), key=lambda x: -x[1]):
                f.write(f"- **{s}**: {n}\n")
            f.write("\n## QA scan\n\n")
            if qa_issues:
                f.write(f"**{len(qa_issues)} potential issues flagged.** Review each before declaring the render complete.\n\n")
                for q in qa_issues:
                    f.write(f"- {q}\n")
            else:
                f.write("Clean — no doubled letters, stranded characters, missing spaces, repeated tokens, or font drift detected.\n")
            f.write("\n## Per-edit detail\n\n")
            for r in results:
                f.write(f"### Edit #{r['idx']} — `{r['status']}`\n")
                f.write(f"- Para idx: {r.get('para_idx')}\n")
                if r["deletion"]:
                    f.write(f"- Deletion: `{r['deletion']}`\n")
                if r["insertion"]:
                    f.write(f"- Insertion: `{r['insertion']}`\n")
                if r["tag"]:
                    f.write(f"- Tag: `{r['tag']}`\n")
                f.write("\n")
        print(f"Report written: {report_path}", file=sys.stderr)

    # Exit code: 0 if all applied, 1 if any failures
    failed = sum(n for s, n in statuses.items() if s not in ("applied",))
    if failed:
        print(f"NOTE: {failed} edits did not apply cleanly. See report.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
