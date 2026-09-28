# Regia questionnaire: summary of metrics

## Sample

- Respondents: 26
- CS only: 17
- CS + game: 6
- Game only: 3
- Without any computing background: 3
- Attempted the generation task: 10 of 26
- Rubric raters: 1 (A) -- single rater, no inter-rater reliability available

## Comprehension items, in questionnaire order

| Item | Q | Level | Metric | n | Mean | Median | Min | Max |
|---|---|---|---|---|---|---|---|---|
| C1 | Q3 | Playbook | normalised plus/minus | 26 | 0.73 | 1.00 | -0.17 | 1.00 |
| O1 | Q4 | Playbook | rubric proportion | 26 | 0.80 | 0.86 | 0.57 | 0.93 |
| O2 | Q5 | Playbook | rubric proportion | 26 | 0.91 | 1.00 | 0.50 | 1.00 |
| C2 | Q6 | Plot | normalised plus/minus | 26 | 0.77 | 1.00 | -0.17 | 1.00 |
| C3 | Q7 | Plot | normalised plus/minus | 26 | 0.76 | 0.75 | -1.00 | 1.00 |
| O3 | Q8 | Plot | rubric proportion | 26 | 0.81 | 0.83 | 0.42 | 1.00 |
| O4 | Q9 | Plot | rubric proportion | 26 | 0.80 | 0.79 | 0.43 | 1.00 |

## Closed options most often misjudged

| Option | Correct? | Selected by | Answered correctly by |
|---|---|---|---|
| C3_o4 | false | 34.6% | 65.4% |
| C2_o4 | false | 34.6% | 65.4% |
| C1_o4 | true | 69.2% | 69.2% |
| C3_o1 | false | 30.8% | 69.2% |
| C1_o1 | true | 84.6% | 84.6% |
| C2_o5 | true | 88.5% | 88.5% |

## Open rubric units with the lowest mean

| Item | Unit | Description | Mean (0-2) |
|---|---|---|---|
| O1 | U2 | applies to agents assigned NobleSocializing (role/playbook scope, not one guest) | 0.96 |
| O1 | U7 | nothing happens when the guard is false (no else branch) | 1.15 |
| O3 | U6 | the trigger is live throughout the phase, not only at entry | 1.23 |
| O4 | U7 | ON EXIT fires on leaving the phase, so UNASSIGN happens then | 1.27 |
| O4 | U5 | MAPPING Guest TO Challenger is a role mapping into the subplot | 1.38 |
| O3 | U1 | the block scopes behaviour to one phase of a plot | 1.46 |

## Generation task

- Respondents: 10 (self-selected: the task was optional)
- Semantic score: median 0.38, range 0.17-0.77
- Behaviours attempted: median 8 of 15
- Quality when attempted: median 0.69
- Syntax errors per 100 lines: median 13.89
- Submissions truncated by the form's length limit: 3

Errors by category (166 in total, across 10 submissions):

| Cat. | Description | Total | Share | Respondents | Max by one |
|---|---|---|---|---|---|
| E1 | pure syntax (missing dots, DO omitted, identifier case, block structure) | 89 | 53.6% | 10 of 10 | 24 |
| E2 | invented or malformed construct (WHEN true, SUBPLOT, SIGNAL, ...) | 24 | 14.5% | 6 of 10 | 9 |
| E3 | vocabulary used without being declared | 45 | 27.1% | 8 of 10 | 13 |
| E4 | plot-level construct inside a playbook (or vice versa) | 2 | 1.2% | 1 of 10 | 2 |
| E5 | vocabulary category confused (event used as action, FORGET on a non-fact) | 6 | 3.6% | 4 of 10 | 2 |

## Likert items

| # | Item | Characteristic | n valid | DK | Net agreement | Median |
|---|---|---|---|---|---|---|
| 1 | Completeness | Functional Suitability | 24 | 2 | +0.88 | 4.0 |
| 2 | Appropriateness | Functional Suitability | 25 | 1 | +0.96 | 4.0 |
| 3 | Comprehensibility | Usability | 26 | 0 | +0.58 | 4.0 |
| 4 | Learnability | Usability | 26 | 0 | +0.62 | 4.0 |
| 5 | Minimum steps | Usability | 24 | 2 | +0.71 | 4.0 |
| 6 | Likeability | Usability | 25 | 1 | +0.76 | 4.0 |
| 10 | Error protection | Reliability | 25 | 1 | -0.12 | 3.0 |
| 11 | Correctness | Reliability | 23 | 3 | +0.39 | 4.0 |
| 12 | Design reflection | Expressiveness | 24 | 2 | +0.50 | 4.0 |
| 13 | Uniqueness | Expressiveness | 21 | 5 | +0.10 | 3.0 |
| 14 | Orthogonality | Expressiveness | 25 | 1 | +0.76 | 4.0 |
| 15 | Necessity | Expressiveness | 20 | 6 | +0.65 | 4.0 |
| 16 | No conflicts | Expressiveness | 19 | 7 | +0.58 | 4.0 |
| 18 | Process fit | Compatibility | 23 | 3 | +0.87 | 4.0 |
| 23 | Power | MAS Development | 25 | 1 | +0.80 | 4.0 |

## Composites (descriptive only)

- Calibration, self-rated comprehensibility vs measured comprehension: rho = 0.31, 95% bootstrap interval [-0.05, 0.60] (n = 26)
  - agreeing it takes little effort (n = 19): median comprehension 0.86; the rest (n = 7): 0.76
- Convergence, closed J vs open rubric score: rho = 0.42 (n = 26)

Group medians:

| has_game_experience   |   n |   closed_score |   open_score |   comprehension |
|:----------------------|----:|---------------:|-------------:|----------------:|
| No game experience    |  17 |           0.81 |         0.83 |            0.82 |
| Game experience       |   9 |           0.81 |         0.86 |            0.88 |

| group     |   n |   closed_score |   open_score |   comprehension |
|:----------|----:|---------------:|-------------:|----------------:|
| CS + game |   6 |           0.9  |         0.87 |            0.89 |
| CS only   |  17 |           0.81 |         0.83 |            0.82 |
| Game only |   3 |           0.81 |         0.78 |            0.79 |

| attempted_generation   |   n |   closed_score |   open_score |   comprehension |
|:-----------------------|----:|---------------:|-------------:|----------------:|
| Did not attempt        |  16 |           0.82 |         0.81 |            0.84 |
| Attempted              |  10 |           0.81 |         0.88 |            0.84 |
