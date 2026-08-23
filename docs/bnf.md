# Regia Language — BNF Reference

> **Scope**: This document is a formal BNF-style description of the Regia grammar.
> For the design rationale and high-level semantics of each construct, see the [Language Design Document](regia_design_document.md).

The grammar uses the following conventions:
- `'KEYWORD'` — literal keyword terminal (case-sensitive).
- `ID` — an identifier terminal (see §8).
- `NUMBER`, `FLOAT`, `STRING` — lexical terminals (see §8).
- `( ... )?` — optional element.
- `( ... )+` — one or more repetitions.
- `( ... )*` — zero or more repetitions.
- `|` — alternatives.
- `ε` — the empty production (nothing).

---

## 1. File Structure

A Regia file is a flat sequence of **import declarations** followed by **element declarations**, **Playbook definitions**, and **Plot definitions**, in any order. However, the compiler enforces that all `IMPORT` statements come before any other top-level item.
```
<program>        ::= (<import-stmt> | <item>)+

<import-stmt>    ::= 'IMPORT' STRING '.'

<item>           ::= <element-decl>
                   | <playbook-def>
                   | <plot-def>

<element-decl>   ::= <action-decl>
                   | <event-decl>
                   | <fact-decl>
```

**`IMPORT`** pulls in a second Regia source file by path. The resolved ASTs are merged before validation and emission, so all symbols declared in the imported file become available in the importing file.

---

## 2. Base Element Declarations

These declare the **shared vocabulary** — actions, events, and facts — that both Playbooks and Plots can reference. They must be declared before first use.
```
<action-decl>     ::= 'ACTION' ID <param-names>? ('AS' ID)? '.'
<event-decl>      ::= 'EVENT' ID '.'
<fact-decl>       ::= 'FACT'   ID <param-names>? '.'
```

- **`ACTION`** declares an action that agents can execute. The optional `(param, ...)` list names the parameter slots. The optional `AS alias` clause provides an alternate AgentSpeak name used during emission (useful when the Regia name would clash with a reserved word or when bridging to an external agent API).
  ```
  ACTION greet.
  ACTION give_item(item, target).
  ACTION .print AS print_action.
  ```

- **`EVENT`** declares a signal that agents can emit or receive.
  ```
  EVENT fan_greets.
  EVENT heartbeat.
  EVENT earthquake.
  ```

- **`FACT`** declares a belief predicate with an optional arity. Zero-arity facts are simple boolean flags; parametric facts carry typed slots.
  ```
  FACT happy.
  FACT has_item(item).
  FACT relationship(agent, value).
  ```
```
<param-names>   ::= '(' ID (',' ID)* ')'
```

---

## 3. Playbooks

A Playbook is a **reusable, composable bundle of reactive plans**. It is context-free: it has no knowledge of Plots or phases, and can only trigger self-directed actions or emit signals back to a Director.

```
<playbook-def>   ::= 'PLAYBOOK' ID ':' <pb-when-block>+
```

Each Playbook contains one or more `WHEN` blocks:

```
<pb-when-block>  ::= 'WHEN' ID <priority>? <temper>? ':' <pb-when-body>
```

### 3.1 Priority and Temper

These optional annotations affect plan selection when multiple plans match the same event.

```
<priority>      ::= 'PRIORITY' NUMBER

<temper>        ::= 'TEMPER' <temper-entry> (',' <temper-entry>)* <effects>?
<temper-entry>  ::= ID '(' FLOAT ')'
<effects>       ::= 'EFFECTS' <temper-entry> (',' <temper-entry>)*
```

- `PRIORITY N` — higher numbers are preferred. Defaults to `0`.
- `TEMPER` — declares prerequisite emotional/personality thresholds (VEsNA integration). A plan only fires if all listed dimension values fall within the agent's current temper range.
- `EFFECTS` — describes how executing this plan shifts the agent's temper dimensions.

### 3.2 Playbook WHEN Body

The body supports three patterns:

1. **Pure unconditional**: a flat list of statements.
2. **Pure conditional**: one or more `IF` branches, optionally ending in `ELSE`.
3. **Mixed (prefix + conditional)**: unconditional statements prepended to every branch's body at emission time.

```
<pb-when-body>      ::= <pb-body-item>+ <pb-else-branch>?

<pb-body-item>      ::= <pb-stmt>
                      | <pb-if-branch>

<pb-stmt>           ::= <do-stmt>
                      | <signal-stmt>

<pb-if-branch>      ::= 'IF' <condition> ':' <pb-stmt>+
<pb-else-branch>    ::= 'ELSE' ':' <pb-stmt>+
```

### 3.3 Playbook Statements

