# A Plan's Statements in ASL

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05, 10

## Question

Group B of the [inventory](../jason-open-questions.md#b-plan-bodies-in-asl-a-plans-statements-in-asl): no chapter holds the translation of a Plan's Statements, and the notes in chapters 06–26 leave pieces open.

Decide:

- where the Statement translations live: the notes in chapters 06–26, or a new Jason chapter;
- how a Placeholder becomes a Jason variable, and the prefix generated variables take;
- `FOR EACH` as Jason's `for` or a recursive goal (with the research on `for`);
- the shape of `regia.wait(Cond, D)` for `WAIT … UNTIL`, and its `time` entry;
- the stale `regia_if__N`/`regia_either__N` lines in chapters 29 and 35.

Closes when the chapters are edited.

## Resolution

Grilled with the user on 2026-11-18; all five recommendations accepted. Written into the spec.

1. **Where the translations live:** a new chapter, `docs/spec/39-jason-plan-bodies.md` (*Plan bodies in Jason*), after the Interfaces chapter so nothing is renumbered. The ASL notes in chapters 06, 08, 09, 12 and 26 now keep only what any AgentSpeak Target must respect and point to it. Chapter 28's list of the full ASL mapping names it. *Messages and told Facts in ASL* and *A Goal's life in ASL* add their Statements to it.
2. **Variables:** a Placeholder's first letter is uppercased (`?speaker` → `Speaker`), and blanks (`?`, `?_name`) become `_`. A generated variable is a Generated name with its first letter uppercased (`Regia_weight__1`, `Regia_total`, `Regia_roll`, `Regia_each__1`), replacing chapter 09's `W1`, `T`, `R`. Chapter 10: `R1008` covers Placeholder names, and `R1007` covers two Placeholders of one Plan that differ only in case.
3. **`FOR EACH`:** a `.setof` snapshot, then Jason's `for (.member(m(…), L))`. The snapshot is needed because `for` works out its solutions lazily (`dining.regia:30` forgets inside its own loop), and `for`'s unbinding between rounds is Regia's scoping. The recursive `regia_each__N` stays only for Targets without loops (chapter 26).
4. **`regia.wait(Cond[, D])`:** `Cond` is a Jason logical formula. It is tested at the call and then on every new event (Jason's `.wait` mechanism; every belief change raises one). It never fails on timeout, unlike `.wait`. It writes the `time` entry itself, printing the instantiated condition through the source map with `_` as `?`, plus `waited`, the milliseconds it waited (chapter 34). `at` comes from the source map. It is listed in chapter 35.
5. **Stale lines:** `regia_if__N` and `regia_either__N` were removed from chapters 29 and 35, and chapter 28's example name is now `regia_when__ready`. The in-house lowerings stay in chapters 06, 09 and 26, marked "not Jason".

The Jason showcase outline (section 2) now quotes chapter 39.
