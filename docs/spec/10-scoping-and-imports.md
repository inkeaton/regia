# Scoping and imports

How names are organised across files and constructs: imports, the program-wide namespace, External names, and Vocabulary declared inside a Playbook or Plot. Decided in the ticket *Scoping, imports and aliases* (`.scratch/regia-2/issues/10-scoping-and-imports.md`). It builds on chapters 01, 03 and 05, and replaces the import, alias and declaration-placement parts of primer ch.2–3. The rule that a name has one parameter count is recorded in `docs/adr/0006-one-parameter-count-per-name.md`.

## Imports

```regia
#@desc: The tavern brawl.

IMPORT "shared/food"
IMPORT "../common/insults.regia"

PLAYBOOK Brawler:
    WHEN insult_heard(?s): DO punch(?s)
```

- `IMPORT "<path>"` is a Statement of its own. Imports come **first in the file**, after the file's doc comment (chapter 02) and before any declaration. An `IMPORT` anywhere else is an error.
- The path is a **string relative to the importing file**. The `.regia` extension may be left out. There are no project roots, search paths or packages in 2.0.
- Imports are **transitive**: a file sees everything it declares, everything it imports, and everything those files import, all the way down. So a hub file that only imports others works as a single import.
- A file is **loaded once**, however many import paths lead to it, so diamond dependencies are fine.
- An **import cycle** is an error that names every file in the loop.
- There is **no export control**: everything at a file's top level is visible to any file that reaches it. The only private names are Local Vocabulary (below).

### Broken transitive names

A name a file gets through another file's import breaks when that import is removed, and the error shows up in a file nobody edited. So the Transpiler says where the name used to come from:

```
error: `hungry` is not declared
  --> brawl.regia:12
  hint: `hungry` is declared in `shared/food.regia`, which this file no longer reaches.
        Add `IMPORT "shared/food"`.
```

The Transpiler can only offer the hint when the declaring file is still part of the program (below). Showing, per file, which names it uses through other files is for the Visual Editor (*What the graph shows*).

## The program

- A Program starts from **one Entry file**. The **Program** is every file reachable from it through imports. Builds are layered by importing (`test.regin` imports `banquet.regin`, chapter 21), never by naming several Entry files, so `regia check a.regin b.regin` checks two Programs, one after the other (chapter 23). Entry files are often `.regin` Instancing files, which import `.regia` files and other `.regin` files; a `.regia` file can't import a `.regin` (chapter 21). Only a `.regin` Entry can be built; a `.regia` Entry is checked without a Root Plot (chapter 21).
- **Visibility is per file**: a file can only use names it declares or reaches through its imports.
- **Uniqueness is program-wide**: the checks below cover every file of the Program, even two files that never import each other (both reached from the Entry through different paths). At runtime they could meet on one Agent that runs Playbooks from both, so one name must mean one thing everywhere.

## One namespace

- Vocabulary items, Playbooks and Plots share **one flat, program-wide namespace**. Names are never qualified by file (`food.hungry` means nothing). A Playbook and a Fact can't share a name.
- Role and Phase names stay **local to their Plot** (glossary), so two Plots may each have a `Host` Role.
- Declared Names (chapter 03) are in the same namespace: `NAME roast` and `FACT roast` can't both exist.
- A name has **one kind** (chapter 05) and **one parameter count** (ADR 0006). `FACT hates(a)` and `FACT hates(a, b)` in the same Program is an error, as is using a name with the wrong number of arguments.
- **Re-declaring** a name with the same kind, the same parameter count and the same External name (or none) declares **the same item**. This lets a Playbook file declare what it uses without a shared file. Parameter names may differ, since they only document (chapter 03). Any mismatch is an error that names both declarations.
- Re-declaring a **Playbook or Plot** is always an error: they have bodies, so two of them can't be "the same".

## Name rules

Decided in the ticket *ASL infrastructure layout* (`.scratch/regia-2/issues/34-asl-infrastructure-layout.md`), so that every Target can turn names into its own and make up names of its own (chapter 28).

- **Names are unique ignoring case.** `Guest` and `guest` can't both be declared in the program-wide namespace, nor as two Roles or two Phases of one Plot. Readers would mix them up, and Targets that change case (Jason lowercases the first letter) or file systems that ignore case would merge them. For the same reason a Plot's Role and a Playbook's Role bind by name ignoring case: `Host` fills `host` (chapter 15). Two Placeholders of one Plan (a Plot's parameters included) can't differ only in case either: `?x` and `?X` would become one Jason variable (chapter 39).
- **A name can't start with `regia_`** (in any case), and **can't contain `__`**. Both are kept for Generated names (chapter 28), so the Transpiler's own names never collide with a designer's. This holds for Placeholder names too (`?regia_w`, `?a__b`), since the Transpiler makes up variables of its own (chapter 39).
- External names (below) are exempt: they are the game's names, not Regia's.

## Declaration order

