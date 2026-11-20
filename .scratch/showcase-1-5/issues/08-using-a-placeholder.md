# What counts as using a Placeholder

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 03

## Question

`R0307` warns about a named Placeholder that is filled and never used (chapter 03). The written showcase ([*Write the 1.5 showcase Program*](03-write-the-program.md)) relies on readings the spec doesn't state:

- A Placeholder named only in a Pick: `HIGHEST ?stake` in `HonorDuel`, `LOWEST ?size` in `Scheming`, `WEIGHT ?size` in `NobleSocializing`. A Pick needs a named Placeholder (chapter 26), but only `COUNT` is said to spare it the warning.
- A Trigger's Placeholder that some `GIVEN` siblings use and others don't (`?speaker` in `NobleSocializing`'s gossip about others).

Decide whether each counts as a use, and write it into chapters 03 and 26.

Then decide the showcase's one allowed warning: `#@allow: R0307` on the alternative that only laughs. Chapter 02 says a warning the language avoids by itself is fixed in the language, "as `?_name` does", and `?_who` is exactly that fix here. Either keep the allow, give the reason it is chosen over `?_who`, and say so in chapter 02, or write `?_who` and show `#@allow` only in a snippet. *What the showcase must show* chose the allowed warning.

## Resolution

What `R0307` spares is what `?` can't be written for (*Language vs game design*). The showcase drops its allowed warning.

- **A Pick is a use.** `HIGHEST ?p`, `LOWEST ?p` and a Weight that names `?p` use it, since a Pick needs a named Placeholder filled by its own condition (`R2602`). That covers `?stake` in `HonorDuel`, `?size` in `Scheming`, and `?size` in `NobleSocializing`'s `vent`.
- **A join is a use.** A named Placeholder that appears a second time in the Trigger or Context restricts the Match, even with no Body use. That includes a second appearance under `NOT`. One that appears *only* under `NOT` is still `R0308`.
- **A shared Trigger is checked as a whole.** A Trigger Placeholder is used if any `GIVEN` Block under it, or the `ELSE`, uses it, because the Trigger is written once and can't say `?` for one Block. A Placeholder filled by a `GIVEN`'s own Context is checked in that Block alone. That covers `?victim` and `?speaker` in `WHEN scandal(?victim) FROM peer ?speaker`.
- **`COUNT`** stays as it was: a Placeholder named only inside it is a use.
- **The allowed warning goes.** The laughing alternative writes `FROM peer ?_who`, which is exactly the fix chapter 02 points to. The source now has no warning and nothing allowed. `#@allow` becomes a snippet on chapter 02's own case, an order by name between two Playbooks never held together (`R1305`). `?_name` gains a coverage row. This supersedes the warnings line of *What the showcase must show*.
- **Spec.** Chapter 03 lists what counts as a use under *"Don't care": `?`*, and `R0307` points there. Chapter 06's *What the Plans share* adds the shared-Trigger rule. Chapter 26's *The ranked Placeholder* adds the Pick rule. Chapter 02 is unchanged, since it already says this.
- **Showcase.** `noble_socializing.regia`, and the README's *Diagnostics* paragraph and its `#@allow` and "Don't care" rows. Also the walkthrough outline's insult line and open-question line.
