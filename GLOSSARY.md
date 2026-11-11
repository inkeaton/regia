# Regia

Regia is a language for describing game agents (NPCs) as BDI agents, written for game designers and programmers alike. This glossary uses the designer-facing names; BDI and target-language terms appear only under _Avoid_.

## Agents and narrative

**Agent**:
A single character living in the game at runtime. An Agent may play several Roles in several Plots at the same time.
_Avoid_: Instance, agent instance, NPC, actor

**Role**:
A class of Agents named by a Plot or a Playbook. A Plot's Role is played by the Agents cast in it; a Playbook's Role is filled by the Plot that gives the Playbook, through a Mapping. A Role's name is local to the Plot or Playbook that declares it. In a Playbook a Role is only an address for Messages: a Playbook never directs another Agent.
_Avoid_: Agent (1.0 name), character, class, part, slot

**Role setup**:
What every Agent of a Plot's Role starts with, written in a `STARTS WITH` Block on the Role: Playbooks, Facts and Goals, given by the Director each time an Agent starts playing the Role in a Staging.
_Avoid_: Role instantiation, initial state, starting kit, init block

**Plot**:
A narrative state machine describing how a scenario unfolds through its Phases and the Roles that take part in it.
_Avoid_: Story (1.0 name), quest, scenario

**Staging**:
One running copy of a Plot. The same Plot may have several Stagings at once, each with its own Agents and current Phase. Stagings have no names in the language; each knows only its parent and the Subplots it started.
_Avoid_: Plot instance, run, session

**Cast**:
The Agents playing a Plot's Roles in one Staging. It is set when the Staging starts and changes only when Agents join or leave the Program.
_Avoid_: Role instances (Target-level term), participants, members

**Joining**:
An Agent entering the Program while it runs. It joins the Root Plot's Cast in the Roles of its Agent kind, never a Subplot already running.
_Avoid_: Spawning, arriving, entering (a Plot)

**Leaving**:
An Agent leaving the Program while it runs. It stops playing every Role in every Staging at once. An Agent that is dead but still in the world has not left.
_Avoid_: Despawning, dying, exiting (a Plot)

**Root Plot**:
The one Plot every Agent starts in; every other Plot is a Subplot below it. Baseline behaviour is a Playbook the Root Plot gives out.
_Avoid_: Default story, main plot, world plot

**Phase**:
One of the mutually exclusive states of a Plot. A Plot is in exactly one Phase at a time.
_Avoid_: State, stage

**Subplot**:
A Plot started from within another Plot, which becomes its parent. The parent's Roles are mapped onto the Subplot's Roles, and its cast is fixed when it starts. It runs until it ends itself, the parent ends it, or the parent ends.
_Avoid_: Child story, nested plot

**Outcome**:
The Event a Subplot ends with, handed to its parent so the parent can react to how it went.
_Avoid_: Result, return value, ending (when meaning the Event)

**Mapping**:
How a Plot fills a Role of a Playbook it gives, or of a Subplot it starts, with one of its own Roles, with a number or share of that Role's Agents picked at random, or with one Agent held by a Placeholder. Roles with the same name are mapped without writing it.
_Avoid_: Binding, casting, role assignment

**Giving**:
One handing of a Playbook to Agents by a Plot, with its own Mappings. An Agent may hold several givings of the same Playbook; they add up, and taking one away leaves the others. A giving to a whole Role is standing: it also reaches Agents who join the Role later, until it is taken away. A giving to one Agent held by a Placeholder is not.
_Avoid_: Assignment (when meaning the result), grant

**Director**:
The behind-the-scenes agent that runs a Plot: it moves the Plot between Phases, gives Playbooks to Roles, tells and asks its Agents through Messages, and reacts to the game and to Signals. It has its own Facts but no Goals and no Propensities, and it never reads its Agents' Facts.
_Avoid_: Narrator, manager, game master

**Playbook**:
A named set of Plans that are given to or taken away from a Role together. It describes local behaviour, independent of any Plot.
_Avoid_: Behaviour, module, plan library

## Vocabulary

**Vocabulary**:
The declared Facts, Events, Actions, Goals and Propensities that Plans are built from.
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

**Propensity**:
A named disposition of an Agent, either a Trait or a Mood. Labels use Propensities to choose between Plans and to say how running a Plan changes the Agent. Propensities are not Facts: a Context can't test them.
_Avoid_: Temper, personality, emotion, attribute

**Trait**:
A Propensity that never changes during a run, such as bravery.
_Avoid_: Personality, stat

**Mood**:
A Propensity that changes as the Agent runs Plans, such as sympathy.
_Avoid_: Emotion, dynamic temper, feeling
_Avoid_: Notification, message