After the imports, top-level declarations (Vocabulary, Playbooks, Plots) can come **in any order**, and a name can be used before it is declared. The primer's rule that Vocabulary must come first is dropped.

## What the game produces: `GAME`

Decided in the ticket *The Vocabulary and the game* (`.scratch/regia-revision/issues/07-vocabulary-and-the-game.md`), with ADR 0026.

```regia
GAME CUE   food_served, insult_heard(speaker)
GAME FACT  hungry, door_open
CUE        scandal(person)          # told between Agents
FACT       on_duty                  # learned and told by Agents
```

- A `FACT` or `CUE` declared with **`GAME`** in front is a **game item**: the game produces it. Every other Fact and Cue is produced only by the Program itself: `LEARN`, `UPDATE`, `TELL`, `SIGNAL`, `END PLOT WITH` and `FAIL WITH`.
- `GAME` says where an item comes from and nothing else. Plans test, react to and tell a game item like any other: `GIVEN hungry`, `WHEN food_served:`, `TELL Guest food_served` (a told game Cue is the same Cue, chapter 07).
- **Only a game item comes from the game.** A game message for a Fact or Cue not declared `GAME` is dropped by the Target, with a Trace warning.
- `GAME` goes on `FACT` and `CUE` only (`R1016`). A `GOAL` never comes from the game. An `ACTION` is split by its External name instead (below).
- **A local item is never `GAME`** (below): local Facts and Cues never come from the game.
- In a Multi-definition `GAME` covers every item of the line, like the kind word.
- A re-declaration merges only if both say `GAME` or neither does (`R1005`).
- What `GAME` lets the Transpiler check: a Cue that isn't `GAME` and that nothing in the Program sends (`R3807`, chapter 38), and a Plan that changes a game Fact (`R0807`, chapter 08).

## External names

```regia
ACTION engine.security.summon_guards AS call_guards
GAME CUE engine.combat.hit AS hit_by(attacker)
GAME FACT  world.time.is_night AS night, hungry
```

- A game item and an `ACTION` may give an **External name** with `<external> AS <name>`: the name the game, or the Target, uses. The source always uses the name after `AS`; only the Target sees the External name. Without `AS`, the External name is the Regia name as written.
- An External name has **no meaning in Regia**. It may contain dots and any other character the game uses.
- **A Fact's or Cue's External name is the game's name for it.** The Target translates it into the Regia name when the game reports the item, so no Target ever has to hold the game's spelling (chapter 28).
- **An Action's External name says who runs it.** With no dot it is a **game Action**: the Target asks the game to perform it, under the External name. With a dot it is the **Target's own code**: a Java internal action in Jason (`vesna.walk`), a function of the project in another Target. Regia doesn't know what such code does, and doesn't wait on the game for it (chapter 37). A game can't name an Action with a dot.
- A **dotted name** is only ever an External name, and a dotted name without `AS` is an error, since the Body would have to write it out.
- `AS` on a `FACT` or `CUE` that isn't `GAME` is an error: only the game uses its names. `GOAL` takes no `AS`.
- Parameters are written once, after the Regia name. In a Multi-definition, `AS` belongs to the one item it follows.
- **One External name, one Regia name**: `ACTION a.summon AS call_guards` in one file and `ACTION a.summon AS summon` in another is an error.
- A re-declaration merges only if the External names match too: `ACTION call_guards` and `ACTION a.summon AS call_guards` is an error.

## Local Vocabulary

```regia
PLAYBOOK Greeter:
    FACT already_greeted(person)
    GOAL greet(person)

    WHEN arrived(?p):
        GIVEN NOT already_greeted(?p): PURSUE greet(?p)

    TO greet(?p): DO wave(?p). LEARN already_greeted(?p)
```

- `FACT` may be declared **inside a `PLAYBOOK` or `PLOT`** Block. `GOAL` and `CUE` may be declared inside a `PLAYBOOK` only. `ACTION` may not be local: it is the game's interface and stays at file level.
- **A Plot has no local Goals.** Its Director can't pursue a Goal or write a recipe (chapter 20), so the declaration could never be used. It is an error, with a hint to declare the Goal at file level if the Plot means to `ASK` for it.
- **A Plot has no local Cues.** An Outcome has to be named by the parent, and a Signal by the Playbook that sends it.
- Local declarations go **anywhere in the Block**, in any order, and are visible **everywhere inside it**, including every `DURING` of a Plot. They are never visible outside the Block, not even in the same file, and can't be imported.
- A local item has **no External name** (no `AS`) and is never `GAME`.
- **No shadowing**: a local name that matches any name the file can see is an error. Two different Playbooks may each declare the same local name; those are two different items.
- A local Fact or Goal is **private to its Playbook**, or to its Plot's Director, even on an Agent that runs other Playbooks. Another Playbook on the same Agent can't test, change or react to it.
- Local Facts and local Cues **never come from the game**. Only the Playbook's own `LEARN`, `FORGET` and `UPDATE` touch a local Fact, and only the Playbook's own `TELL` sends a local Cue.
- Local Facts and Goals **can't be sent**: `TELL`, `ASK … TO` or `SIGNAL` with one is an error, because nothing outside the Playbook can name it.
- A local Cue **can be told** (below).
- **When a Playbook is taken away**, its local Facts stay but no Plan can see them. They are there again if the Playbook is given back, so `already_greeted` survives. A Playbook that wants one gone forgets it in its `WHEN REMOVED:` Plan (chapter 15). Local Goals being pursued are dropped, since their recipes are gone; their `DROPPED` and `ENDED` Plans still run (chapter 15, *Taking a Playbook away*).

