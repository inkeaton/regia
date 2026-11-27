# Jason: the game and the Trace

A Guest walks to its seat. In the Program that is one line, `DO walk_to(?place)`. On Jason it is a JSON message from the Agent's body to the game, one or two replies, a suspended intention woken again, and two lines in the Trace. This chapter covers the messages between a Jason Build and the game, and then how the Build writes the Trace: one writer, a source map back to our names, a file per run, the console, and the stand-in game that runs behaviour cases.

| Who talks | Over | What goes across |
|---|---|---|
| an Agent and the game | the Agent's VEsNA body, one connection each | the game's Cues and Facts to the Agent; the Agent's Actions and their replies |
| the Directors and the game | the game link, one connection shared by all | the game's Cues and Facts, each Director's state request, Actions and replies, leaves, pausing, the end of the story |
| any agent and the Trace | the Trace writer, inside the run | every entry, to the file and to the console |

No Transpiler exists yet, so every message and every line of the source map below was put together by hand from the spec. We don't read these messages in our daily work: whoever writes the Jason Target, or the game's side of the protocol, does. The files and ports are in *Jason: the Build*; how a Director hears the game and attaches is in *Jason: Directors and Stagings*; the Trace's entries and the `.trace` format are in *The Trace*.

## The envelope

```json
{"sender": "body", "receiver": "noble_1", "type": "regia_cue",
 "data": {"name": "hall.clock.idle", "args": []}}
```

Every message between Regia and the game uses VEsNA's JSON envelope: `sender`, `receiver`, `type` and `data`. Regia adds its own types:

| Type | From → to | `data` |
|---|---|---|
| `regia_cue` | game → body or game link | `{"name", "args"}` |
| `regia_fact` | game → body or game link | `{"op": "add" \| "remove", "name", "args"}` |
| `regia_action` | body or game link → game | `{"id", "name", "args"}` |
| `regia_action_result` | game → body or game link | `{"id", "status", "reason"?}` |
| `regia_action_cancel` | body or game link → game | `{"id"}` |
| `regia_state` | game link → game, for a Director that attaches | `{"id", "facts", "agents"}` |
| `regia_state_result` | game → game link, for that Director | `{"id", "facts", "left"}` |
| `regia_leave` | game → game link, for every attached Director | `{"name"}` |
| `regia_join` | game → game link, for the Root Director | `{"kind", "name", "port"}` |
| `regia_pause`, `regia_resume` | game → game link | `{}` |
| `regia_story_ended` | game link → game, for the Root Director | `{"outcome"}` |

- An Agent's messages travel on its own body. Every Director's travel on the game link, whose name on the wire is `regia_game_link`: the game writes it as `receiver`, and the link writes it as `sender` for whichever Director it sends. The game never learns that Directors or Stagings exist.
- `name` is always the External name: `hall.clock.idle`, not `idle`. `regia-jason` translates it both ways.
- `args` is a JSON array, encoded the same way in every type and both directions: a Number is a JSON number, a name or an Agent's name a JSON string, a list a JSON array. The game never parses Jason terms.
- In 1.5 nobody joins. The Root Director ignores every `regia_join` and writes `T1902` (*Jason: the Build*, *Agent kinds*).
- VEsNA's own types (`signal`, `sight`, …) pass through as before. On the game link, a type the link doesn't know is ignored with a warning.

**Checks**

- A message of an unknown type on the game link → `T3702` (Trace warning)
- A spawn reported during a 1.5 run → `T1902` (Trace warning)

Spec: chapter 37, *The envelope*, *Arguments*.

## A game Action

[`playbooks/courtesy.regia`](../showcase/playbooks/courtesy.regia)
```regia
TO take_seat, FROM DIRECTOR:
    GIVEN seat(?place):
        DO walk_to(?place)               # waits until we have arrived
        DO sit_down
        TELL host greeting
    # no ELSE: with no seat laid for us, take_seat fails at once
```

```asl
regia.act("walk_to", walk_to(Place));
```

`walk_to`'s External name has no dot, so it is a game Action. `regia.act` takes the External name, then the Action under our name, so the Trace and the mind inspector show ours. It sends `regia_action` through the Agent's body and suspends the intention until the reply it needs arrives:

```json
{"sender": "noble_1", "receiver": "body", "type": "regia_action",
 "data": {"id": 7, "name": "walk_to", "args": ["seat_3"]}}
```

```json
{"sender": "body", "receiver": "noble_1", "type": "regia_action_result",
 "data": {"id": 7, "status": "done"}}
```

- `id` is a whole number from a counter each body keeps, starting at 1. Each reply names the `id` it answers.
- Only that intention waits. The Agent's other Plans go on: a `WHEN greeting` can bow to someone while the Guest is still walking.
- `regia.act` sends through `VesnaAgent.perform`, which is public. Nothing changes in VEsNA-Pro.

