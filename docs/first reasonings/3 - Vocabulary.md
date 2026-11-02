The vocabulary, made of facts, events, actions and goals, contains the building blocks of the higher level constructs. These must be defined at the top of the file, after imports. #discuss we may also consider local vocabulary, defined inside of a playbook or plot. 

Facts are defined as follows:
```regia
FACT is_hungry
FACT is_drunk
FACT hates(person)
```
They support bounded parameters. #discuss we may want to reason on how could we support unbounded parameters, or variables as a whole

#changes Goals would be implemented very similarly to facts.

Actions are defined as follows
```regia
ACTION toast(target)
ACTION engine.security.summon_guards AS call_guards
ACTION lock_doors
```
They too support parameters. #discuss we may want to see if it makes sense to specify types. Aliases are supported, used to use simpler names instead of more complex ones inside of the file

Events are defined as follows:
```
EVENT food_served
EVENT insult_heard
EVENT digestion_check
EVENT assassin_spotted
EVENT insult_thrown
EVENT duel_resolved
```
#changes they currently do not support parameters, they need to be added. #discuss also, with the addition of goals, we must distinguish different types of events (fact addition/deletion, goal addition/deletion). We must reason on how to specify these, in the most comprehensible way

#changes all vocabulary definitions should allow for multi-definition, writing multiple declarations/definitions on one line (e.g `FACT a, b, c`)
#changes We may add a new feature, `GROUP` which allows to create group of elements. For example `FACT GROUP a, b, c` declares three facts, and says they belong to a single group. This could later be used for choosing from a set of options. See if this is too similar to multi-defs and if we may choose a slightly different wording to make it different