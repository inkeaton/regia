# The Cast is a Role every Plot has

Chapter 20 said there is no whole-Cast recipient, since every Role can be named. We now reserve `CAST` as the Role every Agent of a Staging plays. A Plot doesn't declare it and writes it wherever one of its own Roles can be: as a recipient, an `ASSIGN` target, the giver's side of a `MAPPING`, after `FROM` and `BY`, in a Quota, before `JOINED`, after `PLAYS`, and as the header of a setup (spec 15, 16).

Naming every Role was not the same thing. A knight playing `Guest` and `Guard` heard a `TELL` per Role twice. The showcase wrote `ASSIGN Courtesy, MAPPING Host TO host` in four setups, and a new Role meant a fifth. `EVERYONE` is the whole game, other Stagings included.

## Considered Options

- **A recipient only** (`TELL CAST …`), with a separate `ALL ROLES STARTS WITH:` for the setup: two words for one idea, and no answer for "everyone else" in a Mapping or for a Quota over the whole Staging.
- **Narrow `EVERYONE` to the Staging inside a Plot**: a Director would lose the whole game, and the word would mean two things on either side of the Playbook's edge.
- **A list of Roles as a recipient** (`TELL Guest AND Guard …`) with duplicates removed: it still has to be kept up to date by hand, and chapter 07 allows one recipient per Statement.
- **Leave it**: the double `TELL` is a wrong behaviour that nothing warns about.

## Consequences

- `CAST` is a reserved word. A Plot or a Playbook that had a Role called `Cast` must rename it.
- It never binds by name: a Playbook Role is filled from the whole Cast only by an explicit `MAPPING CAST TO …`.
- Giving and taking stay symmetric. `UNASSIGN P FROM Guest` takes `P` from the Guests even when it was given to the whole Cast: the Cast Giving narrows to `CAST EXCEPT Guest`, for those already there and for joiners. `UNASSIGN P FROM CAST` takes every Giving of `P` the Staging made. Making the Cast Giving untouchable from a Role was considered and rejected, because adding and removing Playbooks per Role is the core of the language, and a Director shouldn't have to remember which word a Playbook was given with.
- `CAST STARTS WITH:` runs before the Role setups, once per Agent per Staging.
- With `EXCEPT`, `CAST EXCEPT Duellist` is "everyone else" in a Mapping.
- A Playbook can't write it. A Playbook doesn't know a Plot.
- Recasting, once sketched as `CAST ?who AS Host`, will need another word.
