# Label syntax and mood Labels

Type: grilling
Status: open

## Question

How are Labels written on a Trigger (primer ch.4)? Proposal: `,`-separated (`WHEN insult_heard, PRIORITY 5, TEMPER sympathy(-0.5), EFFECTS aggressiveness(0.2):`). What should `TEMPER` and `EFFECTS` be called (closer to VEsNA-Pro "propensities")? Is the Label set fixed or extensible by Target? What happens to a Label a Target doesn't support (ignored, warning, error)?

## Comments

- From Statement and block syntax: lines continue only after a trailing `,` or inside an open `(`. How a long Trigger with many Labels wraps is left to this ticket.
- From *Goals and Trigger kinds* (05): a Trigger reads `WHEN`/`TO`, item, kind word, `FROM …`, then Labels: `WHEN hates(?h) LEARNED FROM ?teller, PRIORITY 5:`. See `docs/spec/05-goals-and-triggers.md`.
- From *Context vs control flow* (06): the Context is a `GIVEN` Block nested under the Trigger, and Labels on the Trigger's header apply to every `GIVEN` Plan under it. Decide whether a single `GIVEN` can carry its own Labels, and how. See `docs/spec/06-context-and-control-flow.md`.
- From *Priority model* (14): `PRIORITY` is removed from the language; precedence is written as relations in a Plot's `PRECEDENCE:` Block. Mood Labels now carry semantics: Trigger Blocks with the same Trigger in one Playbook that all carry mood Labels are **Mood alternatives** for the Selection function, and mixing labelled and unlabelled Blocks for one Trigger is an error. Decide the Label names (`TEMPER`/`EFFECTS`), what counts as a "mood Label" for that rule, how a neutral alternative is written, and how unsupported Labels are reported (spec 13 already asks for one warning per Program on a Target without a Selection function). A Label on a single `GIVEN` must never make `GIVEN` siblings alternatives. See `docs/spec/13-plan-selection.md`.
