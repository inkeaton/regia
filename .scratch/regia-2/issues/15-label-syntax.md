# Label syntax and mood Labels

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How are Labels written on a Trigger (primer ch.4)? Proposal: `,`-separated (`WHEN insult_heard, PRIORITY 5, TEMPER sympathy(-0.5), EFFECTS aggressiveness(0.2):`). What should `TEMPER` and `EFFECTS` be called (closer to VEsNA-Pro "propensities")? Is the Label set fixed or extensible by Target? What happens to a Label a Target doesn't support (ignored, warning, error)?

## Answer

Spec chapter: `docs/spec/14-labels.md`. Glossary: *Propensity*, *Trait*, *Mood*, *Suits Label*, *Shifts Label*, *Suits alternative* added (replacing *Mood alternative*), *Label*, *Selection function* and *Vocabulary* updated. Specs 01, 05, 06, 07 and 13 updated (`TEMPER` placeholders replaced); `mood(...)` example Facts in 04, 08, 09 renamed, since `MOOD` is now reserved. No ADR: every decision is cheap to reverse. Input: VEsNA-Pro research on branch `research/vesna-pro-temper`, file `research/vesna-pro-temper.md`.

- **Syntax:** Labels come last on a Trigger header, each written `, KEYWORD …`, in any order, each at most once. Several Propensities in one Label are joined with `AND`, so `,` always means "next Label". A long header wraps after a `,` (spec 01).
- **Fixed set of two:** `SUITS p AT n` (the Plan best fits an Agent whose `p` is near `n`; the only Label that affects selection) and `SHIFTS m BY n` (running the Plan changes Mood `m`). Values are Number literals in [-1, 1]. Targets can't add Labels. `TEMPER`, `EFFECTS`, `PRIORITY` are gone.
- **Propensities:** VEsNA-Pro's umbrella term. Declared in the Vocabulary as `TRAIT x` (never changes) and `MOOD x` (changes), file level only, no parameters, External names allowed. `SUITS` names either kind, `SHIFTS` only Moods, both checked at compile time. They aren't Facts: no Context test, no Action. Starting values come from Instancing.
- **Where:** both Labels on Playbook `WHEN`/`TO` headers. `SHIFTS` also on `GIVEN`/`ELSE`, adding to the header's (the same Mood twice is an error). `SUITS` on `GIVEN`/`ELSE` is an error. Any Label on a Director Plan is an error until *Director capabilities*.
- **Suits alternatives** (renamed from mood alternatives): only `SUITS` creates them; `SHIFTS`-only Trigger Blocks are ordinary. No neutral alternative: every alternative says what it suits. A `TIES` pool mixing `SUITS` and unlabelled candidates ranks them as the Target does, with a warning.
- **Timing:** when a Shift applies belongs to the Target; the language only promises that running the Plan shifts those Moods.
- **Unsupported Labels:** ignored, one warning per Program per Label.
- **VEsNA-Pro facts recorded in the ASL notes:** an unlabelled plan scores as a perfect fit under `most_similar`; effects apply only at contested intention selection; no mood change from a Body; `strategy` must be set; range and clipping bugs.
- **Handed off:** Propensity values and the VEsNA strategy in `#%` to *Instancing comments*; Director Propensities to *Director capabilities*; a `SHIFT` Body Statement, a language-defined neutral ranking, and testing Propensities in a Context to the fog.

## Comments

- From Statement and block syntax: lines continue only after a trailing `,` or inside an open `(`. How a long Trigger with many Labels wraps is left to this ticket.
- From *Goals and Trigger kinds* (05): a Trigger reads `WHEN`/`TO`, item, kind word, `FROM …`, then Labels: `WHEN hates(?h) LEARNED FROM ?teller, PRIORITY 5:`. See `docs/spec/05-goals-and-triggers.md`.
- From *Context vs control flow* (06): the Context is a `GIVEN` Block nested under the Trigger, and Labels on the Trigger's header apply to every `GIVEN` Plan under it. Decide whether a single `GIVEN` can carry its own Labels, and how. See `docs/spec/06-context-and-control-flow.md`.
- From *Priority model* (14): `PRIORITY` is removed from the language; precedence is written as relations in a Plot's `PRECEDENCE:` Block. Mood Labels now carry semantics: Trigger Blocks with the same Trigger in one Playbook that all carry mood Labels are **Mood alternatives** for the Selection function, and mixing labelled and unlabelled Blocks for one Trigger is an error. Decide the Label names (`TEMPER`/`EFFECTS`), what counts as a "mood Label" for that rule, how a neutral alternative is written, and how unsupported Labels are reported (spec 13 already asks for one warning per Program on a Target without a Selection function). A Label on a single `GIVEN` must never make `GIVEN` siblings alternatives. See `docs/spec/13-plan-selection.md`.
