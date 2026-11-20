# How Jason behaves where the translation waits

Type: research
Status: closed
Assignee: Edoardo Vassallo (claude session)
Blocked by: 05

## Question

Find out the facts about Jason, and about VEsNA-Pro's `Temper`, that group A of the [inventory](../jason-open-questions.md#a-facts-about-jason-the-decisions-wait-on-how-jason-behaves-where-the-translation-waits) lists: a known belief told again from a new source, an `[atomic]` intention that suspends, variables in `for`, the `-!g` event's annotations, testing a Goal pursued by another intention, and the range and effects of a Mood in `Temper`.

Read the local sources first: Jason's source in `references/jason-main/` (the interpreter is `jason-interpreter/`), the Jason book in `references/` (*Programming Multi-Agent Systems in AgentSpeak using Jason*), and VEsNA-Pro in `references/vesna-pro-main/`. Go online (Jason's documentation, release notes) only for what they don't settle, and note which version the source is. Cite file and line for each answer. Write the findings to a research note and link it here.

Done when each of the six questions has a sourced answer, or says plainly that the source doesn't settle it.

## Comments

Research running on throwaway branch `research/jason-facts` (file `research/jason-facts.md`). Never merged.

## Resolution

Findings in `research/jason-facts.md` on branch `research/jason-facts` (commit `d367d83`), with file and line or book page for each answer, and small `.mas2j` runs on the 3.2.1 jar. The local source is Jason 3.3.4; VEsNA-Pro pins 3.2.1 through JaCaMo 1.2, and every finding was checked against both.

1. **A Fact told again from a new source** raises `+f[source(c)]` again; the same source telling again raises nothing. The context sees the merged sources, so "held before" is only "has a source other than the trigger's". Feeds *Messages and told Facts in ASL*.
2. **An `[atomic]` intention that suspends** blocks every other intention and event, but messages are still read. It resumes only if Java wakes it. If waking needs an AgentSpeak plan to run, the agent deadlocks. Feeds *Entering and leaving a Phase in ASL* (a `DO` in `EXITED`) and *Subplot arguments and endings in ASL* (a Root relaying a child's `DO` while ending).
3. **`for`** unbinds the body's variables between rounds and after the loop. Feeds *A Plan's Statements in ASL*.
4. **`-!g`** keeps the original `+!g` annotations (`source(S)` included), adds `error(…)` and code-location annotations, and every argument of `.fail(…)`, which can carry a Reason. `.fail_goal(g)` adds none. **Against the book (p. 90):** if a `-!g` plan exists but its context is false, the whole intention is dropped; the failure passes down only when there is no `-!g` plan. Feeds *A Goal's life in ASL*.
5. **Another intention pursuing `g`:** in a plan body, `.intention(Me,_,_,current) & .intend(g,I) & I \== Me` is exact. In a context, `current` is stale (last cycle's intention). Feeds *A Goal's life in ASL*.
6. **`Temper`** takes Moods, `temper([…])` targets and `effects` in [-1, 1] (Traits in [0, 1]), so chapter 14's note that "Regia follows the code, [0, 1]" is wrong. Negative values work with `most_similar` and break `random`. `effects` apply only when several intentions compete, at every step chosen, never for a lone or atomic intention. No public method changes a Mood, so `regia.shift` needs a VEsNA-Pro change. Further bugs: a Mood pushed below -1 becomes 0; a missing `strategy` throws; the readme's `nearest` is rejected. Feeds *Moods and Labels on VEsNA-Pro*.
