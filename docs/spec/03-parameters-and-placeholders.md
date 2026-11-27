# Parameters and Placeholders

How Vocabulary items take parameters, and how Plans fill and use them. Decided in the ticket *Parameters and variables* (`.scratch/regia-2/issues/03-parameters-and-variables.md`). This chapter replaces the parameter parts of primer ch.3 and ch.4. The design choice behind Placeholders is recorded in `docs/adr/0001-placeholders-are-filled-by-matching.md`.

## Declaring parameters

Every kind of Vocabulary item (Fact, Cue, Action, Goal) declares its parameters the same way: a list of **parameter names** in parentheses after its name.

```regia
FACT hates(person)
CUE insult_heard(speaker)
ACTION toast(target)
```

- Parameter names are documentation. They tell readers and tools what each slot means (the Visual Editor can show `hates(person: …)`), but they never bind anything. A Plan is free to use different names.
- An item without parentheses takes no parameters.
- A Signal is sent with the parameters of the Cue it is declared as: `SIGNAL insult_thrown(host)`.
- Parameters are **untyped**: any slot accepts any value. The Transpiler checks that every use has as many arguments as the declaration has parameters. A name has one parameter count across the Program, so `hates(a)` and `hates(a, b)` can't both be declared (chapter 10, ADR 0006).
- Writing `?` in a declaration is an error, since a declaration describes slots and doesn't fill them.

Optional types (`target: Role`) are not part of 2.0. The `name: type` form is kept free so they can be added later.

In the examples, the Context is written as the `IF` directly under the Trigger, as in 1.0. Chapter 06 (`06-context-and-control-flow.md`) replaces this with `GIVEN`.

## Values and Placeholders

Every argument slot holds either a Value or a Placeholder.

A **Value** is fixed when the Plan is written:

| Value | Example |
|---|---|
| Name | `kitchen`, `red_wine`, declared with `NAME` (below) |
| Number | `3`, `-0.5` (see chapter 04, `04-numbers-and-expressions.md`) |
| String | `"A guest finishes their meal."` (its form is in chapter 01) |

### Names are declared

Decided in the ticket *The Vocabulary and the game* (`.scratch/regia-revision/issues/07-vocabulary-and-the-game.md`), with ADR 0027.

```regia
NAME kitchen, hall, gate
NAME roast, red_wine

WHEN hungry: DO walk_to(kitchen)
```

- **Every Name written in the source is declared** with `NAME`, at the top level of a file, like any other declaration (chapter 10). A Name that isn't declared is an error: `DO walk_to(kitchn)` no longer compiles, and the hint suggests the closest declared Name.
- A `NAME` line declares Names only. It takes no parameters, no `AS` and no `GAME`, and it has no kind beyond being a Name.
- Names share the program-wide namespace (chapter 10): `NAME roast` and `FACT roast` can't both exist, and two Names can't differ only in case. Re-declaring a Name declares the same Name, so a Playbook file can declare the Names it uses.
- **Only the source is checked.** A Name that arrives at runtime, from the game or in a Message, isn't checked against the declarations: the game may send Names the Program never writes.
- A declared Name can go in any slot. Which Names suit which slot is a matter for types (*Declaring parameters*, above), not in 2.0.
- An Agent's name is a Name only inside Instancing (chapter 21, *Individual Agents*): a `.regia` file never writes one (chapter 07), and a Plan reaches an Agent through a Placeholder, meeting its name at runtime as an ordinary Name.

### `ME`

`ME` is a reserved Value: **the Agent running the Plan**. It is the same thing `FROM ?who` fills when that Agent is the Sender, so the two compare equal.

```regia
WHEN scandal(?victim):
    GIVEN ?victim != ME:                           # gossip about somebody else
        DO gasp

WHEN scandal(ME):                                  # gossip about me
    PURSUE save_face

WHEN insulted, FROM ?foe:
    TELL peer wronged(ME, ?foe)                    # each peer hears about the teller
```

- It goes wherever a Value goes in a Playbook: a Trigger slot, a Context or `IF`, an argument, an Expression's comparison.
- **It is filled in by the Agent that writes it**, when the Trigger is matched or the Statement runs. In a Message it travels as that Agent: the receiver doesn't read it as itself. At the receiver, `?x = ME` is true exactly when `?x` holds the receiver.
- It is not a recipient: `TELL ME …` is an error (`R07_04-value-as-recipient`, chapter 07).
- **It is an error anywhere in a Plot**, a Role setup included: a Director is not an Agent, and a setup is the same for every Agent of the Role (chapter 16). Allowing it in a setup is left for later.
- `FROM ME` on a Trigger means the Agent caused the item itself (chapter 05).
- "Regia never names an Agent" (chapter 07) still holds: `ME` is not a name from Instancing.

A Role name can't be a Value (`toast(Host)` is `R03_03-role-as-value`): Roles are only recipients and `FROM` Senders (chapter 15, `15-roles-and-mappings.md`). Fill a Placeholder with `FROM Host ?h` and use `?h`.

A **Placeholder** is a blank the Agent fills in by matching. It is written `?name`, with the same `?` wherever it appears, so a reader never has to look elsewhere to tell it apart from a Value.

```regia
WHEN insult_heard(?speaker):       # filled with whoever insulted
    IF hates(?someone):            # filled with anyone I hate
        DO toast(?speaker)         # uses what was filled
```

A Placeholder is **not** a programming variable:

- It is **filled by matching**, or **once by `LET`** in the Body (`LET ?dmg BE RANDOM(1, 6)`, see chapter 04). It is never reassigned.
- It is filled **once per Plan run**, and keeps that value until the run ends.
- It is gone when the run ends. Anything an Agent must remember, or that changes over time, is a Fact: `FORGET counter(3)`, `LEARN counter(4)`.

