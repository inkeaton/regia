# Events are momentary; Fact changes and Goals are Trigger kinds

Everything a Plan can start from is a Trigger kind: an Event happening, a Fact being learned or forgotten, a Goal being pursued or dropped. Fact changes are not a separate mechanism; they are just as much "things that happen" as Events are. What sets a declared `EVENT` apart is that it is **momentary**: it triggers Plans and leaves nothing behind, so it can never be tested in a Context, believed or forgotten. A Fact lasts until it is forgotten. We kept both because "the food was served" and "I am hungry" are different things to a designer, and because modelling momentary happenings as Facts leaves stale Facts behind, a classic BDI bug.

In the Trigger, a kind word follows the item (`WHEN hates(?h) LEARNED:`), Fact Triggers always need one, and Goal recipes read `TO find_food:`. So a reader can tell every kind apart without looking up a declaration.

## Considered Options

- **Merge Events into Facts** (as in AgentSpeak, where a percept is a belief): one fewer concept, but every momentary happening must be forgotten by hand, and a Context could test things that are already over.
- **Facts can't trigger, only be tested**: simpler Triggers, but designers lose "react when I start hating someone", which BDI supports natively.
- **Kind word before the item** (`WHEN LEARNED hates(?h)`): the kind is read first, but it reads less naturally than a participle after the item.
- **No kind word, inferred from the declaration** (`WHEN hates(?h):`): shorter, but a reader can't tell a Fact from an Event without looking elsewhere.
- **Rename `EVENT` to `CUE`** so that "Event" could be the umbrella term: deferred. 2.0 keeps `EVENT` and uses "Trigger kind" as the umbrella.

## Consequences

- The ASL mapping must make Events momentary (for example, by removing the belief after the reaction), and must map `LEARNED`/`FORGOTTEN`/`TO`/`DROPPED` to `+b`/`-b`/`+!g`/`-!g`.
- One name belongs to one Vocabulary kind, so the Transpiler can check every kind word against the declaration.
- `ON ENTER` / `ON EXIT` in Plots become `WHEN` Triggers, so there is one reaction keyword.