**External name**:
The name the game uses for a Fact, Event or Action, given when it differs from the name used in Regia: `ACTION engine.security.summon_guards AS call_guards`. Only the Target sees it; the source always uses the name after `AS`.
_Avoid_: Alias (when meaning the external name), qualified name, namespace

**Local Vocabulary**:
Facts and Goals declared inside a Playbook or Plot. They are private to it: other Playbooks on the same Agent, and other files, can't see them, and they can't be sent.
_Avoid_: Private facts, scoped declarations, inner vocabulary

**Multi-definition**:
Shorthand for declaring several Vocabulary items in one line. It creates no relationship between the items.
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

**Duration**:
An amount of time, written as an Expression followed by `SECONDS` or `MINUTES`. The language says how long; the Target decides which clock measures it, such as wall-clock time or game time that pauses with the game.
_Avoid_: Delay, timeout, ticks

**Expression**:
Something that works out to a Value: a Value, a filled Placeholder, a random roll, a count of Matches, or these combined with arithmetic.
_Avoid_: Formula, computation, term

## Plans and statements

**Plan**:
A reaction to something that happened, or a recipe for reaching a Goal. It is made of a Trigger, an optional Context and a Body. Several Plans can share one Trigger, each with its own Context; only the first whose Context holds runs.
_Avoid_: Rule, reaction, behaviour

**Trigger**:
The part of a Plan that names what starts it: an Event, a Fact learned or forgotten, or a Goal pursued, dropped or failed. One Trigger can head several Plans, which share everything written in it.
_Avoid_: Condition, head

**Trigger kind**:
Which sort of thing starts a Plan, such as an Event happening or a Fact being learned. Written as a word after the item (`LEARNED`, `FORGOTTEN`, `DROPPED`, `FAILED`), or as `TO` for a Goal recipe.
_Avoid_: Event type, triggering event

**Quota Trigger**:
A Trigger that fires once enough different Agents of a Role have sent the same Event, written `FROM ALL Guest`, `FROM 3 OF Guest` or `FROM 50 PERCENT OF Guest`. Each Agent counts once, and the count starts again after it fires.
_Avoid_: Quantifier, aggregate condition, barrier, threshold trigger

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

**Match**:
One way a condition holds: a Value for each of its blanks. When a condition has several Matches, one is used and the language doesn't say which, unless a Pick chooses.
_Avoid_: Unifier, binding, solution, result

**Pick**:
A clause on a condition's header that chooses which Match is used: `, AT RANDOM`, `, HIGHEST ?p` or `, LOWEST ?p`. It never changes whether the condition holds.
_Avoid_: Selector, filter, sort, order by

**For each**:
A Body Statement, `FOR EACH <condition>:`, that runs its Block once for every Match of the condition, taken when the Body reaches it.
_Avoid_: Loop, iteration, foreach, map

**Body**:
The ordered Statements a Plan carries out.
_Avoid_: Procedure, steps

**Failure**:
What happens when a Plan can't carry out one of its Statements: the Plan stops there, and nothing it already did is undone. A Goal fails when its Plan fails or no Plan for it applies, and so does every Plan waiting on it.
_Avoid_: Error, exception, crash

**Trace**:
The record an Agent leaves of each Failure and runtime warning: what failed, why, and what failed in turn because of it. It explains a run after the fact; where it is written depends on the Target.
_Avoid_: Stack trace, error log

**Random choice**:
A Body Statement that runs exactly one of its Options, picked at random, written `EITHER:` … `OR:`.
_Avoid_: Group, switch, random block, selector

**Option**:
One `EITHER` or `OR` Block of a Random choice.
_Avoid_: Branch (kept for `IF`), case, alternative

**Weight**:
How likely an Option is to be picked compared with the others, written `, WEIGHT …` on its header. An Option without one has weight 1.
_Avoid_: Chance, probability, percentage

**Label**:
An optional tag on a Plan's Trigger that influences how the Plan is chosen or what it changes. The set is fixed by the language: Suits and Shifts.
_Avoid_: Flag, annotation, modifier

**Precedence**:
The order in which Plans from different Playbooks, Plots or Phases are considered when several could react to the same Trigger on one Agent. It is written by whoever puts them together (a Plot), never inside a Playbook about another.
_Avoid_: Priority, salience, rank

**Suits Label**:
A Label saying which Propensity values a Plan best fits, written `, SUITS sympathy AT -0.5`. It is the only Label that affects which Plan runs.
_Avoid_: Temper, mood Label, propensity annotation

**Shifts Label**:
A Label saying how running a Plan changes the Agent's Moods, written `, SHIFTS aggressiveness BY 0.2`.
_Avoid_: Effects, post-effects, mood change

**Selection function**:
The Target's way of choosing among equally ranked Plans by the Agent's Propensities. It only ever chooses where a designer allowed it: among Suits alternatives, or between Playbooks declared tied.
_Avoid_: Temper selection, option selection, utility

