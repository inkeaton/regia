# Readable generated ASL

Type: grilling
Status: open
Assignee:
Blocked by: none

## Question

Which recurring patterns of the generated ASL become named Infrastructure, and in which form?

Chapter 28, *Generated ASL is readable*, sets the rule (a generated plan reads like the designer's Plan; each Statement one step) and the three forms (rule, internal action, Infrastructure plan). Apply it pattern by pattern across chapters 29–40.

Candidates found in *Review: Model to Target*: the Givings guard `regia_given(p, _, _, _, _, _)` (a rule such as `regia_active(p)`); the `FROM` tests (`regia_holds(p, S, …)`, `S \== percept & S \== self`); `TELL Role` and `TELL n OF Role` (`.setof` + `regia.pick` + `for` + `regia.send`); `SIGNAL`; the four-step `-!g` of `goals.asl` (check what `regia.goal_failed` reads if part of it becomes a subgoal). Also the Director side (chapters 30, 31, 33).

Decide as well: whether a plan label should name its Trigger, as 1.0's `pb__NobleSocializing__insult_heard__0` did (now `regia_plan__<owner>__<n>`, chapter 28).

Work by hand: `courtesy.regia` and `serving.regia`, rewritten. Then bring the guide's hand-written ASL (`docs/guide/22`–`25`) to the result, labels included.

Blocks the M7 emit tickets, once they are cut. Chapters 28–40; references `references/` (Jason source) for subgoal and internal action costs.
