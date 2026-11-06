# Basic Action set

Type: grilling
Status: open
Blocked by: 03, 05, 08

## Question

What is the final set of Basic Actions, and what are their names (primer ch.4)? Starting from `PRINT`, `BELIEVE`, `FORGET`, `ACHIEVE`, `WAIT`, `BROADCAST`, `TELL`, `SIGNAL`: rename `ACHIEVE` to `PURSUE`? Add `DISCARD` to drop a Goal? Anything else (e.g. Actions over Groups)? Confirm that only Custom Actions take `DO`, and check every name against the readability rule.

## Comments

- From *Numbers and arithmetic* (04): changing a numeric Fact is `FORGET health(?h)` then `BELIEVE health(?h - ?dmg)` for now. Decide whether a single replacing Basic Action is worth adding, and its name. Also decide how `PRINT` joins text and values (there is no `+` on strings; the spec examples use `PRINT("Ouch! Lost", ?dmg)`). Arithmetic must work inside any Basic Action's arguments. See `docs/spec/04-numbers-and-expressions.md`.
- From *Goals and Trigger kinds* (05): a Body can give itself a Goal and **wait** for it, or start it and carry on; both must exist. Decide their syntax (e.g. `PURSUE g AND WAIT`) and which is the default. Also the action that drops a Goal (it fires `WHEN g DROPPED`). Fact Triggers are written `LEARNED`/`FORGOTTEN`, so check that the Fact action names read well next to them. See `docs/spec/05-goals-and-triggers.md`.
- From *Messaging between Agents* (08): sending is `TELL <recipient> <fact or event>.`, `ASK <recipient> TO <goal>.` and `SIGNAL <event>.`; `BROADCAST` became the recipient `EVERYONE`. Confirm these names next to the rest of the set. Message Statements may later take trailing `,` clauses (`ASK ?g TO find_sword, AND WAIT`); decide whether self-pursuit's "wait" uses the same shape so both line up. `REFUSE`, `TOLD`, `AGREED`, `REFUSED`, `REACHED`, `FAILED` are reserved. See `docs/spec/07-messaging.md`.
