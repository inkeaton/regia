# Words that do several jobs, and syntax nobody used

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 19

## Question

After the language tickets have settled what stays, which words get a second spelling and which unused syntax goes?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- D1 A few words do many jobs
- D16 Parts of the syntax the showcase never needed (the language notes)
- D15 the Doc comment above a Multi-definition
- L1 Placeholders are filled by matching (ADR 0001, ADR 0002)
- L4 A Director asks; a setup is written in the Agent's words (ADR 0009)
- L7 Phases are a set, and the `PHASE` lines look like a sequence

Decide:

- Go through the table of D1 row by row: rename, keep, or already changed by an earlier ticket.
- The optional `.`, the `;`, the blank line under a Doc comment, `#@` against `#`, unchecked Imports.
- Confirm or reopen ADRs 0001, 0002 and 0009 as far as the notes touch them.
- Whether `ENDED` stays the word for a Goal that is over, since it is also a Subplot's ending (spec 05, from [*A Goal's life: reached, dropped, repeated*](02-goal-lifecycle.md)).
- Whether `BY` and `WITH` stay the words on a Goal's ending (`WHEN g FAILED WITH r BY Role ?who`, spec 05 and 11, from [*Failure a Plan can read, and answers to an `ASK`*](03-failure-and-replies.md)), next to `SHIFTS … BY` and `END PLOT WITH`.
- Whether `GAME`, `ME` and `OR` stay the words after `FROM` (`TO g FROM DIRECTOR OR ME`, spec 03 and 05, from [*The Sender, the game and "me"*](04-sender-and-self.md)).
- Whether `IN <phase>`, `<Plot> RUNNING`, `ENDED WITHOUT OUTCOME`, `DROPPED` on a Subplot, and `EXITED BY PARENT` (a `BY` that isn't a Goal's ending) stay the words (spec 17 and 20, from [*What a Director knows about itself, and how a Subplot's ending is heard*](09-director-state-and-endings.md)).
- Whether `ASSIGNED`, `UNASSIGNED` and `UNTIL EXITED` stay the words for a Playbook given and taken and for a Giving or a Subplot that lasts a Phase (spec 15, from [*When a Giving starts and ends, and what a joiner gets*](05-givings-and-joiners.md)).
- Whether `KIND`, `AGENT`, `LIKE`, `NO KIND`/`NO AGENT` and `SEED` stay the words in Instancing, and the `=` of a Target setting next to the comparison and the naming of a Body (spec 21, from [*Agent kinds and Instancing files*](15-instancing.md)). `COUNT` is now only a kind's starting number and the count of Matches.
- Whether `UNTIL` stays the word for a wait's condition (`WAIT 1 MINUTE, UNTIL on_plate(roast).`) next to `UNTIL EXITED`, and whether `AFTER 30 SECONDS:` stays a Trigger written without `WHEN`, when spec 05 says `WHEN` is the only reaction keyword (spec 12, from [*Time and Actions in the game*](19-time-and-actions.md)).
- Whether `#@allow: <code>` (a doc-comment key that answers a warning) and `?_name` (a named "don't care") stay the spellings (spec 02 and 03, from [*The command line, Programs and Diagnostics*](16-command-line-and-diagnostics.md)).

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

Blocked by every language ticket (01 to 15), since a word is only worth renaming once its construct is known to stay.

## Resolution

Resolved on 2026-11-17, with the user.

- **D1, kept.** No word gets a second spelling. Rows already changed by earlier tickets: `FROM Guest`/`FROM ALL Guest` and the quantity ([*Quotas*](10-quotas.md)), `SELF` ([*Which Plan runs*](12-which-plan-runs.md)), `#%` gone ([*Agent kinds and Instancing files*](15-instancing.md)); `#!` is already a plain comment read only by the test runner (spec 27). The rest is kept because the next word or the place tells the jobs apart, and the checks catch the confusions: `TO`; `AT` (`, AT RANDOM` after a comma, `SUITS p AT n` literals only, `p AT …` only in Instancing); `OR` (`OR:` against the operator); `=` (`R0404`, `R0405`; a Target setting is in another file kind); `COUNT` (`COUNT(cond)` against Instancing's `COUNT n`); the `,` after a condition (Pick words and Label words don't overlap); `.` (spec 01's rule and hint); the quantity in Instancing (no Value exists yet).
- **The words the earlier tickets introduced, kept:** `ENDED` (a Goal's and a Subplot's, both "over, whichever way"), `WITH` (always the Reason or Outcome carried), `BY` (who, in a Goal's ending and `EXITED BY PARENT`; how much, in `SHIFT(S) … BY`), `FROM GAME`, `FROM ME`, `OR`, `ME` next to `SELF`, `IN <phase>`, `<Plot>(args) RUNNING`, `ENDED WITHOUT OUTCOME`, `DROPPED`, `ASSIGNED`, `UNASSIGNED`, `UNTIL EXITED` and a wait's `UNTIL`, `KIND`, `AGENT`, `LIKE`, `NO KIND`/`NO AGENT`, `SEED`, `=` in a Target setting, `#@allow:`, `?_name`, `?x SENT e(args)` and `?` in a Quota.
- **`AFTER d:`, kept.** Spec 05 no longer says `WHEN` is the only reaction keyword: `WHEN` reacts to an Event, and the two Triggers without it are `TO g:` and `AFTER d:`.
- **New, raised by the user: `EVENT` renamed `CUE`, and Event is the general word.** A Cue is the Vocabulary item (`CUE`, `GAME CUE`, a Signal is a Cue). An Event is anything that can start a Plan (a Cue, a Fact learned or forgotten, a Goal pursued or over, a Phase entered, left or timed out, a Playbook given or taken, a Role joined, left or emptied), as in Jason. A Trigger names one Event; a Trigger kind is a sort of Event. `EVENT` is the error `R0513` with the hint "renamed `CUE`". ADR 0039.
- **D16, partly fixed** (its Instancing part was fixed in [*Agent kinds and Instancing files*](15-instancing.md)):
  - *The `.` and the `;`*: both kept, and optional. The user keeps them for generated code and to avoid indentation in complex code: `.` ends a Statement as a new line does, `;` closes a Block as a dedent does. **New: the Flat block.** A header that ends its line, followed by a line at the same indentation, opens a Block that runs until its `;`; inside it, indentation means nothing, all the way down, and `;` closes the innermost open Block. An Inline block still ends at the end of its line, so the indented reading never lies. A Flat block open at the end of the file is `R0107`; a `;` that closes nothing is `R0108`. Which style the guide and the showcase write is under *Not yet specified*.
  - **New, raised by the user: `PASS`**, a Statement that does nothing and gets no warning. An empty Block that has a sibling after it is written `: PASS` (otherwise it would open a Flat block); a bare empty Block still warns (`R0106`), since it may not be written yet; there is no `TODO` keyword. The Visual Editor writes `PASS` in the Blocks it creates empty. An empty Option stays warning-free, and spec 09's example writes `PASS`.
  - *The blank line under a Doc comment, `#@` against `#`*: kept. The blank line is what tells a file's doc comment from the first declaration's, a detached one already warns, and a plain `#` above a Plan can be meant. The showcase writing its Plan docs with `#@` is guide work.
  - *Unchecked Imports*: kept. Using a name reached through another file's import is meant (hub files), `R1004`'s hint covers the break, and the Visual Editor marks such names `↗↗`.
  - *The Visual Editor's `↗`*: fixed. A name from a directly imported file has no mark, only its underline and tooltip; `↗↗` stays for transitive names.
- **D15 (a Doc comment above a line of several items), fixed.** It documents every item on the line; to document one item, declare it alone.
- **L1, kept.** ADR 0001 and ADR 0002 stand. A misspelt `?woh` is `R0307` or `R0304`; naming against comparing is `R0404`/`R0405`.
- **L4, kept.** ADR 0009 stands. Under `STARTS WITH:` the setup lines describe the state the Agent starts in, and the same lines are on a `KIND` in Instancing, where no Director speaks. Spec 16 now says that a setup's `PURSUE` is the Director's nudge, the one `PURSUE` that isn't the Agent's decision.
- **L7, kept.** Phases stay a set: `INITIAL` marks the start, the drawing shows the transitions, and a Phase no `TRANSITION TO` reaches is already the warning `R2011` (agreed as new during the grilling; it was there).

Changed:

- Spec: chapter 01 (the two styles, Flat blocks, `;` that isn't redundant, indentation rules, `PASS` and empty Blocks, `R0107`, `R0108`), 02 (a doc comment on a line of several items), 05 (`CUE`, *Events*, `WHEN` and the Triggers without it, `R0513`, the rename out of *Not decided here*), 08 (`PASS` in the set, the reserved words and the ASL notes), 09 (the empty Option writes `PASS`), 16 (a setup's `PURSUE` is a nudge), 25 (no `↗` for a direct import). `EVENT` → `CUE` and Event → Cue across every chapter, with `regia_cue`, `regia_game(cue, …)` and the console's `> cue` (28, 30, 34, 37). The Conformance cases in `docs/spec/cases/` declare `CUE`, and the one trace case uses `> cue`.
- ADRs: 0039 *A Cue is declared; an Event is anything that starts a Plan*. 0001, 0002 and 0009 stand.
- Glossary: *Cue* (was *Event*), *Event* (new, the general word), *Trigger*, *Trigger kind*, *Block*, *Flat block* (new).

Handed on:

- To the guide and showcase (fog on the map): `EVENT` → `CUE`, one house style for the trailing `.`, Plan docs written with `#@`, empty Options with `PASS`.
- New Conformance cases for `R0107`, `R0108`, `R0513` and `PASS`: under *Not yet specified*.

1.5: D1 kept, D15, D16, L1, L4, L7: in. Flat blocks, `PASS` and the `CUE` rename: in. The words of systems that are later (`FROM GAME`/`FROM ME`/`OR`, `BY`, `SENT`) follow their systems. None of this needs a later part.