```
<do-stmt>       ::= 'DO' <action-name> <arg-list>? '.'
<signal-stmt>   ::= 'SIGNAL' ID <arg-list>? '.'
```

- **`DO`** — the agent executes the named action on itself.
- **`SIGNAL`** — broadcasts a belief-change event to all Directors managing Plots this agent is enrolled in. This is the mechanism by which role agents communicate reactive intent back to the plot orchestrator.

```
<action-name>   ::= ID
                  | 'TELL'
                  | 'BROADCAST'
                  | 'ACHIEVE'
                  | 'BELIEVE'
                  | 'FORGET'
                  | 'PRINT'
                  | 'WAIT'

<arg-list>  ::= '(' <arg> (',' <arg>)* ')'
<arg>       ::= ID | NUMBER | STRING
```

The named keywords (`TELL`, `BROADCAST`, etc.) are reserved AgentSpeak primitives that bypass the standard action dispatch, allowing direct manipulation of the agent's belief base and communication channels.

---

## 4. Plots

A Plot is a **director-centric narrative scenario**. It coordinates multiple role-playing agents through a sequence of named phases. Every active Plot instance spawns its own Director agent at runtime.

```
<plot-def>   ::= 'PLOT' ID '.' <plot-header> <during-block>+
```

### 4.1 Plot Header

The header declares the **phases** and **roles** that make up the scenario.
It must appear immediately after the `PLOT` name declaration and before any `DURING` blocks.

```
<plot-header>  ::= (<phase-decl> | <role-decl>)+

<phase-decl>   ::= 'PHASE' ID 'INITIAL' '.'
                 | 'PHASE' ID '.'

<role-decl>    ::= 'ROLE' ID '.'
```

- **`PHASE`** — declares a named phase. Exactly one phase must carry the `INITIAL` modifier; it is the phase the plot begins in at runtime.
- **`ROLE`** — declares a role template. Actual agents are bound to roles at Plot instantiation time via the `MAPPING` clause of `START SUBPLOT`, or externally by the runtime environment.

### 4.2 DURING Blocks

A `DURING` block groups all behaviour that is active while a specific phase is running. It can also be declared `DURING PLOT` to apply in *all* phases.

```
<during-block>   ::= 'DURING' ID ':' <during-content>+
                   | 'DURING' 'PLOT' ':' <during-content>+

<during-content> ::= <on-enter>
                   | <on-exit>
                   | <plot-when-block>
                   | <plot-when-subplot-ends-block>
                   | <plot-when-role-signals-block>
```

- **Phase-specific** (`DURING phaseName:`) — content is only active while the plot is in the named phase. A matching phase guard is automatically injected into each compiled plan.
- **Plot-wide** (`DURING PLOT:`) — content is always active regardless of the current phase; no phase guard is injected. May not contain `ON ENTER` or `ON EXIT` hooks (those only make sense for a specific phase).

### 4.3 Lifecycle Hooks

```
<on-enter>   ::= 'ON' 'ENTER' ':' <imperative-stmt>+
<on-exit>    ::= 'ON' 'EXIT' ':' <imperative-stmt>+
```

- **`ON ENTER`** — executed once when the phase is entered. May not contain
  `TRANSITION TO` or `END PLOT`.
- **`ON EXIT`** — executed once just before the phase is left. Same
  restrictions as `ON ENTER`.

Both hooks may only appear inside phase-specific `DURING` blocks.

---

## 5. Director WHEN Blocks

`WHEN` blocks inside `DURING` sections define the Director's **reactive plans** — how the Director responds to events while a given phase is active. There are three variants, each with a different triggering condition.

### 5.1 Event WHEN Block

Reacts to any occurrence of the named event, regardless of which agent emitted it.

```
<plot-when-block>   ::= 'WHEN' ID <priority>? ':' <plot-when-body>
```

Example:
```
WHEN emergency PRIORITY 9:
    WORLD DO trigger_alarm.
    Singer DO acknowledge.
```

### 5.2 Subplot Ends WHEN Block

Reacts when a running child Plot (subplot) terminates normally.

```
<plot-when-subplot-ends-block>   ::= 'WHEN' 'SUBPLOT' ID 'ENDS' <priority>? ':' <plot-when-body>
```

Example:
```
WHEN SUBPLOT ArenaTrial ENDS:
    TRANSITION TO next_phase.
```

### 5.3 Role Signals WHEN Block

Reacts to a named event **only if** it was emitted by an agent currently assigned to the specified role. This allows the Director to distinguish, for example, a `done` signal coming from a `Hero` versus the same `done` signal coming from a `Villain`.

```
<plot-when-role-signals-block>   ::= 'WHEN' 'ROLE' ID 'SIGNALS' ID <priority>? ':' <plot-when-body>
```

