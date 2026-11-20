# The Trace's fields and entries

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05, 20

## Question

Group M of the [inventory](../jason-open-questions.md#m-the-traces-pieces-the-traces-fields-and-entries): the walkthrough's runs state expected lines, and chapters 34 and 35 leave the pieces open. The script step for one Agent is [*Scripting the game for one Agent*](09-scripting-one-agent.md), not this.

Decide:

- `regia.trace`'s fields per kind, and `sourcemap.json`;
- how `by`, `over` and `fits` reach a `plan` entry;
- `giving` entries: writer, granularity, the form for one Agent;
- which Statements and events write entries (setup `LEARN`/`PURSUE`, a Director's Facts, the initial Phase, `SIGNAL`, `T1104`, a waiting Plan and its Goal, `RUN ENDED`);
- the `code` on a failure in turn;
- who numbers a Plot's Stagings for `#<n>` and `ALSO IN`;
- Agent names in Target-neutral chapter 34.

Closes when chapters 34 and 35 are edited.

## Comments

- From [*A Playbook's opening and closing in ASL*](16-opening-and-closing.md): a closing's id is the `seq` of its take step's first `TAKE` entry, and the entries of the Pursuits and `WHEN` Plans it stops are `because:` that entry (`plan … stopped` at `info`; `T2902` retired). A closing Plan's `SIGNAL` to a Director whose Staging has ended writes an `info` entry from `regia.send`, not `T3303`: decide its form with the other `giving` entries.

- From [*Entering and leaving a Phase in ASL*](18-phase-change.md): the `phase` entry is written at `TRANSITION` step 4, after `EXITED` and the taking, and before the new Phase's setups (chapter 30). What its `ON <trigger>` names when the `TRANSITION` is in a `DURING PLOT` Plan, or an `AFTER`, is still open.

- From [*Subplot arguments and endings in ASL*](19-subplot-endings.md): `T3802` is written by the `regia_subplot_endings` dispatcher, which has the Subplot, its `Args`, `How` (`with(O)` or `without`) and the parent's Phase at hand (chapter 31, *`Heard` and `T3802`*). Fix its fields here. Also: does a `staging` entry for an ending say whether it was `BY PARENT` (the walk now carries `By`)?

- From [*Moods and Labels on VEsNA-Pro*](20-moods-on-vesna.md): a `SHIFTS` Label's `mood` entries and a `SUITS` choice's `fits` are both written by `RegiaAgent.selectOption` (chapter 32, step 5), when the plan is chosen and before its first `regia.trace` call. Decide how they relate to the plan's `plan` entry (`because:`, and how `fits` reaches it when that entry is written later by ASL).

- From [*The Target's own code in a Build*](21-target-code.md): a dotted Action's two `action` entries are written by `regia.act`, which runs the Java itself and has no `id` for it (no message is sent). Make sure the `action` fields don't need an `id`: the outcome entry links by `of: <seq>`. Its `reason` on `FAILED` is the exception's message, or `no Java class <name>`.

## Resolution

Decided with the user on 2026-11-19. Chapters 34 and 35 are edited, with the knock-on changes in 11's case (`failed-action-fails-its-goal`), 13, 14, 29, 30, 31, 32, 33, 36, 39 and 40. The game-link map had already turned `director:` script steps into `link` steps. Nothing else in this ticket depended on it.

- **The `plan` entry is written at selection**, by `RegiaAgent.selectOption` (chapter 32's new step 6) and `DirectorAgent.selectOption`, for any chosen option whose label is a designer's Block in the source map. `by`, `over` and `fits` are known there. A `SHIFTS` Label's `mood` entries follow it, `plan:` its `seq`. Generated Bodies lose their `regia.trace(plan, …)` call. **`GIVEN` and `ELSE` are dropped from `by`**: siblings never compete, and the line already shows which one ran. `by` is `SUITS`, `PRECEDENCE`, `NAME` or `DEFAULT`.
- **The failure chain mirrors the drop.** The `failure` kind is only the cause: one per Failure, always coded (`FAILURE T1104 GOAL take_seat: no applicable TO Plan`). Each Pursuit that fails writes `GOAL … FAILED` at `error`, `because:` the cause. A waiting `WHEN` Plan writes `PLAN … FAILED`. A `TO` Plan has no entry apart from its Goal's. `FAILURE <what> because #<seq>` is retired. Cases must list the cause, and the levels that failed in turn may go unlisted.
- **`giving` entries** are written by the Agent, one per Giving received or lost (setup, set aside, restored included): `GIVE Spectating TO noble_1 AS Spectator IN director:HonorDuel#2`. A Giving to one Agent has no ` AS`. A Phase-tied one adds ` UNTIL <phase> EXITED`.
- **`SIGNAL`** is a `message` entry, one per Statement, from `regia.send`: `SIGNAL c TO <director>, …`. A Director whose Staging had ended is marked ` ENDED`, at `info`, instead of `T3303`.
- **Setup `LEARN`/`PURSUE`** are `message` entries (`TELL`, `ASK`) on the Director, with the setup line as `at`. A setup writes no `plan` entry. **A Director writes `fact` entries** like an Agent, its starting game Facts included.
- **A Staging's start** writes `STAGING … STARTED`, then `PHASE -> <initial>` (none for a Plot without Phases), then its starting game Facts, then the setups (`regia_begin` step 1). **`ON <trigger>`** is the Trigger of the Plan that ran the `TRANSITION`, and the entry carries `plan: <seq>`.
- **Endings**: `STAGING … ENDED WITH o`, `… ENDED`, `… ENDED BY PARENT`, written at step 1 of the ending (chapter 31). `T3802` carries `plot`, `args`, `outcome` and the parent's `phase`.
- **Staging numbers and `ALSO IN`** are worked out by the Trace writer from its own entries: the next number for the Plot at a Director's `STARTED`, and `also_in` from the `STARTED`, `ENDED` and `LEFT` entries already written. They are names for the output only, and no agent reads them, so the *Java is plumbing only* rule holds.
- **Agent names** are fixed in Target-neutral chapter 34 (individuals by name, `<kind>_<n>` in Instancing order). Chapter 36 uses them.
- **`RUN ENDED`** is written on `regia.end_story`, or by a shutdown hook as `RUN ENDED (STOPPED)` (`how: stopped`).
- **Fields.** Chapter 34 has the per-kind field table. `regia.trace(Kind, Level, Code, Fields)` takes `""` for no code and `key(Value)` terms. `at` comes from the caller's frame through the source map, and Infrastructure entries have none. Actions link by `of` and have no id.
- **`sourcemap.json`** has three maps: `lines` (ASL line → `.regia` location), `names` (Generated name → designer name, `null` to fold), `plans` (plan label → Block, `at`, ASL variables → Placeholders).
- Fixed along the way: chapter 39's Weight warnings were written with kind `plan`. They are now `warning`.
