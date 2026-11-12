# Write: Messages

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/9 - Messages.md`.

Covers: `TELL`, `ASK`, `SIGNAL`, Recipients, Senders and `FROM`, what a Message becomes for its receiver.

Sources: 07; ADR 0005, 0009.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-12: [`docs/guide/9 - Messages.md`](../../../docs/guide/9%20-%20Messages.md), about 3,300 words counting snippets, tables and the diagram, over eight sections (telling an Event, Recipients, who sent it, telling a Fact, asking for a Goal, Signals, what a Director sends, a conversation). Not yet read by the user.

- Every snippet with a path line is cut from the showcase, and the showcase Program is unchanged. Throwaway snippets cover what it lacks: `EVERYONE`, `LEARNED FROM`, a Quota Trigger in a Playbook.
- One diagram: the order between a Guest and a Servant, with both replies.
- Thirteen `#revise`. New ones: no way to write "from nobody" (`WHEN saw_pouring(?who):` can be set off by any Agent's `TELL`); no recipient between one Role and the whole game; `TELL` of a Fact and of an Event read the same; a told Fact can't be taken back; only the first teller of a Fact counts, so provenance means switching to an Event; where a Signal goes is not on its line, and one no Plan handles is dropped silently; a standing Giving and a one-off `ASK` to the same Role sit side by side; a conversation has no shape in the source; the `waiter`/`patron` relation is written in three places that nothing checks. Three repeat the README's notes (no "me", a Role recipient reaching every Servant, the insult outside `feast`).
- The `#revise` on `ASK` not waiting and on hand-written replies are in *Goals and Failure* and *Plans*; this chapter points at them.
- README: one spec-wording note (whether `FROM ?who` matches a Director) and one line under *Gaps in the showcase*.
- Checked by hand against spec chapters 05, 07, 08, 11, 15, 16, 18, 19 and 20, and ADR 0005 and 0009.
- Passed through `humanizer:humanizer`: two sentences reworded.
