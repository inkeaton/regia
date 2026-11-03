# Parameters and Placeholders

How Vocabulary items take parameters, and how Plans fill and use them. Decided in the ticket *Parameters and variables* (`.scratch/regia-2/issues/03-parameters-and-variables.md`). This chapter replaces the parameter parts of primer ch.3 and ch.4. The design choice behind Placeholders is recorded in `docs/adr/0001-placeholders-are-filled-by-matching.md`.

## Declaring parameters

Every kind of Vocabulary item (Fact, Event, Action, Goal) declares its parameters the same way: a list of **parameter names** in parentheses after its name.

```regia
FACT hates(person)
EVENT insult_heard(speaker)
ACTION toast(target)
```

- Parameter names are documentation. They tell readers and tools what each slot means (the Visual Editor can show `hates(person: …)`), but they never bind anything. A Plan is free to use different names.
- An item without parentheses takes no parameters.
- A Signal is sent with the parameters of the Event it is declared as: `SIGNAL insult_thrown(host)`.
- Parameters are **untyped**: any slot accepts any value. The Transpiler checks that every use has as many arguments as the declaration has parameters.
- Writing `?` in a declaration is an error, since a declaration describes slots and doesn't fill them.

Optional types (`target: Role`) are not part of 2.0. The `name: type` form is kept free so they can be added later.

## Values and Placeholders

Every argument slot holds either a Value or a Placeholder.

A **Value** is fixed when the Plan is written:

| Value | Example |
|---|---|
| Name | `host`, `red_wine` |
| Number | `3`, `-0.5` (see chapter 04, `04-numbers-and-expressions.md`) |
| String | `"A guest finishes their meal."` |

Whether a Role name can be a Value (`toast(Host)`) is decided in *Roles inside Playbooks*.

A **Placeholder** is a blank the Agent fills in by matching. It is written `?name`, with the same `?` wherever it appears, so a reader never has to look elsewhere to tell it apart from a Value.

```regia
WHEN insult_heard(?speaker):       # filled with whoever insulted
    IF hates(?someone):            # filled with anyone I hate
        DO toast(?speaker).        # uses what was filled
```

A Placeholder is **not** a programming variable:

- It is **filled by matching**, or **named once** in the Body (`?dmg = RANDOM(1, 6).`, see chapter 04). It is never reassigned.
- It is filled **once per Plan run**, and keeps that value until the run ends.
- It is gone when the run ends. Anything an Agent must remember, or that changes over time, is a Fact: `FORGET counter(3)`, `BELIEVE counter(4)`.

## Where Placeholders are filled and used

- **Filled** in the Trigger and the Context of a Plan by matching, or in the Body by naming (chapter 04).
- **Used** in the Body, in any argument slot.
- Using a Placeholder in the Body that was never filled, or before the Statement that names it, is an error.
- The rules are the same for Plans in Playbooks and Plans in Plots.

Whether an `IF` inside a Body can also fill Placeholders is decided in *Context vs control flow*.

### Values in a Trigger restrict it

A Value in a Trigger slot must match exactly, so it restricts the Plan to that value:

```regia
WHEN insult_heard(host):           # only when the host is the speaker
    DO complain.
WHEN insult_heard(?speaker):       # anyone
    DO toast(?speaker).
```

When both Plans match, which one runs is decided in *Priority model*.

### Same name, same value

A Placeholder name written more than once in a Trigger and Context stands for one value. The first appearance, reading left to right, fills it, and every later appearance must match it. This is how a Context joins Facts:

```regia
IF owes(?debtor, ?lender) AND hates(?lender):
```

### "Don't care": `?`

A bare `?` fills a slot without naming it: `IF hates(?)` means "I hate someone". Every `?` is independent of the others and can't be used in the Body. A named Placeholder that is filled but never used gets a warning suggesting `?`.

## Matching a Context

A match must satisfy the **whole** Context. In

```regia
IF hates(?x) AND is_nearby(?x):
```

the Agent looks for someone it hates *who is also nearby*. It does not take the first person it hates and then fail because they are far away.

### Only what is certainly filled can be used

The Body can only use a Placeholder that is filled on every way the Context can succeed:

- **`NOT`** never fills anything. After `IF NOT hates(?someone)` ("I hate nobody"), using `?someone` is an error. A named Placeholder that appears only under `NOT` gets a warning suggesting `?`.
- **`OR`** fills a Placeholder only if every branch fills it. `IF hates(?x) OR fears(?x)` fills `?x`. After `IF hates(?x) OR is_drunk`, using `?x` is an error, and the message names the branch that leaves it empty.

### Several matches

When several matches satisfy the Context, the Agent uses **one**, and **the language does not say which**. A Plan must not rely on any particular order, even if one Target always gives the same answer. Explicit ways to choose (at random, for every match, by priority or ranking) are not yet specified.

## Not decided here

- Parameters of Goals and the Trigger kinds: chapter 05 (`05-goals-and-triggers.md`).
- Facts as arguments, such as `TELL(Guest, hates(host))`: *Messaging between Agents*.
