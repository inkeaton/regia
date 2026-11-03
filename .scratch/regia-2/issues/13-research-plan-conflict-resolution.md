# Research: plan conflict resolution in BDI and game AI

Type: research
Status: resolved

## Question

How do existing systems resolve conflicts when several plans, or several sources of behaviour, apply at once? Look at BDI platforms (Jason/AgentSpeak option selection, 2APL, GOAL, JACK, priority-based BDI extensions), and game AI (behaviour tree priorities, utility AI, GOAP, layered or subsumption arbitration). Collect the models (absolute vs relative priority, hierarchical priority, utility scoring, mutual exclusion of actions) and their trade-offs for designers. This is input for the Regia priority model, where Playbooks from several Plots may be active on one Agent.

## Comments

Research running on throwaway branch `research/plan-conflict-resolution` (file `research/plan-conflict-resolution.md`). Never merged.

## Answer

Full findings are on branch `research/plan-conflict-resolution`, file `research/plan-conflict-resolution.md` (it includes a comparison table of models and their trade-offs for designers).

- **"Priority" is four separate decisions:** which event to handle, which plan to pick for it, which running intention advances or pre-empts, and which actions can't run together. ABL (Façade) has a separate knob for three of them. A single `PRIORITY n` would be read as covering all four.
- **Jason today:** events are handled first-in first-out; the first applicable plan in source order wins, so only one plan runs per event; running intentions take turns one step at a time; `[atomic]` is the only exclusion. There is no numeric plan priority. Two Playbooks reacting to the same event won't both fire unless the compiler restructures them.
- **Hooks in Jason:** a `select__option/4` rule written in AgentSpeak can filter which plans are allowed, so priority logic can be emitted without Java. Overriding `selectOption` in Java is the other route.
- **JACK:** layered: declaration order, then a 0–9 rank that can be computed from beliefs, then first-or-random, then meta-plans. Plan bundles (the closest thing to Playbooks) rank above single plans. You can choose run-to-completion or taking turns.
- **GOAL:** "first applicable rule only" vs "all applicable rules" is a one-word option per module. This maps onto Regia's "which fires, or both" question.
- **AgentSpeak(RT):** priorities go on events, not plans. Higher-priority intentions are scheduled first, and lower ones that clash are dropped.
- **Game AI:**
  - Behaviour trees: position in the tree is the priority. Unreal adds interrupt settings, and stateless trees can loop between two behaviours.
  - Utility AI: predictable (always take the top score) vs varied (random, weighted by score). Dual utility (Dill) combines a rank for hard categories with a weight within each.
  - GOAP: simple goal priorities with fallback, but authorial control over scripted scenes gets weaker.
- **Precedent for "the story overrides everyday behaviour":** Zoo Tycoon 2 gave scripted shows ranks 98–102 over everyday needs at 0. Façade's interruption handlers outrank beat goals. In subsumption, a higher layer overrides lower ones.
- **Not confirmed from primary sources:** 2APL tie-breaking, GOAL's exact semantics, Halo 2, Brooks 1986, BOID.
