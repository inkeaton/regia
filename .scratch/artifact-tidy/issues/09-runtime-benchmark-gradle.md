# Runtime benchmarks run through the wrapper

Type: task
Status: open
Assignee:
Blocked by: 06, 07

## Question

How do the runtime benchmarks launch JaCaMo with the pinned Gradle and JDK instead of a bare `gradle` on the PATH?

Today `language/benchmarks/runtime/jcm_generator.py` writes a Groovy `build.gradle`, and `runtime_runner.py` runs `gradle run --no-daemon`. Pick one of two approaches and record why:

- the generated project calls the `minds` wrapper with `-p <dir>`
- the generated project is a minimal Kotlin build that reuses the wrapper and toolchain config

Either way, the generated `.jcm` follows ticket 07's layout convention. Smoke-test with the smallest runtime experiment and `--reps 1`.
