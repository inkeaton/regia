### First Language Version

The language is thought up for game designers. As such, it will follow their design pipeline, describing agents as they act during a story, a named, prioritized, concurrently activable context. Given that the users may not be familiar with coding, the syntax will be as simple as possible.

An example of the language.

STORY a PRIORITY 1.
ACTION run.
ACTION dance.
EVENT b.
EVENT c.

DURING a:
    WHEN b IF d AND NOT e:
        DO run,
        DO dance.
    WHEN c:
        DO dance.

The main concepts used in the language are the following:

* Stories: named, prioritized, concurrently activable context, they are used to change the beahviour of the agent based on events of the world (example, during a quest). Multiple can be active at the same time, and they possess a priority value to decide which story's plan should be chosen in the case of plans with the same name. They should be implemented as beliefs story(name, priority) which are used to tag plans. plans can be defined which do not belong to a story and as such are always active
* Events: precepts or goals that arrives from the environment and triggers plan selection. They will be translated as trigger events of plans in AgentSpeak
* Actions: they are the available actions of the agents, which could be internal actions or goals
* Conditions: They are the condition verified in the body of the plans
We should also add actions to start/end stories and add/remove beliefs for the conditions. Still, we must remain at an high level of abstraction, so we must understand what it should mean to do these last two actions. We must also reason on what should be defined before describing the plans, even if we should do it