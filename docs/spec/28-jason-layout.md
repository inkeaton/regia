# Jason Build layout

What a Build for the Jason Target looks like as a set of files, how its Infrastructure is shared, where the Infrastructure keeps its state, and how Regia names become Jason names. Decided in the ticket *ASL infrastructure layout* (`.scratch/regia-2/issues/34-asl-infrastructure-layout.md`). It is the first chapter of the full ASL mapping, and the others build on its layout: *Giving and taking Playbooks at runtime*, *Director runtime in ASL*, *Stagings and Subplots runtime in ASL*, *Precedence encoding in ASL*, *Quota counts and cast changes in ASL*, *Trace and logging*, *.jcm generation* (chapter 36, `36-jason-jcm.md`) and *A Plan's Statements in ASL* (chapter 39, `39-jason-plan-bodies.md`). It builds on chapter 10 (names), 12 (time), 13 (plan selection), 21 (Instancing) and 23 (Targets emit files). It replaces the file layout of primer ch.8. How Playbooks are given and taken away at runtime is chapter 29 (`29-jason-givings.md`); how Directors run is chapter 30 (`30-jason-directors.md`); how Stagings start and end is chapter 31 (`31-jason-stagings.md`); how precedence is enforced is chapter 32 (`32-jason-precedence.md`); how the Cast changes and Quota Triggers are counted is chapter 33 (`33-jason-cast-changes-and-quotas.md`); how the Trace is written is chapter 35 (`35-jason-trace.md`); how a Plan's Contexts and Statements are written is chapter 39 (`39-jason-plan-bodies.md`).

## Files

A Build of Entry `<entry>` is written to its Build folder, `build/<Entry path>/` (chapter 23), where `<entry>` is the Entry's name without its extension:

```
build/<Entry path>/
    <entry>.jcm                        only when Instancing declares Agents (chapter 21)
    asl/regia/agent.asl                Infrastructure, fixed
    asl/regia/director.asl             Infrastructure, fixed
    asl/playbooks/NobleSocializing.asl one per Playbook
    asl/directors/RoyalBanquet.asl     one per Plot
    asl/roles/Guest.asl                one per Role of the Root Plot (a .regia Entry: below)
    asl/roles/Guard__Guest.asl         one per Role set of a kind playing several Roles (chapter 36)
    asl/unheard.asl                    the Agents' catch-alls for told Cues no Plan takes (chapter 39)
    asl/goals.asl                      the generated `-!g` plan of every Goal (chapter 40)
    cast.json                          the starting cast for the game, with the `.jcm` (chapter 36)
    asl/regia/sourcemap.json           ASL locations and Generated names back to the designer's (chapter 35)
    traces/<timestamp>.jsonl           one Trace per run, written at run time (chapter 35)
```

- **Playbook files** hold the Plans of one Playbook and nothing else. Which Playbooks a Role file includes, and the `regia_playbook` beliefs that list them, are in chapter 29. They never include any file.
- **Director files** hold one Plot's Director. Every Staging of that Plot runs the same file (chapter 17). A Director file includes `regia/director.asl`.
- **Role files** exist only for the **Root Plot's Roles**, because only they start Agents (chapter 21; a `.regia` Entry's Build is below). A Role file includes `regia/agent.asl` and every Playbook file the Role can be given in its lifetime, following Subplot Mappings down the Plot tree. A Subplot Role such as `Challenger` gets no file: the Playbooks it brings are included in the Root Plot Role files that map to it. An Agent kind that plays several Roles runs a generated combination file, `roles/<RoleA>__<RoleB>.asl` (chapter 36).
- **`unheard.asl`** is generated, one per Build, and every Role file (or combination file) includes it once. It depends on the Program, since it lists every Cue some `TELL` sends, so it isn't Infrastructure. **`goals.asl`** is the same kind of file, holding one unguarded `-!g` plan for every Goal of the Program (chapter 40).
- **File names** are the Regia names exactly as written. Names are unique ignoring case (chapter 10), so this is safe on file systems that ignore case.
- Every generated file starts with a comment naming the Transpiler version and the source file, and saying it is generated.
- Include paths are relative to `asl/`, which the `.jcm` sets as the ASL source path.

### A Build of a `.regia` Entry

A `.regia` Entry's Build has no Root Plot and no cast (chapter 21, ADR 0049). It holds the same files, except:

