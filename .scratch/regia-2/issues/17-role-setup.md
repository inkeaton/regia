# Role setup

Type: grilling
Status: open

## Question

Can a Role declare a starting state (primer ch.5)? Facts, Goals and Playbooks an Agent receives when it starts playing the Role. Decide the syntax and when it applies (at the start of the Staging, or when the Agent joins), and whether that state is removed when the Agent stops playing the Role.

## Comments

- From *Roles inside Playbooks* (16): Playbooks now declare Roles of their own (`ROLE host.`), filled by Mappings when given. Role setup is about a Plot's Roles; check whether a Playbook given as part of a Role's starting state takes Mappings the same way. See `docs/spec/15-roles-and-mappings.md`.
