# A Build is one `.regin` Entry that names its Root Plot

Chapter 10 let several Entry files make one Program, while a Build was made from one Entry and the Visual Editor treated each `.regin` as a Program of its own, so `regia build banquet.regin test.regin` couldn't be read. The Root Plot was inferred when exactly one Plot was never started as a Subplot. So a Playbook file given to `regia check` got "no Root Plot", and a Subplot's file was taken for the whole story and got errors that vanished inside the banquet. Only a whole story could be checked.

We decided that a Program has **one Entry file**, and builds are layered by importing, never by naming several Entries. The Root Plot is **named** with `ROOT` in Instancing and never inferred, because which story a game setup runs is a fact about that setup (ADR 0035's layers). Only a `.regin` Entry can be built or run. A `.regia` Entry has no Root Plot: it is checked for what it says (names, Plans, Precedence, Interfaces), and the checks that need a Root Plot don't run.

Amended by ADR 0049: a `.regia` Entry can be built too, without a Root Plot. Everything else here stands.

## Considered options

- **Several Entries, one Program**: no use that importing doesn't already cover, and two readings of one command line.
- **Keep inference, add `--root <Plot>` or `--fragment` to `check`**: the writer has to say on every command what the file already knows, and a lone Subplot file still passes for the Root by default.
- **Infer the Root only in `.regia` Entries**: keeps `regia build plots/royal_banquet.regia`, at the price of the same guess that broke checking a Subplot alone.

## Consequences

- Every `.regin` that is built must reach a `ROOT`. Existing ones gain one line (`R2104` is narrowed to that).
- Building ASL alone from a Plot file goes away: even a Build with no cast is a `.regin` with a `ROOT`.
- The Visual Editor's Build menu lists `.regin` files only. A `.regia` file no `.regin` reaches is still checked as its own Entry.
- A behaviour case is always a folder with a `.regin` (chapter 27).
- In Regia 1.5 all of it is in.
