# Goals and Trigger kinds

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo
Blocked by: 03

## Question

How do Goals work, and which kinds of Trigger exist (primer ch.2–4)? Adding Goals means a Trigger can be a Fact being added or removed, a Goal being pursued, dropped or failed, a world Event, or a Signal. Decide the list of Trigger kinds and how a designer writes each one (e.g. `WHEN food_served KNOWN/FORGOT/PURSUED/DISCARDED`). Also decide how Goals are declared, who can give an Agent a Goal (the Agent itself, or the Director), and whether world Events and Fact changes are the same thing for a designer.

## Answer

Spec chapter: `docs/spec/05-goals-and-triggers.md`. ADR: `docs/adr/0003-events-are-momentary-fact-changes-are-trigger-kinds.md`. Glossary: Event, Signal, Goal, Trigger, Plan revised; Trigger kind and Sender added.

- **Goals** are achievement Goals only, declared like Facts (`GOAL avenge(person)`). One name belongs to one Vocabulary kind. A Goal can come from the Agent itself, the Director or another Agent. It is reached when a Plan for it finishes; no "reached" Trigger. A duplicate request with the same arguments is ignored. A Body can wait for a Goal or start it and carry on (syntax and default: *Basic action set*). A Context can test `PURSUING g`.
- **Events are momentary**: never tested in a Context, believed or forgotten. Fact changes and Goals are Trigger kinds too; there is no umbrella noun besides "Trigger kind". `EVENT` keeps its keyword; renaming it `CUE` is deferred.
- **Trigger kinds**: `WHEN e(?x):` (Event, including a Signal at a Director), `WHEN f(?x) LEARNED:` / `FORGOTTEN:`, `TO g:` (recipe), `WHEN g DROPPED:`. Goal failure is reserved for *Plan failure*. Fact Triggers always need the kind word, written after the item. `WHEN` is the only reaction keyword: `ON ENTER` / `ON EXIT` become `WHEN` Triggers.
- **`FROM`** on anything sent: `FROM Role`, `FROM ?who`, `FROM Role ?who`, `FROM DIRECTOR` (any Director whose Plot currently gives this Playbook, resolved at runtime). An error on Triggers with no sender; self-given Goals have no sender.
- **Order**: `WHEN`/`TO`, item, kind word, `FROM`, Labels.
