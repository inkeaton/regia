# Continuous integration on GitHub

Type: task (implementation)
Status: draft
Assignee:
Blocked by: the first crates in `transpiler/crates/` (roadmap stage 1). Until a crate exists, there is nothing to build.

## Question

What shows that `main` builds and passes its checks somewhere other than the author's machine?

Set up GitHub Actions on `main` for the Transpiler. Requested by the user on 2026-11-25, as something for later.

## Starting point

- Run the checks listed in `CLAUDE.md`, *Development procedure*, step 5, from `transpiler/`. In CI, a warning fails the job.
- Branch `1.0` already has a workflow (`.scratch/artifact-tidy/issues/13-ci.md`) to take conventions from: actions pinned by commit, a read-only token, caches, and a failure if the tree isn't clean afterwards.
- CI has only tracked files: `docs/.dev/`, `references/` and `1.0/` aren't there, so no check may need them.

## To decide when it is taken up

- Which triggers: pushes to `main`, pull requests, or both, and whether to skip changes that touch only docs.
- Whether to pin a Rust toolchain, and which systems to build on (ADR 0010 promises one native binary per platform).
- When to add later jobs: the `wasm32-unknown-unknown` build once `regia-wasm` exists, the Conformance cases once there is a runner, and behaviour cases, which need a JDK and Jason.
- Whether to check links between documents.

## Done when

The workflow is on `main` and has run green. Pushing needs the user's go-ahead.
