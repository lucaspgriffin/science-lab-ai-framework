# Reply format template: Reviewer-reply conventions

> **This is a scaffold, not a finished file.** Copy it to `conventions/reply-format.md` in your lab's working framework and fill in every `[adopter: ...]` slot. The worked examples use a running adopter scenario (a fictional terrestrial ecology lab handling a *Journal of Animal Ecology* revision). Delete the examples once you have written your own.

This file is a **delta** on `conventions/voice.template.md` and `conventions/manuscript-format.template.md`. Those two files set the lab's writing voice and document conventions; this one adds the reply-specific rules for tone with reviewers, structure of the response document, comment labelling, and tracked-changes manuscript conventions.

---

## 1. Response document structure

The reply document is a separate file from the revised manuscript. Its structure should be predictable so that reviewers can scan it efficiently.

`[adopter: state your reply document structure: opening paragraph, per-reviewer sections, per-comment formatting, closing.]`

> **Example: the ecology lab uses this structure.**
> ```
> # Response to Reviewers: [Manuscript ID]
>
> We thank the reviewers for their careful reading and constructive comments. The
> revised manuscript has benefited substantially from their feedback. Below, each
> reviewer comment appears in italic, followed by our response and pointers to
> specific manuscript locations where changes were made.
>
> ## Reviewer 1
>
> ### R1-C1
> *[verbatim reviewer comment]*
>
> Response: [reply text]
>
> Manuscript changes: [location: page/line refs, or section/paragraph refs]
>
> ### R1-C2
> ...
>
> ## Reviewer 2
> ...
>
> ## Editor comments
> ...
> ```

---

## 2. Comment labelling

`[adopter: state your comment ID scheme and any classification taxonomy you use to triage comments before drafting.]`

> **Example: the ecology lab uses these labels.**
> - **R[N]-C[M]**: Reviewer N, Comment M (e.g., R1-C3).
> - Comment classification (internal, not in the reply document):
>   - **AGREE**: reviewer is right; manuscript was updated to reflect the suggestion.
>   - **PARTIAL**: reviewer raises a valid point but the full fix is out of scope; explain and partially accommodate.
>   - **PUSHBACK**: reviewer's premise is incorrect, the suggestion would worsen the paper, or the comment misreads the manuscript. Push back politely with specific evidence.
>   - **ADD-CITE**: reviewer wants a citation added; verify the citation supports the claim, then add.
>   - **NEW-ANALYSIS**: reviewer requests a new analysis; budget the work, do it if feasible, defer with justification if not.
>   - **RESTRUCTURE**: reviewer wants paragraphs or sections moved; consider the trade-off against the existing narrative.

---

## 3. Tone with reviewers

The reply voice is closer to a polite colleague than to the manuscript voice. It is direct but warm; specific but not pedantic; assertive when pushing back but never dismissive.

`[adopter: state your reply tone in 3 to 5 sentences. Include the opening-paragraph convention and rules for thanking reviewers.]`

> **Example: the ecology lab uses this reply tone.** Direct, specific, warm but not effusive. Open the reply document with one paragraph thanking the reviewers; do not repeat thanks per comment (that becomes performative). Use "we" throughout. Quote the reviewer's wording verbatim when responding ("The reviewer notes that ..."); avoid paraphrasing the reviewer in a way that softens or hardens their point. When the reviewer is correct, say so without grovelling: "The reviewer is correct; we have updated [section] accordingly." When pushing back, lead with the evidence, not the disagreement: "The cited analysis (Figure 3B, Methods p. 12) addresses this; we have added a sentence in the Results to make the connection clearer."

---

## 4. When to push back

Pushback is structurally important: a reply that accepts every comment without question signals that the authors are anxious, not that the manuscript is good. Reviewers can be wrong, and editors expect authors to defend the science.

`[adopter: state your criteria for pushback. When is it appropriate? What evidence must accompany pushback? What tone?]`

