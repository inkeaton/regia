# Where generated agents live: asl-path or src/agt

Type: prototype
Status: closed
Assignee: claude (session 2026-11-24)
Blocked by: 06

## Question

Can generated `.asl` files stay in a separate `src/agt/gen/` folder while subplot directors are still found at runtime?

The generated root director spawns subplot directors with `.create_agent(ChildId, "director_<subplot>.asl")`, a bare name looked up on the ASL source path (`src/agt/`). That's why `director_missingdonut.asl` was copied up out of `gen/` by hand. JaCaMo 1.2's `.jcm` parser accepts `asl-path:`.

The prototype has four steps:

1. Add `asl-path: "src/agt", "src/agt/gen"` to `science.jcm`.
2. Delete `src/agt/director_missingdonut.asl`.
3. Run the MAS headless.
4. Check whether the MissingDonut subplot director spawns when ForScience starts the subplot. If needed, trigger it by sending the percepts, or by a minimal scripted `start_plot`.

- **It spawns (option B):** keep `gen/`, gitignore it, and simplify `include("gen/…")` if `asl-path` makes the prefix unnecessary.
- **It doesn't (option A):** have the compiler write straight into `src/agt/`, and gitignore generated files by the compiler's name patterns (`director_*`, `role_*`, `playbook_*`), with the handwritten `scientist/cop/dog.asl` kept tracked.

The answer records which option won and the evidence. That's the runtime log lines.

## Resolution (2026-11-24)

**Option B wins: generated agents stay in `src/agt/gen/`.** With `asl-path: "src/agt", "src/agt/gen"` in `science.jcm`, the subplot director is found at runtime. `1.0` is now at **`e7ddab3` "Keep generated agents in src/agt/gen via asl-path"** (anonymous, no trailer), on top of `a68d387`. **Not pushed.**

**Experiment** (a scratch copy of `minds` with fresh `regia compile` output in `gen/` and the top-level `director_missingdonut.asl` deleted; no Godot). The directors call no Vesna actions, so `forscience_director` ran as a plain Jason agent. A probe agent sent it `achieve start_subplot("missingdonut", …)`, so the real generated `.create_agent` at `director_forscience.asl:178` ran. Prototype files (jcm variants, probe, filtered logs): [prototypes/07-asl-path/](../prototypes/07-asl-path/).

| Variant | jcm | Result |
|---|---|---|
| A (control) | no `asl-path` | `GRAVE: Error in internal action '.create_agent(ChildId,SourceFile)' (file:src/agt/gen/director_forscience.asl:178): director_missingdonut.asl (File o directory non esistente)`. Agents afterwards: `[forscience_director,cop,scientist,dog,probe]` |
| B | `asl-path: "src/agt", "src/agt/gen"` | `[ForScience] Spawning subplot 'missingdonut' as agent missingdonut_forscience_director_136 …` → `[MissingDonut] Booting up director agent missingdonut_forscience_director_136 in phase 'trade'...`. Agents: `[…, missingdonut_forscience_director_136, …]` |
| C | B, plus bare `include("role_…")` and agent source `director_forscience.asl` | same as B, no errors |
| D (negative) | bare includes, no `asl-path` | `GRAVE: The included file 'role_forscience_scientist.asl' was not found!` (also cop and dog), plus A's `create_agent` error |

So `asl-path` serves `include` and `.create_agent` alike, and the `gen/` prefix is unnecessary.

- **Syntax gotcha:** in JaCaMo 1.2, `asl-path:` must come **after** the agent declarations in the `mas` block. Placed first, it gives `ParseException: Encountered "agent"`.

**What `e7ddab3` changes** (in `science_game/minds/`):
- `science.jcm`: `asl-path: "src/agt", "src/agt/gen"` (with a comment) at the end of the block, and the director source becomes `director_forscience.asl`.
- `scientist/cop/dog.asl`: `include("gen/role_…")` → `include("role_…")`.
- `src/agt/director_missingdonut.asl` → `src/agt/gen/` (`git mv`; it is byte-identical to the compiler output).
- `src/agt/gen/playbook_copbaselineplaybook.asl` is removed: it is stale, no `.regia` source emits it, and nothing includes it.
- Check: `diff -r` of a fresh `regia compile src/regia/for_science.regia -o …` against `src/agt/gen/` is empty. `./gradlew classes` passes. A real `./gradlew run` shows no parse or include errors; the VesnaAgents die with "Connessione rifiutata" as expected without Godot.

`gen/` is still tracked: untracking and gitignoring it is ticket 08's job.

### Facts for later tickets

- **08:** compile into `src/agt/gen/` and gitignore `science_game/minds/src/agt/gen/` as a whole; the handwritten `scientist/cop/dog.asl` stay in `src/agt/`. `regia compile -o` doesn't delete stale files (that's how `playbook_copbaselineplaybook.asl` survived), so the Exec task should clear the dir before compiling (or declare it as an output Gradle owns). The README section "Recompiling the Regia Sources" (lines 85–89) still points at `gen/`; 08 removes it anyway.
- **09:** `jcm_generator.py` already writes `<target>/gen/*.asl` and uses `gen/` prefixes in the `.jcm` (`asl_subdir="gen"`). To follow this convention it should add an `asl-path` line listing the gen dir (after the agents) and drop the prefix. That matters for any experiment whose plot spawns subplots.
- **README (12):** the `gen/` layout description can stay as is; mention that `asl-path` is what makes subplot directors resolvable.
