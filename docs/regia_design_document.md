# Regia — Language Design Document

> **Scope**: This document describes the *design* of the Regia language: what each construct is, why it exists, and how it maps to AgentSpeak. For implementation details detailing how these constructs map to the transpiler (parser, AST, compiler pipeline), see the [Compiler Architecture Document](compiler_architecture.md).

---

## 1. Purpose and Motivation

Regia is a **Domain-Specific Language for writing BDI agents and controlling narrative flow**. It targets interactive fiction and game environments where multiple autonomous agents coexist in a shared world, each reacting to events while also participating in larger coordinated storylines.

### The Two Problems It Solves

**1. Behaviour modularity.** In raw AgentSpeak, the full behaviour of a character must be written in a single monolithic file. Regia replaces this with *Playbooks* — small, composable behaviour bundles that can be attached to and detached from agents at runtime, depending on the narrative situation.

**2. Narrative coordination.** Raw AgentSpeak has no built-in concept of structured story progression. Regia introduces *Plots* — director-centric scenario descriptions that orchestrate multiple agents across a sequence of named phases, managing which behaviours are active at each moment and triggering world-level events.

### Target Audience

Regia is intended to be readable and writable by **game designers** who may not be expert programmers. Its keyword-heavy, declarative syntax is deliberately closer to a script or screenplay format than to a programming language.

### Target Platform

Regia compiles to **AgentSpeak**, the language used by the Jason BDI agent platform. All Regia constructs have a well-defined, deterministic AgentSpeak equivalent. The runtime is Jason; Regia only changes the *authoring experience*.

---

## 2. Core Concepts Overview

Regia is built around six core concepts, layered from most concrete to most abstract:

| Concept | Layer | Description |
|---|---|---|
| **Facts** | Vocabulary | Named beliefs an agent can hold |
| **Events** | Vocabulary | Named triggers the agent can perceive |
| **Actions** | Vocabulary | Named operations the agent can execute |
| **Playbooks** | Behaviour | Reusable bundles of reactive plans |
| **Plots** | Narrative | Structured, multi-phase narrative scenarios |
| **Director** | Runtime | An autonomous agent that manages a Plot |

The three vocabulary elements (Facts, Events, Actions) form the **shared vocabulary** that Playbooks and Plots reference. They must be declared before use.

---

## 3. Vocabulary: Base Elements

### 3.1 Actions

An **Action** is a named operation that an agent can perform. It may optionally accept parameters.

```regia
ACTION greet_back.
ACTION give_item(item, target).
ACTION vesna.transition_to(state).
ACTION .print(message).
ACTION vesna.via.set_visible(visible) AS set_visible.
```

Aliases are useful for mapping deeply namespaced internal actions to simpler names for use within the `.regia` script. When an alias is declared, both the original name and the alias can be used in the Playbook. The compiler will automatically replace the alias with the original name in the generated AgentSpeak code.

Actions are the atomic units of agent behaviour. They correspond to AgentSpeak internal actions or environment commands. Regia deliberately does not specify *how* an action is implemented — it only names the interface.

**Why a declaration?** Explicit declaration serves as a contract: both Playbooks and Plots reference the same named actions, and the compiler can verify that no undefined action is used.

**AgentSpeak mapping:**

| Regia | AgentSpeak |
|---|---|
| `ACTION greet_back.` | No output — declaration only |
| `DO greet_back.` (in a plan body) | `greet_back` |
| `DO give_item(sword, player).` | `give_item(sword, player)` |

### 3.2 Events

An **Event** is a named trigger that an agent can perceive. Events drive plan selection in the BDI cycle.

```regia
EVENT fan_greets.
EVENT internal_check SELF.
```

The optional `SELF` qualifier indicates that this event is generated internally by the agent itself (a self-perception), rather than arriving from the environment. The default origin, when omitted, is `ENVIRONMENT`.

**Why the origin qualifier?** In AgentSpeak, the source of a belief addition is tracked via annotations (e.g., `[source(percept)]` vs. `[source(self)]`). The origin qualifier makes this distinction explicit in Regia without exposing the annotation syntax.

**AgentSpeak mapping:**

