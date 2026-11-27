# Plan selection

Which Plan runs when several could react to the same Trigger on one Agent: inside a Playbook, between Playbooks, between a Plot and its Subplots, and in a Director. Decided in the ticket *Priority model* (`.scratch/regia-2/issues/14-priority-model.md`). It builds on chapters 03, 05, 06 and 11, and replaces `PRIORITY` in primer ch.2, ch.4 and ch.5. The proposal `docs/agents/Regia Plan Precedence and Composition (Proposal).md` was input: its composition-level relations, fall-through and conflict report are kept; its `STORY` unit, layers, numeric tie-breaks, handler labels and `WITH`/`PARALLEL` are not (see *Not in 2.0*). Why precedence is declared where Playbooks are put together is recorded in `docs/adr/0008-precedence-is-declared-where-playbooks-are-put-together.md`. Revised in the ticket *Which Plan runs* (`.scratch/regia-revision/issues/12-which-plan-runs.md`): falling through is one rule for every Trigger, a default gives way where it would close a cycle (`docs/adr/0032-a-default-gives-way-to-what-is-written.md`), and `SELF` has one meaning.

Labels and Propensities (`SUITS`, `SHIFTS`, `TRAIT`, `MOOD`) are defined in chapter 14 (`14-labels.md`).

## What this chapter decides

A Trigger arriving at an Agent raises four separate questions. 2.0 lets designers influence only the second:

| Question | 2.0 |
|---|---|
| Several things happened: which is handled first? | In arrival order. Fixed, no construct. |
| Several Plans could react to this Trigger: which runs? | **This chapter.** |
| A Plan is running: can a more important one interrupt it? | No. Running Plans take turns, one step at a time. Fixed, no construct. |
| Two running Plans do things that can't happen together | Not handled in 2.0. |

- **One Plan runs per Trigger on an Agent.** If two Playbooks react to the same Cue, only one of them does. Several Playbooks reacting to one Trigger is a future feature.
- The rules are the same for every Trigger kind: Cues, `LEARNED`, `FORGOTTEN`, `DROPPED`, `FAILED` and `TO` recipes, in Playbooks and in Plots.
- Choosing **among the matches of one Context** ("the guest I hate most") is a different question, decided in chapter 26 (`26-match-selection.md`).
- **The Trace says which mechanism decided.** When a Plan had rivals, its `plan` entry names them and how it won: `SUITS`, `PRECEDENCE`, name order or a default giving way (chapter 34). A `GIVEN` or `ELSE` needs no mention: the entry already shows which one ran.

## Candidates

The unit that competes is the **Trigger Block**: one `WHEN` or `TO` header with everything under it. Its `GIVEN` siblings never compete with each other; the first that holds wins (chapter 06).

A Trigger Block is a **candidate** for a Trigger when:

- its Playbook is currently given to the Agent (or, in a Director, its `DURING` Block is active), and
- its Trigger matches, Values and `FROM` included (chapters 03, 05; a Quota Trigger never matches the plain Cue, chapter 18), and
- it can run: one of its `GIVEN`s holds, or it has an `ELSE`, or it has no Context.

A Trigger Block whose `GIVEN`s all fail and that has no `ELSE` is **not a candidate**, and the Trigger **falls through** to the next candidate in order. This lets a story Playbook take over only when its own Context holds:

```regia
PLAYBOOK Duelling:
    WHEN insult_heard(?s):
        GIVEN rival(?s):
            DO draw_sword
        # no ELSE: any other insult falls through to the everyday reaction
```

Falling through is the same for every Trigger kind, `TO` recipes included: a recipe whose `GIVEN`s all fail and that has no `ELSE` passes the Goal to the next recipe in the order, just as a Cue passes to the next `WHEN`. Only the end of the order differs. If no candidate is left, a Cue or Fact change is dropped (chapter 07), and a Goal fails because no Plan applies (chapter 11).

A Trigger Block with an `ELSE`, or with no Context, always applies, so it stops the Trigger: nothing ranked after it ever sees it. Whether a Playbook stops a Trigger or lets it pass is written in that Playbook, by its author, who can't see what comes after it. This is deliberate. The conflict report marks such a Block as a **full stop** and lists the candidates below it as unreachable, so the effect of adding an `ELSE` can be read in one place. There is no warning: stopping the Trigger is often what the Playbook means, and the Transpiler can't tell which Playbooks are given at the same time.

