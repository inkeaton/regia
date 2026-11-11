# Write: Introduction

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/0 - Introduction.md`.

Covers: What Regia is, the Transpiler and the Visual Editor in one paragraph each, how the guide is organised, the `#revise` and `#changes` tags, and the example world in brief.

Sources: glossary; map Notes.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-11: [`docs/guide/0 - Introduction.md`](../../../docs/guide/0%20-%20Introduction.md), about 1,400 words. Not yet read by the user.

- **Sections**: What Regia is; The Transpiler; The Visual Editor; How the guide is organised (a table of chapter groups); The two tags; The example world; Since 1.0.
- **Snippets**: `TO take_seat` from `showcase/playbooks/courtesy.regia` and `DURING arrival` from `showcase/plots/royal_banquet.regia`, both verbatim. Nothing was added to the showcase.
- **Diagram**: one mermaid flowchart, source to Transpiler to Build to Jason and the game, with Diagnostics and the Trace.
- **Departure from the template**: no *How this combines with…* part, since the Introduction covers no construct. The chapter says every other chapter has one.
- **Checked against**: the glossary; spec chapters 22 (text is the only thing stored), 23 (`regia check`, `regia build`, emit only without errors), 24 and 25 (Project, split view, Phase map, no manual layout), 34 (Trace); the showcase README for the world, the kinds and the small cast.
- **Review notes**: no `#revise` of its own and no showcase gap. The chapter names the `#revise` and `#changes` tags in inline code inside a bullet list; *Write: Review List* should collect only paragraphs that start with the tag.
- **For the consistency pass**: the chapter table uses the file titles (*Quotas and Cast Changes*), while *Matching* writes *Quotas and cast changes*. The Introduction also states the game side only as "the game"; VEsNA and Godot are left to *Translation to ASL*.
- Three `#changes` lines: the Transpiler in Rust and inside the editor; Story and Agent renamed Plot and Role; `#discuss` replaced by `#revise`.
