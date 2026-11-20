# The Jason showcase's shape

Type: prototype
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 04

## Question

What do the Jason reference Build and its guide look like? Make a rough outline to react to.

Decide:

- The Build's file layout in `docs/showcase/jason/`, following chapter 28, and whether the generated parts are marked apart from the Infrastructure.
- The guide's order: file by file through the Build, or feature by feature with links into the Build. Every feature of the coverage table should be found by name.
- How it relates to the old guide chapter *Translation to ASL*: what it keeps, and its small `evening` Build.
- Whether it shows Traces from the walkthrough's runs next to the Jason that writes them.

## Resolution

Resolved on 2026-11-18, with the user, by reacting to a prototype outline. The decided outline is [`prototypes/jason-showcase-outline.md`](../prototypes/jason-showcase-outline.md), and it holds the detail.

**The Build.** One reference Build, of `banquet.regin` (the full cast), in `docs/showcase/jason/banquet/`, laid out exactly as chapter 28's `build/banquet/`, so that a real build can be diffed against it file by file. It has nine Playbook files, three Director files, four Role files and `Guest__Guard.asl`, the Infrastructure in `asl/regia/`, the source map, `banquet.jcm` and `cast.json`. It has no `traces/` and no `regia-jason` Java. Where `hall.music.fanfare` lives is left to *The Target's own code in a Build* (ticket 21). The four walkthrough runs get no Builds of their own: the guide shows each run's cast as a diff (`regia_start_cast`, `regia_kind`, start setups, the `.jcm`, `cast.json`).

**Generated vs Infrastructure.** Chapter 28's separation as it stands: the `asl/regia/` folder, and the generated header with `reference` as the version. The guide adds a file table giving each file's kind and source. No other marking.

**The guide.** It lives in `docs/showcase/jason/README.md` and goes **feature by feature**, in grouped parts: the Build; a Plan's Statements; Goals, Actions and Failure; Messages; Givings, Roles and Precedence; the Director and its Phases; Subplots and Stagings; the cast; the game and the Infrastructure; the Trace; costs you can see in the ASL; what has no ASL. Each quote gives `file:line` for both the Regia and the ASL.

**Found by name.** The showcase README's coverage table gets a **Jason** column linking each row to its guide section. Rows with no ASL say why, and the guide's last section lists them.

**The old *Translation to ASL*.** Kept: its opening, its names table (updated for ADR 0026), its game-protocol tables and one sequence diagram (the `evening` run's `arrival`). Dropped: the small `evening` Build (replaced by two real files printed whole, `Keeping_watch.asl` and `roles/Guest__Guard.asl`) and *Since 1.0*. The `#revise` notes that are still true become *Costs you can see in the ASL*.

**Traces.** Short `.trace` excerpts from `runs/<run>/case.trace` sit beside the `regia.trace` call that writes them. One section follows a single entry from the call to its JSONL line to its `.trace` line, with the source map. This depends on tickets 09 and 22.

No new tickets. Changed: [`docs/showcase/README.md`](../../../docs/showcase/README.md) (the Jason folder's place, and the Jason column to come). Nothing in the spec, ADRs or glossary.
