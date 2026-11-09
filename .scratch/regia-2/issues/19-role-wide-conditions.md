# Conditions over a whole Role

Type: grilling
Status: open
Blocked by: 18

## Question

How does a Director react to conditions over a whole Role (Q4d)? For example "when ALL Guests signal X", "when ANY Guest…", "when 3 Guests…", or Facts aggregated across a Role's Agents. Decide which quantifiers exist and how they read.

## Comments

- From *Messaging between Agents* (08): a Signal reaches every Director giving the Playbook, and Agents can `TELL`/`ASK` a whole Role. Quantifiers over a Role's Signals ("when ALL Guests signal X") build on that. See `docs/spec/07-messaging.md`.
- From *Subplots and Stagings* (18): a Subplot's cast is fixed when it starts, and a parent hears its Subplots only through `WHEN P ENDED[, WITH e]` (one Trigger, first match). Role-wide conditions are about a Director's own Roles in its own Staging; check that quantified Triggers read alongside `ENDED`. See `docs/spec/17-subplots.md`.