## Order

The candidates are ranked, and the first one runs:

1. **Precedence**: the order of the Playbooks the candidates belong to, as described below.
2. **The Selection function**: only among candidates that precedence leaves deliberately tied (*Propensities*, below).
3. **Name order**: the last resort, for competitions nobody ordered. It always comes with a warning.

The order never depends on file order between files, include order, or the order Playbooks were loaded or given.

### Inside a Playbook

**First in the text wins**, the same reading rule as `GIVEN` siblings:

```regia
PLAYBOOK NobleSocializing:
    WHEN insult_heard(host):     # wins when the host speaks
        DO complain
    WHEN insult_heard(?speaker): # everyone else
        DO frown
```

The Transpiler warns about a Trigger Block that can never run because an earlier one always catches its Trigger first. The exception is Suits alternatives (*Propensities*, below).

### Who orders what

Each author orders only what they can see:

- **A Playbook never names another Playbook.** It can't say "I beat Drunkard". Playbooks stay independent of each other and of any Plot.
- **A Plot orders the Playbooks it gives out**, by name.
- **A Plot orders its direct Subplots against itself and against each other.** It names a Subplot by its Plot name (it writes that name in `START SUBPLOT` anyway) and itself as `SELF`. It never names a Subplot's Playbooks.
- **`SELF` is always a Plot's own Playbooks and its Director's own Plans**, never its Subplots, in a parent and in a Subplot alike. When a Subplot writes `PARENT OVER SELF`, its whole subtree moves with it, because of the next rule, not because `SELF` means more there.
- **A Subplot counts together with everything it starts.** When RoyalBanquet says `HonorDuel OVER SELF`, every Playbook given by HonorDuel or by any Plot HonorDuel starts is ranked above RoyalBanquet's own. How HonorDuel and its own Subplots compare is HonorDuel's business. Nobody ever names a grandchild.
- **A Subplot may refer to the Plot that started it only as `PARENT`**, since a reusable Subplot can't know its name. If parent and Subplot contradict each other, **the parent wins**, and the Transpiler warns about the dropped relation (`R13_11-overridden-subplot-relation`): something the Subplot's author wrote has no effect. A `PARENT` relation is a statement about the Subplot's own Plans ("on `scandal`, I come after whoever started me"), which its author can see. Under a parent with no Plans for that item it orders nothing. `PARENT` is the parent's `SELF`, so a Subplot can place itself against its parent and never against its siblings: that order is the parent's business.
- **There are no independent Plots.** Every Plot is the Root Plot or a Subplot below it (chapter 21), so every two Plots have a common ancestor that orders them.

The result is a hierarchy: first the order between Plots (and their Subplots), then the order of Playbooks inside the winning Plot.

### Defaults

With nothing declared:

| Competition | Winner | The designer hears |
|---|---|---|
| Two Trigger Blocks in one Playbook | the first in the text | a warning only if one can never run |
| A Subplot and its parent | **the Subplot** | a line in the conflict report |
| A Phase's Plan and a `DURING PLOT` Plan (Director) | **the Phase** | a warning only if the Phase's Trigger Block always catches the Trigger |
| One Playbook given by two Plots | no competition | nothing |
| Two Playbooks given by the same Plot | name order | a **warning** |
| Two sibling Subplots | name order | a **warning** |

