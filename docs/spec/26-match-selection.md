# Match selection

What a Plan does with the several matches of one condition: picking one on purpose, running a Block for every match, and counting matches. Decided in the ticket *Match selection over a Context* (`.scratch/regia-2/issues/32-match-selection.md`). It builds on chapters 03, 04, 06, 08 and 09, and answers the questions those chapters (and 13, 18, 19) left to *Match selection*.

## Matches

A **Match** is one way a condition holds: a Value for each of its blanks, named Placeholders and `?` alike (chapter 03). `hates(?x) AND is_nearby(?x)` with two hated Agents nearby has two Matches.

Matches are always **distinct**. If two branches of an `OR` produce the same Values, that is one Match, not two.

## The default: one Match, unspecified

A plain condition keeps the rule of chapter 03: when several Matches satisfy it, the Agent uses **one**, and **the language does not say which**. A Plan must not rely on any order, even though Jason always gives the same answer.

This is deliberate. A plain `GIVEN` stays as cheap as the Target's own test, and choosing a Match is something the author writes when it matters.

## Picks

A **Pick** is a trailing clause on a condition's header that chooses which Match is used:

```regia
WHEN bored:
    GIVEN guest(?g), RANDOMLY:
        TELL ?g joke

WHEN insulted:
    GIVEN hates(?x, ?how_much), HIGHEST ?how_much:
        ASK ?x TO duel

WHEN tired:
    IF friend(?f, ?distance), LOWEST ?distance, RANDOMLY:
        DO walk_to(?f)
```

| Clause | Uses |
|---|---|
| `, RANDOMLY` | one Match, every Match equally likely |
| `, HIGHEST ?p` | the Match with the largest value of `?p` |
| `, LOWEST ?p` | the Match with the smallest value of `?p` |
| `, HIGHEST ?p, RANDOMLY` | the largest, ties broken at random |
| `, WEIGHT <Expression>` | one Match at random, each as likely as its Weight (below) |

- A Pick chooses among the Matches of the **whole condition**, not of one Fact.
- A Pick changes **whether** the condition holds only when it leaves no Match to use: a ranked Placeholder that is never a Number (below), or Weights that are all 0 (below). Otherwise the condition holds when at least one Match exists, and first-match-wins between sibling `GIVEN`s (chapter 06) is unaffected.
- **Ties** in `HIGHEST`/`LOWEST` are unspecified, like the default. Adding `RANDOMLY` breaks them at random. `HIGHEST` together with `LOWEST` is an error, and so is a clause written twice.
- The clauses come in any order and mix freely with a `SHIFTS` Label on a `GIVEN` (chapter 14): `GIVEN hates(?x, ?h), HIGHEST ?h, SHIFTS anger BY 0.1:`.

### The ranked Placeholder

- `?p` must be a named Placeholder **filled by the same condition**. A Trigger Placeholder or one filled earlier in the Body is an error: it has the same value in every Match.
- Matches whose `?p` is **not a Number are skipped**, as a comparison with a non-Number is false (chapter 04). If no Match is left, the condition doesn't hold.
- One ranked Placeholder per Pick. Ranking by a second value is not in 2.0.
- Ranking by `?p` **uses** it: a `?p` named only in the condition and the Pick gets no "never used" warning (`R03_07-unused-placeholder`, chapter 03). The same holds for a Placeholder named in a Weight.

### A weighted Pick

```regia
WHEN insulted:
    GIVEN grudge(?foe, ?size), WEIGHT ?size:     # the bigger the grudge, the likelier
        DO sneer_at(?foe)
```

