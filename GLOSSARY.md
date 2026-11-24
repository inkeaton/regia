# Regia

Regia is a language for describing game agents (NPCs) as BDI agents, written for game designers and programmers alike. This glossary uses the designer-facing names; BDI and target-language terms appear only under _Avoid_.

## Agents and narrative

**Agent**:
A single character living in the game at runtime. An Agent may play several Roles in several Plots at the same time.
_Avoid_: Instance, agent instance, NPC, actor

**Role**:
A class of Agents named by a Plot or a Playbook. A Plot's Role is played by the Agents cast in it; a Playbook's Role is filled by the Plot that gives the Playbook, through a Mapping. A Role's name is local to the Plot or Playbook that declares it. In a Playbook a Role is an address for Messages, and a condition may ask who plays it; it is never a Value, and a Playbook never directs another Agent. Every Plot also has the Role of its whole Cast, without declaring it.
_Avoid_: Agent (1.0 name), character, class, part, slot

**Role setup**:
What every Agent of a Plot's Role starts with, written as the Role's Block: Playbooks, Facts and Goals, given by the Director each time an Agent starts playing the Role in a Staging. A setup may also be written once for the whole Cast. A Phase may carry a setup of its own for a Role: it is given when the Phase is entered and to whoever joins during it, and its Playbooks are taken away when the Phase is left.
_Avoid_: Role instantiation, initial state, starting kit, init block, `STARTS WITH` block (retired spelling)

**Plot**:
A narrative state machine describing how a scenario unfolds through its Phases and the Roles that take part in it. A Plot may take parameters, passed when it is started as a Subplot and fixed for that Staging.
_Avoid_: Story (1.0 name), quest, scenario

**Staging**:
One running copy of a Plot. The same Plot may have several Stagings at once, each with its own Agents and current Phase. Stagings have no names in the language; each knows only its parent and the Subplots it started. A parent tells its Subplots' Stagings apart by their arguments, by matching. An Agent may play in several Stagings of one Plot at once.
_Avoid_: Plot instance, run, session

**Cast**:
The Agents playing a Plot's Roles in one Staging. It is set when the Staging starts and changes only when Agents join or leave the Program. A Plot can address it as a Role, written `CAST`, in which each Agent counts once however many Roles it plays.
_Avoid_: Role instances (Target-level term), participants, members

**Joining**:
An Agent entering the Program while it runs, because the game spawned it. It joins the Root Plot's Cast in the Roles of its Agent kind, never a Subplot already running. Regia 1.5 has no joining: there the game can't spawn an Agent mid-run.
_Avoid_: Spawning, arriving, entering (a Plot)

**Leaving**:
An Agent leaving the Program while it runs. It stops playing every Role in every Staging at once. An Agent that is dead but still in the world has not left.
_Avoid_: Despawning, dying, exiting (a Plot)

**Root Plot**:
The one Plot every Agent starts in; every other Plot is a Subplot below it. Instancing names it with `ROOT`; it is never guessed. Baseline behaviour is a Playbook the Root Plot gives out.
_Avoid_: Default story, main plot, world plot

**Phase**:
One of the mutually exclusive states of a Plot. A Plot that declares Phases is in exactly one at a time, starting in the one marked `INITIAL`, and its Director can ask which one. Moving from one Phase to another is a transition. A Plot may declare none, and then has only its `DURING PLOT` Plans.
_Avoid_: State, stage

**Timeout**:
A Plan of a Plot that runs once a Duration has passed since a Phase was entered, or since the Staging started, written `AFTER`. A timeout is imposed on Agents from outside, so only a Plot has one; an Agent that chooses to wait writes `WAIT`.
_Avoid_: Timer, delayed trigger, deadline

**Subplot**:
A Plot started from within another Plot, which becomes its parent. The parent's Roles are mapped onto the Subplot's Roles, and its cast is fixed when it starts. It runs until it ends itself, the parent ends it, or the parent ends. The parent hears how it ended: the Subplot **finished** (ended itself, with or without an Outcome), or was **dropped** (the parent stopped it), and in either case that it **ended**. It hears nothing only when the parent is ending too.
_Avoid_: Child story, nested plot

