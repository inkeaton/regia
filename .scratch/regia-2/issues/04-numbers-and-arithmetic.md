# Numbers and arithmetic

Type: grilling
Status: resolved
Blocked by: 03
Assignee: Edoardo Vassallo

## Question

Can Regia work with numbers? For example numeric Facts (`health(80)`), comparisons in a Context (`health < 20`), arithmetic in a Body (raise or lower a value), and maybe random numbers. What is in scope for 2.0, and what does it look like in a readable form?

## Answer

Spec chapter: `docs/spec/04-numbers-and-expressions.md`. ADR: `docs/adr/0002-values-are-named-in-the-body.md` (amends ADR 0001). Glossary: Number and Expression added, Placeholder revised.

- **In scope:** numeric Values, comparisons in a Context, arithmetic in argument slots, `RANDOM`. No math library.
- **One Number kind** (`5 = 5.0`). Literals `80`, `-3`, `0.5`: leading digit required, no exponents, separators or other bases. Precision is up to each Target.
- **Operators:** `< > <= >= =` (inequality via `NOT … = …`); `+ - * /` and parentheses, `/` always a true division, no modulo. Arithmetic binds tighter than comparisons, comparisons tighter than `NOT`/`AND`/`OR`. Chained comparisons are an error with a hint. Spacing is free.
- **`=` works on any Values**; ordering and arithmetic only on Numbers.
- **Comparing a Fact's number is explicit:** `health(?h) AND ?h < 20`.
- **Expressions** go in Body argument slots and on either side of a Context comparison; never in Trigger slots or declarations.
- **The Context tests, the Body names.** In a Context `=` only compares; `RANDOM` may appear in comparisons (`RANDOM(1, 100) <= 30`). In a Body, `?name = Expression.` names a value: an error if already filled, usable only after its Statement, and after an `IF` only if every branch names it.
- **`RANDOM(a, b)`** is inclusive; whole when both bounds are whole, decimal otherwise. Every call is a fresh roll.
- **Misuse:** the Transpiler reports what it can see. At runtime a Context comparison on a non-Number is false; Body arithmetic on a non-Number, or division by zero, makes the Plan fail.
- **Handed over:** changing a numeric Fact in one step and joining strings to *Basic action set*; Body `IF` operators and matching to *Context vs control flow*; the runtime failure to *Plan failure and fallback*. Shorthand comparisons, a math library and Context-side naming went to *Not yet specified*.

## Comments

- From Statement and block syntax: a `.` followed by anything other than a space, the end of the line or `;` belongs to a name or number, so decimals like `0.5` are safe. See `docs/spec/01-statements-and-blocks.md`.