- **A Subplot beats its parent**: it is the more specific part of the story. Since every story hangs under the Root Plot, "the story beats everyday behaviour" needs no declaration.
- **A Phase beats `DURING PLOT`** for the same reason: it is the more specific state.
- **A default gives way to what is written.** The written relations of a Plot, its Subplots' `PARENT` relations included, are placed first. Each default is then added only if it doesn't contradict what the written relations already imply, directly or through a chain. A default is never part of a cycle: in `RoyalBanquet`, `PARENT OVER SELF ON scandal` in `HonorDuel` and `HonorDuel OVER Poisoning` already put the banquet above `Poisoning` on `scandal`, so the default `Poisoning OVER SELF` is left out for that item, and the conflict report says so. Nothing written is ignored, so it is a line of the report, not a Diagnostic. A cycle made only of written relations is still an error (`R13_01-precedence-cycle`). Why: ADR 0032.
- **A Playbook given by two Plots** is still one Playbook with one set of Trigger Blocks. Against other Playbooks it ranks at the **best** of its positions.
- **Name order** is the Playbook's or Plot's name, alphabetically, wherever the relations leave a free choice: the members of a Plot are placed one at a time, and when several could come next, the alphabetically first goes. Comparing unordered pairs by name one at a time isn't used, since it can form a cycle with the relations (chapter 32). It is deliberately arbitrary, and the warning names the pair and suggests the relation to add. A rename can therefore change behaviour. This is kept: every order a rename can't change (file order, text order across files, load order) is just as invisible and changes when files are reorganised, an error would demand relations for pairs that never meet (ADR 0008), and a random pick would make runs irreproducible. A rename in the Visual Editor that flips an unordered pair should say so (left to the ticket *The Visual Editor*, `.scratch/regia-revision/issues/18-visual-editor.md`).

Warnings only appear for Playbooks that share a Trigger. A Program whose Playbooks react to different things gets none. The Transpiler knows which Playbooks an Agent *can* hold, not which are given at the same time, so two Playbooks that are never given together (one in `reception`, one in `feast`) can still be warned about.

## `PRECEDENCE`

A Plot writes its relations in one `PRECEDENCE:` Block, next to its `ROLE` and `PHASE` declarations:

```regia
PLOT RoyalBanquet:
    ROLE Host
    ROLE Guest
    PHASE reception INITIAL
    PHASE feast

    PRECEDENCE:
        Brawling OVER NobleSocializing
        Brawling OVER Drunkard ON insult_heard
        Drunkard TIES NobleSocializing ON digestion_check
        HonorDuel OVER SELF
        Rematch OVER Wedding
        DURING PLOT OVER DURING feast ON assassin_spotted

    DURING reception:
        ...
```

```regia
PLOT HonorDuel:
    PRECEDENCE:
        PARENT OVER SELF      # this duel yields to whoever started it
```

| Relation | Meaning |
|---|---|
| `A OVER B` | Every candidate of A ranks above every candidate of B. |
| `A OVER B ON item` | The same, only for Triggers on `item`. Elsewhere A and B stay unordered. |
| `A TIES B` / `A TIES B ON item` | A and B are equal on purpose: the Selection function chooses between their candidates (*Propensities*, below). |

- `A` and `B` name:
  - Playbooks this Plot gives out;
  - its direct Subplots, by Plot name, or `SELF` (its own Playbooks and Director Plans), in either order;
  - `PARENT`, in a Plot started as a Subplot;
  - `DURING PLOT` and `DURING <phase>`, for the Director's own Plans.
- `ON` takes a Trigger's item, with its kind word if it has one: `ON insult_heard`, `ON hates LEARNED`, `ON dinner` (a `TO` recipe), `ON dinner FAILED`.
- **Relations are static.** They hold for the Plot's whole life, in every Phase. A relation only matters while both sides are given, so "Brawling beats NobleSocializing during the feast" follows from when each is given.
- **`OVER` is not transitive across Plots.** Each Plot's relations order only what that Plot names. Inside one Plot, relations combine: `A OVER B` and `B OVER C` put A above C.
- **`TIES` joins only Playbooks given by the same Plot.** It can't join Subplots, `SELF`, `PARENT` or Phases.
- Numeric priorities (`PRIORITY 5`) don't exist. An order is always written as a relation by someone who can see both sides.

## Propensities

