# Write guide chapter 22, Jason: Plans and Goals

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Write `docs/guide/22-jason-plans-and-goals.md`, *Jason: Plans and Goals*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 39, 40.
- **Covers:** Placeholders and variables, Contexts and `GIVEN`, `IF`, random choice, Picks, `FOR EACH`, `COUNT`, Basic Actions, `WAIT`, Messages; a Pursuit's identity, the ending goals, the generated `-!g`, the walker, `PURSUING`, intentions.
- **Quotes most:** `courtesy.regia`, `scheming.regia`.
- **"In 2.0" notes:** none expected.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.

## Resolution

Done on 2026-11-23 (AFK). [`docs/guide/22-jason-plans-and-goals.md`](../../../docs/guide/22-jason-plans-and-goals.md) written from the template, with `Courtesy`'s `take_seat` as the spine: the whole recipe in ASL (label, trigger with Sender and `Id`, guard, `FROM DIRECTOR` test, `TELL host` to a local Cue, `regia.reached`), then its `T1104` path, its `FAILED`/`ENDED` plans and `WHEN greeting, FROM ?who`.

- Sections: *A Plan in ASL* (with *Placeholders and variables*), *Contexts and `GIVEN`*, *`IF`*, *Random choice*, *Picks*, *`FOR EACH`*, *`COUNT`*, *Basic Actions on Facts*, *`WAIT`*, *Messages* (*Sending*, *Who sent it*, *A told Fact*, *`ME`*, *Nothing heard*), *Goal Statements*, *A Pursuit's identity*, *The ending goals*, *`REACHED`*, *`FAILED`: the generated `-!g`* (with *No applicable `TO` Plan*, *The cause entry*, *A `WHEN` Plan that fails on its own*), *`DROPPED`: the walker*, *`PURSUING`*, *Intentions, in one table*, *How this combines with…*.
- Worked by hand beyond the spec's examples: `Scheming`'s `LOWEST ?size` Pick, `NobleSocializing`'s `WHEN idle` Random choice with `COUNT … PLAYS` and a nested `RANDOM`, `resent`'s `IF`, the `scandal(?victim)` `GIVEN` pair with `effects`, `Duelling`'s non-constant `WAIT RANDOM(1, 3) SECONDS`, `Serving`'s `NOT PURSUING bring(?, ?)`; a sequence diagram of the `sold_out(roast)` chain.
- Quotes `courtesy`, `scheming`, `noble_socializing`, `dining`, `serving`; all snippets checked verbatim against the showcase.
- One "In 2.0" note (`BY`: the ending goals already carry `Id` and Sender), against the ticket's "none expected", because chapter 40's *Regia 1.5* names it.
- Checks borrowed: `R1007`, `R1008`, `R1204`, `T0401`–`T0403`, `T0701`, `T0702`, `T0801`, `T0901`–`T0903`, `T1101`, `T1103`, `T1104`, `T1201`, `T1202`, `T1502`, `T1503`, `T1901`, `T2601`.
- No `Guide:` line: the showcase README's *Coverage* has no heading for chapter 39 or 40.
- Re-read against chapters 39, 40, 29, 32, 35, 37 and 14; grep for retired spellings and glossary _Avoid_ words clean; humanizer pass done.

**Findings** (non-blocking, in `findings.md`): `Me` as the sender's variable in chapters 39 and 29 can join a Placeholder `?me`; no ASL form for `DO a, WITHOUT WAITING`; `UPDATE`'s test needs a `seq` `regia.trace` doesn't return, and the `LEARN`/`FORGET` guards have no form; one `message` entry per `SIGNAL` (35) against one `regia.send` per Director (39).
