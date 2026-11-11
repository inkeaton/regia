# Conformance

How a spec chapter shows that it is complete and correct, in a form a Transpiler can be tested against. Decided in the ticket *How a spec chapter proves itself* (`.scratch/regia-2/issues/33-spec-conformance.md`). It covers the language chapters only: 01–21 and 26. The architecture chapters (22–25) describe how the tools are built, not what the language means, and have no Conformance cases.

## What a case checks

A **Conformance case** is a small Program with the outcome the spec promises for it. There are two kinds:

- A **check case** gives the exact Diagnostics the Transpiler reports for it: which errors, warnings and notes, by Diagnostic code and line. It may also say there are none (an accepting case).
- A **behaviour case** adds a scripted run (Events from the game, Agents joining and leaving) and gives the Trace that run is expected to leave.

Emitted ASL is **not** part of the spec. The spec promises what a Program means, not one way of writing it in a Target, so a golden `.asl` file would freeze one particular lowering. The development effort may keep ASL snapshot tests of its own; they aren't Conformance cases.

The `.trace` format, the script of a run and how a Trace is matched are in chapter 34. Behaviour cases run against a scripted stand-in for the game (chapter 35, ADR 0014).

## Diagnostic codes

Every error, warning and note a language chapter defines has a stable **Diagnostic code**: `R`, the chapter's two digits, then two digits numbering the check within the chapter. Chapter 13's first error is `R1301`. The `code` field of a Diagnostic (chapter 23) carries it, and each code has a docs page.

Numbers run in order through a chapter's section, errors first, then warnings, then notes; a check added later takes the next free number, whatever its severity. Codes are never reused. A check that is dropped keeps its number, marked retired in its chapter.

Every language chapter lists its checks in a `## Transpiler checks` section, grouped as **Errors**, **Warnings** and **Notes**, each with its code:

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
    root-plot-inferred/
      banquet.regia
      duel.regia
      game.regin
```

- A case is one `.regia` file, or a **folder** when it needs several files (Imports, Instancing). The name is a slug saying what it exercises.
- In a folder case, the Entry is the `.regin` file at its root if there is one; otherwise every `.regia` file in the folder is an Entry.
- A behaviour case adds a sibling `.trace` file (a single-file case) or a `.trace` file inside its folder. Its format is in chapter 34.

The spec owns the cases. The development effort copies or vendors them into the Transpiler's test suite and doesn't edit them there; a disagreement with a case is a change to the spec.

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

1. every error, warning and note in its `Transpiler checks` section has at least one check case that reports it;
2. every rule the chapter states has at least one accepting case (`#! ok`) that uses it;
3. every case names, in `rule:`, the rule or check it exercises;
4. every rule about what a Program does at run time has at least one behaviour case.

The spec itself carries **one exemplar case per language chapter**, to show the format on that chapter's material. Full coverage is written by the development effort, test-first, as it builds each chapter's part of the Transpiler.

## Not decided here

- How the test runner is built, and how cases are vendored into the Transpiler's repository: the development effort.
- ASL snapshot tests: the development effort, outside the spec.
