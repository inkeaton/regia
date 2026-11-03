# Messaging between Agents

Type: grilling
Status: open
Blocked by: 03

## Question

How do Agents communicate (primer ch.4, Q4e of the charting session)? Can a `TELL` target a Role, a specific Agent, or both? What can a message carry (a Fact, a Goal, a request), and what does the receiver see (an Event? a Fact?)? How does `BROADCAST` relate to Plots and Roles? How does a `SIGNAL` reach the right Director when an Agent is in several Plots?

## Comments

- From *Goals and Trigger kinds* (05): anything sent can be matched with `FROM Role`, `FROM ?who`, `FROM Role ?who` or `FROM DIRECTOR` (any Director whose Plot gives this Playbook). Decide the sender forms for messages between Agents, how another Agent gives a Goal, and whether `SIGNAL` picks its Director the same way as `FROM DIRECTOR`. The sender is never a hidden annotation, only `FROM`. See `docs/spec/05-goals-and-triggers.md`.
