# The shape of a code

Type: grilling
Status: closed
Assignee: claude
Blocked by:

## Question

What does a Diagnostic code and a Trace code look like, so that a reader understands it from the code alone, while a machine still has a short, stable identity to match on? Which files does the migration rewrite, and how is it kept from inventing anything?

## Resolution

Decided with the user on 2026-11-27, while charting the map.

**The shape.** `<kind><chapter>_<index>-<name>`, for example `R01_11-clause-without-comma`.

- **Kind**: one letter, `R` for a Diagnostic code (build time), `T` for a Trace code (run time), as today.
- **Number**: the chapter's two digits, `_`, then the check's two digits in that chapter. These are today's numbers unchanged, with a separator: `R0111` becomes `R01_11`. `_` was chosen over `.` (breaks double-click selection and must be escaped in a regex) and `-` (can't be told from the name's hyphens).
- **Name**: lowercase kebab-case, at most 4 words and about 30 characters, in glossary terms, with no articles. It names the **mistake or event** a reader sees (`clause-without-comma`, `role-as-value`, `negative-weight`), not the rule or the fix.
- The whole code is one token, matched by `[RT]\d{2}_\d{2}-[a-z0-9-]+`. It also serves as the code's docs-page file name.

**Identity.**

- The **number is the identity**. Machines match on it: the Conformance runner, `#@allow`, the Trace `code` field, and docs-page lookup. The name is for people, and a wrong name next to a right number is an error.
- Names are **unique across all R and T codes**, so a name alone is unambiguous.
- Names may be fixed freely **until the 1.5 release**, and are frozen after it, like numbers. A retired name stays reserved, as a retired number does.
- 1.5-only codes (`R0109`, `T1902`) and retired codes get ordinary names with no status marker: status can change, a code can't. Status stays in the chapter text.

**Where it is written.**

- Live docs write the **full code everywhere**: check lists, prose, the `#! error` and `#! rule:` lines of cases, the guide, ADR titles. The Transpiler prints it the same way (`error[R01_11-clause-without-comma]: …`). A table column headed "code" may go bare only if full forms prove too cramped.
- After the migration, each chapter's check list (and each Trace code list) is the **single source** of a code's name. The mapping file is kept in this effort's folder as the frozen record of old to new, not as a second registry.

**The migration.**

- **Rewritten**: `docs/spec` (chapters and cases), `docs/guide`, `docs/showcase`, `GLOSSARY.md`, `docs/adr`, and `.scratch` tickets whose `Status:` is `open`. **Left as history**: closed and resolved tickets, finished maps, `docs/primer`, and the `1.0` branch. The mapping file is how you look up an old code found there.
- One hand-written **mapping file** (`old,new`), reviewed by the user, is the script's only input. The script never invents a name.
- The script matches whole tokens only (`\b[RT]\d{4}\b`). It **fails** on a code missing from the mapping and on a mapping entry it never used, has a dry run that prints a count per file, runs once, and is checked with `git diff` and the full test run. It lives in this effort's folder, not in `transpiler/`.

**Overrides.** This reverses chapter 27's "A better shape is deferred past 2.0". That sentence goes, and the switch gets an ADR (*Rewrite the spec text on codes*).
