# Messages for the whole run

Type: grilling
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by:

## Question

Some game messages are about the whole Program, not one Plot's Facts and Cues: `regia_join`, `regia_leave`, `regia_pause`, `regia_resume`, and the end of the story the Root sends (chapters 33 and 37). Today each comes to the Root Director's body. Decide where each goes once Directors are attached to one game link, by the test of "decentralised" in the map's Notes:

- `regia_join`: stays the Root's (only the Root Plot gains Agents), or not;
- `regia_leave`: delivered by the link to every attached Director, each running its own leave walk if the Agent is in its cast, or still walked down the Staging tree, pruned by cast (chapter 33, *Passing a leave down*); and who kills the agent, when;
- `regia_pause`/`regia_resume`: straight to the shared clock, with no Director in between;
- the end of the story: still sent by the Root when the Root Staging ends.

Also **audit Subplot–cast messaging** against the same test: the cast copy, Givings, `TELL`/`ASK`, Signals to the Director of a Giving, `EVERYONE`, and the parent → child messages (`regia_start`, `regia_left`, `regia_end`, `regia_ended`). Name anything else that runs through a Director on another Staging's behalf. The parent–child messages that are about the Staging tree itself (starting and ending a child) stay.

Closes when chapters 33 and 37 are edited (and 30 or 31 if the audit finds anything).

## Comments

## Resolution

Decided with the user on 2026-11-19.

- **`regia_leave` goes to every attached Director.** Each runs its own leave walk, a no-op when A isn't in its cast. Step 4 ("pass it down") and the `regia_left` message are gone. The start race (A leaves between `START SUBPLOT` and the child attaching) is closed by **a Subplot reconciling its cast when it attaches**, dropping Agents that have already left the Program before `!regia_begin`. How attaching is ordered with `regia_start` belongs to *A Director hearing the game for itself*, since it is the same race as the Fact snapshot. Rejected: keeping the walk down the tree.
- **The link kills a leaver**, once it has handed the leave to the Directors, without waiting for their walks (sends after the kill are caught by `regia.send`, as before). `T3302` is the link's.
- **`regia_join` goes to the Root Director only**, which still spawns from its own `regia_kind` beliefs. Joining is the Root Staging gaining a cast member.
- **The Root is killed at the end of its walk** like any Director, after sending `regia_story_ended` through the link. After that, the link drops joins (`T3304`, no agent created) and still kills leavers. Rejected: keeping the Root alive and idle.
- **`regia_pause`/`regia_resume` go straight to the clock** through the link, which writes the `CLOCK` entries. `T3702` is about the link.
- **Audit.** The cast copy, Givings, `TELL`/`ASK`, Signals, `EVERYONE`, `regia_end_staging` and `regia_cast_left` already go directly between a Director and its own Agents, so they pass. `regia_start`, `regia_end` and `regia_ended` are the Staging tree's own business and stay. The only other failures are percept forwarding with its start snapshot (*A Director hearing the game for itself*) and the Action relay (*A Director doing its own Actions*).

Edited: chapter 33 (*What the game reports*, *Reports that make no sense*, *Joining*, *The leave walk*, *Every Director hears a leave* replacing *Passing a leave down*, *Clearing counts*, *Messages*, *Trace entries*, *Regia 1.5*, *Not decided here*), chapter 37 (envelope table, *Pausing*, *The end of the story*, additions, `T3702`, *Not decided here*), chapter 31 (*The walk* step 5, *An ending Director hears nothing*, *The Root Director's `END PLOT`*), chapter 28 (new *The game link* section), and one line each in chapters 12 and 36.
