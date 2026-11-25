# Documentation style guide

This guide describes how the project's prose documentation is written: the
README and the documents under `docs/` that explain the transpiler to a
maintainer (section 2 lists them, and what is out of scope). Comments and doc comments inside source files follow `comments.md`
and `comments-rust.md` instead.

The guide builds on the Diátaxis framework (https://diataxis.fr), available
to Claude as the `diataxis` skill. Diátaxis says what each kind of document
is for; this guide says where each lives, who reads it, and how it is
written here. Where the two disagree, this guide wins.

## Principles

1. **Write for the maintainer.** The reader is someone about to change the
   code (section 1). Every document helps them understand the system or
   change it safely.
2. **One document, one job.** Every document is a tutorial, a how-to
   guide, reference, or explanation, and stays that kind throughout. When a
   passage drifts into another kind, it moves to a document of that kind
   and is replaced by a link.
3. **Architecture first.** The most important documents explain how the
   transpiler is built and why. They are written before, and kept more
   carefully than, anything else.
4. **Docs describe the project as it is now.** History lives in version
   control, `CHANGELOG.md` and ADRs. A document says "the parser does X",
   not "the parser now does X" or "since v0.3".
5. **Say it once.** Each fact has one home. Other documents link to it
   rather than restating it, so a change is made in one place.
6. **The code is the reference for the code.** Item-level API details
   belong in doc comments, which rustdoc renders. Prose docs cover what
   rustdoc cannot: the architecture, how the stages fit together, the
   source and target languages, and the reasons behind the design.
7. **Name things precisely, in three vocabularies** (section 5): project
   terms from `GLOSSARY.md`, Rust terms as the Rust Book and Reference use
   them, and source-language terms as its specification uses them.

## Layout limits

- Plain Markdown, as rendered by GitHub. No site generator; every page is
  read on its own, so navigation is by links (section 7).
- Prose lines wrap at column **80**, matching the comment guides. Tables,
  links and code may run longer when wrapping would break them.
- American English, as in `comments-rust.md`.
- Sentence-case headings ("Adding a target backend", not "Adding A Target
  Backend"). One `#` title per file; sections start at `##`.
- Plain text: no emoji, badges inside prose, or decorative Unicode.

## 1. Readers

There is one reader: **a maintainer about to change the code**. That is the
author six months from now, or anyone else working on the codebase.

What they know:

- general programming and compiler concepts (lexing, parsing, ASTs, code
  generation);
- some Rust, but not necessarily every feature this codebase uses;
- some of the source language, but not its fine points.

What they don't know, and the docs must give them:

- how the transpiler is structured, and why;
- where to make a given change, and what else it touches;
- which Rust features the code relies on, and where to read up on them;
- which source-language rules the code implements, and where they are
  specified.

Users who only run the transpiler are served by the README alone.

## 2. The document set

Every prose document lives in one place, by kind:

| Kind | Where | Holds |
|---|---|---|
| Overview | `README.md` | What the transpiler is, how to build and run it, one short usage example, a map of `docs/` |
| Tutorial | `docs/tutorials/` | Guided first steps in the codebase, e.g. "Making your first change": adding a small language feature end to end |
| How-to | `docs/how-to/` | Steps for one maintenance task, e.g. adding an AST node, adding a target backend, updating the expected output of an example |
| Reference | `docs/reference/` | What the code adds to the spec, e.g. the source-to-target mapping tables by module. The language, the command line and Diagnostic codes are in `docs/spec/`: link to it |
| Explanation | `docs/explanation/` | The architecture: pipeline stages, data flow between them, module layout, key design choices and trade-offs |
| Decisions | `docs/adr/` | One ADR per decision, in the format of the `domain-modeling` skill |
| Terms | `GLOSSARY.md` | Project domain terms, maintained by the `domain-modeling` skill |
| Examples | `docs/examples/` | Runnable source programs with their expected output (section 6) |

- **`docs/explanation/architecture.md` is the entry point** for a new
  maintainer, and the first document written. It gives the pipeline as a
  whole (a diagram in a `text` block, then one section per stage) and links
  to a deeper explanation page per stage once one exists.
- ADRs are explanation documents with a fixed format. Explanation pages
  link to them instead of repeating their reasoning.
- The API reference is rustdoc output (`cargo doc --document-private-items`).
  Don't copy item docs into `docs/reference/`; link to the source file.
- `docs/README.md` lists every document, grouped by kind in the order of
  the table above, with one line each. It is updated whenever a document
  is added, renamed or removed.
- Create a folder only when its first document is written.
- **Out of scope**: `docs/spec/`, `docs/guide/`, `docs/showcase/` and
  `docs/primer/` describe the language and keep their own form.
  `docs/standards/` and `docs/.dev/` are tooling and study material. This
  guide doesn't apply to any of them.

## 3. Every document

### File names

Lowercase words joined by hyphens, naming the topic, not the kind:
`docs/how-to/add-target-backend.md`, not `docs/how-to/how-to-backend.md`.

### Title

The title tells the reader what they get, in the form of its kind:

| Kind | Title form | Example |
|---|---|---|
| Tutorial | What the reader will have done | "Making your first change" |
| How-to | The task, starting "How to" | "How to add a target backend" |
| Reference | The thing described, as a noun | "Command-line options" |
| Explanation | The subject, often "About ..." | "About the pipeline stages" |

### Opening paragraph

Directly under the title, one short paragraph saying:

1. what the document covers, in one sentence;
2. what the reader needs first (a prior document, a built binary, a Rust
   Book chapter);
3. for tutorials and how-tos, what the reader has at the end.

No "Introduction" heading above it; the opening paragraph is the
introduction.

### Code map

Explanation and how-to pages name the modules and files they concern, as
links, near the top or in the section that discusses each. A reader should
always know where in `transpiler/` the described behavior lives.

### Ending

Tutorials and how-tos end with a short "Next steps" list of links. Reference
and explanation pages end when the content does: no closing summary.

## 4. Writing each kind

Read the matching page of the `diataxis` skill before writing or reviewing a
document of that kind. On top of it:

- **Tutorials** use numbered steps, each ending in something the reader can
  see (output, a file, a passing test). Every command and its output is
  shown in full. No choices or alternatives: one path that works.
- **How-to guides** assume the reader has read the architecture page.
  Numbered steps; preconditions at the top; every file to edit named as a
  link; the tests to run at the end. Link to explanation instead of
  explaining.
- **Reference** mirrors the structure of what it describes: one section per
  CLI flag, language construct, or diagnostic, always in the same order of
  fields. Tables over prose where entries share fields. Neutral and
  complete; no advice. Mapping tables have one row per source construct:
  source form, target form, notes, and the module that implements it.
- **Explanation** is prose. It describes the architecture and the reasons
  for it: why a stage exists, what it guarantees to the next one, what was
  considered instead. It may give history that explains the present
  design. It links to ADRs for individual decisions.

## 5. Terminology

A maintainer moves between three vocabularies. Each has one source of
truth, and docs use its words exactly.

| Vocabulary | Source of truth | Examples |
|---|---|---|
| Project terms | `GLOSSARY.md` | the project's names for stages, passes and intermediate forms |
| Rust terms | The Rust Book and the Rust Reference | trait object, lifetime, borrow, `enum` variant, crate, module |
| Regia terms | `GLOSSARY.md`, then `docs/spec/` | Plot, Playbook, Giving, Staging |

- **First mention in each document is linked** to its source of truth:
  `GLOSSARY.md` for project terms, the Rust Book (or the Reference, when
  the Book doesn't cover it) for Rust terms, the specification for
  source-language terms. Later mentions in the same document are plain.
- **Rust features are named when the code relies on them.** When a design
  depends on a Rust feature a maintainer might not know (trait objects for
  backends, lifetimes tying tokens to the source text, `Box` for the
  recursive AST), the explanation says so by name and links to where it is
  taught. It does not teach the feature itself.
- **Source-language and target-language terms are kept apart.** When both
  languages have a construct of the same name with different meaning, say
  which one is meant ("a source-language *module*", "a Rust module"), and
  record the clash in `GLOSSARY.md` under _Avoid_ or as a note.
- A term with no entry yet is added to `GLOSSARY.md` (project terms) before
  the document uses it.

## 6. Language, code and examples

### Language

- Second person and imperative mood for instructions ("Run `cargo test`"),
  third person for describing the system ("The parser reports...").
- Present tense. Active voice, unless the actor doesn't matter.
- Short sentences. One idea per paragraph.
- No filler: "simply", "just", "easy", "obviously", "note that". If
  something deserves attention, say why.
- Items, files, commands and source-language keywords in backticks.

### Code blocks

- Every code block has a language tag: `rust`, `toml`, `console` for a
  shell session, `text` for output, diagrams and formats, plus the source
  and target languages' own tags.
- Shell sessions start each command with `$ ` and show output without a
  prompt, in the same `console` block.
- Output is copied from a real run, not typed from memory. Shorten long
  output with a `...` line, never by editing values.
- Literal blocks keep the column-80 limit where the content allows, wrapped
  as in `comments.md` (continuation indented four spaces).

### Runnable examples

Examples of transpiler input and output live as files, and are checked by a
test, so the docs can't drift from the code.

- Each example is a folder `docs/examples/<name>/` holding the source
  program (`input.regin` and the files it imports) and the expected
  transpiler output (`expected/`, the output files).
- An integration test (`transpiler/crates/regia-cli/tests/doc_examples.rs`) transpiles every
  `input.regin` under `docs/examples/` and fails if the result differs from
  `expected/`. `cargo test` therefore checks the docs.
- `docs/examples/basic/` is the example the README shows. It stays small
  enough to read in full.
- A document that shows an example embeds a copy of the files' contents
  and names the folder it came from, so the reader can run it:

  ````markdown
  From `docs/examples/basic/`:

  ```regia
  ...contents of input.regin or an imported file...
  ```
  ````

- When transpiler output changes on purpose, update `expected/` and every
  document that embeds it in the same commit; a how-to guide describes the
  steps.

## 7. Links

- Relative links between documents (`../reference/cli.md`), so they work
  on GitHub and in a local checkout.
- Link a document of another kind instead of borrowing its content: a
  how-to links to the explanation for "why", an explanation links to the
  reference for exact values.
- Code is linked by source path (`transpiler/crates/regia-core/src/...`), relative to the
  document.
- Link text says where it goes ("see the CLI reference"), never "here".
- Every document is reachable from `docs/README.md`, and that index from
  `README.md`.

## 8. Keeping docs current

- A change that alters behavior or structure updates the docs that
  describe it in the same commit. Moving or renaming a module updates the
  architecture page and every code map that names it.
- When code and docs disagree, the docs are wrong until shown otherwise:
  fix them, or record the open question.
- A document no longer true and not worth fixing is deleted, not marked
  "outdated".

## Checklist

- [ ] The document is one kind and lives in that kind's folder, and is
      listed in `docs/README.md`.
- [ ] Title has the form of its kind; opening paragraph states topic,
      prerequisites and outcome.
- [ ] Explanation and how-to pages name the files and modules involved.
- [ ] Nothing restates rustdoc, an ADR or another page; it links instead.
- [ ] Project, Rust and source-language terms are used exactly; first
      mentions are linked to their source of truth.
- [ ] Examples come from `docs/examples/` and pass `cargo test`.
- [ ] Present tense, no history, no filler words.
- [ ] No prose line passes column 80.
