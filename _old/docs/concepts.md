This file presents the **abstract concepts** used inside of the Regia project, their meaning and how they are planned to be used in the **Visual Editor** (RegiaEditor/BIRDBRAIN), in the **Domain Specific Language** (RegiaScript/Regia) and their translation in **AgentSpeak**. Some concepts my be still vague or not decided, and in that case, they will be indicated as such
# Main Elements
## Stories
---
### Concept
Stories are **concurrent, behaviour changing contexts**. In a game, they would map to a **quest**, or a scenario, a situation which begins and ends, and changes the behaviour of agents during it. A **Default story** can be implemented for each agent, containing its default behaviour

Multiple stories can be happening at one time, and a subset of agents participate in them. Some stories could override the default behaviour of the agent or the one described by another story. For this reason, stories possess **priority** values, which are used to determine which story's override has precedence. It should also be possible to specify actions of different name that cannot happen at the same time. How this should be implemented is yet to be decided.

Stories can be divided in multiple **Phases**, which we'll discuss more later. Some behaviours may also be **phase-independent** within the story, always active regardless of phase.

The start and end of Stories is not decided by the agents themselves, but by an external party, a **Director** of sort. How that is implemented is still under work.
### Visual Editor
When working in the editor, the objective of the designer is to design a story. So, each file on which one is working in the editor is a Story. A Story will be represented as a flowchart, composed of blocks of Phases, connected by Transitions. In each of the phases, the Agents' behavior during them is described. Phase-independent behaviours should also be represented, it still must be decided how. The Story name, priority and agents that inhabit it should be specified
### Domain Specific Language
Similarly, in RegiaScript, each file should represent a single story, even though a file can contain more. The top level blocks of the language are story blocks and components definitions, which we'll discuss later.  The following is an example of a story block:
```regia
# name of the story, priority
STORY bring_me_item PRIORITY 1.
	
	# phases definitions
	PHASE asking INITIAL. # starting phase
	PHASE searching.
	PHASE delivered.
	PHASE failed.
	
	# agent definitions
	AGENT Player.
	AGENT Citizen. 
	
	DURING STORY:
		# phase-independant block contents...
		
	DURING asking:
		# phase block contents...
		
	# all other phase definitions
```
### AgentSpeak
In AgentSpeak, stories are translated into beliefs, written as ```story(name, priority).``` They are then used as conditions in the plans, as example: 
```AgentSpeak
+citizen_dies[source(percept)] 
	: story(bring_item, 1) <- 
		farewell.
``` 
To activate a story in an agent, one only needs to add the belief to the agent, which makes the plan available. All plans obtained from the RegiaScript story are labeled with this condition Plans are saved in the agent in order of priority. This method of priority resolution may be subject to change.
## Phases
---
### Concept
Stories are divided in Phases, **non-concurrent states of the current Story**. They are unique to each story, each story can be in only one at the time. 

One should be able to specify Global or Agent Actions that happen at the **entering** or **exiting** of the Phase. How this should be implemented is yet to be decided.

The transition between Phases is not decided by the agents themselves, but by an external party, a **Director** of sort. How that is implemented is still under work. Anyways, the transition is triggered by an Event, and can be controlled with Conditions.
### Visual Editor
A phase should correspond to a block of the flowchart. So, each phase is a state, with a event which causes to enter it and something that causes to exit it. Each phase contains Plans/Reactions to events for each agent. Each phase may specify entering and exiting Actions.
### Domain Specific Language
In RegiaScript, Phase blocks ```DURING name:``` are contained inside of an Story block, and contain agent blocks, with the Reaction in that state for each Agent. 
```regia
# inside story block

# phase-independant behaviours
DURING STORY:

	AGENT Citizen:
		# agent block contents...
	
	AGENT Player:
		# agent block contents...

# phase block
DURING asking:

	# transitions from this phase
	TRANSITION TO searching WHEN player_accepts IF citizen_is_known.
	TRANSITION TO failed WHEN player_rejects.
	TRANSITION TO failed WHEN citizen_dies.
	TRANSITION TO failed WHEN citizen_missing.
	
	# entering phase actions
	# SYNTAX SUBJECT TO CHANGE
	ON ENTER:
		GLOBAL DO improve_morale.
		Player DO thinking.
		
	# exiting phase actions
	# SYNTAX SUBJECT TO CHANGE
	ON EXIT:
		GLOBAL DO decrease_morale.
		Player DO thinking.
	
	# agent blocks
	AGENT Citizen:
		# agent block contents...
	
	AGENT Player:
		# agent block contents...
```
### AgentSpeak
In AgentSpeak, the current phase is a belief ```current_phase(story_name, phase_name). ``` The current phase is changed through an atomic transition plan inside of the agents. Plans of that phase are labeled with the belief.
```
@atomic
+!enter_phase(Story, Phase)
<- -current_phase(Story, _); +current_phase(Story, Phase).

+player_accepts[source(player)] : story(bring_me_item, 1) & current_phase(bring_me_item, asking) & citizen_is_known <- acknowledge.
```
The phase transitions is triggered by an external agent, called Director. This may be subject to change
```
// inside director
player_accepts[source(player)] : story(bring_me_item, 1) & current_phase(bring_me_item, asking) & citizen_is_known <- 
	!enter_phase(bring_me_item, searching);
	.send(citizen, achieve, enter_phase(bring_me_item, searching));
	.send(player, achieve, enter_phase(bring_me_item, searching)).
```

