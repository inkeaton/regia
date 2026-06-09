
# RegiaScript and RegiaEditor

## Abstract Concepts and their Mappings

### Stories
Stories are concurrent, behaviour changing contexts. In a game, they would map to a quest, or a scenario, a situation which begins and ends, and changes the behaviour of agents during it. Multiple stories can be happening at one time, and a subset of agents partecipate in them. Some stories could override the deafult behaviour of the agent or the one described by another story. For this reason, stories possess priority values, which are used to determine which story's override has precedence. Stories can be divided in multiple Phases, which we'll discuss later.

In the Visual editor, which we will call from now on RegiaEditor, each file, each graph should represent a Story. In abstract, the designer is designing the story itself. So, each file and graph should represent a story. The story should declare at the start its participants, its name and priority.

Similarly, in RegiaScript, each file should represent a single story, even though a file can contain more. They begin with a story block defined as ```STORY name PRIORITY 1.```

In AgentSpeak, stories are beliefs, written as ```story(name, 1).``` They are used as preconditions in the plans, as example ```+citizen_dies[source(percept)] : story(bring_item, 1) <- farewell.```. To activate a story in an agent, one only needs to add the belief to the agent, which makes the plan available. Plans are saved in the agent in order of priority. This method of priority resolution may be subject to change.

### Agents

Agents are the main actors of the Stories, and what we are ultimately trying to represent. The obvious roadblock we are trying to surpass is that game designers design stories focusing on the scenario, and not the agent themselves. 

In RegiaEditor, Agents are declared explicitly at actors of the story. we could define a special agent name for the player. Agents live through the phases and do Actions. How "global" actions are done and declared is still to be decided.

In RegiaScript, Actor blocks are contained inside of the stories as ```AGENT name:``` , and inside the behaviour is described for each Phase of the Stroy, and their reaction to each Event. They also conatain some default behaviour, in the ```DURING ALWAYS``` block

In AgentSpeak, each single file represents a single Agent

### Phases

Stories are divided in Phases, non-concurrent states of the current Story. They are unique to each story, each story can be in only one at the time. Right now, What determines the entering/exit from both stories and phases is still to be decided, it should not be the agents, but an external "director"

In RegiaEditor, it should correspond to a block of the graph. So, each phase is a state, with a event which causes to enter it and something that causes to exit it. Each phase contains plans, reactions to events for each agent.

In RegiaScript, Phase blocks ```DURING name:``` are contained insied of an Agent block, and conatin the reaction plans to events for the respective agent. The hierachy between agent block and phase block may be subject to change

In AgentSpeak, the current phase is a belief ```current_phase(story_name, phase_name). ``` The current phase is changed through an atomic transition plan. Plans of that phase are labeled with the belief.

### Plans / Reactions

Plans or reactions are the way in which an agent reacts to an event in a story during a specific phase. They are the smallest unit of logic of the system

In RegiaEditor, plans shoudl correspond to blocks, triggered by Events, whcih start only if Conditions are verified, and the plan corresponds in a series of actiosn done by an Agent.

In RegiaScript, a plan is a Plan block ```DURING item_requested: WHEN item_delivered ENVIRONMENT IF NOT is_tired MYSELF: DO reward_player.```

In AgentSpeak, a plan corresponds to a plan.

### Events

Events are things that happen in the world, which could come from the environment, another agent, the player, or the agent itself. They can trigger plans, reactions to the Event, or phase changes.

In RegiaEditor, events should be used to label phase changes, or start reactions/plans blocks. 

In RegiaScript, events must be declared beforehand in the story, e.g. ```EVENT item_delivered    ENVIRONMENT.```. They can later be used insied of phases to create Plans/Reaction blocks e.g. ```DURING item_requested: WHEN item_delivered ENVIRONMENT IF NOT is_tired MYSELF: DO reward_player.```. They are tagged with their origin.

In AgentSpeak, events nicely map to triggering events: ```+item_delivered[source(percept)] : story(bring_item, 1) & current_phase(bring_item, item_requested) & ~is_tired <- reward_player.```

### Conditions

Conditions are facts about the world, other agents, the current agent or the player. They can be used in plan/reactions to decide what to do

In RegiaEditor, they can be added/removed or changed, and similarly to the Events, they can be used to decide the phase transitions, or the start of a reaction/plan.

In RegiaScript, they are declared similarly to events,with an origin tag, and used in the IF block, with boolean logic available

In AgentSpeak, they nicely translate to beliefs.

### Actions

Actions are things that the individual agent can do. They should be thought as operators, functions which can be called and done by the Agent.

In RegiaEditor, the designer should be able to define new actions, with their necessary input, and use them inside of plans/reactions. The game designer should have the freedom to create whatever action they want, it must be later translated in actual code

In RegiaScript, actions are defined in the agent, and then used inside of the plans. sPECIAL TYPE OF CATIONS CORESPOND TO ADDING/REMOVING BELIEF. oTHER SPECIAL TYPES COULD BE ADDED IN TEH FUTURE

In AgentSpeak, they correspond to either internal actions or spcific behaviour, like communicating or adding/removing beliefs

## Executable is built with Nuitka