# What the Jason chapters leave open

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 03

## Question

Walk spec chapters 28–37 against the written showcase Program, construct by construct, and list every question a hand-written Jason reference Build would hit that the spec doesn't answer.

Done when:

- each question is stated sharply, with the chapter it belongs to and the showcase line that raises it;
- the questions are grouped by subject, each group sized for one decision ticket;
- the revision map's Jason fog and the old README's *Review notes* on chapters 30, 31, 34 and 35 are checked off against the list.

The groups graduate into decision tickets on this map.

## Resolution

The inventory is [*What the Jason chapters leave open*](../jason-open-questions.md). It walks chapters 28–37, and the *ASL mapping notes* of the language chapters they build on, against every file of `docs/showcase/`. Each question names its chapter and the showcase lines that raise it.

**Thirteen groups, thirteen tickets.** One research ticket holds the facts about Jason and VEsNA-Pro's `Temper` that several decisions wait on: [*How Jason behaves where the translation waits*](10-jason-facts.md). Twelve grilling tickets hold the decisions:

- [*A Plan's Statements in ASL*](11-statements-in-asl.md): where Statement translations live, variable names, `FOR EACH`, `WAIT … UNTIL`.
- [*Messages and told Facts in ASL*](12-messages-in-asl.md): a told Cue's form, Signals, catch-alls, told Facts learned once, `ME`.
- [*A Goal's life in ASL*](13-goal-life-in-asl.md): Pursuit identity, ending events, Reasons, `DROP`, `PURSUING`.
- [*Roles an Agent reads*](14-roles-an-agent-reads.md): counted recipients, `PLAYS`, the reach of `MAPPING ?who`.
- [*Exclusions, one Agent and a Phase in the Giving record*](15-giving-record.md).
- [*A Playbook's opening and closing in ASL*](16-opening-and-closing.md): chapter 29 brought up to ADR 0021.
- [*What a Staging runs when it starts*](17-staging-start.md): `!regia_begin`'s data, `CAST` setup, `EMPTIED` at start, kinds' setup lines.
- [*Entering and leaving a Phase in ASL*](18-phase-change.md): Phase setups and Givings, `UNTIL EXITED`, `AFTER`, `IN`, a waiting `DO` in `EXITED`.
- [*Subplot arguments and endings in ASL*](19-subplot-endings.md): chapter 31 brought up to ADR 0030.
- [*Moods and Labels on VEsNA-Pro*](20-moods-on-vesna.md): negative Moods, `SHIFTS` on a lone Plan, the `Temper` hooks.
- [*The Target's own code in a Build*](21-target-code.md): where `hall.music.fanfare` lives.
- [*The Trace's fields and entries*](22-trace-pieces.md).

**Two findings stand out.** Chapter 31 is behind ADR 0030: it has the parent hear nothing for `END SUBPLOT` and run only the first matching `ENDED` Block. Read as written, a Subplot's `DO` in `EXITED BY PARENT` while the Root ends is never answered, and the Root waits for that child forever (`honor_duel.regia:74`, `poisoning.regia:20`). And chapter 14's Moods in [-1, 1] meet VEsNA-Pro's [0, 1], while the showcase starts Moods below zero.

**Checklists.** Every item of the revision map's Jason fog, and every *Review note* on chapters 30, 31, 34 and 35, is ticked off at the end of the inventory: placed in a group, covered by the spec as it now stands, or not raised by the showcase (2.0-only, or not exercised). Not raised: Goal-ending reports to an asker, `FROM GAME`/`FROM ME`, Quotas, joiners, `CAST` beyond its setup, `UNASSIGN … FROM CAST ?who` and plain `FROM ?who`, a Director's `PERCENT` pick.

Changed: nothing in the spec, ADRs or glossary. The decisions close by editing chapters 28–37.
