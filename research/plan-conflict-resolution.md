# Research: how existing systems resolve conflicts between plans and behaviour sources

Input for designing Regia 2.0's `PRIORITY` model. This note lays out options with evidence. It does not pick one.

- **Question:** When several plans, or several sources of behaviour, apply at once, how do BDI platforms and game-AI architectures decide what runs? What models exist (absolute vs relative priority, hierarchical priority, utility scoring, mutual exclusion, intention interleaving), and what do they cost a non-programmer designer?
- **Date:** 2026-11-03
- **Regia context:** A Regia Agent can hold Playbooks from several Plots at once, so several `WHEN` plans can react to the same event. The current docs already sketch `WHEN insult_heard PRIORITY 5` and `WHEN assassin_spotted PRIORITY 9` and note the priority system is "not currently implemented nor enforced" and that "relative priority, and hierarchical ones" should be considered (`docs/first reasonings/2 - Language Architecture.md`, `4 - Plans and Playbooks.md`).

Source-quality legend: **[P]** primary (source code, official manual, the author's own paper or talk). **[S]** secondary (third-party slides, summaries); used only where the primary was unreachable, and flagged.

---

## 1. The conflict points, in vocabulary every system shares

Every system below resolves conflicts at one or more of four distinct points. Keeping them apart matters, because "priority" means something different at each one.

| # | Decision point | Question it answers | Jason name |
|---|---|---|---|
| 1 | **Event selection** | Several things happened; which do I react to first? | `selectEvent` |
| 2 | **Option (plan) selection** | Several plans apply to *this* event; which one do I adopt? | `selectOption` |
| 3 | **Intention selection / scheduling** | I am pursuing several things; which advances now, and may one pre-empt another? | `selectIntention` |
| 4 | **Action arbitration / mutual exclusion** | Two running behaviours want the same body part, resource, or incompatible effect | (none built in) |

A Regia Agent holding Playbooks from two Plots hits point 2 when both Playbooks have a `WHEN` for the same event, and point 3/4 when both plans are running and want incompatible things (e.g., "flee" vs "guard the door").

---

## 2. BDI platforms

### 2.1 Jason / AgentSpeak (Regia's target)

What Jason does by default, read from the interpreter source (`jason-lang/jason`, `master` at commit `84e131b`, 2026-10-30) **[P]**:

- **Event selection is FIFO.** `selectEvent` is `return events.poll();` (`jason-interpreter/src/main/java/jason/asSemantics/Agent.java`).
- **Option selection is "first applicable plan in plan-library order".** The reasoning cycle computes relevant plans, then applicable plans (`TransitionSystem.java`, `C.RP = getAg().relevantPlans(...)`, `C.AP = getAg().applicablePlans(C.RP)`), then calls `ag.selectOption(C.AP)`, whose default body is `return options.removeFirst();` (`Agent.java`). Exactly **one** plan is adopted per event; the other applicable plans do not run.
- **Plan-library order is source order**, adjustable at runtime: `PlanLibrary.add(Plan p, Term source, boolean before)` — "If *before* is true, the plan will be added in the beginning of the PlanLibrary; otherwise, it is added in the end" (`pl/PlanLibrary.java`). Exposed to AgentSpeak as `.add_plan(Plan, Source, begin|end)`.
- **Intention selection is round-robin.** `selectIntention` is `return intentions.poll();` with the comment "make sure no intention will 'starve'"; executed intentions are re-queued at the end via `Circumstance.addRunningIntention` (`I.offer(intention)`). So concurrent intentions **interleave** one step at a time.
- **Atomic plans are the only built-in exclusion mechanism.** A plan labelled `@l[atomic]` sets `isAtomic` (`asSyntax/Plan.java`), and `applySelInt` checks "Rule for Atomic Intentions" first: `C.SI = C.removeAtomicIntention(); if (C.SI != null) return;` (`TransitionSystem.java`). An atomic intention runs to completion before any other intention gets a step. There is no notion of resource-level mutual exclusion.
- **No built-in numeric plan priority.** The only plan-label annotations the interpreter interprets are `atomic`, `breakpoint` and `all_unifs` (`Plan.setLabel`). Any other annotation (e.g. `[priority(5)]`) is legal syntax but ignored unless custom code reads it.
- **Two customisation hooks:**
  1. *Java override.* Subclass `Agent` and override `selectOption` / `selectIntention` / `selectEvent` (the classic route, described as user-customisable selection functions in Bordini, Hübner & Wooldridge, *Programming Multi-Agent Systems in AgentSpeak using Jason*, Wiley 2007).
  2. *AgentSpeak rule `select__option/4`* (newer). If the belief base contains rules for `select__option(Event, IntentionId, Plan, Unifier)`, `selectOptionBB` keeps only the options for which the rule holds, then `removeFirst()` (`Agent.java`; `bb/DefaultBeliefBase.java` sets `hasSelectOption` when such a literal is added). The demo filters on a label annotation: `select__option(E,I,P,U) :- P = {@Label +!Trigger : Context <- Body} & Label =.. [Functor, Terms, Annots] & .member(kk, Annots).` (`demos/selectOptionBB/bob.asl`). This means **a priority filter can be generated as plain AgentSpeak**, without Java, as long as it can be phrased as "keep these options" (combine with plan order for "pick the best").
- **Reflective control from AgentSpeak:** `.relevant_plans`, `.drop_intention`, `.suspend`, `.succeed_goal`, `.fail_goal` (all in `jason/stdlib/`) let one plan pre-empt another by dropping or suspending its intention. This is how "a higher-priority Plot interrupts a lower one" would have to be compiled today.

**Consequence for Regia.** If two Playbooks each contribute `+insult_heard` plans to one agent, stock Jason runs *only the first applicable one in source order*. "Both fire" is not the default; it needs either distinct events, a dispatcher plan that posts one `!!subgoal` per Playbook (each becomes its own interleaved intention), or a custom `selectOption`.

### 2.2 2APL

From Dastani's *Syntax and Operational Semantics of 2APL* slides (MAS Programming Summer School 2014) **[P]**:

- Three rule kinds: PG-rules (goal → plan), PC-rules (events/messages/procedure calls → plan), PR-rules (plan repair).
- Deliberation cycle: "Repeat — Apply PG-rules; For each internal event, find and apply a PR-rule; For each message and external event, find and apply a PC-rule; **Execute one step for each plan**." All current plans interleave step-by-step.
- Atomic plans: grammar `<atomicplan> ::= "[" <plan> "]"`; atomic plans execute without interleaving with other plans (also stated in Dastani, "2APL: a practical agent programming language", JAAMAS 16(3), 2008).
- **Goal base is ordered.** "The successful execution of a goal adopt action `adopta(g)` adds the goal to the beginning of the goal base" (and `adoptz` to the end). Ordering of goals is the main implicit priority device.

*Not verified from primary text:* exactly how 2APL breaks ties between several applicable PG-rules for the same goal (the JAAMAS paper was paywalled). Treat "rule order" as likely but unconfirmed.

### 2.3 GOAL

- Rules live in modules; each module has an `order` option. Hindriks' slides: "Default: `[order=linear]`. Other options: random, linearall, randomall" **[S]** (Hindriks, *Agent Programming in GOAL: Modules*, via SlideServe). GOAL-Eclipse Quick Start Guide **[P]**: "in a module that uses the random order, a rule that is applicable is randomly selected"; the event module "by default uses the linearall order".
- Semantics, per Huang & Alexander, *Semantic Mutation Testing for Multi-Agent Systems* (EMAS 2015) **[S]**: under `linearall`, "rules are examined in the order they appear ... and all enabled rules are selected"; `linear` fires only the first applicable rule.
- Wikipedia (citing Hindriks) **[S]**: when several actions are enabled, "a GOAL agent will select an arbitrary enabled action for execution."
- GOAL has no intention stack; a selected rule's action runs immediately, so there is no interleaving question.

**Design takeaway:** GOAL exposes the "first only vs all applicable" choice *per module* as a one-word option. That is directly the "which fires, or both" question in Regia's docs.

### 2.4 JACK

From the *JACK Intelligent Agents Agent Manual*, Release 5.3 (AOS, 2005) **[P]**:

- **Prominence (default ordering).** "In the absence of precedence, the order in which plans appear in an agent or capability (the order of the `#uses plan` declarations) determines the order in which the corresponding entries appear in the applicable plan set" (§8.1.4). "Note that inner capabilities are more prominent than plans." *Capabilities* are JACK's reusable plan bundles, i.e. the closest analogue to Regia Playbooks; their prominence is decided by structure, not numbers.
- **Precedence (numeric rank).** A plan may define `getInstanceInfo()` returning `PlanInstanceInfo.def[0..9]`; "the entries in the applicable plan set are ordered according to rank ... 0 is the lowest rank and 9 is the highest", and a higher rank wins "regardless of their prominence" (§8.1.5). The rank can be computed per binding from beliefs (the manual's example reads `<"important",8>, <"normal",5>, <"background",3>` from a belief set), i.e. **dynamic** priority.
- "The applicable plan set only includes the highest ranking plans" for rule-behaviour events (§5).
- **ApplicableChoice:** `first` ("The first plan instance generated by the `#uses plan` declaration ... is chosen. [DEFAULT]") or `random` ("A plan is chosen from the applicable set at random") (§5, Table 5-8).
- **Meta-level reasoning.** When more than one plan applies, a `PlanChoice` event can be posted and handled by an ordinary plan that inspects the applicable set and picks one; "If the meta-level reasoning plan fails and does not select a plan for execution, the default plan selection method is invoked" (§5.3.1.1, §8).
- **Task (intention) scheduling.** Default `SimpleTaskManager` "persist[s] with its currently active task" until it blocks; `SimpleRRTaskManager(<steps>)` "rotates its efforts between all tasks", each allowed a number of plan steps (§3.4.3). So JACK makes **non-interleaved vs interleaved** an explicit per-agent choice.

JACK is the most complete example of a layered model: structural order → numeric rank (0–9, possibly computed) → optional random tie-break → optional meta-plan override.

### 2.5 Priority and conflict extensions in the BDI literature

- **AgentSpeak(RT)** — Vikhorev, Alechina & Logan, "Agent programming with priorities and deadlines", AAMAS 2011 **[P]**. Priorities attach to **events** (hence intentions), not plans: "Priorities define a partial order over events and are expressed as non-negative integer values, with larger values taken to indicate higher priority"; syntax `+!bid(client2, a102, price2)[1010, 15]` (deadline 1010, priority 15); default priority 0. The scheduler processes candidate intentions "in descending order of priority", adding each if the schedule stays feasible; "intentions which are dropped are incompatible with some scheduled higher priority intention(s)", and scheduling is "pre-emptive". Unprioritised tasks behave as plain AgentSpeak. *Relevance:* a worked design for "priority = which intention survives/runs", layered on AgentSpeak.
- **Goal interference** — Thangarajah, Padgham & Winikoff, "Detecting & avoiding interference between goals in intelligent agents", IJCAI 2003 **[P, abstract]**: agents should not "blindly pursu[e] goals that will conflict"; uses summary information about plan effects to detect and avoid negative interactions. *Relevance:* the alternative to designer-specified priority is declaring effects/resources and letting the runtime detect clashes.
- **Intention progression problem** — Logan, Thangarajah & Yorke-Smith, "Progressing intention progression: a call for a goal-plan tree contest", AAMAS 2017 (Blue Sky) **[P, abstract]**: frames *which plan to use for a goal* and *which intention to advance next* as one open scheduling problem, noting the research is fragmented. *Relevance:* confirms points 2 and 3 above are recognised as the hard part; there is no settled standard.
- **BOID** — Broersen, Dastani, Hulstijn, Huang & van der Torre, "The BOID architecture: conflicts between beliefs, obligations, intentions and desires", AGENTS 2001 **[S for details]**. Conflicts between *sources* of motivation (e.g. obligations imposed from outside vs the agent's own desires) are resolved by an ordering among components; **agent types** ("realistic", "social", "selfish", "stable") are defined as constraints on that ordering. *Relevance:* closest academic analogue to "Director-imposed Plot behaviour vs a Role's own Playbook"; it suggests priority between *sources* can be a per-character personality setting rather than per-plan numbers.

---

## 3. Game AI

### 3.1 Behaviour trees: priority = position

- Dawe, Gargolinski, Dicken, Humphreys & Mark, "Behavior Selection Algorithms: An Overview", *Game AI Pro* ch. 4 (2013) **[P]**: "At each level of the tree, only one behavior can be selected, so if a behavior executes, none of its siblings will be checked ... the algorithm has decided on the highest-priority behaviors to run." Behaviours "can (and should) be written to be completely unaware of each other". Known failure mode: a citizen fleeing combat stops fleeing once safe, "the highest-priority behavior that takes over could take the citizen back into the combat area, making the citizen continually loop between two behaviors" (**oscillation**). Extensions: random or utility-based selectors, and "nonexclusive" behaviours that let siblings also run.
- Unreal Engine BT decorators, *Observer Aborts* (Epic docs) **[P]**: "Self: Abort self and any subtrees running under this node. Lower Priority: Abort any nodes to the right of this node. Both: ..." Left-to-right position *is* priority, and pre-emption is an explicit per-condition setting.
- Isla, "Handling Complexity in the Halo 2 AI", GDC 2005. Isla's own text (via search excerpt) describes a prioritized-list decider: "march down a prioritized list of the children. The first one that can run, does, but higher-priority siblings take precedence." **[P, excerpt only]** Course slides summarising the talk state the problem "what happens when the priority is not constant?" and the fix: split alternative triggers into separate **behaviour impulses**, which can run in place or redirect execution **[S]**. *Relevance:* fixed tree-position priority breaks when importance depends on context, and Halo's fix was to give one behaviour several entry points at different priorities.

### 3.2 Utility AI: priority = score

- Dill, "Dual-Utility Reasoning", *Game AI Pro 2* ch. 3 (2015) **[P]**:
  - **Absolute utility** "evaluates each option and takes the one with the highest score" — "best when you want to ensure that the AI always takes the most appropriate action", but "it can become predictable".
  - **Relative utility** "selects an option at random, but it uses the score of each option to define the probability" (weight-based random) — gives variation but "there is always some chance that an option with very low utility will be selected. This can easily make your AI look stupid."
  - **Dual utility** gives each option "a rank and a weight. Rank uses absolute utility to divide the options into categories, and we only select options from the best category. Weight is used to evaluate options within the context of their category." Steps: drop weight ≤ 0; keep highest rank; drop options far below the best weight; weighted-random among the rest. Setting weight to 0 is "a convenient way to mark an option as invalid".
  - Zoo Tycoon 2 case: everyday needs at rank 0; context-locked behaviours (koala in a tree) at rank ~5; scripted marine shows at ranks 98–102, "coordinated by a simple FSM"; dying at rank 1,000,000. **This is a direct precedent for "a narrative state machine raises the rank of its scripted behaviours above a character's ambient behaviours."**
  - Dill emphasises computing utility "in game, at run time. It is not enough to assign fixed weights to the options a priori."
- Game AI Pro ch. 4 **[P]** on utility trade-offs: utility systems "are often somewhat unpredictable ... if your design calls for specific behaviors at very certain moments, you must make a point to override the utility calculations with more scripted actions", and they "can be somewhat challenging to tune ... This is often more art than science."

### 3.3 GOAP: priority = goal ordering; plans are synthesised

- Orkin, "Three States and a Plan: The A.I. of F.E.A.R.", GDC 2006 **[P]**: designers "assign a Goal Set to each A.I. ... These goals compete for activation, and the A.I. uses the planner to try to satisfy the highest priority goal." If no valid plan exists (the rat cannot attack), it "falls back to the lower priority Patrol goal." Example goal priorities in the paper's figure: Work 8.0, Stunned 80.0/100.0.
- Game AI Pro ch. 4 **[P]**: planner-driven characters "remove a lot of the authorial and directorial control ... creating plans that ... do not achieve the broader goals of creating immersive and engaging experiences, and this can then potentially disrupt cinematic set-pieces." *Relevance:* a warning for a narrative DSL; GOAP's conflict model is simple (goal priority + fallback) but authorial control is weak.

### 3.4 Layered / subsumption arbitration

- Brooks, "A robust layered control system for a mobile robot", IEEE J. Robotics & Automation 2(1), 1986 (MIT AI Memo 864) **[P cited; text is a scanned PDF, details via S]**. Behaviour is built as layers of increasing competence; higher layers override lower ones by **suppression** (replacing a lower layer's input for a fixed time) and **inhibition** (blocking its output); lower layers keep running when higher ones are silent. Priority is fixed by wiring, and only a layer that is currently emitting overrides anything.
- *Relevance:* this is "hierarchical priority by source", with the useful property that a silent higher layer costs nothing. It maps naturally onto "Plot layer above Playbook layer above ambient behaviour".

### 3.5 ABL (Façade): specificity, step priority, conflicts, and a drama manager

Mateas & Stern, "A Behavior Language for Story-based Believable Agents", AAAI Spring Symposium on AI and Interactive Entertainment, 2002 **[P]**. ABL is the closest prior art to Regia: a reactive-planning language for authors, with a drama manager sequencing *beats* over autonomous characters.

- **Plan (behaviour) selection by specificity:** "In the event that both preconditions are satisfied, the behavior with the highest specificity is chosen. If there are multiple satisfied behaviors with highest specificity, one is chosen at random." On failure, another not-yet-tried applicable behaviour is chosen.
- **Concurrency:** parallel behaviours make the execution state a tree (the Active Behavior Tree) whose leaves are the runnable steps; "multiple lines of expansion mix (based on priority, blocking on physical acts, and a preference for pursing the current line of expansion)".
- **Mutual exclusion:** "declaration of behavior and step conflicts (and the resulting concept of suspended steps and behaviors)". Conflicting steps are suspended, not cancelled (definitive semantics in Loyall's 1997 Hap dissertation).
- **Priority tiers for interrupts:** handlers are started `with (persistent, priority 20)`, `(persistent, priority 15)`, `(priority 10, ...)`; "Handlers are started in various priority tiers corresponding to the relative importance of handling that interaction ... A higher priority handler can interrupt a lower priority handler", and "In general handlers are higher priority than beat goals so that if an interaction occurs in the middle of the beat goal, the handler will 'wake up' and interrupt it."
- **Meta-behaviours:** reflection lets a behaviour "succeed, fail or suspend a goal or behavior, and modify ... the persistence or priority" of others. Façade's handlers use this to reorder beat goals.

ABL therefore separates three knobs that Regia's single `PRIORITY` currently conflates: **specificity** (which plan for this goal, point 2), **priority** (which running step pre-empts, point 3), and **conflicts** (what cannot run together, point 4).

---

## 4. The models, side by side

| Model | Where seen | What the designer writes | Strengths | Weaknesses for non-programmer designers |
|---|---|---|---|---|
| **Implicit order** (source / declaration order) | Jason default, JACK prominence, GOAL `linear`, BT left-to-right | Nothing; order in file/tree | Zero syntax; deterministic | Invisible; breaks when Playbooks from different files/Plots merge (whose file is "first"?) |
| **First-only vs all-applicable switch** | GOAL `linear`/`linearall`, BT "nonexclusive" | One keyword per group | Answers "which fires, or both" directly | Global switch is coarse; "all" reintroduces point-4 conflicts |
| **Absolute numeric priority** (highest wins) | JACK rank 0–9, AgentSpeak(RT), F.E.A.R. goal priorities, Regia's `PRIORITY 5` draft | A number per plan/event/goal | Easy to read locally; deterministic | Global number space across independent Playbooks; "priority inflation"; ties need a rule; predictable (Dill) |
| **Relative / weighted random** | Utility AI weight-based random | A weight | Variety, believability | Can pick silly low options; hard to test and tune ("more art than science") |
| **Dual / tiered (rank + weight)** | Dill's dual utility, ABL priority tiers | A tier (category) + an in-tier weight | Tiers give hard guarantees (scripted scene beats ambient), weights give variety inside a tier | Two concepts to learn; still a global tier vocabulary |
| **Hierarchical by source / layer** | Subsumption, BOID agent types, JACK "inner capabilities more prominent", Zoo Tycoon FSM-set ranks | Which *layer* a Playbook/Plot belongs to; optionally a per-character ordering of layers | Matches Regia's Plot/Playbook structure; Playbooks need no global numbers; Plot authors don't need to know each other | Needs a rule for two Plots at the same layer; less fine-grained |
| **Specificity** (more specific plan wins) | ABL | A specificity value (or inferred from how constrained the context is) | Natural reading: "the special case overrides the default" | Only chooses among alternatives for one goal; says nothing about pre-emption |
| **Dynamic / computed priority** | JACK `getInstanceInfo()`, utility scores, AgentSpeak(RT) "priority determined by importance of client" | An expression over beliefs (mood, relationship) | Context-sensitive; fits Regia's TEMPER propensities | Harder to predict and debug |
| **Meta-level reasoning** | JACK `PlanChoice`, Jason `select__option`, ABL reflection | A plan/rule that chooses among plans | Unlimited power | Programmer-level; not a designer feature |
| **Pre-emption policy** | UE Observer Aborts, ABL handler tiers, AgentSpeak(RT) | Whether a newly applicable higher-priority behaviour interrupts the running one | Makes interrupt behaviour explicit | Another knob; interrupted behaviour needs resume/abandon semantics |
| **Mutual exclusion / atomicity** | Jason `[atomic]`, 2APL `[ ]`, ABL conflicts | Mark a block atomic, or declare that two acts conflict | Prevents half-finished interleavings ("lock doors" interleaved with "open doors") | Atomic hurts reactivity (Mateas & Stern warn atomic behaviours "could impair reactivity"); conflict declarations need a resource vocabulary |
| **Interleaving vs run-to-completion** | Jason/2APL round-robin, JACK RR vs Simple task manager | Usually a platform default | Interleaving = responsiveness; run-to-completion = predictability | Interleaving is surprising to designers who read a plan as a script |
| **Interference detection** | Thangarajah et al. 2003 | Effects/resources of plans | No numbers; runtime avoids clashes | Research-grade; requires effect annotations |

---

## 5. Observations relevant to Regia (evidence, not a decision)

1. **"Priority" is at least three separate decisions** in every mature system (plan choice, pre-emption/scheduling, mutual exclusion). ABL names all three separately; Jason has hooks for the first two and only `atomic` for the third. A single `PRIORITY n` on a `WHEN` will be read by designers as answering all three.
2. **Stock Jason picks exactly one plan per event**, by source order. Whatever Regia's model is, the transpiler must either order the generated plans, emit a `select__option` rule (pure AgentSpeak, no Java needed), or override `selectOption` in Java. "Both fire" requires restructuring (one sub-intention per Playbook).
3. **Pure absolute numbers are fragile across independently authored modules.** JACK bounds ranks to 0–9 and puts structure (capabilities) before numbers; Dill puts categories before weights. Regia's draft examples already use 5, 9 and 10 in different Plots with no shared scale.
4. **Layer/tier-by-source has the strongest precedent for "narrative overrides ambient":** Zoo Tycoon's show ranks (98–102, set by an FSM), ABL's handlers over beat goals, subsumption's higher layers. This lines up with Plot → Playbook → personality, and BOID shows the ordering of sources can be a per-character trait.
5. **Determinism vs believability is a real trade.** Designers testing a narrative want reproducibility (absolute); players want variety (relative). Dual utility and ABL's random tie-break among equal specificity are the established compromises: deterministic across tiers, varied within one.
6. **Pre-emption needs explicit semantics.** UE makes it a per-condition setting; AgentSpeak(RT) drops incompatible lower-priority intentions; ABL suspends conflicting steps and lets handlers interrupt. In Jason it would compile to `.suspend`/`.drop_intention` calls.
7. **Oscillation is the classic failure of stateless priority** (BT flee/return loop; Halo's "priority is not constant"). Any dynamic-priority option needs hysteresis or commitment, which BDI intentions provide.

## 6. Open questions this research could not settle

- 2APL's exact tie-break among several applicable PG-rules (primary paper paywalled).
- GOAL `linearall`/`randomall` exact semantics from the official manual (only slides, quick-start guide and a third-party paper reached).
- Full Hap/ABL conflict semantics (Loyall 1997 not consulted).
- Halo 2 impulses: only an excerpt of Isla's text plus third-party slides; the Game Developer reprint was not readable from this environment.
- Brooks 1986: scanned PDF; suppression/inhibition details rely on secondary descriptions.

## Sources

Primary:
- Jason interpreter source, `github.com/jason-lang/jason` @ `84e131b`: `jason-interpreter/src/main/java/jason/asSemantics/{Agent,TransitionSystem,Circumstance,Intention}.java`, `asSyntax/Plan.java`, `pl/PlanLibrary.java`, `bb/DefaultBeliefBase.java`, `stdlib/`, `demos/selectOptionBB/bob.asl`.
- Bordini, Hübner, Wooldridge. *Programming Multi-Agent Systems in AgentSpeak using Jason.* Wiley, 2007.
- Dastani. *Syntax and Operational Semantics of 2APL* (slides). https://www.cs.ubbcluj.ro/~gabis/cia/Docs/MASProgrammingSummerSchool_2014/2APLSyntaxSemantics.pdf ; Dastani, "2APL: a practical agent programming language", JAAMAS 16(3), 2008, doi:10.1007/s10458-008-9036-y.
- GOAL-Eclipse Quick Start Guide. https://goalapl.atlassian.net/wiki/spaces/GOAL/pages/4828295/GOAL-Eclipse+Quick+Start+Guide
- AOS. *JACK Intelligent Agents Agent Manual*, Release 5.3. https://aosgrp.com.au/wp-content/uploads/2022/08/JACK-Agent-Manual.pdf (§3.4.3, §5, §8).
- Vikhorev, Alechina, Logan. "Agent programming with priorities and deadlines." AAMAS 2011. https://www.cs.huji.ac.il/~jeff/aamas11/papers/B3_R52.pdf
- Thangarajah, Padgham, Winikoff. "Detecting & avoiding interference between goals in intelligent agents." IJCAI 2003. https://mlanthology.org/ijcai/2003/thangarajah2003ijcai-detecting
- Logan, Thangarajah, Yorke-Smith. "Progressing intention progression." AAMAS 2017. https://ifaamas.csc.liv.ac.uk/Proceedings/aamas2017/pdfs/p768.pdf
- Mateas, Stern. "A Behavior Language for Story-based Believable Agents." AAAI 2002. https://www.qrg.northwestern.edu/Resources/aigames.org/papers2002/MMateas02.pdf
- Dill. "Dual-Utility Reasoning." *Game AI Pro 2*, ch. 3. http://www.gameaipro.com/GameAIPro2/GameAIPro2_Chapter03_Dual-Utility_Reasoning.pdf
- Dawe et al. "Behavior Selection Algorithms: An Overview." *Game AI Pro*, ch. 4. http://www.gameaipro.com/GameAIPro/GameAIPro_Chapter04_Behavior_Selection_Algorithms.pdf
- Orkin. "Three States and a Plan: The A.I. of F.E.A.R." GDC 2006. https://pages.cs.wisc.edu/~dyer/cs540/handouts/gdc2006_orkin_jeff_fear.pdf
- Epic Games. "Behavior Tree Node Reference: Decorators" (Observer Aborts). https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-behavior-tree-node-reference-decorators
- Brooks. "A robust layered control system for a mobile robot." IEEE J. Robotics & Automation 2(1):14–23, 1986. https://people.csail.mit.edu/brooks/papers/AIM-864.pdf
- Isla. "Handling Complexity in the Halo 2 AI." GDC 2005. https://www.gamedeveloper.com/programming/gdc-2005-proceeding-handling-complexity-in-the-i-halo-2-i-ai

Secondary (flagged in text):
- Hindriks, *Agent Programming in GOAL: Modules* (slides, via SlideServe). https://www.slideserve.com/levana/agent-programming-in-goal-modules
- Huang, Alexander. "Semantic Mutation Testing for Multi-Agent Systems." EMAS 2015. https://www-users.york.ac.uk/~rda2/paper%20-%20final%20post-proc%20version%207.pdf
- Wikipedia, "GOAL agent programming language"; "Subsumption architecture".
- Broersen et al., BOID: https://dspace.library.uu.nl/handle/1874/19919 and summaries.
- Halo 2 lecture slides (Univ. Michigan EECS 494, 2006). https://web.eecs.umich.edu/~sugih/courses/eecs494/fall06/lectures/lecture18-halo2.pdf
