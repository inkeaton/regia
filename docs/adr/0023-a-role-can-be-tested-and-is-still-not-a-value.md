# A Role can be tested, and is still not a Value

In a Playbook a Role was only an address: a recipient or a `FROM`. The one way from a Role to an Agent was a Message arriving from it. We now add the condition `<who> PLAYS <Role>`, in Plots and Playbooks, matched like a Fact so that it fills a Placeholder (spec 15). A Role name as an argument or in an Expression stays an error.

In the showcase, `DO lunge` had no target because a duellist couldn't name its `opponent`. The Director of `HonorDuel` couldn't name its one `Challenger`, so the winner Signalled `duel_won` to hand the Director a name the Director had given out, and `duel_abandoned` couldn't say who had been duelling. The Host's Plans sat in a Playbook every Servant held, with no way to ask "am I the host".

## Considered Options

- **Roles as Values** (`DO lunge(opponent)`, `hates(host)`): the shortest to write. A Role is a set that changes, so the Value would mean one Agent in some places and many in others, and a Fact holding a Role would have to be re-read whenever the Cast changes.
- **A Placeholder on the recipient** (`TELL opponent ?o …`): it names an Agent only at the moment of sending, and gives nothing to a `DO` or to a Director ending a Plot.
- **The Mapping hands over the Agent as a Fact** when the Playbook is given: it would go stale for a live whole-Role binding, the thing chapter 15 avoids.
- **Leave it, and keep the Signal**: the workaround says the opposite of what happens, and it is the one a reader of the showcase is most misled by.

## Consequences

- `PLAYS` is checked live, like `FROM host`: in a Playbook over the union of the Givings held, in a Plot in this Staging.
- It doesn't leave the Agent itself out, unlike a recipient. `ME PLAYS host` needs that, and a Plan that wants someone else writes `AND NOT ?o = ME`.
- Counting a Role comes with it (`COUNT(? PLAYS Guest)`), which also gives a Director part of what it couldn't ask about itself (N7).
- It is a condition only. An Agent still doesn't hear of cast changes.
- `PLAYS` now has two uses with one meaning: Instancing's `AGENT noble PLAYS Guest` and the condition.