### The replies

| `status` | Means | Final? |
|---|---|---|
| `accepted` | the game has started the Action | no |
| `refused` | the game couldn't start it: an unknown Action, a missing target, a character that can't act | yes |
| `done` | the Action is finished | yes |
| `failed` | it was started and couldn't be finished | yes |

- A `done` or `failed` with no `accepted` before it implies acceptance. An instant Action needs one reply, `done`.
- What `done` means is the game's choice for each Action, and the `ACTION` doc comment records it: `walk_to` is done when the Agent has arrived.
- `reason` is an optional string. It goes into the Trace and never reaches the Program.
- A reply under an `id` the body doesn't know, or after that `id`'s final reply, is ignored with a warning.

How long the Statement waits depends on how it is written:

| We write | Goes on at | Fails the Plan on |
|---|---|---|
| `DO walk_to(?place)` | the final reply | `refused`, `failed` |
| `DO pour_poison(?mark), WITHOUT WAITING` | `accepted`, or a final reply | `refused` |

- A `failed` that comes after a `WITHOUT WAITING` Body has moved on fails nothing. It is written in the Trace.
- Nothing times out. A game that never answers leaves a waiting `DO` waiting until its Plan is stopped, and then the Action is called off.
- An Agent with no body connected, because it never connected or the connection dropped, sends nothing: `regia.act` fails at once, as if refused, with the reason `no body`.
- An Agent's body that drops with an Action in flight sends no reply, so a waiting `DO` waits until its Plan is stopped. The spec leaves this case open for Agents. A Director's Actions fail on a lost link (*A Director's Actions*, below).

**Checks**

- A `DO` refused, or a waiting `DO` reported as failed, or an Agent with no body → `T1101` (Trace, Failure)
- A `regia_action_result` with an unknown `id`, or after the final reply → `T3701` (Trace warning)

Spec: chapter 37, *Sending*, *The game's replies*, *Waiting*. For the Failure, chapter 11.

### Calling an Action off

[`playbooks/dining.regia`](../showcase/playbooks/dining.regia)
```regia
WHEN hungry FORGOTTEN:
    DROP have_dinner                     # stops the recipe, even while it waits
```

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
#@desc: Done when the dish is eaten. Called off, the Agent puts down what is left.
ACTION eat(dish)
```

The game forgets `hungry` while a Guest is in the middle of `DO eat(roast)`. `DROP have_dinner` drops the intention that waits in `regia.act`, and the body tells the game:

```json
{"sender": "noble_1", "receiver": "body", "type": "regia_action_cancel",
 "data": {"id": 12}}
```

- `regia.act` keeps the suspended intention of each waiting Action, and a Jason circumstance listener sees it dropped: a Goal dropped, a Phase's intentions dropped, a Playbook taken away, a Staging ended, an Agent gone.
- The cancel has no reply. Anything the game sends later under that `id` is dropped silently, with no `T3701`.
- What calling off means is the game's choice, as `done` is. The Guest puts down its fork.
- Only a waiting `DO` is called off. One started `WITHOUT WAITING` was set loose and runs to its end. A Plan that fails never has an Action under way.

Spec: chapter 37, *A Plan that stops while waiting*. For what stops a Plan, chapter 08.

### The Target's own code

[`playbooks/hosting.regia`](../showcase/playbooks/hosting.regia)
```regia
TO open_feast, FROM DIRECTOR:
    DO stand_up
    DO play_fanfare                      # the Target's own code: Regia doesn't wait on the game
    DO raise_cup
```

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
#@desc: The Target's own code, not the game's: done when that code returns.
ACTION hall.music.fanfare AS play_fanfare
```

```asl
regia.act("hall.music.fanfare", play_fanfare);
```

A dotted External name is a Java class. `regia.act` sees the dot and sends nothing: no body, no game link and no `id`. It finds the class through Jason's internal-action table, `Agent.getIA`, and runs it in the agent, at once, with the Action's arguments.

- It is done when the code returns `true`. It fails when the code returns `false` or throws, with the exception's message as the reason, and the Plan fails as for a game Action.
- A class that isn't on the class path fails the same way, with the reason `no Java class hall.music.fanfare`. Nothing checks for it before the run: the class lives in a jar of the Project's `lib/`, which `regia check` and `regia build` never read.
- `WITHOUT WAITING` changes nothing, and a dotted Action can't be called off: the code has returned before the next Statement either way.

VEsNA-Pro's own internal actions, `vesna.walk` and the like, are outside Regia. They report completion through VEsNA's `signal` messages, which Regia never reads. `ACTION vesna.walk AS walk` builds, since a dotted name may be the Project's own class, but its waiting and failure aren't Regia's. A Regia game offers movement as a game Action, `walk_to`.

**Checks**

- A dotted Action whose class is missing, returns `false` or throws → `T1101` (Trace, Failure)

Spec: chapter 37, *The Target's own code*, *VEsNA-Pro's own actions*. For the `lib/` folder, chapter 28.

### Actions in the Trace

```
#38 DO walk_to(seat_3)
…
#57 DO walk_to(seat_3) DONE
```

Every `DO` writes two `action` entries, for a game Action and a dotted one alike: one when it is sent, one for its outcome.

| When | Console line |
|---|---|
| the Action is sent | `DO <action>` |
| its final reply arrives | `DO <action> DONE`, `FAILED` or `REFUSED`, with the reason when there is one |
| its Plan stops while it waits | `DO <action> CANCELLED` |

- The outcome entry has `of`, the `seq` of the sent entry.
- `accepted` writes nothing. A sent entry with no outcome says the game never finished the Action, or never saw it.
- An Action started `WITHOUT WAITING` gets its outcome entry when the reply comes, after its Body has moved on.
- A `no body` refusal writes both entries at once.
- A `FAILED` or `REFUSED` that fails a waiting Plan is followed by the failure chain (*The Trace*).
- `regia.act` writes the sent entry, and the reply intake of the agent class writes the outcome. Generated ASL writes neither.

Spec: chapter 37, *The Trace*. For the `action` entry's fields, chapter 34.

## Game messages in an Agent

[`vocabulary.regia`](../showcase/vocabulary.regia)
```regia
#@desc: The seat the game has laid for this Agent. Servants and Guards have none.
GAME FACT hall.seating.seat AS seat(place)
```

[`playbooks/keeping_watch.regia`](../showcase/playbooks/keeping_watch.regia)
```regia
WHEN saw_pouring(?who):
    DO seize(?who)
    SIGNAL culprit_seized(?who)          # reaches every Director that gave us this Playbook
```

```json
{"sender": "body", "receiver": "noble_1", "type": "regia_fact",
 "data": {"op": "add", "name": "hall.seating.seat", "args": ["seat_3"]}}
```

```json
{"sender": "body", "receiver": "knight_1", "type": "regia_cue",
 "data": {"name": "hall.senses.saw_pouring", "args": ["noble_5"]}}
```

`regia.RegiaAgent` extends VEsNA-Pro's `VesnaAgent`, which passes every message from the body to its public `myHandleMsg`. `RegiaAgent` overrides it:

| Type | Becomes |
|---|---|
| `regia_cue` | the event `+saw_pouring(noble_5)[source(percept)]`, of Jason's `signal` type: no belief is kept |
| `regia_fact`, `add` | the belief `+seat(seat_3)[source(percept)]` |
| `regia_fact`, `remove` | `seat(seat_3)` removed with every source, so a Fact the Agent was also told goes too |
| `regia_action_result` | the intention waiting in `regia.act` resumes |
| anything else | `super.myHandleMsg`, so VEsNA works as before |

- The External name is translated first, through the receiver's `regia_game` beliefs (*Jason: the Build*, *External names*). `noble_5`, a JSON string, becomes an atom.
- A name with no `regia_game` entry is dropped with a warning: it isn't a game item, or this Agent never uses it.
- `source(percept)` is what keeps a game Cue apart from a told one: a told Cue carries its Sender as `source`, so `FROM` can test it. A game Cue matches only a Trigger with no `FROM`.
- A told Cue is the same kind of event as a game Cue, so `WHEN saw_pouring(?who):` would also run if another Agent told a Guard `saw_pouring(…)` (*Messages*, *Who sent it*).

**Checks**

- A `regia_cue` or `regia_fact` whose name has no `regia_game` entry in the receiving Agent → `T2801` (Trace warning)

Spec: chapter 37, *Game messages in an Agent*. For the message types, chapter 30, *What the game sends*.

## Game messages on the game link

[`plots/poisoning.regia`](../showcase/plots/poisoning.regia)
```regia
WHEN poison_drunk:                   # a game Cue, straight to the Director
    END PLOT WITH poison_taken
```

```json
{"sender": "body", "receiver": "regia_game_link", "type": "regia_cue",
 "data": {"name": "hall.table.poison_drunk", "args": []}}
```

No Director has a body. The game link reads everything the game sends on its connection and either handles it or hands it to the Directors that should have it:

| Type | The link |
|---|---|
| `regia_cue`, `regia_fact` | delivers it to every attached Director whose Plot hears the item; drops it with no entry if none does |
| `regia_state_result` | delivers it to the Director that asked |
| `regia_action_result` | delivers it to the Director that sent the Action |
| `regia_leave` | delivers it to every attached Director |
| `regia_join` | delivers it to the Root Director |
| `regia_pause`, `regia_resume` | stops or starts the clock itself |
| anything else | ignores it, with a warning |

The game sends `poison_drunk` once, with no receiver but the link. While the poisoning runs, `director:Poisoning#1` hears it and ends. Before it starts, no attached Director hears `poison_drunk`, and the Cue is dropped. A Director takes in what the link delivers through `regia.DirectorAgent`'s own intake, which runs the same code as an Agent's `myHandleMsg` (*Jason: Directors and Stagings*, *Hearing the game*).

Spec: chapter 37, *Game messages on the game link*. For routing, chapters 28 and 30.

### The game's starting state

A Director that attaches asks the game what is true for it now, under an `id` from the link's counter. `RoyalBanquet` names no game Fact, so the banquet's request asks for none:

```json
{"sender": "regia_game_link", "receiver": "body", "type": "regia_state",
 "data": {"id": 1, "facts": [], "agents": ["king", "percival", "hothead_1", …, "servant_3"]}}
```

```json
{"sender": "body", "receiver": "regia_game_link", "type": "regia_state_result",
 "data": {"id": 1, "facts": [], "left": []}}
```

A Plot that tested `GIVEN in_stock(pie)` would list `in_stock` in `facts`, and the reply would carry every instance true now, in `regia_fact`'s form: `{"name": "in_stock", "args": ["pie"]}`.

- `facts` are the External names of the Facts the Director's Plot hears. A Fact with no instance true is left out of the reply.
- `agents` are the Director's starting cast, and `left` names those that have already left the game.
- The game keeps no record of Stagings. Each request is a question about its own state.
- The game must answer every request, in order with everything else it sends: the reply describes the game when it is sent, and every change after it follows it. A game that never answers holds that Director unstarted.
- The first request is always the Root's. Once it has answered it, the game knows the story has begun, and only then may it send a `regia_join`.
- With no link, there is no request: the Director starts with no game Facts and nobody left.

**Checks**

- A `regia_state_result` with an unknown `id`, or a second one for the same `id` → `T3703` (Trace warning)

Spec: chapter 37, *The game's starting state*. For attaching, chapter 30.

### A Director's Actions

[`plots/poisoning.regia`](../showcase/plots/poisoning.regia)
```regia
WHEN EXITED, BY PARENT:              # the feast ended first
    DO discard_cup
```

```json
{"sender": "regia_game_link", "receiver": "body", "type": "regia_action",
 "data": {"id": 9, "name": "discard_cup", "args": []}}
```

A Director writes `DO` as an Agent does, and its `regia.act` hands the Action to the link. Every Director sends its own Actions this way, the Root included. None acts for another.

- The `id` comes from the link's one counter, the same one `regia_state` uses, so no two requests on the connection share an `id`. The link records which Director the `id` belongs to; the game never learns it.
- The link routes each reply by `id` alone, into that Director's mailbox, in socket order. A Fact the game sent before a `done` is a belief before the Plan's next Statement runs.
- A dropped intention calls the Action off as in an Agent: the link sends `regia_action_cancel` and forgets the `id`.
- A Director that stops hearing at the start of its ending still gets its Action replies until it detaches. `discard_cup` runs inside the poisoning's ending, after it has stopped hearing the game, and its reply still comes back.
- A Director that dies without its intentions being dropped has its waiting Actions called off by the link when it detaches, with `DO <action> CANCELLED` written under its name. Its `WITHOUT WAITING` Actions stay in flight, and the link writes their outcome entries under its name. The link never delivers such a reply to an agent, since Jason reuses a killed agent's name.
- A lost link fails every Director Action still in flight with the reason `no game link`, and every later one at once. A `DO` in an `EXITED` Plan no longer holds up its Staging's ending.

**Checks**

- A Director Action failed for `no game link`, or refused, or reported as failed while it waits → `T1101` (Trace, Failure)

Spec: chapter 37, *Custom Actions in a Director*. For a `DO` in `EXITED`, chapters 30 and 31.

## Pausing

```json
{"sender": "body", "receiver": "regia_game_link", "type": "regia_pause", "data": {}}
```

The game tells the game link when it pauses and when it resumes, and the link stops and starts the run's one clock. No Director is involved.

- Every `WAIT`, with or without `UNTIL`, and every `AFTER`, of every Agent and Director, is measured on that clock (*Jason: the Build*, *The clock*).
- Only Durations stop. Messages, Cues and Actions go on: a body still sending Cues while paused is the game's choice.
- A second `regia_pause`, or a `regia_resume` while running, does nothing.
- Each change writes a `time` entry, `CLOCK PAUSED` or `CLOCK RESUMED`, written by the link.
- A link that never connects, or is lost while the clock is stopped, starts the clock again and writes `CLOCK RESUMED`, since no resume can come any more.

Spec: chapter 37, *Pausing*. For Durations, chapter 12.

## The end of the story

[`plots/royal_banquet.regia`](../showcase/plots/royal_banquet.regia)
```regia
WHEN Guest EMPTIED:
    END PLOT
WHEN Host EMPTIED:
    END PLOT
```

```json
{"sender": "regia_game_link", "receiver": "body", "type": "regia_story_ended",
 "data": {"outcome": null}}
```

When the Root Staging ends, the Root Director tells the game, through the link, with the internal action `regia.end_story(O)`. It does so after the last `regia_ended` from its children and before it is killed (*Jason: Directors and Stagings*, *The Root's `END PLOT`*).

- `outcome` is the Root's Outcome as a JSON string, or `null` for an `END PLOT` with none, as the banquet's are.
- The game decides what to do with it, credits or a menu, and sends no reply.
- After it, no Director is left. The link still kills Agents the game reports as leaving, and still stops and starts the clock. Agents keep running on their own bodies, with no Givings.
- `regia.end_story` also ends the Trace: the writer writes `RUN ENDED`.

Spec: chapter 37, *The end of the story*. For the `run` entry, chapter 35.

## The Trace writer

```
[noble_1] #57 DO walk_to(seat_3) DONE  playbooks/courtesy.regia:11:13
[noble_1] #58 DO sit_down  playbooks/courtesy.regia:12:13
```

Every agent of a Jason run lives in one JVM, so every Trace entry goes through one writer, a shared object in `regia-jason`. It hands out `seq` in one order for the whole Program and writes each entry twice:

- to the Trace file, as one JSON object per line;
- to the console, as the entry's console line, through a logger named after the entry's `agent`. Lines show up under `[noble_1]`, `[director:RoyalBanquet]` or `[director:HonorDuel#2]`, never under a Generated name such as `regia_director__royalBanquet`. A `.print` a developer adds shows under the Jason agent's own name, mixed in with them.

Generated ASL reaches the writer through one internal action:

```asl
regia.trace(unheard, info, "T3801",
            [cue(insult_thrown(hothead_1)), sender(noble_4), plot(royalBanquet), phase(reception)])
```

- `regia.trace(Kind, Level, Code, Fields)`: `Code` is a string, `""` for an entry with none, and `Fields` a list of `key(Value)` terms with the field names of *The Trace*. Java callers pass the same keys.
- The writer adds `seq`, `t`, `agent`, `kind`, `level` and `code`. It writes atoms and structures as Regia text, lists as arrays and numbers as numbers, and turns every Generated name into ours through the source map (below).
- `at` comes from the caller's frame: the ASL file and line of the instruction running on the current intention, mapped back to `.regia`. An Infrastructure plan's frame isn't mapped, and gives no `at`.
- `regia.trace` never fails. A writer error, such as a full disk, is reported once on the console and the run goes on.

Most entries aren't written by generated ASL at all. The internal actions and the agent classes write their own:

| Kind | Written by |
|---|---|
| `run` | the writer: `RUN STARTED` at start-up; `RUN ENDED` at `regia.end_story`, or from a JVM shutdown hook, `how: stopped`, if the run is stopped first. In test mode, `RunCase` |
| `action` | `regia.act` when it sends; the reply intake of `RegiaAgent` and `DirectorAgent`; the game link for a detached Director's Actions and when it is lost |
| `message` | `regia.send`, which every send goes through |
| `plan` | `selectOption` of both agent classes, when they choose the option; the walker, `regia.stop_playbook` and `regia.pass_failure` for one stopped or failed |
| `goal` | `regia.trace` for a `PURSUE`, `RegiaAgent.socAcc`, `regia_reach`, `regia.goal_failed`, the drop walker |
| `fact` | `regia.trace` after each `LEARN`, `FORGET` and `UPDATE`; the plan that takes in a told Fact; the Java intake of a game Fact; `regia_begin`, for a Director's starting game Facts |
| `phase`, `staging`, `cast` | the Infrastructure plans that do these things |
| `giving` | the receiving Agent's `regia_give`, `regia_restore`, take steps and `regia_set_aside` |
| `failure` | the Statement that knows its cause, else the catcher |
| `warning`, `unheard` | wherever the spec names the code |
| `mood` | `regia.shift`, and `RegiaAgent.selectOption` for a `SHIFTS` Label |
| `time` | `regia.wait` when a `WAIT … UNTIL` ends; the game link for the clock |

- A Plan's `plan` entry is written when the agent class chooses it, not from its Body. Only `selectOption` sees the rivals, so `by`, `over` and `fits` are known there and nowhere else. `selectOption` writes one for every chosen option whose label is a designer's Block, contested or not. `values` is read from the option's unifier, through the plan's variable map in the source map.
- A `SHIFTS` Label's `mood` entries are written in the same call, after the `plan` entry they belong to.
- Generated helper plans write nothing of their own. `IF`, `RANDOMLY` and `FOR EACH` stay inside the Plan's body, so there are no control-flow plans to trace.
- A Failure's cause entry is written exactly once (*Jason: Plans and Goals*, *The cause entry*).

Spec: chapter 35, *The writer*, *The `plan` entry*. For each source, chapters 29–33, 37, 39 and 40.

### Staging numbers

```
[director:HonorDuel#2] STAGING HonorDuel(hothead_2) STARTED hothead_2 AS Defender, noble_3 AS Challenger, knight_1 AS Spectator ALSO IN #1, …
```

`#2` and `ALSO IN #1` exist only in the Trace. No agent reads them, and a Subplot Director's Jason name is unique but numbered by nothing. So the writer works them out from the entries it has already written, and from nothing else:

- When it writes a Director's first entry, its `STAGING … STARTED`, it gives that Director the next number for its Plot in this run, and names it `director:<Plot>#<n>` from then on, on the console too.
- For each Agent of the new cast, `also_in` lists the numbers of the Stagings of the same Plot whose `STARTED` entry names it, with no `ENDED` entry yet, and which it hasn't `LEFT`.

The writer holds no Program state.

Spec: chapter 35, *Staging numbers*. For the names, chapter 34.

## The source map

Jason reports where things happen in ASL. The Trace speaks in `.regia` locations and our names. Every Build holds `asl/regia/sourcemap.json`, written by the Transpiler, to get from one to the other. For `TO take_seat` it holds, among much else:

```json
{
  "lines": { "playbooks/Courtesy.asl": { "4": "playbooks/courtesy.regia:9:5",
                                          "8": "playbooks/courtesy.regia:11:13",
                                          "9": "playbooks/courtesy.regia:12:13" } },
  "names": { "regia_director__royalBanquet": "director:RoyalBanquet",
             "regia_local__courtesy__greeting": "greeting" },
  "plans": { "regia_plan__courtesy__1": { "owner": "Courtesy", "trigger": "TO take_seat, FROM DIRECTOR",
                                "given": "seat(?place)", "at": "playbooks/courtesy.regia:10:9",
                                "vars": { "Place": "?place" } } }
}
```

| Map | From | To |
|---|---|---|
| `lines` | an ASL file and a line that comes from a Statement or a Plan | the `.regia` file, line and column |
| `names` | every Generated name | the name it stands for, or `null` to fold it away |
| `plans` | the label of every plan of a designer's Block | the Block as a `plan` entry names it (`owner`, `trigger`, `given` or `else`), its `at`, and each ASL variable's Placeholder |

- The writer reads it once at start-up. Nothing in it changes during the run.
- Every entry's `at` and every name go through it, so the rule that the Trace never shows a Generated name is kept in one place, and the ASL carries no location annotations.
- A Subplot Director's name has no number in `names`. The writer adds it.
- `null` folds away frames that never show in the Trace, such as a generated helper.

The ASL line numbers above are made up for the example; the `.regia` locations are the showcase's.

Spec: chapter 35, *The source map*. For Generated names, chapter 28.

## The file and the console

```
build/banquet/traces/20261123-201544.jsonl
```

- Each run writes a new file, `traces/<YYYYMMDD-HHMMSS>.jsonl`, under the Build folder. Runs are kept, so two runs of one Build can be compared, and `regia build` never touches `traces/`.
- The path is printed on the console when the run starts.
- The file always gets every entry. Nothing turns it off.

`regia run --console <level>` filters the console and never the file. How much the console shows changes nothing in the run, so it isn't a Target setting and isn't in the Build: `regia run` passes it to the JVM as the system property `regia.trace_console`, which the writer reads at start-up.

| `--console` | The console shows |
|---|---|
| `all` (the default) | every entry |
| `warnings` | `warning` and `failure` entries only |
| `off` | nothing |

**Checks**

- A console level written as a Target setting → `R3501` (warning; retired: it is an option of `regia run`)

Spec: chapter 35, *The file*, *The console*. For `regia run`, chapter 23.

## Starting a run

```
regia run banquet.regin --seed 4127 --console warnings
```

`regia run` builds, then starts the MAS from the Build's `.jcm`:

- The class path is the `regia-jason` jar the command line carries, then every jar in the Project's `lib/`. Nobody writes a class path.
- The seed is `--seed`, else the Build's `SEED`, else one the run picks. It is given to `regia-jason` as the system property `regia.seed`, from which each agent seeds its own generator (*Random draws*, below), and the `run` entry records it: `RUN STARTED banquet.regin SEED 4127`.
- The console level goes in as `regia.trace_console`.
- The game connects as it always does: each body to its port, the link to `base_port`.

### Random draws

Jason gives every agent one random generator, shared by `.random` and `math.random`. When an agent starts, `regia.RegiaAgent` or `regia.DirectorAgent` seeds it from the run's seed and the agent's name. So a run with the same seed draws the same way, and one agent's draws don't depend on how the others are scheduled.

| What draws | How |
|---|---|
| a Random choice | the Infrastructure plan `regia_choose`, with `.random` |
| `RANDOM a TO b` | the rule `regia_roll(A, B, whole \| decimal, R)`, built on `math.random` |
| a `RANDOMLY` Pick | the rule `regia_random_match`, with `.random` on the Matches |
| a weighted Pick | `regia.weighted_pick(L, M)`, which takes the agent's generator from Java |
| every `n OF` and `n% OF` | the Infrastructure plan `regia_draw`, with `.random` |

- The Transpiler picks `whole` or `decimal` from how the bounds are written. A failed whole roll in a Body is `T0403`.
- `regia.RegiaAgent` draws `RANDOM` Propensity values from the same generator (*Jason: the Build*, *Drawing `RANDOM`*).
- Generated code never uses `.shuffle`, which draws from a source the seed doesn't reach. VEsNA-Pro's own choices use their own source; if one turns out to matter, it is a gap the Target's development closes.

**Checks**

- A whole roll with no whole number between its bounds, in a Body → `T0403` (Trace, Failure)

Spec: chapter 35, *Starting a run*, *Random draws*. For the seed, chapter 21; for why it is per agent, ADR 0050.

## Test mode

[`playbooks/courtesy.regia`](../showcase/playbooks/courtesy.regia)
```regia
WHEN take_seat FAILED:
    DO stand_by(wall)
```

```
java -cp regia-jason.jar:lib/*:… regia.testing.RunCase build/cases/no_seat/no_seat cases/no_seat/no_seat.trace
```

`regia test` runs each behaviour case through `RunCase`, a class of `regia-jason`'s `regia.testing` package, with the Project's `lib/` jars on the class path as `regia run` has them. A dotted Action runs the Project's Java for real in a case too. The case itself, the Guest with no seat, is in *The Trace*, *Behaviour cases*.

1. `RunCase` starts `ScriptedGame`, a WebSocket server on every address and port the `.jcm` gives. It speaks the game's envelope and types, and tells its connections apart by port, never by `sender`: the port of the `.jcm`'s `regia.GameLink` line is the link's, every other port is the body of the Agent the `.jcm` gives it. Under `#! game link: none` it doesn't serve the link's port, so the link writes `T2802` at start.
2. It starts the MAS from the Build's `.jcm`, in the same JVM, with Jason's synchronous execution control, so agents step in lockstep reasoning cycles, and with the case's seed, from which each agent seeds its generator. The bodies and the link connect to `ScriptedGame` as they would to the game.
3. For each `>` step, it waits for the run to settle, plays the step through `ScriptedGame`, and writes a `script` entry.
4. After the last step, once the run has settled, it writes `RUN ENDED`, stops the MAS and exits. The Trace file is its only output.

The Transpiler's Conformance suite, in Rust, does the matching: it builds the case, runs `RunCase`, reads the `.jsonl` and matches the expected lines against it. `RunCase` never reads them.

Spec: chapter 35, *Test mode*. For `regia test`, chapter 23; for the matching, chapter 34.

### Steps as messages

| Step | `ScriptedGame` sends |
|---|---|
| `> cue noble_2 idle` | one `regia_cue` on `noble_2`'s body, `receiver: "noble_2"` |
| `> fact noble_1 +hungry` | one `regia_fact`, `op: "add"`, on `noble_1`'s body |
| `> cue link poison_drunk` | one `regia_cue` on the link's connection, `receiver: "regia_game_link"` |
| `> cue * idle` | one message to each body that uses `idle`, in Trace order, then one on the link if any Director file lists it |
| `> leave noble_4` | `regia_leave` on the link |
| `> pause`, `> resume` | `regia_pause`, `regia_resume` on the link |
| `> lose link` | nothing: it closes the link's connection from its side |

- The step names our item. `ScriptedGame` sends its External name, read from the receiver's `regia_game` beliefs, or for the link from those of the Build's Director files, Subplots' included. A receiver with no entry for it gets our name as it is, and an Agent writes `T2801`.
- A `*` step sends all its messages before the run is next checked for settling. Its `script` entry lists the receivers, `link` last.
- A step that names an Agent with no connected body, one the run never had or one that has left, is a case error, and so is a `link` step after `> lose link` or under `#! game link: none`. `RunCase` sends nothing, writes `RUN ENDED`, stops the MAS and exits with a non-zero status naming the step. The Conformance suite fails the case without matching it.
- `> lose link` makes the link write `T2803` and fail what it has in flight.

Spec: chapter 35, *Test mode*, step 3. For the steps, chapter 34, *The script*.

### Actions in a case

By default `ScriptedGame` answers every `regia_action` with one `done`, at once, under the `id` it came with: a body's own, or the link's for a Director's Action. The case's standing rules change that for the Actions matching a pattern:

| Rule | `ScriptedGame` answers |
|---|---|
| `> action fails <pattern>` | `accepted`, then `failed` |
| `> action refused <pattern>` | `refused` |
| `> action holds <pattern>` | `accepted`, and nothing more until told |
| `> action succeeds <pattern>` | `done` at once, the default |
| `> action done <pattern>`, `> action failed <pattern>` | the final reply, to every held Action that matches |

- A pattern matches an Action's name and arguments, never its `sender`, so a Director's Action is held and finished like an Agent's.
- It records every `regia_action_cancel` and stops holding that Action. A case expects the call-off through the `DO <action> CANCELLED` entry, and a later `> action done` no longer matches it.
- It never sees a dotted Action, which runs inside the agent, so no rule holds it or makes it fail.
- It ignores `regia_story_ended`, which the Trace already shows as the Root's `STAGING … ENDED` entry.

Spec: chapter 37, *Test mode*. For the rules, chapter 34.

### The game's state in a case

`ScriptedGame` answers each `regia_state` at once, in order with everything else it sends, from the smallest record a game would keep:

- Facts: the instances that `link` steps, and `*` steps that reached the link, have made true and not made false since. `fact` steps to a body don't count, since they say what one body perceives. `> fact link +…` steps before `> start` set the record without sending anything, so the Root's reply carries them.
- Left: every Agent named by a `> leave` step.

A case can't hold a state reply or send a second one. So `T3305`, a join before the state reply, and `T3703`, which only a misbehaving game causes, can't be scripted.

Spec: chapter 35, *The game's state*.

### Settled

`RunCase` plays the next step, or ends the case, only when the run has settled. For every agent:

- no intention is running, except ones paused in `regia.wait`, or waiting in `regia.act` on an Action `ScriptedGame` holds;
- the mailbox and the event queue are empty;
- and `ScriptedGame` has nothing left to send, with nothing it sent still on its way on any connection, the link's included,

all of it for one whole cycle. A Director waiting for its state reply needs no rule of its own: `ScriptedGame` answers at once, so the run is never settled while a request is unanswered.

If the run has settled with an intention waiting in `regia.wait`, the virtual clock jumps to the earliest wake-up instead of going on to the next step. While the case has paused the clock with `> pause` (*Pausing*, above), it doesn't jump, and a run settled with only such waits goes on to the next step. `regia.wait` waits on the wall clock in a normal run and on the virtual clock in a case; dropping its intention during the wait removes it either way.

Spec: chapter 35, *Test mode*, step 4, and *Time*.

## How this combines with…

### Actions and time

Every rule of *Actions and time* about a `DO` lands here: waiting for the final reply, `WITHOUT WAITING` going on at `accepted`, calling off as a `regia_action_cancel`, the dotted Action run in the agent. The Target's clock is the one the game link stops and starts. (*Actions and time*)

### The Trace

*The Trace* says what each entry holds and how a case is matched. Here one writer gives `seq` and writes file and console, the source map gives `at` and our names, and `RunCase` with `ScriptedGame` plays the script. (*The Trace*)

### Jason: the Build

The ports `ScriptedGame` serves, and the game serves in a real run, are the `.jcm`'s; `cast.json` tells a real game the same. External names reach the wire through each file's `regia_game` beliefs. `sourcemap.json` and `traces/` sit in the Build folder. (*Jason: the Build*)

### Jason: Directors and Stagings

A Director's game Facts come from its `regia_state_result` when it attaches, and its game Cues and Facts afterwards from the link. Its Actions travel on the link under the link's counter, and the Root's last act is `regia_story_ended`. (*Jason: Directors and Stagings*)

### Jason: Plans and Goals

`DO` is `regia.act`, which suspends the intention as `regia.wait` does, so the walker that drops a Goal finds it there and the cancel follows. A `T1101` from the reply is a cause entry, written once, and the plan fails with `regia_because`. (*Jason: Plans and Goals*)

### When an Agent leaves

The game reports a leave with `regia_leave` on the link, and every attached Director hears it. A body closing is not a leave: VEsNA kills that agent, it stays in every cast, and sends to it are caught. A step naming a leaver in a case is a case error. (*When an Agent leaves*)

### Randomness

The seed `regia run` hands over, or the case's, seeds the one source behind every `RANDOM`, `RANDOMLY`, Pick and `n OF`, and the `run` entry records it. (*Randomness*)
