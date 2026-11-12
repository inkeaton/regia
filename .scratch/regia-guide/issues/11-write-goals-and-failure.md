# Write: Goals and Failure

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/8 - Goals and Failure.md`.

Covers: `PURSUE` (waits) and `DROP`, Goal recipes with `TO`, `DROPPED` and `FAILED` Triggers, `FAIL`, what fails and how Failure spreads, what is not undone.

Sources: 05, 11; ADR 0005, 0007.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/8 - Goals and Failure.md`](../../../docs/guide/8%20-%20Goals%20and%20Failure.md), about 3,800 words counting snippets, tables and the diagram, over nine sections (a Goal and its recipe, `PURSUE` waits, the same Goal twice, `DROP`, what fails a Plan, how Failure spreads, `FAIL`, `FAILED`, writing a fallback). The longest chapter so far: it carries two systems, and Failure touches every other chapter. Not yet read by the user.

- Snippets are cut from `vocabulary.regia`, `Courtesy`, `Serving`, `Dining` and `RoyalBanquet`; the showcase Program is unchanged. Two throwaway snippets: a `PURSUING` test and a fallback Goal pursued from a `FAILED` Plan. One sequence diagram follows the order of pie that fails in the Servant and, separately, in the Guest.
- Checked by hand against spec chapters 05, 07, 08, 10, 11, 12, 13, 16, 20, 29, 34 and 37, and ADR 0005 and 0007.
- Fifteen `#revise`:
  - no Trigger for a Goal being reached, so every recipe a Director depends on ends with a hand-made Signal;
  - `PURSUE` waits and `ASK … TO` doesn't, and the two lines look alike;
  - an ignored duplicate request loses its Sender;
  - Goal arguments used only to keep two pursuits apart (repeats the README's note);
  - a drop travels down as `DROPPED` and up as `FAILED`;
  - a Director can't call off a Goal it asked, and taking the Playbook away skips that Playbook's own `DROPPED` Plan;
  - a failed `WHEN` Plan can't be reacted to, only a failed Goal;
  - the missing-recipe warning is Program-wide, so an `ASK` to an Agent without the recipe fails silently;
  - `FROM` on a recipe makes the Agent's own `PURSUE` of that Goal fail at once;
  - `SIGNAL finished_eating.` written four times in `Dining`, since "over, however it went" has no Trigger;
  - the reason for a Failure can't be read, so `Serving` says `sold_out` for an unreachable seat;
  - `WHEN take_seat FAILED` has to send the Signal that means success;
  - replies to an `ASK` are written by hand;
  - a `FAILED` Plan may pursue the Goal that just failed, and loop;
  - `PURSUE` in a Role setup is the Director's `ASK` and never waits.
- One line added to the README's *Gaps in the showcase*.
- For the consistency pass: chapter 11 says "a cleanup Plan for a Goal always runs, however the Goal ended", while a reached Goal fires nothing and chapter 29 skips a taken-away Playbook's own `DROPPED` Plans. The chapter reports both as they are.
