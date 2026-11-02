Regia is meant to be highly readable and accessible to non-programmers. This is realised through two design choices:
+ **As few symbols as possible**: what may be a symbol in a language, is swapped for a specific keyword. For example, in ASL declaring a belief is a simple case of stating it (`person(George).`). Here, we may use a capitalised keyword to indicate it (`FACT person(George)`). While this increases verbosity, make it clear what we are writing to even inexperienced readers.
+ **Use less specialised lingo**: As seen above, we are not directly using BDI terms for the language's concepts. Beliefs for example are called facts. The names are decided together with our audience, and as such we may always consider what is the best name for a concept
+ **Modularity**: the language is meant to be modular and extensible. By that we mean that when designing a construct, we must consider how this can be isolated and written in isolation from others. This comes from two requirements. First, working on a concept in isolation means having less to think on your mind, easing reasoning and development. Moreover, such modularity highly enables reuse, allowing to build programs by putting together smaller building blocks already implemented
All these concepts must be considered when designing the language syntax and constructs
---
Being more practical, here's an example of a 1.0 Regia program:
```regia
# Vocabulary Declarations

# Actions used by Playbooks
ACTION toast(target).
ACTION eat_food.
ACTION complain.

# Actions used by the Director (WORLD DO and Role DO)
ACTION engine.security.summon_guards AS call_guards.
ACTION lock_doors.
ACTION play_music.
ACTION serve_wine.
ACTION stop_music.

# Events triggering Playbook and Plot WHEN blocks
EVENT food_served.
EVENT insult_heard.
EVENT digestion_check.
EVENT assassin_spotted.
EVENT insult_thrown.
EVENT duel_resolved.

# Facts used in Playbook IF conditions
FACT is_hungry.
FACT is_drunk.
FACT hates(person).

# Playbooks

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

# Plots

#@desc: A dummy subplot to satisfy the START SUBPLOT requirement.
PLOT HonorDuel.

    PHASE combat INITIAL.

    ROLE Challenger.

    DURING combat:
        WHEN duel_resolved:
            WORLD DO PRINT("The duel is over.").
            END PLOT.

#@desc: The main narrative flow of the Royal Banquet.
PLOT RoyalBanquet.

    PHASE reception INITIAL.
    PHASE feast.
    PHASE duel_interruption.

    ROLE Host.
    ROLE Guest.

    DURING PLOT:
        WHEN assassin_spotted PRIORITY 9:
            WORLD DO lock_doors.
            Host DO call_guards.
            END PLOT.

    DURING reception:
        ON ENTER:
            WORLD DO play_music.
            ASSIGN NobleSocializing TO Guest.
            
        WHEN food_served:
            TRANSITION TO feast.

    DURING feast:
        ON ENTER:
            WORLD DO serve_wine.
            
        WHEN ROLE Guest SIGNALS insult_thrown:
            WORLD DO stop_music.
            START SUBPLOT HonorDuel MAPPING Guest TO Challenger.
            TRANSITION TO duel_interruption.
            
        ON EXIT:
            UNASSIGN NobleSocializing FROM Guest.

    DURING duel_interruption:
        WHEN SUBPLOT HonorDuel ENDS:
            WORLD DO PRINT("The duel is settled. The banquet is ruined.").
            END PLOT.
```

This describes a banquet, as a set of Plots and Playbooks. The meaning of these concepts is deferred to later, right now we focus on the syntax and structure of the language.

We can see that statements ends with `.`. blocks start with `:`. While present in the file, tabulation has no meaning. comments begin with `#`. We also have documentation comments, which start with `#@`. Multi-line comments continue with `#-`. All other elements of the language are written through capitalised keywords. 

#changes in 2.0, we will both make the language simpler, and add more features. First, we will make tabulation mandatory. By default, we will use tabulation and new lines to determine statements end and blocks opening and closing. An example based on the previous snippet is the following:

```regia
PLAYBOOK NobleSocializing:

    WHEN insult_heard PRIORITY 5 TEMPER sympathy(-0.5) EFFECTS aggressiveness(0.2):
        IF NOT is_drunk AND hates(host):
            DO complain
            SIGNAL insult_thrown
        ELSE:
            DO toast(host)

    WHEN digestion_check:
        IF is_hungry:
            DO eat_food
            DO FORGET(is_hungry)
            DO PRINT("A guest finishes their meal.")

    WHEN food_served:
        DO PRINT("A guest notices food arriving.")
        IF (is_hungry OR is_drunk) AND NOT hates(host):
            DO eat_food
        ELSE:
            DO complain
```
This removes the need for `.`, simplifying the syntax. We keep the `:` to signify the beginning of a block, given it's simplicity of meaning. Still, one may want to disregard the tabulation, for aesthetic reasons. As such, we may also support the `.` to write an explicit statement end, and the `;` for a block end. This would allow to write the previous code as follows:
```regia
PLAYBOOK NobleSocializing:

    WHEN insult_heard PRIORITY 5 TEMPER sympathy(-0.5) EFFECTS aggressiveness(0.2):
        IF NOT is_drunk AND hates(host): DO complain. SIGNAL insult_thrown;
        ELSE: DO toast(host);

    WHEN digestion_check:
        IF is_hungry: DO eat_food. DO FORGET(is_hungry). DO PRINT("A guest finishes their meal.");

    WHEN food_served:
        DO PRINT("A guest notices food arriving.")
        IF (is_hungry OR is_drunk) AND NOT hates(host): DO eat_food;
        ELSE: DO complain;
```
Or:
```regia
PLAYBOOK NobleSocializing: WHEN insult_heard PRIORITY 5 TEMPER sympathy(-0.5) EFFECTS aggressiveness(0.2): IF NOT is_drunk AND hates(host): DO complain.SIGNAL insult_thrown; ELSE: DO toast(host); WHEN digestion_check: IF is_hungry: DO eat_food. DO FORGET(is_hungry). DO PRINT("A guest finishes their meal."); WHEN food_served: DO PRINT("A guest notices food arriving."). IF (is_hungry OR is_drunk) AND NOT hates(host): DO eat_food; ELSE: DO complain;;
```
Basically a `.` translates to a line break, a `:` to an inner tabulation, a `;` to an outer tabulation. #discuss we may specify some particular cases (like not needing a `;` between an IF and ELSE), but it depends on the implementation #discuss we may wanna swap the roles of `.` and `;` to bring it closer to general purpose languages.

For multi definitions, a new feature to be implemented in 2.0, we may use the `,` to separate elements:

```regia
 DO eat_food, FORGET(is_hungry), PRINT("A guest finishes their meal.")
```
#discuss we may consider to remove the need of tabulation when using a `,`, by thate we mean that one may write the various elemnts on one line or more 

---

All comments start with` #`. #changes we may change how multiline comments work. Previously one neede to add a `#-` after one comment to make it multi line. Now, we may strat a comment with a double `#` to mean it to be multiline. It must be closed with a `##`. This should work regardless of comment type

```regia
 ## This comment
 is multiline
 i can write a lot
 ##
 
 DO PRINT("This is code")
 
 ##@desc: This should work
 for doc comments too ##
```

#changes We may also introduce a new type of comments, compilation comments. They will be discussed in another file, but in general they contain information for agent instancing after transpilation, depending on the target language. they may start with `#%`. #discuss we may thing of other symbols to use