## Where Placeholders are filled and used

- **Filled** in the Trigger and the Context of a Plan by matching, or in the Body by `LET` (chapter 04).
- **Used** in the Body, in any argument slot.
- Using a Placeholder in the Body that was never filled, or before the Statement that fills it, is an error.
- The rules are the same for Plans in Playbooks and Plans in Plots.
- **A Plot's parameters** (`PLOT HonorDuel(quarrel):`) are Placeholders already filled in every Plan and Role setup of the Plot, for the whole Staging: `?quarrel`. A Trigger or Context that names one tests it, and no Plan fills it again (chapter 17).

An `IF` inside a Body can also fill Placeholders, usable only inside its branch: see chapter 06 (`06-context-and-control-flow.md`).

### Values in a Trigger restrict it

A Value in a Trigger slot must match exactly, so it restricts the Plan to that value:

```regia
WHEN insult_heard(host):           # only when the host is the speaker
    DO complain
WHEN insult_heard(?speaker):       # anyone
    DO toast(?speaker)
```

When both Plans match in the same Playbook, the first in the text runs, so the narrower one goes first. Between Playbooks, precedence decides (chapter 13, `13-plan-selection.md`).

### Same name, same value

A Placeholder name written more than once in a Trigger and Context stands for one value. The first appearance, reading left to right, fills it, and every later appearance must match it. This is how a Context joins Facts:

```regia
IF owes(?debtor, ?lender) AND hates(?lender):
```

### "Don't care": `?`

A bare `?` fills a slot without naming it: `IF hates(?)` means "I hate someone". Every `?` is independent of the others and can't be used in the Body. A named Placeholder that is filled but never used gets a warning suggesting `?`.

A named Placeholder is **used** when any of these holds:

- the Body names it (an argument, an expression, a recipient);
- it appears a second time in the Trigger or Context, so it joins two conditions (`hates(?x) AND is_nearby(?x)`), the second appearance under `NOT` included;
- a Pick ranks or weighs by it: `HIGHEST ?p`, `LOWEST ?p`, or a Weight that names it (chapter 26). A Pick needs a named Placeholder, so `?` couldn't be written there;
- it appears only inside a `COUNT(…)`, where naming it documents the slot (chapter 26).

A Placeholder filled by a Trigger shared by several `GIVEN` Blocks is used if any of the Blocks, or the `ELSE`, uses it (chapter 06). This is the only case the writer can't fix with `?`, so it's the only one spared the warning. One filled by a `GIVEN`'s own Context is checked in that Block like any other. Decided in *What counts as using a Placeholder* (`.scratch/showcase-1-5/issues/08-using-a-placeholder.md`).

A `?` may carry a name for the reader: **`?_victim`**, a name starting with `_`. It is still a "don't care": it fills nothing the Plan can use, two of them never join even with the same name, and it never gets the warnings below. It says what is ignored, so a Trigger can keep the shape of its neighbours (`WHEN insult_heard(?_who):` next to Plans that use `?who`) without being warned for it.

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

When several matches satisfy the Context, the Agent uses **one**, and **the language does not say which**. A Plan must not rely on any particular order, even if one Target always gives the same answer. Choosing on purpose (`, RANDOMLY`, `, HIGHEST ?p`, `, LOWEST ?p`), running for every match (`FOR EACH`) and counting matches (`COUNT`) are in chapter 26 (`26-match-selection.md`).


## Transpiler checks

**Errors**

- `R03_01-wrong-argument-count` A use with a different number of arguments from the declaration's parameters.
- `R03_02-placeholder-in-declaration` A `?` in a declaration.
- `R03_03-role-as-value` A Role name used as a Value, as an argument or in an Expression (hint: fill a Placeholder with `FROM Role ?x`).
- `R03_04-unfilled-placeholder` A Placeholder used in the Body that was never filled, or used before the Statement that fills it. Its *never filled* part is an absence check (chapter 23).
- `R03_05-maybe-unfilled-placeholder` A Placeholder used that isn't certainly filled: filled only under `NOT`, or in only some branches of an `OR`, an `IF` or a `RANDOMLY` (the message names the branch).
- `R03_06-dont-care-in-body` A bare `?`, or a `?_name`, in the Body.
- `R03_09-me-in-plot` `ME` in a Plot, a Role setup included.
- `R03_10-undeclared-name` A Name that isn't declared with `NAME` (the hint names the closest declared Name).
- `R03_11-misused-name-declaration` A `NAME` line with parameters, `AS` or `GAME`, or inside a `PLAYBOOK` or `PLOT`.

**Warnings**

- `R03_07-unused-placeholder` A named Placeholder that is filled but never used (hint: `?`). What counts as a use is listed under *"Don't care": `?`*. Absence check (chapter 23).
- `R03_08-placeholder-only-under-not` A named Placeholder that appears only under `NOT` (hint: `?`). Absence check (chapter 23).

## Regia 1.5

All of this chapter is in 1.5 (ADR 0025), the Value `ME` included. `FROM ME` is later: in a 1.5 build it is `R01_09-later-regia-construct` (chapter 01). `ME` in a Plot is still `R03_09-me-in-plot`.

Decided in the ticket *The Regia 1.5 cut* (`.scratch/regia-revision/issues/22-the-1-5-cut.md`).

## Not decided here

- Parameters of Goals and the Trigger kinds: chapter 05 (`05-goals-and-triggers.md`).
- Facts as arguments, such as `TELL(Guest, hates(host))`: *Messaging between Agents*.
- Typed parameters (`walk_to(place: Place)`), and a Placeholder known to hold an Agent of a Role: after 2.0. The `name: type` form stays free for them.
