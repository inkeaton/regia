# Decide: Diagnostic codes and the Vocabulary

Type: grilling
Status: closed
Assignee: claude
Blocked by:

## Question

Which code, if any, does each of these misuses get, and what does the Vocabulary include? Tool builders hard-code codes, so each answer has to be final.

- F9: is an unclosed `#@key[` `R0201`? (Guide: yes.)
- F10, F13: does `GAME TRAIT` / `GAME MOOD` get a code (a new one, or `R1016` widened)? Should `R1005`'s line name `GAME`?
- F12 (first half): does the glossary's *Vocabulary* include declared Names?
- F14: a Role name used as a Value is `R0303` or `R1501`. Which one is retired? (Guide: `R0303`.)
- F15: a Placeholder filled by `LET` in only some branches or Options: widen `R0305` or add a code? (Guide: `R0305`.)
- F16: chapter 03, *"Don't care"*: one case or two, and what does the sentence say?
- F17: does `R0404`'s line cover an `IF` condition too?
- F19: does `GIVEN 3 OF …` get a code?
- F20: is `, UNTIL` part of `WAIT`'s own form, or does `R0805` name it? (Guide: its own form.)
- F28: is a `ROLE` line after a Trigger Block an error with a code, or a convention?
- F29: which `ENDED` does `R2005` mean? (Guide: only `ENTERED` and `EXITED`.)
- F33: `ENTER` in a Plot with no Phases: `R2008`, or a code of its own? (Guide: `R2008`.)
- F36: a local Cue as an Outcome: `R1703`, `R1004`, or a new code?
- F41: is `WHEN e, FROM ?who` with no Role checked by `R3802`?

Start each question from the guide's reading. For each answer, record the code and its chapter, and whether a code is retired.

Applying the answers is *Apply: Diagnostic codes and the Vocabulary*.

## Resolution

Decided with the user on 2026-11-23. Every answer takes the guide's reading where it had one. Codes are listed with their chapter.

- **F9** (ch 02): an unclosed `#@key[` is `R0201`. Line: "An unclosed multiline comment, plain (`#[`) or doc (`#@key[`), pointing at its opener."
- **F10** (ch 10): `R1016` widened and written positively: "`GAME` on anything but a `FACT` or a `CUE`, or on a local declaration (a `NAME` line is `R0311`)." No new code.
- **Overlap found while deciding F10**: `GAME` on a `NAME` was both `R0311` and `R1016`. `R0311` keeps it; `R1016` no longer lists `NAME`. Nothing retired.
- **F13** (ch 10): `R1005` reads "…don't agree on kind, parameter count, External name or `GAME`."
- **F12, first half** (`GLOSSARY.md`): Names are **not** Vocabulary. *Vocabulary* adds: "Names are declared too (`NAME`), but they are Values, not Vocabulary."
- **F14**: `R0303` (ch 03) is kept and absorbs `R1501`'s detail: "A Role name used as a Value, as an argument or in an Expression (hint: fill a Placeholder with `FROM Role ?x`)." **`R1501` is retired** in chapter 15, pointing at `R0303`.
- **F15** (ch 03): `R0305` widened: "…filled only under `NOT`, or in only some branches of an `OR`, an `IF` or a `RANDOMLY` (the message names the branch)." `FOR EACH` stays `R2604`. Chapters 04 (*Branches*) and 09 (*Placeholders in an Option*) cite it.
- **F16** (ch 03, *"Don't care"*): one case. "A Placeholder filled by a Trigger shared by several `GIVEN` Blocks is used if any of the Blocks, or the `ELSE`, uses it (chapter 06). This is the only case the writer can't fix with `?`, so it's the only one spared the warning. One filled by a `GIVEN`'s own Context is checked in that Block like any other."
- **F17** (ch 04): `R0404` reads "A comparison in a Context or an `IF` condition with a side that isn't filled yet."
- **F19** (ch 26): **new code `R2607`**: "`n OF` in a Context: a Quota form only (chapter 18; hint: `COUNT(…) >= n`)." The *`COUNT`* bullet cites it.
- **F20** (ch 12): `, UNTIL` is part of `WAIT`'s own form; chapter 12 says so in one bullet. `R0805` is unchanged.
- **F28** (ch 15): convention, no code. "`ROLE` lines are written before the Trigger Blocks by convention; the Transpiler reads them anywhere in the Playbook."
- **F29** (ch 20): `R2005` widened beyond the guide's reading so Subplot endings in a Playbook get a code: "`ENTERED` or `EXITED`, or a Subplot's `FINISHED`, `DROPPED` or `ENDED`, in a Playbook." A Goal's `ENDED` stays legal there.
- **F33** (ch 20): `ENTER` in a Plot with no Phases is `R2008`. The *Declaring Phases* sentence cites it. (`R2014` stays `IN`'s own, since `IN` in a Playbook needs it anyway.)
- **F36** (ch 17, ch 10): a local Cue as an Outcome is `R1004`, since a Plot can't see it. Chapter 17: "…can't be an Outcome: a Plot can't see it (`R1004`)." `R1014` drops its dead "or `END PLOT WITH`" clause (`END PLOT` in a Playbook is already `R1507`).
- **F41** (ch 38): `R3802` widened: "`WHEN e` with any `FROM` (a Role or `?who`) in a Plot where no Playbook the Plot gives Signals `e`." The prose's "a Trigger with no `FROM` is not checked" stays.

**Codes:** one new (`R2607`), one retired (`R1501`). **ADR:** one, for retiring `R1501` into `R0303` (a retired code, per the map's Notes). Every other change is a code assignment or wording change and goes in the spec only.

**Guide impact for the Apply ticket:** the *Checks* lines for `R1016` (guide ch 03), `R2005` (ch 11, adding Subplot endings), `R3802` (ch 15, adding `?who`), any `R1501` citation, and new lines for `R2607` and the `R0305` widening.
