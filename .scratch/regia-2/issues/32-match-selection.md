# Match selection over a Context

Type: grilling
Status: open

## Question

How does a Plan work with the several matches of one Context? Decide:
- Picking one match: at random (read alongside `EITHER`/`OR`, spec 09) or ranked by priority or by a value ("the guest I hate most").
- Running a Body for every match, and whether 2.0 needs any looping construct beyond that (it has no `WHILE`/`FOR`, spec 06).
- Changing or forgetting everything that matches a blank (`FORGET hates(?x)` for every `?x`, spec 08).
- Counting matches in a Context (`GIVEN 3 OF hates(?x)`, spec 18), and whether that makes `EMPTIED` (spec 19) redundant.
- The ASL mapping of each (Jason's `.findall`, `.count`).
Precedence is not part of this: it only ranks Plans (spec 13).

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- Six spec chapters defer to it: 06, 08, 09, 13, 18, 19.
