# Director runtime in ASL

Type: grilling
Status: open
Blocked by: 34, 35

## Question

How does a Director run in Jason? Decide:
- Routing game percepts to the right Directors.
- Phase switching: `EXITED` inside the atomic switch, `ENTERED` after it, and dropping a Phase's running intentions on leaving it (spec 20).
- Each Director's ordered record of standing Givings (spec 19).
- Running Role setups at Staging start and when an Agent joins, as Director messages (spec 16).
- One-Agent Givings and Mappings (spec 20).

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
