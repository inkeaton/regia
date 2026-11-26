# Instancing

How a Program becomes a running cast: which Plot is the Root Plot, which Agent kinds and individual Agents exist and how many start, what they start with, the seed, and settings for a Target. Decided in the ticket *Instancing comments* (`.scratch/regia-2/issues/22-instancing-comments.md`) and revised in *Agent kinds and Instancing files* (`.scratch/regia-revision/issues/15-instancing.md`, ADR 0035). It builds on chapters 02, 10, 13, 14, 15, 16, 17 and 19.

Instancing sits at a different level from the rest of the language. Playbooks and Plots describe behaviour for Roles. Instancing says who actually plays them in one build. It is **optional**.

## Who says what

Three layers can say something about an Agent:

| Layer | Written in | Says | Example |
|---|---|---|---|
| **Program** | `.regia` files | what holds for any cast of the story | every Guest is told `invited`, gets `Courtesy`, rolls a purse (chapter 16) |
| **Instancing** | `.regin` files | what holds for one cast, in one game setup, fixed before the run starts | six nobles start; `gawain` sits in seat 3 and holds a grudge against `percival` |
| **Game** | runtime | what only comes up during the run | a latecomer is spawned, and the game seats them where there is room (`GAME FACT`, `GAME CUE`, chapter 10) |

**A thing is said in the earliest layer that can know it.** What holds for every cast is written in the Program, never in Instancing. What changes between two builds of one story, but is known before the run, is written in Instancing. Only what comes up while the game runs is left to the game. A Program never names a particular Agent or kind (ADR 0035).

The same Fact may be Instancing's in one game setup and the game's in another: a seat fixed by the level is written in Instancing, a seat the game hands out is told by the game. Neither is an error.

## Instancing files

Instancing is written only in **Instancing files**, `.regin`:

```regia
# test.regin
IMPORT "banquet.regin"

KIND noble:
    COUNT 2

SEED 42

TARGET jason:
    strategy random
```

- A `.regin` holds only `IMPORT`s and Instancing: no Vocabulary, Playbooks or Plots.
- A `.regin` may import `.regia` files and other `.regin` files. Importing another `.regin` layers builds: `test.regin` imports `banquet.regin` and changes only what differs.
- A `.regia` file importing a `.regin` is an error. Design files never depend on a build.
- `.regin` files are usually Entry files (chapter 10), but anything they reach is part of the Program as usual. Only a `.regin` Entry can be run, and only its Build has a cast.

Several builds of one story (a 2-guest test, a 50-guest release, a build for each Target) are several small `.regin` files importing the same `.regia` files. Instancing has no other home: the Instancing comments of earlier drafts (`#%`) are gone (chapter 02), so a Plot file is never built into a cast by itself (a `.regia` Entry builds Target code only, below).

## Overriding

**The importer overrides what it imports.** A setting in a file replaces the same setting in any file it reaches through its imports, directly or not.

- **The items are single lines.** They are:
  - the `ROOT` Statement and the `SEED` Statement;
  - each Target setting (`TARGET jason: strategy`);
  - for each kind and each individual Agent, by name: whether it exists (a declaration or a `NO`), its `PLAYS` list, its `LIKE` list, its `COUNT` (kinds only), each `<propensity> AT` line, and its **setup lines taken together** (below).
