# Messaging between Agents

Type: grilling
Status: resolved
Blocked by: 03
Assignee: Edoardo Vassallo

## Question

How do Agents communicate (primer ch.4, Q4e of the charting session)? Can a `TELL` target a Role, a specific Agent, or both? What can a message carry (a Fact, a Goal, a request), and what does the receiver see (an Event? a Fact?)? How does `BROADCAST` relate to Plots and Roles? How does a `SIGNAL` reach the right Director when an Agent is in several Plots?

## Comments

- From *Goals and Trigger kinds* (05): anything sent can be matched with `FROM Role`, `FROM ?who`, `FROM Role ?who` or `FROM DIRECTOR` (any Director whose Plot gives this Playbook). Decide the sender forms for messages between Agents, how another Agent gives a Goal, and whether `SIGNAL` picks its Director the same way as `FROM DIRECTOR`. The sender is never a hidden annotation, only `FROM`. See `docs/spec/05-goals-and-triggers.md`.

## Answer

Spec chapter: `docs/spec/07-messaging.md`. Spec 05 fixed (`FROM` valid on `LEARNED`, an error on `FORGOTTEN`). Glossary: Message and Recipient added; Signal and Sender revised. No ADR: hiding Fact sources is reversible, since ASL keeps them underneath.

- **Three Statements:** `TELL <recipient> <fact or event>.`, `ASK <recipient> TO <goal>.`, `SIGNAL <event>.` The kind of a name picks the right verb; the wrong one is an error with a hint. Final names confirmed in *Basic action set*.
- **Recipients:** a certainly-filled Placeholder holding an Agent, a Role (its Agents except the sender), or `EVERYONE` (every Agent in the game except the sender). Regia never names an Agent: a Value as recipient is an error. One recipient per Statement. `BROADCAST` is gone.
- **Signals** go to the Directors of every Plot currently giving the Playbook that contains the `SIGNAL`, the same set as `FROM DIRECTOR`. Events only, no recipient, and the only way an Agent reaches a Director.
- **Failures:** a recipient that isn't an Agent at runtime fails the Plan; an empty Role or `EVERYONE` alone sends nothing.
- **Delivery:** sending never waits; per sender-receiver order is kept; nothing is lost.
- **Messages only add.** Undoing (forget a Fact, drop a Goal) is not in 2.0.
- **Receiving:** a told Fact is the receiver's own, with no source kept; `LEARNED FROM ?who` fires only if new; `FORGET` removes it completely; `FORGOTTEN` has no Sender. A told Event is the same as a game Event, told apart by `FROM`. An asked Goal is the receiver's own Goal. Sender forms are the existing `FROM` forms.
- **Room for cooperation:** `ASK` means a request (a future `REFUSE` fits); `AGREED`/`REFUSED`/`REACHED`/`FAILED` reserved as Goal kind words for replies; message Statements may later take trailing `,` clauses (any is an error in 2.0); no conversation ids, the Goal's arguments plus `FROM` identify a request; `TOLD` reserved for Fact provenance.
