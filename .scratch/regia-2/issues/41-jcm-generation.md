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
