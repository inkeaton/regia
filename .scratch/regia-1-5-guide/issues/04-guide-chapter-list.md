# The guide's chapter list

Type: prototype
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 02

## Question

Which chapters does the 1.5 guide have, in what order, and what does each cover? Draft an outline to react to: per chapter, its title, the spec chapters it draws on, the constructs it covers, and the showcase files it quotes most. Starting points: the old guide's 0–20, and the 1.5 cut (chapter 27's index), which drops Quotas, joining, `BY`, `FROM GAME`/`FROM ME` and hearing an asked Goal's ending.

Settled already: 1.5 only with "In 2.0" notes; chapters on *The Transpiler*, *The Visual Editor* and the translation to Jason/ASL stay in; no Review List and no showcase walkthrough chapter. Open: whether the Jason/ASL material is one chapter or several (chapters 28–40 are now much larger than when the old *Translation to ASL* was written), where the Trace and Interfaces go, whether `README.md`'s coverage table gets a column pointing at the guide, file naming (the old `<n> - <Title>.md` or otherwise), and which chapters can be written in parallel.

The outline is linked from the resolution; each chapter graduates into a writing ticket.

## Resolution

Done with the user on 2026-11-20 (prototype). The outline is [`prototypes/chapter-list-outline.md`](../prototypes/chapter-list-outline.md); the user took it as drafted.

- **26 files in five parts**: `README.md` (introduction and index) and *01 The logic of Regia*; the language (02–10: Syntax, Vocabulary and files, Plans, Placeholders and Expressions, Matching, Actions and time, Randomness, Goals and Failure, Messages); Plots and Directors (11–17: Playbooks and Roles, Plots and Directors, Subplots and Stagings, When an Agent leaves, Interfaces, Precedence and Labels, Instancing); the tools (18–20: The Trace, The Transpiler, The Visual Editor); the Jason Target (21–25: the Build, Plans and Goals, Givings and Precedence, Directors and Stagings, the game and the Trace).
- **Jason** is five chapters, each grouping two or three of spec 28–40.
- **Leaving** is its own chapter (14), which also carries the "In 2.0" note on Quota Triggers, since 1.5 has no chapter for them.
- **The Trace** (spec 34) is chapter 18, before *The Transpiler*; Jason's Trace (35) goes with the game protocol in 25.
- **File naming**: `docs/guide/NN-slug.md` like the spec, `README.md` as the introduction. The new files sit beside the old `<n> - <Title>.md` ones until the old guide is deleted.
- **The showcase's coverage**: no column; each writing ticket adds a `Guide:` line under the showcase `README.md`'s *Coverage* heading of every spec chapter it draws on.
- **Order**: *Messages* (10) is the sample of *The chapter template, fixed by a sample chapter*; then 02–25 in parallel (they cite each other by title only); then 01, then `README.md`.

New tickets: one writing ticket per chapter (06–30), all blocked by the template ticket; *Write guide chapter 01* is also blocked by 02–25, and *Write the guide's README* by all of them. No findings.
