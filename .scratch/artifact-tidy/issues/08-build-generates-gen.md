# The minds build generates its agents from .regia

Type: task
Status: open
Assignee:
Blocked by: 04, 06, 07

## Question

How does building or running minds always regenerate its AgentSpeak from the `.regia` sources, so the two can't drift?

Add a Gradle task (an `Exec` running `uv run regia compile src/regia/for_science.regia -o <dir from ticket 07>`) that declares `src/regia/**` as its inputs and the generated dir as its output. Wire it before `classes` and `run`. Then untrack the generated files and gitignore them, following ticket 07's layout.

The task should fail with a clear message if `uv` is missing. Delete the old "Recompiling the Regia Sources" section from the science_game README, because the build now owns that step.

Check two things: a clean clone + `./gradlew classes` produces the agents, and editing a `.regia` file reruns the task.
