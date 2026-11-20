# The showcase: a royal banquet in Regia 1.5

Every example in the guides comes from this one world. This file is its outline: what the world is, who is in it, and where each part of Regia 1.5 has its place. The Program sits beside this file:

| File | Holds |
|---|---|
| `vocabulary.regia` | every shared Name, Fact, Cue, Goal, Action and Propensity |
| `playbooks/*.regia` | one Playbook per file, each importing the Vocabulary |
| `plots/*.regia` | one Plot per file, importing the Playbooks it gives and the Subplots it starts |
| `banquet.regin` | the full cast, and the Build's Entry |

The walkthrough follows four runs, each a test cast and a behaviour case in `runs/<run>/` (`evening`, `grudges`, `short_evening`, `two_duels`), and each cast imports `banquet.regin`. Decided in *The walkthrough's shape* (`.scratch/showcase-1-5/issues/04-walkthrough-shape.md`).

The Jason reference Build is `jason/banquet/`: the Build of `banquet.regin`, written by hand and laid out as chapter 28's Build folder. The guide that goes from each construct to its ASL is `jason/README.md`, and the coverage table below will gain a **Jason** column linking each row to its section. Decided in *The Jason showcase's shape* (`.scratch/showcase-1-5/issues/06-jason-showcase-shape.md`).

The Program uses only Regia 1.5 (ADR 0025). Where a 1.5 pattern stands in for a 2.0 construct, the guide adds an "In 2.0" note. The outline is derived from the spec, never the other way round: where they disagree, the spec wins and this file is fixed. It replaces the 2.0 showcase in `docs/guide/showcase/`, which is kept as it was.

## The world

