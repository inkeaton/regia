# .jcm generation

Type: grilling
Status: open
Blocked by: 34

## Question

How does Instancing (spec 21) become a Jason `.jcm`? Decide:
- The `.jcm` from Agent declarations.
- `RANDOM` Propensity values drawn by the infrastructure per Agent.
- The Root Plot's Director knowing each Agent kind's Roles and values for joiners.
- Combining Role files for an Agent kind playing several Roles.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *ASL infrastructure layout* (34): Role files exist only for Root Plot Roles, under `asl/roles/`, and include `regia/agent.asl`; Jason doesn't skip duplicate includes, so combining Role files for a kind must include the Infrastructure once. `ag-class` defaults to the `regia-jason` agent class; `asl/` is the source path (spec 28).
- From *Giving and taking Playbooks at runtime* (35): each Role file lists its Playbooks as `regia_playbook(P)` initial beliefs; combining Role files must not duplicate those or the Playbook includes (chapter 29).
- From *Director runtime in ASL* (36): the Root Director's entry uses `ag-class: regia.DirectorAgent` and is the only Director with `address`/`port`, since it alone talks to the game. Subplot Directors have no body (chapter 30).
- From *Stagings and Subplots runtime in ASL* (37): the Root Director's agent name is `regia_director__<plot>`; Subplot Directors are created at runtime by `regia.start_staging`, not listed in the `.jcm`. The Root's starting cast reaches it before `regia_begin` (chapter 31).
