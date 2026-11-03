# Director capabilities

Type: grilling
Status: open

## Question

What can a Director do and know (primer ch.5)? Decide the `WORLD` keyword (rename?), whether the Director has its own Facts (whose Facts does a Plot Context read?), whether it receives world Events directly, and whether it should have Goals or stay a simple state machine (what would richer Directors give us?).

## Comments

- From *Goals and Trigger kinds* (05): `ON ENTER` / `ON EXIT` are retired; Phase entry and exit are `WHEN` Triggers. Decide their wording (e.g. `WHEN ENTERED:`). Also decide how a Director gives a Goal to a Role or to an Agent filled by `FROM Guest ?who`, and what it can do with `?who`. Signals arrive as Events and can be matched with `FROM Role [?who]`. See `docs/spec/05-goals-and-triggers.md`.
