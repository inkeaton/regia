# ASL infrastructure layout

Type: grilling
Status: resolved
Assignee: Edoardo Vassallo

## Question

What does the Jason output look like as a set of files? Decide:
- Shared infrastructure files imported by each generated file, instead of copied plans (primer ch.8).
- What infrastructure state each Agent holds (its Playbooks, which Plots gave them).
- Generated names for Local Vocabulary (spec 10) and External names in Jason.
- Which clock Jason measures Durations with, wall or game time (spec 12).

## Answer

Spec chapter: `docs/spec/28-jason-layout.md`. Name rules added to `docs/spec/10-scoping-and-imports.md`. Generated names in chapters 06, 09, 11 and 26 renamed to the `regia_<kind>__<part>` shape. Specs 12, 13 and 21 point to the new chapter. Glossary: *Infrastructure* and *Generated name* added.

- **Layout**: `build/<entry>/` holds `<entry>.jcm` and `asl/` with `regia/{agent,director}.asl`, `playbooks/` (one per Playbook), `directors/` (one per Plot, run by every Staging) and `roles/` (Root Plot Roles only, each including every Playbook reachable through Subplot Mappings). File names are Regia names as written.
- **Shared Infrastructure**: fixed ASL built into the Transpiler and written into every Build with a version header. Only top-level files (Role, Director) include it, since Jason doesn't skip duplicate includes. Playbook files include nothing.
- **Java**: a `regia-jason` library versioned with the Transpiler, never generated. Its agent class extends VEsNA-Pro's and follows VEsNA's annotation approach with a new ranking annotation in `selectOption`. The annotation holds only the fixed part of a rank; the part that depends on the Giving is a belief. The `.jcm` points at it by default. A Build is ASL plus `.jcm` only. VEsNA is maintained in the same department, so its code can be extended freely.
- **State**: all Infrastructure state is beliefs with one Generated functor per concept, catalogued in chapter 28. The owning tickets fill in the arguments.
- **Names**: designer names are unique ignoring case, can't start with `regia_` and can't contain `__`. Generated names start with `regia_` and use `__` between parts; Local Vocabulary is `regia_local__<owner>__<name>`. Regia names get their first letter lowercased; Jason reserved words are renamed quietly to `regia_word__<name>`.
- **External names**: emitted exactly as written. A dotted Action is a Java internal action; a plain one goes to the environment. Fact and Event External names must be Jason atoms, or the Jason Target reports an error.
- **Clock**: wall clock only (`.wait`), no setting. A game clock is post-2.0.

## Comments

- Graduated from the map's fog in the scoping pass of 2026-11-09.
- First of the full ASL mapping tickets; the others build on its layout.
- From *Match selection over a Context* (32): Picks, `FOR EACH` and `COUNT` lower to `.setof` over a tuple of the condition's blanks (notes in `docs/spec/26-match-selection.md`). Open check: whether Jason's `for` keeps variables bound in its body across rounds; if so, `FOR EACH` lowers to a generated recursive goal.
- Open check carried to the development effort: Jason resolves `{ include(...) }` against the source path set in the `.jcm`; confirm when the first Build runs.
