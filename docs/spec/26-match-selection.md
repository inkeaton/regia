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
    GIVEN guest(?g), AT RANDOM:
        TELL ?g joke.

WHEN insulted:
    GIVEN hates(?x, ?how_much), HIGHEST ?how_much:
        ASK ?x TO duel.

WHEN tired:
    IF friend(?f, ?distance), LOWEST ?distance, AT RANDOM:
        DO walk_to(?f).
```

| Clause | Uses |
|---|---|
| `, AT RANDOM` | one Match, every Match equally likely |
| `, HIGHEST ?p` | the Match with the largest value of `?p` |
| `, LOWEST ?p` | the Match with the smallest value of `?p` |
| `, HIGHEST ?p, AT RANDOM` | the largest, ties broken at random |

- A Pick chooses among the Matches of the **whole condition**, not of one Fact.
- A Pick never changes **whether** the condition holds: it holds when at least one Match exists. So first-match-wins between sibling `GIVEN`s (chapter 06) is unaffected.
- **Ties** in `HIGHEST`/`LOWEST` are unspecified, like the default. Adding `AT RANDOM` breaks them at random. `HIGHEST` together with `LOWEST` is an error, and so is a clause written twice.
- The clauses come in any order and mix freely with a `SHIFTS` Label on a `GIVEN` (chapter 14): `GIVEN hates(?x, ?h), HIGHEST ?h, SHIFTS anger BY 0.1:`.

### The ranked Placeholder

- `?p` must be a named Placeholder **filled by the same condition**. A Trigger Placeholder or one filled earlier in the Body is an error: it has the same value in every Match.
- Matches whose `?p` is **not a Number are skipped**, as a comparison with a non-Number is false (chapter 04). If no Match is left, the condition doesn't hold.
- One ranked Placeholder per Pick. Ranking by a second value is not in 2.0.

### Where Picks are allowed

On `GIVEN`, `IF` and `ELSE IF` headers only. They are an error on:

- `FOR EACH`, which uses every Match;
- Triggers, which match a single Event, Fact change or Goal;
- `COUNT(…)`, which counts every Match;
- `ELSE`, which has no condition.

## `FOR EACH`

```regia
WHEN party_over:
    FOR EACH hates(?x):
        FORGET hates(?x).
        TELL ?x apology.
    PRINT("All forgiven.").
```

- A **For each** is a Body Statement: `FOR EACH <condition>:` followed by a Block. The Block runs **once per Match**, in no specified order, then the Body carries on after it.
- **Snapshot.** The Matches are collected **once**, when the Body reaches the `FOR EACH`. Nothing the Block does adds or removes rounds, and a round still runs with its Match after that Fact is gone (forgotten in an earlier round, or changed during a `WAIT`). To test again, write an `IF` inside the Block.
- **No Matches**: the Block doesn't run and the Body carries on. This isn't a failure.
- **Failure** in any round fails the Plan (chapter 11). The remaining rounds don't run.
- **Placeholders.** The condition can use certainly-filled Placeholders from before it, as fixed values. The Placeholders it fills, and any filled inside the Block, can be used **only inside the Block**, as for `IF` branches (chapter 06). Each round fills them afresh.
- The Block can hold **any Statement**: `WAIT`, `PURSUE` (which waits in each round), `IF`, `EITHER`, another `FOR EACH`.
- `FOR EACH` can be used in **Directors**, over the Director's own Facts (chapter 20).
- The condition is written like any condition (chapter 06): `AND`, `OR`, `NOT`, comparisons, `PURSUING`.

### Forgetting everything that matches

A blank in a Basic Action is still an error (chapter 08). Changing every match is written with `FOR EACH`, and the error message suggests it:

```regia
FOR EACH hates(?x): FORGET hates(?x).
FOR EACH avenge(?who): DROP avenge(?who).
```

Each `FORGET` is its own change, so each fires its own `FORGOTTEN` Triggers. The same holds for `DROP` and `DROPPED`.

## `COUNT`

`COUNT(<condition>)` is a Number **Expression** (chapter 04): the number of distinct Matches of the condition, right now.

```regia
WHEN party_starts:
    GIVEN COUNT(friend(?)) >= 3:
        DO dance.
    ELSE:
        DO sulk.

