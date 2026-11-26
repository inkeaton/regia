# A `.regia` Entry builds too, without a Root Plot

ADR 0036 let only a `.regin` Entry be built. Every Target file was then made for one named Root Plot, and a Playbook or Plot file could only be checked. That took away something Regia 1.0 had: compile a `.regia` file, get its ASL, and put it in a Jason project written by hand. It also meant that no part of a Program could be built before its `.regin` existed.

We decided that a `.regia` Entry can be built. Its Build has **no Root Plot and no cast**: the Target code of the whole Program, and nothing that starts it. For Jason that is ASL files and no `.jcm`. The rest of ADR 0036 stands: one Entry per Program, a `.regin` Entry must reach a `ROOT`, and the Root Plot is never inferred. Only a `.regin` Entry can be run.

Any Plot of such a Build may be the one a hand-written project starts, so **every Role of every Plot gets a Role file**, named `<Plot>__<Role>` because Role names are local to their Plot. The facts that make a Director the Root are left out of every Director file, and the project supplies them.

## Considered options

- **Keep ADR 0036**: the fewest kinds of Build, but a writer who only wants ASL has to name a Root Plot they may not have.
- **Infer the Root in a `.regia` Entry**: the guess ADR 0036 removed.
- **No Role files**: a smaller Build, but nothing an Agent can start from.

## Consequences

- A `.regia` Build skips the checks that need a Root Plot, as `check` does, so it can hold a problem that only a `.regin` Entry reports.
- A `.regia` Entry builds into a folder that keeps its extension, so `banquet.regia` and `banquet.regin` don't share one.
- `run`, behaviour cases and the Visual Editor's Build menu stay with `.regin`.