| Regia | AgentSpeak plan trigger |
|---|---|
| `EVENT fan_greets.` | `+fan_greets[source(percept)]` |
| `EVENT check SELF.` | `+check[source(self)]` |

### 3.3 Facts

A **Fact** is a named proposition that the agent can believe, with optional parameters.

```regia
FACT happy.
FACT has_item(item).
```

Facts are the epistemic state of the agent. They appear in `IF` guards and `TRANSITION` conditions to make plan selection context-sensitive.

**AgentSpeak mapping:**

| Regia | AgentSpeak |
|---|---|
| `FACT happy.` | Belief `happy` |
| `FACT has_item(item).` | Belief `has_item(X)` |
| `IF happy:` (in a plan guard) | `: happy` |

---

## 4. Playbooks

A **Playbook** is a named, reusable bundle of reactive plans. It describes how an agent should behave in a particular context, without being tied to any specific narrative.

```regia
PLAYBOOK SingerInBackstage:

    WHEN fan_greets:
        IF happy:
            DO greet_back.
        IF angry:
            DO curse.
        ELSE:
            DO ignore.

    WHEN player_asks_about_quest PRIORITY 7:
        DO TELL(player, busy_message).

    WHEN attacked:
        DO flee.
        SIGNAL emergency.
```

### 4.1 Design Rationale

Playbooks serve two goals:

1. **Reuse**: The same Playbook can be assigned to multiple agents playing the same role, or even to different roles in different Plots.
2. **Context isolation**: A Playbook only knows about the agent itself. It cannot directly affect other agents or the world. This keeps behaviours composable and prevents tight coupling with specific Plot structures.

Playbooks are assigned to and removed from agents at runtime by the Director (via `ASSIGN` and `UNASSIGN` statements inside Plots). This means an agent's active behaviour set can change dynamically as the narrative progresses.

### 4.2 WHEN Blocks

Each `WHEN` block inside a Playbook defines a **reactive plan**: when the named event occurs, execute the given body.

```regia
WHEN fan_greets:
    DO greet_back.
```

The event name must refer to a declared `EVENT`. The body executes on the agent that perceives the event.

**Priority**: Each `WHEN` block may carry an optional `PRIORITY` number. When multiple plans match the same event, the plan with the highest priority number is selected. Plans without a priority default to `0`.

```regia
WHEN player_asks_about_quest PRIORITY 7:
    DO TELL(player, busy_message).
```

**AgentSpeak mapping:** Each `WHEN` block compiles into one or more AgentSpeak plans. The plan's trigger is the event, the context includes the `playbook_active(Name)` guard (to enable static gating) plus any `IF` condition, and the body contains the statements.

### 4.3 Playbook Statements

Inside a Playbook `WHEN` block, only two kinds of statements are allowed:

**`DO action.`** — Execute an action on the agent itself. This is the primary way an agent does something in the world.

```regia
DO greet_back.
DO TELL(player, message).
DO ACHIEVE(perform_song).
DO BELIEVE(has_weapon).
DO FORGET(has_weapon).
DO BROADCAST(alert_message).
```

The special action names `TELL`, `BROADCAST`, `ACHIEVE`, `BELIEVE`, `FORGET`, and `PRINT` are reserved and map to specific AgentSpeak primitives:

| Special Action | AgentSpeak |
|---|---|
| `DO TELL(target, msg).` | `.send(target, tell, msg)` |
| `DO BROADCAST(msg).` | `.broadcast(tell, msg)` |
| `DO ACHIEVE(goal).` | `!goal` |
| `DO BELIEVE(fact).` | `+fact` |
| `DO FORGET(fact).` | `-fact` |
| `DO PRINT(text).` | `.print(text)` |
| `DO WAIT(ms).` | `.wait(ms)` |

**`SIGNAL event.`** — Send a message to the Director that manages the Plot this agent is currently participating in. This is the *only* way a Playbook can communicate upward to the narrative layer.

```regia
SIGNAL emergency.
```

