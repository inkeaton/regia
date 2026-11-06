# Instancing comments

Type: grilling
Status: open
Blocked by: 02

## Question

What information do instancing comments carry, and where do they live (primer ch.8, ch.9)? Candidates: Agent counts per Role, the Root Plot, Target-specific configuration (Jason `.jcm`, custom interpreters). Decide whether they are comments, a separate file, or both; what they look like; and whether they can be specific to one Target. The markers `#%` and `#%[ … ]#` are already reserved by [Comment syntax](02-comment-syntax.md); this ticket decides their content, placement, and whether a separate file is needed too.

## Comments

- From *Context vs control flow* (06): an Instancing comment selects the ASL dialect the Transpiler emits for, such as `#% ASL_VERSION = JASON` / `GENERIC` (native `if/elif/else` vs `IF` lowered to subgoal plans for the in-house interpreters). Decide its name, values, default and where it may appear. See `docs/spec/06-context-and-control-flow.md`.
- From *Priority model* (14): Instancing may order **independent** Plots only (no common ancestor Plot), as an ordered list of top-level Plots, highest first, with no ties. An order between Plots that share an ancestor is an error. Decide its syntax, and whether Plots other than the Root Plot can be started by Instancing at all (if not, this never occurs). See `docs/spec/13-plan-selection.md`, section *Instancing*.
