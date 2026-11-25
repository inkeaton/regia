# Regia

A language for describing game Agents, its Transpiler (Rust, `transpiler/`)
and, later, its Visual Editor and Jason runtime. Regia **1.5** is built first
(ADR 0025); the 1.0 paper artifact is on branch `1.0`.

## Sources of truth

When two disagree, the higher one wins; report the disagreement.

| Source | Decides |
|---|---|
| `docs/spec/` | What Regia means (01–21, 26, 38), how the tools are built (22–25), Conformance (27, 34), the Jason Target (28–33, 35–37, 39–40). Each chapter's `## Regia 1.5` section gives the cut |
| `docs/adr/` | Why a decision was taken |
| `GLOSSARY.md` | Every term, and the synonyms to avoid |
| `docs/guide/`, `docs/showcase/` | The 1.5 reference for tool builders, and the example Program, both derived from the spec |
| `docs/primer/` | Frozen and superseded: read for history only |

Jason and VEsNA-Pro behavior: read the source in `references/` (local) first.
Changes VEsNA-Pro needs: `.scratch/implementation/vesna-pro-for-regia.md`.

## Standards

- Before writing or reviewing code or comments, read `CODING_STANDARDS.md`.
- Before writing or reviewing project documentation, read
  `docs/standards/docs.md`.

## Development procedure

1. **Ticket.** Work is tracked as local Markdown:
   `.scratch/<effort>/map.md` and `.scratch/<effort>/issues/NN-<slug>.md`,
   with `Type:`, `Status:`, `Assignee:` and `Blocked by:` lines. The frontier
   is the open, unblocked, unclaimed tickets, lowest number first. Transpiler
   tickets are cut small: one construct, check or pass each.
2. **Read** the spec chapter the ticket implements, and its 1.5 section. An
   unclear or wrong spec is settled with the user and edited there first.
3. **Test first.** A language rule starts as a failing Conformance case in
   `docs/spec/cases/` (format: chapter 27). The spec owns the cases: code is
   changed to satisfy a case, and a disagreement with a case is a spec change.
   ASL snapshots belong to the Transpiler's own tests.
4. **Implement** inside the architecture of chapter 23.
5. **Check**, from `transpiler/`, all clean:
   `cargo fmt --check`, `cargo clippy --workspace --all-targets`,
   `cargo test --workspace`,
   `cargo doc --workspace --no-deps --document-private-items`.
6. **Document** in the same change: the docs that describe what changed,
   `GLOSSARY.md` for a new term, an ADR for a decision that is hard to
   reverse, surprising and a real trade-off.
7. **Review** against `CODING_STANDARDS.md` and the spec, then resolve the
   ticket. The user decides when to commit.
