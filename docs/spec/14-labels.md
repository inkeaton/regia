# Labels and Propensities

How a Trigger carries Labels, which Labels exist, and the Propensities they name. Decided in the ticket *Label syntax and mood Labels* (`.scratch/regia-2/issues/15-label-syntax.md`). It builds on chapters 01, 05, 06 and 13, and replaces `PRIORITY`, `TEMPER` and `EFFECTS` in primer ch.1 and ch.4. The facts about VEsNA-Pro used here are in the research note on branch `research/vesna-pro-temper` (file `research/vesna-pro-temper.md`). When a `SHIFTS` Label applies, and the Jason notes below, were settled in the ticket *Moods and Labels on VEsNA-Pro* (`.scratch/showcase-1-5/issues/20-moods-on-vesna.md`), with the facts of the research note *How Jason behaves where the translation waits* (branch `research/jason-facts`, question 6).

## Propensities

A **Propensity** is a named disposition of an Agent, used to choose between Plans and changed by running them. The word comes from VEsNA-Pro. There are two kinds:

- a **Trait** never changes during a run (VEsNA-Pro's personality);
- a **Mood** changes as the Agent runs Plans.

Both are declared in the Vocabulary:

```regia
TRAIT bravery
MOOD sympathy, aggressiveness
```

- Propensities take **no parameters**.
- They share the Program's one flat namespace and its one-kind-per-name rule (chapter 10, ADR 0006). `MOOD angry` and `FACT angry` is an error.
- They are declared at **file level only**, like `CUE` and `ACTION`. A Propensity belongs to the whole Agent, never to one Playbook.
- They may give an External name with `<external> AS <name>` (chapter 10), for when the Target calls them something else.
- Matching re-declarations merge (chapter 10).
- **Starting values come from Instancing**, per Agent kind or individual Agent, as `bravery AT 0.3` or `AT RANDOM(a, b)` drawn per Agent (chapter 21; VEsNA-Pro: the `temper(...)` parameter in the `.jcm`). A **Trait** lies in [0, 1], a **Mood** in [-1, 1].
- **A Propensity a kind gives no value is neutral**: 0.5 for a Trait, 0 for a Mood. No warning: an ordinary Agent is something a writer can mean. Revised in the ticket *Labels and the Selection function* (`.scratch/regia-revision/issues/13-labels-and-selection.md`), ADR 0033.
- **Propensities are not Facts.** In 2.0 a Context can't test them. Labels mention them, and the `SHIFT` Statement changes a Mood (below).

## Writing Labels

Labels are clauses of a Trigger's header, after its core (chapter 05, *The shape of a Trigger*). They may stand in any order with `FROM` or `BY`; tools write them last. Each one starts with `, KEYWORD`:

```regia
WHEN insult_heard, SUITS sympathy AT -0.5, SHIFTS aggressiveness BY 0.2:
    DO complain
```

- Labels can come **in any order**. Each Label appears **at most once** on a header.
- A Label naming several Propensities lists them with **`,`**: `SUITS sympathy AT -0.5, bravery AT 0.8`. After a `,`, a Propensity name continues the list and a Label keyword (or `FROM`, `BY`) starts the next clause (chapter 01). Propensities joined with `AND` are the retired spelling (`R14_12-retired-and-in-label`): `AND` is only the Context operator.
- Naming the same Propensity twice in one Label is an error.
- A long header wraps after any `,` (chapter 01):

  ```regia
  WHEN hates(?h) LEARNED, FROM ?teller,
          SUITS sympathy AT -0.5, bravery AT 0.8,
          SHIFTS aggressiveness BY 0.2:
      ...
  ```

- The same `,` shape is used by `, WEIGHT` on `OPTION` (chapter 09) and `, WITHOUT WAITING` (chapter 08). Weights are not Labels.

## The Labels

The set is **fixed by the language**. A Target can't add its own. 2.0 has exactly two:

| Label | Form | Names | Meaning |
|---|---|---|---|
| **Suits** | `SUITS p AT n[, …]` | Traits and Moods | The Plan best fits an Agent whose `p` is close to `n`. The Selection function uses it to choose (chapter 13). |
| **Shifts** | `SHIFTS m BY n[, …]` | Moods only | Running the Plan changes Mood `m` by `n` (signed). |

- **Values** are Number literals: in [0, 1] for a Trait after `SUITS`, in [-1, 1] for a Mood and for every `SHIFTS` amount. A value outside its range, an Expression or a Placeholder is an error. Labels are fixed when the Program is written, so they can't depend on a run.
- A name that isn't a declared Propensity is an error. So is `SHIFTS` naming a Trait.
- **Only `SUITS` affects which Plan runs.** `SHIFTS` never makes a Trigger Block an alternative.
- **A `SHIFTS` Label applies once, when the Plan is chosen**, before its first Statement runs, whether or not it was chosen among alternatives. It applies even if the Plan then fails at its first Statement. A Mood is kept within [-1, 1]: a Shift that would take it past a bound leaves it at that bound.

## Where Labels go

| Header | `SUITS` | `SHIFTS` |
|---|---|---|
| `WHEN …` / `TO …` in a Playbook | yes | yes |
| `GIVEN …` / `ELSE` under a Trigger | **error** | yes |
| A Director's Plans (in a Plot) | **error** | **error** |

- **On a Trigger**, Labels apply to every Plan under it: each `GIVEN` and the `ELSE` (chapter 06).
- **On a `GIVEN` or `ELSE`**, `SHIFTS` adds to the Trigger's own `SHIFTS` for that one Plan. The same Mood in both is an error.

  ```regia
  WHEN insult_heard, SHIFTS sympathy BY -0.1:
      GIVEN hates(host), SHIFTS aggressiveness BY 0.2: DO complain
      ELSE: DO toast(host)
  ```

  Complaining lowers sympathy and raises aggressiveness. Toasting only lowers sympathy.
- `SUITS` is never allowed on a `GIVEN` or `ELSE`, since `GIVEN` siblings never compete (chapter 13).
- **On a Director's Plans**, any Label is an error, and so is `SHIFT`: Directors have no Propensities (chapter 20).

## Suits alternatives

Chapter 13's rule, restated in terms of `SUITS`:

- When one Trigger Block for a Trigger in a Playbook carries `SUITS`, **every** Trigger Block for that Trigger in the Playbook is a **Suits alternative**. The Selection function picks one of those whose Context holds.
- **An unlabelled alternative is neutral.** It competes as if it suited every Propensity the labelled alternatives name at the neutral value: 0.5 for a Trait, 0 for a Mood. It is the Plan for an Agent with nothing particular about it. Mixing labelled and unlabelled Blocks is allowed; a `SHIFTS` Label doesn't make a Block labelled.
- **`TIES` pools** (chapter 13) work the same way: an unlabelled candidate in a pool with at least one `SUITS` is neutral, so labelling one side of a tie is enough.
- How the Selection function weighs the fit belongs to the Target. VEsNA-Pro's is in *ASL mapping notes*.

Revised in the ticket *Labels and the Selection function*, ADR 0033.

## The `SHIFT` Statement

`SHIFT m BY n` changes Mood `m` by `n` when the Statement runs. Several Moods are listed with `,`: `SHIFT sympathy BY 0.1, anger BY -0.2`.

```regia
TO have_dinner:
    DO eat(?dish)
    IF tasty(?dish):
        SHIFT sympathy BY 0.1
```

- It is a Basic Action (chapter 08). It names **Moods only**; a Trait is an error.
- `n` is any Number Expression (chapter 04), Placeholders included: unlike a Label, it is worked out at run time. `SHIFT sympathy BY ?amount * 0.1`.
- It applies **at once**, before the next Statement, whatever happens to the Plan afterwards. The Mood is kept within [-1, 1], as for a Label.
- It is allowed in Playbooks only. A Director has no Propensities (chapter 20).
- The `SHIFTS` Label stays. It is fixed and part of the Plan's header, so it can be read without running the Body. `SHIFT` is for a change that depends on what happens in the Body.
- **Every Mood change is in the Trace**, as a `mood` entry: from a `SHIFT` Statement when it runs, and from a `SHIFTS` Label when the Plan is chosen (chapter 34). A `SUITS` choice records in the winner's `plan` entry the fit of each alternative, so why it was chosen can be read.

## Targets without Labels

A Target that doesn't support a Label **ignores** it, with **one warning per Program per Label** ("`SUITS` has no effect on Target X"). The Program still compiles. Ignoring `SUITS` means Suits alternatives fall back to text order and `TIES` to name order (chapter 13). Ignoring `SHIFTS` means only `SHIFT` Statements change Moods.

## Transpiler checks

**Errors**

- `R14_01-unknown-or-repeated-label` An unknown Label keyword, or a Label repeated on one header.
- `R14_02-repeated-propensity` A Propensity named twice in one Label, or in both a Trigger's `SHIFTS` and a `GIVEN`'s.
- `R14_03-undeclared-label-name` A name in `SUITS` that isn't a declared Propensity, or a name in `SHIFTS` or `SHIFT` that isn't a declared Mood.
- `R14_04-wrong-label-value` A Label value that isn't a Number literal, or that lies outside its range ([0, 1] for a Trait in `SUITS`, [-1, 1] otherwise).
- `R14_05-misplaced-suits` `SUITS` on a `GIVEN` or `ELSE`.
- `R14_06-label-in-director` Any Label on a Director's Plan, or `SHIFT` in a Director's Body.
- `R14_07-local-propensity` A `TRAIT` or `MOOD` declared inside a `PLAYBOOK` or `PLOT`.
- `R14_11-repeated-mood-in-shift` The same Mood named twice in one `SHIFT`.
- `R14_12-retired-and-in-label` Propensities in a `SUITS` or `SHIFTS` Label, or Moods in a `SHIFT`, joined with the retired `AND` (hint: list them with `,`).

**Warnings**

- `R14_08-unsupported-label` A Label the Target doesn't support (once per Program per Label).
- `R14_09-unused-propensity` A declared Propensity that no Label and no `SHIFT` names. Absence check (chapter 23).
- `R14_10-inapplicable-shifts-label` Retired: a `SHIFTS` Label always applies when its Plan is chosen (*Moods and Labels on VEsNA-Pro*).

`R13_04-mixed-suits-trigger-blocks` and `R13_09-unlabelled-ties-candidate` (mixing labelled and unlabelled candidates) are retired, ADR 0033. `R14_10-inapplicable-shifts-label` (a `SHIFTS` Label the Target can never apply) is retired: a `SHIFTS` Label now always applies when its Plan is chosen (*Moods and Labels on VEsNA-Pro*).

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## Not in 2.0

Map: *Not yet specified*. Deferred in the ticket *Labels and the Selection function*, ADR 0033.

- **The fit defined by the language** (for instance the mean distance over the Propensities an alternative names), scored by the Infrastructure instead of the Target. Today alternatives naming different sets of Propensities are compared however the Target weighs them.
- **Testing Propensities in a Context** (`GIVEN aggressiveness > 0.5`).
- Named value levels (`SUITS sympathy AT LOW`), alongside named Weight levels.
- Labels from other Targets.

## ASL mapping notes

For *The full ASL mapping* to pick up. VEsNA-Pro facts are from the research notes above, as of upstream commit `3f857f5`. The changes Regia needs in VEsNA-Pro are collected in *Changes to VEsNA-Pro for Regia* (`.scratch/implementation/vesna-pro-for-regia.md`).

- **Labels stay plan annotations**, so the emitted ASL stays plain AgentSpeak that VEsNA-Pro already reads. `SUITS p AT a, q AT b` becomes the plan annotation `temper([p(a), q(b)])`. `SHIFTS m BY d` becomes `effects([m(d)])`. A `GIVEN`'s `SHIFTS` merges into its own plan's `effects` list. External names replace Regia names.
- **Moods are in [-1, 1] in VEsNA-Pro too.** `Temper` takes Moods, `temper([…])` targets and `effects` amounts in [-1, 1], and Traits in [0, 1]. A negative Mood or target needs no translation: `most_similar` compares |Mood − target| (research `research/jason-facts`, question 6).
- **A neutral alternative** gets `temper([…])` naming every Propensity that a labelled candidate of its competition names, at 0.5 for a Trait and 0 for a Mood (`m(0)[mood]`). Its competition is the Trigger's Blocks in its Playbook, or the `TIES` pool it is in. It may get several, one per pool: the plan carries the union.
- **Propensity values** go into the Agent's `.jcm` as `temper(t1(v), …, m1(v)[mood], …)`, with Moods tagged `[mood]`. The `strategy` parameter (`most_similar` or `random`) must be written whenever `temper` is, or VEsNA-Pro's `Temper` constructor throws. It is the `strategy` setting of Instancing's `TARGET jason` group, defaulting to `most_similar` (chapter 21).
- **Emitting as little as possible.** Most Programs have no Propensities, and VEsNA-Pro runs an Agent without a `temper` safely (it takes the first option it is given, which `selectOption` has already ordered, chapter 32, and ignores `temper` annotations; `RegiaAgent` then applies no `effects`). So:
  1. A Program where no Label and no `SHIFT` names a Propensity emits no `temper` or `effects` annotation and no `temper` or `strategy` parameter.
  2. A kind gets `temper` and `strategy` in its `.jcm` only if a Playbook its Roles can be given (the reach that decides which Role file holds a Playbook, chapters 28 and 29, `MAPPING ?who` included: in the showcase `king` gets one, because `Duelling` names `bravery`) names a Propensity in a Label or a `SHIFT`. Its `temper` lists exactly those Propensities, each with the kind's value or the neutral one. A Mood must be listed to be shifted: `Temper.shift` skips a Mood the Agent doesn't hold.
  3. A neutral `temper` is emitted only for an unlabelled candidate whose competition has at least one `SUITS`.
  4. `effects` is emitted only where a `SHIFTS` Label is written.
- **`regia.RegiaAgent.selectOption` applies a `SHIFTS` Label.** Once an agent class overrides `selectOption`, Jason calls it exactly once for every event that has applicable plans, even a single one (`TransitionSystem`, rule *SelAppl*). After choosing, it reads the chosen plan's `effects` and shifts each Mood through `Temper.shift`, then writes the plan's `plan` entry and one `mood` entry per Mood, `plan:` that entry (chapters 32 and 35). So a `SHIFTS` applies once, when the Plan is chosen, whether it was contested or not: a lone `FAILED` Plan, a `GIVEN` sibling, a Suits alternative whose rivals' Contexts failed. The same call computes each candidate's fit with `Temper.computeWeight` for the winner's `plan` entry (chapter 35), before handing Suits alternatives and `TIES` pools to temper selection (chapter 32).
- **Temper never schedules intentions.** VEsNA-Pro's `selectIntention` uses Moods to choose which running intention takes the next step, and applies the chosen plan's `effects` on every step it picks it. Under `most_similar` a plan with no `temper` scores 0, so every unlabelled intention, the generated `regia_*` plans included, would step before any labelled one, and `effects` would apply many times. `regia.RegiaAgent.selectIntention` therefore takes Jason's default, `intentions.poll()`: running Plans step in turn, and Moods only choose among a Trigger's alternatives (*Only `SUITS` affects which Plan runs*, above).
- **`SHIFT m BY e`** becomes `regia.shift([m(E)])` after `E` is computed, a `regia-jason` internal action that shifts each Mood through `Temper.shift` and writes the `mood` entry. A Statement's amount is known only at run time, so it can't be an annotation.
- **Moods live in `Temper`**, which is the Agent's own state in VEsNA-Pro, not `regia-jason` plumbing. No belief mirrors them: a Context can't read Propensities, and the Trace shows their values (the `TEMPER` `cast` entry, chapter 36, and every `mood` entry).
- **What Regia needs from VEsNA-Pro**, as an upstream patch: `VesnaAgent.getTemper()`, since the field is private and a subclass can't reach it; `Temper.shift(mood, delta)`, which keeps the Mood within [-1, 1] (today a Mood pushed below -1 is set to 0) and skips a Mood the Agent doesn't hold; and `computeWeight` returning the `most_similar` score under both strategies, with `random` drawing by weights that fall as that score rises. Today `random` weighs by Σ Mood × target, which goes wrong for negative values, and its draw is wrong for fractional or negative weights. No hook in `Temper` is needed: `RegiaAgent` writes the Trace.
- **Known VEsNA-Pro behaviour** that the language doesn't promise:
  - Scores under `most_similar` are the sum of |agent − plan| over the plan's listed Propensities, unnormalised; the lowest wins, and on a tie the first option. A Propensity the Agent lacks adds 0. A plan without `temper` scores 0, a perfect fit, which is why neutral alternatives get one.
  - Leaving out `strategy` throws (above). The 1.0 vendored copy never runs temper-based intention selection.
- Spec 13's ranking runs in `selectOption` before temper selection, so VEsNA-Pro only ever compares candidates of equal rank.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025). The `BY` of `SHIFTS` and `SHIFT` is an amount: chapter 01's closed exception, since every other `BY` names who did it (ADR 0044).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- Directors have no Propensities (chapter 20). Plot moods (pacing, tension) are with *Richer Propensities*.
- How Labels and Propensities map on Targets other than Jason+VEsNA: *Supporting multiple Targets*.
