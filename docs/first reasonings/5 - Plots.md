Plots are narrative state machines. Practically, they describe the behaviour of an infrastructural director agent, whose role is to manage all the other agents during the different phases of the Plot. The director can communicate with the agents, assign them playbooks or removing them, reacting to signals sent by them.

All roles and phases present in the Plot must be declared at the start. On phase must be marked as initial, the one that the plot starts in. #changes we may add some sort of role instantiation, maybe a set of facts and playbooks that the role starts with #changes as any block, the PLOT block should start with the `:`
```regia
PLOT RoyalBanquet.
	PHASE reception INITIAL.
	PHASE feast.
	PHASE duel_interruption.
	
	ROLE Host.
	ROLE Guest.
```
Then, each Phase is described on its own, as a `DURING` block. This contains plans which are active during this phase. There are also two types of plans, `ON ENTER` and `ON EXIT` which are triggered when entering and exiting the phase, respectively. 

```regia
DURING reception:
	ON ENTER:
		WORLD DO play_music.
		ASSIGN NobleSocializing TO Guest.
		
	WHEN food_served:
		TRANSITION TO feast.
```

Also, a special phase called `PLOT` always exists, and contains plans which must always be active, regardless of phase.

```regia
DURING PLOT:
	WHEN assassin_spotted PRIORITY 9:
		WORLD DO lock_doors.
		Host DO call_guards.
		END PLOT.
```

Inside of the plans, the director can do actions, just like roles in playbooks, by prefacing them with `WORLD`. #discuss we may change this keyword. They can also ask a Role to do something, by prefacing the Role name before the action. Moreover, there a set of actions unique to the director:
+ `ASSIGN ... TO ...` assigns a Playbook to a Role. `UNASSIGN ... FROM ...` does the opposite
+ `TRANSITION TO ...` transitions the plot to another phase. Should be the last statement in its branch
+ `START SUBPLOT ... MAPPING .. TO ...` starts another plot as a children of this one.
+ `END PLOT` ends the plot. Should be the last statement in its branch. It should alert parent and children plots.

Plots should remain in communication between children and mother. In particular, parents should be able to react to children ending, as follows:

```regia
DURING duel_interruption:
        WHEN SUBPLOT HonorDuel ENDS:
            WORLD DO PRINT("The duel is settled. The banquet is ruined.").
            END PLOT.
```

#discuss let's reason on how should they cooperate

#changes as roles are mapped into subplots, we may need to add role mapping into playbooks.

#discuss the director agent should not have goals or similar, its plans are simpler and should describe only changes in the plot. let's reason if it still makes sense to improve it, what would we gain 