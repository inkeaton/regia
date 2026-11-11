# Instancing

How a Program becomes a running cast: which Plot is the Root Plot, which kinds of Agent exist and how many start, their starting Propensity values, and settings for a Target. Decided in the ticket *Instancing comments* (`.scratch/regia-2/issues/22-instancing-comments.md`). It builds on chapters 02, 10, 13, 14, 15, 17 and 19.

Instancing sits at a different level from the rest of the language. Playbooks and Plots describe behaviour for Roles. Instancing says who actually plays them in one build. It is **optional**.

## Where Instancing is written

Instancing can be written in two places, with the same syntax:

- **Instancing comments** in any `.regia` file: `#%` for one Statement, `#%[ … ]#` for Blocks (chapter 02).
- An **Instancing file**, `.regin`, which holds only `IMPORT`s and Instancing, written without the `#%` markers.

```regia
# banquet.regia
IMPORT "playbooks.regia".

#% ROOT RoyalBanquet.
#%[
AGENT noble PLAYS Guest:
    COUNT 5.
]#

PLOT RoyalBanquet:
    ...
```

```regia
# test.regin
IMPORT "banquet.regia".

AGENT noble PLAYS Guest:
    COUNT 2.
    bravery AT 0.5.

TARGET JASON:
    strategy = random.
```

Rules:

- In a `.regia` file, Instancing comments sit at the **top level** only, after the `IMPORT`s, never inside a Plot, Playbook or other Block. Like doc comments, they start their own line.
- A `.regin` holds only `IMPORT`s and Instancing: no Vocabulary, Playbooks or Plots.
- A `.regin` may import `.regia` files and other `.regin` files. Importing another `.regin` layers builds: `test.regin` imports `base.regin` and changes only what differs.
- A `.regia` file importing a `.regin` is an error. Design files never depend on a build.
- `.regin` files are usually Entry files (chapter 10), but anything they reach is part of the Program as usual.

Several builds of one story (a 2-guest test, a 50-guest release, a build for each Target) are several small `.regin` files importing the same `.regia` files.

## Overriding

**The importer overrides what it imports.** A setting in a file replaces the same setting in any file it reaches through its imports, directly or not.

- **Whole items are replaced.** The items are: the `ROOT` Statement, each single Target setting (`TARGET JASON: strategy`), and each Agent declaration (by kind name). A file that redeclares `AGENT noble` replaces its Roles, count and Propensity values together. Nothing is merged field by field.
- **Siblings that disagree are an error.** If two files set the same item differently and neither reaches the other, some file reaching both must set it, or the Transpiler reports both files. Import order never decides (chapter 10).
- Two identical settings never conflict.

## With no Instancing

Instancing is optional. With no Agent declarations, the Transpiler emits Target code only (for Jason: the ASL files, no `.jcm`). Instancing that only names the Root Plot or gives Target settings also produces Target code only. The instancing output (the `.jcm` for Jason) is produced as soon as at least one Agent declaration exists.

## The Root Plot

A Program has **exactly one Root Plot**. Every other Plot is a Subplot below it, reached only through `START SUBPLOT` (chapter 17). Instancing never starts a Plot. Stories that run side by side are Subplots started by the Root Plot (usually from `DURING PLOT: WHEN ENTERED:`) and ordered by its `PRECEDENCE` (chapter 13).

- The Root Plot is **inferred** when exactly one Plot of the Program is never started as a Subplot.
- Otherwise it must be named: `ROOT RoyalBanquet.`
- Naming a Plot that is started as a Subplot somewhere is an error, since its Staging would have no clear parent.
- With no named Root Plot and none or several candidates, the Transpiler stops with an error, **even with no other Instancing**. Rank keys and Role files depend on the Root Plot.
- Plots that the Root Plot never reaches are compiled like the rest but never run. The Transpiler warns about them.

## Agent declarations

An Agent declaration describes an **Agent kind**: what each Agent of that kind plays and starts with, and how many start.

```regia
AGENT noble PLAYS Guest:
    COUNT 3.
    bravery AT RANDOM(0.2, 0.6).
    sympathy AT 0.

AGENT drunk_noble PLAYS Guest AND Drunkard:
    COUNT 2.
    bravery AT 0.8.

AGENT servant PLAYS Servant.        # only ever spawned by the game
```

