# Research: Source Faithfulness, Citation, and Integrity Contract

> **Read this file any time you are searching for sources, citing literature, extracting from papers, or making any factual claim that depends on a specific source.** This is the integrity contract for everything in the framework that touches sources.

This file applies universally:
- Manuscript writing (literature reviews, citations)
- Topic writing (syntheses, briefs, perspectives)
- Reviewer replies (when ADD-CITE or DEFEND comments need literature support)
- Knowledge base ingestion (must be source-faithful)
- Domain-specific extraction workflows (e.g., per-species or per-system parameter pulls)
- Any agent specialist doing literature work

---

## Part 1: Integrity Contract

These five rules are mandatory for any task involving sources, citations, or quantitative claims from literature. Violating them is a hard failure: better to flag uncertainty than to ship a fabricated claim.

### 1. Source faithfulness

Every claim attributed to a source must trace to an actual document the agent has read or has direct access to.

- No "sounds plausible" citations. No half-remembered numbers.
- Verbatim quotes are verbatim. No paraphrase smuggled into quote marks.
- Paraphrases preserve meaning. They don't embellish, extend, or invert what the source actually said.
- If you're paraphrasing, the source must say substantially what you're claiming. Don't stretch a study about one system to support a claim about another unless the study explicitly addresses both.

### 2. Citation accuracy

Every citation in any document the user ships must have correct metadata.

- Authors, year, title, journal, volume, pages, DOI: all match the actual source
- No fabricated citations
- When pulling a citation from another paper's bibliography, verify the original exists. Telephone-game citations are common; the original sometimes doesn't say what the second-hand source claims
- The references list matches the in-text citations exactly. No orphans (in references but not cited), no ghosts (cited but not in references)
- Author lists are accurate (et al. only when there are at least three authors and journal style permits)

### 3. Quantitative claims

Numbers from literature must be exact and traceable to a specific source location.

- Sample sizes, effect sizes, p-values, ranges, percentages: all verified against the source
- Units checked, including SI vs imperial conversions, log vs linear scales
- If estimating a number from a figure (for example, reading a value off a published curve), flag it explicitly: "approximately X, estimated from Fig. 2 of Smith et al. 2020"
- Page references are useful for extracted quantities, especially in long sources

### 4. Uncertainty handling

When unsure whether a source supports a claim, hedge or refuse. Don't make plausible-sounding stuff up.

- Distinguish "I read this and it says X" from "this is broadly believed in the field"
- Distinguish "the source explicitly states X" from "the source implies X"
- When you cannot verify a citation's metadata or content, flag it explicitly: "I believe there is a paper by [Author] on [topic] around [year], but I cannot verify the full citation. Please confirm."
- When evidence is mixed across sources, present both rather than silently choosing one
- Better to say "this claim needs a citation I can't verify" than to provide a confident-sounding fake

### 5. Quality control gate

Before any drafted document goes out (manuscript, report, reviewer reply, knowledge base article, parameter record), self-check:

- Every citation traces to a real, verifiable source
- Every number has a source location
- Every direct quote is verbatim against the source
- Every paraphrase faithfully preserves the source's meaning
- Unverified content is flagged for the user, not shipped silently

If you can't verify it, you flag it. Never ship it.

---

## Part 2: Methodology Rules

These extend the integrity contract with practical guidance for how to find, evaluate, and integrate references.

### Rule M1: Verify claim-citation alignment

A citation must actually say what you're using it to say.

- **Read, don't assume.** If you have access to the paper (or its abstract), confirm the finding matches the claim. Don't cite a paper based on its title alone.
- **Check specificity.** A paper about one species or system doesn't support a claim about a different species or system unless the paper explicitly makes that comparison or the claim is framed generally.
- **Watch for telephone-game citations.** Papers often get cited for claims they don't actually make, usually because an intermediate review paper paraphrased loosely. Go to the primary source when possible.
- **Flag mismatches.** If an existing citation in a draft doesn't support the claim it's attached to, flag it: "This citation appears to address [X], but the claim is about [Y]. Please verify or replace."

### Rule M2: Prioritize relevance over prestige

The best citation is the one that most directly supports the specific claim.