**Suits alternative**:
One of several Trigger Blocks in a Playbook with the same Trigger, all carrying a Suits Label. They are different Plans even with identical Contexts, and the Selection function picks among those whose Context holds.
_Avoid_: Mood alternative, variant, duplicate plan

**Statement**:
A single step of a Plan's Body: an Action, a Director Statement, control flow (`IF`/`ELSE`), or a Random choice. An `IF` is checked when the Body reaches it, unlike the Context.
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
An Action built into Regia that any Agent can use, for changing its own Facts and Goals (`LEARN`, `FORGET`, `CHANGE`, `PURSUE`, `DROP`), sending (`TELL`, `ASK`, `SIGNAL`), printing, waiting for a Duration (`WAIT`), or failing on purpose (`FAIL`). It is written without `DO`.
_Avoid_: Built-in, primitive, internal action, BELIEVE, ACHIEVE

**Director Statement**:
A Statement only a Director can use, changing the Plot's infrastructure (such as `ASSIGN`, `UNASSIGN`, `TRANSITION`, `START SUBPLOT`, `END SUBPLOT`, `END PLOT`). Director Statements never fail.
_Avoid_: Director action, plot command, `Role DO` (1.0 order to a Role)

## Files and names

**Import**:
A line at the top of a file, `IMPORT "path".`, that makes another file's declarations visible, together with everything that file imports in turn.
_Avoid_: Include, require, use

**Entry file**:
A file the Transpiler is given to start from.
_Avoid_: Main file, root file (Root is kept for the Root Plot)

**Program**:
Every file reachable from the Entry files through Imports. A name means the same thing everywhere in a Program.
_Avoid_: Project, package, module, build

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

**Instancing**:
The information that turns a Program into a running cast: which Plot is the Root Plot, which kinds of Agent exist and how many, their starting Propensity values, and settings for a Target. It sits at a different abstraction level from the rest of the language and is optional.
_Avoid_: Deployment, configuration, compilation settings

**Instancing comment**:
A line of Instancing written inside a Regia file, starting with `#%` (or enclosed in `#%[ … ]#`).
_Avoid_: Compilation comment, deployment config

**Agent kind**:
A sort of Agent in one build, such as `noble`: which Root Plot Roles its Agents play, how many start, and their starting Propensity values. The game names a kind when it adds an Agent. Regia code never mentions kinds; Plans address Roles.
_Avoid_: Archetype, class, prefab, template, Role (a Role belongs to a Plot)

**Agent declaration**:
The Instancing Block that describes an Agent kind, written `AGENT noble PLAYS Guest:` with `COUNT` and Propensity values inside.
_Avoid_: Agent definition, spawn rule

**Instancing file**:
A `.regin` file holding only Imports and Instancing, written without the `#%` markers. It overrides the Instancing of the files it imports.
_Avoid_: Config file, cast file, `.jcm` (the Jason file it can produce)

**Target**:
A language Regia is translated into so that it can run, for example AgentSpeak.
_Avoid_: Backend, output language

**Transpiler**:
The tool that translates Regia source into a Target.
_Avoid_: Compiler

**Model**:
What a Program means, as the Transpiler understands it once every file is read: each name tied to what it names, across files, with the constructs kept as the designer wrote them. Checks, translation into a Target and the Visual Editor's graph all work from it.
_Avoid_: AST, syntax tree (those describe one file's text), IR

**Visual Editor**:
The tool that shows Regia source next to a flowchart of it, with both sides editable and kept in sync.
_Avoid_: Editor (unqualified), BIRDBRAIN

**Project**:
A folder of Regia files opened together in the Visual Editor. It bounds which files are seen; it is not a namespace, and imports stay relative to the importing file.
_Avoid_: Workspace (the Transpiler's in-editor state), package

**Build**:
The Target files produced from one Entry file, with the Instancing that Entry reaches.
_Avoid_: Compilation, output (unqualified)

**Graph view**:
The Visual Editor's drawing of one Plot. The **Phase map** (the default) draws Phases, transitions labelled with their Triggers, and endings; the **Nested Plans** view draws each Phase as a box of Plan cards. The layout is always automatic.
_Avoid_: Diagram, canvas (the drawing surface, not what is drawn), state chart

**Layer**:
A kind of detail the graph view can show or hide, such as Givings, Messages or Subplots. Layers are off by default and are an editor setting, never part of the source.
_Avoid_: Filter, overlay

**Extent**:
A construct together with the comments that belong to it: the comment lines directly above it with no blank line between, and a comment after it on the same line. Moving or deleting a construct in the Visual Editor moves or deletes its extent.
_Avoid_: Span, range, trivia
