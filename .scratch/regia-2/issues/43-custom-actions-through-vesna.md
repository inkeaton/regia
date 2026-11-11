# Custom Actions through VEsNA

Type: grilling
Status: open

## Question

How do Custom Actions and Regia's game messages work with VEsNA-Pro (`vesna-pro-main/`)? Decide:
- How a dot-less Custom Action (chapter 28's "environment action") reaches the game: VEsNA-Pro today only sends its own internal actions (`vesna.walk`, `jump`, `rotate`) through `perform()`, fire-and-forget.
- Whether `DO` waits for the game's answer, and how the game reports a failed Action (spec 11 relies on it).
- How the Root Director performs Actions passed up from Subplot Directors (`regia_act(A)`, chapter 30) and returns their result.
- How `regia-jason` receives its `regia_event` and `regia_fact` messages (chapter 30) inside an Agent's `VesnaAgent` body, whose message handler is private and logs unknown types: an upstream hook in VEsNA-Pro, or something else.

## Comments

- Surfaced by *Director runtime in ASL* (36), 2026-11-11.
- From *Stagings and Subplots runtime in ASL* (37): the Root Director's `END PLOT` leaves its agent alive and idle; decide whether and how the game hears that the story has ended (chapter 31).
- From *Quota counts and cast changes in ASL* (39): the Root Director's body also receives `regia_join` and `regia_leave` (chapter 33).
- From *Trace and logging* (40): `action` Trace entries are written when an Action's result comes back, so the design here must give the agent architecture that result. Behaviour cases run against `ScriptedGame` (ADR 0014), a WebSocket server that speaks the game's JSON protocol and must fake whatever result messages are decided here (success unless `> action fails`). The answer also fixes what the `regia_event`/`regia_fact` intake looks like to `ScriptedGame` (chapter 35).
- From *.jcm generation* (41): `regia_join` carries exactly `{kind, name, port}`; the Build writes `cast.json` (starting Agents with kind and port, the Root Director's port) for the game (chapter 36).
