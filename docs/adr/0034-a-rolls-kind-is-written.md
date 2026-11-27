# A roll's kind is written

`RANDOM(a, b)` used to give a whole number when both bounds came out whole and a decimal otherwise. A bound can be a Placeholder or an Expression, so the kind was only known at runtime: `RANDOM(1, ?gold / 2)` staked whole coins with 12 in the purse and 3.71 coins with 13. Nothing rounded.

We decided that the kind is fixed by the source. A roll is a decimal when either bound is a decimal number written out (`3.0`, `-0.5`), and whole otherwise, whatever its Placeholders and Expressions hold. A whole roll gives one of the whole numbers from `a` to `b`, so `RANDOM(1, 6.5)` gives 1 to 6. Bounds in either order mean the same range. A whole roll with no whole number between its bounds fails the Plan (`T04_03-empty-whole-roll`), or makes its comparison false in a Context. A starting Propensity value in Instancing is always a decimal roll, since a whole one in [0, 1] or [-1, 1] is never what is meant.

## Considered options

- **The kind from the values** (the old rule): dice keep their look, but the same line rolls differently from one run to the next.
- **Two spellings**, one word for a whole roll and another for a decimal: the clearest to read, at the cost of a new word for the less common case.
- **Every roll a decimal**, with whole numbers through a rounding function: needs a math library 2.0 doesn't have, and makes the die roll the long form.
- **The kind from where the roll is used** (a `WAIT` always decimal, a count always whole): fewer surprises in those places, but a rule per place, and no rule for a Body argument.

## Consequences

- `RANDOM(1, 6)` is still a die roll, and the Transpiler knows every roll's kind.
- "Any wait from one to three seconds" is still written `RANDOM(1, 3.0)`. A whole-second wait can be meant, so a `WAIT` gets no exception.
- `bravery AT RANDOM(-1, 1)` in a `.regin` file is any bravery, unlike the same bounds in a Body. Chapter 21 says so.
- A roll is the only place a Number is rounded. Shares of a Role still round up (chapters 15 and 18).
