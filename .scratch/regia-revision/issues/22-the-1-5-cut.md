# The Regia 1.5 cut

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21

## Question

With every cause decided for 2.0, and the systems of 1.5 chosen in [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md), what exactly is in 1.5, and how does the spec say so?

Decide:

- The *1.5* line of every ticket, the closed ones included, checked against the systems list.
- That nothing in 1.5 needs something that is later, and what to do where it does.
- What the parts of 2.0 that lean on joining become in 1.5: Givings that stay standing, setups as sugar for `ASSIGN` plus `JOINED`, Phase setups for latecomers.
- The checks and Diagnostic codes that are in 1.5, and a 1.5 Program using a later word: an error, or a warning that says "2.0".
- How the spec marks 1.5: a mark per section of the 2.0 spec, a list of what's left out, or a spec of its own. The same for the Conformance cases and the Jason chapters.

## Resolution

Resolved on 2026-11-17, with the user.

**The *1.5* lines.** All twenty closed tickets have one, and they agree with [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md) and ADR 0025. None of them needs a later part. There is one gap: **spawning**.

- **Spawning.** Joining starts with the game spawning an Agent. Without joining, a spawned Agent would play nothing, and the writer couldn't avoid it. So in 1.5 the game can't spawn an Agent while the run goes on. The Root Director refuses a `regia_join`, and the Trace writes the runtime warning **`T1902`**. Every Agent comes from the starting Instancing, and a kind that only the game would spawn has no Agents. `T1902` is reported by a 1.5 run only, and is retired in 2.0.
- **Setups and "standing".** No new rule. A Role setup or the `CAST` setup is sugar for the initial Phase's entry Plan acting on each starting Agent. A Phase setup is sugar for `ENTERED` with a whole-Role `ASSIGN … UNTIL EXITED`, a `TELL` and an `ASK`. "Standing" matters only when a Phase is entered again. The 2.0 text stays, and the 1.5 sections state the reduced sugar.
- **A later construct in a 1.5 build.** The 1.5 Transpiler parses all of 2.0. For a construct of a later system it reports one error, **`R0109`** (chapter 01), which names the construct and says it is Regia 2.0. The constructs are `FROM GAME`, `FROM ME`, `OR` in `FROM`, `BY` on a Goal's ending, a Goal's ending in a Plot, a quantity after `FROM` or `BY`, `SENT`, and `JOINED`. A construct reported with `R0109` gets no other Diagnostic. The checks about later systems are never emitted in 1.5: `R0507` to `R0512`, `R1801` to `R1806`, `R1905`, `R2012`, `R2013`, `R3805`, `R3806`, `T1801` and `T1802`. `R0109` is retired in 2.0.
- **Marking the spec.** Every chapter ends in a `## Regia 1.5` section, the Jason chapters and 38 included. Chapter 27's `## Regia 1.5` indexes them by what is left out. There is no separate 1.5 spec.
- **Cases.** A new header line: `#! regia: 2.0` marks a case a 1.5 runner skips, and `#! regia: 1.5` marks a case a 2.0 runner skips. A case without the line runs on both. Coverage is judged per version.
- **Command line.** No option picks the version. A build has one version, and `regia --version` prints it. `regia test` runs the cases that fit.

1.5: this ticket decides the cut itself. `R0109`, `T1902` and the `regia:` line are 1.5-only, and are retired in 2.0.

Changed:

- Spec: a `## Regia 1.5` section in chapters 01–20, 26 and 28–38. Chapter 21's section is corrected for spawning, and chapter 23's has the version note. Chapter 01 gets *A word of Regia 2.0 in a 1.5 build* and `R0109`. Chapter 19 gets `T1902`, also listed in chapter 34's table. Chapter 27 gets the `regia:` annotation and the 1.5 index.
- Cases: `18-quota-triggers/percent-over-a-hundred` and `19-cast-changes/joined-in-a-playbook` are marked `regia: 2.0`. New 1.5 exemplars: `01-statements-and-blocks/later-word-in-a-1-5-build` (`R0109`) and `19-cast-changes/spawn-refused-in-1-5` (`T1902`).
- ADR 0025: a pointer to this cut, and two consequences added (spawning refused, `R0109`). Its decision is unchanged, so it isn't superseded.
- Glossary: **Regia 1.5** added, and **Joining** now says the game spawns the Agent and that 1.5 has none.

