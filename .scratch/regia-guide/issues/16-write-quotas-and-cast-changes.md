# Write: Quotas and Cast Changes

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/13 - Quotas and Cast Changes.md`.

Covers: Quota Triggers (`FROM ALL`, `FROM n OF`, `FROM n PERCENT OF`), Joining and Leaving and what each does to Casts, Givings and Quota counts.

Sources: 18, 19.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/13 - Quotas and Cast Changes.md`](../../../docs/guide/13%20-%20Quotas%20and%20Cast%20Changes.md), about 4,100 words counting snippets, tables and the diagram, over nine sections (a Quota Trigger, the three quantities, counting per argument, when a count starts, fires and ends, Joining, Leaving, what the Director hears, what a cast change does to a count). Standing Givings are left to *Playbooks and Roles* and the `JOINED` Plan that beats `DURING PLOT`'s to *Plots and Directors*. Not yet read by the user.

- The showcase Program is unchanged. `LEFT`, a Quota in a Playbook, and a plain Trigger beside a Quota on one Event are shown with throwaway snippets, and listed under *Gaps in the showcase*.
- Seventeen `#revise`. The ones that came from reading the two systems together: a latecomer raises the bar of `finished_eating FROM 75 PERCENT OF Guest` without ever having been asked for `have_dinner`, so a few latecomers can keep the feast from ending; a Quota can fire on a departure, with no Event arriving; a latecomer in `farewell` is sent to its seat by the setup and to the door by the `JOINED` Plan. On Quotas alone: `PERCENT` rounds up in a Trigger and down in a Mapping, the quantity is a literal while a Mapping's is an Expression, `3 OF` can be unreachable in a small cast with no warning, `ALL` of an empty Role never fires, a Quota fires again every time the count refills, and a Quota met while no `GIVEN` holds spends its whole count silently. On cast changes: a Director can't count its Roles (`EMPTIED` covers one case), `?who` from `LEFT` compiles as a recipient and is dropped at run time, and Agents never hear of a cast change.
- Three entries added to the README's *Spec wording*: the order of a leave between Stagings and after an `END PLOT`, rules stated only in the Jason chapters (`ON` covering Quota Triggers, Joining after the Root Plot has ended), and what fills a Quota's Placeholders when a departure completes it.
- Every example was re-read against spec chapters 18 and 19, with 05, 13, 15, 16, 20, 21, 33 and 34 for the parts they own. `humanizer` was run as the last pass.
