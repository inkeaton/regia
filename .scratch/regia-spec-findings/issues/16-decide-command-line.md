# Decide: Command line and conformance

Type: grilling
Status: open
Assignee:
Blocked by:

## Question

- F52: does chapter 38 join Conformance's language chapters (and get an exemplar case), or does chapter 27 say why it doesn't?
- F53: what form, code and exit status do command-line errors take: a `.regia` Entry to `build`/`run`, an Entry file that doesn't exist, an unknown `--target`?
- F54: what does `--deny-warnings` add to `regia test`? Is a behaviour case's Program checked against annotations, or must it have no Diagnostics?
- F55: does `--target none` skip `R21_13-unknown-target-setting` and `R21_16-unknown-target` too?

Start each question from the guide's reading. Mark which answers need an ADR.

Applying the answers is *Apply: Command line and conformance*.