- `, WEIGHT <Expression>` picks one Match at random, each Match as likely as its Weight compared with the sum of all of them: the Weights of a Random choice (chapter 09), with Matches in the place of Options.
- The Weight is **worked out once per Match**, with the Placeholders the condition fills in that Match, and with any certainly-filled Placeholder from before it as a fixed value. `WEIGHT ?size * 2` and `WEIGHT 10 - ?distance` are both fine.
- It stands alone. Next to `HIGHEST`, `LOWEST` or `RANDOMLY` it is an error (`R26_01-conflicting-pick-clauses`): it is already a random Pick, and it ranks nothing.
- It mixes with Labels like the other Picks: `GIVEN grudge(?foe, ?size), WEIGHT ?size, SHIFTS anger BY 0.1:`.
- **Wrong Weights** follow chapter 09. A negative Weight counts as 0. If **every Match weighs 0** (or less), the condition is treated as having **no Match**: a `GIVEN` doesn't apply and an `IF` goes on to its `ELSE IF` or `ELSE`. The Trace records it (`T26_01-all-pick-weights-zero`), as an entry and not a warning.
- A Weight that **isn't a Number**: on a `GIVEN`, that Match is left out, as a comparison with a non-Number is false in a Context (chapter 04). On a Body `IF` or `ELSE IF`, it fails the Plan (`T09_01-weight-not-number`), as a Weight in a Body does.

### Where Picks are allowed

On `GIVEN`, `IF` and `ELSE IF` headers only. They are an error on:

- `FOR EACH`, which uses every Match;
- Triggers, which match a single Cue, Fact change or Goal;
- `COUNT(…)`, which counts every Match;
- `ELSE`, which has no condition.

## `FOR EACH`

```regia
WHEN party_over:
    FOR EACH hates(?x):
        FORGET hates(?x)
        TELL ?x apology
    PRINT("All forgiven.")
```

- A **For each** is a Body Statement: `FOR EACH <condition>:` followed by a Block. The Block runs **once per Match**, in no specified order, then the Body carries on after it.
- **Snapshot.** The Matches are collected **once**, when the Body reaches the `FOR EACH`. Nothing the Block does adds or removes rounds, and a round still runs with its Match after that Fact is gone (forgotten in an earlier round, or changed during a `WAIT`). To test again, write an `IF` inside the Block.
- **No Matches**: the Block doesn't run and the Body carries on. This isn't a failure.
- **Failure** in any round fails the Plan (chapter 11). The remaining rounds don't run.
- **Placeholders.** The condition can use certainly-filled Placeholders from before it, as fixed values. The Placeholders it fills, and any filled inside the Block, can be used **only inside the Block**, as for `IF` branches (chapter 06). Each round fills them afresh.
- The Block can hold **any Statement**: `WAIT`, `PURSUE` (which waits in each round), `IF`, `RANDOMLY`, another `FOR EACH`.
- `FOR EACH` can be used in **Directors**, over the Director's own Facts (chapter 20).
- The condition is written like any condition (chapter 06, *Conditions*): `AND`, `OR`, `NOT`, comparisons, and every condition word that list names.

### Forgetting everything that matches

A blank in a Basic Action is still an error (chapter 08). Changing every match is written with `FOR EACH`, and the error message suggests it:

```regia
FOR EACH hates(?x): FORGET hates(?x)
FOR EACH avenge(?who): DROP avenge(?who)
```

Each `FORGET` is its own change, so each fires its own `FORGOTTEN` Triggers. The same holds for `DROP` and `DROPPED`.

## `COUNT`

`COUNT(<condition>)` is a Number **Expression** (chapter 04): the number of distinct Matches of the condition, right now.

```regia
WHEN party_starts:
    GIVEN COUNT(friend(?)) >= 3:
        DO dance
    ELSE:
        DO sulk

WHEN insulted(?who):
    LET ?grudges BE COUNT(hates(?, ?who))
    RANDOMLY:
        OPTION, WEIGHT ?grudges: DO punch(?who)
        OPTION: DO ignore(?who)
```

- It can go anywhere an Expression can: a comparison in a Context or `IF`, a `LET` in a Body (`LET ?n BE COUNT(…)`), a `WEIGHT`, an argument.
- It counts distinct Matches over **every blank**, `?` included. `COUNT(hates(?))` is the number of Agents the Agent hates. `COUNT(hates(?x, ?))` counts `hates` Facts, so an Agent hated for two reasons counts twice.
- A condition with no blanks counts **1 or 0**: `COUNT(is_drunk)`.
- Placeholders filled inside `COUNT(…)` are **never filled outside it**. Certainly-filled Placeholders from outside can be used inside it as fixed values (`?who` above). A named Placeholder used only inside a `COUNT` gets no "never used" warning, since naming it there only documents the slot.
- `n OF` stays a Quota form (chapter 18). There is no `GIVEN 3 OF …` (`R26_07-quantity-in-condition`): write `GIVEN COUNT(…) >= 3`.
- `COUNT` is a noun, "how many", here and in the `.regin` line `COUNT 2` (chapter 21), which says how many Agents of a kind start the Program.

