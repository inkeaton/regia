# Write the showcase Program

Type: prototype
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01

## Question

What does the whole example world look like as one Regia 2.0 Program? Write it as real files in `docs/guide/showcase/` (Vocabulary, Playbooks, Plots, a `.regin` Instancing file), for the user to react to. Decide along the way:
- The file split and Imports.
- Whether every row of the coverage table from *Choose the example world* (01) is met; anything that can't be placed naturally is the first `#revise` entry.
- Its size: large enough to be meaningful, small enough to walk through in one chapter.

Every construct is checked by hand against its spec chapter, since no Transpiler exists. Awkward spots found while writing are noted as `#revise` comments in the README, not fixed in the design.

## Resolution

Accepted by the user on 2026-11-11. The Program is in [`docs/guide/showcase/`](../../../docs/guide/showcase/), about 550 lines, checked by hand against spec chapters 01–21 and 26.

- **File split**: `vocabulary.regia` holds all shared Vocabulary; `playbooks/` has one Playbook per file, each importing the Vocabulary; `plots/` has one Plot per file, importing the Playbooks it gives and the Subplots it starts; `banquet.regin` is the full cast and `test.regin` layers the small cast on it.
- **Coverage**: every row of the coverage table has a place. The README's outline, coverage table and interactions are updated to match the Program.
- **Departures from *Choose the example world***, all accepted:
  - The insulted Guest is `Challenger` and the insulter `Defender`, both by Placeholder Mapping; every Guest is a `Spectator`; the counted Mapping is only in `Poisoning`.
  - An eighth Playbook, `Wagering`, for Spectators.
  - `Scheming` is given by Role setup; the Giving to one Agent is `ASSIGN Keeping_watch TO ?winner`. `Keeping_watch` is also given by `Poisoning`, so one Playbook comes from two Plots.
  - `FOR EACH` is in `Dining` and `Duelling`, not in `Serving`.
  - The "failure climbing" interaction runs inside the Servant; the Guest reacts after a `WAIT` and a `COUNT`, since an `ASK` can't be waited on.
- **Review notes**: 19 `#revise` entries and one spec-wording note in the README's *Review notes*, for *Write: Review List* to collect.
- No glossary change and no ADR.
