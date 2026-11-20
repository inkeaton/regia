# Agent kinds and Instancing files

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

What can a kind give its Agents, and how does one `.regin` file build on another?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- N8 An Agent kind gives Propensity values and nothing else
- N15 A kind is written whole every time
- B15 An unknown Target is skipped without a word
- D16 the Instancing notes (Instancing comments, Target settings)

Decide:

- Starting Facts per kind, and the contradiction between chapters 16 and 21.
- A kind built on another, overriding one line of a kind, removing a kind.
- Whether Instancing comments stay.
- A check for an unknown Target, and the rules of Target settings.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user. The ticket first settled what Instancing is for: **three layers, and a thing is said in the earliest layer that can know it.** The Program says what holds for any cast. Instancing says what holds for one cast in one game setup, fixed before the run. The game says what only comes up while it runs. Per-kind and per-Agent lines follow from that.

- **N8** fixed.
  - A `KIND` and an `AGENT` may hold the setup Statements `ASSIGN`, `LEARN` and `PURSUE`, under chapter 16's rules (Expressions per Agent, no Placeholders, no `ME`). They run after the Root Plot's setups and before its entry Plans: Role setups, then the kind's lines, then the Agent's own.
  - Everything Instancing gives is told and asked by the Root Plot's Director, a `GAME FACT` included, and neither is a warning. One rule, and the Trace shows the source.
  - Individual Agents (`AGENT gawain LIKE knight: LEARN seat(3).`) carry what belongs to one character, such as the seat and the grudges. Their names are Values inside Instancing only (`LEARN grudge(percival)`). A `.regia` file never names a kind or an individual Agent.
  - Chapter 16's "values set per Agent come from Instancing" now says per kind or per Agent, with the same three Statements.
- **N15** fixed.
  - `AGENT` becomes `KIND` for a kind. `CLASS` was proposed and turned down, because it clashes with Jason's agent class.
  - `LIKE` builds a kind (or an individual Agent) on any number of kinds. It takes everything except `COUNT`. `PLAYS` lists and setup lines from the bases are joined. Any other item the bases set differently is an error unless the kind writes it (`R2120`).
  - Overriding goes line by line, as for `TARGET`. The items are `PLAYS`, `LIKE`, `COUNT`, each `AT` line, and the setup lines taken together. `KIND knight: COUNT 1.` goes from two knights to one.
  - `NO KIND` and `NO AGENT` remove a kind or an Agent in a later file. A removed kind can't be spawned but can still be built on.
  - `AGENT <name>` declares one individual Agent: no `COUNT`, in the starting cast, never spawned, and its name is its Agent name. `AGENT king PLAYS Host.` replaces the kind that only existed to give a Role a number. That is how *`king PLAYS Host` says one thing twice* is resolved: by individuals, not by a shortcut.
  - `R2110` and `R2115` count individual Agents.
- **B15** fixed. A `TARGET` group for a Target the Transpiler doesn't know gets a warning (`R2116`). It isn't an error, because a file may configure a Target a newer Transpiler supports.
- **D16** (Instancing comments and Target settings) fixed.
  - Instancing comments are removed. `.regin` files are Instancing's only home. `R2101` is narrowed and `R0202` no longer mentions them.
  - Target names are written in lowercase, as on the command line (`TARGET jason:`).
  - A value outside the set a known key takes gets a warning (`R2113` widened).
  - The `=` is handed on (below).
- **Added**: `SEED <n>.` in Instancing, one item for overriding. A seed given when the run starts beats it.
- **Deliberate limits confirmed**: Instancing never picks at random, and `PLAYS` names only Roles of the Root Plot.

Settled while writing, not asked:

- The setup lines of the bases are joined in `LIKE` order, like their `PLAYS` lists, so a kind built on two kinds with setup lines isn't a conflict.
- Instancing lines run after the initial Phase's setups too, so that all of the Root Plot's setups come first. For a joiner they run after chapter 19's step 2.
- Kind names and Agent names share one namespace (`R2123`). An individual Agent can't be named `<kind>_<digits>` on Jason (`R3603`). On Jason, individual Agents take the first ports, sorted by name, and appear in `cast.json` without a kind.
- A behaviour case's seed is its header's, else the Build's `SEED`, else 1.
- Removed `NO KIND` kinds have no `regia_kind` belief, and a join naming one is `T3301`.
- The conformance case *failed-action-fails-its-goal* became a folder with a `.regin`, because it used an Instancing comment.

Changed:

- Spec:
  - Chapter 21 rewritten: *Who says what*, Instancing files only, line-by-line overriding, `KIND` with `LIKE` and `NO KIND`, individual Agents and Instancing names, setup lines, the seed, lowercase Targets.
  - New codes `R2116` to `R2123`. `R2101`, `R2108`, `R2109`, `R2110`, `R2113` and `R2115` changed.
  - Chapter 02: Instancing comments removed, `R0202` narrowed.
  - Chapter 14: starting values per kind or per Agent.
  - Chapter 15: the `PLAYS` example.
  - Chapter 16: the per-Agent sentence.
  - Chapter 19: only kinds join, and a joiner runs its kind's lines.
  - Chapter 24: no `#%` to edit or highlight.
  - Chapter 33: an unknown or removed kind.
  - Chapter 34: a case's seed falls back to `SEED`.
  - Chapter 35: lowercase `jason`, the run's seed from `SEED`, individual names.
  - Chapter 36: individual Agents' names, ports, `.jcm` entries and `cast.json`, value sets for `strategy` and `trace_console`, new `R3603`.
  - Cases: `21-instancing/plays-a-role-the-root-plot-lacks` uses `KIND`, and `11-failure/failed-action-fails-its-goal` is now a folder.
- ADR: new ADR 0035 *Instancing is the cast of one game setup*.
- Glossary: *Instancing*, *Agent kind*, *Instancing file* and *Seed* revised; *Individual Agent* added; *Instancing comment* and *Agent declaration* removed.

Handed on:

- To [*Words that do several jobs, and syntax nobody used*](20-words-and-syntax.md): `KIND`, `AGENT`, `LIKE`, `NO`, `SEED` and the `=` of a Target setting.
- To [*The command line, Programs and Diagnostics*](16-command-line-and-diagnostics.md): the option that gives a run its seed.
- To the Jason chapters (fog on the map): how the Root Director's file runs the setup lines of kinds and Agents, at start and for a joiner, and the `regia_kind` belief carrying a kind's setup lines.
- To the guide (fog on the map): *Instancing* and the showcase's `.regin` files are rewritten with `KIND`, `LIKE`, individual Agents (the king, the seats), line-by-line overriding in `test.regin` and `NO KIND hothead`. The `#revise` notes on Instancing comments and the unknown Target are dropped.
- New Conformance cases for the new codes (fog on the map).

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- N8, N15, B15, D16 (the Instancing part) and `SEED`: in, all of them, and none of it needs a later part.
- A spawned Agent running its kind's setup lines: later, with joining.
