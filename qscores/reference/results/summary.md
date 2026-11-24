# Regia questionnaire: summary of metrics

## Sample

- Respondents: 32
- CS only: 22
- CS + game: 7
- Game only: 3
- Without any computing background: 3
- Attempted the generation task: 11 of 32
- Rubric raters: 1 (A) -- single rater, no inter-rater reliability available

## Overall scores

Median and interquartile range per respondent (quartile method: linear).

| Score | n | Median | Q1 | Q3 | Min | Max |
|---|---|---|---|---|---|---|
| Comprehension (all seven items) | 32 | 0.84 | 0.73 | 0.90 | 0.28 | 0.99 |
| Multi-select items (plus/minus) | 32 | 0.81 | 0.70 | 0.92 | -0.33 | 1.00 |
| Explanation items (rubric) | 32 | 0.86 | 0.79 | 0.90 | 0.58 | 0.98 |

## Comprehension items, in questionnaire order

| Item | Q | Level | Metric | n | Mean | Median | Min | Max |
|---|---|---|---|---|---|---|---|---|
| C1 | Q3 | Playbook | normalised plus/minus | 32 | 0.75 | 1.00 | -0.17 | 1.00 |
| O1 | Q4 | Playbook | rubric proportion | 32 | 0.81 | 0.86 | 0.57 | 0.93 |
| O2 | Q5 | Playbook | rubric proportion | 32 | 0.92 | 1.00 | 0.50 | 1.00 |
| C2 | Q6 | Plot | normalised plus/minus | 32 | 0.76 | 1.00 | -0.17 | 1.00 |
| C3 | Q7 | Plot | normalised plus/minus | 32 | 0.77 | 0.75 | -1.00 | 1.00 |
| O3 | Q8 | Plot | rubric proportion | 32 | 0.80 | 0.83 | 0.17 | 1.00 |
| O4 | Q9 | Plot | rubric proportion | 32 | 0.80 | 0.79 | 0.36 | 1.00 |

## Closed options most often misjudged

| Option | Correct? | Selected by | Answered correctly by |
|---|---|---|---|
| C3_o4 | false | 34.4% | 65.6% |
| C2_o4 | false | 34.4% | 65.6% |
| C1_o4 | true | 71.9% | 71.9% |
| C3_o1 | false | 28.1% | 71.9% |
| C1_o1 | true | 84.4% | 84.4% |
| C2_o5 | true | 87.5% | 87.5% |

## Open rubric units with the lowest mean

| Item | Unit | Description | Mean (0-2) |
|---|---|---|---|
| O1 | U2 | applies to agents assigned NobleSocializing (role/playbook scope, not one guest) | 1.03 |
| O1 | U7 | nothing happens when the guard is false (no else branch) | 1.12 |
| O3 | U6 | the trigger is live throughout the phase, not only at entry | 1.22 |
| O4 | U7 | ON EXIT fires on leaving the phase, so UNASSIGN happens then | 1.31 |
| O4 | U5 | MAPPING Guest TO Challenger is a role mapping into the subplot | 1.44 |
| O4 | U1 | ON ENTER -> serve_wine at world level | 1.50 |

## All open rubric units, by mean

| Rank | Item | Unit | Description | Mean (0-2) | Coded 2 | Coded 1 | Coded 0 |
|---|---|---|---|---|---|---|---|
| 1 | O1 | U2 | applies to agents assigned NobleSocializing (role/playbook scope, not one guest) | 1.03 | 10 | 13 | 9 |
| 2 | O1 | U7 | nothing happens when the guard is false (no else branch) | 1.12 | 4 | 28 | 0 |
| 3 | O3 | U6 | the trigger is live throughout the phase, not only at entry | 1.22 | 9 | 21 | 2 |
| 4 | O4 | U7 | ON EXIT fires on leaving the phase, so UNASSIGN happens then | 1.31 | 19 | 4 | 9 |
| 5 | O4 | U5 | MAPPING Guest TO Challenger is a role mapping into the subplot | 1.44 | 16 | 14 | 2 |
| 6 | O4 | U1 | ON ENTER -> serve_wine at world level | 1.50 | 19 | 10 | 3 |
| 7 | O3 | U1 | the block scopes behaviour to one phase of a plot | 1.50 | 17 | 14 | 1 |
| 8 | O4 | U2 | trigger is a SIGNAL raised BY an agent playing Guest (bottom-up) | 1.59 | 20 | 11 | 1 |
| 9 | O3 | U4 | ASSIGN targets the Guest ROLE, hence all its occupants | 1.62 | 22 | 8 | 2 |
| 10 | O4 | U6 | TRANSITION TO duel_interruption | 1.62 | 23 | 6 | 3 |
| 11 | O3 | U2 | ON ENTER fires once, at phase entry | 1.66 | 25 | 3 | 4 |
| 12 | O1 | U1 | triggered by the digestion_check event | 1.66 | 22 | 9 | 1 |
| 13 | O3 | U3 | WORLD DO is an environment/director-level action, not an agent's | 1.75 | 25 | 6 | 1 |
| 14 | O2 | U4 | AND NOT hates(host) - both conjuncts, correct precedence | 1.78 | 26 | 5 | 1 |
| 15 | O2 | U2 | PRINT executes unconditionally, before the test | 1.78 | 26 | 5 | 1 |
| 16 | O2 | U1 | triggered by the food_served event | 1.78 | 26 | 5 | 1 |
| 17 | O4 | U3 | stop_music executes | 1.78 | 27 | 3 | 2 |
| 18 | O1 | U6 | PRINT emits the message | 1.81 | 28 | 2 | 2 |
| 19 | O3 | U5 | WHEN food_served causes TRANSITION TO feast | 1.84 | 29 | 1 | 2 |
| 20 | O1 | U5 | FORGET retracts the is_hungry belief | 1.88 | 29 | 2 | 1 |
| 21 | O2 | U3 | condition includes (is_hungry OR is_drunk) | 1.91 | 29 | 3 | 0 |
| 22 | O2 | U6 | complain on the else branch | 1.91 | 29 | 3 | 0 |
| 23 | O1 | U4 | eat_food executes when the guard holds | 1.94 | 30 | 2 | 0 |
| 24 | O1 | U3 | body guarded by the is_hungry fact | 1.94 | 30 | 2 | 0 |
| 25 | O2 | U5 | eat_food on true | 1.94 | 30 | 2 | 0 |
| 26 | O4 | U4 | START SUBPLOT HonorDuel | 1.94 | 30 | 2 | 0 |

