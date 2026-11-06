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
An objective an Agent has decided, or been told, to pursue. It is reached when a Plan for it finishes.
_Avoid_: Desire, intention, achievement

**Event**:
Something that happens in the world and is over once noticed. It triggers Plans but leaves nothing behind, so a Context can't test it afterwards. To remember it, a Plan records a Fact.
_Avoid_: Triggering event, percept, message, happening

**Signal**:
An Event an Agent sends to the Directors of every Plot currently giving it the Playbook the Signal is written in. The Directors react to it like any other Event, and can tell which Role sent it. It is an Agent's only way to reach a Director.
_Avoid_: Notification, message

**Group**:
A named set of Vocabulary items that are declared to belong together, for example so that one can be picked at random.
_Avoid_: Multi-definition, enum, list

**Multi-definition**:
Shorthand for declaring several Vocabulary items in one line. Unlike a Group, it creates no relationship between the items.
_Avoid_: Group, batch declaration

**Parameter name**:
The name given to a slot when a Vocabulary item is declared, such as `person` in `FACT hates(person)`. It documents what the slot means and never binds anything.
_Avoid_: Parameter (when meaning an argument), formal parameter

**Value**:
A fixed name, number or string written in a slot, such as `host` in `hates(host)`.
_Avoid_: Constant, atom, bound parameter, literal

**Placeholder**:
A blank in a slot, written `?name`, that the Agent fills by matching in a Plan's Trigger or Context, or that the Body names with `?name = …`. It is filled once per Plan run and never reassigned.
_Avoid_: Variable, unbound parameter, logic variable, wildcard

**Number**:
A Value that is a number, whole or decimal, such as `80` or `-0.5`. There is only one kind of Number.
_Avoid_: Integer, float, numeric literal

**Expression**:
Something that works out to a Value: a Value, a filled Placeholder, a random roll, or these combined with arithmetic.
_Avoid_: Formula, computation, term

## Plans and statements

**Plan**:
A reaction to something that happened, or a recipe for reaching a Goal. It is made of a Trigger, an optional Context and a Body. Several Plans can share one Trigger, each with its own Context; only the first whose Context holds runs.
_Avoid_: Rule, reaction, behaviour

**Trigger**:
The part of a Plan that names what starts it: an Event, a Fact learned or forgotten, or a Goal pursued or dropped. One Trigger can head several Plans, which share everything written in it.
_Avoid_: Condition, head

**Trigger kind**:
Which sort of thing starts a Plan, such as an Event happening or a Fact being learned. Written as a word after the item (`LEARNED`, `FORGOTTEN`, `DROPPED`), or as `TO` for a Goal recipe.
_Avoid_: Event type, triggering event

**Sender**:
The Agent or Director that sent what a Trigger reacts to, such as a Signal, a Message or a Goal. A Trigger can restrict or name it with `FROM`. Things the game or the Agent itself caused have no Sender.
_Avoid_: Source

**Message**:
A Fact, an Event or a request to pursue a Goal that one Agent sends to others. A told Fact or Event becomes the receiver's own, like one from the game; a requested Goal becomes the receiver's own Goal. Messages only add, never take away.
_Avoid_: Communication, performative, speech act

**Recipient**:
Who a Message goes to: an Agent held by a Placeholder, every Agent playing a Role, or everyone. Never the sender, and never an Agent named in the source.
_Avoid_: Receiver (when meaning the written target), addressee, target

**Context**:
The condition that must hold for a Plan to be chosen, written after `GIVEN`. It is checked once, when the Plan is chosen, before any of its Body runs.
_Avoid_: Guard, precondition, IF (when meaning the context)

**Body**:
The ordered Statements a Plan carries out.
_Avoid_: Procedure, steps

**Label**:
An optional tag on a Plan's Trigger that influences how the Plan is chosen or what it changes (e.g. priority, mood).
_Avoid_: Flag, annotation, modifier

**Statement**:
A single step of a Plan's Body: an Action, a Director Statement, or control flow (`IF`/`ELSE`). An `IF` is checked when the Body reaches it, unlike the Context.
_Avoid_: Instruction, command

**Block**:
A group of Statements or declarations that belong to a header, such as a Playbook, a Trigger, a `GIVEN` or an `IF` branch. Its body is either indented under the header or written on the header's line.
_Avoid_: Scope, suite, section

**Block header**:
The line, or part of a line, that opens a Block. It always ends with `:`.
_Avoid_: Head, opener

**Inline block**:
A Block whose body is written on the same line as its header. It ends at a `;` or at the end of the line.
_Avoid_: One-liner, explicit block

**Action**:
Anything an Agent does: acting on the world, changing its own Facts and Goals, or communicating.
_Avoid_: Command, operation

**Custom Action**:
An Action defined outside Regia and declared in the Vocabulary, usually affecting the game world. It is always written after `DO`.
_Avoid_: External action, user action

**Basic Action**:
An Action built into Regia that any Agent can use, for changing its own Facts and Goals (`LEARN`, `FORGET`, `CHANGE`, `PURSUE`, `DROP`), sending (`TELL`, `ASK`, `SIGNAL`), printing or waiting. It is written without `DO`.
_Avoid_: Built-in, primitive, internal action, BELIEVE, ACHIEVE

**Director Statement**:
A Statement only a Director can use, changing the Plot's infrastructure (such as `ASSIGN`, `TRANSITION`, `START SUBPLOT`, `END PLOT`).
_Avoid_: Director action, plot command

## Comments

**Comment**:
Text for human readers that has no meaning for the language. It starts with `#`, or is enclosed in `#[ … ]#` across several lines.
_Avoid_: Note, remark

**Doc comment**:
A comment documenting the declaration directly below it, written `#@key: value`. Unlike a plain Comment, it belongs to the declaration and is read by tools.
_Avoid_: Docstring, annotation, documentation comment

**Doc key**:
The name in a Doc comment saying what the text is about, such as `desc`, `author` or `version`. A Doc comment without a key is a `desc`.
_Avoid_: Tag, field, attribute

## Instancing and tooling

**Instancing comment**:
A comment carrying information for instancing the agents after transpilation (for example, how many Agents play a Role), starting with `#%`. It sits at a different abstraction level from the rest of the language.
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
