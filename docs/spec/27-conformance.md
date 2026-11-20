# Conformance

How a spec chapter shows that it is complete and correct, in a form a Transpiler can be tested against. Decided in the ticket *How a spec chapter proves itself* (`.scratch/regia-2/issues/33-spec-conformance.md`). It covers the language chapters only: 01–21 and 26. The architecture chapters (22–25) describe how the tools are built, not what the language means, and have no Conformance cases.

## What a case checks

A **Conformance case** is a small Program with the outcome the spec promises for it. There are two kinds:

- A **check case** gives the exact Diagnostics the Transpiler reports for it: which errors and warnings, by Diagnostic code and line. It may also say there are none (an accepting case).
- A **behaviour case** adds a scripted run (Cues from the game, Agents joining and leaving) and gives the Trace that run is expected to leave.

Emitted ASL is **not** part of the spec. The spec promises what a Program means, not one way of writing it in a Target, so a golden `.asl` file would freeze one particular lowering. The development effort may keep ASL snapshot tests of its own; they aren't Conformance cases.

The `.trace` format, the script of a run and how a Trace is matched are in chapter 34. Behaviour cases run against a scripted stand-in for the game (chapter 35, ADR 0014).

## Diagnostic codes

Every error and warning a language chapter defines has a stable **Diagnostic code**: `R`, the chapter's two digits, then two digits numbering the check within the chapter. Chapter 13's first error is `R1301`. The `code` field of a Diagnostic (chapter 23) carries it, and each code has a docs page.

Numbers run in order through a chapter's section, errors first, then warnings; a check added later takes the next free number, whatever its severity. Codes are never reused. A check that is dropped keeps its number, marked retired in its chapter. A check that changes severity keeps its number too, so the severity is printed beside a code and never read from it.

This shape is kept for 2.0 because codes must be stable and findable from the spec. It isn't readable or memorable: `R13` means Plan selection only to someone who knows the spec's table of contents. A better shape is deferred past 2.0, and will have to map every code already given.

Every language chapter lists its checks in a `## Transpiler checks` section, grouped as **Errors** and **Warnings**, each with its code:

```markdown
## Transpiler checks

**Errors**

- `R1301` A cycle in one Plot's relations (the message prints the cycle).

**Warnings**

- `R1305` A competition ordered only by name.
```

A chapter may still explain a check in its prose; the section is where the check is listed and numbered.

## Case files

Cases live beside the spec, one folder per chapter:

```
docs/spec/cases/
  13-plan-selection/
    precedence-cycle.regia
    tied-playbooks-without-suits.regia
  21-instancing/
    root-plot-named/
      banquet.regia
      duel.regia
      game.regin
```

- A case is one `.regia` file, or a **folder** when it needs several files (Imports, Instancing). The name is a slug saying what it exercises.
- In a folder case, the Entry is the `.regin` file at its root if there is one; otherwise every `.regia` file in the folder is the Entry of a Program of its own, as on the command line (chapter 10).
- A **behaviour case** is always a folder, with a `.trace` file and a `.regin` Entry naming its `ROOT`, since only a `.regin` Entry can be built and run (chapter 21). The `.trace` format is in chapter 34.

The format is not only the spec's: `regia test` (chapter 23) runs cases of this form written by anyone, so a writer can keep cases for their own Program.

The spec owns its cases. The development effort copies or vendors them into the Transpiler's test suite and doesn't edit them there; a disagreement with a case is a change to the spec.

## Annotations

A case states what it expects in **annotations**: comments starting with `#!`. To the language they are plain comments (chapter 02); only the test runner reads them.

**Header.** The first lines of a case file, before any code:

```
#! case: two Playbooks ordered over each other form a cycle
#! rule: R1301
```

- `case:` says in one line what the case shows.
- `rule:` names the chapter and the section, or the check's code, that the case exercises. A case may name several rules, one line each.
- `ok` (`#! ok`) marks an accepting case: the Program has no Diagnostics at all.
- `regia:` (`#! regia: 2.0`) marks a case that needs a system Regia 1.5 leaves out, so a 1.5 runner skips it. `#! regia: 1.5` marks a case that shows a 1.5 refusal (`R0109`, `T1902`), so a 2.0 runner skips it. A case without the line runs on both (*Regia 1.5*, below).
- Cases are matched as with `--all-warnings`: a warning silenced by `#@allow` (chapter 02) is still annotated, so a case can show what an allow covers.

**Expected Diagnostics.** An annotation after code expects a Diagnostic whose primary span starts on that line:

```
    PRECEDENCE:
        Brawling OVER Drunkard.
        Drunkard OVER Brawling.      #! error R1301
```

On a line of its own, `#!^` points at the line above. Use it where a trailing comment can't go, such as after a single-line doc comment, whose value runs to the end of the line:

```
#@desc: the host's welcome
#!^ warning R0203
```

(The codes in these examples are the real ones: chapters 02 and 13.)

Several Diagnostics on one line are written one after another: `#! error R1301, warning R1305`.

**Matching.** A check case passes when the Transpiler reports exactly the annotated Diagnostics: same severity, same code, primary span starting on the same line. A Diagnostic with no annotation, or an annotation with no Diagnostic, fails the case. Message wording, labels, hints and quick fixes aren't checked, so they can improve without breaking cases. In a folder case, each annotation sits in the file the Diagnostic lands in.

## Coverage

A language chapter is **proven** when:

1. every error and warning in its `Transpiler checks` section has at least one check case that reports it;
2. every rule the chapter states has at least one accepting case (`#! ok`) that uses it;
3. every case names, in `rule:`, the rule or check it exercises;
4. every rule about what a Program does at run time has at least one behaviour case.

The spec itself carries **one exemplar case per language chapter**, to show the format on that chapter's material. Full coverage is written by the development effort, test-first, as it builds each chapter's part of the Transpiler.

## Regia 1.5

Regia 1.5 is the subset of 2.0 that is built first (ADR 0025). Every chapter of the spec ends in a `## Regia 1.5` section, which says whether all of the chapter is in 1.5 or lists what is left out. A 1.5 build reports `R0109` for a construct of a later system (chapter 01), and a 1.5 run refuses a spawn with `T1902` (chapter 19). Both codes are retired in 2.0.

What 1.5 leaves out, and where each chapter says so:

| Left out | Chapters |
| --- | --- |
| `FROM GAME`, `FROM ME`, `FROM` with `OR` | 03, 05, 07, 10, 20, 25, 30; `R3805` and `R3806` in 38 |
| `BY`, and hearing how an asked Goal ended, a Reason included | 05, 07, 11, 15, 20, 38 |
| Quota Triggers and `SENT` | all of 18; 05, 15, 16, 19, 20, 25, 28, 29, 30, 33, 34, 35, 36 |
| Joining: `JOINED`, spawning, Givings and setups that reach a joiner | 15, 16, 17, 19, 21, 28, 29, 30, 33, 34, 36 |

Chapters 01, 02, 04, 06, 08, 09, 12, 13, 14, 22–24, 26, 31, 32 and 37 are all in 1.5, with notes in a few of them.

**Cases.** A case is marked with `#! regia:` (*Annotations*, above) only when it doesn't run on both. `regia test` runs the cases that fit its build's version (chapter 23). The coverage rules apply to each version on its own: a 1.5 build is proven on the cases it runs.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- How the test runner is built inside `regia test`, and how cases are vendored into the Transpiler's repository: the development effort.
- ASL snapshot tests: the development effort, outside the spec.
