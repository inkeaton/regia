# Precedence in Jason

How the Jason Target enforces precedence (chapter 13). It covers how a Plot's `PRECEDENCE` relations become numbered levels, the shape of a Giving's `Rank`, how a Subplot learns its place under its parent, the annotation on every Playbook plan, and the steps `selectOption` follows in Agents and Directors. Decided in the ticket *Precedence encoding in ASL* (`.scratch/regia-2/issues/38-precedence-encoding.md`). It builds on chapter 28's layout, chapter 29's Giving record, chapter 30's Directors and chapter 31's Stagings, and fills in the *ASL mapping notes* of chapter 13. It was checked against the latest VEsNA-Pro source (`vesna-pro-main/src/agt/vesna/VesnaAgent.java`, `Temper.java`).

## Levels: the order is worked out at compile time

At runtime the Infrastructure only compares numbers. The Transpiler turns each Plot's relations into **levels**: 0, 1, 2, …, where **lower wins**.

Each Plot gets two **level tables**:

- **The Staging table** ranks its direct Subplots (by Plot name) and `SELF`.
- **The Playbook table** ranks the Playbooks it gives out.

A Director's own Plans get a third, smaller table (*Directors*, below).

Each table is worked out **once for every Trigger item** named in an `ON` relation of that table, and once for every other item:

1. Collect the relations that apply to the item: those without `ON`, plus those `ON` that item.
2. Add the defaults of chapter 13 as relations: every Subplot `OVER SELF`, unless a relation says otherwise.
3. Fold in each Subplot's `PARENT` relations, rewritten from the parent's side (`PARENT OVER SELF` in HonorDuel is `SELF OVER HonorDuel` here). Where they contradict the parent's own relations, the parent's win and the Transpiler notes the dropped relation (chapter 13).
4. Merge `TIES` pairs into one member. If the item has no `SUITS` on either side, the pair isn't really tied: the members stay separate, ordered by name, and chapter 13's warning applies.
5. **Topological sort**: repeatedly take the members nothing unplaced is above; when several are free, take the **alphabetically first** name. The position at which a member is placed is its level. Merged `TIES` members share one level.

Step 5 is what chapter 13's "name order" means: alphabetical order **where the relations leave a free choice**. Comparing unordered pairs by name one at a time can't be done, because it can form a cycle with the relations: with `C OVER A` and B unordered against both, pairwise name order gives A over B and B over C, while the relation puts C over A. The sort gives B, C, A.

The **conflict report** (chapter 13) prints these same tables, so what the report shows and what runs can't disagree.

A Plot started from several parents has a level in each parent's Staging table, worked out with each parent's relations. Nothing is shared between them.

## The Rank of a Giving

A Giving's `Rank` (the `Rank` of `regia_given`, chapter 29, and of `regia_standing`, chapter 30) is a **path of levels from the Root Plot down**:

```
Rank = Prefix ++ [SELF's level in G's Staging table, P's level in G's Playbook table]
```

for a Giving of Playbook P by Staging G, where `Prefix` is G's own place in the tree (*The prefix*, below).

Each step of the path is one of:

- a number `N`: the level for every item;
- `lv(N, [Item-M, …])`: level `N`, except `M` for the listed items. This only appears where the table has `ON` relations.

```
[1, lv(0, [when(insult_heard)-2]), 0]
```

reads: level 1 under the Root; then level 0 in the next table, except level 2 for `insult_heard`; then level 0.

### Comparing two Ranks

A Rank is always compared **for one item**, the one the competing plans react to:

1. Resolve each step for the item: `N` stays `N`; `lv(N, Overrides)` becomes the item's override, or `N`.
2. Compare the resulting lists of numbers step by step; the first difference decides, and lower wins.

Every path starts at the Root and goes down through the same tables. Wherever two paths first differ, both steps come from the same table, so one path is never a proper prefix of another one that also differs.

### The prefix

