# Delete the old guide

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 30

## Question

Delete the old guide chapters (`docs/guide/<n> - <Title>.md`, 0–20) and `docs/guide/showcase/`; git history keeps them.

Before deleting, re-point what cites them outside `.scratch/`:

- `docs/showcase/README.md` says it replaces `docs/guide/showcase/`, "kept as it was": reword to name the commit or drop the clause.
- grep `docs/`, `GLOSSARY.md`, `CLAUDE.md`/`AGENTS.md` and the ADRs for `guide/showcase`, `guide/<n> - ` and old chapter titles (*Translation to ASL*, *Review List*, *Quotas and Cast Changes*, *Showcase*).

Closed scratch maps and tickets (`.scratch/regia-guide/`, `.scratch/showcase-1-5/`, `.scratch/regia-revision/`) are history and keep their citations. Done when the old files are gone and nothing outside `.scratch/` links to them.

## Resolution

Done. `git rm` of the 21 old chapters (`docs/guide/0 - Introduction.md` … `20 - Review List.md`) and `docs/guide/showcase/` (15 files); `docs/guide/` now holds only `01`–`25` and `README.md`. The last commit with them is `c30d1d4`.

Re-pointed outside `.scratch/`:

- `docs/showcase/README.md`: "replaces the 2.0 showcase in `docs/guide/showcase/`, which is kept as it was" → "replaces the 2.0 showcase that lived in `docs/guide/showcase/` until commit `c30d1d4`".
- ADRs 0037, 0038, 0039 cited Review List items (N12, F10, D1): now "(the old guide's Review List, <item>, at commit `c30d1d4`)". The ADRs' text is otherwise untouched.

Nothing else in `docs/` (spec, primer, new guide), `GLOSSARY.md` or `CLAUDE.md` cited the old files or titles. Closed scratch maps keep their citations. No findings.
