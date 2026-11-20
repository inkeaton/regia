# `TO` and `FROM` outside Triggers

Type: grilling
Status: closed
Assignee: claude (with Edoardo)
Blocked by: 01

## Question

`TO` has six uses: `TO g:` (the recipe header), `ASK x TO g`, `ASSIGN P TO Role`, `MAPPING a TO b`, `TRANSITION TO p` and `CHANGE f TO f2`. `FROM` is a Trigger's Sender and also the target of `UNASSIGN P FROM Role`, whose `FROM Role ?who` only looks like the Sender form (ADR 0029).

Apply the test of *The principles of the 1.5 syntax*. For each use, keep it, rename it, or restructure it:
- whether the recipe header changes its word (it is a Trigger, `WHEN`'s sibling);
- whether `ASK … TO` and `ASSIGN … TO`/`UNASSIGN … FROM` share one sense;
- whether `MAPPING a TO b` reads as a direction;
- whether `CHANGE … TO` is "replace with".

Done when chapters 05, 07, 08, 15, 16, 17 and 20 and the affected ADRs (0029) are edited.

## Resolution

Grilled with the user on 2026-11-20. ADR 0043 (`docs/adr/0043-to-introduces-a-goal-with-two-closed-exceptions.md`), amending ADR 0041.

1. **`TO` introduces a Goal.** `TO g:` and `ASK x TO g` are unchanged. The user chose this over making `TO` a destination, because the recipe header is the most-written line in the language.
2. **Two closed exceptions keep a destination `TO`**, for the English idiom: `ASSIGN P TO Role` (unchanged; the user preferred it over recipient-first `ASSIGN Guest P` or a new preposition) and **`UPDATE f TO f2`**, which replaces `CHANGE f TO f2` (the user chose it over `CHANGE f INTO f2`). Chapter 01's *One sense* rule names them, and no other construct may cite them.
3. **`TRANSITION TO p` → `ENTER p.`**: it pairs with `WHEN ENTERED`. "Transition" stays the name of the concept and of the Phase map's edges.
4. **`, MAPPING a TO b` → `, MAPPING a AS b`**: `AS` has the gloss of `ext AS name`.
5. **`UNASSIGN`/`UNASSIGNED` → `REMOVE`/`REMOVED`** (the user's rename, for readability). `REMOVE P FROM R` keeps `FROM`. Its gloss is "where something comes from or leaves", which also covers the Sender. The comma rule wasn't at stake, because chapter 01 already lets a Clause keyword introduce the core's required item (`WAIT UNTIL c`). ADR 0029's shapes are unchanged.
6. **Trace formats are unchanged** (`GIVE … TO … AS …`, `TAKE … FROM …`): they are log output, not Regia. Jason identifiers such as `regia_unassigned` and `regia_transition` are plumbing and were left alone.
7. **Retired spellings are errors with a hint**: `R0808` (`CHANGE`), `R1514` (`MAPPING a TO b`), `R1515` (`UNASSIGN`, `UNASSIGNED`), `R2016` (`TRANSITION TO`). New reserved words: `UPDATE` (08), `REMOVED` (15, with `AS` cross-listed from 10), `ENTER` (20).

Edited: chapters 01 (*One sense*, with the exception), 04, 05, 07, 08 (*Updating a Fact*), 10, 11, 12, 15, 16, 17, 18, 19, 20 (*What `ENTER` does*), 25, 29, 30, 31, 33, 34, 35, 38, 39, 40; the case `cases/08-basic-actions/update-to-another-fact.regia` (renamed from `change-to-…`); `GLOSSARY.md` (*Basic Action*, *Director Statement*, *Phase* now names a transition); ADRs 0029 and 0041 (pointers to 0043). The *Endings and kind words* ticket's question now says `REMOVED`.