### Local Cues

```regia
PLAYBOOK Duelling:
    ROLE opponent
    CUE challenged, hit, yielded

    TO fight:
        TELL opponent challenged

    WHEN hit, FROM opponent:
        ...
```

A Cue that one Playbook both sends and reacts to may be declared inside it (ADR 0016). `challenged`, `hit` and `yielded` are what two holders of `Duelling` say to each other, and no other Playbook or Plot can name them.

- A local Cue is sent with **`TELL`, to any recipient** `TELL` accepts (chapter 07): a Role of the Playbook, a Placeholder that holds an Agent, or `EVERYONE`.
- A receiver that holds the Playbook reacts with the Playbook's `WHEN` Plans, with `FROM` as for any told Cue. A receiver that doesn't hold it has no Plan for the Cue, and nothing happens, as with any told Cue nobody reacts to.
- A local Cue **can't be Signalled** (`R1014`) and **can't be an Outcome** (`R1004`): a Director is outside the Playbook and couldn't name it.
- A local Cue **can be a Reason** (`FAIL WITH`, chapter 11). Only Plans of the same Playbook can match it with `FAILED WITH`; an asker outside the Playbook hears the Failure and matches it with plain `FAILED`.
- It follows the other rules of local items: no External name, no shadowing, not importable, and two Playbooks may each declare the same local name as two different Cues.

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## Transpiler checks

**Errors**

- `R1001` An `IMPORT` that isn't at the top of the file, after its doc comment and before any declaration.
- `R1002` An import path that leads to no file.
- `R1003` An import cycle (the message names every file in the loop).
- `R1004` A name that isn't declared in the file or anything it reaches (when the declaring file is still in the Program, the hint names it and suggests the `IMPORT`).
- `R1005` Two declarations of one name that don't agree on kind, parameter count, External name or `GAME` (the message names both).
- `R1006` A Playbook or Plot declared twice.
- `R1007` Two names that differ only in case, in the program-wide namespace, among one Plot's Roles or Phases, or among one Plan's Placeholders.
- `R1008` A name, a Placeholder's included, that starts with `regia_` or contains `__`.
- `R1009` A dotted name without `AS`.
- `R1010` `AS` on a `GOAL`, on a local declaration, or on a `FACT` or `CUE` that isn't `GAME`.
- `R1011` One External name given two Regia names.
- `R1012` `ACTION` declared inside a `PLAYBOOK` or `PLOT`, or `CUE` declared inside a `PLOT`.
- `R1013` A local name that shadows a name the file can see.
- `R1014` A local Fact or Goal sent with `TELL`, `ASK … TO` or `SIGNAL`, or a local Cue sent with `SIGNAL`.
- `R1015` `GOAL` declared inside a `PLOT` (hint: declare it at file level to `ASK` for it).
- `R1016` `GAME` on anything but a `FACT` or a `CUE`, or on a local declaration (a `NAME` line is `R0311`).

## ASL mapping notes

For *The full ASL mapping* to pick up:

- Imports are resolved by the Transpiler. Nothing about them reaches the Target.
- A game item's External name never appears in ASL: beliefs and events use the Regia name, and `regia-jason` translates the game's name on the way in (chapter 28). A game Action's External name travels in the message to the game (chapter 37). A dotted Action's External name is passed to `regia.act`, which runs the Java internal action of that name (chapter 37).
- Local Facts, Goals and Cues get Generated names that can't collide across Playbooks: `regia_local__<Playbook or Plot>__<name>` (chapter 28). A told local Cue travels under that name, which is the same on every holder of the Playbook.
- Names, Generated names and External names in Jason: chapter 28.
- Keeping local Facts while the Playbook is taken away fits filtering Plans by a belief (*Research: dynamic plan loading in Jason*). The beliefs stay, only the Plans that read them are switched off. Dropping local Goals belongs to the code that takes a Playbook away: chapter 29 (`29-jason-givings.md`).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025), `GAME FACT` and `GAME CUE` included. `FROM GAME` is chapter 05's, and later.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- Project roots, search paths and packages: not in 2.0. The Visual Editor's Project only bounds which files the Workspace holds (chapter 24). Roots can be added later, since a relative path stays valid.
- How the Visual Editor shows names that come through other files: *What the graph shows*.
- Per-Target External names (the same Fact named differently in each Target): *Supporting multiple Targets*.
