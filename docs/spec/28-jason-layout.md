# Jason Build layout

What a Build for the Jason Target looks like as a set of files, how its Infrastructure is shared, where the Infrastructure keeps its state, and how Regia names become Jason names. Decided in the ticket *ASL infrastructure layout* (`.scratch/regia-2/issues/34-asl-infrastructure-layout.md`). It is the first chapter of the full ASL mapping, and the others build on its layout: *Giving and taking Playbooks at runtime*, *Director runtime in ASL*, *Stagings and Subplots runtime in ASL*, *Precedence encoding in ASL*, *Quota counts and cast changes in ASL*, *Trace and logging* and *.jcm generation* (chapter 36, `36-jason-jcm.md`). It builds on chapter 10 (names), 12 (time), 13 (plan selection), 21 (Instancing) and 23 (Targets emit files). It replaces the file layout of primer ch.8. How Playbooks are given and taken away at runtime is chapter 29 (`29-jason-givings.md`); how Directors run is chapter 30 (`30-jason-directors.md`); how Stagings start and end is chapter 31 (`31-jason-stagings.md`); how precedence is enforced is chapter 32 (`32-jason-precedence.md`); how the Cast changes and Quota Triggers are counted is chapter 33 (`33-jason-cast-changes-and-quotas.md`); how the Trace is written is chapter 35 (`35-jason-trace.md`).

## Files

A Build of Entry `<entry>` is written to `build/<entry>/` (chapter 24):

```
build/<entry>/
    <entry>.jcm                        only when Instancing declares Agents (chapter 21)
    asl/regia/agent.asl                Infrastructure, fixed
    asl/regia/director.asl             Infrastructure, fixed
    asl/playbooks/NobleSocializing.asl one per Playbook
    asl/directors/RoyalBanquet.asl     one per Plot
    asl/roles/Guest.asl                one per Role of the Root Plot
    asl/roles/Drunkard__Guest.asl      one per Role set of a kind playing several Roles (chapter 36)
    cast.json                          the starting cast for the game, with the `.jcm` (chapter 36)
    asl/regia/sourcemap.json           ASL locations and Generated names back to the designer's (chapter 35)
    traces/<timestamp>.jsonl           one Trace per run, written at run time (chapter 35)
```

- **Playbook files** hold the Plans of one Playbook and nothing else. Which Playbooks a Role file includes, and the `regia_playbook` beliefs that list them, are in chapter 29. They never include any file.
- **Director files** hold one Plot's Director. Every Staging of that Plot runs the same file (chapter 17). A Director file includes `regia/director.asl`.
- **Role files** exist only for the **Root Plot's Roles**, because only they start Agents (chapter 21). A Role file includes `regia/agent.asl` and every Playbook file the Role can be given in its lifetime, following Subplot Mappings down the Plot tree. A Subplot Role such as `Challenger` gets no file: the Playbooks it brings are included in the Root Plot Role files that map to it. An Agent kind that plays several Roles runs a generated combination file, `roles/<RoleA>__<RoleB>.asl` (chapter 36).
- **File names** are the Regia names exactly as written. Names are unique ignoring case (chapter 10), so this is safe on file systems that ignore case.
- Every generated file starts with a comment naming the Transpiler version and the source file, and saying it is generated.
- Include paths are relative to `asl/`, which the `.jcm` sets as the ASL source path.

## Shared Infrastructure

- The Infrastructure is **fixed ASL text built into the Transpiler**. It is the same for every Program and is written out unchanged into every Build, with a header naming the Transpiler version, so a Build stands on its own. Anything that depends on the Program goes in the generated files instead. This replaces 1.0's copying of infrastructure plans into every file.
- Jason doesn't skip a file that is included twice. So only an **Agent's top-level file** (a Role file, or a Director file) includes the Infrastructure. Playbook files include nothing.
- `regia/agent.asl` holds what every Agent runs: receiving Givings, Signals to Directors, failure and trace plumbing. `regia/director.asl` holds what every Director runs: Phase switching, Staging life cycle, Role records. Their contents are decided by the tickets listed at the top.

## The Java library

Some of the Infrastructure has to be Java. Jason picks among the applicable plans for an event in `Agent.selectOption`, and ASL code can't see the other options, so precedence (chapter 13) can only be enforced there.

