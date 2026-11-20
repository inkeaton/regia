# The chapter template, fixed by a sample chapter

Type: prototype
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 04

## Question

What does a chapter of the 1.5 guide look like on the page? Write chapter 10, *Messages* (`docs/guide/10-messages.md`, spec 07; see `../prototypes/chapter-list-outline.md`), as the sample, for the user to react to, and fix from it the template sketched in the map's Notes:

- the old template's parts that stay (voice, example first, sections simple to full, snippet paths, *How this combines with…*, mermaid, `Spec:` pointers);
- the "In 2.0" note: its shape and where it sits;
- the *Checks* list: its shape, which Diagnostics it lists (errors, warnings, Trace codes?), and how it relates to the spec's own *Transpiler checks*;
- length and how much a reference chapter restates rules versus pointing at the spec, now that its readers are the people building the tools.

The settled template is written into the map's Notes, so every writing ticket loads it. The sample counts as that chapter's writing ticket.

## Resolution

Done with the user on 2026-11-20 (prototype). The sample is the real chapter, [`docs/guide/10-messages.md`](../../../docs/guide/10-messages.md), taken as drafted; it also closes that chapter's writing. The showcase `README.md` has its `Guide: Messages` line under *07 Messaging*.

The template, now in the map's Notes:

- **Kept from the old one**: "we" voice; example first, rule second; one `##` per construct, simple to full; *How this combines with…* as the last `##`, one `###` per neighbouring chapter, cited by title; mermaid where a relation is easier seen than read; `Spec: chapter NN` (plus borrowed chapters) as the last line of every section.
- **Snippet paths**: a link above each snippet, relative to `docs/showcase/` (``[`playbooks/courtesy.regia`](../showcase/playbooks/courtesy.regia)``), **no line numbers** (they go stale). The snippet is copied verbatim, with the enclosing `PLAYBOOK`/`PLOT` indentation stripped.
- **"In 2.0" note**: a blockquote starting `> **In 2.0**`, two or three sentences, in the section where the 1.5 stand-in shows, before *Checks*. It names the construct and the spec chapter and section, says what 1.5 does instead, and has no 2.0 code (keyword names in backticks are fine).
- ***Checks***: **per section**, just before `Spec:`, a bold `**Checks**` line and a list, one misuse per item: `misuse → code`, followed by a tag when it isn't a build error: `(warning)`, `(Trace warning)`, `(Trace, Failure)`, `(Trace, unheard)`; a hint in parentheses where the spec gives one. It lists build errors, build warnings, Trace codes, and `R0109` for 2.0 constructs. It **borrows codes from other spec chapters** when the misuse is in this section's constructs. Codes never appear in prose.
- **Length and restating**: about the old chapters' length (the sample is ~380 lines). Every rule a tool builder needs is stated as plain prose or a bullet, not left as "see spec"; design rationale and ASL notes stay in the spec and the Jason chapters. Settled questions that the old guide carried as `#revise` become plain statements.
- **Last pass**: `humanizer:humanizer` removes decorative bold from bullet leads; bold stays only on `**Checks**` and `**In 2.0**`.

No findings. The writing tickets 06–28 are unblocked.