WHEN insulted(?who):
    ?grudges = COUNT(hates(?, ?who)).
    EITHER, WEIGHT ?grudges: DO punch(?who).
    OR: DO ignore(?who).
```

- It can go anywhere an Expression can: a comparison in a Context or `IF`, naming in a Body (`?n = COUNT(…).`), a `WEIGHT`, an argument.
- It counts distinct Matches over **every blank**, `?` included. `COUNT(hates(?))` is the number of Agents the Agent hates. `COUNT(hates(?x, ?))` counts `hates` Facts, so an Agent hated for two reasons counts twice.
- A condition with no blanks counts **1 or 0**: `COUNT(is_drunk)`.
- Placeholders filled inside `COUNT(…)` are **never filled outside it**. Certainly-filled Placeholders from outside can be used inside it as fixed values (`?who` above). A named Placeholder used only inside a `COUNT` gets no "never used" warning, since naming it there only documents the slot.
- `n OF` stays a Quota form (chapter 18). There is no `GIVEN 3 OF …`.

`COUNT` doesn't replace `EMPTIED` (chapter 19). That Trigger counts the Agents playing a Role, which no condition can test in 2.0, and a Director never reads Agents' Facts (chapter 20).

## Reserved words

`AT`, `RANDOM`, `HIGHEST`, `LOWEST`, `FOR`, `EACH`, `COUNT`. `RANDOM` is also the Expression `RANDOM(a, b)` (chapter 04) and appears in Instancing (`AT RANDOM(a, b)`, chapter 21): followed by `(` it is the function, and otherwise it is the Pick.

## ASL mapping notes

For *The full ASL mapping* to pick up. Generated names use a prefix designers can't produce (chapter 06). Every `?` becomes a fresh variable in the templates below, so that Matches are told apart by every blank.

- **Default**: the plain context, unchanged. Jason uses the first unifier.
- **`AT RANDOM`**: collect the distinct Matches with `.setof` over a tuple of the condition's blanks, then pick by index. In a context:

  ```
  +bored : .setof(m(G), guest(G), L) & .length(L, N) & N > 0
           & .nth(math.floor(math.random(N)), L, m(G)) <- …
  ```

  `.setof` (not `.findall`) removes duplicates, such as the same Match from both branches of an `OR`. Jason accepts internal actions in contexts and in `if` conditions, so `IF … , AT RANDOM` uses the same formula.
- **`HIGHEST ?p` / `LOWEST ?p`**: `.setof` the Matches, keep those with `.number(P)`, take `.max`/`.min` of the values, then take a Match with that value (`.member`). With `AT RANDOM`, `.setof` the tied Matches and pick by index as above.
- **`FOR EACH`**: snapshot with `.setof` into a list, then iterate. Jason's `for (.member(m(X), L)) { … }` is the direct form. Check how Jason treats variables bound inside a `for` body across rounds. If they carry over, lower to a generated recursive goal instead: `!regia_each__N(L, captured Placeholders)`, one plan for `[]` and one for `[m(X)|T]` that runs the Block and recurses. Either way a failure inside fails the Plan. The recursive form also serves Targets without loops.
- **`COUNT`**: `.count(f, N)` when the condition is a single Fact, and `.setof(m(…), cond, L) & .length(L, N)` otherwise (an empty `.setof` gives `[]`, so 0). In a Body: the same, then the arithmetic.
- **Cost**: Picks, `FOR EACH` and `COUNT` build a list each time they are checked, linear in the matching Facts. The plain default doesn't.

## Not decided here

- Weighted random Picks (`, AT RANDOM WEIGHTED BY ?w`), ranking by more than one value, an ordered `FOR EACH`, and `FORGET EVERY …` shorthand: post-2.0 (map's Out of scope).
- `WHILE` and counted loops: post-2.0 (map's Out of scope). `FOR EACH` is the only repetition construct in 2.0.
- Counting a Role's Agents or testing Role membership in a condition: *Richer Mappings and Role tests*, post-2.0.
- The format and routing of runtime warnings: chapters 34 and 35.
