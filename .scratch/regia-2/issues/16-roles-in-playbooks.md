# Roles inside Playbooks

Type: grilling
Status: open

## Question

How does a Playbook refer to other Agents without knowing who they are (primer ch.4, ch.5)? Proposal: Playbooks declare Roles of their own (e.g. `TELL host …`), bound when the Playbook is given out. Decide how those Roles are declared and bound (`ASSIGN NobleSocializing TO Guest WITH host = Host`?), and how this relates to mapping Roles into Subplots.

## Comments

- From *Goals and Trigger kinds* (05): Playbooks stay Plot-independent; `FROM DIRECTOR` is resolved at runtime to the Director of whichever Plot gives the Playbook. `FROM Role` names a Role of the Staging; how a Playbook can name Roles at all is this ticket's question.
- From *Messaging between Agents* (08): a Role is a valid recipient (`TELL Guest …`, `ASK Guest TO …`: every Agent playing it except the sender), and `FROM Role` is a sender form on messages between Agents. Decide how a Playbook names such a Role, and which Staging's Agents it means when several Plots give the Playbook. See `docs/spec/07-messaging.md`.
