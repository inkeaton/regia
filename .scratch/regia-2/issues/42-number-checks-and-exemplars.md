# Number the checks and add exemplar cases

Type: task
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 33

## Question

Bring every language chapter (01–21, 26) to the shape `docs/spec/27-conformance.md` sets, so the spec hands development a complete list of checks:

- Give each chapter a `## Transpiler checks` section (Errors / Warnings / Notes), gathering the checks its prose states today. Ten chapters have one already; the others keep their errors in the prose.
- Assign each check its Diagnostic code `R<chapter><nn>`.
- Write one exemplar Conformance case per chapter under `docs/spec/cases/NN-<chapter>/`, using the `#!` annotations.
- Where gathering the checks shows a gap (a rule with no error for its misuse, two chapters claiming one check), record it in a resolution comment rather than deciding it silently; a real gap becomes its own ticket.

AFK: mechanical, no design decisions. Nothing to decide beyond what chapter 27 fixes.

## Answer

Every language chapter (01–21, 26) now has a `## Transpiler checks` section with `R<chapter><nn>` codes, and every chapter that defines a runtime warning or Failure cause has a `## Trace entries` section with `T<chapter><nn>` codes. That includes the Jason Target chapters: `R2801`, `R3501`, `R3601`–`R3602`, and Trace codes in 29, 30, 32, 33 and 37. Chapter 34's list of sources became an index of where each code lives. Chapter 27 gained one rule: numbers run in order through a section, errors first, then warnings, then notes, and a later check takes the next free number. Its examples now use the real codes. There are 22 exemplar cases under `docs/spec/cases/`: one check case per chapter, except chapter 11's, which is a behaviour case (a failed Custom Action failing its Goal, with a `.trace`), and chapters 10 and 21, which are folder cases.

What gathering the checks showed, recorded rather than decided:

- **A check claimed by two chapters** was kept in one chapter, with a cross-reference in the other:
  - mixing `SUITS` Trigger Blocks, and a `TIES` pool mixing `SUITS` with unlabelled candidates, are in 13 (`R1304`, `R1309`); 14 refers to them.
  - `SUITS` on a `GIVEN` is in 14 (`R1405`), not 06.
  - a Label on a Director's Plan is in 14 (`R1406`); 20 refers to it.
  - Director Trigger kinds in a Playbook are split: `JOINED`/`LEFT`/`EMPTIED` in 19 (`R1901`), `ENTERED`/`EXITED`/`ENDED` in 20 (`R2005`).
  - an unfilled Placeholder in Director Statements is 03's `R0304`/`R0305`.
  - a failed `EXITED` (chapters 30 and 31) writes 20's `T2002` and has no code of its own.
  - an unknown key in the `JASON` group is 21's `R2113`; 36 refers to it.
- **Rules the prose states without calling them errors**, listed as errors: number forms Regia lacks (`R0401`), an import path leading to no file (`R1002`), a bare `?` in the Body (`R0306`), `SIGNAL` with something other than an Event (`R0703`), a Custom Action without `DO` (`R0803`), and a reserved reply kind word or `REFUSE` used in 2.0 (`R0706`).
- **A real gap**: no chapter states the checks on Phase declarations (a Plot with no `INITIAL` Phase or several, `DURING` or `TRANSITION TO` naming a Phase the Plot doesn't declare). New ticket: [Phase declaration checks](44-phase-declaration-checks.md). The exemplar cases assume a Plot declares exactly one `INITIAL` Phase.

## Comments

- Graduated from *How a spec chapter proves itself* (33).
- From *ASL infrastructure layout* (34): new checks to number: in chapter 10, names that differ only in case, names starting with `regia_`, and names containing `__`; in chapter 28 (a Target chapter), a Fact or Event External name that isn't a Jason atom.
- From *Trace and logging* (40): also give every chapter that defines a runtime warning or Failure cause a `## Trace entries` section with `T<chapter><nn>` codes, from the list of sources in `docs/spec/34-trace.md`, including the Jason Target's own (chapters 29–33). Behaviour cases now exist (chapter 34), so a chapter whose exemplar is about run time can use a `.trace` case.
- From *.jcm generation* (41): chapter 36 adds checks (a port past 65535, an invalid `base_port`) and the known `JASON` keys `strategy`, `address`, `base_port`, `trace_console`; and a `TEMPER` `cast` Trace entry (chapter 34).
- From *Custom Actions through VEsNA* (43): chapter 37 adds Jason Target Trace warnings (an Action reply with an unknown or finished `id`, an unknown message type at the Root Director's body), and the `action` entry now has sent and `DONE`/`FAILED`/`REFUSED` forms (chapter 34).
