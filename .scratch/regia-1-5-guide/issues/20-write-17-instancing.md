# Write guide chapter 17, Instancing

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

Write `docs/guide/17-instancing.md`, *Instancing*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 21.
- **Covers:** `.regin` files, Agent kinds, how many start, a kind in several Roles, individual Agents, setup lines, starting Propensities, the Root Plot, the seed, Target settings.
- **Quotes most:** `banquet.regin`.
- **"In 2.0" notes:** spawning.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-20 (task). [`docs/guide/17-instancing.md`](../../../docs/guide/17-instancing.md), about 470 lines, written from the template:

- An opening table of the Statements and where each is written.
- Sections, simple to full: Who says what (a Guest's first moment across Program, Instancing and game); Instancing files; The Root Plot; Agent kinds (with *A kind in several Roles*: the knight, and why `Keeping_watch OVER NobleSocializing ON scandal` matters); Starting Propensities; `LIKE` (a table of what a hothead takes from `noble`, `hot_knight` as a throwaway for clashing bases); Individual Agents (with *Instancing names*: `grudge(percival, 2)`); Setup lines (with *Order*, a mermaid of the Root Staging's start); Layering builds (throwaway `small.regin`, an items table, `NO KIND`/`NO AGENT`, `no_percival.regin` breaking the hotheads' grudge, siblings that disagree); With no cast; The seed; Target settings (Jason's three keys).
- One "In 2.0" note, on spawning, under *Agent kinds*. `R2115` is left out: Quotas are 2.0.
- Every showcase snippet checked against `banquet.regin` by script (8 linked snippets); the `.regin` throwaways are named in their first comment line. Codes only in *Checks*.
- `Instancing` added to the `Guide:` line under *21 Instancing* in the showcase README.
- Grep for retired spellings: only `key = value`, on purpose, in the `R2124` check. The humanizer pass replaced a table dash and one staged sentence.

Three non-blocking findings: a kind's setup lines can be replaced but never emptied by a later file; whether `R2122` checks a removed kind's template lines; `runs/short_evening`'s `NO AGENT percival` against the hotheads' grudge.
