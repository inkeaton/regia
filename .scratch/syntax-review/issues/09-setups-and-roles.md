# Setups and `ROLE`

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 01, 05

## Question

In a Body, `LEARN` and `PURSUE` are the Agent's own Actions. In `ROLE X STARTS WITH:`, `CAST STARTS WITH:` and an Instancing `KIND`/`AGENT` Body, they are the Director's tell and ask (chapter 16, kept once already in the revision's *Words and syntax*). `ROLE` declares a played Role in a Plot and an address in a Playbook, and inside `DURING` it declares nothing (`ROLE Guest STARTS WITH:` there names a Role the Plot already has).

*`BY`, `WITH`, `WITHOUT`, `AT` and `UNTIL`* found that `WITH` in `STARTS WITH:` fails the one-meaning test (elsewhere it introduces the Cue an ending carries), so the header must change: pick its new spelling here, with a retired-spelling error and hint. With the new principles in hand, decide whether setups keep the Body words, whether a Phase's setup keeps the `ROLE` header, and whether a Playbook's Roles keep the Plot's word. Fix the setup example that breaks chapter 16 at `17-subplots.md:31` (no `ROLE`, a `TELL`, a Placeholder) as part of it. Done when chapters 15, 16, 17 and 21 and `GLOSSARY.md` are edited.

## Resolution

Grilled with the user on 2026-11-20. ADR 0046 (`docs/adr/0046-a-roles-block-is-its-setup.md`).

1. **`LEARN` and `PURSUE` stay** in setups and on `KIND`/`AGENT`. They pass the one-meaning test with a gloss read from the Agent's side ("comes to know", "takes on"). Only the source differs, and it follows from where the line is written. Chapter 16's *Sender* no longer says they "don't mean the Agent's own Actions". Chapter 21 notes the shared gloss.
2. **A Role's Block is its setup:** `ROLE Guest:` and `CAST:`, at Plot level and inside `DURING`. `STARTS WITH:` is retired (`R1608`, `STARTS` stays reserved for the hint). Inside `DURING`, `ROLE` names a Role without declaring it, as `DURING PLOT` does, and it passes as a noun. `R1601` is now only "a Block on a Playbook's Role".
3. **A Playbook keeps `ROLE`** for its addresses (chapter 15 says why). It takes no Block.
4. **A setup may use the Plot's parameters.** Any other Placeholder is still `R1604`. The example at `17-subplots.md:31` became `ROLE Challenger: LEARN grievance(?quarrel).`

Edited: chapters 15, 16, 17, 20, 21, 30; `GLOSSARY.md` (**Role setup**); cases in 11, 13, 16, 19, plus the new `16-role-setup/retired-starts-with.regia` and `plot-parameter-in-a-setup.regia`. ADRs 0022 and 0024 are left as historical records, since they quote the old header.
