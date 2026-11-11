# Map: Regia 2.0 guide

Label: wayfinder:map

## Destination

A guide to Regia 2.0 in `docs/guide/`: primer-style files, one per topic, describing the language, the Transpiler, the Visual Editor and the translation to ASL as we plan to build them, from the point of view of someone using the language. It is full of examples drawn from one example world, and ends with a showcase Program, its walkthrough, and a Review List of every design smell found while writing. The guide is then used to revise the design in a later effort.

## Notes

- **This map carries execution.** Three decision tickets come first; the rest are writing tickets, one per file, each sized to one session.
- **The guide is derived, never normative.** `docs/spec/`, `GLOSSARY.md` and `docs/adr/` stay the source of truth. Where the guide and the spec disagree, the spec wins and the guide is fixed. `docs/primer/` stays frozen.
- **No design changes here.** Anything awkward (constructs that read alike, an example needing too much ceremony, a rule that is hard to explain) is tagged inline `#revise` with a one-line reason, and collected in the Review List.
- **Voice**: "we", as in the primer ("we write…", "we declare…"). Example first, rule second. Spec pointers ("Spec: chapter NN") at the foot of a section instead of restated rules or Diagnostic codes.
- **Vocabulary**: glossary names only. Precedence, not priority; Placeholder, not variable; Match and Pick, not "matching system".
- **One example world.** Every chapter takes its snippets from `docs/guide/showcase/`, written before the chapters. A chapter may add to the showcase when a construct has no natural place; a construct that never finds one is a `#revise`. Small throwaway snippets are fine where the world doesn't fit.
- **Chapter template**, fixed by the sample `docs/guide/6 - Matching.md`. Read the sample before writing a chapter.
  - *Opening*: no heading. One paragraph on what the construct is for, starting from a concrete case at the banquet, then a line naming the neighbouring chapters.
  - *Sections*: one `##` per construct, from simple to full. A snippet first, then two to four short paragraphs. Rules that need listing go in a short bullet list or one small table. About 1,300 words for a chapter of this size.
  - *Snippets*: the showcase path on its own line above the code block (`` `showcase/playbooks/dining.regia` ``). Cut verbatim from the showcase, trimmed if needed. A snippet with no path line is a throwaway variant.
  - *`#revise`*: its own paragraph at the end of the section it belongs to, starting with the tag, one or two sentences of reason. Only for problems of the language.
  - *Showcase gaps*: a problem of the example alone (a construct the world doesn't use yet) is not a `#revise`. It goes in the README's *Gaps in the showcase*, with the chapter that found it.
  - *Spec pointers*: the last line of a section, `Spec: chapter 26.` No Diagnostic codes.
  - *Cross-references*: other chapters by title in italics, no numbers and no links.
  - *How this combines with…*: one `###` per interacting system, built on a showcase snippet where there is one, ending with the chapters to read in parentheses.
  - *Diagrams*: a `mermaid` block where a relation between parts is easier to see than to read (who sends what to whom, Phases, which Plot gives which Playbook). Not for decoration.
  - *Since 1.0*: two or three lines of prose, then one `#changes` line per change.
  - *Style*: no bold for emphasis, no em dashes, sentence-case headings.
- **Newer systems get the most examples and scrutiny**: Placeholders and Expressions, Goals and Trigger kinds, `GIVEN` versus `IF`, Match selection, Random choice, Failure, Precedence with Suits and Shifts, Playbook Roles and Mappings, Role setup, Subplots and Stagings, Quota Triggers, cast changes, Instancing. Their interactions matter most.
- **Examples can't be run**: no Transpiler exists. Every writing ticket ends by re-reading its examples against the cited spec chapters.
- **The ASL chapter** covers the whole translation, ordered by construct (the guide's order), not by mechanism (the spec's order).
- Files are named as the primer's: `docs/guide/<n> - <Title>.md`.
- Tickets: `.scratch/regia-guide/issues/NN-<slug>.md`, with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first. Writing tickets 04–20 are independent and may run in parallel.
- Skills: `grilling` and `domain-modeling` for the grilling ticket; `prototype` for the two prototype tickets; `humanizer:humanizer` as a last pass on each chapter.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [Choose the example world](issues/01-choose-the-example-world.md): the 1.0 royal banquet extended into one evening in a concrete 3D hall; `RoyalBanquet` is the Root Plot with Subplots `HonorDuel` and `Poisoning`, seven Playbooks, six Agent kinds; outline in `docs/guide/showcase/README.md`.
- [Write the showcase Program](issues/02-write-the-showcase-program.md): about 550 lines in `docs/guide/showcase/` (one Vocabulary file, eight Playbooks, three Plots, two `.regin` files); the outline was adjusted (duel casting, an eighth Playbook `Wagering`, `Scheming` by Role setup) and 19 `#revise` notes are in the README.
- [Fix the chapter template with a sample chapter](issues/03-chapter-template-and-sample.md): the sample is `docs/guide/6 - Matching.md`; the template is in the Notes; showcase-only problems go in the README's *Gaps in the showcase*, and mermaid diagrams are used where they explain a relation.
- [Write: Introduction](issues/04-write-introduction.md): `docs/guide/0 - Introduction.md` is written, with no *How this combines with…* part since it covers no construct; it found no `#revise` and left the showcase unchanged.
- [Write: The Logic of Regia](issues/05-write-the-logic-of-regia.md): `docs/guide/1 - The Logic of Regia.md` reads the banquet up to the toast as cuts of five showcase files (nothing added to the showcase), about 2,050 words; one new `#revise` (a Playbook's Goals and Signals are an undeclared contract with its Plot) and one repeating the README's `Host`/`host` note.

## Not yet specified

- A consistency pass across chapters once they exist. Its shape depends on how much the parallel writing drifts (terms, repeated explanations, snippets that changed in the showcase after a chapter quoted them). First drift seen: chapter titles are cited in two capitalisations (*Quotas and Cast Changes* in *Introduction*, *Quotas and cast changes* in *Matching*).
- Whether *Write: Translation to ASL* splits into two tickets, known once the template fixes chapter length.
- Filling the *Gaps in the showcase* (the first is a use for `LOWEST`), once the chapters have listed them. One ticket or several, depending on how many there are.
- Glossary fixes, if writing shows a term that is wrong or missing rather than merely awkward (awkward is a `#revise`).

## Out of scope

- Changing the design, the spec or the ADRs: the later revision effort, fed by the Review List.
- Building the Transpiler or the Visual Editor, and running any example.
- Editing or replacing `docs/primer/`.
- A tutorial or reference for end users of a released Regia: this guide is a design-review instrument.
