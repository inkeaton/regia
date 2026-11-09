# Labels and Propensities

How a Trigger carries Labels, which Labels exist, and the Propensities they name. Decided in the ticket *Label syntax and mood Labels* (`.scratch/regia-2/issues/15-label-syntax.md`). It builds on chapters 01, 05, 06 and 13, and replaces `PRIORITY`, `TEMPER` and `EFFECTS` in primer ch.1 and ch.4. The facts about VEsNA-Pro used here are in the research note on branch `research/vesna-pro-temper` (file `research/vesna-pro-temper.md`).

## Propensities

A **Propensity** is a named disposition of an Agent, used to choose between Plans and changed by running them. The word comes from VEsNA-Pro. There are two kinds:

- a **Trait** never changes during a run (VEsNA-Pro's personality);
- a **Mood** changes as the Agent runs Plans.

Both are declared in the Vocabulary:

```regia
TRAIT bravery
MOOD sympathy, aggressiveness
```

- Propensities take **no parameters**.
- They share the Program's one flat namespace and its one-kind-per-name rule (chapter 10, ADR 0006). `MOOD angry` and `FACT angry` is an error.
- They are declared at **file level only**, like `EVENT` and `ACTION`. A Propensity belongs to the whole Agent, never to one Playbook.
- They may give an External name with `<external> AS <name>` (chapter 10), for when the Target calls them something else.
- Matching re-declarations merge (chapter 10).
- **Starting values come from Instancing**, per Agent (VEsNA-Pro: the `temper(...)` parameter in the `.jcm`). The `#%` syntax for them is decided in *Instancing comments*. An Agent with no value for a Propensity is the Target's business; VEsNA-Pro skips it.
- **Propensities are not Facts.** In 2.0 a Context can't test them and no Action changes them. Only Labels mention them.

## Writing Labels

Labels come last on a Trigger's header, after the item, its kind word and `FROM` (chapter 05). Each one starts with `, KEYWORD`:

```regia
WHEN insult_heard, SUITS sympathy AT -0.5, SHIFTS aggressiveness BY 0.2:
    DO complain.
```

- Labels can come **in any order**. Each Label appears **at most once** on a header.
- A Label naming several Propensities joins them with **`AND`**: `SUITS sympathy AT -0.5 AND bravery AT 0.8`. A `,` always starts the next Label.
- Naming the same Propensity twice in one Label is an error.
- A long header wraps after any `,` (chapter 01):

  ```regia
  WHEN hates(?h) LEARNED FROM ?teller,
          SUITS sympathy AT -0.5 AND bravery AT 0.8,
          SHIFTS aggressiveness BY 0.2:
      ...
  ```

- The same `,` shape is used by `, WEIGHT` on `EITHER`/`OR` (chapter 09) and `, WITHOUT WAITING` (chapter 08). Weights are not Labels.

## The Labels

The set is **fixed by the language**. A Target can't add its own. 2.0 has exactly two:

| Label | Form | Names | Meaning |
|---|---|---|---|
| **Suits** | `SUITS p AT n [AND …]` | Traits and Moods | The Plan best fits an Agent whose `p` is close to `n`. The Selection function uses it to choose (chapter 13). |
| **Shifts** | `SHIFTS m BY n [AND …]` | Moods only | Running the Plan changes Mood `m` by `n` (signed). |

- **Values** are Number literals between -1 and 1, inclusive. A value outside that range, an Expression or a Placeholder is an error. Labels are fixed when the Program is written, so they can't depend on a run.
- A name that isn't a declared Propensity is an error. So is `SHIFTS` naming a Trait.
- **Only `SUITS` affects which Plan runs.** A Trigger Block with only `SHIFTS` is an ordinary Trigger Block: first in the text wins (chapter 13), and it can sit next to unlabelled Trigger Blocks for the same Trigger.
- **When a Shift applies belongs to the Target.** The language promises only that running the Plan shifts those Moods. What the Mood's value is kept within (VEsNA-Pro clips to [-1, 1]) also belongs to the Target.

## Where Labels go

| Header | `SUITS` | `SHIFTS` |
|---|---|---|
| `WHEN …` / `TO …` in a Playbook | yes | yes |
| `GIVEN …` / `ELSE` under a Trigger | **error** | yes |
| A Director's Plans (in a Plot) | **error** | **error** |

- **On a Trigger**, Labels apply to every Plan under it: each `GIVEN` and the `ELSE` (chapter 06).
- **On a `GIVEN` or `ELSE`**, `SHIFTS` adds to the Trigger's own `SHIFTS` for that one Plan. The same Mood in both is an error.

  ```regia
  WHEN insult_heard, SHIFTS sympathy BY -0.1:
      GIVEN hates(host), SHIFTS aggressiveness BY 0.2: DO complain.
      ELSE: DO toast(host).
  ```

  Complaining lowers sympathy and raises aggressiveness. Toasting only lowers sympathy.
- `SUITS` is never allowed on a `GIVEN` or `ELSE`, since `GIVEN` siblings never compete (chapter 13).
- **On a Director's Plans**, any Label is an error until *Director capabilities* decides whether Directors have Propensities.

## Suits alternatives

Chapter 13's rule, restated in terms of `SUITS`:

- Trigger Blocks in one Playbook with the same Trigger, all carrying `SUITS`, are **Suits alternatives**. The Selection function picks one of those whose Context holds.
- **Mixing is an error.** For one Trigger in one Playbook, either every Trigger Block carries `SUITS` or none does. `SHIFTS` doesn't count.
- **There is no neutral alternative.** Every alternative says what it suits. For a "default" reaction, give it the values of an ordinary Agent (`SUITS sympathy AT 0`).
- **`TIES` pools that mix** `SUITS` candidates with unlabelled ones (from different Playbooks, chapter 13) are allowed. How an unlabelled candidate ranks against a labelled one belongs to the Target, and the Transpiler **warns** once per pool. On VEsNA-Pro an unlabelled candidate counts as a perfect fit and wins under the default strategy (*ASL mapping notes*).

## Targets without Labels

A Target that doesn't support a Label **ignores** it, with **one warning per Program per Label** ("`SUITS` has no effect on Target X"). The Program still compiles. Ignoring `SUITS` means Suits alternatives fall back to text order and `TIES` to name order (chapter 13). Ignoring `SHIFTS` means Moods never change.

## Transpiler checks

**Errors**

- An unknown Label keyword, or a Label repeated on one header.
- A Propensity named twice in one Label, or in both a Trigger's `SHIFTS` and a `GIVEN`'s.
- A name in `SUITS` that isn't a declared Propensity, or a name in `SHIFTS` that isn't a declared Mood.
- A value that isn't a Number literal, or that lies outside [-1, 1].
- `SUITS` on a `GIVEN` or `ELSE`. Any Label on a Director's Plan.
- Mixing Trigger Blocks with and without `SUITS` for one Trigger in one Playbook (chapter 13).
- A `TRAIT` or `MOOD` declared inside a `PLAYBOOK` or `PLOT`.

**Warnings**

- A Label the Target doesn't support (once per Program per Label).
- A `TIES` pool mixing `SUITS` and unlabelled candidates (once per pool).
- A declared Propensity that no Label names.

## Reserved words

`TRAIT`, `MOOD`, `SUITS`, `SHIFTS`, `AT`, `BY`. `AND` is shared with Contexts. `TEMPER`, `EFFECTS` and `PRIORITY` are not words of the language.

## Not in 2.0

Map: *Not yet specified*.

- **A `SHIFT` Body Statement** (`SHIFT aggressiveness BY 0.2.`), to change a Mood from inside an `IF` branch or at a precise point. VEsNA-Pro has no way to change a Mood from a Body today.
- **A neutral ranking defined by the language** ("an unlabelled candidate loses to any fitting alternative"). It needs a change to VEsNA-Pro's scoring.
- **Testing Propensities in a Context** (`GIVEN aggressiveness > 0.5`).
- Named value levels (`SUITS sympathy AT LOW`), alongside named Weight levels.
- Labels from other Targets.

## ASL mapping notes

For *The full ASL mapping* to pick up. VEsNA-Pro facts are from the research note above, as of upstream commit `3f857f5`.

- `SUITS p AT a AND q AT b` becomes the plan annotation `temper([p(a), q(b)])`. `SHIFTS m BY d` becomes `effects([m(d)])`. A `GIVEN`'s `SHIFTS` merges into its own plan's `effects` list. External names replace Regia names.
- **Propensity values** go into the Agent's `.jcm` as `temper(t1(v), …, m1(v)[mood], …)`, with Moods tagged `[mood]`. The `strategy` parameter (`most_similar` or `random`) must be set, or VEsNA-Pro crashes. Picking it belongs to Instancing.
- **Known VEsNA-Pro behaviour** that the language doesn't promise:
  - A plan without `temper` scores as a perfect fit. Under `most_similar` it beats every labelled plan that doesn't fit exactly; under `random` it is almost never picked.
  - Effects apply only when the temper path picks an intention: at least two pending intentions, one with `temper`. A lone running Plan never shifts a Mood, and a contested one may shift it at every step.
  - Personality values are kept in [0, 1] in the code but [-1, 1] in the paper. A Mood that would drop below -1 is set to 0 (a bug). The 1.0 vendored copy never runs temper-based intention selection (another bug).
- Spec 13's ranking runs in `selectOption` before temper selection, so VEsNA-Pro only ever compares candidates of equal rank.

## Not decided here

- The `#%` syntax for Propensity values and the VEsNA strategy: *Instancing comments*.
- Whether Directors have Propensities: *Director capabilities*.
- How Labels and Propensities map on Targets other than Jason+VEsNA: *Supporting multiple Targets*.
