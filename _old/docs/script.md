# RegiaScript Transpiler — Structure Summary

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3 | Entire compiler implementation |
| Parser generator | ANTLR4 (4.13.2) + Python3 runtime | Lexer/parser generation from grammar |
| Testing | pytest | 76-test suite across 6 categories |
| Packaging | Nuitka | Single-binary executable, no dependencies |

No external runtime dependencies beyond the ANTLR4 Python runtime (`antlr4-python3-runtime`), which Nuitka bundles into the final binary.

---

## Directory Structure

```
regia/
├── grammars/
│   └── RegiaScript.g4              ← Grammar source of truth
│
├── src/
│   ├── generated/                  ← Auto-generated, never hand-edited
│   │   ├── RegiaScriptLexer.py
│   │   ├── RegiaScriptParser.py
│   │   ├── RegiaScriptVisitor.py
│   │   └── RegiaScriptListener.py  (generated, unused)
│   │
│   ├── errors.py                   ← Error/warning collection and display
│   ├── antlr_error_listener.py     ← ANTLR syntax error → human-readable
│   ├── symbol_table.py             ← Pass 1: declaration validation
│   ├── emitter.py                  ← Pass 2: AgentSpeak generation
│   └── compiler.py                 ← Pipeline orchestrator
│
├── main.py                         ← CLI entry point
├── build.sh                        ← Nuitka build script
│
├── tests/
│   ├── test_regiascript.py         ← pytest test suite
│   ├── generate_test_files.py      ← Generates all .rgs fixtures
│   ├── rgs/                        ← Generated fixture files
│   │   ├── valid/
│   │   ├── syntax_errors/
│   │   ├── declaration_errors/
│   │   ├── semantic_errors/
│   │   ├── warnings/
│   │   └── integration/
│   ├── expected/integration/       ← Expected .asl snapshots
│   ├── complex_test.rgs            ← Large multi-story manual test
│   └── bring_me_item.rgs           ← Snippet-style manual test
│
└── regiascript-vscode/
    ├── package.json
    ├── language-configuration.json
    └── syntaxes/regiascript.tmLanguage.json
```

---

## The Compilation Pipeline

```
.rgs source text
    │
    ├─[Lexer]──────────────► token stream
    ├─[Parser]─────────────► parse tree (ProgramContext)
    │   └─ errors → antlr_error_listener.py → errors.py → stop
    │
    ├─[Pass 1: SymbolTableBuilder]─► SymbolTable
    │   └─ errors → errors.py → stop
    │
    ├─[Pass 2: AgentSpeakEmitter]──► dict[agent_name → AgentBuffer]
    │   └─ errors/warnings → errors.py → stop on errors
    │
    └─[main.py]─────────────► one .asl file per agent + Director.asl
```

Each stage only runs if the previous produced zero errors. Information flows strictly forward.

---

## What Each File Does

### Grammar

**`grammars/RegiaScript.g4`** — The single source of truth for syntax. Defines the full hierarchy: `program` → `storyDef` (`defaultStory` | `namedStory`) → `declaration*`/`phaseDecl*`/`duringBlock+` → `duringBlock` (`transitionRule*` + `agentBlock+`) → `agentBlock` → `agentSection*` (declarations + `whenBlock`s) → `whenBlock`/`transitionRule` (event, origin, optional `IF condExpr`) → `condExpr`/`condAnd`/`condTerm`/`condAtom` (OR-of-AND-of-NOT-atoms with parens) → `doSequence`/`doAction`. Lexer section defines all keywords (`STORY`, `DEFAULT`, `PHASE`, `AGENT`, `DURING`, `ALWAYS`, `WHEN`, `IF`, `TRANSITION`, `TO`, `END`, `DO`, `BELIEVE`, `FORGET`, all five origins, `AND`/`OR`/`NOT`), punctuation, `ID`/`NUMBER`, and comment handling (`DOC_COMMENT` for `# @KEY:` lines, `COMMENT` skipped, `WS` skipped). **This is the first file to change for any language modification** — regenerate `src/generated/` afterward via:

```bash
rm -rf src/generated/*.py src/generated/*.interp src/generated/*.tokens
antlr4 -Dlanguage=Python3 -visitor -o src/generated grammars/RegiaScript.g4
```

---

### Generated Code

**`src/generated/RegiaScriptLexer.py`** — Character stream → token stream. Generated; never hand-edited.

**`src/generated/RegiaScriptParser.py`** — Token stream → parse tree. Each grammar rule becomes a `*Context` class with accessor methods (`.ID()`, `.origin()`, `.condExpr()`, etc.) and an `accept()` method dispatching to `visitor.visitRuleName(self)`.

**`src/generated/RegiaScriptVisitor.py`** — Base visitor class with one `visitRuleName` per grammar rule, each defaulting to `visitChildren`. `SymbolTableBuilder` and `AgentSpeakEmitter` subclass this and override only the rules they care about.

---

### Cross-Cutting: Error Handling

