# Replace main's 1.0/ copy with a pointer to the branch

Type: task
Status: closed
Assignee: claude (session 2026-11-23)
Blocked by: 01

## Question

How does `main` refer to the paper artifact without keeping a second copy of it that drifts?

`main` tracks a full copy of the tree under `1.0/`. Remove it, and in `main`'s README add one line pointing to branch `1.0` (and the `artifact-submitted` tag). First check that nothing on `main` links into `1.0/`. This is the only ticket that commits to `main`. Leave the user's own uncommitted changes there untouched.

## Resolution (2026-11-23)

Done. `main` is now at **`20a59c9` "Replace the 1.0/ copy with a pointer to branch 1.0"** (anonymous, no trailer, **not pushed**). It untracks the 964 files under `1.0/`, adds a root `README.md` (there was none) that points to branch `1.0` and the `artifact-submitted` tag, and adds `/1.0/` to `.gitignore`. The user's uncommitted docs edits on `main` weren't touched.

Nothing on `main` linked into `1.0/`. But the regia-2 map's Notes (`.scratch/regia-2/map.md:55`) and some earlier research notes use local `1.0/` paths as reference material. So, with the user's agreement, **`1.0/` is now a git worktree of branch `1.0`**. The paths still resolve, and they show the tidied branch.

### Facts for later tickets

- **Commit on `1.0` from inside `~/Progetti/PhD/regia/1.0/`.** The branch is checked out there, so `git worktree add … 1.0` elsewhere fails. Its working tree is the branch, so check `git -C 1.0 status` is clean before starting.
- `git log 1.0` from the main checkout is still ambiguous, because the directory exists on disk. Use `refs/heads/1.0`, or `--`.
