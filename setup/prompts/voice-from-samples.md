# Voice inference from sample paragraphs

A prompt template invoked by `setup/SKILL.md` Phase 2. Used to infer voice rules from 2 to 3 sample paragraphs pasted by the adopter, then populate `conventions/voice.md` from `conventions/voice.template.md`.

## Inputs

- 2 to 3 sample paragraphs from the lab's recent published papers (intro, discussion, or abstract).
- The adopter's explicit preferences gathered during Phase 2 Part B (register, hedging stance, banned words, signature phrases, em-dash policy).

## Prompt body (run against the samples)

Read the pasted paragraphs carefully. The goal is to derive a voice fingerprint that will let any future writing match the lab's existing published voice. Do not paraphrase the samples; treat them as the canonical reference.

Identify and record:

1. **Hedging patterns.** For each claim category (direct measurement, statistical result, mechanistic interpretation, generalisation, implication), note how the samples hedge. Quote the exact construction. Example: if a mechanistic claim reads "These results are consistent with X acting upstream of Y", record that pattern as the lab's mechanistic-claim template.

2. **Vocabulary preferences.** List 10 to 15 verbs and 5 to 10 multi-word phrases that recur across the samples. Flag any that appear more than once (these are signature constructions).

3. **Sentence rhythm.** Measure average sentence length, variation, and opening constructions. Note: do three or more sentences in a row begin with the same word; does the lab use single-sentence paragraphs for emphasis; what is the rhythm of short-then-long sentences.

4. **Punctuation quirks.** Are em-dashes present in the samples (count them); is the Oxford comma used; are en-dashes used for ranges; are typographic or straight quotes used. The framework default is hard-ban on em-dashes. If the samples use em-dashes, flag this for the adopter to decide.

5. **Anti-patterns.** Words or constructions that are absent from the samples but common in LLM-default prose (superlatives, "groundbreaking", "highly significant" without numbers, "demonstrates" for correlational findings). Note absences as well as presences.

6. **Register depth.** Technical-vocabulary density (count discipline-specific terms per 100 words). Citation density (citations per 100 words in the samples).

## Merging with explicit preferences

The adopter's explicit Phase 2 Part B answers always win on conflict with the inferred rules. The inference fills gaps the adopter did not explicitly cover.

If the adopter selected "keep em-dash ban" (the framework default) but the samples contain em-dashes, note the discrepancy and prefer the explicit preference. Add a short note in `conventions/voice.md` Section 3 explaining that the published voice once used em-dashes but the lab has chosen to retire them going forward.

## Output

Populate every `[adopter: ...]` slot in `conventions/voice.template.md` with content derived from the inference and the explicit preferences. Specifically:

- Section 1 (Register): fill from explicit preference + inferred technical density.
- Section 2 (Hedging calibration): fill from the inferred patterns in step 1 above.
- Section 3 (Punctuation rules): fill from the explicit em-dash policy + the inferred Oxford-comma and en-dash use.
- Section 4 (Sentence rhythm): fill from step 3 above.
- Section 5 (Words to use): fill from step 2 above, prioritising recurring multi-word phrases.
- Section 6 (Words to avoid): fill from the adopter's explicit banned-words list + step 5 anti-pattern absences.
- Section 7 (Authoring vs editing): use the framework default unless the adopter specified otherwise.
- Section 8 (Writing evolution): fill from any adopter note about voice shifts; otherwise write "Voice is stable as of [year]."
- Section 9 (Voice exemplars): list the source papers of the pasted samples as exemplars.

Remove every worked-example block (`> **Example: ...**`) from the template before saving. These were instructional only.

## Voice constraints on the generated file itself

The generated `conventions/voice.md` must comply with the rules it is documenting:

- No em-dashes in the prose (use colons, semicolons, parentheses, or restructure).
- No superlatives in scaffold text.
- Sentence rhythm should vary across the file (no runs of three or more sentences of similar length in any section).

## Output path

`conventions/voice.md` (with `.template` suffix dropped).