**`src/errors.py`** — `Severity` enum (WARNING/ERROR), `CompilerMessage` dataclass (line, column, length, message, hint, source_line for caret display), and `ErrorReporter` class. `ErrorReporter` is constructed once per compilation with the full source text (split into lines for caret display), and passed to every stage. Provides `.error()`/`.warning()`, `.has_errors()`, `.error_count()`/`.warning_count()`, and `.print_all()` (sorts by line, prints with carets, prints summary). Knows nothing about the grammar or AgentSpeak — pure message collection/formatting.

**`src/antlr_error_listener.py`** — `RegiaScriptErrorListener`, registered on both lexer and parser (replacing ANTLR's default listeners). Translates raw ANTLR `syntaxError()` callbacks into human-readable messages via `_friendly_token` (a mapping from token types to plain-English descriptions, including all origins and keywords), then forwards to `ErrorReporter.error()`. The only bridge between ANTLR's error mechanism and the project's error system.

---

### Pass 1 — Symbol Table

**`src/symbol_table.py`** — Defines the data model for everything *declared* in a `.rgs` file and the visitor that populates it.

Data classes: `ActionInfo`, `EventInfo`, `ConditionInfo` (name, origin where applicable, line, doc), `PhaseInfo` (name, line, `initial: bool`, doc), `TransitionInfo` (from_phase, to_phase Optional, is_terminal, event_name, event_origin, `cond_ctx` — raw parse tree node for pass 2 to walk, line), `AgentInfo` (name, line, local actions/events/conditions dicts, doc), `StoryInfo` (name, priority Optional for DEFAULT, is_default, story-level actions/events/conditions/phases dicts, `agents: dict[str, AgentInfo]`, `agent_names: list[str]` ordered for Director generation, `transitions: list[TransitionInfo]`, doc). `SymbolTable` wraps `stories: dict[str, StoryInfo]`.

`SymbolTableBuilder(RegiaScriptVisitor)` — visits `storyDef` → `defaultStory`/`namedStory` → story-level declarations → `phaseDecl*` (first = initial) → `duringBlock+` → validates phase references and collects `transitionRule*` via `_visit_transition_rule` → `agentBlock+` (agents accumulate across multiple `DURING` appearances — no duplicate error) → `agentSection*` (local declarations only; `whenBlock` ignored in pass 1). Validates: duplicate names within a scope, priority ≥ 1, duplicate phases, undeclared phase references in `DURING`/`TRANSITION TO`, undeclared events in `TRANSITION`. `parse_doc_comments()` is a shared helper extracting `@NAME`/`@MEANING` from `DOC_COMMENT` tokens.

---

### Pass 2 — Emission

**`src/emitter.py`** — Defines the AgentSpeak output model and the visitor that produces it.

`_GENERIC_PLANS` — a hardcoded string constant with the three universal infrastructure plans (`+!enter_phase(Story, Phase)`, `+!activate_story(Name, Priority)`, `+!deactivate_story(Name)`), emitted identically in every agent file including the Director.

`CompiledPlan` (priority, agentspeak string) and `AgentBuffer` (name, plans list, initial_beliefs list, `get_output()` assembling Initial beliefs / Infrastructure plans / Plans sections, plans sorted by `-priority`).

`AgentSpeakEmitter(RegiaScriptVisitor)`:
- `visitProgram` → per `storyDef` → `visitDefaultStory`/`visitNamedStory` → per `duringBlock` → `_emit_during_block_new` → per `agentBlock` → `_emit_agent_in_during`
- `_emit_agent_in_during` — gets/creates the agent's `AgentBuffer`, emits initial `current_phase(story, phase)` belief once (first declared phase), then for each `agentSection.whenBlock` calls `_emit_when`
- `_emit_when` — validates event against effective symbol table (agent-local merged with story-level), validates origin matches declaration, builds trigger (`_emit_trigger`: ENVIRONMENT→`[source(percept)]`, DIRECTOR→`[source(director)]`, PLAYER→`[source(player)]`, TIMER→`[source(timer)]`, MYSELF→none), builds context (`story(name,priority)` conjunct for named stories + `current_phase(story,phase)` conjunct for non-ALWAYS + IF clause), builds body via `_emit_doSequence`
- `_emit_condExpr`/`_emit_condAnd`/`_emit_condTerm`/`_emit_condAtom` — recursive condition emission mirroring the grammar's OR-of-AND-of-NOT structure, validates conditions against effective symbol table
- `_emit_doSequence`/`_emit_doAction` — `DO action`→action name, `DO BELIEVE`→`+cond`, `DO FORGET`→`-cond`; validates each reference
- After all stories: `_emit_director()` — for each named story with transitions, creates/extends the `"Director"` buffer: emits initial `current_phase` belief, and per `TransitionInfo` calls `_emit_transition_plan` (builds context from story+phase+optional condition via the same `_emit_condExpr` machinery; body = `!enter_phase(...)` or `!deactivate_story(...)` followed by semicolon-separated `.send(agentname_lowercase, achieve, ...)` to every `story.agent_names`)
- `check_unused()` — after full traversal, warns on any declared action/event/condition never referenced (tracked via `_used_actions`/`_used_events`/`_used_conditions` sets)

**This is the file most likely to need updates whenever AgentSpeak output mapping changes**, alongside the grammar/symbol table for new syntax.

---

### Orchestration and CLI

**`src/compiler.py`** — `CompileResult` dataclass (`success`, `outputs: dict[str, str]`, `error_count`, `warning_count`, `messages`). `compile_file(filepath)`: reads source → constructs `ErrorReporter` → lexes/parses with `RegiaScriptErrorListener` attached → if errors, `_failure()` → Pass 1 `SymbolTableBuilder` → if errors, `_failure()` → Pass 2 `AgentSpeakEmitter` + `check_unused()` → if errors, `_failure()` → returns success with `emitter.get_outputs()`. Contains no grammar/emission logic itself — pure orchestration.

**`main.py`** — CLI entry point. Calls `compile_file()`, prints all messages sorted by line with carets (mirroring `ErrorReporter._print_message` format), prints success/failure summary. On success, for each `agent_name → agentspeak_string` in `outputs`, builds a header (source filename, agent name, timestamp) and either writes to `output_dir/AgentName.asl` or prints to stdout with a banner (special-cased `"Director"` gets its own banner like any other agent). The only place that calls `sys.exit()`.

**`build.sh`** — Nuitka build script: `NUITKA_PATCHELF_PATH=.venv/bin/patchelf python -m nuitka --onefile --output-filename=regiascript --include-package=antlr4 --include-package=src --include-data-dir=src/generated=src/generated --follow-imports main.py`.

---

### Tests

**`tests/generate_test_files.py`** — Generates all `.rgs` fixtures and expected `.asl` snapshots into `tests/rgs/` and `tests/expected/integration/`, organized into 6 categories (A–F below). Run once to (re)populate fixtures after grammar changes.

**`tests/test_regiascript.py`** — pytest suite, 76 tests across:
- **Category A — Valid syntax** (`tests/rgs/valid/`) — every legal construct compiles with 0 errors
- **Category B — Syntax errors** (`tests/rgs/syntax_errors/`) — malformed constructs produce parser errors
- **Category C — Declaration errors** (`tests/rgs/declaration_errors/`) — duplicates, invalid priorities, duplicate phases/agents
- **Category D — Semantic errors** (`tests/rgs/semantic_errors/`) — undeclared refs, wrong origins, undeclared phases in `DURING`/`TRANSITION`
- **Category E — Warnings** (`tests/rgs/warnings/`) — unused actions/events/conditions
- **Category F — Output correctness** (`tests/rgs/integration/`) — exact AgentSpeak snapshot comparison via `_extract_plans()` (strips initial beliefs/infrastructure plans, compares only the Plans section)

**`tests/complex_test.rgs`** / **`tests/bring_me_item.rgs`** — Hand-written manual test files inspired by the designer snippets (Crackhead Assault, Bring Me Item, O.R.A. Gathering), exercising multi-story, multi-phase, multi-agent, all origins, all condition operators, and `TRANSITION TO`/`TO END`.

---

### VS Code Extension

**`regiascript-vscode/`** — Syntax highlighting only (no LSP). `syntaxes/regiascript.tmLanguage.json` defines TextMate scopes: `declaration_keywords` (STORY/DEFAULT/AGENT/PHASE/ACTION/EVENT/CONDITION/PRIORITY), `control_keywords` (DURING/ALWAYS/WHEN/IF/DO/BELIEVE/FORGET/TRANSITION/TO/END — needs updating if `TRANSITION`/`TO`/`END` weren't yet added here), `operator_keywords` (AND/OR/NOT), `origin_tags` (all five origins), doc/plain comments, numbers, punctuation, identifiers. `language-configuration.json` handles bracket matching, comment toggling, auto-indent on `:`.

---

## What to Touch When the Grammar Changes

In dependency order:

1. **`grammars/RegiaScript.g4`** — add/modify rules and keywords
2. **Regenerate `src/generated/`** — delete and rerun `antlr4 -Dlanguage=Python3 -visitor`
3. **`src/symbol_table.py`** — new data classes/fields, new validation in `SymbolTableBuilder`
4. **`src/emitter.py`** — new emission logic in `AgentSpeakEmitter`, possibly new `_GENERIC_PLANS` entries
5. **`src/antlr_error_listener.py`** — add new keywords to `_friendly_token` mapping if they can appear in syntax error hints
6. **`tests/generate_test_files.py`** — add fixtures for new constructs (valid/error/integration cases)
7. **`tests/test_regiascript.py`** — add corresponding test methods
8. **`regiascript-vscode/syntaxes/regiascript.tmLanguage.json`** — highlight new keywords

This is the mirror-image checklist of the editor's — `types/story.ts` ↔ `symbol_table.py`'s data classes, `toRegiaScript.ts`/`fromRegiaScript.ts` ↔ grammar + emitter, and both sides' test fixtures should stay representative of the same language version.