- **`AGENT <kind> PLAYS <Role> [AND <Role>…]`** names the kind and its Roles **in the Root Plot**. Every Agent of the kind plays **every** listed Role, from the start and when it joins. To mix (5 guests, 2 of them drunk), write two kinds. Instancing makes no random picks. Random casting belongs to the Plot (`n OF`, chapter 15).
- **`COUNT <n>.`** is how many Agents of the kind exist when the Program starts. A whole, non-negative literal. Left out, it means 0: the kind only enters by **joining** (chapter 19).
- **`<propensity> AT <value>.`** gives a starting Propensity value (chapter 14), worded like `SUITS … AT`. The value is a literal in [-1, 1] or `RANDOM(a, b)` with literal bounds in [-1, 1], drawn **once per Agent** when it is created, so a spawned Agent gets its own draw too. Traits and Moods are written the same way.
- With no Body, the header ends with `.`.
- A Propensity a kind doesn't mention has no value. What that means is the Target's business (VEsNA-Pro skips it).
- No per-Agent overrides in 2.0: Agents of one kind differ only through `RANDOM`.

### Kind names and Agent names

- Kind names live **only in Instancing**, in their own namespace. A kind `noble` and a Fact `noble` can coexist. Regia code never names a kind: Plans address Roles.
- The game uses kind names: when it spawns an Agent, it reports the kind and a name of its own for the new Agent (chapter 19). The Agent joins the Root Plot in the kind's Roles, with its Role setups (chapter 16) and the Propensity values of its kind.
- Names of the starting Agents (such as `noble_1` … `noble_3`) come from the Target.

## Target settings

Which Target to build for is chosen **outside** Instancing: on the Transpiler's command line, or in the Visual Editor. Instancing only configures Targets:

```regia
TARGET JASON:
    strategy = most_similar.
    base_port = 9000.

TARGET PYTHON:
    tick = 0.1.
```

- `TARGET <NAME>:` groups the settings of one Target. A build reads only its own group and ignores the others, so one `.regin` can configure several Targets.
- Settings are `key = value.`, with lowercase keys defined by the Target. Values are a word, a Number or a string.
- The Transpiler checks the keys of the Targets it knows and **warns** about unknown ones.
- **Every setting has a default.** Mechanical details (Jason's `ag-class`, addresses, ports, Agent names) never have to be written. A setting with no natural default gets one from the Transpiler: VEsNA-Pro's `strategy` defaults to `most_similar`.
- The ASL encoding of control flow (chapter 06: native `if` or subgoal plans) is **implied by the Target**, not set. The `ASL_VERSION` comment is retired: Jason gets native `if`, the in-house interpreters get subgoal plans. If an interpreter gains native `if`, its Target changes, not the designer's files.

The set of Targets and their keys belong to *Supporting multiple Targets*.

## Transpiler checks

Checks on Agent declarations run only when at least one exists.

**Errors**

- A `#%` comment inside a Block, or a `.regia` file importing a `.regin`.
- A `.regin` declaring anything other than Imports and Instancing.
- Two sibling files setting the same item differently, with no file above them settling it.
- No Root Plot: no `ROOT`, and zero or several Plots are never started as a Subplot. Or a `ROOT` naming a Plot that is started as a Subplot.
- A `PLAYS` Role that isn't a Role of the Root Plot.
- A Propensity that isn't declared as `TRAIT` or `MOOD`.
- A value, or a `RANDOM` bound, outside [-1, 1] or not a literal.
- A `COUNT` that isn't a whole, non-negative literal.
- The same kind declared twice in one file.

**Warnings**

- A Root Plot Role that no kind plays.
- A kind with no value for a Propensity that a `SUITS` Label mentions in a Playbook its Agents can hold.
- A Plot the Root Plot never reaches.
- An unknown key in the group of a known Target.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- The `.jcm` gets one `agent` entry per starting Agent, named by the Target (`noble_1` …), with its Role file(s), and the Propensity values as the user parameter `temper(t(v), …, m(v)[mood], …)` (chapter 14). `RANDOM` values are drawn by the infrastructure when the Agent is created, not by the Transpiler, so each run and each joiner draws again.
- `strategy` from the `JASON` group goes into each Agent's parameters.
- The Root Plot's Director starts with the cast: each starting Agent and its Roles. Joining reaches the same Director with the kind's Roles (chapter 19), so the Director needs each kind's Roles and Propensity values.
- An Agent playing several Root Plot Roles needs every Playbook those Roles can be given. Role files exist for Root Plot Roles only (chapter 28); a kind playing several Roles runs a generated combination file (chapter 36).
- The `.jcm`, Agent names, ports, `cast.json`, the drawing of `RANDOM` and the Root Director's `regia_kind` beliefs are in chapter 36 (`36-jason-jcm.md`).

## Not decided here

- The set of Targets, their settings and how Instancing maps per Target: *Supporting multiple Targets*.
- Per-Agent overrides, counted picks at instancing time, and Roles outside the Root Plot: not in 2.0.
- How the Visual Editor shows and edits `.regin` files: *Visual Editor architecture*.
