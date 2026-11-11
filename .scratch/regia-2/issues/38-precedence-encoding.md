# Precedence encoding in ASL

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 34, 35

## Question

How is precedence (spec 13) encoded in Jason? Decide the rank key's encoding, how a Plot's position is computed when it is started from two parents, and how `selectOption` compares keys.

## Answer

Spec chapter: `docs/spec/32-jason-precedence.md`, checked against VEsNA-Pro's `VesnaAgent.selectOption`. Chapters 13, 17 and 28–31 point to it; chapter 31's `regia_start` gains a `Prefix` argument; `playbook(P)` is retired.

- **Levels at compile time**: per Plot, a Staging table (Subplots and `SELF`, with children's `PARENT` relations folded in, parent winning) and a Playbook table, each worked out per item named in an `ON` and once for the rest. Defaults go in as relations; `TIES` share a level (only if `SUITS` is on either side for that item); a topological sort takes the alphabetically first free member. Lower wins. The conflict report prints the same tables. Chapter 13's "name order" now means alphabetical where the sort has a free choice, since pairwise name order can cycle with relations.
- **Rank**: a path of levels from the Root, `Prefix ++ [SELF's level in G, P's level in G]`. A step is `N` or `lv(N, [Item-M, …])`. It is compared for one item, step by step.
- **Two parents**: the parent sends `regia_start(Cast, Prefix)`, stored as `regia_rank_prefix(Path)` (Root: `[]` as an initial belief). Each Staging has its own prefix; a Playbook given several times keeps every Giving, and the best per item is taken at selection time, never stored merged.
- **Annotation**: `regia_rank(Playbook, Item, Pos)` on every Playbook plan, with `Item` as `when(e)`, `learned(f)`, `forgotten(f)`, `to(g)`, `dropped(g)`, `failed(g)`; Suits alternatives and `GIVEN` siblings share a `Pos`. It replaces `playbook(P)`; `regia.stop_playbook` reads it.
- **`selectOption`**: no `regia_rank` → `super`; keep the best Rank for the item (best over the Playbook's Givings; a ranked option with no Giving is dropped and traced); keep each Playbook's lowest `Pos`; sort by Playbook name and hand a fresh list to `VesnaAgent.selectOption` (temper if any `temper`, else first).
- **Directors**: `regia_rank(Level, Pos)` resolved at compile time (Phases 0, `DURING PLOT` 1, `ON` swaps per item); `regia.DirectorAgent` compares `[Level, Pos]`. A shared helper resolves and compares paths.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *ASL infrastructure layout* (34): selection lives in the `regia-jason` agent class, which extends VEsNA-Pro's and follows its annotation approach (spec 28). The user's direction: a new ranking annotation on plans. It can carry only the fixed part of a rank (Playbook, Trigger Block position); the Giving's part is the `regia_given` belief. Decide the annotation's shape here.
- From *Giving and taking Playbooks at runtime* (35): the rank is the `Rank` argument of `regia_given(Playbook, Staging, Director, Target, Rank, Bindings)`, sent in `regia_give`. Combine ranks across several `regia_given` beliefs of one Playbook (chapter 29).
- From *Director runtime in ASL* (36): `regia_standing(Seq, Playbook, Role, Rank, Bindings)` stores the Rank to replay. Directors run `regia.DirectorAgent` and rank Phase over `DURING PLOT` through a helper shared with the Agents' class (chapter 30).
- From *Stagings and Subplots runtime in ASL* (37): `regia_given` is now `regia_given(Playbook, Director, Target, Rank, Bindings)` and `regia_give(P, Target, Rank, Bindings)`: the Director's name is the Staging (chapter 31). A Subplot's rank is its position under its parent; the child knows its parent as `regia_parent(D)` and its Plot as `regia_staging(Plot)`.
