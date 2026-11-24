# Findings

New spec contradictions, gaps and glossary problems found while working the *Closing the 1.5 guide's findings in the spec* map. One line each: what, where, and the ticket that found it. Handled in this map when in scope.

- Chapter 29, *Which Playbooks a Role file includes*: the showcase example says `RoyalBanquet` maps `?offender TO Defender`, a retired spelling (`R1514`); it is `AS`. Fixed in *Fix the obvious slips*.
- Chapter 36, *The top-level file of an Agent*: the combination file example included neither `unheard.asl` nor `goals.asl`, which chapter 28 says every Role or combination file includes once. Fixed with F69 in *Fix the obvious slips*: the example and the "once" bullet now include them.
- Chapters 03 and 10: `GAME` on a `NAME` had two codes, `R0311` and `R1016`. Decided in *Decide: Diagnostic codes and the Vocabulary* (`R0311` keeps it); applied in *Apply: Diagnostic codes and the Vocabulary*.
- Chapter 10, `R1014`: "a local Cue sent with … `END PLOT WITH`" can't happen, since `END PLOT` in a Playbook is already `R1507`. Decided in *Decide: Diagnostic codes and the Vocabulary* (drop the clause); applied in *Apply: Diagnostic codes and the Vocabulary*.
- ADR 0016 says a local Cue can't be an Outcome with `R1014`; that is now `R1004` (chapters 10, 17). Left as the historical record, like ADR 0030. Found by *Apply: Diagnostic codes and the Vocabulary*.
