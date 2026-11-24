# Apply: Diagnostic codes and the Vocabulary

Type: task
Status: closed
Assignee: claude
Blocked by: 01, 02

## Question

Write the decisions of *Decide: Diagnostic codes and the Vocabulary* into the spec chapters' *Transpiler checks* and prose, chapter 27's *Regia 1.5* table where a code is in it, `GLOSSARY.md`, and any ADR the decision called for.

Then fix the guide's *Checks* lines and passages that the findings name, remove any point settled here from the guide README's paragraph on open details, and grep the edited chapters for retired spellings. Anything new goes to `findings.md`.

Done when every decision is in the spec and the guide agrees with it.

## Resolution

Applied on 2026-11-23. Every decision of *Decide: Diagnostic codes and the Vocabulary* is in the spec, and the guide agrees with it.

**Spec**

- ch 02: `R0201` names plain (`#[`) and doc (`#@key[`) openers.
- ch 03: `R0303` takes "as an argument or in an Expression"; `R0305` adds `IF` and `RANDOMLY` branches; *"Don't care"* now speaks of one spared case; the *Values* prose cites `R0303`.
- ch 04: *Branches* cites `R0305`; `R0404` covers an `IF` condition.
- ch 09: *Placeholders in an Option* cites `R0305`.
- ch 10: `R1005` names `GAME`; `R1014` drops "or `END PLOT WITH`"; `R1016` reads "`GAME` on anything but a `FACT` or a `CUE`, or on a local declaration (a `NAME` line is `R0311`)"; *What the game produces* cites `R1016`; *Local Cues* cites `R1014` and `R1004`.
- ch 12: a bullet saying `, UNTIL` is part of `WAIT`'s own form, so `R0805` doesn't apply.
- ch 15: `ROLE` order is a convention; `R1501` removed from the list and marked retired into `R0303` (ADR 0048), after the existing `R1505` note; the `PLAYS` paragraph cites `R0303`.
- ch 17: *Outcomes* cites `R1004` ("a Plot can't see it").
- ch 20: `R2005` widened to a Subplot's `FINISHED`, `DROPPED`, `ENDED` (a Goal's `ENDED` stays legal); `R2008` covers `ENTER` in a Plot with no Phases; *Declaring Phases* cites it.
- ch 26: new `R2607`; the *`COUNT`* bullet cites it with the `COUNT(…) >= n` fix.
- ch 38: `R3802` and its prose cover `FROM ?who`.
- ch 27's *Regia 1.5* table holds none of these codes; nothing to change there.

**Glossary:** *Vocabulary* says Names are Values, not Vocabulary.

**ADR:** [0048 A Role used as a Value has one code](../../../docs/adr/0048-a-role-used-as-a-value-has-one-code.md).

**Guide:** *Checks* lines updated for `R0201` (02), `R1016` and `R1014`/`R1004` (03), `R0305` (05), `R2005` (11, 12), `R3802` (10, 15, 20 twice); new lines for `R2607` (06) and `R1004` on an Outcome (13). Prose: Names aren't Vocabulary (03), a local Cue isn't visible to a Plot (03), `ROLE` order is a convention (11), the Director's Triggers listed in a Playbook include Subplot endings (11), `FROM ?who` is checked by `R3802` (15), `, UNTIL` is `WAIT`'s own form (07). No guide passage cited `R1501`. The README's open-details paragraph no longer lists codes for uncoded misuses: no *Checks* line gives a code the spec lacks any more (F37 and F53 have no guide code).

**Checks:** grep of added lines for retired spellings: none. `R1501` appears only in ch 15's retired note and ADR 0048. The spec's exemplar cases annotate none of the changed codes except `R0305`, whose `OR` case still holds. Guide additions are a few plain sentences; `humanizer` was not run on them.

One new finding (ADR 0016), logged in `findings.md`.
