# Consistency pass across the guide

Type: task
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 30

## Question

Read `docs/guide/README.md` and `01`–`25` as one book, and fix what drifted between chapters written in parallel:

- terms against `GLOSSARY.md` (its *Avoid* lists included) and chapter titles as cited in *How this combines with…* and in prose (each must match an existing chapter's `#` title, in italics);
- every snippet with a showcase link still verbatim against `docs/showcase/` (outer indentation stripped);
- the template in the map's Notes: *Checks* format (`misuse → code (tag)`), `Spec:` as the last line of every section, "In 2.0" blockquotes, no codes in prose, no bold bullet leads;
- the showcase `README.md`'s `Guide:` lines point at chapters that exist and cover that spec chapter;
- a code given different tags or meanings in two chapters.

Fix the guide where it is wrong. Where two chapters disagree because the spec is unclear, add a line to `findings.md` and make both chapters say what the spec says. Done when a re-read finds nothing left and a grep for retired spellings across `docs/guide/[0-9][0-9]-*.md` and `README.md` is clean.

## Resolution

Done on 2026-11-23. The pass was scripted where it could be (the scripts lived in the session's scratchpad) and read by hand where a script flagged something.

- Snippets: every snippet under a showcase link is verbatim against `docs/showcase/` (outer indentation stripped). Unlinked blocks are either continuations of the file linked above them, also verbatim, or throwaways and variations that say so. The one-line forms in *Syntax* match their Plans.
- Template: `Spec:` closes every `##` section except *How this combines with…*, which closes no section in any chapter, the sample included, so that is the template. Fixed: an "In 2.0" sentence inside a `Spec:` line (*When an Agent leaves*, now a blockquote); two *Checks* bullets with no `→` (*Matching*, *Interfaces*); bold defined terms in *Interfaces* and *Precedence and Labels*; Trace codes in the prose of *When an Agent leaves* and one `R2008` in *The Visual Editor*. Kept: codes in the prose of *The Trace*, *The Transpiler* and the Jason chapters, where the code is what a component writes or prints; `#@allow: R1305` (*Precedence and Labels*), which is source text; codes in `Spec:` lines; inline 2.0 headers in "In 2.0" notes, which name the construct and are not code blocks.
- Codes: no code has two meanings across chapters. Missing tags added (*Goals and Failure*'s list of Failure causes, `T1503` in *Messages* and *Jason: Plans and Goals*, `T1902` and `T1601` in *Instancing*). Every `R` code's error/warning tag matches its spec chapter, and every `T` code's Failure/warning tag matches chapter 34, except `R2016` (one finding).
- Citations: every chapter title cited exists; section citations use the heading's text before its `:` (*Naming a value*, *Tied Playbooks*), which is the convention throughout. Fixed *Deleting* → *Deleting, and Extents*.
- Glossary: no *Avoid* term is used in the sense it forbids, except "loop" for `FOR EACH` (*Matching*, *Actions and time*, fixed) and "the vocabulary" (*Vocabulary and files*, fixed). "Story" is plain English, as in the spec; "namespace" is the spec's word for names, not External names.
- Showcase `README.md`: its `Guide:` lines agree with the guide index's spec-chapter column, heading for heading.
- Guide `README.md`: the table of where each "In 2.0" note sits listed only some chapters. It now lists every language chapter that has one.
- A real disagreement: *The Trace*'s `no_seat` case said `WHEN take_seat FAILED` and `ENDED` run unordered. Chapters 05 and 40 run the `ENDED` Plan after the `FAILED` one has finished, and *Goals and Failure* agrees. The case now finishes `stand_by` with `> action done stand_by(*)` before the Director can hear `took_seat`.
- Retired spellings: the grep across `docs/guide/[0-9][0-9]-*.md` and `README.md` finds them only in *Checks* lists and the *Retired spellings* section of *Syntax*.
- One non-blocking finding: chapter 20 files `R2016` under warnings, against its own prose and chapter 01.