- There is no `.jcm` and no `cast.json`.
- **Every Role of every Plot gets a Role file**, `roles/<Plot>__<Role>.asl` (`roles/HonorDuel__Challenger.asl`), since any Plot may be the one a hand-written project starts. It includes what that Role can be given if its Plot is the top one: chapter 29's rules, read with that Plot in the Root Plot's place. There are no combination files: an Agent that plays several Roles needs a top-level file written by hand, in the form chapter 36 gives.
- **No Director file is the Root's.** None holds `regia_rank_prefix`, `regia_start_cast`, `regia_kind`, `!regia_root_start` or plans for the setup lines of kinds. Every one holds the do-nothing catch-all of `regia_instance_setup` (chapter 30). A hand-written `.jcm` makes one Director the Root by giving it the beliefs `regia_rank_prefix([])` (chapter 32) and `regia_start_cast([…])` (chapter 33) and the goal `regia_root_start`, and by starting the game link as chapter 36 shows. Each entry's `Source` there is `agent(<Agent>)`.

Playbook files are written exactly as in a Build with a Root Plot.

**A Program with no Plot**, such as `regia build courtesy.regia`, gets no Role file at all. Its Build holds the Playbook files, the Infrastructure, `unheard.asl`, `goals.asl` and the source map. What a Role file would carry (the includes, the `regia_playbook` beliefs of chapter 29 and the `regia_game` beliefs of *External names*) is written by hand in the project's top-level file, in the form chapter 36 gives.

## Shared Infrastructure

- The Infrastructure is **fixed ASL text built into the Transpiler**. It is the same for every Program and is written out unchanged into every Build, with a header naming the Transpiler version, so a Build stands on its own. Anything that depends on the Program goes in the generated files instead. This replaces 1.0's copying of infrastructure plans into every file.
- Jason doesn't skip a file that is included twice. So only an **Agent's top-level file** (a Role file, or a Director file) includes the Infrastructure. Playbook files include nothing.
- `regia/agent.asl` holds what every Agent runs: receiving Givings, Signals to Directors, failure and trace plumbing. `regia/director.asl` holds what every Director runs: Phase switching, Staging life cycle, Role records. Their contents are decided by the tickets listed at the top.

### Generated ASL is readable

A generated plan reads like the designer's Plan. Its context is the Givings guard, the Sender test and the designer's Context, in that order, each a named rule or the designer's own formula. Each Statement is one body step, or a test goal and the one action it feeds (`?regia_audience(…); regia.send(…)`). Mechanics that recur from plan to plan are named Infrastructure, kept in the shared files, not written out in every plan. This was 1.0's idea (its `!signal_directors`), and 2.0 keeps the named part out of the generated files.

**Jason first** (ADR 0050). Generated and Infrastructure ASL use Jason's language and its stdlib (`.send`, `.setof`, `.intend`, `.random`, `.create_agent`, `for`, `if`). A Regia element that compiles to more than one step or conjunct is named by an ASL mechanism first. A `regia.*` internal action exists only when ASL can't do the job, for one of four reasons:

