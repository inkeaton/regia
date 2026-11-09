# Research: VEsNA-Pro temper and effects

Input for *Label syntax and mood Labels* (`.scratch/regia-2/issues/15-label-syntax.md`, on `main`). Throwaway branch: never merged.

## Sources

- **[U]** Upstream code: https://github.com/VEsNA-ToolKit/vesna-pro at HEAD `3f857f5` (2026). Files: `readme.md`, `src/agt/vesna/Temper.java`, `VesnaAgent.java`, `src/agt/alice.asl`, `vesna.jcm`. Commit `f2e98ee` (23 Mar 2026), "Update the mood only on selectIntention", is relevant.
- **[V]** The older copy vendored in this repo: `1.0/science_game/minds/src/agt/vesna/{Temper,VesnaAgent}.java`. It predates the refactor and behaves differently.
- **[P]** The paper: Gatti, Casale, Mascardi, Stucchi, Ferrando, "VEsNA-Pro: Exploiting BDI Agents with Propensities for Emergent Narrative", AAMAS 2026, pp. 967–976. https://ifaamas.org/Proceedings/aamas2026/pdfs/PDPF4024.pdf. The appendix is `docs/appendix.pdf` in [U].
- The 1.0 Regia emitter: `1.0/language/src/regia/emitter.py:1197-1229`. It emits `@label[priority(N), temper([...]), effects([...])]`.

The paper and the code disagree on several points. [P] is the formal model; [U] is what actually runs.

## 1. Plan annotations that are read

- `temper([t1(v), …])` and `effects([m1(d), …])` go on the plan label. The code reads them with `label.getAnnot("temper")` and `getAnnot("effects")`, and the argument must be a single list.
- An effect entry may carry `[mood]` (`x(0.1)[mood]`) to resolve a name clash with a personality trait.
- No other annotations are read. `priority(N)` is not a VEsNA-Pro annotation.
- [P] calls the tags `pr(...)` and `eff(...)`. The code doesn't use those names.
- The agent is configured in the `.jcm`, as user parameters:
  - `temper: temper( prop1(0.2), prop2(0.3), prop3(-0.5)[mood], prop4(0.3)[mood] )`
  - `strategy: most_similar | random`
  - Only the arguments of the outer literal are read; its functor name is ignored.
- The readme mentions `nearest`, but the code accepts only `most_similar` and `random`. Any other value throws, and a missing `strategy` causes a NullPointerException.
- [V] bug: `areIntentionsWithTemper` looks for `propensions(X)` instead of `temper(X)`, so temper-based intention selection never triggers.

## 2. Dimensions

- **Both kinds exist.** Personality is immutable. Mood is mutable, and a trait is mood if it is tagged `[mood]`. The general term is "propensities" ([P] Def. 3.1: Pr = Pr_immut ∪ Pr_mut).
- **The names are arbitrary and user-defined.** The case studies in [P] use OCEAN traits, but the code imposes no list.
- **Unknown names are tolerated:**
  - A plan trait the agent lacks is skipped and adds 0 to the score.
  - An effect on an unknown mood is skipped.
  - A personality trait name in `effects` without `[mood]` throws `IllegalArgumentException`.
- **Value ranges:**

  | Item | Code [U] | Paper [P] |
  |---|---|---|
  | Personality | [0, 1] | [-1, 1] |
  | Mood | [-1, 1] | [-1, 1] |
  | Plan `temper` values | [-1, 1] | [-1, 1] |
  | `effects` deltas | [-1, 1] | [-1, 1] |

- Mood updates are meant to clip to [-1, 1] (Def. 3.4). Bug in both [U] and [V]: a sum below -1 sets the mood to 0.0, not -1.0.

## 3. How a plan is scored

- **Both personality and mood count.** For each trait in the plan's `temper`, the agent's value is taken from mood if the name exists there, otherwise from personality.
- **`most_similar` (deterministic):**
  - The score is the sum of |agent − plan| over the plan's listed traits. It is not normalised.
  - The lowest score wins. On a tie, the first plan in Jason's option order wins.
- **`random`:**
  - The weight is the sum of agent × plan, followed by a weighted roll.
  - The roll is buggy: an `int` accumulator, negative weights mishandled, and a fallback to index 0.
- **[P] specifies more than the code does:**
  - normalised compatibility (L1, dot or cosine);
  - a stochastic variant;
  - intention-level aggregation and a fairness factor.

  None of these are in [U].
- **When temper selection runs at all:** only if the agent has a temper, there is more than one applicable option, and at least one has `temper`. Otherwise Jason's default applies (first option).
- **Plans without `temper`** get weight 0:
  - Under `most_similar`, 0 is the best possible distance, so an unannotated plan beats any annotated plan that doesn't fit exactly.
  - Under `random`, weight 0 means the plan is effectively never picked.
  - In [V], `select()` skips unannotated plans, so the weights and choices lists no longer line up (wrong plan returned).

## 4. When effects apply

- **[U], since `f2e98ee`:**
  - Effects apply only in `Temper.selectIntention`, from the plan on top of the selected intention.
  - They apply every time that intention is picked through the temper path, which can be every step.
  - That path needs more than one pending intention, at least one with `temper`. A lone intention never updates mood.
- **[V] and older upstream:** effects apply at option and intention selection.
- **[P] Def. 3.4:** effects apply at plan selection. The paper also calls them "post-effects … once executed". No version applies them at the end of a plan.
- **Effects without `temper`:** read independently, so they're syntactically allowed. They only apply if the temper path runs.
- **No mood change from a plan body.** The only internal actions are `vesna.walk`, `vesna.rotate` and `vesna.jump`, and mood is a private Java map. [P] says propensities are "mirrored as beliefs", but there is no such code in [U].
- **No decay.** [P] §4.1: "propensities do not decay over time in this scenario."

## 5. VEsNA-Pro's terms

| Term | Meaning |
|---|---|
| propensities | Umbrella term for personality and mood |
| Temper | The agent's whole set of propensities |
| personality / personality traits | Immutable propensities |
| mood | Mutable propensities |
| effects / post-effects | Mood changes a plan causes ([P]: "plan post-effect profile") |
| plan propensity / intention propensity | A plan's or intention's temper ([P]) |
| compatibility, most similar, random / stochastic | How selection scores and picks |

## Not confirmed

- Paper features with no code: `pr`/`eff` tag names, mirroring as beliefs, the fairness factor, aggregation, and the choice of metric.
- Forks (ZahraD-a/Vesna-pro-CFR, Vesna-pro-Mask, Vesna_with_RL) were not checked.
