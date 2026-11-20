# The command line, Programs and Diagnostics

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

What can the `regia` command do, what is one Program, and how is a Diagnostic named and answered?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N9 The command line is two words
- N10 Only a whole story can be checked
- N11 A warning can't be answered
- B2 A Target's checks run only in the emit
- B11 Several Entry files: one Program or two
- B12 The Build folder
- D20 Diagnostic codes follow the spec's table of contents

Decide:

- The list of commands and options: running a Build, a behaviour case of our own, the conflict report, the seed, the Target, the console. A seed given when a run starts beats the Build's `SEED`, and with neither the run picks one and the Trace records it (spec 21, from [*Agent kinds and Instancing files*](15-instancing.md)). The conflict report is where the order for a Trigger is read whole (L6 kept, in [*Which Plan runs*](12-which-plan-runs.md)); it now also marks full stops with the candidates they make unreachable, and defaults left out (`R1312`).
- Checking a Playbook or a Subplot alone.
- The command that prints the Interface of a Playbook or a Plot (spec 38, from [*What passes between a Playbook and a Plot*](01-playbook-plot-interface.md)).
- Marking a warning as seen.
- Target checks in `regia check`.
- One Entry file or several; the name and the content of the Build folder.
- Codes and the note severity.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user.

- **N9** fixed. Five commands: `regia check <entry>…`, `regia build <entry>`, `regia run <entry>` (build, then start the MAS with the `regia-jason` the CLI carries, so no class path), `regia test <case or folder>…` (our own cases in the Conformance format, matched in Rust), and `regia explain <entry> precedence | interface <Playbook or Plot>`. The options are `--target` (default `jason`, or `none`), `--seed` and `--console` on `run`, `--deny-warnings`, `--all-warnings` and `-q`. The `trace_console` Target setting is removed and `R3501` retired: how much the console shows changes nothing in the run, so it isn't Instancing (ticket 15's layers).
- **N10** fixed, and it reshaped the Root Plot. The Root Plot is **named** with `ROOT` in Instancing and never inferred. Only a `.regin` Entry can be built or run. A `.regia` Entry has no Root Plot and is checked for what it says, with the Root-only checks skipped. `R2104` narrowed. ADR 0036.
- **N11** fixed. `?_name` is a named "don't care": independent, never usable in the Body, and never warned (`R0306` widened). `#@allow: <code>, …` on a declaration (or the file) accepts the warnings whose span lies inside it. Allowing an error code is `R0204`, and an allow that silences nothing is the warning `R0205`. Allowed warnings come back with `--all-warnings`, and appear faded in the Visual Editor.
- **B2** fixed. A Target has a check step separate from its emit, run in validate, so `check` and `build` give the same Diagnostics (`R1310`, `R1408`, `R1410`, `R36xx`).
- **B11** fixed. A Program has exactly one Entry file. Builds are layered by `IMPORT`, and `check a b` checks two Programs. ADR 0036.
- **B12** fixed. The Build folder is `build/<Entry path relative to the current directory or Project, without extension>/`. A build replaces everything in it except `traces/`, which nothing clears. There is no project marker file (`regia.toml` turned down).
- **D20**:
  - Code shape kept for 2.0. Codes are essential and stable, and the severity is printed beside them, never read from them. **Deferred**: a more readable, memorable shape, which the user wants after 2.0 (recorded in chapter 27).
  - The note severity: fixed. Two severities only. `R1311` becomes a warning, and `R1312` is retired into a line of the conflict report.

Settled while writing, not asked:

- The run's seed and the console level reach `regia-jason` as the system properties `regia.seed` and `regia.trace_console`.
- `explain` works on a `.regia` Entry with what can be known without a Root Plot. The Workspace gains `report(entry, kind)`.
- A behaviour case is always a folder with a `.regin` naming its `ROOT`. In a folder case without a `.regin`, each `.regia` is its own Program. Cases are matched as with `--all-warnings`.
- `R0205` can't itself be allowed. The exit status is 1 on an error, a failed case, or a warning under `--deny-warnings`.
- *Allow here* is a Visual Editor quick fix on every warning.

Changed:

- Spec:
  - Chapter 23: one Entry per Program, two severities, allowed warnings, the Target's check and emit, new sections *The command line* and *The Build folder*, the crate table, `build(entry)` for `.regin` only, `report(entry, kind)`, and a 1.5 section.
  - Chapter 10: one Entry file.
  - Chapter 21: `ROOT` required and inference removed, `.regia` Entries check-only, *With no cast*, `R2104` narrowed, `--seed` and `--target`.
  - Chapter 02: the `allow` key, with `R0204` and `R0205`.
  - Chapter 03: `?_name`, and `R0306` widened.
  - Chapter 13: `R1311` is a warning, `R1312` retired, the conflict report is `regia explain … precedence` and shows a default left out.
  - Chapter 24: Build menu `.regin` only, Target as a project setting, the Build folder keeps `traces/`, allowed warnings faded, *Allow here*.
  - Chapter 27: two severities, the deferred code shape, behaviour cases as folders, `regia test`, matching with `--all-warnings`.
  - Chapter 28: the Build folder path.
  - Chapter 32: `R1311` and the report line.
  - Chapter 35: *The console* becomes a run option, *Starting a run* is new, and `R3501` is retired.
  - Chapter 36: `trace_console` removed from the `.jcm`, `regia_kind` and the known keys.
  - Chapter 38: the `explain` command.
  - Cases: `ROOT` added to `11-failure/failed-action-fails-its-goal/game.regin` and `21-instancing/plays-a-role-the-root-plot-lacks/game.regin`.
- ADR: new ADR 0036 *A Build is one `.regin` Entry that names its Root Plot*.
- Glossary: *Root Plot*, *Entry file*, *Program*, *Build*, *Diagnostic* and *Instancing* revised. *Build folder*, *Allowed warning* and *Conflict report* added.

Handed on:

- To [*Words that do several jobs, and syntax nobody used*](20-words-and-syntax.md): the spellings `#@allow` and `?_name`.
- To [*The Visual Editor*](18-visual-editor.md): which Program a `.regia` reached by several `.regin` files takes its markers from.
- To the guide (fog on the map): *The Transpiler* is rewritten for the five commands, `ROOT` in every `.regin`, `?_who` on the laughing Plan, `#@allow` in place of the two silencing `PRECEDENCE` lines, and the Build folder. The showcase's `.regin` files gain `ROOT`.
- New Conformance cases for `R0204`, `R0205`, `?_name` and the narrowed `R2104` (fog on the map).
- To the Jason chapters (fog on the map): `regia.seed` and `regia.trace_console` read by `regia-jason`.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N9, N10, N11, B2, B11, B12 and D20: in, all of them, and none of it needs a later part. The more readable code shape is later than 2.0 itself.