A `SIGNAL` maps to an infrastructural helper `!signal_directors` in AgentSpeak, which queries all active `playbook_active(Name, DirectorId)` beliefs and broadcasts the signal to every Director currently managing this agent. To prevent Jason from dropping duplicate signals if the same event occurs twice, the helper explicitly broadcasts an `untell` immediately followed by a `tell` to force the Director to process the signal as a new event. The Playbook does not need to know who the Directors are — that binding is resolved dynamically at runtime, allowing an agent to safely participate in multiple concurrent Plots.

### 4.4 Conditional Branching (IF / ELSE)

A `WHEN` block may contain conditional branches, selecting different action sequences based on the agent's current beliefs.

```regia
WHEN fan_greets:
    IF happy:
        DO greet_back.
    IF angry:
        DO curse.
    ELSE:
        DO ignore.
```

**Mixed form**: Unconditional statements placed *before* any `IF` are prepended to every branch. This is syntactic sugar for repeating the prefix in each branch:

```regia
WHEN event:
    DO log_event.       # prepended to every branch
    IF happy:
        DO greet.
    ELSE:
        DO ignore.
```

**Branch semantics**: `IF` branches are exclusive — at most one fires per event occurrence. The `ELSE` branch fires when no `IF` condition holds. In AgentSpeak, each branch compiles into a separate plan with the corresponding context guard. The mutual exclusion is guaranteed by the guards themselves.

### 4.5 Conditions

Boolean expressions over Facts, used in `IF` guards and `TRANSITION` guards.

```regia
IF happy.
IF NOT angry.
IF happy AND has_item(sword).
IF happy OR neutral.
IF (happy OR neutral) AND NOT busy.
```

Operator precedence: `NOT` > `AND` > `OR`. Parentheses override.

### 4.6 Emotional and Personality Modeling (TEMPER / EFFECTS)

Regia supports an extension for the VEsNA (Virtual Emotion and Narrative Architecture) system. Playbook and Director `WHEN` blocks can optionally specify a `TEMPER` clause to model personality prerequisites and an `EFFECTS` clause to model emotional outcomes.

```regia
WHEN fan_greets TEMPER sympathy(0.8), aggressiveness(-0.5) EFFECTS fear(-0.05):
    DO greet_back.
```

- **`TEMPER`**: Defines the personality dimensions and their float values required for this plan to be applicable or preferred by the agent.
- **`EFFECTS`**: Defines the emotional impact on the agent if this plan is executed.

**AgentSpeak mapping:** These clauses compile into plan annotations.
```asl
@pb__SingerInBackstage__fan_greets__0[temper([sympathy(0.8), aggressiveness(-0.5)]), effects([fear(-0.05)])]
+fan_greets : playbook_active(SingerInBackstage) <-
    greet_back.
```

---

## 5. Plots

A **Plot** is a structured narrative scenario. It describes the overall arc of a scripted situation — the phases it passes through, the roles that agents play in it, and how the Director should manage transitions and world events.

```regia
PLOT Concert.

    PHASE backstage INITIAL.
    PHASE performing.
    PHASE aftermath.

    ROLE Singer.
    ROLE AudienceMember.

    DURING PLOT:
        WHEN emergency PRIORITY 9:
            WORLD DO trigger_alarm.

    DURING backstage:
        WHEN time_to_start:
            TRANSITION TO performing.

        ON ENTER:
            ASSIGN SingerInBackstage TO Singer.
            WORLD DO add_waiting_for_concert.

        ON EXIT:
            UNASSIGN SingerInBackstage FROM Singer.
            WORLD DO announce_concert.
```

### 5.1 Design Rationale

Plots exist to solve the **narrative coordination problem**: how do you make a group of agents behave in a structured way over time, without hardcoding every possible interaction into every agent?

The key design choice is the **Director pattern**: every active Plot instance spawns its own Director agent. The Director acts as a hidden orchestrator — it perceives events, manages phase state, sends directives to role-bound agents, and triggers world actions. Individual agents don't know they're in a Plot; they simply receive and execute directives.

This separation means:
- Agents (and their Playbooks) stay generic and reusable.
- Narrative logic stays centralised in the Director.
- Multiple Plots can run concurrently, each with its own Director.

### 5.2 Phases

