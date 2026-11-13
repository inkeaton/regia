# Write: Translation to ASL

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18

## Task

Write `docs/guide/18 - Translation to ASL.md`: every construct next to the ASL it becomes, in the guide's own order (a Plan, a Placeholder, a Pick, a Random choice, a Goal, a Message, a Giving, a Phase, a Subplot, a Quota, a cast change, Precedence, Instancing and the `.jcm`), then the Infrastructure and the game protocol in brief, ending with the whole Build of a cut-down showcase.

Sources: 28–37; ADR 0013, 0014; `docs/primer/examples/*.asl` for the 1.0 shape.

The longest chapter: expect two sessions. Blocked by the language chapters because it reuses their examples.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-13, in one session: [`docs/guide/18 - Translation to ASL.md`](../../../docs/guide/18%20-%20Translation%20to%20ASL.md), about 8,200 words counting snippets, tables and two diagrams, over sixteen sections (the files and the names, a Plan, a Placeholder, a Pick, a Random choice, a Goal, a Message, a Giving, a Phase, a Subplot, a Quota Trigger, a cast change, Precedence and Labels, Instancing and the `.jcm`, the Infrastructure and the game, a whole Build). Every line of ASL is put together by hand, and the chapter says so. Where the spec gives a step only in words, the snippet has a comment in its place. The whole Build is of a throwaway cut of the banquet (one Playbook, one Plot with two Phases, three Agents), printed in full except for the two Infrastructure files and the source map. The showcase Program is unchanged. Not yet read by the user.

The main finding is about the showcase and not the chapter: it doesn't build on Jason. Its five External names of Facts and Events are dotted, which chapter 28 makes an error (`R2801`). The chapter reads them with `_` for each dot. The showcase was left as it is because three earlier chapters quote the dotted lines and *The Transpiler* shows the Program building; this is in the README's *Gaps in the showcase* and in the map's consistency pass.

The second finding is about the spec: no chapter holds the translation of a Plan. Chapters 28 to 37 decide the Infrastructure in detail, and the Statements have only the *ASL mapping notes* of chapters 06 to 26, some still open (told Events, a joined pursuit, `DROPPED`, `FAILED` under `selectOption`, `for`).

Seven `#revise`:
- Dotted External names are invited for Facts and Events by the language and refused by the only Target.
- A dot in an Action's External name decides whether the game or a Java class carries it out, and `seize` was meant for the game.
- `Host` and `host` need a Mapping in the source and are written alike in the Build.
- `ASSIGN Keeping_watch TO ?winner` puts the Playbook in every Role file, because the source can't say that `?winner` is a Guest.
- The plans of a Playbook that isn't given are still tested for every event they name.
- A Duration is wall-clock time, so a duel can be abandoned while the game is paused.
- A Plan that is stopped doesn't stop its Action in the game.

Seven entries were added to the README's *Spec wording* and one to *Gaps in the showcase*.
