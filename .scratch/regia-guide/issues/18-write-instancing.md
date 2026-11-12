# Write: Instancing

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/15 - Instancing.md`.

Covers: Agent kinds and Agent declarations, `COUNT`, starting Propensity values, `#%` Instancing comments, `.regin` files and overriding, Target settings.

Sources: 21.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/15 - Instancing.md`](../../../docs/guide/15%20-%20Instancing.md), about 3,250 words counting snippets, tables and the diagram, over nine sections (an Agent kind, how many start, a kind in several Roles, starting Propensity values, naming the Root Plot, Instancing files, a second build, Instancing comments, Target settings). The Root Plot itself is left to *Plots and Directors*, the draw of `RANDOM` values to *Randomness*, and the `.jcm` to *Translation to ASL*. Not yet read by the user.

Checked by hand against spec chapters 02, 10, 14, 16, 18, 19, 21, 35 and 36.

The showcase Program is unchanged. Instancing comments have no place in it (all Instancing is in the two `.regin` files, and *Syntax* and *Plots and Directors* say so), so the chapter shows them in a throwaway snippet and the gap stays in the README.

Fourteen `#revise`:

- `king PLAYS Host` and `servant PLAYS Servant` say one thing twice: a kind that only gives a Role a number.
- `latecomer` repeats `noble`: a kind can't be built on another.
- Kinds multiply: one per temperament or extra Role, each written in full.
- `Keeping_watch OVER NobleSocializing ON scandal` is needed only because of an `AND` in a `.regin` file, and neither file shows the link.
- What a `SUITS` does on a Propensity with no value is left to the Target.
- A kind gives only Propensity values (the same note as in *Plots and Directors*, from the other side).
- Changing a count means rewriting the whole kind: `test.regin` copies the knight to go from 2 to 1.
- A kind can't be removed by a later file (already in the README).
- Overriding has two grains: a `TARGET` Block line by line, an `AGENT` Block whole.
- Instancing has two homes, comments and files, and the showcase needed one.
- A misspelt Target name is skipped without a warning.
- The one setting the showcase writes is the default, and the seed has no key.
- Target settings follow rules of their own (`JASON` in capitals, undeclared words, a third `=`).
- An Agent's start is written in three places, and the game's part can't be stated in the Program.

Added to the README: three *Spec wording* items (chapter 23 against chapter 21 on who chooses the Target; an unknown Target's group; `COUNT 0` against no `COUNT`) and one *Gaps in the showcase* entry.

Drift seen for the consistency pass: `.regin` snippets are fenced as `regia` in most chapters and as `regin` in *Quotas and Cast Changes*.
