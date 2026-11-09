# Instancing comments

Type: grilling
Status: open
Blocked by: 02

## Question

What information do instancing comments carry, and where do they live (primer ch.8, ch.9)? Candidates: Agent counts per Role, the Root Plot, Target-specific configuration (Jason `.jcm`, custom interpreters). Decide whether they are comments, a separate file, or both; what they look like; and whether they can be specific to one Target. The markers `#%` and `#%[ … ]#` are already reserved by [Comment syntax](02-comment-syntax.md); this ticket decides their content, placement, and whether a separate file is needed too.

## Comments

- From *Context vs control flow* (06): an Instancing comment selects the ASL dialect the Transpiler emits for, such as `#% ASL_VERSION = JASON` / `GENERIC` (native `if/elif/else` vs `IF` lowered to subgoal plans for the in-house interpreters). Decide its name, values, default and where it may appear. See `docs/spec/06-context-and-control-flow.md`.
- From *Priority model* (14): Instancing may order **independent** Plots only (no common ancestor Plot), as an ordered list of top-level Plots, highest first, with no ties. An order between Plots that share an ancestor is an error. Decide its syntax, and whether Plots other than the Root Plot can be started by Instancing at all (if not, this never occurs). See `docs/spec/13-plan-selection.md`, section *Instancing*.
- From *Label syntax and mood Labels* (15): each Agent's starting Propensity values (`TRAIT`/`MOOD`, spec 14) come from Instancing, as does VEsNA-Pro's selection `strategy` (`most_similar` or `random`; it must be set or VEsNA-Pro crashes). In ASL they become the `.jcm` user parameters `temper: temper(t(v), …, m(v)[mood], …)` and `strategy: …`. Decide the `#%` syntax, per Agent or per Role, and what happens to a Propensity with no value. See `docs/spec/14-labels.md`.
- From *Subplots and Stagings* (18): Subplots are started only by `START SUBPLOT`; `END PLOT WITH` in a Plot that is never a Subplot is ignored with a warning. Decide whether top-level Plots other than the Root Plot exist and who starts them. See `docs/spec/17-subplots.md`.
- From *Cast changes mid-Plot* (20): an Agent the game adds while the Program runs joins the Root Plot in the Roles Instancing gives its kind, like a starting Agent. So Instancing must describe Agent kinds with their Root Plot Roles (and Propensity values), usable for spawned Agents as well as the starting count, not only "n Agents play Role X". See `docs/spec/19-cast-changes.md`.
