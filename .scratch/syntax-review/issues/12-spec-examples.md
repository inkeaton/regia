# Spec examples after the review

Type: task
Status: closed
Assignee: claude
Blocked by: 02, 03, 04, 05, 06, 07, 08, 09, 10, 11

## Question

AFK. Once every syntax ticket is closed, sweep `docs/spec/` chapters 01–21 and 26, `GLOSSARY.md` and the ADRs for examples still written in an old spelling. Fix what the tickets left behind, including inventory §4 item 5 (a Statement after a `GIVEN` Block, `18-quota-triggers.md:105`) and anything else from §4 that no ticket covered. Drop the trailing `.` at the end of example lines (some 290 of them): indentation and new lines are the house style, and `.` appears only where two Statements share a line (*`.`, `;` and the Block styles*). Chapter 02's `DO eat_food.  # …` lines stay, since they show `.` before a comment. Also gather every chapter's *Reserved words* list into one list in chapter 01 (ADR 0041: all keywords are reserved), and leave each chapter a pointer to it. Record which files changed. No design decisions are made here: anything that needs one goes back to the map as a new ticket.

## Resolution

Done by claude (AFK) on 2026-11-20.

- **Old spellings.** A sweep for every retired spelling (`STARTS WITH`, `PERCENT OF`, `EITHER:`/`OR:`, `AT RANDOM`, `EXITED BY`, `ENDED WITH`, `WITHOUT OUTCOME`, `END SUBPLOT`, `CHANGE … TO`, `TRANSITION TO`, `MAPPING … TO`, `UNASSIGN`, `?x = e`, `NOT ?a = ?b`, clause keywords without `,`, `AND` in lists) found none left outside the error entries and history sentences that name them on purpose. The tickets had already carried their own renames.
- **Inventory §4.** Items 1–4 were already fixed by their tickets. Item 5: in chapter 18's `SENT` example, `ENTER fighting` moved inside the `GIVEN` Block, so no Statement follows a `GIVEN` Block (`R0603`).
- **Trailing `.`.** Removed from 305 lines in ```` ```regia ```` and ```` ```regin ```` examples (chapters 03–21 and 26; chapter 01 had none) and from about 190 inline code spans in prose (chapters 03–21, 26, `GLOSSARY.md` and 15 ADRs), including Statement shapes like `WAIT <Duration>` and the hint in chapter 10's sample error output. Where the `.` inside a span had also ended the sentence, the full stop now follows the span (13 places). Kept: chapter 02's `.`-before-a-comment lines and its doc-comment text, chapter 01 (where `.` is the subject), Inline blocks whose inner `.` separates Statements, and `docs/spec/cases/` (conformance inputs, not in this ticket; four of them are retired spellings on purpose).
- **Reserved words.** Chapter 01 has a new section, *Reserved words*: every keyword once, by family, with the chapter that specifies it, plus the retired spellings that stay reserved (`EVENT`, `EITHER`, `PERCENT`, `STARTS`, `OUTCOME`) and the draft words that aren't in the language. It was checked against every uppercase word in the spec's examples. The *Keywords* principle points to it, and the sentence saying some chapters still show older spellings is gone. Chapters 04, 07–20 and 26 now hold a one-line pointer in their *Reserved words* section.
- **Back to the map.** Chapters disagree on whether a retired keyword stays reserved: 09, 15, 16 and 17 say so for theirs, while `CHANGE`, `TRANSITION`, `UNASSIGN`/`UNASSIGNED` (and `.regin`'s `=`) have an error with a hint but no statement. The list records only what the chapters say. That question went to *Retired spellings and their codes*.
- **Files changed:** `docs/spec/01`, `03`–`21` and `26` (all but `02`), `GLOSSARY.md`, ADRs 0001, 0002, 0005, 0007, 0009, 0017, 0019, 0023, 0024, 0033, 0035, 0038, 0042, 0043, 0046.
