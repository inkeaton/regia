# Research: dynamic plan loading in Jason

Type: research
Status: resolved

## Question

How can Jason/JaCaMo agents gain and lose plans at runtime? Compare `.add_plan`/`.remove_plan`, `include` directives, plan labels and `.relevant_plans`, and the current approach of including every possible Playbook and filtering with a belief in the Context. Cover performance, debuggability, how plan annotations survive, and constraints from running with VEsNA. This is input for how Regia's ASL Target should give and take away Playbooks (primer ch.8).

## Comments

Research running on throwaway branch `research/jason-dynamic-plans` (file `research/jason-dynamic-plans.md`). Never merged.

## Answer

Full findings are on branch `research/jason-dynamic-plans`, file `research/jason-dynamic-plans.md`. Sources: Jason master 84e131b checked against jason-3.1.jar, the Jason docs, and the VEsNA-Pro source. No benchmarks.

- **Cost of an event:** Jason finds candidate plans by a hash lookup on the trigger, so the cost depends on how many plans share a trigger, not on library size. VEsNA's `selectOption` override checks the context of *every* candidate plan.
- **Include all, filter with a belief (current):** inactive Playbooks are still candidates, and their percepts still create events. In return it is simple, reproducible from the files, and safe when several Directors give the same Playbook.
- **`.add_plan` / `tellHow`:** plans carry `source(Director)` and Jason counts sources, which gives the same multi-Director behaviour as `playbook_active(Name, Director)`. Hazards: `.remove_plan` reports success when no plan matches; plan equality ignores labels, so a plan shared by two Playbooks gets merged; `tellHow` always appends at the end and can race with the Director's next message; plan terms pick up values from the Director's variables of the same name.
- **Runtime `.include`:** always `source(self)`, so no source counting; it re-reads the file every time and re-adds any initial beliefs and goals.
- **Annotations:** `temper`, `effects`, `priority` and custom label annotations survive every path, and VEsNA-Pro reads them at decision time.
- **Priority:** nothing reads `priority(N)` today. Plan order decides which plan wins, so appending at the end would change behaviour. Tagging plans with `playbook(Name)` and removing them through `.plan_label` with that pattern works for every dynamic option.
- **Removal mid-run:** an intention already running keeps going after its plan is removed. An `[atomic]` add/remove stops new events being handled in between.
- Side note: VEsNA-Pro `Temper.updateDynTemper` sets a mood that drops below -1.0 to 0.0 instead of -1.0 (looks like a bug).