- A redeclaration changes only the items it writes and keeps the rest. `KIND knight: COUNT 1` in `test.regin` changes the number of knights and keeps their Roles and values.
- Setup lines can't be told apart line by line, so a redeclaration that writes any setup line replaces all of the kind's (or the Agent's) setup lines.
- **Siblings that disagree are an error.** If two files set the same item differently and neither reaches the other, some file reaching both must set it, or the Transpiler reports both files. Import order never decides (chapter 10).
- Two identical settings never conflict.

## With no cast

In a `.regin`, a cast is optional and the `ROOT` isn't. A `.regin` that only names the Root Plot, sets the seed or gives Target settings produces Target code only (for Jason: the ASL files, no `.jcm`). The instancing output (the `.jcm` for Jason) is produced as soon as at least one kind or individual Agent is declared.

## The Root Plot

A Program has **exactly one Root Plot**. Every other Plot is a Subplot below it, reached only through `START SUBPLOT` (chapter 17). Instancing never starts a Plot. Stories that run side by side are Subplots started by the Root Plot (usually from `DURING PLOT: WHEN ENTERED:`) and ordered by its `PRECEDENCE` (chapter 13).

- The Root Plot is **named**, never inferred: `ROOT RoyalBanquet`. Which story a game setup runs is a fact about that setup, so it is said in Instancing (ADR 0036).
- A `.regin` Entry must reach a `ROOT`, **even with no other Instancing**. Its Role files and the Root Director depend on the Root Plot.
- Naming a Plot that is started as a Subplot somewhere is an error, since its Staging would have no clear parent.
- A `.regia` Entry has no Root Plot (*A `.regia` Entry*, below): the checks that need a Root Plot (this chapter's, and chapter 13's ranking across the hierarchy) don't run, and everything else does. So a Playbook file or a Subplot's file is checked for what it says, never as if it were the whole story.
- Plots that the Root Plot never reaches are compiled like the rest but never run. The Transpiler warns about them.

## A `.regia` Entry

A `.regia` file can be the Entry of a Build too (ADR 0049). Its Program has no Root Plot and no Instancing.

- **The Build is Target code only**: every Playbook and every Plot of the Program, and nothing that starts them (for Jason: ASL files, no `.jcm`, chapter 28). It is for putting into a project of the Target written by hand.
- **No Plot is taken for the Root**, not even the only one. The Target code is made so that any Plot of the Program can be the one that project starts.
- It is checked as `check` checks it, without the checks that need a Root Plot, so a problem may appear only when a `.regin` Entry reaches the file.
- Target settings take their defaults, and there is no `SEED`.
- It **can't be run** (chapter 23): a run needs a Root Plot and a cast.

## Agent kinds

A **`KIND`** describes an Agent kind: a sort of Agent the game may have many of, what each of them plays and starts with, and how many start.

```regia
KIND noble, PLAYS Guest:
    COUNT 3
    bravery AT RANDOM(0.2, 0.6)
    sympathy AT 0

KIND drunk_noble, LIKE noble, PLAYS Guest, Drunkard:
    COUNT 2
    bravery AT 0.8

KIND hothead, PLAYS Guest:
    aggressiveness AT RANDOM(0.6, 1)
    LEARN purse(RANDOM(30, 50))

KIND servant, PLAYS Servant         # only ever spawned by the game
```

- **`KIND <kind>[, LIKE <kind>, …][, PLAYS <Role>, …]`** names the kind, the kinds it starts from, and its Roles **in the Root Plot**. Each list ends at the next clause keyword (`LIKE`, `PLAYS`) or at the `:` (chapter 01). Roles joined with `AND` are the retired spelling (`R2125`). Every Agent of the kind plays **every** Role the kind ends up with, from the start and when it joins. To mix (5 guests, 2 of them drunk), write two kinds. Instancing makes no random picks. Random casting belongs to the Plot (`n OF`, chapter 15).
- **`COUNT <n>`** is how many Agents of the kind exist when the Program starts. A whole, non-negative literal. Left out, it means 0: the kind only enters by **joining** (chapter 19). It is the same noun as the Expression `COUNT(…)` (chapter 26), "how many", here of the kind's Agents.
- **`<propensity> AT <value>`** gives a starting Propensity value (chapter 14), worded like `SUITS … AT`. The value is a literal or `RANDOM(a, b)` with literal bounds, in [0, 1] for a Trait and [-1, 1] for a Mood, drawn **once per Agent** when it is created, so a spawned Agent gets its own draw too. A Propensity roll is **always a decimal**, however its bounds are written: `aggressiveness AT RANDOM(-1, 1)` is any aggressiveness from -1 to 1, not one of three. This is the one place chapter 04's rule for a roll's kind doesn't apply, since a Propensity value is never meant to be whole. Traits and Moods are written the same way.
- **Setup lines**: `ASSIGN`, `LEARN` and `PURSUE`, under the rules of a Role setup (below, *Setup lines*).
- The lines of the Body come in any order.
- A Propensity no line gives is **neutral**: 0.5 for a Trait, 0 for a Mood (chapter 14, ADR 0033). No warning.

### Building on other kinds: `LIKE`

`LIKE` names the kinds a kind starts from:

```regia
KIND latecomer, LIKE noble                  # a noble the game only spawns
KIND hot_knight, LIKE knight, hothead:
    COUNT 1
```

- The kind takes **every item of its bases except `COUNT`**, then its own lines replace the items they write, as a later file does (*Overriding*).
- The `PLAYS` lists of the bases are **joined**, and their setup lines are **joined** in `LIKE` order. A `PLAYS` or a setup line of the kind's own replaces what it took.
- **Two bases that set any other item differently are an error**, unless the kind writes that item itself. This is the rule for sibling files (`R2103`) in one declaration.
- A base may itself build on others. A kind can't reach itself through `LIKE`.
- A kind's first declaration needs `PLAYS` or `LIKE`, so that it plays something. A redeclaration in a later file may leave both out and keep what it had.

### Removing a kind: `NO KIND`

```regia
NO KIND hothead
```

A later file removes a kind with `NO KIND <kind>`. A removed kind has no Agents at the start and can't be spawned: the game naming it gets chapter 19's treatment of an unknown kind. Kinds and Agents built on it with `LIKE` still take its lines, so a kind can be kept as a template only. An importer may declare the kind again.

## Individual Agents

An **`AGENT`** declares one individual Agent, named by the writer:

```regia
AGENT king, PLAYS Host:
    LEARN seat(1)

AGENT gawain, LIKE knight:
    LEARN seat(3)
    LEARN grudge(percival)

AGENT percival, LIKE knight, hothead:
    LEARN seat(4)
```

- **`AGENT <name>[, LIKE <kind>, …][, PLAYS <Role>, …]`** is written and resolved like a `KIND`: the same lines, the same `LIKE`, the same overriding, line by line.
- An individual Agent has **no `COUNT`**. It is always one Agent, in the starting cast.
- **Its name is its Agent name.** The Target uses it as it is, so the game's character `gawain` is this Agent (chapter 36 for Jason). The game can spawn a kind but never an individual Agent: after it leaves, it doesn't come back.
- `NO AGENT <name>` removes it in a later file.
- An Agent of no kind is the common case for a part only one character plays: `AGENT king, PLAYS Host` says it once.

The starting cast is every individual Agent plus, for each kind, its `COUNT` of Agents named by the Target.

### Instancing names

Each individual Agent's name is a **Name inside Instancing**: it may be an argument of the Instancing's setup lines, as in `LEARN grudge(percival)`, and needs no `NAME` declaration (chapter 03). A `.regia` file can't name an individual Agent, since the story can't depend on a cast. A Plan meets `percival` at runtime as an ordinary Name arriving in a Fact.

Kind names and Agent names share one namespace, apart from the rest of the Program: a kind `noble` and a Fact `noble` can coexist, a kind `noble` and an Agent `noble` can't.

## Setup lines

The Body of a `KIND` or an `AGENT` may hold the three Statements of a Role setup (chapter 16):

| Statement | Gives the Agent |
|---|---|
| `ASSIGN <Playbook>[, MAPPING …]` | a Giving of the Playbook in the Root Plot, with no `TO` |
| `LEARN <fact>` | the Fact |
| `PURSUE <goal>` | the Goal, without waiting |

- They follow chapter 16's rules: arguments are Values or Expressions, `RANDOM` included; Expressions are worked out **per Agent**, so a roll is made once per Agent; no Placeholders and no `ME`; a Statement that can't be carried out is skipped with a Trace entry.
- An `ASSIGN`'s Mappings name Roles of the Root Plot.
- `LEARN` and `PURSUE` keep their one gloss, "the Agent comes to know" and "the Agent takes on" (chapter 16, *Sender*): the line says what the Agent starts with, and where it is written says who gives it.
- **Everything Instancing gives is told and asked by the Root Plot's Director**, like a setup, whether or not the Fact is a `GAME FACT`. `WHEN seat LEARNED, FROM DIRECTOR:` fires for it; `FROM GAME` doesn't.
- **Order.** When the Root Plot's Staging starts, the Root Plot's setups run for its starting cast as chapter 16 says: `CAST`, the Roles, then the initial Phase's. Then, for each starting Agent, its kind's lines (or, for an individual Agent, its own lines, which already hold what it took through `LIKE`), all before the entry Plans. A kind's lines say more about one Agent than its Role's, and run later.
- **Joining.** A spawned Agent runs its kind's lines after the setups of chapter 19's step 2, before the standing Givings reach it.

## The seed

```regia
SEED 42
```

`SEED <n>` sets the seed of every run of this Build (chapter 34: every random draw the language makes), so that a run can be played again. It is a whole, non-negative literal, and one item for overriding. A seed given when the run is started (`regia run --seed <n>`, chapter 23, or a behaviour case's header) beats it. With neither, each run picks its own seed and the Trace records it.

## Target settings

Which Target to build for is chosen **outside** Instancing: with `--target` on the command line (chapter 23), or in the Visual Editor's project settings. Instancing only configures Targets:

```regia
TARGET jason:
    strategy most_similar
    base_port 9000

TARGET python:
    tick 0.1
```

- `TARGET <name>:` groups the settings of one Target. The name is written as the command line writes it, in lowercase. A build reads only its own group and ignores the others, so one `.regin` can configure several Targets.
- Settings are `key value`, a lowercase key defined by the Target followed by its value, the shape of `SEED 42` and `COUNT 2`. Values are a word, a Number or a string. A setting is not a `LET` (chapter 04): it fills no Placeholder, and a later `.regin` may override it. The retired spelling `key = value` is an error with the hint `key value` (`R2124`).
- The Transpiler **warns** about a group for a Target it doesn't know, about an unknown key under a Target it knows, and about a value outside the set a known key takes (such as `strategy`: `most_similar` or `random`).
- **Every setting has a default.** Mechanical details (Jason's `ag-class`, addresses, ports, Agent names) never have to be written. A setting with no natural default gets one from the Transpiler: VEsNA-Pro's `strategy` defaults to `most_similar`.
- The ASL encoding of control flow (chapter 06: native `if` or subgoal plans) is **implied by the Target**, not set. The `ASL_VERSION` comment is retired: Jason gets native `if`, the in-house interpreters get subgoal plans. If an interpreter gains native `if`, its Target changes, not the designer's files.

The set of Targets and their keys belong to *Supporting multiple Targets*.

## Transpiler checks

Checks on kinds and individual Agents run only when at least one exists.

**Errors**

- `R2101` A `.regia` file importing a `.regin`.
- `R2102` A `.regin` declaring anything other than Imports and Instancing.
- `R2103` Two sibling files setting the same item differently, with no file above them settling it.
- `R2104` A `.regin` Entry that reaches no `ROOT`, or a `ROOT` naming a Plot that is started as a Subplot.
- `R2105` A `PLAYS` Role that isn't a Role of the Root Plot.
- `R2106` A Propensity that isn't declared as `TRAIT` or `MOOD`.
- `R2107` A value, or a `RANDOM` bound, that isn't a literal, or lies outside [0, 1] for a Trait or [-1, 1] for a Mood.
- `R2108` A `COUNT` or a `SEED` that isn't a whole, non-negative literal.
- `R2109` The same name declared twice in one file, as a kind or an individual Agent.
- `R2114` A Root Plot with parameters: Instancing has nothing to pass them (chapter 17).
- `R2117` A kind or an individual Agent that plays nothing: a first declaration with neither `PLAYS` nor `LIKE`. Absence check (chapter 23).
- `R2118` A `COUNT` in an `AGENT`.
- `R2119` A `LIKE` naming something that isn't a kind, or a kind reaching itself through `LIKE`.
- `R2120` Two bases setting the same item differently, with the kind or Agent not writing it (the message names both bases).
- `R2121` A `NO KIND` or `NO AGENT` naming nothing declared in the files the file reaches. Absence check (chapter 23).
- `R2122` An argument naming an individual Agent this build doesn't have.
- `R2123` A kind and an individual Agent with the same name.
- `R2124` A Target setting written with the retired `=` (`strategy = random`; hint: `strategy random`).
- `R2125` Roles after `PLAYS` joined with the retired `AND` (`PLAYS Guest AND Drunkard`; hint: `PLAYS Guest, Drunkard`).

A setup line that breaks chapter 16's rules gets chapter 16's code (`R1602`, `R1603`, `R1604`) or chapter 03's `R0309` for `ME`, as in a Role setup.

**Warnings**

- `R2110` A Root Plot Role that no kind and no individual Agent plays. Absence check (chapter 23).
- `R2111` Retired (ADR 0033): a missing value is neutral.
- `R2112` A Plot the Root Plot never reaches. Absence check (chapter 23).
- `R2113` An unknown key in the group of a known Target, or a value outside the set its key takes.
- `R2115` A Quota `FROM n OF Role` or `BY n OF Role` in the Root Plot, with n made of Values only, where the individual Agents that play the Role plus the `COUNT`s of the kinds that play it add up to fewer than n, and none of those kinds has a `COUNT` of 0 (which only enters by joining). The Role can never be that large in this build, so the Quota can never be met (chapter 18).
- `R2116` A `TARGET` group for a Target the Transpiler doesn't know. It is skipped.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- The `.jcm` gets one `agent` entry per starting Agent: individual Agents under their own names, the Agents of a kind named by the Target (`noble_1` …), each with its Role file(s), and, when chapter 14's emission rules call for it, the Propensity values as the user parameter `temper(t(v), …, m(v)[mood], …)`, neutral values filled in. `RANDOM` values are drawn by the infrastructure when the Agent is created, not by the Transpiler, so each run and each joiner draws again.
- `strategy` from the `jason` group goes into the parameters of every Agent that gets a `temper`, and of no other.
- The Root Plot's Director starts with the cast: each starting Agent and its Roles. Joining reaches the same Director with the kind's Roles (chapter 19), so the Director needs each kind's Roles, Propensity values and setup lines.
- The Root Plot's Director runs the setup lines of kinds and individual Agents, as it runs Role setups. `LIKE` is resolved at compile time. A line's `ASSIGN` is a Giving to that one Agent. For Jason, chapter 30 (*Setup lines of kinds and individual Agents*).
- An Agent playing several Root Plot Roles needs every Playbook those Roles can be given. Role files exist for Root Plot Roles only (chapter 28); an Agent playing several Roles runs a generated combination file (chapter 36).
- The seed from `SEED` is the run's seed unless one is given when the run starts (chapter 35).
- The `.jcm`, Agent names, ports, `cast.json`, the drawing of `RANDOM` and the Root Director's `regia_kind` beliefs are in chapter 36 (`36-jason-jcm.md`).

## Regia 1.5

Instancing is in 1.5 as this chapter describes it (ADR 0025), with one exception: joining. In 1.5 the game can't spawn an Agent while the run goes on, and a spawn is refused with `T1902` (chapter 19). Every Agent is in the starting cast. A kind that only the game would spawn has no Agents in 1.5, and a spawned Agent running its kind's lines comes with joining, later. Revised in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- The set of Targets, their settings and how Instancing maps per Target: *Supporting multiple Targets*.
- Counted picks at instancing time, and Roles outside the Root Plot: not in 2.0. Instancing never picks.
- How the Visual Editor shows and edits `.regin` files: *Visual Editor architecture*.
