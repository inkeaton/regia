# Leaving two Agents out of one Role

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 03

## Question

A duel's Spectators are the Guests minus both duellists. Chapter 15 allows one `EXCEPT` per Role, so the showcase splits it: `RoyalBanquet` maps `Guest EXCEPT ?offended TO Spectator`, and `HonorDuel` gives `Wagering TO Spectator EXCEPT ?offender` and tells `Spectator EXCEPT ?offender duel_on`. The Defender still plays `Spectator` (see [*Write the 1.5 showcase Program*](03-write-the-program.md)).

Decide:

- Whether the split is how the showcase should read, with a guide note that explains it, or whether `EXCEPT` should take more than one Agent or Role (`Guest EXCEPT ?a, ?b`), in 1.5 or only in 2.0.
- If the language changes: the chapter 15 text, `R1510`, the `UNASSIGN` and narrowing rules it touches, and the showcase lines that then change.

## Resolution

`EXCEPT` takes a list, in 1.5 and so in 2.0: `MAPPING Guest EXCEPT ?offended, ?offender TO Spectator`. The Defender no longer plays `Spectator`.

- **Why.** "The Guests minus both duellists" is something a writer means. No reason for the limit was recorded, and the runtime already keeps a list of exclusions through narrowing (*Language vs game design*).
- **Syntax.** One `EXCEPT` per Role, followed by a comma-separated list. A comma followed by a keyword (`, MAPPING`, `, UNTIL EXITED`) ends the list. `EXCEPT … EXCEPT …` stays an error, and `R1510` suggests the list.
- **Items.** Roles of this Plot and filled Placeholders, in any mix. The same Role or Placeholder twice in one list is `R1510`. Two Placeholders that hold one Agent at run time are fine.
- **Everything else carries over, item by item.** `T1504` per Placeholder, while the other items still apply. A count picks from what's left. No `EXCEPT` on `UNASSIGN`, `FROM`/`BY`/Quotas, `PLAYS` or in a Playbook. A Giving to `Guest EXCEPT …` counts as made to `Guest`. Narrowing adds to the same list, and `ASSIGN P TO Guest ?who` lifts from it.
- **Spec.** Chapter 15 (*Leaving Agents out*, `R1510`, *Not in 2.0*, the ASL note) and chapter 16's setup Mapping line.
- **Showcase.** `royal_banquet.regia` maps `Guest EXCEPT ?offended, ?offender TO Spectator`. `honor_duel.regia` tells `Spectator duel_on` and gives `Wagering TO Spectator`, and the split comment is gone. The coverage row is now "on a Mapping, with a list", with a Giving and a recipient left to snippets. The README's `Wagering` row reads "Spectators".
- **Knock-on.** The inventory's F1 and F2 lose their showcase lines. *Exclusions, one Agent and a Phase in the Giving record* still decides them for the spec, now with a list, and the reference Build needs only the Mapping's list.