The first `ID` is the **role name**; the second is the **event name**.
At runtime, the Director checks the triggering event's `source` annotation against the `role_agent/2` belief (populated by the role-registration infrastructure) to filter correctly.

Example:
```
WHEN ROLE Hero SIGNALS warning PRIORITY 5:
    WORLD DO PRINT("Warning received from the hero!").
    Sidekick DO assist.
```

### 5.4 Plot WHEN Body

All three WHEN block forms share the same body grammar:

```
<plot-when-body>    ::= <plot-body-item>+ <plot-else-branch>?

<plot-body-item>    ::= <imperative-stmt>
                      | <plot-if-branch>

<plot-if-branch>    ::= 'IF' <condition> ':' <imperative-stmt>+
<plot-else-branch>  ::= 'ELSE' ':' <imperative-stmt>+
```

Like Playbook bodies, the mixed (prefix + conditional) pattern is allowed: unconditional statements before the first `IF` are prepended to every branch's body during compilation.

---

## 6. Imperative Statements

Director-level commands available inside `ON ENTER`, `ON EXIT`, and all Plot `WHEN` body forms.

```
<imperative-stmt>   ::= <assign-stmt>
                      | <unassign-stmt>
                      | <world-do-stmt>
                      | <role-do-stmt>
                      | <inline-transition-stmt>
                      | <start-subplot-stmt>
                      | <plot-end-stmt>

<assign-stmt>            ::= 'ASSIGN' ID 'TO' ID '.'
<unassign-stmt>          ::= 'UNASSIGN' ID 'FROM' ID '.'
<world-do-stmt>          ::= 'WORLD' 'DO' <action-name> <arg-list>? '.'
<role-do-stmt>           ::= ID 'DO' <action-name> <arg-list>? '.'
<inline-transition-stmt> ::= 'TRANSITION' 'TO' ID '.'
<start-subplot-stmt>     ::= 'START' 'SUBPLOT' ID ('MAPPING' <role-mapping> (',' <role-mapping>)*)? '.'
<role-mapping>           ::= ID 'TO' ID
<plot-end-stmt>          ::= 'END' 'PLOT' '.'
```

| Statement                              | Purpose                                                      |
| -------------------------------------- | ------------------------------------------------------------ |
| `ASSIGN PbName TO RoleName .`          | Inject a Playbook into all agents playing the role           |
| `UNASSIGN PbName FROM RoleName .`      | Remove a Playbook from all agents playing the role           |
| `WORLD DO action (args)? .`            | Director executes an action itself (ownerless)               |
| `RoleName DO action (args)? .`         | Director sends an achievement goal to all agents in the role |
| `TRANSITION TO phaseName .`            | Trigger an inline phase transition                           |
| `START SUBPLOT PlotName MAPPING ... .` | Spawn a child Plot instance with bound roles                 |
| `END PLOT .`                           | Terminate the current Plot                                   |

**Validator-enforced placement rules:**
- `TRANSITION TO` and `END PLOT` are **forbidden** inside `ON ENTER` and `ON EXIT`.
- `TRANSITION TO` must be the **last** statement in any body or branch.
- `END PLOT` must be the **last** statement in any body or branch.
- `TRANSITION TO` may only appear inside **phase-specific** `DURING` blocks (not `DURING PLOT`).

---

## 7. Conditions

Boolean expressions over declared facts. Used as guards in `IF` branches.

```
<condition>      ::= <condition-and> ('OR' <condition-and>)*

<condition-and>  ::= <condition-atom> ('AND' <condition-atom>)*

<condition-atom> ::= 'NOT' <condition-atom>
                   | <fact-ref>
                   | '(' <condition> ')'

<fact-ref>       ::= ID ('(' <arg> (',' <arg>)* ')')?
```

**Operator precedence** (tightest binding first): `NOT` > `AND` > `OR`.
Parentheses override any precedence level.

Examples:
```
IF happy AND has_item(sword):
    ...

IF NOT injured OR (is_hiding AND in_safe_zone):
    ...
```

---

## 8. Lexical Terminals

```
ID      ::= (\.)?[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*
NUMBER  ::= [0-9]+
FLOAT   ::= -?[0-9]+(\.[0-9]+)?
STRING  ::= "[^"]*"
```

- **`ID`** — supports an optional leading dot (`.print`) for Jason internal actions, and dot-qualified names (`vesna.transition_to`) for namespaced AgentSpeak calls. Higher-priority named terminals (see below) take precedence over `ID` where they overlap.
- **`NUMBER`** — non-negative integer; used for `PRIORITY` values and integer action arguments.
- **`FLOAT`** — signed decimal number; used for `TEMPER` and `EFFECTS` dimension values (e.g. `0.8`, `-0.5`, `1.0`).
- **`STRING`** — double-quoted string literal; used in `PRINT` and as string-typed action arguments. Cannot contain embedded double-quote characters.

