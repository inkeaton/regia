# Map: The Regia 1.5 showcase and guide, after the syntax review

Label: wayfinder:map

## Destination

The 1.5 showcase in `docs/showcase/` is written in the syntax the syntax review settled, and the spec's line citations into it point at the right lines again. A new guide to Regia 1.5 in `docs/guide/` replaces the old one, as the human-friendly reference used while building the Transpiler and the Visual Editor. The old guide chapters and `docs/guide/showcase/` are deleted (git history keeps them).

Charted with the user on 2026-11-20.

## Notes

- **This map carries execution.** Decision tickets (the chapter list, the template) come first; the rest are execution tickets that write files, each sized to one session.
- **Strictly 1.5.** The guide describes Regia 1.5 only (ADR 0025; every spec chapter's `## Regia 1.5` section; the index in chapter 27). Where a 1.5 pattern stands in for a 2.0 construct, a short "In 2.0" note names the construct and its chapter, with no 2.0 code, as in the showcase.
- **A reference, not a review.** The old guide was a design-review instrument; this one is read by whoever builds the Transpiler and the Visual Editor. No `#revise` tags and no Review List. The guide is derived and never normative: `docs/spec/`, `GLOSSARY.md` and `docs/adr/` win, and where the guide disagrees the guide is fixed.
- **Findings** (a spec contradiction, a gap, a glossary term that is wrong) go one per line into [`findings.md`](findings.md), with the ticket that found them. Fixing them is a later spec effort, unless a finding blocks a chapter: then it becomes a ticket here.
- **Write fresh.** Each chapter is written against the spec and the new showcase. The old chapters (`docs/guide/0–20`) are source material for examples and explanations that are still true, never a base to patch.
- **Template** (fixed by [*The chapter template, fixed by a sample chapter*](issues/05-chapter-template-and-sample.md); the sample is [`docs/guide/10-messages.md`](../../docs/guide/10-messages.md), copy its shape). "We" voice, example first and rule second, one `##` per construct from simple to full, *How this combines with…* last, mermaid where a relation is easier seen than read, `Spec: chapter NN` as the last line of every section. Above each snippet, a link to its showcase file, no line numbers; the snippet verbatim, outer indentation stripped. "In 2.0": a `> **In 2.0**` blockquote of two or three sentences where the 1.5 stand-in shows, naming construct and spec section, no 2.0 code. *Checks* per section before `Spec:`: `misuse → code (tag)`, errors, warnings, Trace codes and `R0109`, borrowing other chapters' codes where the misuse is in this section; codes only there, never in prose. State every rule a tool builder needs; rationale stays in the spec. No bold on bullet leads. Dropped: `#revise`, *Since 1.0*, *Gaps in the showcase*. Each writing ticket adds `Guide: <title>` under the showcase README's heading for each spec chapter it draws on.
- **Every snippet comes from `docs/showcase/`**, so the showcase is brought up to date before any chapter is written. Throwaway snippets are fine where the banquet doesn't fit.
- **The syntax hand-off.** The renames are chapter 01's *Retired spellings* table; the changes that aren't errors and the prose check against `GLOSSARY.md` are in the resolution of [*The hand-off to the showcase*](../syntax-review/issues/14-showcase-hand-off.md).
- **Examples can't be run**: no Transpiler exists. Every execution ticket ends by re-reading its examples against the cited spec chapters, plus a grep for retired spellings.
- Tickets: `.scratch/regia-1-5-guide/issues/NN-<slug>.md`, with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier is the open, unblocked, unclaimed tickets, lowest number first.
- Skills: `prototype` for prototype tickets; `grilling` and `domain-modeling` for any grilling ticket; `humanizer:humanizer` as a last pass on each chapter. Memories: *Regia is generated too*, *Language vs game design*, *Playbooks decide, Plots nudge*.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

- [Rename generated ASL names built on retired words](issues/01-rename-generated-asl-names.md): `regia_unassigned` → `regia_removed`, `!regia_transition` → `!regia_enter`, Quota `percent(p)` → `share(p)`; nothing else in 28–40 or the glossary was built on a retired word
- [Bring the showcase to the 1.5 syntax](issues/02-showcase-to-1-5-syntax.md): Program, README and spec citations in the 1.5 syntax; only `noble_socializing.regia` moved (+1 from line 11, four citations re-pointed); two non-blocking findings
- [Refresh the two decided outlines](issues/03-refresh-decided-outlines.md): walkthrough and Jason outlines reworded for 1.5 syntax, renamed ASL names and the game link (plus chapter 28's current Build tree); no decision changed, no findings
- [The guide's chapter list](issues/04-guide-chapter-list.md): 26 files in five parts ([outline](prototypes/chapter-list-outline.md)), `NN-slug.md` plus `README.md`; five Jason chapters, leaving and the Trace get their own; *Messages* is the sample, then 02–25 in parallel, then 01 and the README
- [The chapter template, fixed by a sample chapter](issues/05-chapter-template-and-sample.md): *Messages* written and accepted as drafted; Checks per section with borrowed codes, snippet links without line numbers, "In 2.0" as a short blockquote, old chapters' length; template in Notes
- [Write guide chapter 02, Syntax](issues/06-write-02-syntax.md): `02-syntax.md` written; adds clauses and the comma to the outline's list; one finding (`#@key[` and `R0201`)
- [Write guide chapter 03, Vocabulary and files](issues/07-write-03-vocabulary-and-files.md): `03-vocabulary-and-files.md` written; adds Propensities, `.regin` imports and a broken-transitive-name example; four non-blocking findings
- [Write guide chapter 04, Plans](issues/08-write-04-plans.md): `04-plans.md` written; falling through gets its own section; "In 2.0" notes on `FROM GAME` and `FROM ME` (the `fight`/`strike` split); no findings

## Not yet specified

- **A consistency pass** across chapters: terms, chapter titles, snippets that drifted from the showcase. Its shape depends on how much the writing drifts.
- **Deleting the old guide** (`docs/guide/` old chapters, `docs/guide/showcase/`) once nothing in the repo cites them; who cites them (spec chapter headers, ADRs, scratch maps) is checked then.
- **Findings that block a chapter**, if any, become tickets here.

## Out of scope

- The showcase map's hand-off work: the walkthrough guide, the four runs in `docs/showcase/runs/`, and the Jason reference Build with its guide in `docs/showcase/jason/`. This map only refreshes their two outlines.
- Fixing findings in the spec, ADRs or glossary: a later spec effort.
- Constructs that only Regia 2.0 has.
- Editing `docs/primer/`.
