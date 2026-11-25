# Runtime benchmarks run through the wrapper

Type: task
Status: closed
Assignee: claude (session 2026-11-24)
Blocked by: 06, 07

## Question

How do the runtime benchmarks launch JaCaMo with the pinned Gradle and JDK instead of a bare `gradle` on the PATH?

Today `language/benchmarks/runtime/jcm_generator.py` writes a Groovy `build.gradle`, and `runtime_runner.py` runs `gradle run --no-daemon`. Pick one of two approaches and record why:

- the generated project calls the `minds` wrapper with `-p <dir>`
- the generated project is a minimal Kotlin build that reuses the wrapper and toolchain config

Either way, the generated `.jcm` follows ticket 07's layout convention. Smoke-test with the smallest runtime experiment and `--reps 1`.

## Resolution (2026-11-24)

Done, with both approaches combined. `1.0` is now at **`b0bf219` "Run the runtime benchmarks through the minds' Gradle wrapper"** (anonymous, no trailer), on top of `1990cb2`. **Not pushed.**

- **Launch:** `runtime_runner.py` runs `science_game/minds/gradlew -p <dir> run --no-daemon` (`gradlew.bat` on Windows). No second wrapper copy, so the Gradle version and checksum have one home.
- **Build:** the generated project is a Kotlin `build.gradle.kts` plus `settings.gradle.kts` (foojay, JDK 21 toolchain). `-p` alone would run JaCaMo on whatever JDK runs Gradle, and the Groovy template was a second DSL. JVM flags and the JaCaMo version are unchanged.
- **Layout:** agents stay in `<dir>/gen/`. The `.jcm` uses bare names and `asl-path: "gen"` after the agents (ticket 07). The empty `src/` is gone.
- **Added:** a `prepare` task, run once per experiment before measuring, downloads Gradle, the JDK and JaCaMo. Otherwise a fresh machine's downloads would fall inside the first measurement window. A broken setup now raises instead of looking like a run.

**Checks** (in a PID namespace with an empty Gradle home, so no JVM outside it was touched):
- `prepare`: the wrapper downloads Gradle 9.9.2 and succeeds. An installed JDK 21 was used, so the foojay download was not exercised here.
- `run` with 2 agents per role: launcher on `java-21-openjdk` (Gradle on 27), threads `role0_0 … role1_1, director` alive, log "[MainPlot] Booting up director agent director in phase 'phase_0'".
- Negative: without `asl-path`, `FileNotFoundException: role_mainplot_role0.asl`.
- The first two `scale_agents` points through `run_runtime_experiment` (10 s window): both OK, 20 samples each. The runtime CLI has no `--reps`, and no full experiment was run.

### Facts for later tickets

Pre-existing and left alone (scope):
- The runner measures every JVM matching `JVM_MARKERS`, Gradle's own included, and **terminates all of them** at the end of each run. That includes unrelated Gradle daemons, such as the one `./gradlew classes` leaves behind. **11:** use `--no-daemon` (or `./gradlew --stop`) before any runtime benchmark.
- `success` only means some matching JVM was sampled. The second run had `jvm_found_s` = 0.001, consistent with picking up the previous run's dying JVM (the runner doesn't wait for JVMs it terminates).
- The generated agents call `act_N` actions that nothing implements, so the director's `on_enter` fails at its first action and the rest of the broadcast does not run.
- **12:** `benchmarks/README.md` doesn't document the runtime benchmarks at all (`python -m benchmarks.runtime run <experiment>`). They need a JDK ≥ 17, and the network once.
