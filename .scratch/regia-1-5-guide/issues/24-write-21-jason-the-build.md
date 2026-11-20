# Write guide chapter 21, Jason: the Build

Type: task
Status: open
Assignee:
Blocked by: 05

## Question

Write `docs/guide/21-jason-the-build.md`, *Jason: the Build*, as listed in the chapter list (`../prototypes/chapter-list-outline.md`).

- **Spec:** 28, 36.
- **Covers:** files, names, Shared Infrastructure, the Java library, the game link, the clock, the `.jcm`, starting names, ports, `cast.json`, `regia_kind`, setup lines.
- **Quotes most:** `banquet.regin`, a throwaway Build tree.
- **"In 2.0" notes:** the `regia_join` body fields.

Write it from the template in the map's Notes (fixed by *The chapter template, fixed by a sample chapter*), with that sample, `docs/guide/10-messages.md`, open beside it. Write fresh against the spec and the showcase; the old `docs/guide/` chapters are source material only.

Then:

- add a `Guide: [<title>](../guide/<file>)` line under the showcase `README.md`'s *Coverage* heading of each spec chapter above;
- re-read every example against the cited spec chapters, and grep the chapter for retired spellings (spec chapter 01's table);
- a last pass with `humanizer:humanizer`;
- anything the spec gets wrong goes to `findings.md`.

Done when the chapter is in `docs/guide/` and the checks above pass.
