# Decide: Jason Target forms

Type: grilling
Status: open
Assignee:
Blocked by:

## Question

Which forms does the Jason Target fix, and which are left to the Transpiler? For each one, decide whether the spec fixes the form or says plainly that it's the Transpiler's choice.

- F68: in which order are a `temper`'s Propensities written? (Guide: Vocabulary declaration order.)
- F70: what reads `regia_kind` in 1.5, or is it written for 2.0 only? (Guide: nothing reads it.)
- F71: what is the order of a Role file's includes and initial beliefs, which file carries `regia_game`, and what form does `regia_instance_setup`'s catch-all take?
- F72: what is the sender's name bound to: `Me` (which clashes with `?me`) or `Regia_me`? (Guide: `Regia_me`.)
- F73: what is the ASL of `DO a, WITHOUT WAITING`, and how does `regia.act` know to return on `accepted`?
- F74: how does `UPDATE`'s test get the `seq` for `regia_because`, and what form do `LEARN`'s and `FORGET`'s guards take?
- F75: does `SIGNAL` write one `message` entry, or one per Director? (Guide: one per call, following 39.)
- F77: which Item do `WHEN REMOVED`'s plans carry? (Guide: `removed`.)
- F84: should `regia_cast_copy` be added to a *Messages* table? What name and form does a setup line's subgoal take? (Guide: `regia_setup_line__1`, marked as its own.)

Start each question from the guide's reading. Mark which answers need an ADR.

Applying the answers is *Apply: Jason Target forms*.
