# Parameters and variables

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How do parameters and variables work across the Vocabulary and Plans (primer ch.3, ch.4)? Facts and Actions take bound parameters today, and Events take none. Decide: do Events get parameters? Are unbound parameters (variables) supported, and how are they written so a non-programmer can read them? How does a Plan use the parameters of the Event that triggered it? Are parameters typed, and if so, which types exist?

## Answer

Spec chapter: `docs/spec/03-parameters-and-placeholders.md`. ADR: `docs/adr/0001-placeholders-are-filled-by-matching.md`. Glossary entries added: Parameter name, Value, Placeholder.

- **Events take parameters.** Every kind of Vocabulary item (Fact, Event, Action, Goal) declares them as `name(param, …)`. Signals reuse their Event's declaration.
- **Untyped.** The Transpiler checks argument counts at every use. Optional types (`param: type`) are deferred, and that syntax is kept free.
- **Parameter names** in declarations are documentation only. Writing `?` in a declaration is an error.
- **A slot holds a Value or a Placeholder.** A Value is a name, a number or a string. Role names as Values are left to *Roles inside Playbooks*.
- **Variables become Placeholders (`?name`).** A Placeholder is a blank filled by matching, once per Plan run, and never reassigned. There's no assignment statement, and anything that changes over time lives in Facts. The name avoids "variable" because that suggests mutable state.
- **Filled in the Trigger and Context, used in the Body.** Using one that was never filled is an error. Plot Plans follow the same rules.
- **The same name twice is the same value.** A bare `?` means "don't care". A filled Placeholder that's never used gets a warning.
- **A Value in a Trigger restricts the Plan to it.** Which Plan wins when several match belongs to *Priority model*.
- **Only what's certainly filled can be used.** `NOT` never fills anything. Under `OR`, a Placeholder counts as filled only if every branch fills it.
- **A match satisfies the whole Context**, not one Fact at a time.
- **Which match is used when several satisfy a Context is unspecified.** Explicit choice (random, every match, ranking by priority) is fog, linked to *Groups* and *Priority model*.
- **Handed over:** whether a Body `IF` can fill Placeholders goes to *Context vs control flow*.
