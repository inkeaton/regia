# Instancing is the cast of one game setup

An Agent kind gave its Agents Propensity values and nothing else. A hothead couldn't start with a heavier purse, and the Facts that most set one Guest apart, its seat and its grudges, couldn't be stated anywhere in the Program. Chapter 16 sent per-Agent values to Instancing, and chapter 21 had no per-Agent lines. A kind was also written whole every time and replaced whole by a later file, it couldn't be built on another or removed, and a single character needed a kind of its own with a name invented for it (`king PLAYS Host`).

We decided that three layers say what an Agent starts with, and each thing is said in the earliest layer that can know it. The **Program** says what holds for any cast. **Instancing** says what holds for one cast in one game setup, fixed before the run. The **game** says what only comes up while it runs. So Instancing can give what a Role setup gives (`ASSIGN`, `LEARN`, `PURSUE`, told by the Root Director), on a kind (`KIND`) or on one named Agent (`AGENT`). An individual Agent is in the starting cast, is never spawned, and its name is its Agent name, which Instancing may use as a Value. Kinds and Agents build on kinds with `LIKE`, override line by line, and are removed with `NO KIND` and `NO AGENT`. Instancing comments are gone: `.regin` files are its only home.

## Considered options

- **Per-kind Facts only**, keeping "Agents of one kind differ only through `RANDOM`": the hothead's purse is solved, the seat and the grudge stay with the game even when the level fixes them.
- **Individuals as kinds with `COUNT 1`**: no new construct, but the game can spawn more of them, and the Agent is still `gawain_1`.
- **Leave individuals to the game** (`GAME FACT`): the Program stays free of particular characters, and a seat known before the run is still invisible in every file.
- **Instancing's lines arrive `FROM GAME` when the Fact is a game Fact**: closer to "the game setup", but a sender would depend on a declaration in another file.
- **`CLASS` for kinds**: plural in spirit, but it clashes with Jason's agent class in the `.jcm`.

## Consequences

- A `.regin` can now hold story-like lines. The layer rule keeps them apart: a line that would hold for every cast belongs in a Role setup, never in a kind.
- A Program never names a kind or an individual Agent; a Plan meets an individual's name only as a Value arriving at runtime.
- On Jason, individual Agents get their own `.jcm` entries and appear in `cast.json` without a kind (chapter 36). The Root Director runs the setup lines of kinds and Agents after the Root Plot's setups.
- Going from two knights to one is `KIND knight: COUNT 1`; a fifth kind of Guest is one `LIKE` line.
- A Plot file can't be built into a running cast alone: a cast needs a `.regin`.
- In Regia 1.5 all of it is in except a joiner running its kind's lines, which comes with joining.
