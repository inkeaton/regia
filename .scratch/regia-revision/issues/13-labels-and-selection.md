# Labels and the Selection function

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 12

## Question

How much of what `SUITS`, `SHIFTS` and `TIES` do does the language promise, and how much is the Target's?

Causes from [*Review List*](../../../docs/guide/20%20-%20Review%20List.md):

- B9 A Shift is promised by the language and applied by chance
- B10 A tie only works by editing both Playbooks
- F7 What the Selection function does is the Target's business

Decide:

- When a Shift is applied, or what the language stops promising.
- What an unlabelled Plan is worth against a labelled one (chapter 14's neutral ranking), and what that needs from VEsNA-Pro.
- Alternatives that name different Propensities, and a Propensity with no value.
- Reading or changing a Mood from a Plan: 2.0 or later.

For every cause, the answer is one of: fixed now (with the spec chapters, ADRs and glossary entries to change), kept as it is (with the reason), or deferred past 2.0. The sorting in *Review List* is a proposal and can be overturned here.

Blocked by: [Which Plan runs](12-which-plan-runs.md).

## Resolution

Resolved on 2026-11-17, with the user. Choosing between Plans stays VEsNA-Pro's, as it is today. The language changes only what the Transpiler hands it, and adds one way to change a Mood.

- **B9** deferred past 2.0. When a `SHIFTS` Label applies stays the Target's. The spec records VEsNA-Pro's behaviour: effects apply only through `selectIntention`, with several intentions and one carrying `temper`. New warning `R1410` for a `SHIFTS` Label the Target can never apply (a kind that meets no `SUITS`). The reliable way is the new `SHIFT` Statement.
- **B10** fixed in part, kept for the rest.
  - An unlabelled candidate in a `TIES` pool with a `SUITS` is neutral: 0.5 for a Trait, 0 for a Mood. Labelling one side is enough, and the tie no longer behaves as an `OVER` for the unlabelled side. `R1309` retired.
  - Kept: a Plot can't write Labels for the Playbooks it ties, because only a Playbook's author can say what its Plans suit.
  - `TIES` with no `SUITS` on either side keeps name order and `R1308`.
- **F7** fixed in part, deferred for the rest.
  - Fixed:
    - Neutral alternatives inside a Playbook, so mixing is allowed (`R1304` retired).
    - A missing starting value is neutral (0.5 Trait, 0 Mood) with no warning (`R2111` retired).
    - Trait values are limited to [0, 1], as VEsNA-Pro keeps them.
    - New Statement `SHIFT m BY expr [AND …].` for Moods only, in Playbooks only, applied when it runs.
    - Propensity code is emitted only where something needs it: no `temper`, `effects` or `strategy` for a Program without Labels or `SHIFT`; `strategy` is always written next to `temper`; a Mood that can be shifted is always in the `.jcm`.
  - Deferred past 2.0: the fit defined by the language, when a Shift applies, and testing a Propensity in a Context.

Changed:

- Spec:
  - Chapter 08: `SHIFT` in the set and the reserved words; a Director can't use it.
  - Chapter 13: Suits alternatives include unlabelled Blocks as neutral; ties labelled on one side; the Target weighs the fit; `R1304`, `R1309` retired.
  - Chapter 14: neutral values; Trait range; when a Shift applies stays the Target's; neutral alternatives; *The `SHIFT` Statement*; `R1403`, `R1404`, `R1406`, `R1409` revised, new `R1410`, `R1411`; *Not in 2.0* rewritten; ASL notes on the neutral `temper`, the emission rules, `regia.shift` and VEsNA-Pro's scoring.
  - Chapter 20: no `SHIFT` in a Director.
  - Chapter 21: Trait range, neutral missing values, `R2107` revised, `R2111` retired, `temper`/`strategy` only when needed.
  - Chapter 32: neutral `temper` on the plan annotation.
  - Chapter 36: when `temper` and `strategy` are written.
- ADR: new ADR 0033 *Choosing by Propensity is the Target's, and an unlabelled Plan is neutral*.
- Glossary: *Propensity*, *Mood*, *Shifts Label*, *Selection function*, *Suits alternative* revised; *Shift* and *Neutral alternative* added.

Handed on:

- To the Jason chapters (fog on the map): `regia.shift` and the public method it needs on VEsNA-Pro's `Temper`; chapter 36's example writes the Mood `sympathy(0)` without `[mood]`.
- To [*The Trace*](17-trace.md): recording Mood changes, from `SHIFT` and from `SHIFTS`.
- To the guide (fog on the map): chapter 14's three ways to take an insult can drop the forced Labels; the escalation example should use `SHIFT`; `test.regin`'s bare `hothead` no longer warns.

1.5, from [*Which systems Regia 1.5 keeps*](21-which-systems-1-5-keeps.md):

- B9, B10, F7: in, as decided here. What is deferred adds to this and replaces nothing.