1. **It leaves the agent with semantics the stdlib lacks**: the game link, a VEsNA body, the Trace file, the Java class of a dotted Action, and a send that never fails its sender (`regia.send`: Jason's `.send` fails the plan on a receiver that has left).
2. **It needs the run's clock**, which stops while the game is paused (`regia.wait`).
3. **It reshapes intentions beyond the stdlib**: removing frames or whole intentions with their endings and their waiting `DO`s, or quietly (`regia.drop`, `regia.stop_playbook`, `regia.stop_phase`, `regia.end_body`, `regia.pass_failure`).
4. **It hooks the reasoning cycle**: `selectOption`, `brf`, `socAcc` and the failure hook, which are overrides in the agent class, never calls in ASL.

Each `regia.*` action the Jason chapters name states its reason where it is defined. The Jason facts behind these choices are in the research note of the ticket *Readable generated ASL* (`.scratch/transpiler/research/13-jason-native-facts.md`).

Each named mechanic takes one of three forms:

| Form | When | Examples |
| --- | --- | --- |
| A **rule** in `agent.asl` or `director.asl` | a test in a context, or a collection a step reads | `regia_is_given`, `regia_from_director`, `regia_plays` (chapter 29), `regia_audience` (chapter 39) |
| An **Infrastructure plan** | several steps, or steps that wait, fail or write the Trace | `regia_reach`, `regia_endings` (chapter 40), `regia_choose`, `regia_update` (chapter 39), `regia_close` (chapter 29) |
| An **internal action** of `regia-jason` | only for one of the four reasons above | `regia.act`, `regia.send`, `regia.trace`, `regia.wait` |

A rule costs nothing at run time. An Infrastructure plan is a subgoal: it takes at least one more reasoning cycle, goes through `selectOption`, and adds a frame to the intention, which matters to what reads the intention (chapter 40). It hands its bindings back to the step that posted it, so `!regia_choose(Ws, N)` binds `N`. A rule never writes the Trace, since backtracking could run it twice. An internal action is plumbing: game and Regia information stays in the game and in the Agents' beliefs, never in its Java state.

Plan labels stay `regia_plan__<owner>__<n>` (*Generated names*, below): the rank annotation right after the label already names the plan's Item (chapter 32).

The rules and Infrastructure plans each chapter adds are listed in its *`regia-jason` additions* or *Infrastructure* section.

## The Java library

Some of the Infrastructure has to be Java. Jason picks among the applicable plans for an event in `Agent.selectOption`, and ASL code can't see the other options, so precedence (chapter 13) can only be enforced there.

- The Java code lives in **`regia-jason`**, a small library released and versioned with the Transpiler. It is never generated.
- The Agents' class **extends VEsNA-Pro's** agent class and follows VEsNA's approach: plans carry annotations, and `selectOption` reads them. Regia adds a ranking annotation. `selectOption` keeps the options with the best rank, hands those to VEsNA's temper selection when they are Suits alternatives or a `TIES` pool, and breaks what remains by Playbook name. The annotation's shape and how ranks compare are decided in chapter 32. A plan annotation can hold only the fixed part of a rank (the Playbook, and the Trigger Block's position in it). The part that depends on who gave the Playbook is runtime state (below).
- **Temper only chooses among a Trigger's alternatives.** `regia.RegiaAgent.selectOption` also applies the chosen plan's `effects` (a `SHIFTS` Label), once, when it is chosen. `regia.RegiaAgent.selectIntention` overrides VEsNA's with Jason's default round-robin, so Moods never decide which running intention steps next, and VEsNA never applies `effects` itself (chapter 14, *ASL mapping notes*).
- **Platform versions.** Regia runs on **JaCaMo 1.3.1, so Jason 3.3.2** (CArtAgO 3.1), on JDK 21 or later. VEsNA-Pro itself pins JaCaMo 1.2 (Jason 3.2.1), and it runs unchanged on 1.3.1. Moving it, along with the small `Temper` additions Regia needs, is collected in *Changes to VEsNA-Pro for Regia* (`.scratch/implementation/vesna-pro-for-regia.md`). Decided in the ticket *Moods and Labels on VEsNA-Pro* (`.scratch/showcase-1-5/issues/20-moods-on-vesna.md`).
- Directors run on a separate class, `regia.DirectorAgent`, which extends Jason's `Agent`: Directors have no Temper, and no Director has a VEsNA body, without which `VesnaAgent` can't start (chapter 30). The ranking code is a helper shared by both classes.
- The **game link** is `regia.GameLink`, a class of `regia-jason` (below).
- The `.jcm` points at these classes by default (chapter 21: `ag-class` never has to be written). The Agents' class is `regia.RegiaAgent` (chapter 36).
- `regia-jason` is also the home for any other Java the Jason Target needs, such as a trace writer or internal actions.
- A Build contains ASL files and the `.jcm`, and no Java.
- **The project's own Java** (the classes of dotted Actions, chapter 10) is built by the writer, with any tool, into jars in the Project's **`lib/`** folder, beside `build/` in the current directory (chapter 23). `regia run` and `RunCase` put every `lib/*.jar` on the class path after `regia-jason` (chapter 35), so the writer still never writes a class path. Decided in the ticket *The Target's own code in a Build* (`.scratch/showcase-1-5/issues/21-target-code.md`).
- Rejected: a `java/` source folder that the CLI compiles (the CLI would need `javac` and report compile errors, and a Build would hold Java); a `TARGET jason` key naming a class path.

## The game link

Directors reach the game through **one shared game link** for the whole run. Each Director **attaches** to it, hears the game for itself and sends its own Actions; no Director passes a game message on, or performs an Action, for another Staging. The game stays unaware of Stagings. "Body" stays the word for an Agent's own VEsNA connection, which is unchanged.

- Program-wide messages: `regia_join` goes to the Root Director, `regia_leave` to every attached Director, and the link itself kills a leaver and stops and starts the clock (chapters 33 and 37).

Its shape was decided in the ticket *The game link's shape* (`.scratch/director-game-link/issues/02-game-link-shape.md`), with ADR 0040.

