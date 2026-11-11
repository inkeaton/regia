# ASL infrastructure layout

Type: grilling
Status: open

## Question

What does the Jason output look like as a set of files? Decide:
- Shared infrastructure files imported by each generated file, instead of copied plans (primer ch.8).
- What infrastructure state each Agent holds (its Playbooks, which Plots gave them).
- Generated names for Local Vocabulary (spec 10) and External names in Jason.
- Which clock Jason measures Durations with, wall or game time (spec 12).

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- First of the full ASL mapping tickets; the others build on its layout.
- From *Match selection over a Context* (32): Picks, `FOR EACH` and `COUNT` lower to `.setof` over a tuple of the condition's blanks (notes in `docs/spec/26-match-selection.md`). Open check: whether Jason's `for` keeps variables bound in its body across rounds; if so, `FOR EACH` lowers to a generated recursive goal.
