# The minds build generates its agents from .regia

Type: task
Status: closed
Assignee: claude (session 2026-11-24)
Blocked by: 04, 06, 07

## Question

How does building or running minds always regenerate its AgentSpeak from the `.regia` sources, so the two can't drift?

Add a Gradle task (an `Exec` running `uv run regia compile src/regia/for_science.regia -o <dir from ticket 07>`) that declares `src/regia/**` as its inputs and the generated dir as its output. Wire it before `classes` and `run`. Then untrack the generated files and gitignore them, following ticket 07's layout.

The task should fail with a clear message if `uv` is missing. Delete the old "Recompiling the Regia Sources" section from the science_game README, because the build now owns that step.

Check two things: a clean clone + `./gradlew classes` produces the agents, and editing a `.regia` file reruns the task.

## Resolution (2026-11-24)

Done. `1.0` is now at **`1990cb2` "Generate the minds' agents from .regia in the Gradle build"** (anonymous, no trailer), on top of `e7ddab3`. **Not pushed.**

- **Task `compileRegia`** (Exec, in `build.gradle.kts`): `uv run --project <repo root> --package regia --locked regia compile src/regia/for_science.regia -o src/agt/gen`. Output is `src/agt/gen`. Before compiling it deletes `gen/`, because the compiler leaves stale files behind.
- **Inputs:** `src/regia/`, and also the transpiler (`language/src/regia/**/*.py` and `*.lark`, `language/pyproject.toml`, `uv.lock`, `.python-version`). Beyond the ticket's `src/regia/**`, because a transpiler change makes the agents drift too.
- **Wiring:** `compileJava` depends on it, not `classes`. The Java source dir is `src/`, which contains `gen/`, so with `classes` the second build fails Gradle's implicit-dependency check. `classes` and `run` follow from `compileJava`.
- **Untracked and gitignored:** `/science_game/minds/src/agt/gen/`. The handwritten `scientist/cop/dog.asl` stay tracked.
- **README** (`science_game/README.md`): "Recompiling the Regia Sources" is gone. uv is in the Prerequisites row, and the run section says the build compiles the `.regia` files.

**Checks** (exports of the staged tree into scratch dirs):
- Clean export + `./gradlew classes`: passes, and `gen/` is identical to the previously tracked files.
- Unchanged rebuild: `UP-TO-DATE`.
- Editing a `.regia` file reruns the task. Editing a transpiler file, or a generated file by hand, does too (checked before the `ignoreEmptyDirectories()` tweak, which only stops `__pycache__` dirs from counting). A stale file is gone after the next rerun.
- A broken `.regia` fails the build with the compiler's diagnostic. Without `uv` on PATH: "uv was not found on the PATH. … Install it from https://docs.astral.sh/uv/ and try again."
- `./gradlew` (default `run`): the directors boot and the playbooks load from `gen/`. The WebSocket errors come from having no Godot.
- `uv.lock` is unchanged by the build.

### Facts for later tickets

- **Makefile (11):** the minds target (`./gradlew classes`) already transpiles, so a separate transpile step would be a `./gradlew compileRegia`. The build runs `uv run`, which needs the network once (or a synced `.venv`).
- **CI (13):** the minds job needs uv (`astral-sh/setup-uv`) as well as Java.
- **README (12):** uv belongs in the Requirements table for minds too.
- `src/agt/gen/` doesn't exist in a fresh clone until the first build, so anything that reads it must build first.
