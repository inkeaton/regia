# The Vocabulary and the game

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: none

## Question

What does a declaration say about the game's side, and what is checked about the Values that fill it?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- B1 Dotted External names are refused by the only Target
- D14 The Vocabulary names what the game supplies and not what the game does
- F8 Values are neither declared nor typed
- L8 The Role files are fixed at build time (the *Translation to ASL* note)

Decide:

- What an External name may look like for each kind, and what `hall.guards.seize` should be. The showcase is fixed to match.
- Whether a declaration can say who sends an Event, who keeps a Fact, whether an Action can be refused or ends the Agent.
- Declared Names, typed Parameters, or a Placeholder known to hold an Agent of a Role: which of these, and when.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

## Resolution

Resolved on 2026-11-17, with the user.

- **B1, fixed.** An External name has no meaning in Regia. For a game Fact or Event it is the game's name, and `regia-jason` translates it into the Regia name when the game reports the item (`regia_game` beliefs), so beliefs never hold dots. For an Action the dot keeps the meaning the alias was made for: dotted is the Target's own code (a Java internal action in Jason, written into the ASL as it stands), undotted is a game Action, sent through the protocol under its External name (`regia.act(N, A)`). A game can't name an Action with a dot. `R2801` is gone. The showcase's `hall.guards.seize` becomes an undotted game Action.
- **D14, fixed in part.** `GAME FACT` and `GAME EVENT` declare what the game produces; only those can come from the game, and only they take `AS`. It gives two warnings: an Event nothing sends (`R3807`), and a Plan changing a game Fact (`R0807`). Who in the Program sends an Event stays inferred (ADR 0015). **Kept**: no word for "can be refused", since every game Action can be. **Deferred past 2.0**: an Action that ends the Agent. The word `STAGE` was proposed and turned down: it clashes with Staging, and `FROM GAME` already names the same origin.
- **F8, fixed in part.** Every Name in the source is declared with `NAME`, and an undeclared one is an error (`R0310`). Names share the program-wide namespace. Names arriving at runtime are not checked. **Deferred past 2.0**: typed parameters and a Placeholder known to hold an Agent of a Role; `name: type` stays free.
- **L8, the Role-files half, kept.** A Role file holds every Playbook it can be given, filtered by a belief (chapter 29): no hidden state, all of it in the mind inspector. Narrowing it waits for typed Placeholders.

Settled while writing, not asked:

- `NAME` is file-level only, with no parameters, `AS` or `GAME` (`R0311`).
- `GAME` covers every item of a Multi-definition, and two declarations of an item merge only if both say `GAME` or neither does.
- `GAME` on a `GOAL`, an `ACTION`, a `NAME` or a local item is an error (`R1016`).
- A game message whose name has no `regia_game` entry for the receiver is dropped with `T2801`.

Changed:

- Spec: chapter 10 (new section *What the game produces: `GAME`*, *External names* rewritten), chapter 03 (new section *Names are declared*), chapters 07, 08, 28, 30, 37 and 38. New codes: `R0310`, `R0311`, `R0807`, `R1016`, `R3807`, `T2801`. `R1010` widened; `R2801` removed.
- ADRs: 0026 *The Vocabulary says what the game produces, and a dot means the Target's own code*; 0027 *Names are declared*.
- Glossary: *Game item* and *Name* added; *External name*, *Value* and *Custom Action* reworded.

Handed on:

- The Trigger picker can offer only Events someone sends, now that game Events are marked (B13): [*The Visual Editor*](18-visual-editor.md).
- The words `GAME` and `NAME` are open to [*Words that do several jobs, and syntax nobody used*](20-words-and-syntax.md).
- The showcase's vocabulary file still uses the four comment banners, the dotted Fact and Event names, `hall.guards.seize`, and no `NAME` lines; the guide's *Vocabulary* and *Translation to ASL* describe the old rules.
- Conformance cases for the new codes.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- B1 in. D14 in (`GAME`, `R3807`, `R0807`). F8 in for declared Names. L8 in, as it is.
