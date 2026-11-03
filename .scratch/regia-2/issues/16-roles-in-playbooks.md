# Roles inside Playbooks

Type: grilling
Status: open

## Question

How does a Playbook refer to other Agents without knowing who they are (primer ch.4, ch.5)? Proposal: Playbooks declare Roles of their own (e.g. `TELL host …`), bound when the Playbook is given out. Decide how those Roles are declared and bound (`ASSIGN NobleSocializing TO Guest WITH host = Host`?), and how this relates to mapping Roles into Subplots.

## Comments

- From *Goals and Trigger kinds* (05): Playbooks stay Plot-independent; `FROM DIRECTOR` is resolved at runtime to the Director of whichever Plot gives the Playbook. `FROM Role` names a Role of the Staging; how a Playbook can name Roles at all is this ticket's question.
