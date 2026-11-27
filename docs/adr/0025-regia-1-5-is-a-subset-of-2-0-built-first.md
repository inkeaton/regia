# Regia 1.5 is a subset of 2.0, built first

2.0 adds more than twenty systems to 1.0 at once. We design them together, so that they fit, and build a subset first: Regia 1.5, a full version of the language with the same Transpiler and Visual Editor. The rest of 2.0 is added once 1.5 runs.

1.5 leaves out `FROM GAME`, `FROM ME` and `FROM` alternatives with `OR`; `BY`, and with it the asker hearing how an asked Goal ended; Quota Triggers; and Agents joining a running Staging. It keeps `FROM` with a Role, a Placeholder and `DIRECTOR`, counts, `EXCEPT`, `CAST`, `PLAYS`, and Agents leaving. The full list is in the revision ticket *Which systems Regia 1.5 keeps*, and the cut cause by cause, with how the spec marks it, in *The Regia 1.5 cut*: a `## Regia 1.5` section in every spec chapter, indexed in chapter 27.

## Considered Options

- **Build all of 2.0 at once**: every system would reach the Transpiler and the Jason chapters before any of them has run, and a mistake in one would be found late and in the middle of the others.
- **Design 1.5 alone and 2.0 afterwards**: the later systems would be designed against a language already built, and the revision has already shown how much they change each other (ticket 05's setups and joiners, ticket 06's `CAST`).
- **Cut at the start of the revision**: the systems were still moving, and what depends on what wasn't known.

## Consequences

- The revision still decides every cause for 2.0, and records for each whether it is in 1.5.
- Nothing in 1.5 may need a system that is later. The last revision ticket checked this. The one gap was the game spawning an Agent, which belongs to joining: a 1.5 run refuses it (`T19_02-join-refused`).
- A 1.5 build parses all of 2.0 and reports a construct of a later system as `R01_09-later-regia-construct`, "Regia 2.0". There is no 1.5 mode in a 2.0 build.
- Some 2.0 decisions are undone in 1.5 for now: a done-Signal is written by hand where 2.0 hears the ending, and "every Guest has done it" is counted with the Director's own Facts and `PLAYS`.
- Without joiners, a Staging's cast is fixed at start and can only shrink, so the rules about what a joiner gets don't apply in 1.5.
- Programs written for 1.5 should stay valid in 2.0. A later system adds meaning; it doesn't change what a 1.5 Program does.
