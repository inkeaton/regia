# Scoping and imports

How names are organised across files and constructs: imports, the program-wide namespace, External names, and Vocabulary declared inside a Playbook or Plot. Decided in the ticket *Scoping, imports and aliases* (`.scratch/regia-2/issues/10-scoping-and-imports.md`). It builds on chapters 01, 03 and 05, and replaces the import, alias and declaration-placement parts of primer ch.2–3. The rule that a name has one parameter count is recorded in `docs/adr/0006-one-parameter-count-per-name.md`.

## Imports

```regia
#@desc: The tavern brawl.

IMPORT "shared/food".
IMPORT "../common/insults.regia".

PLAYBOOK Brawler:
    WHEN insult_heard(?s): DO punch(?s).
```

- `IMPORT "<path>".` is a Statement of its own. Imports come **first in the file**, after the file's doc comment (chapter 02) and before any declaration. An `IMPORT` anywhere else is an error.
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
        Add `IMPORT "shared/food".`
```

The Transpiler can only offer the hint when the declaring file is still part of the program (below). Showing, per file, which names it uses through other files is for the Visual Editor (*What the graph shows*).

## The program

- The Transpiler is given one or more **Entry files**. The **Program** is every file reachable from them through imports. Entry files are often `.regin` Instancing files, which import `.regia` files and other `.regin` files; a `.regia` file can't import a `.regin` (chapter 21).
- **Visibility is per file**: a file can only use names it declares or reaches through its imports.
- **Uniqueness is program-wide**: the checks below cover every file of the Program, even two files that never import each other. At runtime they could meet on one Agent that runs Playbooks from both, so one name must mean one thing everywhere.

## One namespace

- Vocabulary items, Playbooks and Plots share **one flat, program-wide namespace**. Names are never qualified by file (`food.hungry` means nothing). A Playbook and a Fact can't share a name.
- Role and Phase names stay **local to their Plot** (glossary), so two Plots may each have a `Host` Role.
- A name has **one kind** (chapter 05) and **one parameter count** (ADR 0006). `FACT hates(a)` and `FACT hates(a, b)` in the same Program is an error, as is using a name with the wrong number of arguments.
- **Re-declaring** a name with the same kind, the same parameter count and the same External name (or none) declares **the same item**. This lets a Playbook file declare what it uses without a shared file. Parameter names may differ, since they only document (chapter 03). Any mismatch is an error that names both declarations.
- Re-declaring a **Playbook or Plot** is always an error: they have bodies, so two of them can't be "the same".

## Name rules

Decided in the ticket *ASL infrastructure layout* (`.scratch/regia-2/issues/34-asl-infrastructure-layout.md`), so that every Target can turn names into its own and make up names of its own (chapter 28).

- **Names are unique ignoring case.** `Guest` and `guest` can't both be declared in the program-wide namespace, nor as two Roles or two Phases of one Plot. Readers would mix them up, and Targets that change case (Jason lowercases the first letter) or file systems that ignore case would merge them.
- **A name can't start with `regia_`** (in any case), and **can't contain `__`**. Both are kept for Generated names (chapter 28), so the Transpiler's own names never collide with a designer's.
- External names (below) are exempt: they are the game's names, not Regia's.

## Declaration order

After the imports, top-level declarations (Vocabulary, Playbooks, Plots) can come **in any order**, and a name can be used before it is declared. The primer's rule that Vocabulary must come first is dropped.

## External names

```regia
ACTION engine.security.summon_guards AS call_guards
EVENT  engine.combat.hit AS hit_by(attacker)
FACT   world.time.is_night AS night, hungry
```

- `FACT`, `EVENT` and `ACTION` may give an **External name** with `<external> AS <name>`: the name the game uses, often dotted. The source always uses the name after `AS`; only the Target sees the External name.
- A **dotted name** is only ever an External name. It has no namespace meaning in Regia, and a dotted name without `AS` is an error, since the Body would have to write it out.
- `GOAL` takes no `AS`: Goals never come from the game.
- Parameters are written once, after the Regia name. In a Multi-definition, `AS` belongs to the one item it follows.
- **One External name, one Regia name**: `ACTION a.summon AS call_guards` in one file and `ACTION a.summon AS summon` in another is an error.
- A re-declaration merges only if the External names match too: `ACTION call_guards` and `ACTION a.summon AS call_guards` is an error.

## Local Vocabulary

```regia
PLAYBOOK Greeter:
    FACT already_greeted(person)
    GOAL greet(person)

    WHEN arrived(?p):
        GIVEN NOT already_greeted(?p): PURSUE greet(?p).

    TO greet(?p): DO wave(?p). LEARN already_greeted(?p).
```

- `FACT` and `GOAL` may be declared **inside a `PLAYBOOK` or `PLOT`** Block. `EVENT` and `ACTION` may not: they are the game's interface and stay at file level.
- Local declarations go **anywhere in the Block**, in any order, and are visible **everywhere inside it**, including every `DURING` of a Plot. They are never visible outside the Block, not even in the same file, and can't be imported.
- A local item has **no External name** (no `AS`).
- **No shadowing**: a local name that matches any name the file can see is an error. Two different Playbooks may each declare the same local name; those are two different items.
- A local Fact or Goal is **private to its Playbook**, or to its Plot's Director, even on an Agent that runs other Playbooks. Another Playbook on the same Agent can't test, change or react to it.
- Local Facts **never come from the game**. Only the Playbook's own `LEARN`, `FORGET` and `CHANGE` touch them.
- Local items **can't be sent**: `TELL`, `ASK … TO` or `SIGNAL` with a local item is an error, because nothing outside the Playbook can name it.
- **When a Playbook is taken away**, its local Facts stay but no Plan can see them. They are there again if the Playbook is given back, so `already_greeted` survives. Local Goals being pursued are dropped, since their recipes are gone.

## Reserved words

`IMPORT`, `AS`.

## ASL mapping notes

For *The full ASL mapping* to pick up:

- Imports are resolved by the Transpiler. Nothing about them reaches the Target.
- External names are emitted in place of the Regia name. 1.0 already did this for Actions.
- Local Facts and Goals get Generated names that can't collide across Playbooks: `regia_local__<Playbook or Plot>__<name>` (chapter 28).
- Names, Generated names and External names in Jason: chapter 28.
- Keeping local Facts while the Playbook is taken away fits filtering Plans by a belief (*Research: dynamic plan loading in Jason*). The beliefs stay, only the Plans that read them are switched off. Dropping local Goals belongs to the code that takes a Playbook away: chapter 29 (`29-jason-givings.md`).

## Not decided here

- Project roots, search paths and packages: not in 2.0. The Visual Editor's Project only bounds which files the Workspace holds (chapter 24). Roots can be added later, since a relative path stays valid.
- How the Visual Editor shows names that come through other files: *What the graph shows*.
- Per-Target External names (the same Fact named differently in each Target): *Supporting multiple Targets*.
