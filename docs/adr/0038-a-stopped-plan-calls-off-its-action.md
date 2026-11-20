# A stopped Plan calls off its Action

When a Plan was stopped while it waited in `DO a` (its Goal dropped, its Playbook taken away, its Phase left, its Staging ended, its Agent gone), the game was not told, and the Action carried on. The Guest whose `have_dinner` is dropped during `DO eat(roast)` goes on eating (Review List, F10). The writer can't fix this alone: the `DROPPED` or `UNASSIGNED` Plan that would clean up doesn't know which Action, if any, was under way, and a Playbook taken away by its Plot has no say in when that happens.

We decided that the Target tells the game to call the Action off, with `regia_action_cancel {id}` in the Jason Target (`docs/spec/37-jason-game-protocol.md`). The game decides what calling off means for each Action, as it already decides what "done" means, and the `ACTION` doc comment records it. There is no reply, and the Trace writes `DO a CANCELLED`. Only a waiting `DO` is called off: an Action started `WITHOUT WAITING` was set loose, as a Goal started `WITHOUT WAITING` is not dropped.

## Considered options

- **Keep it, and let the writer clean up in `DROPPED`**: the writer can't know which Action was running, and would have to mirror every Action with a Fact to find out. The language knows; the writer can't avoid the gap.
- **A word on the `ACTION` declaration for Actions that can be called off**: every Action can be told; what it does is the game's, as with refusing. A declaration word would only repeat the doc comment.
- **A reply (`cancelled`, or the Action's real outcome)**: no Plan is left to hear it. A reply the game sends anyway is dropped.
- **Also call off `WITHOUT WAITING` Actions when the Plan that started them stops**: that undoes the meaning of setting something loose.

## Consequences

- The game protocol has a message from the body after an Action is sent. A game that ignores it behaves as before.
- `regia-jason` must see a waiting `regia.act` intention being dropped, through a circumstance listener. A Director's cancel goes out on the game link like any other Action message (ADR 0040; it was first relayed by the Root).
- A Plot that takes a Playbook away, leaves a Phase or ends now stops what the Agents were doing for it. This is the Plot's nudge; inside a Playbook, the Agent still decides what it does.
- In Regia 1.5.
