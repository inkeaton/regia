# Number the checks and add exemplar cases

Type: task
Status: open
Blocked by: 33

## Question

Bring every language chapter (01–21, 26) to the shape `docs/spec/27-conformance.md` sets, so the spec hands development a complete list of checks:

- Give each chapter a `## Transpiler checks` section (Errors / Warnings / Notes), gathering the checks its prose states today. Ten chapters have one already; the others keep their errors in the prose.
- Assign each check its Diagnostic code `R<chapter><nn>`.
- Write one exemplar Conformance case per chapter under `docs/spec/cases/NN-<chapter>/`, using the `#!` annotations.
- Where gathering the checks shows a gap (a rule with no error for its misuse, two chapters claiming one check), record it in a resolution comment rather than deciding it silently; a real gap becomes its own ticket.

AFK: mechanical, no design decisions. Nothing to decide beyond what chapter 27 fixes.

## Comments

- Graduated from *How a spec chapter proves itself* (33).
- From *ASL infrastructure layout* (34): new checks to number: in chapter 10, names that differ only in case, names starting with `regia_`, and names containing `__`; in chapter 28 (a Target chapter), a Fact or Event External name that isn't a Jason atom.
- From *Trace and logging* (40): also give every chapter that defines a runtime warning or Failure cause a `## Trace entries` section with `T<chapter><nn>` codes, from the list of sources in `docs/spec/34-trace.md`, including the Jason Target's own (chapters 29–33). Behaviour cases now exist (chapter 34), so a chapter whose exemplar is about run time can use a `.trace` case.
- From *.jcm generation* (41): chapter 36 adds checks (a port past 65535, an invalid `base_port`) and the known `JASON` keys `strategy`, `address`, `base_port`, `trace_console`; and a `TEMPER` `cast` Trace entry (chapter 34).
- From *Custom Actions through VEsNA* (43): chapter 37 adds Jason Target Trace warnings (an Action reply with an unknown or finished `id`, an unknown message type at the Root Director's body), and the `action` entry now has sent and `DONE`/`FAILED`/`REFUSED` forms (chapter 34).
