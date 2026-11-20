# Roles an Agent reads

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Group E of the [inventory](../jason-open-questions.md#e-roles-read-by-an-agent-and-which-files-hold-a-playbook-roles-an-agent-reads): counted recipients and `PLAYS` in Jason, and which Role files hold a Subplot's Playbooks reached through `MAPPING ?who`.

Decide:

- how an Agent draws `TELL 50 PERCENT OF peer` and `ASK 1 OF waiter`, and how a share rounds;
- `?x PLAYS peer` in an Agent, inside `COUNT` and a `WEIGHT` Pick too;
- `PLAYS` in a Director;
- the reach rule for `MAPPING ?who TO r`, and what it does to `temper` emission (does `king` get one?).

Closes when chapters 29 and 30 (and chapter 15's notes) are edited.

## Resolution

Grilled with the user on 2026-11-18. Recorded in chapter 29 (*Who plays a Playbook Role*, *What reads it*, the reach rule), chapter 30 (*Who plays a Role here*), chapter 39 (*Contexts and `GIVEN`*, *Sending*), chapter 35's internal actions, chapter 15's ASL notes and chapter 14's emission rule 2.

1. **One reading of a Playbook Role**: a rule in `regia/agent.asl`, `regia_plays(Playbook, Role, Agent)`, over every `regia_given` of the Playbook. `live(cast)` reads every `regia_cast(D, _, A)`, `live(R)` reads `regia_cast(D, R, A)`, and `fixed(L)` reads `L`. It leaves the Agent itself in. `TELL host`, counted recipients, `PLAYS`, `FROM host` and Quotas all read it, and generated code never reads `bind` itself, so *Exclusions, one Agent and a Phase in the Giving record* extends this rule only.
2. **`PLAYS` in an Agent** is the conjunct `regia_plays(p, r, X)`, and `ME PLAYS r` is `.my_name(Me) & regia_plays(p, r, Me)`. Inside `COUNT`, a Pick or `FOR EACH` it is one more conjunct in the `.setof`, which removes an Agent reached through two Givings.
3. **A counted recipient**: the pool is `.setof(A, regia_plays(p, r, A) & A \== Me, Pool)`, taken each time the Statement runs. Then `regia.pick(count(N) | share(S), Pool, Picked)` draws from the run's one seeded source, uniformly and without replacement, and a `regia.send` goes to each picked Agent. A share rounds up against the pool with the sender already left out (50 PERCENT of 7 other peers is 4). It writes `T1502` and `T1503`, and fails only on a count that isn't a Number. The Director's counted picks call the same Java (and write `T1501` instead of failing).
4. **`PLAYS` in a Director**: `regia_plays(Role, A)` in `regia/director.asl` over `regia_cast(Me, Role, A)`, with `cast` meaning every Role. `COUNT(? PLAYS Guest)` is always `.setof` plus `.length`, never `.count`, so a knight is counted once under `CAST`.
5. **Reach of `MAPPING ?who TO r`**: the same as `ASSIGN … TO ?who`. In Plot X, `r`'s Playbooks are reachable for every Root Role that maps to any Role of X. In the showcase every Root Role includes `Duelling`, so `king` and the `servant` kind get a `temper` (`bravery`, `sympathy`). That is harmless, and the Jason guide notes it as a visible effect of reach.
6. **Placement**: the rule and the reach in chapter 29, the Director's rule in chapter 30, the compiled forms in chapter 39, and `regia.pick` in chapter 35. Chapters 15 and 14 point to them.