- **Direct relevance first.** A perfectly relevant paper in a specialist journal beats a tangentially related one in a high-profile generalist outlet. Don't pad citations with high-impact papers that only loosely connect.
- **Specific over general.** If a claim is about a specific method or measurement, cite the paper that performed that exact measurement. Not a broad review unless the review specifically synthesizes that point.
- **Same system when possible.** For domain-specific claims, papers from the same study system carry more weight than analogues from distant systems. Use analogues when direct evidence doesn't exist, but frame them as such ("Similar patterns have been observed in [analogous system]; Citation").

### Rule M3: Balance foundational and recent work

A strong reference list includes both landmark papers and current literature.

- **Foundational papers** establish concepts and frameworks. Anchor the intellectual lineage of the work; include them when introducing core concepts. Don't over-cite classics just for authority.
- **Recent papers** (last 5 to 10 years) show the current state of knowledge. They demonstrate awareness of the field and often contain the most relevant methodological or empirical advances. These should make up the majority of citations.
- **Fill the middle** when appropriate: key papers from intermediate decades that shifted thinking or introduced methods still in use.
- **Don't stack one era.** An introduction that only cites the most recent five years looks like it ignores the field's history. One that only cites old work looks out of date.

### Rule M4: Evaluate citation quality

Not all papers carry equal weight. Consider these factors:

#### Journal reputation

- Peer-reviewed journals in the established outlets of the relevant field are the baseline standard
- Be cautious with predatory or very low-impact journals: not automatically excluded, but the findings should be corroborated elsewhere
- High-impact generalist journals are fine for broad claims but often lack the specificity needed for technical points

#### Citation count and influence

- Highly cited papers are often highly cited for a reason. But citation count alone doesn't make a paper the right one for a specific claim
- A paper with 20 citations that directly measures what you need is better than one with 2000 citations that mentions it in passing
- Consider whether a paper is highly cited because it's foundational or because it's a convenient review that everyone cites reflexively

#### Study design and rigour

- Prioritize empirical studies with clear methods and adequate sample sizes for factual claims
- Use reviews and meta-analyses for broad framing ("X is widely recognized...") but go to primary sources for specific results
- Be aware of sample size, geographic scope, and potential biases in the cited work

#### Preprints and grey literature

- Preprints can be cited for very recent work, but flag them as preprints. They lack peer review and may change
- Government technical reports and agency documents are acceptable and sometimes essential, especially for regulatory, status, or policy context
- Theses and dissertations are acceptable for specific data or findings not published elsewhere, but peer-reviewed publications are preferred when available

### Rule M5: Build balanced citation sets

For any given claim or paragraph, the citation set should be purposeful.

