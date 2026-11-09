# Role setup

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

Can a Role declare a starting state (primer ch.5)? Facts, Goals and Playbooks an Agent receives when it starts playing the Role. Decide the syntax and when it applies (at the start of the Staging, or when the Agent joins), and whether that state is removed when the Agent stops playing the Role.

## Answer

Spec chapter: `docs/spec/16-role-setup.md`. Glossary: *Role setup* added. Spec 15's pointer updated. No ADR: it is sugar and cheap to reverse.

- **Sugar:** a Role setup adds nothing a Plan couldn't do; it is a place to write what every Agent of a Plot's Role starts with. Only Plot Roles have one; Playbook Roles stay addresses.
- **Syntax:** `ROLE Guest STARTS WITH:` followed by a Block of `ASSIGN <Playbook>[, MAPPING …]` (no `TO`), `LEARN <fact>`, `PURSUE <goal>`. `ROLE Guest:` with a Block is an error. Values and Expressions only, no Placeholders, the same for every Agent; per-Agent values belong to Instancing.
- **When:** for each Agent when it starts playing the Role, per Staging: for the starting cast at Staging start, in Role declaration order, before the initial Phase's entry Plans; again for each Agent joining later. Two Stagings mean two setups; Givings add up.
- **Sender:** the Director. Setup Facts are told and Goals asked by it, so `LEARNED FROM DIRECTOR` (only if new) and `TO g FROM DIRECTOR` match. `PURSUE` never waits.
- **Order and trouble:** written order; a Statement that can't be carried out is skipped with a Trace entry, the rest still run. Warning for a `PURSUE` above the `ASSIGN` giving its recipe.
- **Mappings:** as on `ASSIGN` (spec 15); counted picks and counted targets are errors in a setup (one shared pick for the cast vs one per joiner).
- **Undoing:** Playbooks are ordinary Givings of the Staging, taken away with the others and reachable by `UNASSIGN`, ranked in `PRECEDENCE:` like any Playbook the Plot gives. Facts stay; Goals get nothing extra.
- **Handed off:** what joining means to *Cast changes mid-Plot*; the Director's own telling and asking to *Director capabilities*; a per-joiner pick to the fog.

## Comments

- From *Roles inside Playbooks* (16): Playbooks now declare Roles of their own (`ROLE host.`), filled by Mappings when given. Role setup is about a Plot's Roles; check whether a Playbook given as part of a Role's starting state takes Mappings the same way. See `docs/spec/15-roles-and-mappings.md`.
