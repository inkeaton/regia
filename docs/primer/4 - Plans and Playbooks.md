Plans are on the second level of abstraction. They represent a reaction to an event, or a recipe to reach a goal. Playbooks are simply sets of these plans, brought together by the need to activate and deactivate them together. They directly correspond to plans in the BDI model. Plans also exist inside of Plots, but we will discuss their specific features there.

They are composed of three elements. A triggering event, a context and a body. The last element is simply a list of statements, the steps to complete the procedure. Here's an example from 1.0: 

```regia
WHEN fan_greets:
	IF happy:
		DO greet_back.
```

`WHEN` contains the trigger, `IF` the context, and later we have the statements which make up the plan. In 1.0, plans with shared context may be grouped under a single block, as follows:

```regia
WHEN fan_greets:
	IF happy:
		DO greet_back.
	IF angry:
		DO curse.
	ELSE:
		DO ignore.
```

While being called `IF`, these behave more closely to `ELSE IF`, being exclusive. #changes we may want to separate the IFs and the context, through a different keyword. We may use the word `GIVEN` to indicate the context, and let IFs work as they do in general purpose languages, even if this is different from the BDI model.

A context is a logic expression made up of facts. the order follows Prolog's one, from its BDI roots. 

```regia
WHEN food_served:
	DO PRINT("A guest notices food arriving.").
	IF (is_hungry OR is_drunk) AND NOT hates(host):
		DO eat_food.
	ELSE:
		DO complain.
```

In the trigger section, we also specify optional flags. We have two closely related to the AgentSpeak translation of the language, in particular the Temper model provided by VEsNA-Pro, the framework used to connect ASL agents to a game engine. TEMPER specifies the mood traits which an agent should be close to to choose this plan, while EFFECTS specifies how this mood changes. The PRIORITY label instead is an unimplemented feature to solve conflicts between plans, already mentioned. #changes we may change the syntax, using the `,` to add the additional labels (e.g. `WHEN insult_heard, PRIORITY 5, TEMPER sympathy(-0.5), EFFECTS aggressiveness(0.2):`) #discuss based on how we will implement PRIORITY, such an annotation may be applied also to other constructs #changes we may change the names of TEMPER and EFFECTS, maybe something closer to propensities, as they are called in VEsNA-Pro.
 
#changes regarding the trigger section, given the addition of goals, we may want to specify the type of triggering event. #discuss We may specify it by adding a word after the event name(e.g. WHEN food_served KNOWN/FORGOT/PURSUED/DISCARDED/ABANDONED)

#changes since we are adding parameters to events, we must reason on how these, for now bounded, can be used inside of the plan.

Statements are actions. These can be custom actions, or basic ones, already implemented. These are:
+ `PRINT()`: prints to terminal
+ `BELIEVE()`: adds a fact to the agent
+ `FORGET()`: forgets a fact
+ `ACHIEVE()`: adds a goal
+ `WAIT()`: wait some time
+ `BROADCAST()`: Send a message to all other agent instances
+ `TELL()`: send a message to a specific instance/role
+ `SIGNAL()`: Send a message to the Director agent which assigned this playbook
These are the ones which can be used inside of a playbook definition. Before using them , one should use `DO` #changes we may remove the need of DO for basic actions (SIGNAL already does not need it) and only keep it for custom ones. #changes we may add an action to remove a goal. Also, we may change the word from achieve to pursue, and the removal one may be something similar to discard

Playbooks group plans simply by inserting them in their block
```regia
#@desc: Reactive behaviour for guests mingling and eating at the banquet.
PLAYBOOK NobleSocializing:

	WHEN insult_heard PRIORITY 5 TEMPER sympathy(-0.5) EFFECTS aggressiveness(0.2):
		IF NOT is_drunk AND hates(host):
			DO complain.
			SIGNAL insult_thrown.
		ELSE:
			DO toast(host).
	
	WHEN digestion_check:
		IF is_hungry:
			DO eat_food.
			DO FORGET(is_hungry).
			DO PRINT("A guest finishes their meal.").
	
	WHEN food_served:
		DO PRINT("A guest notices food arriving.").
		IF (is_hungry OR is_drunk) AND NOT hates(host):
			DO eat_food.
		ELSE:
			DO complain.
```

#changes we may want to add other roles inside of playbooks. this allows playbooks to describe communication with other agents without needing to know the instances' names