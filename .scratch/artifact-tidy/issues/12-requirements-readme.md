# One Requirements table and README pass

Type: task
Status: open
Assignee:
Blocked by: 11, 13

## Question

Where does a reader find every external requirement and the one command to reproduce the paper?

In the top-level README, add:

- a **Requirements** table: uv (which brings Python), JDK 21 (auto-provisioned through the Gradle toolchain), Gradle (the wrapper only), Node (`.nvmrc`) and Godot 4.7, each with what needs it
- a **Reproduce the paper** section: `make all`, what it produces, roughly how long it takes, and where the reference outputs are
- the license, and a CI badge

Sweep all READMEs for stale commands and paths (`./gradlew`, `fig/`, `pip install`, `python server.py`, "wrapper included").
