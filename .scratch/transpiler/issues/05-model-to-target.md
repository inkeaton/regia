# Review: Model to Target

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Question

What does a Target see, and how does it write ASL?

Work by hand: one Plan of `courtesy.regia` to its ASL (chapters 28, 29, 39).

Decide: the `Target` trait's shape; whether the Jason Target builds an ASL tree or writes text; where lowering shared by several files lives; how the source map (chapter 35) is gathered while emitting; how the Build of a `.regia` Entry differs (chapter 28, ADR 0049).

Chapters 23, 28, 39; ADR 0012.

## Resolution

Agreed with Edoardo on 2026-11-26. The answer is in chapter 23, *Targets* and *How the Jason Target emits*; chapter 28, *Generated names*, *Generated ASL is readable* and *A Build of a `.regia` Entry*; chapter 35, *The source map*.

- **Worked example.** `TO take_seat, FROM DIRECTOR` (`courtesy.regia:9`) by hand: one plan in `Courtesy.asl`, plus entries in `goals.asl`, `unheard.asl`, `sourcemap.json` and the Role files' `regia_game`/`regia_playbook` beliefs. Its context comes from three chapters; a `.setof` written with `A` would clash with `?a`.
- **Trait.** `check(&Model) -> Vec<Diagnostic>`, `emit(&Model) -> Vec<OutputFile>`. The Root Plot is read from the Model; `--target none` is `Option`. `dyn` waits for a second Target.
- **Text, not a tree.** An `AslPlan` struct (label, annotations, trigger, context conjuncts, body steps) printed in one place; terms written to text under a `Vars` (Placeholder → variable, counters for generated variables; copied and renamed for negated `GIVEN` siblings).
- **Shared lowering.** Step 1 of Jason emit fills one struct of Program-wide tables (Role file includes, Goals, told Cues, game items per top-level file). Step 2: one writer per file, reading the Model and the tables. Step 3: the source map. Rank `Pos` is local to a Playbook and counted by its writer (corrected during the teach-back; it was first put in the tables).
- **Plan labels** per owner: `regia_plan__courtesy__1`. Spec examples in chapters 32, 33, 35, 39 and 40 renamed; the guide's are left to *Readable generated ASL*.
- **Source map.** Writers record (ASL line, origin) as they write; origins go through the per-file line index, 1-based lines and character columns. Emit is a third edge in *Positions*. JSON maps sorted by key, with `serde_json` in `regia-core`.
- **Emit can't fail.** No `Result`; `expect` naming the check, with a `# Panics` doc. Testable two ways: the case runner (M3) emits every case with no errors, and a `#[should_panic]` unit test on a hand-built Model.
- **Determinism.** Files sorted by path, Plans in source order per owner, JSON maps sorted.
- **A `.regia` Entry with no Plot** gets no Role file; the hand-written top-level file carries the includes, `regia_playbook` and `regia_game` (chapter 36's form).
- **Readable ASL.** Edoardo asked whether the 1.0 idea (recurring patterns as named Infrastructure in shared files) still holds. The layout does; the generated bodies had drifted (guard and `FROM` tests written out, `TELL Role` as `.setof` + `for` + `regia.send`, `SIGNAL`, `-!g`). Chapter 28 now states the rule and the three forms (rule, internal action, Infrastructure plan); the pattern-by-pattern audit is *Readable generated ASL*.
- **Teach-back.** Questions 1–3 (steps, plan parts, source map) were not known and were walked through; then a (a second Plot changes only the tables) and b right; c half right (the Build also holds Infrastructure, `unheard.asl`, `goals.asl`, the source map). Emit panicking on a `None` was right from the start.
- No ADR: each choice is local to `targets/jason` and cheap to change. The readability rule is recorded in chapter 28.