> **Example: the ecology lab pushes back when ...** the reviewer's premise is factually incorrect (e.g., they request an analysis already in the supplement), or their suggested change would weaken the paper (e.g., removing a control that the authors believe is load-bearing). Pushback always cites specific manuscript locations or specific external evidence. The push is two sentences maximum, followed by an offer of a compromise where one exists: "While we maintain that [position], we have added a sentence on page X clarifying [the reviewer's concern]." Never push back on stylistic preferences (figure colour, paragraph order) unless the change would materially harm the paper.

---

## 5. Manuscript-edit conventions for tracked changes

The revised manuscript is submitted as a tracked-changes document so reviewers and editors can see exactly what changed. Your fork's manuscript builder skill should handle the rendering; this section specifies the source-side conventions.

`[adopter: state your tracked-change markup conventions in the source markdown or .docx, and the rules for what gets tracked vs silently edited.]`

> **Example: the ecology lab uses these tracked-change conventions.** Source markdown uses `~~deletion~~` for removed text and `++insertion++` for added text. The manuscript-builder skill converts these to Word tracked changes at .docx render. What gets tracked: any substantive change in response to a reviewer comment (added sentences, modified claims, new figures, expanded methods). What is silently edited: typo fixes, copy-edit cleanups discovered during revision, and any change requested by no reviewer that improves clarity. The tracked-changes document is paired with a clean-version document on submission.

---

## 6. Per-comment reply structure

Each individual reply has a predictable shape. Reviewers scan; they do not read the response document the way they read the manuscript.

`[adopter: state your per-comment reply structure: opening, body, manuscript-pointer convention.]`

> **Example: the ecology lab uses this per-comment structure.**
> 1. **Opening line**: classify the response (one of: "The reviewer is correct ...", "We agree and have ...", "We respectfully maintain that ...", "We have addressed this by ..."). One line.
> 2. **Body**: the actual response. 2 to 5 sentences. Cite evidence (figure refs, methods locations, external papers). For NEW-ANALYSIS comments, summarise the result with at least one number.
> 3. **Manuscript pointer**: explicit reference to where the change appears in the revised manuscript: "Manuscript changes: Results paragraph 3, page 7; new Supp Figure 8."

---

## 7. Citations in the reply document

Replies sometimes need to cite new literature (in support of a pushback or to address an ADD-CITE comment).

`[adopter: state your citation conventions for the reply document. Same style as manuscript? Inline vs full citation? Cross-link to manuscript references?]`

> **Example: the ecology lab uses these conventions.** Reply document uses the same reference style as the manuscript (author-year alphabetical). New references added in revision are inserted into the manuscript reference list; the reply document uses the same author-year citation form. When the reply cites a paper that is NOT being added to the manuscript (e.g., a paper supporting the push-back but not load-bearing in the manuscript itself), the reply gives a full inline citation (Author Year, journal) with the DOI.

---

## 8. Editor-comment handling

`[adopter: state your conventions for handling editor comments. Higher priority than reviewer comments? Different tone?]`

> **Example: the ecology lab handles editor comments distinctly.** Editor comments get their own section at the end of the reply document. Tone is slightly more formal than reviewer responses (editors set policy; reviewers offer opinions). When the editor raises a substantive point already addressed by a reviewer response, cross-reference: "We have addressed this in our response to Reviewer 2, Comment 3." When the editor flags policy items (data deposition, code availability, ethics statements), respond with a one-line confirmation and a manuscript pointer.

---

## 9. Closing

`[adopter: state whether your replies have a closing paragraph and what it contains.]`

> **Example: the ecology lab uses this closing.** One closing paragraph after the editor comments: "We thank the reviewers and the editor for their detailed engagement with this work. We believe the revised manuscript is substantially stronger as a result, and we hope it is now suitable for publication in [journal]." That is the entire closing; no apologies, no further reframing.

---

## Cross-references

- Base voice rules: `conventions/voice.template.md`
- Manuscript-level structure (which sections/lines you cite when pointing reviewers to changes): `conventions/manuscript-format.template.md`
- Citation and source verification for ADD-CITE comments: `conventions/research.md`
