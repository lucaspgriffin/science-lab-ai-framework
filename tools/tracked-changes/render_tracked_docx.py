#!/usr/bin/env python3
"""
render_tracked_docx.py — Reviewer-reply renderer of record.

Converts a markdown manuscript or reply doc with reviewer-reply-style inline
markup into a .docx with NATIVE Word tracked changes and NATIVE Word comments.

Markup convention (from tasks/reviewer-reply/SKILL.md):
  ~~deleted text~~              -> native Word <w:del> revision mark
  ++inserted text++             -> native Word <w:ins> revision mark
  [R1-C3: brief tag]            -> native Word <w:comment> in word/comments.xml
  [EC-N: brief tag]             -> native Word <w:comment>

Render conventions (non-negotiable):
  - Times New Roman everywhere (body 11pt, headings 12pt), every run.
  - Black text everywhere (RGB 000000), no Word-blue heading auto-colour.
  - All revision marks attributed to a single author (passed via --author).
  - Validator fails the build if any non-black <w:color> or non-TNR font slips through.

Modes:
  - tracked  : default; emits <w:ins>/<w:del> for ~~/++ markup; comment markers
               become Word comments. Used for manuscript & appendix.
  - clean    : strips all markup; insertions become plain text, deletions are
               removed; comment markers are stripped. Used for the reply doc.
  - highlight: red-strikethrough deletions + yellow-highlighted insertions +
               bold-blue bracketed comment markers. Visual-review only.

Usage:
  python render_tracked_docx.py INPUT.md OUTPUT.docx \\
      --mode tracked --author "Your Name" --title "Manuscript title"

Dependencies: python-docx, lxml.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_COLOR_INDEX
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % W_NS
NSMAP = {"w": W_NS}

# --- Tokeniser ---------------------------------------------------------------
DELETION = re.compile(r"~~(.+?)~~", re.DOTALL)
INSERTION = re.compile(r"\+\+(.+?)\+\+", re.DOTALL)
COMMENT_TAG = re.compile(
    r"\[((?:EC|R\d+)-C?\d+(?:\s*\+\s*(?:EC|R\d+)-C?\d+)*:\s*[^\]]+)\]"
)
TOKEN = re.compile(
    r"(~~.+?~~)"
    r"|(\+\+.+?\+\+)"
    r"|(\[(?:(?:EC|R\d+)-C?\d+(?:\s*\+\s*(?:EC|R\d+)-C?\d+)*:\s*[^\]]+)\])",
    re.DOTALL,
)
HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$")


def tokenise(text: str):
    """Yield (kind, text) tokens. kind in {'plain', 'del', 'ins', 'comment'}."""
    pos = 0
    for m in TOKEN.finditer(text):
        if m.start() > pos:
            yield "plain", text[pos : m.start()]
        if m.group(1):
            yield "del", m.group(1)[2:-2]
        elif m.group(2):
            yield "ins", m.group(2)[2:-2]
        elif m.group(3):
            yield "comment", m.group(3)[1:-1]
        pos = m.end()
    if pos < len(text):
        yield "plain", text[pos:]


# --- TNR-black enforcement helpers ------------------------------------------
TNR = "Times New Roman"
BLACK = "000000"


def _force_tnr_black_on_run(run_xml):
    """Apply Times New Roman + black colour to a single run XML element."""
    rpr = run_xml.find(W + "rPr")
    if rpr is None:
        rpr = etree.SubElement(run_xml, W + "rPr")
        run_xml.insert(0, rpr)
    # Font
    rfonts = rpr.find(W + "rFonts")
    if rfonts is None:
        rfonts = etree.SubElement(rpr, W + "rFonts")
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(W + attr, TNR)
    # Colour
    color = rpr.find(W + "color")
    if color is None:
        color = etree.SubElement(rpr, W + "color")
    color.set(W + "val", BLACK)


def _make_run(text: str, bold=False, italic=False, sz_half_pts: int | None = None):
    """Build a <w:r> element with TNR-black, optional bold/italic and size."""
    run = etree.Element(W + "r")
    rpr = etree.SubElement(run, W + "rPr")
    rfonts = etree.SubElement(rpr, W + "rFonts")
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(W + attr, TNR)
    color = etree.SubElement(rpr, W + "color")
    color.set(W + "val", BLACK)
    if bold:
        etree.SubElement(rpr, W + "b")
    if italic:
        etree.SubElement(rpr, W + "i")
    if sz_half_pts is not None:
        sz = etree.SubElement(rpr, W + "sz")
        sz.set(W + "val", str(sz_half_pts))
        szcs = etree.SubElement(rpr, W + "szCs")
        szcs.set(W + "val", str(sz_half_pts))
    t = etree.SubElement(run, W + "t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    return run


def _make_del_run(text: str, rev_id: int, author: str, when: str):
    """Build a <w:del> wrapping a single deleted-text run."""
    delete = etree.Element(W + "del")
    delete.set(W + "id", str(rev_id))
    delete.set(W + "author", author)
    delete.set(W + "date", when)
    run = etree.SubElement(delete, W + "r")
    rpr = etree.SubElement(run, W + "rPr")
    rfonts = etree.SubElement(rpr, W + "rFonts")
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(W + attr, TNR)
    color = etree.SubElement(rpr, W + "color")
    color.set(W + "val", BLACK)
    deltext = etree.SubElement(run, W + "delText")
    deltext.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    deltext.text = text
    return delete


def _make_ins_run(text: str, rev_id: int, author: str, when: str):
    """Build a <w:ins> wrapping a single inserted-text run."""
    insert = etree.Element(W + "ins")
    insert.set(W + "id", str(rev_id))
    insert.set(W + "author", author)
    insert.set(W + "date", when)
    run = _make_run(text)
    insert.append(run)
    return insert


# --- Comment helpers --------------------------------------------------------
class CommentRegistry:
    """Tracks comments to be emitted in word/comments.xml and the body anchors."""

    def __init__(self, author: str):
        self.author = author
        self.entries: list[dict] = []  # {id, text, anchor_text}
        self._next_id = 0

    def register(self, body_anchor_text: str, comment_text: str) -> int:
        cid = self._next_id
        self._next_id += 1
        self.entries.append(
            {"id": cid, "text": comment_text, "anchor": body_anchor_text}
        )
        return cid

    def to_comments_xml(self, when: str) -> bytes:
        """Build word/comments.xml content."""
        root = etree.Element(W + "comments", nsmap=NSMAP)
        for entry in self.entries:
            c = etree.SubElement(root, W + "comment")
            c.set(W + "id", str(entry["id"]))
            c.set(W + "author", self.author)
            c.set(W + "date", when)
            c.set(W + "initials", _initials(self.author))
            p = etree.SubElement(c, W + "p")
            r = _make_run(entry["text"])
            p.append(r)
        xml = etree.tostring(
            root, xml_declaration=True, encoding="UTF-8", standalone=True
        )
        return xml


def _initials(name: str) -> str:
    parts = [p for p in name.replace("-", " ").split() if p]
    return "".join(p[0].upper() for p in parts[:3])


def _make_comment_anchor(rid: int, anchor_text: str):
    """Build the body-side comment markers wrapping a run."""
    cstart = etree.Element(W + "commentRangeStart")
    cstart.set(W + "id", str(rid))
    cend = etree.Element(W + "commentRangeEnd")
    cend.set(W + "id", str(rid))
    ref_run = etree.Element(W + "r")
    rpr = etree.SubElement(ref_run, W + "rPr")
    rstyle = etree.SubElement(rpr, W + "rStyle")
    rstyle.set(W + "val", "CommentReference")
    cref = etree.SubElement(ref_run, W + "commentReference")
    cref.set(W + "id", str(rid))
    return cstart, cend, ref_run


# --- Paragraph builders -----------------------------------------------------
def build_paragraph(
    text: str,
    mode: str,
    author: str,
    when: str,
    rev_counter: list[int],
    comments: CommentRegistry,
    style_size_half_pts: int = 22,  # 11pt body
    bold: bool = False,
):
    """Convert one logical paragraph of source markdown to a <w:p> element."""
    p = etree.Element(W + "p")
    ppr = etree.SubElement(p, W + "pPr")
    # Spacing: single line, small space-after
    spacing = etree.SubElement(ppr, W + "spacing")
    spacing.set(W + "after", "120")
    spacing.set(W + "line", "276")
    spacing.set(W + "lineRule", "auto")

    for kind, payload in tokenise(text):
        if kind == "plain":
            # Process bold/italic markdown inside plain
            for run_text, run_bold, run_italic in _split_inline(payload):
                if not run_text:
                    continue
                run = _make_run(
                    run_text,
                    bold=run_bold or bold,
                    italic=run_italic,
                    sz_half_pts=style_size_half_pts,
                )
                p.append(run)
        elif kind == "del":
            if mode == "tracked":
                rev_counter[0] += 1
                p.append(_make_del_run(payload, rev_counter[0], author, when))
            elif mode == "highlight":
                run = _make_run(payload, sz_half_pts=style_size_half_pts)
                # Add strike + red colour
                rpr = run.find(W + "rPr")
                strike = etree.SubElement(rpr, W + "strike")
                color = rpr.find(W + "color")
                if color is None:
                    color = etree.SubElement(rpr, W + "color")
                color.set(W + "val", "C00000")
                p.append(run)
            else:  # clean
                pass  # drop deleted text
        elif kind == "ins":
            if mode == "tracked":
                rev_counter[0] += 1
                p.append(_make_ins_run(payload, rev_counter[0], author, when))
            elif mode == "highlight":
                run = _make_run(payload, sz_half_pts=style_size_half_pts)
                rpr = run.find(W + "rPr")
                hl = etree.SubElement(rpr, W + "highlight")
                hl.set(W + "val", "yellow")
                p.append(run)
            else:  # clean
                run = _make_run(payload, sz_half_pts=style_size_half_pts)
                p.append(run)
        elif kind == "comment":
            if mode == "tracked":
                # Anchor on the immediately preceding run (or empty if none)
                # We register the comment and emit a reference at this point.
                cid = comments.register("", payload)
                cstart = etree.Element(W + "commentRangeStart")
                cstart.set(W + "id", str(cid))
                cend = etree.Element(W + "commentRangeEnd")
                cend.set(W + "id", str(cid))
                ref_run = etree.Element(W + "r")
                rpr = etree.SubElement(ref_run, W + "rPr")
                rstyle = etree.SubElement(rpr, W + "rStyle")
                rstyle.set(W + "val", "CommentReference")
                cref = etree.SubElement(ref_run, W + "commentReference")
                cref.set(W + "id", str(cid))
                # We add the start marker before the last paragraph child if
                # possible (anchored to the prior run); otherwise just append.
                if len(p) > 1:
                    last = p[-1]
                    last.addprevious(cstart)
                else:
                    p.append(cstart)
                p.append(cend)
                p.append(ref_run)
            elif mode == "highlight":
                run = _make_run(
                    "[" + payload + "]",
                    bold=True,
                    sz_half_pts=style_size_half_pts,
                )
                # Override colour to blue
                rpr = run.find(W + "rPr")
                color = rpr.find(W + "color")
                color.set(W + "val", "003399")
                p.append(run)
            else:  # clean
                pass  # strip comment markers
    return p


INLINE_RE = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")


def _split_inline(text: str):
    """Return list of (text, bold, italic) tuples from a plain-text segment."""
    out = []
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append((text[pos : m.start()], False, False))
        token = m.group(0)
        if token.startswith("**") and token.endswith("**"):
            out.append((token[2:-2], True, False))
        elif token.startswith("*") and token.endswith("*"):
            out.append((token[1:-1], False, True))
        else:
            out.append((token, False, False))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False, False))
    if not out:
        out = [(text, False, False)]
    return out


# --- Document assembly ------------------------------------------------------
def build_document(
    source_md: str,
    mode: str,
    author: str,
    title: str | None,
):
    when = (
        datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    # Start from a blank python-docx template, then surgically rebuild the
    # body so we have full control over the XML.
    doc = Document()
    body = doc.element.body
    # Remove existing paragraphs
    for child in list(body):
        if child.tag in (W + "p", W + "tbl"):
            body.remove(child)

    # Set default font on Normal style
    style = doc.styles["Normal"]
    style.font.name = TNR
    style.font.size = Pt(11)
    style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    rev_counter = [0]
    comments = CommentRegistry(author=author)

    if title:
        title_p = etree.Element(W + "p")
        ppr = etree.SubElement(title_p, W + "pPr")
        align = etree.SubElement(ppr, W + "jc")
        align.set(W + "val", "center")
        title_p.append(_make_run(title, bold=True, sz_half_pts=28))
        body.append(title_p)
        # spacer
        body.append(etree.Element(W + "p"))

    # Walk markdown line-by-line; merge into paragraphs
    lines = source_md.splitlines()
    para_lines: list[str] = []

    def flush_para():
        if not para_lines:
            return
        chunk = "\n".join(para_lines).strip("\n")
        if not chunk.strip():
            para_lines.clear()
            return
        # Skip image/figure links and pandoc attribute lines
        if chunk.lstrip().startswith("!["):
            para_lines.clear()
            return
        if chunk.lstrip().startswith("{") and chunk.rstrip().endswith("}"):
            para_lines.clear()
            return
        # Detect heading
        first_line = chunk.lstrip().splitlines()[0] if chunk.strip() else ""
        h_match = HEADING_RE.match(first_line)
        if h_match and "\n" not in chunk:
            level = len(h_match.group(1))
            heading_text = h_match.group(2).strip()
            sz_hp = {1: 28, 2: 26, 3: 24}.get(level, 22)
            p = build_paragraph(
                heading_text,
                mode=mode,
                author=author,
                when=when,
                rev_counter=rev_counter,
                comments=comments,
                style_size_half_pts=sz_hp,
                bold=True,
            )
            body.append(p)
        elif (
            chunk.startswith("**")
            and chunk.endswith("**")
            and "\n" not in chunk
        ):
            # Bold-only line treated as section header
            p = build_paragraph(
                chunk[2:-2],
                mode=mode,
                author=author,
                when=when,
                rev_counter=rev_counter,
                comments=comments,
                style_size_half_pts=24,
                bold=True,
            )
            body.append(p)
        else:
            p = build_paragraph(
                chunk,
                mode=mode,
                author=author,
                when=when,
                rev_counter=rev_counter,
                comments=comments,
            )
            body.append(p)
        para_lines.clear()

    for line in lines:
        if not line.strip():
            flush_para()
            continue
        para_lines.append(line)
    flush_para()

    return doc, comments, when


def save_with_comments(doc: Document, output_path: Path, comments: CommentRegistry, when: str, mode: str):
    """Save the doc and (if tracked mode) inject word/comments.xml + Content_Types entry + relationship."""
    doc.save(str(output_path))

    if mode != "tracked" or not comments.entries:
        return

    # Re-open the .docx (zip) and inject the comments part.
    comments_xml = comments.to_comments_xml(when)

    # Read existing parts
    with zipfile.ZipFile(output_path, "r") as zin:
        names = zin.namelist()
        files = {n: zin.read(n) for n in names}

    # Add comments.xml
    files["word/comments.xml"] = comments_xml

    # Update [Content_Types].xml
    ct_xml = files["[Content_Types].xml"]
    ct_root = etree.fromstring(ct_xml)
    has_comments_ct = any(
        ov.get("PartName") == "/word/comments.xml"
        for ov in ct_root.findall(
            "{http://schemas.openxmlformats.org/package/2006/content-types}Override"
        )
    )
    if not has_comments_ct:
        ov = etree.SubElement(
            ct_root,
            "{http://schemas.openxmlformats.org/package/2006/content-types}Override",
        )
        ov.set("PartName", "/word/comments.xml")
        ov.set(
            "ContentType",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml",
        )
    files["[Content_Types].xml"] = etree.tostring(
        ct_root, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    # Update word/_rels/document.xml.rels
    rels_path = "word/_rels/document.xml.rels"
    rels_xml = files[rels_path]
    rels_root = etree.fromstring(rels_xml)
    pkg_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    existing_ids = {r.get("Id") for r in rels_root.findall(f"{{{pkg_ns}}}Relationship")}
    has_comments_rel = any(
        r.get("Type")
        == "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
        for r in rels_root.findall(f"{{{pkg_ns}}}Relationship")
    )
    if not has_comments_rel:
        # Find an unused rId
        idx = 1
        while f"rId{idx}" in existing_ids:
            idx += 1
        rel = etree.SubElement(rels_root, f"{{{pkg_ns}}}Relationship")
        rel.set("Id", f"rId{idx}")
        rel.set(
            "Type",
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments",
        )
        rel.set("Target", "comments.xml")
    files[rels_path] = etree.tostring(
        rels_root, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    # Repack
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)


# --- Validator --------------------------------------------------------------
def validate(output_path: Path, mode: str) -> list[str]:
    """Inspect the rendered .docx; return a list of warnings/errors."""
    issues: list[str] = []
    with zipfile.ZipFile(output_path, "r") as z:
        body = z.read("word/document.xml")
        body_root = etree.fromstring(body)
        # Font check
        for rfonts in body_root.iter(W + "rFonts"):
            for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
                v = rfonts.get(W + attr)
                if v and v != TNR:
                    issues.append(
                        f"Non-TNR font in body: <w:rFonts w:{attr}='{v}'>"
                    )
                    break
        # Colour check
        for color in body_root.iter(W + "color"):
            v = color.get(W + "val")
            if v not in (None, BLACK, "auto"):
                issues.append(f"Non-black colour in body: <w:color w:val='{v}'>")
        # Tracked-changes check
        if mode == "tracked":
            ins_count = len(list(body_root.iter(W + "ins")))
            del_count = len(list(body_root.iter(W + "del")))
            if ins_count == 0 and del_count == 0:
                issues.append(
                    "tracked mode but no <w:ins> or <w:del> elements found"
                )
            if "word/comments.xml" in z.namelist():
                comments_xml = z.read("word/comments.xml")
                c_count = len(
                    list(etree.fromstring(comments_xml).iter(W + "comment"))
                )
            else:
                c_count = 0
            print(
                f"  tracked-changes: {ins_count} insertions, {del_count} deletions, {c_count} comments"
            )
        # Stray markup
        body_text = etree.tostring(body_root, encoding="unicode")
        for marker in ("~~", "++", "[R", "[EC-"):
            if marker in body_text:
                # Allow these inside CommentReferences? Just warn, not fail.
                if marker in ("[R", "[EC-") and "commentReference" in body_text:
                    pass
                else:
                    issues.append(f"Stray markup token '{marker}' found in body")
                    break
    return issues


# --- CLI -------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument(
        "--mode",
        choices=["tracked", "clean", "highlight"],
        default="tracked",
    )
    ap.add_argument("--author", default="Author")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    src = Path(args.input).read_text(encoding="utf-8")
    out_path = Path(args.output)

    doc, comments, when = build_document(
        source_md=src,
        mode=args.mode,
        author=args.author,
        title=args.title,
    )
    save_with_comments(doc, out_path, comments, when, args.mode)

    issues = validate(out_path, args.mode)
    if issues:
        print("VALIDATION ISSUES:", file=sys.stderr)
        for i in issues:
            print(f"  - {i}", file=sys.stderr)
        sys.exit(2)
    print(f"Wrote {out_path}  (mode={args.mode}, author={args.author!r})")


if __name__ == "__main__":
    main()