- **What it is.** `regia.GameLink` wraps **one VEsNA `WsClient`**. It reads each message the game sends, sorts it out to the attached Directors that should have it, and delivers it into each one's mailbox with `LocalAgArch.receiveMsg`, so it arrives in order with the Director's other messages and wakes it. A Director sends to the game by calling the link directly. `WsClient` reads on one thread, in arrival order, and its `send` is thread-safe.
- **Where it lives.** It is a JaCaMo **platform**, one `.jcm` line (chapter 36):

  ```
  platform: regia.GameLink("localhost", "9080")
  ```

  JaCaMo builds every platform and calls its `init` before it creates any agent. The link connects to `address`:`base_port` in `init`, waiting a bounded time for the connection, so no Director starts, attaches or sends before the link is up. It lives as long as the MAS, not as long as any Director: it outlives the Root (chapter 31), and it closes in the platform's `stop`. Directors reach it through a static accessor, since a run has one.
- **Its name in the envelope** is **`regia_game_link`**. The game writes it as `receiver` on every message it sends the link. The link writes it as `sender` on every message it sends the game, a Director's Actions and `regia_story_ended` included. A Director's name never reaches the game. The link doesn't route on `receiver`: it routes on the message's `type` and, for Facts and Cues, the item's name. The Trace still records which Director sent what.
- **What it holds** is plumbing only (*Infrastructure state*, below): the connection, which Directors are attached, what each hears and whether its state reply has gone through, the state requests in flight, the Actions in flight, and the clock. It keeps **no game information**: a Fact the game reported lives in the game and in the beliefs of the Directors that heard it, never in the link. When the link needs a Regia-shaped answer, it reads it from Jason at that moment instead of keeping it: whether a leaver is an Agent of the Program (`T3302`) is asked of the runtime, and whether the Root Staging has ended (`T3304`) is whether a Root is still attached. The Root attaches *as* the Root, which is all that sets it apart.
- **A link that fails.** If the connection never opens, or closes mid-run, **the run goes on**: Directors stay attached and keep running their Plans, Signals, `WAIT`s and Staging tree, and simply hear nothing more from the game. Every Director's game Action fails at once as if refused, with the reason `no game link` (chapter 37). A paused clock is started again, with a `CLOCK RESUMED` entry, since no `regia_resume` can come any more. The Trace gets `T2802` or `T2803`. There is no reconnecting in 2.0, and the link never kills a Director (VEsNA's own handler kills its agent on an error).
- **Rejected:** a **Jason `Environment`**. JaCaMo 1.2 never creates one and sends every action to CArtAgO (chapter 37), and an `Environment`'s percepts are beliefs, so it can't carry a Cue. **A gateway Root Director**, which forwarded percepts down the Staging tree and relayed Actions: it ran ASL on behalf of other Stagings. **A body per Director**: the game would have to learn about Stagings.
- **Attaching and hearing.** A Director attaches when it gets its start, registering its name, what its own Plot hears and whether it is the Root. The link asks the game for that Director's starting state (`regia_state`, chapter 37) and delivers it nothing until the reply has gone through. An ending Director stops hearing Facts and Cues at the first step of its walk and detaches when its agent stops. Decided in the ticket *A Director hearing the game for itself* (`.scratch/director-game-link/issues/03-hearing-the-game.md`), in chapter 30, *Hearing the game*.
- **Acting.** Every Director sends its own Actions through the link. Their `id`s come from the link's one counter, shared with `regia_state`. Replies are routed by `id` into the requesting Director's mailbox. The link calls off a detaching Director's waiting Actions and fails every in-flight Action when it is lost. Decided in the ticket *A Director doing its own Actions* (`.scratch/director-game-link/issues/04-doing-its-own-actions.md`), in chapter 37, *Custom Actions in a Director*.

## Infrastructure state

- Everything the Infrastructure knows about an Agent or a Director is held as **beliefs**: which Playbooks it was given, by which Staging and with which rank, which Roles it plays, its Directors, quota counts and Phase. Jason's mind inspector shows it all, and a Build has no hidden state.
- **Java holds only plumbing**: the game link's connection and routing, the Actions in flight, the run's clock, and the intentions suspended in `regia.wait` and `regia.act`. Nothing a Regia program could read or act on (Facts, casts, Phases, Givings) is kept in Java, and game information lives in the game or in agents' beliefs, never in Java.
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

