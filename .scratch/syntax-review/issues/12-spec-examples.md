# Spec examples after the review

Type: task
Status: open
Assignee: claude
Blocked by: 02, 03, 04, 05, 06, 07, 08, 09, 10, 11

## Question

AFK. Once every syntax ticket is closed, sweep `docs/spec/` chapters 01–21 and 26, `GLOSSARY.md` and the ADRs for examples still written in an old spelling. Fix what the tickets left behind, including inventory §4 item 5 (a Statement after a `GIVEN` Block, `18-quota-triggers.md:105`) and anything else from §4 that no ticket covered. Drop the trailing `.` at the end of example lines (some 290 of them): indentation and new lines are the house style, and `.` appears only where two Statements share a line (*`.`, `;` and the Block styles*). Chapter 02's `DO eat_food.  # …` lines stay, since they show `.` before a comment. Also gather every chapter's *Reserved words* list into one list in chapter 01 (ADR 0041: all keywords are reserved), and leave each chapter a pointer to it. Record which files changed. No design decisions are made here: anything that needs one goes back to the map as a new ticket.