A **Phase** is a named, mutually exclusive stage of the Plot. At any given moment, exactly one phase is active.

```regia
PHASE backstage INITIAL.
PHASE performing.
PHASE aftermath.
```

The `INITIAL` modifier marks the starting phase. Every Plot must have exactly one `INITIAL` phase.

**AgentSpeak mapping:** The Director holds a belief `current_phase(name)` that tracks the active phase. Transitions update this belief.

### 5.3 Roles

A **Role** is a named placeholder for one or more agents that will participate in the Plot. Roles are the indirection layer between the narrative script (which uses abstract names) and the actual agents (which are concrete runtime entities).

```regia
ROLE Singer.
ROLE AudienceMember.
```

At runtime, when a Plot is started, each role is bound to one or more actual agent instances. The Plot script refers only to role names; the Director resolves them to actual agent identifiers.

**Why Roles instead of agent names?** This makes Plots reusable. The same `Concert` Plot can be run with different agents filling the `Singer` role each time, without modifying the Plot script.

### 5.4 DURING Blocks

A `DURING` block scopes behaviour to a specific phase (or to the entire Plot).

```regia
DURING backstage:
    ...

DURING PLOT:
    ...
```

- `DURING phaseName:` — behaviour inside is only active when that phase is current.
- `DURING PLOT:` — behaviour inside is active across *all* phases. Used for Plot-wide concerns like emergency handlers.

Inside a `DURING` block, three kinds of content can appear: `ON ENTER` hooks, `ON EXIT` hooks, and `WHEN` blocks.

### 5.5 Phase Transitions

A **Transition** declares when and how the Plot moves from one phase to another. It is expressed using the `TRANSITION TO phase.` statement inside a `WHEN` block.

```regia
WHEN time_to_start:
    WORLD DO dim_lights.
    TRANSITION TO performing.
```

The inline form allows imperative actions to precede the transition. It must always be the **last statement** in its block or branch, and is forbidden in `DURING PLOT` blocks (since there is no single current phase to leave).

**Transition execution order:**
1. Transition event fires (or inline `TRANSITION TO` is reached).
2. Director evaluates any enclosing `IF` condition in the `WHEN` block.
3. `ON EXIT` of the current phase executes.
4. The `current_phase` belief is updated.
5. `ON ENTER` of the new phase executes.

### 5.6 Lifecycle Hooks: ON ENTER / ON EXIT

`ON ENTER` and `ON EXIT` are imperative sequences executed at phase boundaries. They are the primary mechanism for setting up and tearing down the state needed for each phase.

```regia
ON ENTER:
    ASSIGN SingerInBackstage TO Singer.
    WORLD DO add_waiting_for_concert.

ON EXIT:
    UNASSIGN SingerInBackstage FROM Singer.
    WORLD DO announce_concert.
```

These hooks only appear inside `DURING phaseName` blocks, never in `DURING PLOT`.

### 5.7 Director WHEN Blocks

Inside a `DURING` block, `WHEN` blocks define the Director's reactive plans — how the Director responds to events while a given phase is active.

```regia
WHEN emergency PRIORITY 9:
    WORLD DO trigger_alarm.
    Singer DO acknowledge.
    AudienceMember DO acknowledge.
```

Like Playbook `WHEN` blocks, these support `PRIORITY`, `IF`/`ELSE` branching, and the mixed prefix form.

Additionally, the Director can react specifically to signals emitted by agents playing a particular role, rather than generic world events. This is done using the `WHEN ROLE <RoleName> SIGNALS <EventName>:` syntax.

```regia
WHEN ROLE Hero SIGNALS warning PRIORITY 5:
    WORLD DO PRINT("Warning received from hero!").
    Sidekick DO assist.
```
This syntax filters the triggering event so that the plan only activates if the event was generated by an agent currently assigned to the specified role.

### 5.8 Director Statements

Inside Plot `WHEN` blocks, `ON ENTER`, and `ON EXIT`, the Director uses a different set of statements from those available in Playbooks:

