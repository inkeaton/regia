# `%` is a share, never a remainder

A part of a Role was written with the unit word `PERCENT`: `ASSIGN Brawling TO 30 PERCENT OF Guest`, and in 2.0 the Quota `FROM 50 PERCENT OF Guest`. `%` was unused once `#%` was retired. The syntax review gave it to percentages: `30% OF Guest`, `?share% OF Guest`, `(?n * 10)% OF Guest`. `PERCENT` is the retired spelling `R15_16-retired-percent`.

`%` goes only between a Number Expression and `OF`. Anywhere else it is `R15_17-misplaced-percent-sign`. Regia has one Number kind, so `50%` is never a Value: `LET ?x BE 50%.` and `WEIGHT 30%` are errors, and a Weight stays relative.

Regia has no remainder (chapter 04), and `%` will never be one. A remainder, if Regia ever needs one, will be a word (`MOD`, or a function like `RANDOM(a, b)`), chosen when it is needed and not reserved now.

## Considered options

- **Keeping `PERCENT`.** It reads well, but it is a long word for a sign every reader knows, and it was the only unit Regia wrote as a word next to a bare Number Expression.
- **Keeping `%` for a future remainder.** It is the mainstream programming meaning, but Regia's writers are designers, who read `%` as "percent". A remainder has few uses in story logic: every n-th Signal is a Quota (chapter 18), and taking turns reads better as a Fact naming the next one. A parser could tell the two apart (a share is followed by `OF`, a remainder by an Expression), but one symbol would carry two glosses, against chapter 01's one-meaning rule.
- **`%` as a general Number suffix** (`50%` meaning `0.5` anywhere). It would bring "half" back next to `0.5 OF Guest`, which is a count, and invite `WEIGHT 30%`, which looks absolute and isn't.

## Consequences

- A programmer who writes `?n % 3` gets `R15_17-misplaced-percent-sign`, whose hint says `%` writes a share and Regia has no remainder.
- Taking `%` back for a remainder later would break every Plot that writes a share.
- In Regia 1.5 (counted picks), and the same spelling in 2.0's Quotas.