- A Generated name always **starts with `regia_`** and **separates its parts with `__`**: `regia_when__ready`, `regia_given`, `regia_local__nobleSocializing__already_greeted`.
- Designer names can do neither (chapter 10), so a Generated name can't collide with a designer's name, and the parts of a Generated name split one way only.
- **Local Vocabulary** (chapter 10) is emitted as `regia_local__<Playbook or Plot>__<name>`. Two Playbooks with the same local name get two different Jason names.
- A **plan label** is `regia_plan__<owner>__<n>`: the Jason name of the Playbook or Plot holding the Block, and its number among that owner's labelled plans, from 1 in source order (`regia_plan__courtesy__1`, `regia_plan__royalBanquet__4`). Labels must be unique within an Agent, which includes many Playbooks. Numbering per owner keeps them unique, and an edit to one file never renumbers another's plans.
- A **generated variable** is a Generated name with its first letter uppercased (`Regia_total`, `Regia_each__1`), and a Placeholder becomes a variable with its first letter uppercased (`?speaker` → `Speaker`): chapter 39.
- Trace entries name the designer's items, never Generated names (chapter 11).

### Regia names in Jason

- A Jason atom must start with a lowercase letter. A Regia name is emitted with **its first letter lowercased**: `NobleSocializing` → `nobleSocializing`, `Guest` → `guest`, `is_drunk` → `is_drunk`. This is one-to-one because names are unique ignoring case (chapter 10).
- A Regia name that is a **Jason reserved word** (`true`, `false`, `not`, `if`, `elif`, `else`, `for`, `while`, `div`, `mod`, …) is renamed quietly to `regia_word__<name>`. Designers never see Jason words, so this is never an error.

### External names

Revised in the ticket *The Vocabulary and the game* (`.scratch/regia-revision/issues/07-vocabulary-and-the-game.md`), with ADR 0026.

- **A game item's External name never appears in ASL.** Its beliefs and events always use the Regia name. Every Agent's and Director's files carry one initial belief per game item they use, `regia_game(fact, "world.time.is_night", night).` or `regia_game(cue, "engine.combat.hit", hit_by).`, and `regia-jason` translates the `name` of each `regia_cue` and `regia_fact` through them (chapter 30). So an External name may hold dots or any other character.
- A game message to an Agent whose name has no `regia_game` entry is dropped with a Trace warning (`T2801`): it is either not a game item, or one this Agent never uses. On the game link, a message no attached Director hears is dropped with no entry (chapter 30).
- An Action's External name **with dots** (`engine.security.summon_guards`) is a **Java internal action**, the Jason form of the Target's own code (chapter 10). It is compiled to `regia.act(N, A)` like a game Action, with `N` the External name exactly as written, and `regia.act` runs the Java class of that name instead of sending anything (chapter 37).
- One **without dots** is a **game Action**, compiled to `regia.act(N, A)`, which sends it to the game through the agent's body and waits for the game's reply (chapter 37). `A` uses the Regia name; `N`, the External name, is a string that travels in the message.

## The clock

- The Jason Target measures Durations with the **wall clock, stopped while the game is paused**: `WAIT` maps to `regia.wait` in milliseconds (chapter 12), and the game's `regia_pause` and `regia_resume` stop and start the run's clock (chapter 37). 2.0 has no setting to choose a clock.
- Cost: Durations ignore the game's time scale. A clock that follows it (VEsNA sending a generated wake-up Cue after some game time) is post-2.0.

## Transpiler checks

None of its own. `R2801` (a Fact or Cue External name that isn't a Jason atom) is no longer given: External names never reach ASL as beliefs.

The names-related checks are in chapter 10 (`R1007`, `R1008`).

## Trace entries

**Errors**

- `T2802` The game link couldn't connect to the game at start. The entry names the address and port. The run starts anyway (*The game link*).
- `T2803` The game link's connection was lost mid-run. The entry names the address and port. The run goes on.

**Warnings**

- `T2801` A `regia_cue` or `regia_fact` whose name matches no `regia_game` entry of the receiving Agent. The entry names the message's name and the receiver. Nothing else happens. A Director never writes it: the game link delivers a Director only what its `regia_hears` lists, and drops a message no attached Director hears with no entry (chapter 30).

## Regia 1.5

In 1.5 (ADR 0025), except the `regia_quota` belief, which is later with Quota Triggers. `regia_kind` is kept for what it carries at start (chapter 36), and creating joiners from it is later.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- The contents of `regia/agent.asl` and `regia/director.asl`, and the arguments of each Infrastructure belief: the tickets listed at the top.
- A plain-Jason agent class (no VEsNA-Pro, `TIES` falling back to name order): not in 2.0.
- A game clock: post-2.0.
