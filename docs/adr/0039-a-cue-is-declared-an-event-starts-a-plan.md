# A Cue is declared; an Event is anything that starts a Plan

Until now `EVENT` declared a Vocabulary item: something that happens in the world and is over once noticed (`EVENT insult_heard(speaker)`). There was then no word for the wider idea, "whatever can start a Plan" (a Fact learned, a Goal over, a Phase entered, a Playbook given), and the glossary had to list *triggering event* under *Avoid*. In Jason, the Target, an *event* is exactly that wider idea (`+b`, `-b`, `+!g`, `-!g`), so the spec's word and the Target's word meant different things.

We decided that the Vocabulary item is a **Cue**, declared with `CUE` (`GAME CUE`, local `CUE`, and a Signal is a Cue an Agent sends to its Directors), and that **Event** is the general word: anything that happens to an Agent or a Director and can start a Plan. A Trigger names one Event, and each sort of Event is a Trigger kind. Cue fits the theatre words Regia already uses (Director, Role, Plot, Staging): a cue is what tells an actor to act. The old keyword `EVENT` is an error with the hint "renamed `CUE`" (`R0513`), not a second spelling.

## Considered options

- **Keep `EVENT` and find another word for the wide idea** (*Trigger kind* alone, or *happening*): the Target and the BDI literature already say *event* for the wide idea, so every Jason chapter would keep translating.
- **Accept `EVENT` as a synonym of `CUE`**: two spellings of one declaration is what *A few words do many jobs* (the old guide's Review List, D1, at commit `c30d1d4`) asks to avoid.
- **Another word for the item** (*Percept*, *Happening*, *Stimulus*): a percept also covers Facts from the game, and the others don't fit the theatre vocabulary.

## Consequences

- Every spec chapter, the glossary and the game protocol say Cue (`regia_cue`, `regia_game(cue, …)`, the console's `> cue`). ADRs before this one keep their wording; read their *Event* as *Cue*.
- The guide and the showcase still say `EVENT` until they are brought up to the revised design.
- In Regia 1.5.