- **No orphan citations.** Every citation must connect to the argument. "(Smith et al. 2015)" sitting alone after a vague statement does no work. See `conventions/manuscript-format.template.md` for citation integration conventions.
- **No citation dumps.** "(refs 1 to 15)" after a general statement signals lazy scholarship. If 15 papers genuinely support the claim, select the three to five most relevant and specific ones.
- **Diverse research groups.** Don't cite only one lab's work to support a claim (unless they're genuinely the only group that has studied it). Show breadth of evidence.
- **Include self-citations naturally.** The user's prior work is often directly relevant. Include it alongside others where appropriate. Don't over-emphasize or avoid.
- **Acknowledge disagreement.** If evidence is mixed, cite both supporting and contradicting papers and frame accordingly: "While [Author1] found X, [Author2] reported Y, suggesting that [contextual explanation]."

### Rule M6: Smart search strategies

When searching for literature to support a claim:

#### Start with what you know

- Check what the user's own papers cite for similar claims; their reference lists are curated and relevant
- Look at recent review papers in the target area for a current overview of who's publishing what

#### Forward and backward citation chaining

- **Backward:** Check the reference list of a key paper to find its sources
- **Forward:** Use Google Scholar's "Cited by" to find newer papers that build on a key finding
- This is often more productive than keyword searching for specific claims

#### Search term strategy

- Use specific terms, not broad ones. A precise multi-word phrase beats a single broad keyword
- Include system, study type, or method names to narrow results
- Try alternative terms and synonyms; field-specific vocabulary varies

#### Databases

- Google Scholar for broad searching and citation chaining
- Web of Science for more structured searches and citation metrics
- Journal-specific searches when targeting a particular outlet

### Rule M7: Match citation style to section

Different sections of a paper call for different citation approaches (see also `conventions/manuscript-format.template.md`):

- **Introduction:** High density. Foundational and recent. Woven into narrative. Citations build the argument for why the work matters
- **Methods:** Moderate. Cite protocols, software, prior methodological papers. Self-citation for established methods is appropriate
- **Results:** Minimal. Only cite benchmarks or comparative values from other studies
- **Discussion:** High density. Compare findings to specific prior work. Cite both supporting and contradicting evidence. Include literature that offers alternative explanations

### Rule M8: When recommending new references

If the user asks you to suggest references for a claim or section:

1. **State the claim clearly**: what exactly needs support
2. **Search using the strategies above**: start with known literature, chain outward
3. **For each recommendation, provide:**
   - Full citation (authors, year, title, journal)
   - Why it's relevant to the specific claim
   - How confident you are in the citation details (verified vs from memory)
   - Any caveats (for example, "this is from a different study system")
4. **Rank by relevance**, not prestige
5. **Flag any claims you cannot find adequate support for**

### Rule M9: Actively seek disconfirming evidence

Confirmation bias in literature search is a research-integrity failure, not a stylistic weakness. The default search strategy of finding sources that support the claim produces literature reviews that look balanced but selectively quote a one-sided record. A comprehensive, well-balanced state of knowledge requires the search to deliberately look for the counter-record, not only stumble across it.

When searching to support any specific claim:

- **Return at least two to three primary sources that complicate or contradict the working claim**, alongside supporting sources. Frame these as complicating evidence in the output, not as failed search results.
- **If no complicating evidence is found after a deliberate search, say so explicitly.** That is itself a finding: either the claim is genuinely well-supported, or the literature on disagreement is thin, or the search strategy missed the relevant community. Distinguish among these.
- **Do not smooth contradictions out of the synthesis.** If Author A finds X and Author B finds the opposite, report both. Do not collapse to "the evidence suggests X."
- **Search terms matter.** Searching for `[claim]` returns confirming evidence. Searching for `[claim] limitations`, `[claim] inconsistent`, `[claim] reanalysis`, `[opposite of claim] evidence`, or recent critical commentary is more likely to surface the counter-record.
- This rule applies during initial searches, not only during post-hoc contradiction audits.

This is a separate operation from Rule M5 (acknowledging disagreement when found) and any post-hoc contradiction audit. M9 asks the search itself to look for disconfirming evidence from the start.

---

## Part 3: Source Type-Specific Verification

Different source types require different verification protocols. See `agents/literature-extractor.md` and `agents/extraction-validator.md` for the full implementations.

### PDFs (peer-reviewed papers, reports)

The 4-check protocol:
1. **Existence check.** Confirm the PDF exists and matches the claimed citation
2. **Content check.** Confirm the specific claim, quote, or number is in the PDF (find the passage)
3. **Context check.** Confirm the surrounding context doesn't contradict or qualify the claim
4. **Page check.** Note the page or section where the source supports the claim

### Structured data sources (databases, APIs)

- Re-query at the time of extraction to confirm current values
- Note the query date and version of the database
- Flag any values that may change with updates

### Webpages and grey literature

- Note the access date
- Capture the URL and, if possible, an archived version
- Distinguish authoritative sources (government agencies, established databases) from informal sources (blogs, forums)
- Be especially cautious with anything not under version control or peer review

---

## Part 4: General Integrity (Beyond Research)

These rules apply to any task that produces claims, summaries, or analyses, not just literature work.

- **Don't paraphrase tool output, paste it.** When summarizing what a tool returned (a database query result, a model output, a script's stdout), reproduce the actual output. Don't synthesize from memory.
- **Don't claim untested code behavior.** Distinguish "I ran this and it returned X" from "this code should return X." Run, then report.
- **Distinguish observation from inference.** "The model converged" (observation) vs "the model fits well" (inference, requires additional checks).
- **Flag ambiguity.** When a request is ambiguous and the answer depends on interpretation, surface that rather than picking silently.
- **Don't fill gaps with confidence.** When data, source, or context is missing, name the gap. Don't paper it over.

---

## Cross-references

- For citation integration in manuscripts, see `conventions/manuscript-format.template.md`
- For reviewer-reply citation handling (ADD-CITE, DEFEND with literature), see `conventions/reply-format.template.md`
- For knowledge-base ingestion source-faithfulness, see `knowledge_base/SKILL.md`