`COUNT` counts a Role's Agents through `PLAYS` (chapter 15): `COUNT(? PLAYS Guest)` in a Plot, `COUNT(? PLAYS waiter)` in a Playbook, the Agent itself included if it plays the Role. `EMPTIED` (chapter 19) stays the Trigger for a Role losing its last Agent; a condition is only read when something else fires. A Director still never reads Agents' Facts (chapter 20).

A Director's other conditions on its own Staging work the same way: `COUNT(HonorDuel(?) RUNNING)` counts the distinct arguments of the running duels this Staging started (chapter 17), and `IN <phase>` holds or doesn't, with nothing to pick (chapter 20).

## Reserved words

Every keyword is listed in chapter 01, *Reserved words* (`01-statements-and-blocks.md`).

## Transpiler checks

**Errors**

- `R26_01-conflicting-pick-clauses` `HIGHEST` together with `LOWEST`, `WEIGHT` together with `HIGHEST`, `LOWEST` or `RANDOMLY`, or a Pick clause written twice.
- `R26_02-rank-on-unmatched-placeholder` A ranked Placeholder not filled by the same condition (a Trigger Placeholder, or one filled earlier in the Body).
- `R26_03-misplaced-pick` A Pick (`WEIGHT` included) on `FOR EACH`, a Trigger, `COUNT(…)` or `ELSE`.
- `R26_04-placeholder-outside-for-each` A Placeholder filled by a `FOR EACH` condition or inside its Block, used after the Block.
- `R26_05-maybe-unfilled-pick-weight` A Weight using a Placeholder that is neither filled by the condition nor certainly filled before it.
- `R26_06-retired-at-random` The retired Pick `, AT RANDOM` (hint: `, RANDOMLY`).
- `R26_07-quantity-in-condition` `n OF` in a Context: a Quota form only (chapter 18; hint: `COUNT(…) >= n`).

A blank in a Basic Action, whose message suggests `FOR EACH`, is chapter 08's `R08_01-unfilled-action-argument`.

## Trace entries

**Entries**

- `T26_01-all-pick-weights-zero` Every Match of a weighted Pick weighs 0 (or less): the condition has no Match to use.

## ASL mapping notes

The Jason translation of Picks, `FOR EACH` and `COUNT` is chapter 39 (`39-jason-plan-bodies.md`): `.setof` into a list in rules of `regia/agent.asl`, picks with `.random` or `regia.weighted_pick`, and `FOR EACH` as Jason's `for` over the snapshot rule `regia_each`. What any AgentSpeak Target must keep:

- Every `?` becomes a fresh variable, so that Matches are told apart by every blank, and the distinct Matches are collected (duplicates from both branches of an `OR` removed).
- Every random draw comes from the seeded source (chapter 35).
- **`FOR EACH`** collects its Matches once, before the first round, and a Placeholder filled inside the Block is unbound again for the next round and after the loop. A failure inside fails the Plan.
- **Targets without loops** (not Jason): `FOR EACH` is lowered to a generated recursive goal, `!regia_each__N(L, captured Placeholders)`, with one plan for `[]` and one for `[m(X)|T]` that runs the Block and recurses.
- **Cost**: Picks, `FOR EACH` and `COUNT` build a list each time they are checked, linear in the matching Facts. The plain default doesn't.

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025).

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- Ranking by more than one value, an ordered `FOR EACH`, and `FORGET EVERY …` shorthand: post-2.0 (map's Out of scope).
- `WHILE` and counted loops: post-2.0. `FOR EACH` is the only repetition construct in 2.0. Repeating "until the plate is empty" is a recipe that ends with `PURSUE g, WITHOUT WAITING` (chapter 08).
- Ties in a bare `HIGHEST`/`LOWEST` stay unspecified with no warning: leaving them open can be meant, for example when no two values can be equal.
- Counting a Role's Agents and testing who plays a Role: `PLAYS`, chapter 15. It takes Picks, `FOR EACH` and `COUNT` like any condition.
- The format and routing of runtime warnings: chapters 34 and 35.