| Statement | Purpose | AgentSpeak mapping |
|---|---|---|
| `WORLD DO action.` | Director executes an action itself (ownerless) | Internal action / environment call |
| `RoleName DO action.` | Director sends a one-off goal to a role's agents | `.send(agent, achieve, action)` |
| `ASSIGN Playbook TO Role.` | Inject a Playbook into a role's agents | `.send(agent, achieve, add_playbook(pb))` |
| `UNASSIGN Playbook FROM Role.` | Remove a Playbook from a role's agents | `.send(agent, achieve, remove_playbook(pb))` |
| `TRANSITION TO phase.` | Inline phase transition (WHEN blocks only) | Phase belief update sequence |
| `START SUBPLOT Plot MAPPING ... .` | Spawn a child Plot | Director creates a child Director |
| `END PLOT.` | Terminate the current Plot | Director notifies parent/children and stops |

### 5.9 Plot Hierarchy: Subplots

A Plot can spawn **child Plots** (subplots) using `START SUBPLOT`. This allows complex narrative structures where a high-level Plot delegates parts of its story to smaller, self-contained sub-scenarios.

```regia
ON ENTER:
    START SUBPLOT ArenaTrial MAPPING Hero TO Fighter.
    START SUBPLOT ArenaTrial MAPPING Champion TO Fighter.
```

The `MAPPING` clause binds roles from the parent Plot to roles in the child Plot. Multiple instances of the same Plot type can be spawned concurrently (each gets its own Director).

**Parent-child communication**: Plots communicate through two mechanisms:
- **Child to Parent**: When a child plot terminates, the parent can react using the `WHEN SUBPLOT <PlotName> ENDS:` keyword.
- **Parent to Child**: When a parent plot terminates, it notifies all children via the `parent_ended` reserved event.

*Note: In the compiled AgentSpeak codebase, these infrastructural lifecycle signals (`plot_ended`, `parent_ended`, `child_ended`) are broadcast as transient achievement goals (e.g. `!parent_ended`) rather than belief additions. This prevents permanently cluttering the agent's belief base with dead plot IDs.*

These mechanisms allow coordinated cleanup and conditional advancement:

```regia
DURING PLOT:
    WHEN parent_ended:
        WORLD DO close_gate.
        END PLOT.

    WHEN SUBPLOT ArenaTrial ENDS:
        WORLD DO announce_winner.
```

**`END PLOT`**: Terminates the current Plot instance. This notifies all children (via `parent_ended`) and the parent (via `child_ended` internally), then destroys the Director agent. Must be the last statement in its block or branch. Forbidden inside `ON ENTER` / `ON EXIT` hooks.

---

## 6. File-Level Constructs

### 6.1 Imports

A Regia source file can import base element declarations from another file:

```regia
IMPORT "base_vocabulary.regia".
IMPORT "npc_actions.regia".
```

Imports must appear at the very top of the file, before any other declarations. They allow the vocabulary (Actions, Events, Facts) to be factored out into shared files and reused across multiple Playbooks and Plots.

### 6.2 Doc Comments

Doc comments attach structured metadata to top-level declarations:

```regia
#@author: Game Design Team
#@desc: Core combat playbook for aggressive enemies.
PLAYBOOK AggressiveEnemy:
    ...
```

A doc comment starts with `#@` followed by a key and value. Comments placed before any declaration are treated as file-level documentation. This system is designed for tooling (editors, documentation generators) rather than the compiler itself.

---

## 7. Priority and Plan Selection

When multiple plans match the same event on the same agent, Regia resolves the conflict using a priority order:

```
Plot one-off directive  >  Playbook plan (by priority number)  >  Default (priority 0)
```

Higher `PRIORITY` number = higher precedence. Plans without a declared priority default to `0`.

This means the Director can always override an agent's Playbook behaviour by sending a `Role DO` directive, regardless of the Playbook's priority. This preserves the Director's authority over the narrative.

---

## 8. Conceptual Model Summary

The following diagram captures the runtime relationships between Regia concepts:

