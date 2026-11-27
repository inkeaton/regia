# The Vocabulary says what the game produces, and a dot means the Target's own code

A `FACT` or `EVENT` declared with `GAME` is produced by the game; every other one is produced only by the Program. An External name is the game's name for a game item, and the Target translates it into the Regia name on the way in, so beliefs never carry the game's spelling. An Action's External name says who runs it: without a dot, the game, through the protocol; with a dot, the Target's own code (a Java internal action in Jason), written into the output as it stands (spec 10, 28, 37).

The Interface (ADR 0015) already works out who in the Program sends each Event. What it can't see is the game. Without `GAME`, an Event nobody sends and an Event the game sends look the same, so a misspelt or forgotten Event fails silently, and an Agent can `LEARN` a Fact the game will overwrite. Before this, an External name went straight into Jason, where a dotted Fact or Event couldn't be a belief and a dotted Action was read as a Java class, so the showcase didn't build.

## Considered Options

- **Infer the game's items** from which Events the Program never sends: this was the rule, and it turns every misspelling into "from the game".
- **Mark only Facts and Events that have an External name**: a game item with Regia's own spelling would have no mark.
- **A word other than `GAME`** (`STAGE` was proposed): `Staging` already names a running Plot, and `FROM GAME` (spec 05) names the same origin; one word is used for both.
- **Declare which Actions are Java in the Instancing Target settings**, leaving the dot without meaning: keeps the source free of any Target, but moves away from what the alias was made for, short names for long namespaced internal actions such as `vesna.walk`.
- **Forbid dots on Facts and Events for Jason**: ties the game's naming to one Target.

## Consequences

- A game can't name an Action with a dot; such an Action is renamed in the game.
- The dot means "not the game" in every Target, so another Target can read a dotted Action as its own code (a Python function, say).
- `AS` on a Fact or Event that isn't `GAME` is an error.
- A game message for an item not declared `GAME`, or not used by the receiver, is dropped with a Trace warning.
- New checks: `R38_07-cue-never-sent` (an Event nothing sends) and `R08_07-edit-of-game-fact` (a Plan changing a game Fact). `R28_01-external-name-not-atom` is gone.
- A Program written before this declares no `GAME` items, so every game Event's Trigger warns until the declarations are marked.
