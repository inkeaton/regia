# Match selection over a Context

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How does a Plan work with the several matches of one Context? Decide:
- Picking one match: at random (read alongside `EITHER`/`OR`, spec 09) or ranked by priority or by a value ("the guest I hate most").
- Running a Body for every match, and whether 2.0 needs any looping construct beyond that (it has no `WHILE`/`FOR`, spec 06).
- Changing or forgetting everything that matches a blank (`FORGET hates(?x)` for every `?x`, spec 08).
- Counting matches in a Context (`GIVEN 3 OF hates(?x)`, spec 18), and whether that makes `EMPTIED` (spec 19) redundant.
- The ASL mapping of each (Jason's `.findall`, `.count`).
Precedence is not part of this: it only ranks Plans (spec 13).

## Answer

Spec chapter: `docs/spec/26-match-selection.md`. Glossary: *Match*, *Pick* and *For each* added, *Expression* updated. Specs 03, 04, 06, 08, 09, 13, 18 and 19 point to the new chapter; ADR 0001's consequence line updated.

- **The default stays unspecified.** A plain `GIVEN guest(?g):` uses one Match and the language doesn't say which (Jason: first unifier). Random by default was weighed and rejected: it puts a `.setof` behind every Context, and choosing is something the author writes when it matters. Note that Jason doesn't run a Plan per match either.
- **Picks** are trailing clauses on `GIVEN`/`IF`/`ELSE IF`: `, AT RANDOM`, `, HIGHEST ?p`, `, LOWEST ?p`, over the Matches of the whole condition. Ties are unspecified; adding `AT RANDOM` breaks them at random. `?p` must be filled by that condition; non-Number values are skipped. A Pick never changes whether the condition holds. Not allowed on `FOR EACH`, Triggers, `COUNT` or `ELSE`.
- **`FOR EACH <condition>:`** is a Body Block run once per Match, from a snapshot taken when the Body reaches it, in no specified order. No Matches: skipped. A failing round fails the Plan. Its Placeholders live in the Block. Any Statement inside; allowed in Directors.
- **Forgetting everything that matches** stays an error with a blank; `FOR EACH hates(?x): FORGET hates(?x).` is the form, suggested by the message. Each change fires its own Triggers.
- **`COUNT(condition)`** is a Number Expression: distinct Matches over every blank, `?` included. Inner Placeholders stay inside. `n OF` stays a Quota form.
- **`EMPTIED` stays**: counting own Facts doesn't count a Role.
- **Out of scope**: `WHILE` and counted loops, weighted Picks, ranking by several values, ordered `FOR EACH`, `FORGET EVERY` shorthand.
- **ASL**: `.setof` over a tuple of the blanks, then `.nth` with `math.random`, `.max`/`.min`, `for`/recursive goal, `.count`/`.length`. Notes in the chapter for the ASL mapping tickets.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- Six spec chapters defer to it: 06, 08, 09, 13, 18, 19.