## Generation task

- Respondents: 11 (self-selected: the task was optional)
- Semantic score: median 0.40, range 0.17-1.00
- Quality when attempted: median 0.70, range 0.60-1.00
- Behaviours attempted: median 9 of 15, range 4-15
- Non-blank lines written: median 123, range 7-145
- Syntax errors per 100 lines: median 11.11
- Submissions truncated by the form's length limit: 3

Errors by category (167 in total, across 11 submissions):

| Cat. | Description | Total | Share | Respondents | Max by one |
|---|---|---|---|---|---|
| E1 | pure syntax (missing dots, DO omitted, identifier case, block structure) | 89 | 53.3% | 10 of 11 | 24 |
| E2 | invented or malformed construct (WHEN true, SUBPLOT, SIGNAL, ...) | 24 | 14.4% | 6 of 11 | 9 |
| E3 | vocabulary used without being declared | 46 | 27.5% | 9 of 11 | 13 |
| E4 | plot-level construct inside a playbook (or vice versa) | 2 | 1.2% | 1 of 11 | 2 |
| E5 | vocabulary category confused (event used as action, FORGET on a non-fact) | 6 | 3.6% | 4 of 11 | 2 |

## Likert items

| # | Item | Characteristic | n valid | DK | Net agreement | Median |
|---|---|---|---|---|---|---|
| 1 | Completeness | Functional Suitability | 29 | 3 | +0.79 | 4.0 |
| 2 | Appropriateness | Functional Suitability | 31 | 1 | +0.97 | 4.0 |
| 3 | Comprehensibility | Usability | 32 | 0 | +0.50 | 4.0 |
| 4 | Learnability | Usability | 32 | 0 | +0.66 | 4.0 |
| 5 | Minimum steps | Usability | 30 | 2 | +0.70 | 4.0 |
| 6 | Likeability | Usability | 31 | 1 | +0.81 | 4.0 |
| 10 | Error protection | Reliability | 29 | 3 | +0.00 | 3.0 |
| 11 | Correctness | Reliability | 27 | 5 | +0.37 | 4.0 |
| 12 | Design reflection | Expressiveness | 30 | 2 | +0.50 | 4.0 |
| 13 | Uniqueness | Expressiveness | 26 | 6 | +0.08 | 3.0 |
| 14 | Orthogonality | Expressiveness | 29 | 3 | +0.79 | 4.0 |
| 15 | Necessity | Expressiveness | 26 | 6 | +0.62 | 4.0 |
| 16 | No conflicts | Expressiveness | 24 | 8 | +0.62 | 4.0 |
| 18 | Process fit | Compatibility | 26 | 6 | +0.88 | 4.0 |
| 23 | Power | MAS Development | 30 | 2 | +0.83 | 4.0 |

## Likert characteristics (pooled across their measures)

| Characteristic | Measures | n valid | DK | Net agreement |
|---|---|---|---|---|
| Compatibility | 18 | 26 | 6 | +0.885 |
| Functional Suitability | 1, 2 | 60 | 4 | +0.883 |
| MAS Development | 23 | 30 | 2 | +0.833 |
| Usability | 3, 4, 5, 6 | 125 | 3 | +0.664 |
| Expressiveness | 12, 13, 14, 15, 16 | 135 | 25 | +0.526 |
| Reliability | 10, 11 | 56 | 8 | +0.179 |

## Composites (descriptive only)

- Calibration, self-rated comprehensibility vs measured comprehension: rho = 0.29, 95% bootstrap interval [-0.03, 0.55] (n = 32)
  - agreeing it takes little effort (n = 22): median comprehension 0.86; the rest (n = 10): 0.76
- Convergence, closed J vs open rubric score: rho = 0.50 (n = 32)

Group medians:

| has_game_experience   |   n |   closed_score |   open_score |   comprehension |
|:----------------------|----:|---------------:|-------------:|----------------:|
| No game experience    |  22 |           0.79 |         0.85 |            0.81 |
| Game experience       |  10 |           0.85 |         0.87 |            0.88 |

| group     |   n |   closed_score |   open_score |   comprehension |
|:----------|----:|---------------:|-------------:|----------------:|
| CS + game |   7 |           0.92 |         0.89 |            0.9  |
| CS only   |  22 |           0.79 |         0.85 |            0.81 |
| Game only |   3 |           0.81 |         0.78 |            0.79 |

| attempted_generation   |   n |   closed_score |   open_score |   comprehension |
|:-----------------------|----:|---------------:|-------------:|----------------:|
| Did not attempt        |  21 |           0.81 |         0.83 |            0.84 |
| Attempted              |  11 |           0.81 |         0.88 |            0.86 |