```
┌─────────────────────────────────────────────────────┐
│                    PLOT (narrative)                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐ │
│  │  Phase   │──▶│  Phase   │──▶│  Phase (INITIAL) │ │
│  └──────────┘   └──────────┘   └──────────────────┘ │
│        │                                             │
│        │ DURING                                      │
│        ▼                                             │
│  ┌───────────────────────────────┐                   │
│  │   DIRECTOR agent              │                   │
│  │   - manages current_phase     │                   │
│  │   - fires transitions         │                   │
│  │   - executes WORLD DO         │                   │
│  │   - sends ASSIGN/UNASSIGN     │                   │
│  │   - sends Role DO directives  │                   │
│  └───────────────────────────────┘                   │
│         │                │                           │
│    ASSIGN Playbook    Role DO action                  │
│         │                │                           │
│         ▼                ▼                           │
│  ┌─────────────────────────────────────────────┐     │
│  │  ROLE-bound AGENT                           │     │
│  │  - holds playbook_active(pb, Director)      │     │
│  │  - runs Playbook WHEN plans                 │     │
│  │  - uses !signal_directors to broadcast      │     │
│  └─────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

---

## 9. Full Worked Example

The following example illustrates all major language constructs working together.

```regia
# =============================================================
# Base Elements
# =============================================================

ACTION greet_back.
ACTION curse.
ACTION ignore.
ACTION flee.
ACTION acknowledge.
ACTION bow.
ACTION perform_song.
ACTION trigger_alarm.
ACTION add_waiting_for_concert.
ACTION announce_concert.
ACTION start_music.

EVENT fan_greets.
EVENT player_asks_about_quest.
EVENT time_to_start.
EVENT emergency.
EVENT song_ends.
EVENT audience_cheers.

FACT happy.
FACT angry.
FACT audience_satisfied.

# =============================================================
# Playbooks
# =============================================================

PLAYBOOK SingerInBackstage:

    WHEN fan_greets:
        IF happy:
            DO greet_back.
        IF angry:
            DO curse.
        ELSE:
            DO ignore.

    WHEN player_asks_about_quest PRIORITY 7:
        DO TELL(player, busy_message).

    WHEN emergency:
        DO flee.
        SIGNAL emergency.

PLAYBOOK SingerOnStage:

    WHEN audience_cheers:
        DO bow.
        DO ACHIEVE(perform_song).

# =============================================================
# Plot
# =============================================================

PLOT Concert.

    PHASE backstage INITIAL.
    PHASE performing.
    PHASE aftermath.

    ROLE Singer.
    ROLE AudienceMember.

    DURING PLOT:
        WHEN emergency PRIORITY 9:
            WORLD DO trigger_alarm.
            Singer DO acknowledge.
            AudienceMember DO acknowledge.

    DURING backstage:

        WHEN time_to_start:
            TRANSITION TO performing.

        ON ENTER:
            ASSIGN SingerInBackstage TO Singer.
            WORLD DO add_waiting_for_concert.

        ON EXIT:
            UNASSIGN SingerInBackstage FROM Singer.
            WORLD DO announce_concert.

    DURING performing:

        WHEN song_ends:
            IF audience_satisfied:
                TRANSITION TO aftermath.

        ON ENTER:
            ASSIGN SingerOnStage TO Singer.
            WORLD DO start_music.

        ON EXIT:
            UNASSIGN SingerOnStage FROM Singer.
