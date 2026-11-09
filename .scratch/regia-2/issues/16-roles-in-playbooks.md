# Roles inside Playbooks

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

How does a Playbook refer to other Agents without knowing who they are (primer ch.4, ch.5)? Proposal: Playbooks declare Roles of their own (e.g. `TELL host …`), bound when the Playbook is given out. Decide how those Roles are declared and bound (`ASSIGN NobleSocializing TO Guest WITH host = Host`?), and how this relates to mapping Roles into Subplots.

## Answer

Spec chapter: `docs/spec/15-roles-and-mappings.md`. Glossary: *Role* widened (Plot or Playbook; only an address in a Playbook), *Mapping* and *Giving* added. Specs 03, 05 and 07 updated where they pointed here. No ADR: every decision is cheap to reverse.

- **Playbook Roles:** a Playbook declares its own Roles with `ROLE x.` at the top of its Block, local to the Playbook, still called *Role*. It never names a Plot or a Plot's Role, so it stays Plot-independent.
- **Addresses only:** in a Playbook a Role is only a `TELL`/`ASK` recipient or a `FROM` Sender; anywhere else (arguments, Context, Custom Action arguments) is an error. A Playbook never directs another Agent (no `Role DO …`, no giving Playbooks); `ASK` stays as a request the receiver decides on. Directing is the Plots' job. Roles are where cooperation will hang after 2.0.
- **Mapping:** `, MAPPING <giver Role> TO <receiver Role>`, one per Role, on both `ASSIGN` and `START SUBPLOT`. Same names bind implicitly; an explicit `MAPPING` overrides; an unfilled Role is a compile-time error. Only Plot Roles on the giver side (`MAPPING ?who` is an error). Many receiving Roles may share one giving Role; one receiving Role gets at most one `MAPPING` per Statement.
- **Bindings:** a whole-Role Mapping is live (checked when sending or receiving), per Staging. Each `ASSIGN` is one Giving with its own bindings; an Agent's Playbook Role is the union over every Giving it holds, across Plots and Stagings, like `SIGNAL`/`FROM DIRECTOR`. `UNASSIGN … FROM Role` removes exactly that Giving.
- **Counts and fractions:** `n OF Role` and `n PERCENT OF Role` (any Expression), only in an `ASSIGN` target and on a `MAPPING`'s giver side. A uniform random pick made once when the Statement runs; it never grows, and leavers drop out. Picks from one Role in one Statement don't overlap; one pick per Statement, shared by every receiver. Rounds down; too many takes everyone left with a warning; negative counts as 0 with a warning; 0 is an empty Role; non-Number fails the Plan.
- **Handed off:** Subplot runtime and Staging identity stay with *Subplots and Stagings*; filling a Role with one Agent to *Director capabilities*; live bindings vs fixed picks under cast changes to *Cast changes mid-Plot*; per-Agent picks (`EACH`), counted recipients, several giving Roles into one, and `?x PLAYS Role` to the fog.

## Comments

- From *Goals and Trigger kinds* (05): Playbooks stay Plot-independent; `FROM DIRECTOR` is resolved at runtime to the Director of whichever Plot gives the Playbook. `FROM Role` names a Role of the Staging; how a Playbook can name Roles at all is this ticket's question.
- From *Messaging between Agents* (08): a Role is a valid recipient (`TELL Guest …`, `ASK Guest TO …`: every Agent playing it except the sender), and `FROM Role` is a sender form on messages between Agents. Decide how a Playbook names such a Role, and which Staging's Agents it means when several Plots give the Playbook. See `docs/spec/07-messaging.md`.
