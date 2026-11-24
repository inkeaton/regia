# Where generated agents live: asl-path or src/agt

Type: prototype
Status: open
Assignee:
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
