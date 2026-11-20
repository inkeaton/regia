# The Target's own code in a Build

Type: grilling
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 05

## Question

Group L of the [inventory](../jason-open-questions.md#l-actions-and-the-targets-own-code-the-targets-own-code-in-a-build): `play_fanfare` is a dotted Action, Java the project writes, and no chapter says where it lives.

Decide:

- where the reference Build keeps `hall.music.fanfare`, and how `regia run` and `RunCase` find it, given that a Build has no Java and `regia run` writes no class path;
- who writes a dotted Action's two `DO` entries;
- chapter 37's stale *Not decided here* line on calling an Action off.

Closes when chapters 28, 35 and 37 are edited.

## Resolution

Decided with the user on 2026-11-19. Chapters 10, 23, 28, 34, 35 and 37 are edited.

- **Where the Java lives.** The writer builds the project's own Java, with any tool, into jars in the Project's **`lib/`** folder, beside `build/` in the current directory. `regia run` and `regia test` (`RunCase`) put every `lib/*.jar` on the class path after `regia-jason`, so the writer still writes no class path. The CLI never compiles, reads (in `check` or `build`) or copies them, and a Build still holds no Java (chapters 23, 28, 35). Rejected: a `java/` folder the CLI compiles, and a `TARGET jason` class-path key.
- **Who writes the two `DO` entries.** A dotted Action compiles to `regia.act("hall.music.fanfare", play_fanfare)`, like a game Action. `regia.act` sees the dot, sends nothing, runs the class through `Agent.getIA` synchronously, and writes `DO` and `DO … DONE`/`FAILED`. A `false` return or an exception fails it, with the exception's message as `reason`. Chapter 37 has a new *The Target's own code* section, and chapters 10 and 28 now say "passed to `regia.act`" instead of "written into the ASL as written". Rejected: the bare call between two `regia.trace` calls.
- **A missing class** is a runtime failure (`no Java class <name>`), chapter 11's "Custom Action failed" cause. No check reads `lib/`.
- **Test mode.** The `> action …` rules script only game Actions. A dotted Action runs its real Java in a case (chapters 34, 37).
- **The reference.** `docs/showcase/java/hall/music/fanfare.java`, source only: it logs the fanfare and returns `true`, with a comment that a real one runs agent-side. The Jason guide says how it is jarred into `lib/` ([outline](../prototypes/jason-showcase-outline.md)).
- **Chapter 37's stale line** ("Cancelling an Action when its Plan stops: post-2.0") is deleted. Chapter 08 already says that a dotted Action is never called off.
