# Regia

Regia is a language for describing game agents (NPCs) as BDI agents, written for game designers and programmers alike. This glossary uses the designer-facing names; BDI and target-language terms appear only under _Avoid_.

## Agents and narrative

**Agent**:
A single character living in the game at runtime. An Agent may play several Roles in several Plots at the same time.
_Avoid_: Instance, agent instance, NPC, actor

**Role**:
A class of Agents inside one Plot. The Role's name, and which Agents play it, are local to that Plot.
_Avoid_: Agent (1.0 name), character, class

**Plot**:
A narrative state machine describing how a scenario unfolds through its Phases and the Roles that take part in it.
_Avoid_: Story (1.0 name), quest, scenario

**Staging**:
One running copy of a Plot. The same Plot may have several Stagings at once, each with its own Agents and current Phase.
_Avoid_: Plot instance, run, session

**Root Plot**:
The Plot every Agent starts in. Baseline behaviour is a Playbook the Root Plot gives out.
_Avoid_: Default story, main plot, world plot

**Phase**:
One of the mutually exclusive states of a Plot. A Plot is in exactly one Phase at a time.
_Avoid_: State, stage

**Subplot**:
A Plot started from within another Plot, which becomes its parent. The parent's Roles are mapped onto the Subplot's Roles.
_Avoid_: Child story, nested plot

**Director**:
The behind-the-scenes agent that runs a Plot: it moves the Plot between Phases, gives Playbooks to Roles, and reacts to Signals.
_Avoid_: Narrator, manager, game master

**Playbook**:
A named set of Plans that are given to or taken away from a Role together. It describes local behaviour, independent of any Plot.
_Avoid_: Behaviour, module, plan library

## Vocabulary

**Vocabulary**:
The declared Facts, Events, Actions and Goals that Plans are built from.
_Avoid_: Declarations, components

**Fact**:
Something an Agent (or a Director) knows about the state of the world.
_Avoid_: Belief, knowledge, percept

**Goal**:
An objective an Agent has decided, or been told, to pursue.
_Avoid_: Desire, intention, achievement

**Event**:
Something that triggers a Plan. It is usually how an Agent finds out that something changed in the world.
_Avoid_: Triggering event, percept, message

**Signal**:
A message an Agent sends to the Director of the Plot that gave it a Playbook. It works like an Event, but it is not called one.
_Avoid_: Event, notification

**Group**:
A named set of Vocabulary items that are declared to belong together, for example so that one can be picked at random.
_Avoid_: Multi-definition, enum, list

**Multi-definition**:
Shorthand for declaring several Vocabulary items in one line. Unlike a Group, it creates no relationship between the items.
_Avoid_: Group, batch declaration

## Plans and statements

**Plan**:
A reaction to an Event, or a recipe for reaching a Goal. It is made of a Trigger, a Context and a Body.
_Avoid_: Rule, reaction, behaviour

**Trigger**:
The part of a Plan that names the Event or Goal starting it.
_Avoid_: Condition, head

**Context**:
The condition on Facts that must hold for a Plan to be chosen.
_Avoid_: Guard, precondition, IF (when meaning the context)

**Body**:
The ordered Statements a Plan carries out.
_Avoid_: Procedure, steps

**Label**:
An optional tag on a Plan's Trigger that influences how the Plan is chosen or what it changes (e.g. priority, mood).
_Avoid_: Flag, annotation, modifier

**Statement**:
A single step of a Plan's Body: an Action, a Director Statement, or control flow (`IF`/`ELSE`).
_Avoid_: Instruction, command

**Action**:
Anything an Agent does: acting on the world, changing its own Facts and Goals, or communicating.
_Avoid_: Command, operation

**Custom Action**:
An Action defined outside Regia and declared in the Vocabulary, usually affecting the game world. It is always written after `DO`.
_Avoid_: External action, user action

**Basic Action**:
An Action built into Regia that any Agent can use (such as `PRINT`, `BELIEVE`, `SIGNAL`). It is written without `DO`.
_Avoid_: Built-in, primitive, internal action

**Director Statement**:
A Statement only a Director can use, changing the Plot's infrastructure (such as `ASSIGN`, `TRANSITION`, `START SUBPLOT`, `END PLOT`).
_Avoid_: Director action, plot command

## Instancing and tooling

**Instancing comment**:
A comment carrying information for instancing the agents after transpilation (for example, how many Agents play a Role). It sits at a different abstraction level from the rest of the language.
_Avoid_: Compilation comment, deployment config

**Target**:
A language Regia is translated into so that it can run, for example AgentSpeak.
_Avoid_: Backend, output language

**Transpiler**:
The tool that translates Regia source into a Target.
_Avoid_: Compiler

**Visual Editor**:
The tool that shows Regia source next to a flowchart of it, with both sides editable and kept in sync.
_Avoid_: Editor (unqualified), BIRDBRAIN
