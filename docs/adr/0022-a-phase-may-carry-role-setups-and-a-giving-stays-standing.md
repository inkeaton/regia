# A Phase may carry Role setups, and a Giving stays standing

What a Role should get "whenever it arrives" had three homes. The Plot's Role setup reached every Agent in every Phase. A whole-Role `ASSIGN` in a Plan was standing and reached joiners until taken away. A `TELL` or an `ASK` in the same Plan reached only who was there. We now let a `DURING <phase>` Block hold a `ROLE … STARTS WITH:` Block: it runs for every Agent of the Role when the Phase is entered and for whoever joins during it, and its Givings are taken away when the Phase is left (spec 16). A whole-Role `ASSIGN` in a Plan **stays standing**, and a Message stays a one-off (spec 19).

In the showcase, `feast` gave `Dining` with an `ASSIGN` and asked `have_dinner` two lines below. A latecomer held the Playbook, was never asked to dine, and was still counted by the Quota that waits for everyone to finish. A latecomer in `farewell` got `take_seat` from the Plot's setup and walked to its seat and to the door at once. Both are a setup that couldn't depend on the Phase.

## Considered Options

- **One strict rule: a setup is for whoever arrives, a Plan is for who is there.** A whole-Role `ASSIGN` in a Plan would become a one-off like `ASK`. It is the cleaner sentence, and it would make every Giving made on an Event miss the joiners unless a `JOINED` Plan repeats it. A Giving is a state that lasts and a Message is something that happened, and the two already differ for that reason when taken away.
- **A `STANDING` clause on `TELL` and `ASK`**: the Director would keep a list of Messages to replay, with no way to say when a replayed request has gone stale.
- **Conditions in the Plot's setup** (`IF` on the Phase): it needs the Director's own state as a condition (N7) and puts every Phase's start in one Block far from the Phase.
- **Leave it, and repeat the `ASK` in a `JOINED` Plan**: that Plan replaces the `DURING PLOT` one for the same Trigger, and has to be written per Phase.

## Consequences

- A Phase's setup, its `ENTERED` Plan and its `JOINED` Plan can now all send at entry. The setup is the one that also reaches joiners.
- Givings have a third way to end: an `UNASSIGN`, the Staging ending, or the Phase they were made for being left. `UNTIL EXITED` gives the same ending to a Giving or a Subplot made in a Plan.
- A Playbook given by the setups of two consecutive Phases is taken and given again at the transition, and its Plans stop.
- The order at entry is fixed: the Phase is current and counting, then its setups, then `ENTERED`. This also settles the Plot's setups against the initial Phase (B3).
- The difference between a standing Giving and a one-off Message remains, and chapter 19 now says why.