**Reserved words** — these have higher parse priority than `ID` and cannot be used as user-defined identifiers:

| Category              | Keywords                                                             |
| --------------------- | -------------------------------------------------------------------- |
| AgentSpeak primitives | `TELL`, `BROADCAST`, `ACHIEVE`, `BELIEVE`, `FORGET`, `PRINT`, `WAIT` |

**Comments** — begin with `#` and extend to end of line. Ignored entirely by the parser.

**Doc Comments** — begin with `#@key: value`. These are extracted by the preprocessor and attached to the following top-level declaration (e.g. `PLAYBOOK`, `PLOT`, `ACTION`). When attached to a `PLAYBOOK` or `PLOT`, the compiler emits them as `// key: value` comments in the resulting `.asl` files. Doc comments on vocabulary (`ACTION`, `EVENT`, `FACT`) are stored in the AST for tooling but omitted from emission. A doc comment can span multiple lines using `# -` continuations.

**Whitespace** — spaces, tabs, and newlines are all insignificant and ignored.

---

## 9. Quick Reference Summary

```
<program>  ::= (<import-stmt> | <element-decl> | <playbook-def> | <plot-def>)+

<import-stmt>    ::= 'IMPORT' STRING '.'
<action-decl>    ::= 'ACTION' ID <param-names>? ('AS' ID)? '.'
<event-decl>     ::= 'EVENT'  ID '.'
<fact-decl>      ::= 'FACT'   ID <param-names>? '.'

<playbook-def>   ::= 'PLAYBOOK' ID ':' <pb-when-block>+
<pb-when-block>  ::= 'WHEN' ID ('PRIORITY' NUMBER)? ('TEMPER' ...)? ':' <pb-when-body>
<pb-when-body>   ::= (<do-stmt> | <signal-stmt> | <pb-if-branch>)+ <pb-else-branch>?
<pb-if-branch>   ::= 'IF' <condition> ':' (<do-stmt> | <signal-stmt>)+
<pb-else-branch> ::= 'ELSE' ':'       (<do-stmt> | <signal-stmt>)+
<do-stmt>        ::= 'DO' <action-name> <arg-list>? '.'
<signal-stmt>    ::= 'SIGNAL' ID <arg-list>? '.'

<plot-def>       ::= 'PLOT' ID '.' (<phase-decl> | <role-decl>)+ <during-block>+
<phase-decl>     ::= 'PHASE' ID 'INITIAL'? '.'
<role-decl>      ::= 'ROLE' ID '.'
<during-block>   ::= 'DURING' (ID | 'PLOT') ':' <during-content>+
<during-content> ::= <on-enter> | <on-exit>
                   | <plot-when-block>
                   | <plot-when-subplot-ends-block>
                   | <plot-when-role-signals-block>

<on-enter>                       ::= 'ON' 'ENTER' ':' <imperative-stmt>+
<on-exit>                        ::= 'ON' 'EXIT'  ':' <imperative-stmt>+
<plot-when-block>                ::= 'WHEN' ID ('PRIORITY' NUMBER)? ':' <plot-when-body>
<plot-when-subplot-ends-block>   ::= 'WHEN' 'SUBPLOT' ID 'ENDS' ('PRIORITY' NUMBER)? ':' <plot-when-body>
<plot-when-role-signals-block>   ::= 'WHEN' 'ROLE' ID 'SIGNALS' ID ('PRIORITY' NUMBER)? ':' <plot-when-body>
<plot-when-body>                 ::= (<imperative-stmt> | <plot-if-branch>)+ <plot-else-branch>?
<plot-if-branch>                 ::= 'IF' <condition> ':' <imperative-stmt>+
<plot-else-branch>               ::= 'ELSE' ':' <imperative-stmt>+

<imperative-stmt>  ::= 'ASSIGN' ID 'TO' ID '.'
                     | 'UNASSIGN' ID 'FROM' ID '.'
                     | 'WORLD' 'DO' <action-name> <arg-list>? '.'
                     | ID 'DO' <action-name> <arg-list>? '.'
                     | 'TRANSITION' 'TO' ID '.'
                     | 'START' 'SUBPLOT' ID ('MAPPING' ID 'TO' ID (',' ID 'TO' ID)*)? '.'
                     | 'END' 'PLOT' '.'

<condition>        ::= <condition-and> ('OR' <condition-and>)*
<condition-and>    ::= <condition-atom> ('AND' <condition-atom>)*
<condition-atom>   ::= 'NOT' <condition-atom> | ID ('(' <arg> (',' <arg>)* ')')? | '(' <condition> ')'
```

---
