Regia tries to model autonomous agents, following the BDI model, while being conscious of the overall coordination and environment in which the agents live. As such, it does not directly model individual agents, but so called **Roles**, classes of agents.  At runtime, we may instantiate as many agents as we like, whose behaviour is described by a Role definition. The role's behaviour is described through two elements, which separate the local and global behaviour of the agent:
+ **Playbooks** are collections of plans, reactions to events and recipes for goals. They can be assigned or unassigned to an agent instance, changing their available plans, and as such their behaviour. Multiple Playbooks can be assigned to a single agent instance. Where two plans may conflict, it must decided which must fire, or both, though a priority system
+ **Plots** are narrative state machines, which describe how a scenarios flows, through the actors, the roles, which live it. The plot describes the roles between each phase, and through the point of view of an infrastructural Director agent, each role is assigned or unassigned playbooks, can be requested to do a specific action, and can be mapped into other plots. An agent instance can be part of multiple plots, and as such be part of multiple Roles at the same time.
The idea is that Playbooks represent a local, static behaviour of an agent, regardless of context. The Plot contains the global knowledge of what is going on, and as such decides when a Role should do something, or switch behaviour. As Directors manage the roles,  agent instances can communicate to the Plot directors, to signal specific events or requests.

Inside these high level constructs, lower level vocabulary items are used. These must be defined before use:
+ **Facts** correspond to BDI Beliefs, and represent things which an agent may know about the state of the world. They may be used by both agents and directors to choose plans and reason
+ **Events** represent things that happen in the world. When these happen, it should trigger a reaction in the agent 
+ **Actions** represent actions which the agent can do in the world. Besides basic actions, already implemented, the user can define as many as they like outside of the language, and must only specify the interface in regia to use them inside it 
#changes We may what to add another element to these, and these are **Goals**. Taking directly from the BDI model, goals function similarly to facts, but instead of knowledge, they represent an objective which the agent intends to pursue. They do not come from the world itself, they are decided by the agent itself, or they may be assigned by the director agent
---
Such architecture should provide ample separation of concerns and modularity. The usage of Roles completely separates the design process form the actual instantiation. Playbooks get defined on their own, and can be reused by multiple Plots. Plots, while higher level, still describe only their own scenario, regardless of other plots which are active simultaneously. The priority system should allow multiple plots and playbooks to be active at once, without each crossing each other wires. This allows for both reuse and reduced mental strain. 
#discuss Sadly, the priority system is not currently implemented nor enforced. We must reason on both its design and usability and its implementation. We may consider relative priority, and hierarchical ones.

---

The language supports splitting files through imports:

```regia
IMPORT "./output/shared_elements.regia".

#@author: AgentSpeak Designer
#@version: 0.2
#@desc: Playbook demonstrating basic actions triggered by an imported event.
PLAYBOOK HeroPlaybook:
    WHEN quest_completed PRIORITY 5:
        DO celebrate(achievement_name).

#@author: AgentSpeak Director
#@desc: Main plot demonstrating inline phase transitions.
PLOT EpicAdventure.
    ROLE Hero.
    PHASE beginning INITIAL.
    PHASE middle.
    PHASE ending.

    DURING beginning:
        # Testing standard declarative transitions for baseline comparison
        WHEN quest_completed:
            TRANSITION TO middle.
        
        # Testing inline transitions embedded inside a Plot WHEN block
        WHEN quest_completed PRIORITY 10:
            IF NOT has_achievement(hero_medal):
                WORLD DO BROADCAST("Giving hero a medal!").
                TRANSITION TO middle.
            ELSE:
                WORLD DO BROADCAST("Hero already has the medal.").
                TRANSITION TO ending.

    DURING middle:
        ON ENTER:
            ASSIGN HeroPlaybook TO Hero.
        
        # Inline transition testing with bare prefix action
        WHEN quest_completed:
            WORLD DO BROADCAST("Quest completed again!").
            TRANSITION TO ending.

    DURING ending:
        ON ENTER:
            UNASSIGN HeroPlaybook FROM Hero.
```

This further allows modularity. imports must stay at the top of the file, in its header, as the first thing. They should allow for diamond dependencies, and obviously stop circular ones.