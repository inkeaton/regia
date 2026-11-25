# One Requirements table and README pass

Type: task
Status: closed
Assignee: claude (session 2026-11-24, e)
Blocked by: 11, 13, 14

## Question

Where does a reader find every external requirement and the one command to reproduce the paper?

In the top-level README, add:

- a **Requirements** table: uv (which brings Python), JDK 21 (auto-provisioned through the Gradle toolchain), Gradle (the wrapper only), Node (`.nvmrc`) and Godot 4.7, each with what needs it
- a **Reproduce the paper** section: `make all`, what it produces, roughly how long it takes, and where the reference outputs are
- the license, and a CI badge

Sweep all READMEs for stale commands and paths (`./gradlew`, `fig/`, `pip install`, `python server.py`, "wrapper included").

## Context from other tickets

- From [Gradle wrapper, Kotlin DSL and JDK 21 toolchain for minds](06-gradle-wrapper-kotlin.md): `science_game/README.md` has the run order backwards. Godot is the WebSocket server and the agents are clients, so Godot must start first. Check what the director on port 9004 connects to.
- From [License for the code and the questionnaire data](14-license.md): code Apache-2.0 (`LICENSE`), data CC-BY-4.0 (`LICENSE-data`), exceptions in `NOTICE`. The README's license section should link all three.

## Resolution (2026-11-24)

Done. `1.0` is now at **`a02ff34` "Add a Requirements table and a Reproduce the Paper section to the README"** (anonymous, no trailer), on top of `e02958e`. **Not pushed.** READMEs only.

- **Root README:** CI badge, Requirements table, Reproduce the Paper (each target of `make all`, its output and the paper's version), License section linking `LICENSE`, `LICENSE-data` and `NOTICE`. Component READMEs refer to the table.
- **Badge:** a relative URL (`../../actions/…`), so the README doesn't name the account. It should resolve on GitHub; not seen until the push.
- **Demo start order:** Godot first. The director (9004) connects to the debug UI (`ui/debug_ui.gd`). The README now also says which scene to run: F5 runs `main.tscn`, which is empty (as in the submitted snapshot), so the demo is `test_scene.tscn` with F6, or `godot --path … res://test_scene.tscn`.
- **Other fixes:** `expand_data.py` needs `--write`, a duplicate install section and an extra-dependency note in the benchmarks README, `make bench-runtime` documented there.

**Checks:** headless Godot 4.7.2 with `main.tscn` listens on no port; with `test_scene.tscn` on 9001-9004. `./gradlew run` without Godot: all four agents fail to connect; with it running: all four connect and messages arrive. `expand_data.py` runs in report mode. All relative file links resolve, except the badge's, which only exist on GitHub. The demo wasn't played on screen, and `make all` wasn't rerun.

### Left alone

- `main.tscn` is still the main scene: changing it is a game change the review doesn't name.
- The benchmarks README mentions "the thesis" and "Section 7.2"; the qscores README says "Section 8.3". Whether these match the paper wasn't checked.
- Two messages in `language/benchmarks` still say `pip install -e .[benchmarks]`, and `regia serve`'s hint mentions `pip install 'regia[server]'`, though the repository gives no evidence that the package is on PyPI.
