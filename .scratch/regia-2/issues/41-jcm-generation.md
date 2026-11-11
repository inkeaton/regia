# .jcm generation

Type: grilling
Status: resolved
Blocked by: 34

## Question

How does Instancing (spec 21) become a Jason `.jcm`? Decide:
- The `.jcm` from Agent declarations.
- `RANDOM` Propensity values drawn by the infrastructure per Agent.
- The Root Plot's Director knowing each Agent kind's Roles and values for joiners.
- Combining Role files for an Agent kind playing several Roles.

## Answer

Spec chapter: `docs/spec/36-jason-jcm.md`, checked against VEsNA-Pro's `vesna.jcm` and `VesnaAgent` (user parameters `temper`, `strategy`, `address`, `port`; one WebSocket client per agent). Chapters 21, 28–31 and 33–35 point to it. No ADR: everything here is cheap to change.

- **Names**: starting Agents are `<kind>_<n>` from 1, always numbered (even `COUNT 1`), first letter lowercased.
- **Ports**: new `TARGET JASON` keys `address` (default `localhost`) and `base_port` (default `9080`). The Root Director gets `base_port`; starting Agents the next ports, kinds sorted by name, then number. Every Agent has its own `.jcm` entry (`instances:` can't vary ports). A port past 65535 is an error.
- **`.jcm`**: `mas <entry>`, `asl` source path, Root Director first (`regia.DirectorAgent`), then the starting Agents on `regia.RegiaAgent` (named here) with `temper` (only when set), `strategy`, `address`, `port`, `trace_console`. No `goals:` or `beliefs:`.
- **Several Roles**: a generated combination file `roles/<RoleA>__<RoleB>.asl` (Roles sorted by name) per Role set used by a kind, including the Infrastructure once and the de-duplicated union of Playbook includes, `regia_playbook`, Quota dispatchers and `regia_quota_watch`. Including the Role files directly was rejected: the Infrastructure's initial goals would run twice, and shared Playbooks and dispatchers would be doubled. Single-Role kinds use the plain Role file, unchanged.
- **`RANDOM`**: travels as `random(a, b)` in `temper`; `regia.RegiaAgent` draws it with the run's seed before VEsNA's `Temper` reads it, and writes a `TEMPER` `cast` Trace entry.
- **`cast.json`**: the Build writes the starting cast for the game (`address`, the Root Director's name and port, `{name, kind, port}` per Agent), next to the `.jcm`.
- **`regia_kind(Kind, Roles, File, Settings)`**: one initial belief per declared kind (also `COUNT 0`) in the Root Director's file; `regia.spawn_agent` reads it to create joiners. Settings are a `key(value)` list of user parameters minus `port`. A side file in Java and having the game send it all were rejected.
- **`regia_join`** carries exactly `{kind, name, port}`; a missing or invalid `port` is a nonsensical report.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *ASL infrastructure layout* (34): Role files exist only for Root Plot Roles, under `asl/roles/`, and include `regia/agent.asl`; Jason doesn't skip duplicate includes, so combining Role files for a kind must include the Infrastructure once. `ag-class` defaults to the `regia-jason` agent class; `asl/` is the source path (spec 28).
- From *Giving and taking Playbooks at runtime* (35): each Role file lists its Playbooks as `regia_playbook(P)` initial beliefs; combining Role files must not duplicate those or the Playbook includes (chapter 29).
- From *Director runtime in ASL* (36): the Root Director's entry uses `ag-class: regia.DirectorAgent` and is the only Director with `address`/`port`, since it alone talks to the game. Subplot Directors have no body (chapter 30).
- From *Stagings and Subplots runtime in ASL* (37): the Root Director's agent name is `regia_director__<plot>`; Subplot Directors are created at runtime by `regia.start_staging`, not listed in the `.jcm`. The Root's starting cast reaches it before `regia_begin` (chapter 31).
- From *Quota counts and cast changes in ASL* (39): the Root Director's file holds `regia_start_cast([cast(Role, Agent), …])` with the starting Agents' names; decide those names. `regia.spawn_agent(Kind, Name, Body)` creates joiners: decide where each kind's Roles, settings and Propensity values live in the Root Director's file, and the body fields `regia_join` carries (a port, for example). Combining Role files must not duplicate Quota dispatchers or `regia_quota_watch` beliefs (chapter 33).
- From *Trace and logging* (40): behaviour cases name starting Agents by their `.jcm` names (`guard_1` …), so those names must be stable and predictable from Instancing. `trace_console` is a new `TARGET JASON:` key; pass it to every agent. The Build also gets `asl/regia/sourcemap.json`, which maps Generated agent names such as `regia_director__<plot>` back to designer names (chapter 35).
