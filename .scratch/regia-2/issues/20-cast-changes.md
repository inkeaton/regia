# Cast changes mid-Plot

Type: grilling
Status: open
Blocked by: 18

## Question

Can Agents join or leave a Staging while it is running (Q4f)? For example an Agent dies, a new guest arrives, a Role is emptied. Decide whether cast changes are allowed, who decides (Director, instancing, game engine), how they are written, and what happens to the Playbooks given to an Agent that leaves.

## Comments

- From *Roles inside Playbooks* (16): a whole-Role Mapping is live (whoever plays the Role when a Message is sent or arrives); a counted pick (`2 OF Guest`) is fixed when the Statement runs, never grows, and an Agent who stops playing the giving Role drops out of it. Decide whether that is enough once Agents join and leave, and what happens to Givings held by an Agent that leaves. See `docs/spec/15-roles-and-mappings.md`.