- The Java code lives in **`regia-jason`**, a small library released and versioned with the Transpiler. It is never generated.
- The Agents' class **extends VEsNA-Pro's** agent class and follows VEsNA's approach: plans carry annotations, and `selectOption` reads them. Regia adds a ranking annotation. `selectOption` keeps the options with the best rank, hands those to VEsNA's temper selection when they are Suits alternatives or a `TIES` pool, and breaks what remains by Playbook name. The annotation's shape and how ranks compare are decided in chapter 32. A plan annotation can hold only the fixed part of a rank (the Playbook, and the Trigger Block's position in it). The part that depends on who gave the Playbook is runtime state (below).
- Directors run on a separate class, `regia.DirectorAgent`, which extends Jason's `Agent`: Directors have no Temper, and a Subplot Director has no VEsNA body, without which `VesnaAgent` can't start (chapter 30). The ranking code is a helper shared by both classes.
- The `.jcm` points at these classes by default (chapter 21: `ag-class` never has to be written). The Agents' class is `regia.RegiaAgent` (chapter 36).
- `regia-jason` is also the home for any other Java the Jason Target needs, such as a trace writer or internal actions.
- A Build contains ASL files and the `.jcm`, and no Java.

## Infrastructure state

- Everything the Infrastructure knows about an Agent or a Director is held as **beliefs**: which Playbooks it was given, by which Staging and with which rank, which Roles it plays, its Directors, quota counts and Phase. There is no state on the Java side. Jason's mind inspector shows it all, and a Build has no hidden state.
- Each concept has **one Generated name** for its functor. The arguments of each are decided by the ticket that owns the concept.

| Concept | Held by | Functor | Owning ticket |
| --- | --- | --- | --- |
| A Giving of a Playbook | Agent | `regia_given` | *Giving and taking Playbooks at runtime* (chapter 29); rank from chapter 32 |
| A Playbook in the Agent's files | Agent | `regia_playbook` | *Giving and taking Playbooks at runtime* (chapter 29) |
| The Plot a Director runs, its parent and children, an ending | Director | `regia_staging`, `regia_parent`, `regia_child`, `regia_ending` | *Stagings and Subplots runtime in ASL* (chapter 31) |
| The current Phase | Director | `regia_phase` | *Director runtime in ASL* (chapter 30) |
| A standing Giving | Director | `regia_standing` | *Director runtime in ASL* (chapter 30) |
| What a Plot hears from the game | Director | `regia_hears` | *Director runtime in ASL* (chapter 30) |
| A Role's members | Director, and a copy in Agents (chapter 29) | `regia_cast` | *Quota counts and cast changes in ASL* (chapter 33) |
| A Quota Trigger count | Agent or Director | `regia_quota` | *Quota counts and cast changes in ASL* (chapter 33) |
| An Agent kind, for creating joiners | Root Director (initial beliefs of its file) | `regia_kind` | *.jcm generation* (chapter 36) |

Tickets that need a concept missing from this table add a row.

## Names

### Generated names

- A Generated name always **starts with `regia_`** and **separates its parts with `__`**: `regia_if__1`, `regia_given`, `regia_local__nobleSocializing__already_greeted`.
- Designer names can do neither (chapter 10), so a Generated name can't collide with a designer's name, and the parts of a Generated name split one way only.
- **Local Vocabulary** (chapter 10) is emitted as `regia_local__<Playbook or Plot>__<name>`. Two Playbooks with the same local name get two different Jason names.
- Trace entries name the designer's items, never Generated names (chapter 11).

### Regia names in Jason

- A Jason atom must start with a lowercase letter. A Regia name is emitted with **its first letter lowercased**: `NobleSocializing` → `nobleSocializing`, `Guest` → `guest`, `is_drunk` → `is_drunk`. This is one-to-one because names are unique ignoring case (chapter 10).
- A Regia name that is a **Jason reserved word** (`true`, `false`, `not`, `if`, `elif`, `else`, `for`, `while`, `div`, `mod`, …) is renamed quietly to `regia_word__<name>`. Designers never see Jason words, so this is never an error.

### External names

- External names (chapter 10) are emitted **exactly as written**, with no lowercasing or renaming.
- An Action's External name with dots (`engine.security.summon_guards`) is a **Java internal action**: Jason looks for a Java class by that name. One without dots is a **game Action**, compiled to `regia.act(A)`, which sends it to the game through the agent's body and waits for the game's reply (chapter 37).
- A Fact's or Event's External name must be a valid **Jason atom** (a lowercase letter, then letters, digits and `_`), because beliefs and percepts can't contain dots. Anything else is an error for the Jason Target.

## The clock

- The Jason Target measures Durations with the **wall clock**: `WAIT` maps to `.wait` in milliseconds (chapter 12). 2.0 has no setting to choose a clock.
- Cost: Agents keep waiting while the game is paused, and ignore the game's time scale. A game clock (VEsNA sending a generated wake-up Event after some game time) is post-2.0.

## Transpiler checks

**Errors**

- `R2801` A Fact or Event External name that isn't a Jason atom, in a Jason Build.

The names-related checks are in chapter 10 (`R1007`, `R1008`).

## Not decided here

- The contents of `regia/agent.asl` and `regia/director.asl`, and the arguments of each Infrastructure belief: the tickets listed at the top.
- A plain-Jason agent class (no VEsNA-Pro, `TIES` falling back to name order): not in 2.0.
- A game clock: post-2.0.