One evening at a royal banquet, from the guests arriving to the last one taking leave. The game behind it is a 3D hall. Walking to a seat takes time, animations finish when they finish, and the game can refuse an Action (a sword can't be drawn at the table, a dish has run out).

## Plots

### `RoyalBanquet` (the Root Plot)

Roles: `Host`, `Guest`, `Servant`, `Guard`. The whole Cast gets `Courtesy`; the Host gets `Hosting` and the Guards `Keeping_watch`.

| Phase | What happens | How it ends |
|---|---|---|
| `arrival` (initial) | Guests walk to their seats. | The Director counts `seated` Guests by hand, against `COUNT(? PLAYS Guest)`. |
| `reception` | Mingling and gossip (`NobleSocializing`). | After two minutes the Host is asked to open the feast; its toast moves on. |
| `feast` | `Dining` and `Serving` for the Phase; `Poisoning` starts until the Phase is left; insults start duels. | Three Guests in four have finished eating, counted by hand, or the poison is drunk. |
| `farewell` | Duels are called off, Guests take leave and leave the Program. | `Guest EMPTIED` ends the Plot. |

`DURING PLOT` counts again when a Guest leaves, ends the Plot when the Guests or the Host are gone, and hears the Subplots end.

### `HonorDuel(offender)` (Subplot, several Stagings at once)

Roles: `Challenger`, `Defender`, `Spectator`. Phases: `challenge`, `betting`, `fighting`.

Every insult taken badly starts a Staging, one per offender at a time. The insulted Guest is the Challenger, the offender the Defender, and the other Guests are Spectators who bet. Betting closes after 20 seconds; the biggest backer drops the handkerchief, and only then does the fight start. It ends with `duel_settled(?winner)` or `duel_abandoned`.

### `Poisoning` (Subplot, one Staging, no Phases)

Roles: `Poisoner`, `Watchman`. `1 OF Guest` is the Poisoner and the Guards are Watchmen. It ends with `poisoner_caught(?who)`, with `poison_taken` when the game reports the cup drunk, or from above when the feast ends.

## Playbooks

| Playbook | Given to | What it carries |
|---|---|---|
| `Courtesy` | the whole Cast, from the `CAST` setup | Taking a seat and leave, a local Cue, a done-Signal on `ENDED` |
| `Hosting` | the Host, from its setup | The toast and the honouring; the one Action whose External name has a dot (the Target's own code) |
| `NobleSocializing` | Guests, from `reception` to `farewell` | Suits alternatives, a Random choice, a weighted Pick, `ME`, a told Fact, counted recipients |
| `Dining` | Guests, for the `feast` | Goals and their endings, `WAIT … UNTIL`, `FAIL WITH`, a fallback Goal, `WHEN ASSIGNED` |
| `Serving` | Servants, for the `feast` | A waiting `PURSUE`, a refused Action, a Reason told back by hand |
| `Keeping_watch` | Guards, from their setup; Watchmen; a duel's winner | One Playbook given by three Givings; `REMOVED` |
| `Duelling` | Challenger and Defender | A crosswise Mapping, local Cues, a repeating Goal, `GIVEN` against `IF` |
| `Wagering` | Spectators | Filling a Placeholder with `LET`, `UPDATE`, a whole roll |
| `Scheming` | the Poisoner | `LOWEST`, `WITHOUT WAITING`, falling through to small talk |

## Agent kinds

| Kind or Agent | Plays | Starts | Why it is here |
|---|---|---|---|
| `king` (`AGENT`) | `Host` | 1 | The single Host, an individual Agent |
| `noble` | `Guest` | 6 | Random Propensity values |
| `hothead` (`LIKE noble`) | `Guest` | 2 | Same Role, other values, and a grudge against `percival` |
| `knight` | `Guest` and `Guard` | 1 | One Agent in two Roles, where Precedence has to be declared |
| `percival` (`AGENT`, `LIKE knight`) | `Guest` and `Guard` | 1 | A knight with a name, so that Instancing can name him |
| `servant` | `Servant` | 3 | Work done through Custom Actions |

## Diagnostics

The Program builds in 1.5 with no error and no warning, and nothing in it is allowed. Every Diagnostic, `#@allow` included, is shown in a snippet, by breaking a line of the Program.

## Coverage

One row per `##`/`###` section of spec chapters 01–21, 26 and 38, each read with its `## Regia 1.5` section. Sections that only list checks, reserved words, Trace entries, ASL notes, or what is decided elsewhere have no row. Decided in *What the showcase must show* (`.scratch/showcase-1-5/issues/02-what-the-showcase-shows.md`); places checked against the written Program in *Write the 1.5 showcase Program*.

**Place** is one of:

- a file and Plan of the Program (`pb/` = `playbooks/`, `pl/` = `plots/`, `voc` = `vocabulary.regia`);
- `snippet`: shown only in the guide, as a variation of a banquet line, never added to the files;
- `—`: the section holds no construct to show (a rule of meaning, a promise, a tool matter);
- `2.0`: left out of 1.5; the guide gives an "In 2.0" note where the 1.5 Program has a stand-in;
- `runs/<run>`: in a test cast or behaviour case of the walkthrough.

### 01 Statements and blocks

Guide: [Syntax](../guide/02-syntax.md)

| Section | Construct | Place |
|---|---|---|
| Two styles | indentation, and the explicit style (`:` then the body, `.`, `;`) | everywhere; Inline blocks for one-line Plans (`WHEN take_seat ENDED: SIGNAL took_seat`); several Statements on one line, and `IF x: DO a; ELSE: DO b`: snippet |
| Block headers | `:` on every header | everywhere |
| Where a Block's body starts | indentation Block, Inline block | everywhere |
| No Block without indentation across lines | a `;` that closes nothing (`R0108`) | snippet |
| Headers inside an Inline block | error | snippet |
| When `.` ends a Statement | `.` vs dotted names | `voc` (`ACTION hall.music.fanfare AS play_fanfare`); a `.` between two Statements: snippet |
| Indentation rules | | everywhere; mixing tabs is a snippet |
| Continuation lines | a Statement split after `,` | `pl/royal_banquet` the two `START SUBPLOT`s |
| Parsing never depends on declarations | | — |
| One meaning per word; Keywords; What syntax can be dropped | | — (rules of the syntax) |
| Clauses and the comma | `, FROM`, `, SUITS`, `, WITHOUT WAITING`, …; `,` in a list | everywhere; `pb/noble_socializing` `WHEN insulted, FROM peer ?who, SUITS aggressiveness AT 0.8, bravery AT 0.8:`; a clause without its `,` (`R0111`): snippet |
| Where condition words go | `?x PLAYS r`, `P RUNNING`, `PURSUING g`, `IN phase` | `pb/noble_socializing` `?foe PLAYS peer`; `pl/royal_banquet` `HonorDuel(?offender) RUNNING`, `IN arrival`; `pb/dining` `PURSUING have_dinner` |
| Empty Blocks | `PASS` | `pb/noble_socializing` small talk: `OPTION, WEIGHT 5: PASS` |
| Retired spellings | an old spelling and its error | snippet |
| A word of 2.0 in a 1.5 build | `R0109` | snippet, once, among the Variations ("In 2.0" notes show no 2.0 code) |

### 02 Comments

Guide: [Syntax](../guide/02-syntax.md)

| Section | Construct | Place |
|---|---|---|
| Plain comments | `#`, `#[ … ]#` | everywhere; one `#[ … ]#` in `pl/royal_banquet` (counting by hand) |
| Doc comments: Form, Keys | `#@key:`, `#@desc[ … ]#`, `desc`/`version` | file Doc comment on `pl/royal_banquet` (`#@version`, `#@desc[ … ]#`) |
| Attachment | on Plot, Playbook, Role, Phase, Plan, item | every Plot and Playbook; Role `Guest` and Phase `feast` in `pl/royal_banquet`; Phase `betting` in `pl/honor_duel`; the scowling Plan in `pb/noble_socializing`; items in `voc` (`seize`, `eat`, …) |
| Allowing a warning: `#@allow` | `#@allow: R1305` | `snippet` (an order by name between two Playbooks never held together, chapter 02's own case) |
| Instancing | (no comment form) | — |

### 03 Parameters and placeholders

Guide: [Vocabulary and files](../guide/03-vocabulary-and-files.md)

| Section | Construct | Place |
|---|---|---|
| Declaring parameters | untyped parameters | `voc` |
| Values and Placeholders; Names are declared | `NAME`, Values vs `?x` | `voc` (`NAME wall, door, kitchen`); everywhere |
| `ME` | in a Trigger and in an argument | `pb/noble_socializing` `WHEN scandal(ME)`, `wronged(ME, ?speaker)` |
| Where Placeholders are filled and used | | everywhere; a Plot parameter in `pl/honor_duel` (`?offender`) |
| Values in a Trigger restrict it | `WHEN served(roast)` | `pb/dining`, above `WHEN served(?dish)` |
| Same name, same value | one Placeholder joining two conditions | `pb/noble_socializing` `grudge(?foe, ?size) AND ?foe PLAYS peer` |
| "Don't care": `?` | `?`, `?_name` | `pb/duelling` `GIVEN stamina(?)`; `pb/serving` `bring(?dish, ?)`; `pb/noble_socializing` `?_who` on the Suits alternative that only laughs |
| Matching a Context | | — |
| Only what is certainly filled | Placeholder under `NOT` avoided with `?`; `IF` that fills a Placeholder | `pb/serving` `NOT PURSUING bring(?, ?)`; `pb/noble_socializing` `resent` |
| Several matches | | — (rule; shown by Picks, ch 26) |

### 04 Numbers and expressions

| Section | Construct | Place |
|---|---|---|
| Numbers | whole and decimal | `banquet.regin` Propensity values; Labels |
| Arithmetic, Comparisons, Order | `*`, `>=`, `/` | `pl/royal_banquet` `COUNT(finished(?)) * 4 >= COUNT(? PLAYS Guest) * 3` |
| Random numbers | `RANDOM(a, b)` in a setup, a Body and a condition | Role setup `purse(RANDOM(5, 20))`; `pb/wagering` `RANDOM(1, ?gold / 2)` (a whole roll, guarded); `pb/noble_socializing` `IF RANDOM(1, 100) <= 30:` |
| Where Expressions can appear | in a Body argument | `pb/wagering` `UPDATE purse(?gold) TO purse(?gold - ?stake)`; in a Message argument: snippet |
| The Context tests, the Body fills | `LET` in a Body | `pb/wagering` `LET ?stake BE …`; `pb/noble_socializing` `LET ?grudges BE COUNT(…)` |
| When a Number isn't a Number | arithmetic Failure | snippet |

### 05 Goals and triggers

Guide: [Plans](../guide/04-plans.md)

| Section | Construct | Place |
|---|---|---|
| Declaring Goals; One name, one kind | `GOAL` | `voc`; local Goals in `pb/dining`, `pb/serving`, `pb/duelling` |
| Who gives a Goal | self, Agent `ASK`, Director `ASK`, setup | `pb/dining` (self), `pb/dining` → `pb/serving` (`ASK`), `pl/royal_banquet` `ASK Host TO open_feast`, Role setups (`PURSUE take_seat`) |
| Reaching a Goal | `TO` recipe finishing | `pb/courtesy` `TO take_seat` |
| Pursuits | | — |
| Waiting for a Goal | `PURSUE g` / `, WITHOUT WAITING` | `pb/serving` `bring` waits on `fetch`; `pb/duelling` `fight` starts `strike` |
| Testing Goals in a Context | `PURSUING` | `pb/dining` (no second dinner), `pb/serving` (no order on hand) |
| Cues are momentary; Events | `CUE` | `voc` |
| Trigger kinds | | spread; each placed under its own chapter |
| How a Pursuit ends | `REACHED`, `DROPPED`, `FAILED`, `ENDED` | `pb/dining` (all four); done-Signals on `ENDED` in `pb/courtesy`, `pb/hosting`, `pb/dining`, `pb/wagering` |
| Where it came from: `FROM` | `, FROM Role`, `, FROM ?who`, `, FROM Role ?who`, `, FROM DIRECTOR` | `pb/dining` `, FROM waiter`, `pb/keeping_watch` `, FROM ?speaker`, `pl/royal_banquet` `, FROM Guest ?g`, `pb/keeping_watch` `LEARNED, FROM DIRECTOR` |
| The game and the Agent itself | `FROM GAME`, `FROM ME` | 2.0 |
| Alternatives: `OR` | | 2.0 |
| Who pursued it: `BY` | | 2.0; "In 2.0" note on each done-Signal |
| The shape of a Trigger | `FAILED WITH …, FROM …` | `pb/serving` |

### 06 Context and control flow

Guide: [Plans](../guide/04-plans.md)

| Section | Construct | Place |
|---|---|---|
| Two different questions | `GIVEN` vs `IF` | `pb/duelling` `strike`: `GIVEN stamina(?)` … `WAIT` … `IF stamina(?)` |
| Conditions | `AND`, `OR`, `NOT`, parentheses | `pb/keeping_watch` `on_duty AND (NOT seat(?) OR NOT hungry)` |
| Plans under one Trigger | `GIVEN` siblings, `ELSE` | `pb/noble_socializing` gossip, `pb/duelling` `hit`, `pb/wagering`, `pl/honor_duel` betting |
| `IF` in a Body | `IF` / `ELSE IF` / `ELSE` | `pl/royal_banquet` `LEFT` Plan |
| Placeholders in an `IF` | | `pb/noble_socializing` `resent` |
| Loops | `FOR EACH` (ch 26), repeating (ch 08) | see ch 26 and 08 |

### 07 Messaging

Guide: [Messages](../guide/10-messages.md)

| Section | Construct | Place |
|---|---|---|
| Three ways to send | `TELL`, `ASK`, `SIGNAL` | everywhere |
| Recipients | Role, `?who`, `EVERYONE`, counted | `pb/noble_socializing` `TELL EVERYONE scandal(?foe)`; `pb/dining` `ASK 1 OF waiter`; `pl/honor_duel` `ASK ?backer` |
| Signals | | `pb/courtesy`, `pb/dining`, `pb/duelling` |
| Delivery | | — |
| A told Fact; A Fact or a Cue | a Fact told by an Agent | `pb/noble_socializing` `wronged`, heard with `LEARNED, FROM peer` |
| Taking a told Fact back | forgetting in the owning Playbook | `pb/keeping_watch` `WHEN REMOVED: FORGET on_duty` |
| A told Cue | | `pb/serving` → Guest `sold_out(?dish)` |
| An asked Goal | | `pb/dining` → `pb/serving` |
| Hearing how an asked Goal ended | | 2.0; the Reason told back by hand in `pb/serving` is the stand-in |
| Sender forms | | as ch 05 |
| Room for cooperation | | — |

### 08 Basic actions

| Section | Construct | Place |
|---|---|---|
| Facts; Updating a Fact | `LEARN`, `FORGET`, `UPDATE` | `pb/wagering` `UPDATE purse(…)`; `pb/duelling` |
| Pursuing; Dropping | `PURSUE`, `DROP` | `pb/dining` `WHEN hungry FORGOTTEN: DROP have_dinner`; `pb/duelling` `DROP strike` (both stop a waiting recipe) |
| Repeating | recipe ending `PURSUE` own Goal `, WITHOUT WAITING` | `pb/duelling` `strike` |
| Sending | `EVERYONE` | as ch 07 |
| `PRINT` | `PRINT` with a String | `pl/royal_banquet` `WHEN Poisoning DROPPED` |
| `WAIT` | Durations | `pb/duelling`, `pb/dining` |
| Custom Actions | waiting game Action; dotted Target Action; `, WITHOUT WAITING`; a called-off Action | `pb/courtesy` `walk_to`; `pb/hosting` `play_fanfare`; `pb/scheming` `pour_poison`; `pb/dining` `eat` when dinner is dropped |

### 09 Random choice

| Section | Construct | Place |
|---|---|---|
| `RANDOMLY` / `OPTION`; Weights | | `pb/noble_socializing` small talk |
| Placeholders in an Option | Option of several Statements; a Weight named before the choice | `pb/noble_socializing` (`?grudges`); a value named inside an Option: snippet |
| Random choice in a Director | | snippet |

### 10 Scoping and imports

Guide: [Vocabulary and files](../guide/03-vocabulary-and-files.md)

| Section | Construct | Place |
|---|---|---|
| Imports | | every file imports `vocabulary.regia` |
| Broken transitive names | | snippet |
| The program; One namespace; Name rules; Declaration order | | — (errors in snippets) |
| What the game produces: `GAME` | `GAME FACT`, `GAME CUE` | `voc` (`seat`, `hungry`, `in_stock`, `idle`, `saw_pouring`, `poison_drunk`) |
| External names | `AS`, dotted Fact/Cue names, dotted Action | `voc` |
| Local Vocabulary; Local Cues | local `FACT`, `GOAL`, `CUE`, a Plot's local `FACT` | `pb/dining`, `pb/serving`, `pb/duelling` (`challenged`, `hit`, `yielded`), `pb/courtesy` (`greeting`); `pl/royal_banquet` `seated`, `pl/honor_duel` `wager` |

### 11 Failure

| Section | Construct | Place |
|---|---|---|
| When a Plan fails; What it leaves behind | refused Action | `pb/serving` `pick_up` refused |
| How failure spreads | through a waiting Goal | `pb/serving` `fetch` → `bring` |
| When no Plan applies | | `pb/courtesy` `take_seat` with no seat; snippet (Trace) |
| `FAIL` | `FAIL WITH` | `pb/serving` `FAIL WITH sold_out(?dish)`; `pb/dining` `FAIL WITH no_food` |
| Reasons | | as above |
| Reacting; Writing a fallback | `WHEN g FAILED WITH r` above plain `FAILED`; a fallback Goal; an `IF` before the risky step | `pb/serving`; `pb/dining` `FAILED WITH no_food` pursues `make_do`; `pb/serving` `fetch` |
| Trying again | | snippet |
| Every Pursuit that ends fires its Triggers | | — |
| The trace | | every run in `runs/`; the `T1104` of a knight with no seat in `runs/evening` |

### 12 Time

Guide: [Vocabulary and files](../guide/03-vocabulary-and-files.md)

| Section | Construct | Place |
|---|---|---|
| The clock belongs to the Target | | — |
| Durations; `WAIT` | `SECONDS`, `MINUTE` | `pb/duelling`, `pb/dining` |
| `WAIT … UNTIL` | with a limit | `pb/dining` `WAIT 1 MINUTE, UNTIL on_plate(?)` |
| `AFTER` | one and several in a Block | `pl/royal_banquet` `reception`; `pl/honor_duel` `betting` (20 s and 1 min) and `fighting` (2 min, `duel_abandoned`) |

### 13 Plan selection

| Section | Construct | Place |
|---|---|---|
| Candidates; Order; Inside a Playbook | falling through | `pb/keeping_watch` and `pb/noble_socializing` on `scandal`; `pb/dining` `served(roast)` |
| Who orders what; Defaults | | — |
| `PRECEDENCE` | `OVER … ON`, `OVER` between Subplots, `PARENT OVER SELF` | `pl/royal_banquet` (`Keeping_watch OVER NobleSocializing ON scandal`, `HonorDuel OVER Poisoning`); `pl/honor_duel` `PARENT OVER SELF ON scandal`; a relation `ON` a recipe or a Fact change: snippet |
| Suits alternatives inside a Playbook | | `pb/noble_socializing` insult reactions; `pb/duelling` `challenged` |
| `TIES` between Playbooks | `TIES … ON` | `pl/royal_banquet` `Dining TIES NobleSocializing ON insulted` |
| What the language promises; Instancing | | — |

### 14 Labels

| Section | Construct | Place |
|---|---|---|
| Propensities; Writing Labels; The Labels | Traits, Moods, `SUITS`, `SHIFTS` | `voc`; `pb/noble_socializing`; `pb/duelling`; `pb/dining` |
| Where Labels go; Suits alternatives | a `SHIFTS` on a `GIVEN`; one alternative with a Context | `pb/noble_socializing` (gossip; the scowling Plan) |
| The `SHIFT` Statement | | `pb/noble_socializing` `SHIFT sympathy BY -0.2` |
| Targets without Labels | | — |

### 15 Roles and mappings

| Section | Construct | Place |
|---|---|---|
| Playbook Roles; Roles are addresses | `ROLE` in a Playbook | `pb/serving` `patron`, `pb/dining` `waiter`, `pb/duelling` `opponent`, `pb/courtesy` `host` |
| Mappings; What a binding means | whole-Role, crosswise, Placeholder | `pl/honor_duel` (`opponent` crosswise); `pl/royal_banquet` `START SUBPLOT HonorDuel` |
| Givings | `ASSIGN`, `REMOVE`, `ASSIGN … TO ?who` | `pl/royal_banquet` (`ASSIGN Keeping_watch TO ?winner`) |
| Taking a giving from one Agent | `REMOVE … FROM <Role> ?who` | `pl/royal_banquet` `WHEN Poisoning FINISHED WITH poisoner_caught(?culprit)` |
| Giving it back: `ASSIGN … TO <Role> ?who` | | snippet |
| Until the Phase is left: `UNTIL EXITED` | on `START SUBPLOT`; by Phase setups | `START SUBPLOT Poisoning, …, UNTIL EXITED`; `feast` setups |
| Given and taken: `ASSIGNED` and `REMOVED` | | `pb/dining` `WHEN ASSIGNED`; `pb/duelling`, `pb/keeping_watch` `WHEN REMOVED` |
| Taking a Playbook away | | interaction 7 (`feast` left) |
| The whole Cast: `CAST` | `CAST:` | `pl/royal_banquet` |
| Counts and fractions; How the pick works; Odd values | `1 OF`, `n% OF` | `pl/royal_banquet` `MAPPING 1 OF Guest AS Poisoner`; `pb/noble_socializing` `TELL 50% OF peer` |
| A counted recipient | in a Playbook | `pb/dining` `ASK 1 OF waiter`; `pb/noble_socializing` `TELL 50% OF peer` |
| Leaving Agents out: `EXCEPT` | on a Mapping, with a list | `pl/royal_banquet` `Guest EXCEPT ?offended, ?offender`; on a Giving and on a recipient: snippet |
| Who plays a Role: `PLAYS` | in a Plot and in a Playbook | `pl/royal_banquet` `COUNT(? PLAYS Guest)`; `pb/noble_socializing` `?foe PLAYS peer` |

### 16 Role setup

| Section | Construct | Place |
|---|---|---|
| A Role's Block; What it means; Sender | `ROLE r:` | `pl/royal_banquet` Role setups; `TO take_seat, FROM DIRECTOR` in `pb/courtesy` |
| Order and trouble | `ASSIGN` before `PURSUE` | `pl/royal_banquet` (`R1605` in a snippet) |
| A setup for a Phase | `DURING feast` setups | `pl/royal_banquet` `Dining`, `Serving` |
| A setup for the whole Cast | `CAST:` | `pl/royal_banquet` `ASSIGN Courtesy` |
| Mappings | same names bind ignoring case | `pl/royal_banquet` (`Courtesy`'s `host` is `Host`) |
| When the Agent stops playing the Role | | — |

### 17 Subplots

| Section | Construct | Place |
|---|---|---|
| Starting a Subplot | `START SUBPLOT` | `pl/royal_banquet` `feast` |
| Plot parameters | `HonorDuel(offender)` | `pl/honor_duel`; `?offender` used inside it |
| Casting; Being in both | | `pl/honor_duel` |
| An Agent in two Stagings of one Plot | | `runs/two_duels` (a Spectator in both duels) |
| Stagings; Running Stagings | `RUNNING` | `pl/royal_banquet` `GIVEN NOT HonorDuel(?offender) RUNNING` |
| A Subplot outlives its Phase | | a duel running into `farewell` |
| `END PLOT`; Outcomes | `END PLOT WITH` | `pl/honor_duel`, `pl/poisoning`; a bare Root `END PLOT` |
| The parent's Triggers: `FINISHED`, `DROPPED`, `ENDED` | `FINISHED WITH`, `ENDED`, `DROPPED`; a plain `FINISHED` | `pl/royal_banquet` `DURING PLOT`; `WHEN Poisoning DROPPED`; a plain `FINISHED` after the `FINISHED WITH` Plans: snippet |
| `DROP SUBPLOT` | | `pl/royal_banquet` `farewell`: `DROP SUBPLOT HonorDuel(?)` |
| Precedence | | as ch 13 |
| No cycles | | snippet |

### 18 Quota triggers

All of it: 2.0. Stand-in: the hand counts of `arrival` and `feast`, with an "In 2.0" note.

### 19 Cast changes

| Section | Construct | Place |
|---|---|---|
| Who changes the Cast | | — |
| Joining; Standing Givings; Order; Subplots | | 2.0 |
| Leaving | | Guests in `farewell`; a Defender walking out; a caught Poisoner led out |
| Quota Triggers (on leaving) | | 2.0 |
| The Director hears about it | `LEFT`, `EMPTIED` | `pl/royal_banquet` `WHEN Guest ?g LEFT` (with `IN`, `ELSE IF`), `Guest EMPTIED`, `Host EMPTIED`; `pl/honor_duel` `Challenger`/`Defender EMPTIED`, `Spectator ?who LEFT` |
| Order when leaving; An empty Role; What the Agents hear | | — |

### 20 Directors

| Section | Construct | Place |
|---|---|---|
| What a Director is; perceives | a game Cue reaching a Director | `pl/poisoning` `WHEN poison_drunk` |
| What a Director knows about its own Staging | `IN`, `RUNNING`, `PLAYS`, own Facts | `pl/royal_banquet` (`seated`, `finished`); `pl/honor_duel` (`wager`) |
| How a Director directs Agents | `ASK`, `TELL`, Givings | everywhere in Plots |
| Hearing how an asked Goal ended | | 2.0 |
| Directing one Agent | `?who` from `FROM`, an Outcome, a Pick | `pl/honor_duel` `ASK ?backer`; `pl/royal_banquet` `?winner`, `?culprit` |
| Actions | Director `DO` | `pl/royal_banquet` `feast` `WHEN EXITED: DO clear_tables` |
| Trigger kinds; Declaring Phases | `PHASE`, `INITIAL` | every Plot but `Poisoning`; a Plot with no Phases (`pl/poisoning`); a Phase with no `DURING` Block: snippet |
| Entering and leaving Phases | `ENTERED`, `EXITED` | `pl/royal_banquet` |
| `EXITED, BY PARENT` | | `pl/poisoning` (the cup is discarded); `pl/honor_duel` on `DROP SUBPLOT` |
| What starting a Staging does; Leaving a Phase stops its Plans; What `ENTER` does | | — (interaction 7) |
| Failure | | — |

### 21 Instancing

| Section | Construct | Place |
|---|---|---|
| Who says what; Instancing files; Overriding | `.regin`, layering | `banquet.regin`; layering in the test casts |
| With no cast | | snippet |
| The Root Plot | `ROOT` | `banquet.regin` |
| Agent kinds; `LIKE` | `KIND`, `COUNT`, `LIKE` | `banquet.regin` (`hothead LIKE noble`) |
| Removing a kind: `NO KIND` | `NO KIND`, `NO AGENT`, a kind kept as a template | `runs/grudges` (`NO KIND knight`, `percival LIKE knight` kept); `runs/short_evening` (`NO AGENT percival`) |
| Individual Agents; Instancing names | `AGENT`, a Name from Instancing | `banquet.regin` `king`, `percival LIKE knight`; `LEARN grudge(percival, 2)` |
| Setup lines | `LEARN` in a kind | `banquet.regin` `hothead` |
| The seed | `SEED` | every cast in `runs/` |
| Target settings | `TARGET jason:` | `banquet.regin` (the default `strategy`, written out) |

### 26 Match selection

| Section | Construct | Place |
|---|---|---|
| Matches; The default | | — |
| Picks; The ranked Placeholder | `HIGHEST`, `LOWEST`, `, RANDOMLY` | `pl/honor_duel` `HIGHEST ?stake, RANDOMLY`; `pb/scheming` `LOWEST ?size` |
| A weighted Pick | | `pb/noble_socializing` `vent`: `WEIGHT ?size` |
| Where Picks are allowed | | — (errors in snippets) |
| `FOR EACH`; Forgetting everything that matches | | `pb/dining` each dish; `pl/honor_duel` `Spectator ?who LEFT` forgets the leaver's wagers |
| `COUNT` | | `pl/royal_banquet` hand counts; `pb/noble_socializing` `?grudges` |

### 38 Interfaces

| Section | Construct | Place |
|---|---|---|
| Nothing is declared; The Interface of a Playbook / a Plot | | the guide prints `Keeping_watch` (`runs/evening`) and `HonorDuel` (`runs/two_duels`) |
| Who sends a Cue | | — (every Cue in `voc` has a sender or is `GAME`) |
| Checks (`R3801`–`R3807`) | | the Program is clean; each check shown in a snippet; `R3805`/`R3806` are 2.0 |

## Gaps that stay gaps

A Subplot inside a Subplot; a Plot started from two parents; a file with two Plots; two sibling `.regin` files; a Multi-definition with `AS`; an item declared in two files; a Goal with recipes in two Playbooks; a Playbook with two Roles; a Failure that climbs three or more levels; a Phase with no `DURING` Block; a relation `ON` a recipe or a Fact change; a Random choice in a Director.

## Interactions the world forces

1. A Pick in a timeout Plan in a Subplot: `betting`'s `AFTER 20 SECONDS` picks `HIGHEST ?stake, RANDOMLY`, with the `ELSE` for no wager, and a second `AFTER` for a handkerchief that never falls.
2. Precedence across Playbooks, Phases and Subplots on one Agent: a knight, Guest and Guard, watching a duel, hears gossip. `Keeping_watch` comes first while it is on duty and not hungry at the table; otherwise the gossip falls through to `NobleSocializing`.
3. Failure climbing through a waiting Goal: `fetch` finds the dish gone and fails `WITH sold_out`, `bring` fails with it, and the Guest is told; or `pick_up` is refused, a Failure with no Reason, and the Servant only bows. The Guest's `WAIT 1 MINUTE, UNTIL on_plate(?)` runs out, it fails `WITH no_food`, and its `FAILED WITH no_food` Plan pursues `make_do`.
4. Leaving in the middle of a Subplot: the Defender walks out, `Defender EMPTIED`, `duel_abandoned`.
5. Leaving during a hand count: a Guest leaves in `arrival`; the `DURING PLOT` `LEFT` Plan forgets its Facts and counts again, so the departure can end the Phase.
6. `GIVEN` versus `IF` on a Fact that changes mid-Plan: `strike` is chosen while the duellist has stamina, and after its `WAIT` checks again.
7. A Phase-setup Giving and a Subplot outliving its Phase: leaving `feast` takes `Dining` away (`have_dinner` is dropped, its `DROPPED` and `ENDED` Plans run) and drops `Poisoning` (`WHEN Poisoning DROPPED`, its `EXITED, BY PARENT`), while a running duel keeps its Givings until `farewell` drops it with `DROP SUBPLOT`.