The **Selection function** is the Target's way of choosing among equally ranked Plans by the Agent's Propensities, its Traits and Moods (VEsNA-Pro's temper selection today). Propensities decide only where a designer chose to let them decide, in exactly two places.

### Suits alternatives inside a Playbook

When a Trigger Block in a Playbook carries a `SUITS` Label, every Trigger Block in that Playbook with the same Trigger is a **Suits alternative**. They are different Plans even when their Contexts are identical, and none shadows another. Every alternative whose Context holds goes to the Selection function, which picks one:

```regia
PLAYBOOK NobleSocializing:
    WHEN insult_heard, SUITS sympathy AT -0.5: DO complain
    WHEN insult_heard, SUITS sympathy AT 0.5:  DO toast(host)
```

- **An unlabelled alternative is neutral** (chapter 14, ADR 0033): it competes as if it suited the Propensities the others name at 0.5 for a Trait and 0 for a Mood. With no `SUITS` on any of them, the Trigger Blocks are not alternatives and the first in the text wins. A `SHIFTS` Label doesn't count.
- The "can never run" warning doesn't apply between alternatives: they are meant to overlap.
- Alternatives are always separate Trigger Blocks. `GIVEN` siblings are never alternatives, and `SUITS` on a `GIVEN` is an error (chapter 14).

### `TIES` between Playbooks

`A TIES B` pools the two Playbooks' candidates into **one** Selection: each side's Suits alternatives that hold, and each side's winning Trigger Block where it has no alternatives. If any candidate in the pool carries `SUITS`, the unlabelled ones are neutral, as inside a Playbook (chapter 14), so labelling one side is enough. A Plot can't write Labels for the Playbooks it ties: only a Playbook's author can say what its Plans suit.

- `TIES` also marks the competition as intended, so name order's warning doesn't fire.
- `TIES` between Playbooks already ordered by `OVER` is an error.
- **`TIES` with no `SUITS`** on any pooled candidate has nothing to choose by. It falls back to name order with a warning ("no `SUITS` on these Trigger Blocks: use `OVER`, or add `SUITS`"). Random variety is written with `RANDOMLY` (chapter 09).

### What the language promises

- The Selection function picks **exactly one** of the candidates it is given, and it is only given candidates of **equal rank**: Propensities never override precedence.
- How it scores (Traits, current Moods, how a fit over several Propensities is weighed, and when `SHIFTS` changes the Moods) belongs to the Target (ADR 0033). A run that uses it is reproducible only given the same Mood history.
- **A Target without a Selection function** resolves Suits alternatives by text order and `TIES` by name order, with **one warning per Program** (chapter 14: an unsupported Label is ignored with one warning per Program per Label).
- A Program with no `SUITS` Labels never uses the Selection function.

## Instancing

Instancing orders nothing. A Program has exactly one Root Plot and Instancing never starts a Plot (chapter 21), so stories that run side by side are Subplots of the Root Plot, ordered by its `PRECEDENCE`. All precedence is written in Regia source.

## Transpiler checks

**Errors**

- `R13_01-precedence-cycle` A cycle in one Plot's written relations, its Subplots' `PARENT` relations included (the message prints the cycle). Defaults are never part of one.
- `R13_02-misused-ties` `TIES` between Playbooks already ordered by `OVER`, or `TIES` on anything but Playbooks.
- `R13_03-relation-to-absent-item` A relation naming a Playbook the Plot never gives out, a Plot it never starts, a Phase it doesn't have, or `PARENT` in a Plot that is never started as a Subplot. Its *never* parts are an absence check (chapter 23).
- `R13_04-mixed-suits-trigger-blocks` Retired (ADR 0033): Trigger Blocks with and without `SUITS` may be mixed.

**Warnings**

- `R13_05-competition-ordered-by-name` A competition ordered only by name.
- `R13_06-relation-without-shared-trigger` A relation that never matters, because its two sides share no Trigger (catches typos and stale relations after a Playbook changes). Absence check (chapter 23).
- `R13_07-unreachable-trigger-block` A Trigger Block that can never run (inside a Playbook, or a `DURING PLOT` Plan fully shadowed by a Phase's).
- `R13_08-ties-without-suits` `TIES` with no `SUITS` to choose by.
- `R13_09-unlabelled-ties-candidate` Retired (ADR 0033): an unlabelled candidate in a mixed `TIES` pool is neutral.
- `R13_10-suits-without-selection-function` `SUITS` on a Target without a Selection function (once per Program).
- `R13_11-overridden-subplot-relation` A Subplot's relation dropped because its parent says the opposite. (It was a note; there are no notes any more, chapter 23.)
- `R13_12-default-left-out` Retired: a default left out is a line of the conflict report.

**Conflict report.** `regia explain <entry> precedence` (chapter 23) lists, per Role and Trigger, the competing Trigger Blocks in the order they rank and why (relation, default, default left out, Selection function, or name). A Trigger Block that always applies (an `ELSE`, or no Context) is marked as a full stop, and the candidates below it as unreachable:

```
Guest, insult_heard:
  1. Duelling           (HonorDuel over RoyalBanquet: default, Subplot over parent)
  2. NobleSocializing   (RoyalBanquet)
Guest, digestion_check:
  1. Drunkard, NobleSocializing   (TIES -> Selection function)
Guest, scandal:
  default left out: Poisoning over RoyalBanquet (contradicts PARENT OVER SELF in HonorDuel, HonorDuel OVER Poisoning)
warning: Guest, food_served: Feasting and Gossip are ordered by name only; add a relation to RoyalBanquet's PRECEDENCE
```

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## Not in 2.0

Map: *Not yet specified*.

- **Several Playbooks reacting to one Trigger**, in order or concurrently (the proposal's `WITH`/`PARALLEL`). In Jason this needs a generated dispatcher that starts one intention per Playbook.
- **Pre-emption** and **Actions that can't run together**: a model of what an Agent's body can do at once, which the language doesn't have. Two Plans of one Agent racing (a Body's `IF` and a `DROP` from another Plan) is the writer's to arrange, and the Trace shows who won.
- **A Phase Plan that adds to `DURING PLOT`'s** instead of replacing it. What both should do goes in a recipe both pursue, or stays in `DURING PLOT` alone.
- **Layers**: named, cross-cutting precedence categories ("every safety reaction beats every social one") ordered once for the whole Program.
- **Naming single Trigger Blocks** in relations.
- **`TIES` between Plots.**
- **Knowing which Playbooks are given at the same time**, which would remove false warnings and could make unordered competition an error.

## ASL mapping notes

Settled in chapter 32 (`32-jason-precedence.md`):

- **The order never comes from the plan library.** Jason's default picks the first applicable plan in plan-library order, which follows include order. Precedence is enforced explicitly instead, so loading Playbooks at runtime and reorganising files can't change behaviour.
- **Rank key.** When a Director gives a Playbook, it passes a rank key: the path of positions from the top down (starting at the Root Plot: the position of each Subplot among its siblings and `SELF`, then the Playbook's position inside its Plot). The Agent stores it with the Playbook, as the `Rank` of its `regia_given` record (chapter 29). A Playbook given twice keeps its best key. Chapter 32 makes each step a level worked out at compile time, with per-item overrides for `ON` relations.
- **Annotations.** Each Trigger Block's plans carry `regia_rank(Playbook, Item, Pos)` (chapter 32), which replaces the `playbook(Name)` proposed by the Jason dynamic-plans research. `priority(N)` is no longer emitted.
- **Selection** happens in `selectOption`, in the `regia-jason` agent class that extends VEsNA-Pro's (chapter 28), which sees every candidate plan: keep the applicable options with the best key (compared position by position); if several remain and they are Suits alternatives or a `TIES` pool, hand them to VEsNA-Pro's temper selection; then break ties by Playbook name. Inside a Playbook, an unlabelled Trigger Block's position in the text is part of the key, so text order holds without relying on plan order.
- **Suits alternatives** are separate plans with their `temper` annotations (a neutral one for an unlabelled alternative, chapter 14) and no negated sibling Contexts between them, so `selectOption` sees them all. `GIVEN` siblings keep chapter 06's negated Contexts and carry no `temper` (a `GIVEN`'s own `SHIFTS` becomes `effects` on its plan only).
- A Plot started from two different parents gets its prefix from whichever parent started each Staging, and the best Giving is taken per item at selection time (chapter 32). Other Targets need only "compare keys, then the Selection function, then names".

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025). What it says about Quota Triggers has nothing to apply to in 1.5.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- How Subplots are started and identified: chapter 17 (`17-subplots.md`). Stagings of one Subplot under one parent share its position; a Plot under two parents keeps its best rank.
- Directors have no Propensities (chapter 20).
- Choosing among a Context's matches: chapter 26 (`26-match-selection.md`).
