# Director capabilities

Type: grilling
Status: open

## Question

What can a Director do and know (primer ch.5)? Decide the `WORLD` keyword (rename?), whether the Director has its own Facts (whose Facts does a Plot Context read?), whether it receives world Events directly, and whether it should have Goals or stay a simple state machine (what would richer Directors give us?).

## Comments

- From *Goals and Trigger kinds* (05): `ON ENTER` / `ON EXIT` are retired; Phase entry and exit are `WHEN` Triggers. Decide their wording (e.g. `WHEN ENTERED:`). Also decide how a Director gives a Goal to a Role or to an Agent filled by `FROM Guest ?who`, and what it can do with `?who`. Signals arrive as Events and can be matched with `FROM Role [?who]`. See `docs/spec/05-goals-and-triggers.md`.
- From *Messaging between Agents* (08): Agents reach a Director only with `SIGNAL`, which goes to every Director currently giving the Playbook. Agents give each other Goals with `ASK <recipient> TO g` and share Facts/Events with `TELL`, with recipients a filled Placeholder, a Role or `EVERYONE`. Decide whether the Director's own way of giving Goals, Facts and Events reuses `ASK`/`TELL`. See `docs/spec/07-messaging.md`.
- From *Plan failure and fallback* (11): Agent Plans fail as in `docs/spec/11-failure.md`. Decide what a failing Director Plan does to its Plot (Phase, Staging), whether Director Statements (`ASSIGN`, `TRANSITION`, …) can fail, and how a Director reacts to a Goal it gave failing (`WHEN g FAILED FROM DIRECTOR` exists on the Agent side; the Director hears nothing in 2.0 unless the Agent signals).
- From *Time and timers* (12): `WAIT <Duration>.` is a Basic Action that pauses only its own Body (`docs/spec/12-time.md`). Decide whether a Director's Plans can use it. 2.0 has no timers or Phase timeouts, so `WAIT` in a Phase Plan is the only way to write a rough "after 30 seconds". Check how that works with leaving the Phase mid-wait.
- From *Priority model* (14): in a Director, a Phase's Plan beats a `DURING PLOT` Plan for the same Trigger by default (warning only when fully shadowed), reversible with `DURING PLOT OVER DURING <phase> [ON item]`. `TIES` can't join Phases. Decide whether Directors have a mood at all. See `docs/spec/13-plan-selection.md`.
