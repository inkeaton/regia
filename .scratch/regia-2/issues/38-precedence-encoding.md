# Precedence encoding in ASL

Type: grilling
Status: open
Blocked by: 34, 35

## Question

How is precedence (spec 13) encoded in Jason? Decide the rank key's encoding, how a Plot's position is computed when it is started from two parents, and how `selectOption` compares keys.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- From *ASL infrastructure layout* (34): selection lives in the `regia-jason` agent class, which extends VEsNA-Pro's and follows its annotation approach (spec 28). The user's direction: a new ranking annotation on plans. It can carry only the fixed part of a rank (Playbook, Trigger Block position); the Giving's part is the `regia_given` belief. Decide the annotation's shape here.
- From *Giving and taking Playbooks at runtime* (35): the rank is the `Rank` argument of `regia_given(Playbook, Staging, Director, Target, Rank, Bindings)`, sent in `regia_give`. Combine ranks across several `regia_given` beliefs of one Playbook (chapter 29).
- From *Director runtime in ASL* (36): `regia_standing(Seq, Playbook, Role, Rank, Bindings)` stores the Rank to replay. Directors run `regia.DirectorAgent` and rank Phase over `DURING PLOT` through a helper shared with the Agents' class (chapter 30).