## Agents
---
### Concept
Agents are the main actors of the Stories, and what we are ultimately trying to represent. The obvious roadblock we are trying to surpass is that game designers design stories focusing on the scenario, and not the agent themselves. Agents possess names. They are in Stories and Phases, which alter their behaviour. They react to Events through Plans/Reactions, doing Actions. 

We could define a special agent type for the Player, since its interaction may be modeled in a Story, but it should not be compiled into an agent.
### Visual Editor
In RegiaEditor, Agents are declared explicitly at actors of the story. Agents may be defined globally in a project, and used in multiple Stories. Agents live through the Phases and do Actions.
### Domain Specific Language
In RegiaScript, Actors are first defined at the Story level. Actor blocks are contained inside of phase blocks, and contain Reaction blocks.
```
# inside phase blocks
AGENT Citizen:
	# reaction block
	WHEN player_accepts IF citizen_is_known:
		DO acknowledge.
	
	WHEN player_rejects:
		DO find_someone_else.
	
	WHEN citizen_dies:
		DO express_disappointment.
	
	WHEN citizen_missing:
		DO express_disappointment.

AGENT Player:
	WHEN player_accepts IF NOT is_busy:
		DO acknowledge.
	
	WHEN player_rejects:
		DO explore.
	
	WHEN citizen_dies:
		DO note_citizen_gone.
	
	WHEN citizen_missing:
		DO note_citizen_gone.
```
### AgentSpeak
In AgentSpeak, each single file represents a single Agent. It contains the story and phase beliefs, infrastructure plans, and the reactions plans.
```AgentSpeak
// Generated by RegiaScript compiler
// Source : bring_me_item.rgs
// Agent : Citizen
// Date : 2026-06-10 11:35:25

// == Initial beliefs ========================================

current_phase(bring_me_item, asking).

// == Infrastructure plans ===================================

@atomic
+!enter_phase(Story, Phase)
<- -current_phase(Story, _); +current_phase(Story, Phase).

@atomic
+!activate_story(Name, Priority)
<- +story(Name, Priority).

@atomic
+!deactivate_story(Name)
<- -story(Name, _).

// == Plans =================================================

+player_accepts[source(player)] : story(bring_me_item, 1) & current_phase(bring_me_item, asking) & citizen_is_known <- acknowledge.

+player_rejects[source(player)] : story(bring_me_item, 1) & current_phase(bring_me_item, asking) <- find_someone_else.

+citizen_dies[source(percept)] : story(bring_me_item, 1) & current_phase(bring_me_item, asking) <- express_disappointment.

+citizen_missing[source(percept)] : story(bring_me_item, 1) & current_phase(bring_me_item, asking) <- express_disappointment.

+item_delivered[source(percept)] : story(bring_me_item, 1) & current_phase(bring_me_item, searching) & player_has_item <- thank_player.

+item_delivered[source(percept)] : story(bring_me_item, 1) & current_phase(bring_me_item, searching) & ~player_has_item <- express_disappointment.

+quest_timed_out[source(timer)] : story(bring_me_item, 1) & current_phase(bring_me_item, searching) <- express_disappointment.

+citizen_dies[source(percept)] : story(bring_me_item, 1) & current_phase(bring_me_item, searching) <- express_disappointment.

+daily_routine : story(bring_me_item, 1) & current_phase(bring_me_item, delivered) <- thank_player.

+daily_routine : story(bring_me_item, 1) & current_phase(bring_me_item, failed) <- express_disappointment.

+citizen_dies[source(percept)] : story(bring_me_item, 1) <- express_disappointment.

+citizen_missing[source(percept)] : story(bring_me_item, 1) <- express_disappointment.

+daily_routine : true <- go_about_day.
```


