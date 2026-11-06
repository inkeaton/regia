# Director capabilities

Type: grilling
Status: open

## Question

What can a Director do and know (primer ch.5)? Decide the `WORLD` keyword (rename?), whether the Director has its own Facts (whose Facts does a Plot Context read?), whether it receives world Events directly, and whether it should have Goals or stay a simple state machine (what would richer Directors give us?).

## Comments

- From *Goals and Trigger kinds* (05): `ON ENTER` / `ON EXIT` are retired; Phase entry and exit are `WHEN` Triggers. Decide their wording (e.g. `WHEN ENTERED:`). Also decide how a Director gives a Goal to a Role or to an Agent filled by `FROM Guest ?who`, and what it can do with `?who`. Signals arrive as Events and can be matched with `FROM Role [?who]`. See `docs/spec/05-goals-and-triggers.md`.
- From *Messaging between Agents* (08): Agents reach a Director only with `SIGNAL`, which goes to every Director currently giving the Playbook. Agents give each other Goals with `ASK <recipient> TO g` and share Facts/Events with `TELL`, with recipients a filled Placeholder, a Role or `EVERYONE`. Decide whether the Director's own way of giving Goals, Facts and Events reuses `ASK`/`TELL`. See `docs/spec/07-messaging.md`.
