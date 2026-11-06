# A name has one parameter count

A Vocabulary name has exactly one parameter count across the whole Program, so `FACT hates(a)` and `FACT hates(a, b)` together are an error. This goes beyond what the Target needs: in Jason, as in Prolog, `hates/1` and `hates/2` are unrelated predicates. We chose it because designers read `hates(host)` and `hates(host, guest)` as the same idea with an argument left out. If they were separate items, `GIVEN hates(host)` would silently never match a `hates(host, guest)` the Agent knows. One count per name also lets errors say "`hates` takes 2 arguments" instead of "no `hates` with 1 argument is declared", gives the Visual Editor one item per name, and matches the existing rule that a name has one kind (chapter 05).

## Considered Options

- **A name plus a parameter count identifies the item** (Prolog style): no translation for the Target, and families like `at(place)` / `at(person, place)` read naturally. Two files declaring different counts would also coexist instead of clashing. Rejected because the silent non-match is the kind of mistake designers can't see.

## Consequences

- Distinct ideas need distinct names: `at(place)` and `sees_at(person, place)`.
- Allowing overloading by count later is backwards compatible, since no valid program would change meaning.