- The Root Director's file holds the initial belief `regia_rank_prefix([])`.
- When a parent starts a Subplot, it sends the child its prefix: `regia_start(Cast, Prefix)` (replacing chapter 31's `regia_start(Cast)`), where `Prefix` is the parent's own prefix plus one step, the child Plot's level in the parent's Staging table. The child stores it as `regia_rank_prefix(Prefix)`.
- Every `ASSIGN`, Role setup `ASSIGN` and standing Giving of a Plot appends the same constant pair of steps for its Playbook, generated inline. The Director builds the Rank with `.concat(Prefix, Suffix, Rank)`.
- Stagings of one Plot under one parent get equal prefixes (chapter 17). A Plot started from two parents gets a different prefix in each Staging, so its Givings carry different Ranks. Which is better is decided per item at selection time (below). Nothing about the second parent is worked out ahead of time.

### A Playbook given several times

The Agent keeps every `regia_given` belief (chapter 29) and **never stores a merged Rank**. For each item it competes on, a Playbook's Rank is the **best** of its Givings' Ranks for that item. Since `ON` relations make steps item-dependent, the best Giving for one item may not be the best for another. This is chapter 13's "a Playbook given twice keeps its best key".

## The plan annotation

Every plan compiled from a Playbook's Trigger Block carries one annotation in its label:

```
@regia_plan__17[regia_rank(nobleSocializing, when(insult_heard), 0), temper([sympathy(-0.5)])]
```

`regia_rank(Playbook, Item, Pos)` is the **fixed part** of the rank:

| Argument | Holds |
| --- | --- |
| `Playbook` | the Playbook's Jason name |
| `Item` | the plan's Trigger item, as written in `ON`: `when(e)`, `learned(f)`, `forgotten(f)`, `to(g)`, `dropped(g)`, `failed(g)` (Jason names). A Quota Trigger on `e` is `when(e)` |
| `Pos` | the Trigger Block's place among the Playbook's Trigger Blocks with the same Trigger, from 0 in text order |

- **Suits alternatives share one `Pos`**, so they all reach temper selection (chapter 13).
- **`GIVEN` siblings share their Trigger Block's `Pos`**. They already exclude each other through negated Contexts (chapter 06).
- Writing the item out means the Java never has to know how each Trigger kind is lowered to ASL.
- It replaces chapter 13's `playbook(Name)` annotation, which is retired. `regia.stop_playbook` (chapter 29) finds a Playbook's plans by `regia_rank`'s first argument.
- `temper` and `effects` (chapter 14) are emitted next to it unchanged.

## `selectOption` in Agents

The `regia-jason` Agents' class overrides `selectOption(options)`. Jason passes it only **applicable** options: the `regia_given` guard (chapter 29) has already removed the plans of Playbooks the Agent doesn't hold, and a Trigger Block whose `GIVEN`s all fail isn't there, which is chapter 13's fall-through.

1. **Infrastructure first.** If no option carries `regia_rank`, call `super.selectOption(options)` unchanged. Infrastructure triggers all start with `regia_`, which designer names can't (chapter 28), so an Infrastructure plan never competes with a Playbook plan.
2. **Best Rank.** For each option, read its Playbook's Rank for the option's `Item`: the best over that Playbook's `regia_given` beliefs. Keep only the options with the best Rank. An option with `regia_rank` but no `regia_given` for its Playbook means the guard was bypassed: drop it and leave a Trace entry.
3. **Best position inside each Playbook.** Among the options of one Playbook, keep only those with the lowest `Pos`. This is chapter 13's "first in the text wins", and it keeps a Playbook's later Trigger Blocks out of a `TIES` pool (chapter 13: each side brings its winning unlabelled Trigger Block).
4. **Hand over.** Sort what remains by Playbook name and call `VesnaAgent.selectOption` on that new list. VEsNA-Pro uses temper selection if at least one option carries `temper` (Suits alternatives, or a `TIES` pool); otherwise it takes the first, which is name order.

After step 2, options from different Playbooks remain only for a `TIES` pool, because step 4 of *Levels* gives every other pair different levels. So the name sort in step 4 only sets the order temper selection sees, and the fallback for a pool with no `temper`.

`VesnaAgent.selectOption` removes the option it picks from the list it gets. The list handed over is a fresh one, and the chosen option is removed from Jason's original list too, as Jason expects.

## Directors

A Director's competing plans all come from one Plot, and each plan has one fixed item. Its rank is therefore **resolved completely at compile time**:

```
@regia_plan__42[regia_phase(feast), regia_rank(0, 0)]
```

`regia_rank(Level, Pos)`:

- `Level` is the plan's level in the Plot's Director table for the plan's item: by default a Phase's plans are 0 and `DURING PLOT`'s are 1, and `DURING PLOT OVER DURING feast ON assassin_spotted` swaps them for that item (chapter 13). Only one Phase is current at a time, so the table has two members: the Phases together, and `DURING PLOT`.
- `Pos` is the Trigger Block's place in its `DURING` Block among those with the same Trigger, as for Playbooks.

`regia.DirectorAgent.selectOption` calls `super` if no option has `regia_rank`, else compares `[Level, Pos]` step by step and takes the first best. There is no runtime part, no prefix, and no temper: Directors have no Propensities (chapter 20) and no Labels (chapter 14).

The **ranking helper** shared by both classes (chapters 28 and 30) resolves a path for an item and compares two lists of numbers.

## Infrastructure state

Rows added to chapter 28's table:

| Concept | Held by | Functor and arguments |
| --- | --- | --- |
| The Staging's place in the tree | Director (the Root: initial belief; a Subplot: from `regia_start`) | `regia_rank_prefix(Path)` |

## Messages

Changed from chapter 31:

| Message | From → to | Meaning |
| --- | --- | --- |
| `achieve regia_start(Cast, Prefix)` | parent → new child | start the Staging with this cast, at this place in the tree |


## Trace entries

**Warnings**

- `T3201` A ranked option whose Playbook has no `regia_given`, so its guard was bypassed: the option is dropped.

## Not decided here

- The Trace entry for an option whose guard was bypassed: chapters 34 and 35.
- A plain-Jason agent class without VEsNA-Pro, where step 4 would be plain name order: not in 2.0 (chapter 28).