```

**Narrative reading of this example:**

The `Concert` Plot begins in the `backstage` phase. On entering, the Director assigns the `SingerInBackstage` Playbook to whoever is playing the `Singer` role, meaning that agent will now react to fan greetings, quest questions, and emergencies.

When the `time_to_start` event fires, the transition moves the Plot to `performing`. The Director first runs the `backstage` exit hook (removing the backstage playbook, announcing the concert), then runs the `performing` entry hook (assigning the `SingerOnStage` Playbook, starting the music).

If an `emergency` event fires at any point, the `DURING PLOT` handler fires: the Director triggers the alarm and sends `acknowledge` directives to both role types, overriding whatever those agents were doing.

---

## 10. AgentSpeak Mapping Reference

| Regia construct | AgentSpeak equivalent |
|---|---|
| `FACT happy.` | Belief atom `happy` |
| `FACT has_item(item).` | Belief functor `has_item(X)` |
| `EVENT fan_greets.` | Plan trigger `+fan_greets[source(percept)]` |
| `EVENT check SELF.` | Plan trigger `+check[source(self)]` |
| `PLAYBOOK Pb: WHEN e: DO a.` | `+e : playbook_active(Pb) <- a.` |
| `IF happy:` | Context clause `: happy` |
| `IF NOT angry:` | Context clause `: not angry` |
| `IF a AND b:` | Context clause `: a, b` |
| `IF a OR b:` | Two plans, one with `: a`, one with `: b` |
| `PRIORITY 7` | Plan annotation `priority(7)` (and file ordering) |
| `TEMPER d(v) EFFECTS e(v)` | Plan annotations `temper([d(v)])` and `effects([e(v)])` |
| `DO TELL(target, msg).` | `.send(target, tell, msg)` |
| `DO BROADCAST(msg).` | `.broadcast(tell, msg)` |
| `DO ACHIEVE(goal).` | `!goal` |
| `DO BELIEVE(fact).` | `+fact` |
| `DO FORGET(fact).` | `-fact` |
| `SIGNAL emergency.` | `!signal_directors(playbook_name, emergency)` |
| `ASSIGN Pb TO Role.` | Director: `.send(agent, achieve, add_playbook(Pb))` |
| `UNASSIGN Pb FROM Role.` | Director: `.send(agent, achieve, remove_playbook(Pb))` |
| `WORLD DO action.` | Director: `action` (internal/env action) |
| `Singer DO acknowledge.` | Director: `.send(singer_agent, achieve, acknowledge)` |
| `TRANSITION TO p.` (inline) | Director body: ON EXIT + belief update + ON ENTER |
| `START SUBPLOT Plot MAPPING ...` | Director creates a child Director agent |
| `END PLOT.` | Director notifies children/parent, then stops |
| `WHEN child_ended:` | Plan triggered when child Director terminates |
| `WHEN parent_ended:` | Plan triggered when parent Director terminates |

---

## 11. Design Decisions and Trade-offs

### 11.1 Static Gating vs. Dynamic Injection for Playbooks

When a Director executes `ASSIGN Playbook TO Role`, one of two strategies could realise this in AgentSpeak:

- **Static gating with Transitive Closure**: All Playbook plans are pre-compiled into every Role's `.asl` template, guarded by a `playbook_active(Name, DirectorId)` belief. `ASSIGN`/`UNASSIGN` simply toggles this belief. To support subplots, the compiler runs a Depth-First Search over all role mappings and statically includes the **transitive closure** of every Playbook the agent might ever need. This is the approach currently implemented.
- **Dynamic injection**: The Director uses Jason's `.add_plan`/`.remove_plan` API to inject and remove plans at runtime.

Static gating is simpler, more predictable, and easier to debug, at the cost of including unused plans in every agent's file (though this is mitigated by the fact that Jason ignores plans whose context beliefs are false).

### 11.2 Fault Tolerance and Agent Death

If an agent unexpectedly terminates, the environment can broadcast a `+agent_died(Agent)` belief to the system. Directors possess infrastructural handlers to catch this event and immediately prune the dead agent from their internal `role_agent` registry. This cleanly decouples failure states and ensures that Directors do not stall indefinitely attempting to communicate with dead agents.

### 11.2 Roles as Indirection

The choice to use Roles (rather than agent names) in Plots is deliberate. It decouples the narrative script from the concrete agent population. The same Plot script can be instantiated multiple times with different agent sets, and the Plot description itself never needs to change.

### 11.3 Director-Centric Narrative Authority

The Director has unconditional priority over Playbook behaviours. This is a deliberate design choice: the narrative layer must be able to override autonomous agent behaviour at any time. A `Role DO` directive preempts any Playbook plan, ensuring that scripted story moments cannot be subverted by agent autonomy.

### 11.4 No Loops or Arithmetic

Regia is intentionally not a general-purpose language. It has no loops, no arithmetic, no variables, and no user-defined functions. This keeps the language readable for non-programmers and ensures that the AgentSpeak mapping remains straightforward. Anything requiring computation should be encapsulated as an `ACTION` implemented in the underlying platform.
