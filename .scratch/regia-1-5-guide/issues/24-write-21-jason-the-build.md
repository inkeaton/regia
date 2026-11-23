# Write guide chapter 21, Jason: the Build

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
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

## Resolution

Done on 2026-11-23 (AFK). [`docs/guide/21-jason-the-build.md`](../../../docs/guide/21-jason-the-build.md) written from the template, with the banquet's whole Build worked out by hand: the Build tree, the four Role files and what each includes (every Root Plot Role gets `Duelling` and `Keeping_watch` through `MAPPING ?offender AS Defender` and `ASSIGN Keeping_watch TO ?winner`), the combination file `Guard__Guest.asl` for `knight_1` and `percival`, the `.jcm` with fourteen Agents on ports 9081–9094, `cast.json`, `regia_start_cast`, the hothead's `regia_instance_setup` plan and `regia_kind`.

- Sections: *The Build folder*, *Role files*, *Shared Infrastructure*, *The Java library*, *Names* (with *External names*), *The game link*, *The clock*, *The `.jcm`* (with *Starting names*, *Ports*), *The top-level file of an Agent*, *Drawing `RANDOM`*, *`cast.json`*, *The Root Director's file* (with *Setup lines*, *Agent kinds: `regia_kind`*), *How this combines with…*.
- Every Agent of the banquet gets a `temper` with all three Propensities, the king and the servants neutral, because `Duelling` reaches every Role.
- "In 2.0" notes: `regia_quota` (Quota counts), and the `regia_join` body fields with creating a joiner from `regia_kind`.
- Checks borrowed: `R1007`–`R1009` (names), `T1101` (`no game link`), `R2113`, `T1902`; own: `T2801`–`T2803`, `R3601`–`R3603`.
- No `Guide:` line: the showcase README's *Coverage* has no heading for chapter 28 or 36.
- Re-read against chapters 28, 29, 30, 33, 36 and 14; grep for retired spellings and glossary _Avoid_ words (*Temper*, temper selection) clean; humanizer pass done.

**Findings** (non-blocking, in `findings.md`): chapter 29's `temper` for `king` misses `aggressiveness`; the order of Propensities in `temper` is unsaid; chapter 36's examples aren't the showcase and miss a `[mood]`; `regia_kind` has no reader in 1.5; a Role file's include order, where `regia_game` lives and the setup catch-all's form are unsaid.
