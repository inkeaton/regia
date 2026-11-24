# Gradle wrapper, Kotlin DSL and JDK 21 toolchain for minds

Type: task
Status: open
Assignee: claude (session 2026-11-24)
Blocked by: 02

## Question

How does `science_game/minds` build with a pinned Gradle and a pinned JDK, whatever happens to be installed?

Steps:

1. Generate the wrapper (latest Gradle 9.x) and commit `gradlew`, `gradlew.bat` and `gradle/wrapper/`.
2. Convert `build.gradle` to `settings.gradle.kts` and `build.gradle.kts`.
3. Set a Java toolchain of 21, with the foojay resolver plugin in settings so JDK 21 is downloaded when missing. The author's machine has JDK 27, which makes it a good test.
4. Keep the `run` task as the default, with the same behaviour.

`./gradlew classes` must pass. In the README, replace "wrapper included" and the bare `./gradlew` with the real commands.