## Plans / Reactions
---
### Concept
Plans or Reactions are the way in which an agent reacts to an Event in a Story during a specific Phase. These are the central blocks of the system, defining the behaviour of the agents, and the one most easily similar to AgentSpeak's Logic.
### Visual Editor
In RegiaEditor, plans should correspond to blocks, triggered by Events, which start only if Conditions are verified, and the plan corresponds in a series of actions done by an Agent. They are part of Phases
### Domain Specific Language
In RegiaScript, a plan is a Plan block, which describes the reaction to an Event, given some Conditions to be true, as a series of Actions that the Agent takes.
``` regia
# inside Agent block
WHEN player_accepts IF NOT is_busy: # on event player_accepts, if NOT is_busy is true
		DO acknowledge. # do the acknowledge action
```
Plans' WHEN blocks may contain multiple IF blocks, in order to more quickly write multiple plans. This is still to be decided
### AgentSpeak
In AgentSpeak, Plans get easily translated into plans.
```AgentSpeak
+player_accepts[source(player)] : story(bring_me_item, 1) & current_phase(bring_me_item, asking) & ~is_busy <- acknowledge.
```
# Building blocks
## Events
---
### Concept
Events are things that happen in the world, which could come from the environment, another agent, the player, the director, or the agent itself. They can trigger plans, reactions to the Event, or phase changes.
### Visual Editor
In RegiaEditor, events should be used to label phase changes, or start reactions/plans blocks. 
### Domain Specific Language
In RegiaScript, events must be declared beforehand in the story block, together with an type tag, which could be of various types. The tags are not yet then exploited in the language.
```
# inside story block
EVENT player_accepts PLAYER.
EVENT player_rejects PLAYER.
EVENT item_delivered ENVIRONMENT.
EVENT citizen_dies ENVIRONMENT.
EVENT citizen_missing DIRECTOR.
EVENT daily_routine MYSELF.
EVENT bored MYSELF.
EVENT quest_timed_out TIMER.
```

They can later be used inside of WHEN blocks to create Plans/Reaction blocks. Here the type tag is not repeated.
```regia
# reaction to daily_routine event
WHEN daily_routine:
	DO go_about_day.
```
### AgentSpeak
In AgentSpeak, events nicely map to triggering events: 
```AgentSpeak
+daily_routine : true <- go_about_day.
```
## Conditions / Beliefs
---
### Concept
Conditions are facts about the world, other agents, the current agent or the player. They can be used in plan/reactions to decide what to do. These facts can be believed, forgotten, shared between Agents. We could create a set of global conditions, shared between everybody, but this is still to be worked on.
### Visual Editor
In RegiaEditor, they can be added/removed or changed, and similarly to the Events, they can be used to decide the phase transitions, or the start of a reaction/plan.
### Domain Specific Language
In RegiaScript, they are declared similarly to events, with a type tag. 
```regia
CONDITION player_has_item ENVIRONMENT.
CONDITION citizen_is_known MYSELF.
CONDITION is_busy MYSELF.
```
They are used inside of the IF blocks, with boolean logic available.
```
WHEN player_accepts IF citizen_is_known:
	DO acknowledge.
```
### AgentSpeak
In AgentSpeak, they nicely translate to beliefs.
```AgentSpeak
+player_accepts[source(player)] : story(bring_me_item, 1) & current_phase(bring_me_item, asking) & citizen_is_known <- acknowledge.
```
## Actions
---
### Concept
Actions are things that an individual Agent can do, or Global changes to the environment, not done by a single Agent. They should be thought as operators, functions which may take an input, may give an output, and can have an Agent has an actuator, or be global. Global actions are yet to be implemented. Special type of actions can be implemented for AgentSpeak specific actions, as tell, believe, forget.
### Visual Editor
In RegiaEditor, the designer should be able to define new actions, with their necessary input, and use them inside of plans/reactions. The game designer should have the freedom to create whatever action they want, it must be later translated in actual code. The way in which actions are then mapped to actual code must be decided.
### Domain Specific Language
In RegiaScript, actions are defined in the Story block as something that can be done. An action may be tagged as Global if it has not an agent that does it.
```regia
# inside story block
ACTION thank_player.
ACTION find_someone_else.
ACTION express_disappointment.
ACTION acknowledge.
ACTION note_citizen_gone.
ACTION explore.
ACTION go_about_day.
```
Actions and also other building blocks may be defined outside of a story, in order to be reused, building a library of building blocks, together with agents, which may be decided in advance with the programmers, for implementation. This is still to be decided
### AgentSpeak
In AgentSpeak, they correspond to either internal actions or specific behaviour, like communicating or adding/removing beliefs. 