**Outcome**:
The Cue a Subplot finishes with, handed to its parent so the parent can react to how it went. A Subplot has no success or failure: the Outcome says how it went. It is to a Subplot what a Reason is to a failed Goal: the Cue an ending carries.
_Avoid_: Result, return value, ending (when meaning the Cue)

**Mapping**:
How a Plot fills a Role of a Playbook it gives, or of a Subplot it starts, with one of its own Roles, with a number or share of that Role's Agents picked at random, with a Role minus the Agents of another, or with one Agent held by a Placeholder. Roles with the same name, ignoring case, are mapped without writing it.
_Avoid_: Binding, casting, role assignment

**Giving**:
One handing of a Playbook to Agents by a Plot, with its own Mappings. A giving belongs to the Staging that made it, and only that Staging takes it away. An Agent may hold several givings of the same Playbook; they add up, and taking one away leaves the others. Taking a Playbook from one Agent reaches the givings made the way it names: to that Agent, to a Role it plays, or every way. A giving to a whole Role is standing: it also reaches Agents who join the Role later, until it is taken away. A giving to one Agent held by a Placeholder is not. A giving ends when it is taken away, when its Staging ends, or, if it was made for a Phase, when that Phase is left. A Playbook can react to its first giving arriving and to its last one going. When the last one goes, the Playbook **closes**: its running Plans stop, and only the Plans that the stop itself sets off (the dropped Goals' endings, then its own reaction to being taken away) still run, through the givings as they were. A Playbook on an Agent is given, closing, or not given.
_Avoid_: Assignment (when meaning the result), grant

**Director**:
The behind-the-scenes agent that runs a Plot: it moves the Plot between Phases, gives Playbooks to Roles, tells and asks its Agents through Messages, and reacts to the game, to Signals and to how the Goals it asked ended. It has its own Facts but no Goals and no Propensities, and it never reads its Agents' Facts. It nudges its Agents towards the Plot's outcome, and never decides for them.
_Avoid_: Narrator, manager, game master

**Playbook**:
A named set of Plans that are given to or taken away from a Role together. It describes local behaviour, independent of any Plot: what the Agent decides to do, from what happens in the world and from its own Goals. Pressure from outside, such as a timeout, belongs to the Plot that gives it.
_Avoid_: Behaviour, module, plan library

## Vocabulary

**Vocabulary**:
The declared Facts, Cues, Actions, Goals and Propensities that Plans are built from. Names are declared too (`NAME`), but they are Values, not Vocabulary.
_Avoid_: Declarations, components

**Fact**:
Something an Agent (or a Director) knows about the state of the world.
_Avoid_: Belief, knowledge, percept

**Goal**:
An objective an Agent has decided, or been told, to pursue. It is reached when a Plan for it finishes.
_Avoid_: Desire, intention, achievement

**Pursuit**:
One run of a Goal by one Agent, from the request to its ending, with its own Sender. Every request starts a Pursuit, so an Agent can have several of one Goal at once. A Pursuit ends reached, dropped or failed.
_Avoid_: Intention, attempt, instance (of a Goal)

**Cue**:
Something that happens in the world and is over once noticed, declared with `CUE`. It triggers Plans but leaves nothing behind, so a Context can't test it afterwards. To remember it, a Plan records a Fact.
_Avoid_: Event (the wider word), percept, message, happening

**Event**:
Anything that happens to an Agent or a Director and can start a Plan: a Cue, a Fact learned or forgotten, a Goal pursued or over, a Phase entered or left or timed out, a Playbook given or taken away, a Role joined, left or emptied. A Trigger names one Event; each sort of Event is a Trigger kind.
_Avoid_: Happening, occurrence, stimulus

**Signal**:
A Cue an Agent sends to the Directors of every Plot currently giving it the Playbook the Signal is written in. The Directors react to it like any other Cue, and can tell which Role sent it. It is the only thing an Agent's Plan can send to a Director; how a Goal the Director asked ended is reported without one, as it is to an Agent that asked. A Signal that finds no Plan in the Director's current Phase is dropped, and the Trace says so.

**Interface**:
What passes between a Playbook and the Plots that give it, or between a Subplot and its parent: the Goals answered, the Cues and Facts told, the Signals sent and handled, the endings and the Reasons. It is never written; the Transpiler works it out from the whole Program and checks one side against the other.
_Avoid_: Contract, signature, protocol

**Propensity**:
A named disposition of an Agent, either a Trait or a Mood. Labels use Propensities to choose between Plans and to say how running a Plan changes the Agent. An Agent given no value for one is neutral on it. Propensities are not Facts: a Context can't test them.
_Avoid_: Temper, personality, emotion, attribute

**Trait**:
A Propensity that never changes during a run, such as bravery.
_Avoid_: Personality, stat

**Mood**:
A Propensity that changes as the Agent runs Plans, such as sympathy, through a Shifts Label or a `SHIFT` Statement.
_Avoid_: Emotion, dynamic temper, feeling

**Game item**:
A Fact or Cue that the game produces, declared with `GAME`. Plans test, react to and tell it like any other; only a game item can come from the game. Every other Fact and Cue is produced by the Program alone.
_Avoid_: Percept, external fact, environment event, stage item

**External name**:
The name outside Regia for a game item or an Action, given with `AS` when it differs from the Regia name: `ACTION engine.security.summon_guards AS call_guards`. For a game item it is the game's name. For an Action it also says who runs it: without a dot the game does, with a dot the Target's own code does. Only the Target sees it; the source always uses the name after `AS`.
_Avoid_: Alias (when meaning the external name), qualified name, namespace

**Local Vocabulary**:
Facts, Goals and Cues declared inside a Playbook, and Facts declared inside a Plot. They are private to it: other Playbooks on the same Agent, and other files, can't see them. Local Facts and Goals can't be sent. A local Cue can be told, and only holders of the same Playbook react to it.
_Avoid_: Private facts, scoped declarations, inner vocabulary

**Multi-definition**:
Shorthand for declaring several Vocabulary items in one line. It creates no relationship between the items.
_Avoid_: Group, batch declaration

**Parameter name**:
The name given to a slot when a Vocabulary item is declared, such as `person` in `FACT hates(person)`. It documents what the slot means and never binds anything.
_Avoid_: Parameter (when meaning an argument), formal parameter

**Value**:
A fixed Name, Number or string written in a slot, such as `kitchen` in `walk_to(kitchen)`. `ME` is the one Value that isn't fixed in the source: it stands for the Agent running the Plan.
_Avoid_: Constant, atom, bound parameter, literal

**Name**:
A Value that is a word, such as `kitchen` or `roast`, declared with `NAME`. Every Name written in the source is declared; Names arriving from the game or in Messages are not checked.
_Avoid_: Symbol, atom, constant, enum

**Placeholder**:
A blank in a slot, written `?name`, that the Agent fills by matching in a Plan's Trigger or Context, or that the Body fills with `LET ?name BE …`. It is filled once per Plan run and never reassigned.
_Avoid_: Variable, unbound parameter, logic variable, wildcard; naming (for filling with `LET`: a Name is a declared word)

**Number**:
A Value that is a number, whole or decimal, such as `80` or `-0.5`. There is only one kind of Number.
_Avoid_: Integer, float, numeric literal

**Duration**:
An amount of time, written as an Expression followed by `SECONDS` or `MINUTES`. The language says how long; the Target decides which clock measures it. One clock measures every Duration in a run, and it stops while the game is paused.
_Avoid_: Delay, ticks

**Expression**:
Something that works out to a Value: a Value, a filled Placeholder, a random roll, a count of Matches, or these combined with arithmetic.
_Avoid_: Formula, computation, term

## Plans and statements

**Plan**:
A reaction to something that happened, or a recipe for reaching a Goal. It is made of a Trigger, an optional Context and a Body. Several Plans can share one Trigger, each with its own Context; only the first whose Context holds runs.
_Avoid_: Rule, reaction, behaviour

**Trigger**:
The part of a Plan that names the Event that starts it: a Cue, a Fact learned or forgotten, a Goal pursued, a Pursuit ending (reached, dropped, failed, or any of the three), and the others listed under Trigger kind. One Trigger can head several Plans, which share everything written in it.
_Avoid_: Condition, head

**Trigger kind**:
A sort of Event that starts a Plan, such as a Cue happening or a Fact being learned. Written as a word after the item (`LEARNED`, `FORGOTTEN`, `REACHED`, `DROPPED`, `FAILED`, `FINISHED`, `ENDED`), or as `TO` for a Goal recipe, or `AFTER` for a Timeout. A few have no item and are about the Block they are written in: `ENTERED` and `EXITED` for a Phase, `ASSIGNED` and `REMOVED` for a Playbook.
_Avoid_: Event type

**Quota Trigger**:
A Trigger that fires once enough different Agents of a Role have sent the same Cue, written `FROM ALL Guest`, `FROM 3 OF Guest` or `FROM 50% OF Guest`. Each Agent counts once, and the count starts again after it fires, so it fires every time the count fills. Its Plan reads which Agents were counted, and what they sent, with `SENT`.
_Avoid_: Quantifier, aggregate condition, barrier, threshold trigger

**Sender**:
The Agent or Director that sent what a Trigger reacts to, such as a Signal, a Message or a Goal. Each Pursuit keeps the Sender of its own request. A Trigger can restrict or name it with `FROM`. Things the game or the Agent itself caused have no Sender; `FROM GAME` and `FROM ME` match them, and several alternatives are joined with `OR`. The Sender of a Pursuit hears how it ended, and names the Agent who pursued it with `BY`.
_Avoid_: Source

**Message**:
A Fact, a Cue or a request to pursue a Goal that one Agent sends to others. A told Fact or Cue becomes the receiver's own, like one from the game; a requested Goal becomes the receiver's own Goal. Messages only add, never take away.
_Avoid_: Communication, performative, speech act

**Recipient**:
Who a Message goes to: an Agent held by a Placeholder, every Agent playing a Role, a number or share of them picked at random when it is sent, or everyone. A Director may also write its whole Cast, or a Role minus some Agents. Never the sender, and never an Agent named in the source.
_Avoid_: Receiver (when meaning the written target), addressee, target

**Context**:
The condition that must hold for a Plan to be chosen, written after `GIVEN`. It is checked once, when the Plan is chosen, before any of its Body runs.
_Avoid_: Guard, precondition, IF (when meaning the context)

**Match**:
One way a condition holds: a Value for each of its blanks. When a condition has several Matches, one is used and the language doesn't say which, unless a Pick chooses.
_Avoid_: Unifier, binding, solution, result

**Pick**:
A clause on a condition's header that chooses which Match is used: `, RANDOMLY`, `, HIGHEST ?p`, `, LOWEST ?p` or `, WEIGHT …`. It changes whether the condition holds only when it leaves no Match to use.
_Avoid_: Selector, filter, sort, order by

**For each**:
A Body Statement, `FOR EACH <condition>:`, that runs its Block once for every Match of the condition, taken when the Body reaches it.
_Avoid_: Loop, iteration, foreach, map

**Body**:
The ordered Statements a Plan carries out.
_Avoid_: Procedure, steps

**Failure**:
What happens when a Plan can't carry out one of its Statements: the Plan stops there, and nothing it already did is undone. A Pursuit fails when its Plan fails or no Plan for its Goal applies, and so does the Plan waiting on it. Dropping a Goal is not a Failure, for the Goal or for anything waiting on it. A Failure made on purpose may carry a Reason.
_Avoid_: Error, exception, crash

**Reason**:
The Cue a Plan gives when it fails on purpose, saying why in the designer's words. The Failure carries it to every Goal that fails because of it and to whoever asked for the Goal. A Failure nobody chose has no Reason; what went wrong is in the Trace.
_Avoid_: Cause (the Trace's word for what went wrong), error, exception

**Trace**:
The record of what a run did, in order: the Actions done, Messages sent, Goals pursued and how they ended, Phase changes, Stagings starting and ending, Givings and cast changes, and every Failure and runtime warning with what failed, why, and what failed in turn because of it. It also says what didn't run (a Signal no Plan took), and why a Plan ran rather than its rivals. It explains a run after the fact, and a behaviour case checks a run against it. It is written to a file and shown on the console at the same time.
_Avoid_: Stack trace, error log

**Random choice**:
A Body Statement that runs exactly one of its Options, picked at random, written `RANDOMLY:` with one `OPTION:` Block per Option.
_Avoid_: Group, switch, random block, selector

**Option**:
One `OPTION` Block of a Random choice.
_Avoid_: Branch (kept for `IF`), case, alternative

**Weight**:
How likely an Option, or a Match of a weighted Pick, is to be picked compared with the others, written `, WEIGHT …`. An Option without one has weight 1. A Weight of 0 or less means never.
_Avoid_: Chance, probability, percentage

**Roll**:
A random Number from `RANDOM(a, b)`. It is whole unless a bound is written as a decimal number, whatever values the bounds work out to. A starting Propensity value is always a decimal roll.
_Avoid_: Random value, dice

**Seed**:
The number a run's random draws start from. With the same seed, every random draw the language makes comes out the same. A Build may set it in Instancing, and a seed given when the run starts takes its place.
_Avoid_: Random state

**Label**:
An optional tag on a Plan's Trigger that influences how the Plan is chosen or what it changes. The set is fixed by the language: Suits and Shifts.
_Avoid_: Flag, annotation, modifier

**Precedence**:
The order in which Plans from different Playbooks, Plots or Phases are considered when several could react to the same Trigger on one Agent. It is written by whoever puts them together (a Plot), never inside a Playbook about another.
_Avoid_: Priority, salience, rank

**Falling through**:
What a Trigger does when a Trigger Block that could react to it has no Context that holds and no `ELSE`: it passes to the next Plan in the Precedence. It is the same for every kind of Trigger. A Trigger Block with an `ELSE` or with no Context never lets a Trigger fall through.
_Avoid_: Passing, bubbling, fallback (kept for a Goal started after a failure)

**Suits Label**:
A Label saying which Propensity values a Plan best fits, written `, SUITS sympathy AT -0.5`. It is the only Label that affects which Plan runs.
_Avoid_: Temper, mood Label, propensity annotation

**Shifts Label**:
A Label saying how running a Plan changes the Agent's Moods, written `, SHIFTS aggressiveness BY 0.2`. When the change happens is the Target's.
_Avoid_: Effects, post-effects, mood change

**Shift**:
The Statement that changes a Mood at the point where it runs, written `SHIFT aggressiveness BY 0.2`.
_Avoid_: Mood change, effect

**Selection function**:
The Target's way of choosing among equally ranked Plans by the Agent's Propensities. It only ever chooses where a designer allowed it: among Suits alternatives, or between Playbooks declared tied. How it weighs a fit belongs to the Target.
_Avoid_: Temper selection, option selection, utility

**Suits alternative**:
One of the Trigger Blocks in a Playbook with the same Trigger, when at least one of them carries a Suits Label. They are different Plans even with identical Contexts, and the Selection function picks among those whose Context holds.
_Avoid_: Mood alternative, variant, duplicate plan

**Neutral alternative**:
A Suits alternative, or a candidate in a tie, with no Suits Label. It competes as an Agent with nothing particular about it would fit.
_Avoid_: Default alternative, fallback, unlabelled Plan

**Statement**:
A single step of a Plan's Body: an Action, a Director Statement, control flow (`IF`/`ELSE`), or a Random choice. An `IF` is checked when the Body reaches it, unlike the Context.
_Avoid_: Instruction, command

**Block**:
A group of Statements or declarations that belong to a header, such as a Playbook, a Trigger, a `GIVEN` or an `IF` branch. Its body is indented under the header, or written on the header's line (an Inline block). A Block meant to be empty holds `PASS`.
_Avoid_: Scope, suite, section

**Block header**:
The line, or part of a line, that opens a Block. It always ends with `:`.
_Avoid_: Head, opener

**Clause**:
An optional part of a Block header or Statement that applies to the whole of it, written after its core as `, KEYWORD …`: the Sender (`, FROM …`), a Label, a Pick, `, WITHOUT WAITING`, `, MAPPING …`. A word that only finishes another word (`FAILED WITH r`, `SHIFT m BY n`) is a complement, not a Clause, and takes no `,`.
_Avoid_: Modifier, option, suffix, qualifier

**Inline block**:
A Block whose body is written on the same line as its header. It ends at a `;` or at the end of the line.
_Avoid_: One-liner, explicit block

**Action**:
Anything an Agent does: acting on the world, changing its own Facts and Goals, or communicating.
_Avoid_: Command, operation

**Custom Action**:
An Action defined outside Regia and declared in the Vocabulary. Most are game Actions, performed by the game; one whose External name has a dot is the Target's own code. It is always written after `DO`. The game decides when it is done (an arrival, an animation finishing, at once), and can refuse it or report it failed. `DO` waits until it is done; `DO …, WITHOUT WAITING` waits only until the game has accepted it. A waiting `DO` whose Plan is stopped calls its Action off, and the game decides what stopping it means.
_Avoid_: External action, user action, environment action

**Basic Action**:
An Action built into Regia that any Agent can use, for changing its own Facts and Goals (`LEARN`, `FORGET`, `UPDATE`, `PURSUE`, `DROP`), sending (`TELL`, `ASK`, `SIGNAL`), printing, waiting for a Duration or until a condition holds (`WAIT`), or failing on purpose (`FAIL`). It is written without `DO`.
_Avoid_: Built-in, primitive, internal action, BELIEVE, ACHIEVE

**Director Statement**:
A Statement only a Director can use, changing the Plot's infrastructure (such as `ASSIGN`, `REMOVE`, `ENTER`, `START SUBPLOT`, `DROP SUBPLOT`, `END PLOT`). Director Statements never fail.
_Avoid_: Director action, plot command, `Role DO` (1.0 order to a Role)

## Files and names

**Import**:
A line at the top of a file, `IMPORT "path"`, that makes another file's declarations visible, together with everything that file imports in turn.
_Avoid_: Include, require, use

**Entry file**:
The one file a Program starts from. Only an Instancing file can be the Entry of a Build; any file can be the Entry of a check.
_Avoid_: Main file, root file (Root is kept for the Root Plot)

**Active Entry**:
The Entry file whose Program the Visual Editor shows for an open file, when several Entry files reach it: its Diagnostics, its name origins and its Interfaces. The designer switches it; the language doesn't know it.
_Avoid_: Current project, main file, default build

**Program**:
Every file reachable from its Entry file through Imports. A name means the same thing everywhere in a Program.
_Avoid_: Project, package, module, build

**Retired spelling**:
A spelling the language once had and has replaced. Writing it is an error whose hint names the new spelling, and that stays true for ever. A retired keyword stays reserved. Words of Regia 1.0 and of earlier drafts are not retired spellings: they were never part of this language.
_Avoid_: Deprecated syntax, legacy keyword, alias, synonym

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

**Regia 1.5**:
The subset of Regia 2.0 that is built first, by the same Transpiler and Visual Editor. A 1.5 Program is a 2.0 Program and does the same thing there. A 1.5 build names what it leaves out as Regia 2.0, and never guesses at it.
_Avoid_: 1.5 mode, lite, Regia light, preview

**Instancing**:
What holds for one cast of a story, in one game setup, fixed before the run starts: which Plot is the Root Plot, which Agent kinds and individual Agents exist and how many start, what they start with, the seed, and settings for a Target. What holds for every cast belongs to the Program, and what only comes up during the run belongs to the game. A Build always has some: at least the name of its Root Plot.
_Avoid_: Deployment, configuration, compilation settings

**Agent kind**:
A sort of Agent in one build, such as `noble`, that the game may have many of: which Root Plot Roles its Agents play, how many start, and what each starts with. It may be built on other kinds. The game names a kind when it adds an Agent. Regia code never mentions kinds; Plans address Roles.
_Avoid_: Archetype, class, prefab, template, Agent declaration, Role (a Role belongs to a Plot)

**Individual Agent**:
One particular Agent declared in Instancing under its own name, such as `gawain`: what it plays and starts with, possibly taken from Agent kinds. It is in the starting cast and is never spawned, and its name is the Agent's name in the game.
_Avoid_: Named instance, singleton kind, character

**Instancing file**:
A `.regin` file holding only Imports and Instancing, the only place Instancing is written. It overrides the Instancing of the files it imports, one line at a time.
_Avoid_: Config file, cast file, `.jcm` (the Jason file it can produce), Instancing comment

**Target**:
A language Regia is translated into so that it can run, for example AgentSpeak.
_Avoid_: Backend, output language

**Transpiler**:
The tool that translates Regia source into a Target.
_Avoid_: Compiler

**Model**:
What a Program means, as the Transpiler understands it once every file is read: each name tied to what it names, across files, with the constructs kept as the designer wrote them. Checks, translation into a Target and the Visual Editor's graph all work from it.
_Avoid_: AST, syntax tree (those describe one file's text), IR

**Diagnostic**:
An error or a warning the Transpiler reports about a Program, pointing at the place in the source it concerns. An error stops the Build; a warning doesn't.
_Avoid_: Compile error, lint, message

**Diagnostic code**:
The stable name of one kind of Diagnostic, such as `R1301`: `R`, the spec chapter that defines it, and its number in that chapter. It never changes meaning and is never reused.
_Avoid_: Error number, error id

**Allowed warning**:
A warning the writer has seen and accepts, marked with `#@allow` on the declaration it falls in. It is hidden but not gone: it can be shown again on request.
_Avoid_: Suppressed warning, ignored warning

**Conflict report**:
The list, per Role and Trigger, of the Plans that compete for it in the order they rank, with the reason for each place. It is a report, not a Diagnostic.
_Avoid_: Precedence table, priority list

**Trace code**:
The stable name of one kind of runtime warning, Failure cause, or thing that didn't run in the Trace, such as `T0901`: `T`, the spec chapter that defines it, and its number in that chapter. Like a Diagnostic code, it never changes meaning and is never reused.
_Avoid_: Error number, warning id

**Conformance case**:
A small Program kept beside the spec, with the outcome the spec promises for it: the exact Diagnostics it gets, or, for a scripted run, the Trace it leaves. A Transpiler is correct when it passes them all.
_Avoid_: Test, fixture, golden file, example

**Scripted game**:
The stand-in that plays the game's part while a Conformance case runs: it sends the case's Cues, Facts, joins and leaves, and answers each Action, through the same connection the real game uses.
_Avoid_: Mock, fake environment, simulator

**Visual Editor**:
The tool that shows Regia source next to a flowchart of it, with both sides editable and kept in sync.
_Avoid_: Editor (unqualified), BIRDBRAIN

**Project**:
A folder of Regia files opened together in the Visual Editor. It bounds which files are seen; it is not a namespace, and imports stay relative to the importing file.
_Avoid_: Workspace (the Transpiler's in-editor state), package

**Build**:
The Target files produced from one Instancing Entry file, with the Instancing that Entry reaches.
_Avoid_: Compilation, output (unqualified)

**Build folder**:
Where a Build is written, named after its Entry file's path. It also keeps the Traces of past runs, which a new Build never removes.
_Avoid_: Output folder, dist

**Infrastructure**:
The fixed Target code every Build carries, the same for every Program, that runs Regia's own machinery (Givings, Phases, Stagings, Precedence) around the designer's Plans.
_Avoid_: Runtime, boilerplate, infrastructural plans

**Generated name**:
A name the Transpiler makes up for its own use in Target code, such as the private name of a Local Fact. Designers can't write one, so it never collides with theirs.
_Avoid_: Mangled name, internal name

**Graph view**:
The Visual Editor's drawing of one Plot. The **Phase map** (the default) draws Phases, transitions labelled with their Triggers, and endings; the **Nested Plans** view draws each Phase as a box of Plan cards. The layout is always automatic.
_Avoid_: Diagram, canvas (the drawing surface, not what is drawn), state chart

**Layer**:
A kind of detail the graph view can show or hide, such as Givings, Messages or Subplots. Layers are off by default and are an editor setting, never part of the source.
_Avoid_: Filter, overlay

**Extent**:
A construct together with the comments that belong to it: the comment lines directly above it with no blank line between, and a comment after it on the same line. Moving or deleting a construct in the Visual Editor moves or deletes its extent.
_Avoid_: Span, range, trivia
