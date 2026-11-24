# Decide: Runtime order and behaviour cases

Type: grilling
Status: open
Assignee:
Blocked by:

## Question

What happens, and in which order, where the spec doesn't say?

- F31: what does a failing `EXITED` Plan do to the transition it runs inside (`ENTER` step 2, `END PLOT`)? (Guide: the Plan stops and the transition goes on.)
- F35: where does `EMPTIED` for a Role that starts empty fall, in chapter 20's steps and relative to `DURING PLOT`'s `ENTERED`? (Guide: after the setups, before both `ENTERED` Plans.)
- F37: what does `ASSIGN P TO ?who` or `MAPPING ?who AS r` do with `?who` from `LEFT`, and which code does it write?
- F38: when a leaver played in several Stagings, in which order do the Directors hear it? Can a Subplot's `END PLOT` from its `EMPTIED` Plan reach the parent before the parent's own `LEFT`? (Guide: no order.)
- F50: may a case's script set percepts or Action rules before `> start`, so the first settle doesn't miss them? (Guide: only `> fact link`; every Guest starts without a seat.)
- F51: when does the virtual clock jump: before the next step, and after the last step? What is `> wait` for? (Guide: before the next step, never after the last.)

Start each question from the guide's reading. Mark which answers need an ADR.

Applying the answers is *Apply: Runtime order and behaviour cases*.
