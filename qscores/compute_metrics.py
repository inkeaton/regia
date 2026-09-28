#!/usr/bin/env python3
"""
Computes every questionnaire metric reported in Section 8.3.

Inputs, read from DATA_DIR:
    data.xlsx            raw form export (backgrounds, closed and open answers, Likert)
    answer_key.csv       correct options for the three closed questions
    coding_sheet_A.csv   0/1/2 rubric codes for the four open questions
    gen_behaviour.csv    0/1/2 rubric codes for the generation task's behaviours
    gen_syntax.csv       syntax-error counts for the generation task

Outputs, written to OUT_DIR:
    respondents.csv          one row per respondent: background, every score, composites
    closed_items.csv         per respondent x closed item: confusion counts, sensitivity,
                             normalised plus/minus score
    closed_options.csv       per option: selection rate, correctness
    open_items.csv           per respondent x open item: rubric proportion
    open_units.csv           per rubric unit: mean code, distribution
    items_summary.csv        all seven comprehension items in questionnaire order
    generation.csv           per generation respondent: semantic and syntax scores
    generation_behaviours.csv per specified behaviour: coverage across respondents
    generation_errors.csv    per syntax-error category: totals, share, respondents affected
    likert_items.csv         per Likert item: distribution, net agreement, median
    likert_characteristics.csv per AgentDSM-Eval characteristic: pooled net agreement
    summary.md               the headline figures, in readable form

All figures are descriptive. With N = 21, a ceiling effect on the comprehension
items, and a population that is mostly computer scientists, no significance
test is computed; correlations are reported as coefficients only.

Usage:  python3 compute_metrics.py [DATA_DIR] [OUT_DIR] [--exclude ID ...]

    --exclude drops the given respondent IDs before any metric is computed, for
    sensitivity analysis. Report which respondents were excluded and why; an
    exclusion decided after seeing the scores must be presented as such.
"""

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from form_data import load_form_rows

parser = argparse.ArgumentParser(description="Compute the Regia questionnaire metrics.")
parser.add_argument("data_dir", nargs="?", default=".")
parser.add_argument("out_dir", nargs="?", default="results")
parser.add_argument("--exclude", type=int, nargs="*", default=[], metavar="ID",
                    help="respondent IDs to drop, for sensitivity analysis")
args = parser.parse_args()
DATA_DIR, OUT_DIR, EXCLUDE = Path(args.data_dir), Path(args.out_dir), set(args.exclude)
OUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Configuration
# =============================================================================

# Column indices in data.xlsx (0-based).
COL_ID, COL_BACKGROUND = 0, 7
COL_GENERATION, COL_COMMENTS = 15, 31
LIKERT_COLS = list(range(16, 31))

# The seven comprehension items, in questionnaire order. Question numbers follow
# the form, where Q1 is the AI-use declaration and Q2 the background question. Each is tagged with the
# language level it tests, so results can be presented by level (Playbook, then
# Plot) rather than by question type.
ITEMS = [
    # id    question  type      column  level       constructs
    ("C1", "Q3", "closed", 8,  "Playbook", "WHEN with PRIORITY, TEMPER, EFFECTS; IF/ELSE; SIGNAL"),
    ("O1", "Q4", "open",   9,  "Playbook", "WHEN, IF, FORGET, PRINT"),
    ("O2", "Q5", "open",   10, "Playbook", "prefix statement, compound condition"),
    ("C2", "Q6", "closed", 11, "Plot",     "Plot header: PHASE INITIAL, ROLE"),
    ("C3", "Q7", "closed", 12, "Plot",     "DURING PLOT, WORLD DO, Role DO, END PLOT"),
    ("O3", "Q8", "open",   13, "Plot",     "DURING phase, ON ENTER, ASSIGN, TRANSITION"),
    ("O4", "Q9", "open",   14, "Plot",     "WHEN ROLE SIGNALS, START SUBPLOT, ON EXIT, UNASSIGN"),
]
ITEM_META = pd.DataFrame(ITEMS, columns=["item", "question", "type", "column", "level", "constructs"])

# The fifteen Likert items retained from AgentDSM-Eval's twenty-four quality
# measures (Alaca et al., Table 2.1), with their measure number and characteristic.
LIKERT_ITEMS = [
    (1,  "Completeness",      "Functional Suitability"),
    (2,  "Appropriateness",   "Functional Suitability"),
    (3,  "Comprehensibility", "Usability"),
    (4,  "Learnability",      "Usability"),
    (5,  "Minimum steps",     "Usability"),
    (6,  "Likeability",       "Usability"),
    (10, "Error protection",  "Reliability"),
    (11, "Correctness",       "Reliability"),
    (12, "Design reflection", "Expressiveness"),
    (13, "Uniqueness",        "Expressiveness"),
    (14, "Orthogonality",     "Expressiveness"),
    (15, "Necessity",         "Expressiveness"),
    (16, "No conflicts",      "Expressiveness"),
    (18, "Process fit",       "Compatibility"),
    (23, "Power",             "MAS Development"),
]
LIKERT_SCALE = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
LIKERT_DK = "I do not know"
COMPREHENSIBILITY_MEASURE = 3        # used for the calibration analysis

# Error categories recorded in gen_syntax.csv.
SYNTAX_ERROR_LABELS = {
    "E1": "pure syntax (missing dots, DO omitted, identifier case, block structure)",
    "E2": "invented or malformed construct (WHEN true, SUBPLOT, SIGNAL, ...)",
    "E3": "vocabulary used without being declared",
    "E4": "plot-level construct inside a playbook (or vice versa)",
    "E5": "vocabulary category confused (event used as action, FORGET on a non-fact)",
}

# Generation rubric: '-' marks a behaviour not attempted, '0' one attempted but
# wrong. Both score zero on the 0/1/2 scale; attempted coverage is reported
# separately so the two are not conflated.
BEHAVIOUR_CODE = {"2": 2, "1": 1, "0": 0, "-": 0}
NOT_ATTEMPTED = "-"


def norm(text):
    """Collapse whitespace so option texts match however the form spaced them."""
    return re.sub(r"\s+", " ", str(text)).strip()


# =============================================================================
# Respondents and backgrounds
# =============================================================================

_, raw_rows = load_form_rows(DATA_DIR / "data.xlsx")
raw = [r for r in raw_rows if int(r[0]) not in EXCLUDE]

respondents = pd.DataFrame({"respondent": [int(r[COL_ID]) for r in raw]})
background = [str(r[COL_BACKGROUND] or "") for r in raw]
respondents["bg_cs"] = [("Computer science" in b) for b in background]
respondents["bg_design"] = [("design" in b) for b in background]
respondents["bg_dev"] = [("development" in b) for b in background]
respondents["bg_game"] = respondents["bg_design"] | respondents["bg_dev"]


def group_of(row):
    if row.bg_cs and not row.bg_game:
        return "CS only"
    if row.bg_cs and row.bg_game:
        return "CS + game"
    if row.bg_game:
        return "Game only"
    return "Other"


respondents["group"] = respondents.apply(group_of, axis=1)
# The primary comparison available in this sample: programmers with and without
# game experience. It is NOT a programmer/designer comparison; only the
# "Game only" respondents lack a computing background.
respondents["has_game_experience"] = respondents["bg_game"]
respondents["attempted_generation"] = [bool(r[COL_GENERATION] and str(r[COL_GENERATION]).strip())
                                       for r in raw]


# =============================================================================
# Closed questions: normalised plus/minus scoring
# =============================================================================
#
# Each closed question offers five statements, any subset of which may be true;
# a statement left unselected is judged false. Each correct selection earns
# 1/n_true and each incorrect selection costs 1/n_false:
#
#     score = TP / n_true - FP / n_false
#
# Normalising each class by its own size matters because the keys are
# unbalanced (3/2, 2/3, 1/4 true/false): without it, one wrong selection on an
# item with a single true statement cancels its full credit. Selecting every
# statement and selecting none both score 0. The score coincides with Youden's
# J = sensitivity + specificity - 1, since specificity = 1 - FP / n_false.

key = pd.read_csv(DATA_DIR / "answer_key.csv")
key["text_norm"] = key["option_text"].map(norm)

# Guard: substring matching is only safe if no option contains another.
for item, grp in key.groupby("item"):
    texts = grp["text_norm"].tolist()
    for a in texts:
        for b in texts:
            assert a == b or a not in b, f"{item}: an option text is a substring of another"

closed_rows, selections = [], {}
for item_id, question, typ, col, level, _ in ITEMS:
    if typ != "closed":
        continue
    options = key[key["item"] == item_id]
    for r in raw:
        rid = int(r[COL_ID])
        answer = norm(r[col] or "")
        chosen = {o.option_id for o in options.itertuples() if o.text_norm in answer}
        selections[(rid, item_id)] = chosen
        tp = sum(1 for o in options.itertuples() if o.is_correct == 1 and o.option_id in chosen)
        fn = sum(1 for o in options.itertuples() if o.is_correct == 1 and o.option_id not in chosen)
        fp = sum(1 for o in options.itertuples() if o.is_correct == 0 and o.option_id in chosen)
        tn = sum(1 for o in options.itertuples() if o.is_correct == 0 and o.option_id not in chosen)
        n_true, n_false = tp + fn, fp + tn   # both >= 1 for every item
        closed_rows.append(dict(respondent=rid, item=item_id, question=question, level=level,
                                tp=tp, fn=fn, fp=fp, tn=tn,
                                plus_minus=tp / n_true - fp / n_false))
closed = pd.DataFrame(closed_rows)

# Verify the parsing against the selection counts stored in the key.
key["n_selected_recomputed"] = [sum(1 for (rid, it), ch in selections.items()
                                    if it == o.item and o.option_id in ch)
                                for o in key.itertuples()]
mismatch = (key[key["n_selected"] != key["n_selected_recomputed"]]
            if not EXCLUDE else key.iloc[0:0])   # the key's counts describe the full sample
if not mismatch.empty:
    print("WARNING: parsed selection counts differ from answer_key.csv:")
    print(mismatch[["option_id", "n_selected", "n_selected_recomputed"]].to_string(index=False))

n_resp = len(respondents)
closed_options = key[["item", "option_id", "is_correct", "option_text"]].copy()
closed_options["n_selected"] = key["n_selected_recomputed"]
closed_options["selection_rate"] = closed_options["n_selected"] / n_resp
# For a true option the selection rate is the share answering correctly; for a
# false option it is the share holding that misconception.
closed_options["correct_rate"] = np.where(closed_options["is_correct"] == 1,
                                          closed_options["selection_rate"],
                                          1 - closed_options["selection_rate"])


# =============================================================================
# Open questions: 0/1/2 analytic rubric
# =============================================================================
#
# Each rubric unit is coded 2 (covered thoroughly), 1 (covered in less detail),
# or 0 (absent). An item's score is its total over twice its number of units,
# so items with more units do not dominate an average.

coding = pd.read_csv(DATA_DIR / "coding_sheet_A.csv")
coding = coding[~coding["respondent"].isin(EXCLUDE)]
raters = sorted(coding["rater"].dropna().unique())

uncoded = coding[coding["code"].isna()]
provisional = coding[coding["flag"].fillna("").str.startswith("PROVISIONAL")]
uncoded_items = uncoded.groupby(["respondent", "item"]).size().reset_index(name="uncoded_units")

open_rows = []
for (rid, item_id), grp in coding.groupby(["respondent", "item"]):
    n_units = grp["unit"].nunique()
    coded = grp["code"].notna().all()
    score = grp["code"].sum() / (2 * n_units) if coded else np.nan
    meta = ITEM_META.set_index("item").loc[item_id]
    open_rows.append(dict(respondent=int(rid), item=item_id, question=meta.question, level=meta.level,
                          n_units=n_units, total=grp["code"].sum() if coded else np.nan,
                          rubric_score=score))
open_items = pd.DataFrame(open_rows)

open_units = (coding.dropna(subset=["code"])
              .groupby(["item", "unit", "unit_desc"])["code"]
              .agg(mean_code="mean", n="size",
                   n2=lambda s: (s == 2).sum(), n1=lambda s: (s == 1).sum(), n0=lambda s: (s == 0).sum())
              .reset_index())
open_units["mean_proportion"] = open_units["mean_code"] / 2


def weighted_kappa(a, b, k=3):
    """Quadratically weighted Cohen's kappa for two raters on a 0..k-1 scale."""
    a, b = np.asarray(a, int), np.asarray(b, int)
    observed = np.zeros((k, k))
    for i, j in zip(a, b):
        observed[i, j] += 1
    observed /= observed.sum()
    expected = np.outer(observed.sum(1), observed.sum(0))
    weights = np.array([[(i - j) ** 2 for j in range(k)] for i in range(k)]) / (k - 1) ** 2
    return 1 - (weights * observed).sum() / (weights * expected).sum()


kappa = None
if len(raters) > 1:
    # Only runs if a second rater's codes are added to the coding sheet.
    wide = coding.pivot_table(index=["respondent", "item", "unit"], columns="rater", values="code").dropna()
    kappa = weighted_kappa(wide[raters[0]], wide[raters[1]])


# =============================================================================
# Per-item summary, in questionnaire order
# =============================================================================
#
# Closed items contribute their plus/minus score and open items their rubric
# proportion. Both reach 1 for a perfect answer, but their zeros differ in
# meaning: a plus/minus score of 0 is what selecting everything or nothing
# earns, a rubric score of 0 is an answer covering nothing. The metric column
# records which applies so the two are never read as the same quantity.

items_summary = []
for item_id, question, typ, col, level, constructs in ITEMS:
    if typ == "closed":
        s = closed.loc[closed["item"] == item_id, "plus_minus"]
        metric = "normalised plus/minus"
    else:
        s = open_items.loc[open_items["item"] == item_id, "rubric_score"]
        metric = "rubric proportion"
    items_summary.append(dict(item=item_id, question=question, type=typ, level=level, constructs=constructs,
                              metric=metric, n=int(s.notna().sum()), mean=s.mean(), median=s.median(),
                              sd=s.std(), min=s.min(), max=s.max()))
items_summary = pd.DataFrame(items_summary)


# =============================================================================
# Generation task
# =============================================================================

gen_beh = pd.read_csv(DATA_DIR / "gen_behaviour.csv", dtype={"code": str})
gen_beh = gen_beh[~gen_beh["respondent"].isin(EXCLUDE)]
gen_beh["code"] = gen_beh["code"].str.strip()

# A respondent whose behaviour rows are not yet fully coded is left out of the
# generation results and reported instead, so that a partly coded sheet cannot
# quietly depress the scores.
uncoded_generation = sorted(int(r) for r in gen_beh.loc[gen_beh["code"].isna(), "respondent"].unique())
gen_beh = gen_beh[~gen_beh["respondent"].isin(uncoded_generation)]
gen_beh["score"] = gen_beh["code"].map(BEHAVIOUR_CODE)
gen_beh["attempted"] = gen_beh["code"] != NOT_ATTEMPTED
gen_beh["truncated"] = gen_beh["flag"].fillna("").str.contains("truncat", case=False)
n_behaviours = gen_beh["behaviour"].nunique()

generation = (gen_beh.groupby("respondent")
              .agg(semantic_total=("score", "sum"),
                   behaviours_attempted=("attempted", "sum"),
                   full_marks=("code", lambda s: (s == "2").sum()),
                   truncated=("truncated", "any"))
              .reset_index())
generation["semantic_score"] = generation["semantic_total"] / (2 * n_behaviours)
generation["attempted_rate"] = generation["behaviours_attempted"] / n_behaviours
# Quality among what was attempted, separating "wrote it badly" from "did not write it".
attempted_only = gen_beh[gen_beh["attempted"]].groupby("respondent")["score"].mean() / 2
generation["quality_when_attempted"] = generation["respondent"].map(attempted_only)

gen_syn = pd.read_csv(DATA_DIR / "gen_syntax.csv")
gen_syn = gen_syn[~gen_syn["respondent"].isin(EXCLUDE)]
err_cols = [c for c in gen_syn.columns if re.fullmatch(r"E\d+", c)]
uncoded_syntax = sorted(int(r) for r in gen_syn.loc[gen_syn[err_cols].isna().all(axis=1), "respondent"].unique())
gen_syn = gen_syn[~gen_syn["respondent"].isin(uncoded_syntax)]
gen_syn["syntax_errors"] = gen_syn[err_cols].sum(axis=1)
# Longer submissions have more opportunity for error, so the count is also
# normalised by length.
gen_syn["errors_per_100_lines"] = 100 * gen_syn["syntax_errors"] / gen_syn["nonblank_lines"]
generation = generation.merge(gen_syn, on="respondent", how="left")

# Per-category breakdown: totals alone would hide that a few submissions
# contribute most of the errors, so respondents affected and the largest
# single contribution are reported alongside.
total_errors = np.nansum(gen_syn[err_cols].to_numpy())
generation_errors = pd.DataFrame([dict(
    category=c, label=SYNTAX_ERROR_LABELS.get(c, c),
    total=int(gen_syn[c].sum()), share=gen_syn[c].sum() / total_errors if total_errors else np.nan,
    respondents_affected=int((gen_syn[c] > 0).sum()), max_by_one=int(gen_syn[c].max()),
    median_per_respondent=float(gen_syn[c].median())) for c in err_cols])

beh_order = sorted(gen_beh["behaviour"].unique(), key=lambda b: int(b[1:]))
generation_behaviours = (gen_beh.groupby(["behaviour", "desc"])
                         .agg(n=("code", "size"),
                              n2=("code", lambda s: (s == "2").sum()),
                              n1=("code", lambda s: (s == "1").sum()),
                              n0=("code", lambda s: (s == "0").sum()),
                              not_attempted=("code", lambda s: (s == NOT_ATTEMPTED).sum()),
                              mean_score=("score", "mean"))
                         .reset_index())
generation_behaviours["mean_proportion"] = generation_behaviours["mean_score"] / 2
generation_behaviours["order"] = generation_behaviours["behaviour"].map(lambda b: int(b[1:]))
generation_behaviours = generation_behaviours.sort_values("order").drop(columns="order")


# =============================================================================
# Likert items: net agreement
# =============================================================================
#
# "I do not know" is excluded from each item's denominator and reported
# separately, since it records unfamiliarity with the term rather than an
# opinion. Net agreement = share agreeing minus share disagreeing, over the
# valid responses. Medians, not means: the scale is ordinal.

likert_rows, likert_long = [], []
for (measure, label, characteristic), col in zip(LIKERT_ITEMS, LIKERT_COLS):
    answers = [str(r[col]).strip() if r[col] is not None else "" for r in raw]
    for r, a in zip(raw, answers):
        likert_long.append(dict(respondent=int(r[COL_ID]), measure=measure, answer=a))
    counts = {lvl: answers.count(lvl) for lvl in LIKERT_SCALE}
    n_dk = answers.count(LIKERT_DK)
    valid = [LIKERT_SCALE.index(a) + 1 for a in answers if a in LIKERT_SCALE]
    n_valid = len(valid)
    agree = counts["Agree"] + counts["Strongly Agree"]
    disagree = counts["Disagree"] + counts["Strongly Disagree"]
    likert_rows.append(dict(measure=measure, label=label, characteristic=characteristic,
                            n_valid=n_valid, n_dont_know=n_dk,
                            **{f"n_{lvl.lower().replace(' ', '_')}": counts[lvl] for lvl in LIKERT_SCALE},
                            pct_agree=agree / n_valid, pct_disagree=disagree / n_valid,
                            net_agreement=(agree - disagree) / n_valid,
                            median=float(np.median(valid))))
likert_items = pd.DataFrame(likert_rows)
likert_long = pd.DataFrame(likert_long)

likert_characteristics = (likert_items.groupby("characteristic", sort=False)
                          .apply(lambda g: pd.Series(dict(
                              measures=", ".join(str(m) for m in g["measure"]),
                              n_valid=g["n_valid"].sum(), n_dont_know=g["n_dont_know"].sum(),
                              net_agreement=((g["n_agree"] + g["n_strongly_agree"]).sum()
                                             - (g["n_disagree"] + g["n_strongly_disagree"]).sum())
                                            / g["n_valid"].sum())),
                                 include_groups=False)
                          .reset_index())


# =============================================================================
# Respondent-level composites
# =============================================================================
#
# Comprehension combines the two measures with equal weight: the mean plus/minus score
# over the three closed items, and the mean rubric proportion over the open
# items the respondent answered. Averaging the two components, rather than all
# seven items, keeps the four open items from outweighing the three closed ones.

per_resp_closed = closed.groupby("respondent")["plus_minus"].mean().rename("closed_score")
per_resp_open = open_items.groupby("respondent")["rubric_score"].mean().rename("open_score")
per_resp_open_n = open_items.groupby("respondent")["rubric_score"].count().rename("open_items_scored")

respondents = (respondents.merge(per_resp_closed, on="respondent")
               .merge(per_resp_open, on="respondent")
               .merge(per_resp_open_n, on="respondent"))
respondents["comprehension"] = respondents[["closed_score", "open_score"]].mean(axis=1)
respondents = respondents.merge(generation[["respondent", "semantic_score", "syntax_errors",
                                            "errors_per_100_lines"]],
                                on="respondent", how="left")

# Self-rated comprehensibility, for calibration against measured comprehension.
self_rating = likert_long[likert_long["measure"] == COMPREHENSIBILITY_MEASURE].copy()
self_rating["self_rated_comprehensibility"] = self_rating["answer"].map(
    lambda a: LIKERT_SCALE.index(a) + 1 if a in LIKERT_SCALE else np.nan)
respondents = respondents.merge(self_rating[["respondent", "self_rated_comprehensibility"]],
                                on="respondent", how="left")


def rho(x, y):
    """Spearman's rho over complete pairs, with the number of pairs used."""
    pair = pd.concat([x, y], axis=1).dropna()
    if len(pair) < 3:
        return np.nan, len(pair)
    return spearmanr(pair.iloc[:, 0], pair.iloc[:, 1]).statistic, len(pair)


calibration_rho, calibration_n = rho(respondents["self_rated_comprehensibility"], respondents["comprehension"])


def bootstrap_rho(x, y, resamples=10_000, seed=0):
    """95% percentile bootstrap interval for Spearman's rho, over complete pairs.

    A fixed seed makes the interval reproducible. Resamples in which either
    variable is constant, and rho is therefore undefined, are skipped.
    """
    pair = pd.concat([x, y], axis=1).dropna().to_numpy()
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(resamples):
        sample = pair[rng.integers(0, len(pair), len(pair))]
        if len(np.unique(sample[:, 0])) > 1 and len(np.unique(sample[:, 1])) > 1:
            draws.append(spearmanr(sample[:, 0], sample[:, 1]).statistic)
    return tuple(np.percentile(draws, [2.5, 97.5]))


calibration_ci = bootstrap_rho(respondents["self_rated_comprehensibility"], respondents["comprehension"])
# The same relationship as a plain split: respondents agreeing that Regia takes
# little effort to understand (4 or 5 on the scale) against the rest.
agrees = respondents["self_rated_comprehensibility"] >= 4
calibration_split = respondents.dropna(subset=["self_rated_comprehensibility"]).groupby(
    agrees)["comprehension"].agg(["size", "median"])
convergent_rho, convergent_n = rho(respondents["closed_score"], respondents["open_score"])


def group_medians(frame, by):
    cols = ["closed_score", "open_score", "comprehension"]
    out = frame.groupby(by)[cols].median()
    out.insert(0, "n", frame.groupby(by).size())
    return out


by_game = group_medians(respondents, "has_game_experience").rename(index={False: "No game experience",
                                                                        True: "Game experience"})
by_group = group_medians(respondents, "group")
by_attempt = group_medians(respondents, "attempted_generation").rename(index={False: "Did not attempt",
                                                                            True: "Attempted"})


# =============================================================================
# Write outputs
# =============================================================================

respondents.to_csv(OUT_DIR / "respondents.csv", index=False)
closed.to_csv(OUT_DIR / "closed_items.csv", index=False)
closed_options.to_csv(OUT_DIR / "closed_options.csv", index=False)
open_items.to_csv(OUT_DIR / "open_items.csv", index=False)
open_units.to_csv(OUT_DIR / "open_units.csv", index=False)
items_summary.to_csv(OUT_DIR / "items_summary.csv", index=False)
generation.to_csv(OUT_DIR / "generation.csv", index=False)
generation_behaviours.to_csv(OUT_DIR / "generation_behaviours.csv", index=False)
generation_errors.to_csv(OUT_DIR / "generation_errors.csv", index=False)
likert_items.to_csv(OUT_DIR / "likert_items.csv", index=False)
likert_characteristics.to_csv(OUT_DIR / "likert_characteristics.csv", index=False)


def pct(x):
    return f"{100 * x:.1f}%"


def f2(x):
    return "n/a" if pd.isna(x) else f"{x:.2f}"


lines = ["# Regia questionnaire: summary of metrics", ""]
lines += ["## Sample", "",
          f"- Respondents: {n_resp}"
          + (f" (excluded: {', '.join(map(str, sorted(EXCLUDE)))})" if EXCLUDE else ""),
          *[f"- {g}: {n}" for g, n in respondents["group"].value_counts().items()],
          f"- Without any computing background: {(~respondents['bg_cs']).sum()}",
          f"- Attempted the generation task: {respondents['attempted_generation'].sum()} of {n_resp}",
          f"- Rubric raters: {len(raters)} ({', '.join(raters)})"
          + ("" if len(raters) > 1 else " -- single rater, no inter-rater reliability available"), ""]

if not uncoded_items.empty or uncoded_generation or uncoded_syntax:
    lines += ["## Data gaps", ""]
    for u in uncoded_items.itertuples():
        lines.append(f"- Respondent {u.respondent}, item {u.item}: {u.uncoded_units} rubric units uncoded; "
                     "the item is excluded from that respondent's open score.")
    if uncoded_generation:
        lines.append(f"- Generation behaviours uncoded for respondent(s) {uncoded_generation}; "
                     "excluded from the generation results.")
    if uncoded_syntax:
        lines.append(f"- Generation syntax errors uncoded for respondent(s) {uncoded_syntax}; "
                     "excluded from the generation results.")
    lines.append("")
if not provisional.empty:
    lines += ["## Provisional codes", ""]
    for (rid, it), g in provisional.groupby(["respondent", "item"]):
        lines.append(f"- Respondent {rid}, item {it}: {len(g)} units coded provisionally, not by rater A. "
                     "Confirm or revise in coding_sheet_A.csv and clear the flag before reporting "
                     "the evaluation as single-rater.")
    lines.append("")
if not mismatch.empty:
    lines += ["- WARNING: parsed closed selections do not match answer_key.csv counts.", ""]

lines += ["## Comprehension items, in questionnaire order", "",
          "| Item | Q | Level | Metric | n | Mean | Median | Min | Max |",
          "|---|---|---|---|---|---|---|---|---|"]
for s in items_summary.itertuples():
    lines.append(f"| {s.item} | {s.question} | {s.level} | {s.metric} | {s.n} | "
                 f"{f2(s.mean)} | {f2(s.median)} | {f2(s.min)} | {f2(s.max)} |")
lines.append("")

lines += ["## Closed options most often misjudged", "",
          "| Option | Correct? | Selected by | Answered correctly by |", "|---|---|---|---|"]
for o in closed_options.sort_values("correct_rate").head(6).itertuples():
    lines.append(f"| {o.option_id} | {'true' if o.is_correct else 'false'} | "
                 f"{pct(o.selection_rate)} | {pct(o.correct_rate)} |")
lines.append("")

lines += ["## Open rubric units with the lowest mean", "",
          "| Item | Unit | Description | Mean (0-2) |", "|---|---|---|---|"]
for u in open_units.sort_values("mean_code").head(6).itertuples():
    lines.append(f"| {u.item} | {u.unit} | {u.unit_desc} | {u.mean_code:.2f} |")
lines.append("")

lines += ["## Generation task", "",
          f"- Respondents: {len(generation)} (self-selected: the task was optional)",
          f"- Semantic score: median {f2(generation['semantic_score'].median())}, "
          f"range {f2(generation['semantic_score'].min())}-{f2(generation['semantic_score'].max())}",
          f"- Behaviours attempted: median {generation['behaviours_attempted'].median():.0f} of {n_behaviours}",
          f"- Quality when attempted: median {f2(generation['quality_when_attempted'].median())}",
          f"- Syntax errors per 100 lines: median {f2(generation['errors_per_100_lines'].median())}",
          f"- Submissions truncated by the form's length limit: {int(generation['truncated'].sum())}", "",
          f"Errors by category ({int(total_errors)} in total, across {len(gen_syn)} submissions):", "",
          "| Cat. | Description | Total | Share | Respondents | Max by one |", "|---|---|---|---|---|---|"]
for e in generation_errors.itertuples():
    lines.append(f"| {e.category} | {e.label} | {e.total} | {pct(e.share)} | "
                 f"{e.respondents_affected} of {len(gen_syn)} | {e.max_by_one} |")
lines.append("")

lines += ["## Likert items", "",
          "| # | Item | Characteristic | n valid | DK | Net agreement | Median |", "|---|---|---|---|---|---|---|"]
for l in likert_items.itertuples():
    lines.append(f"| {l.measure} | {l.label} | {l.characteristic} | {l.n_valid} | {l.n_dont_know} | "
                 f"{l.net_agreement:+.2f} | {l.median:.1f} |")
lines.append("")

lines += ["## Composites (descriptive only)", "",
          f"- Calibration, self-rated comprehensibility vs measured comprehension: "
          f"rho = {f2(calibration_rho)}, 95% bootstrap interval "
          f"[{f2(calibration_ci[0])}, {f2(calibration_ci[1])}] (n = {calibration_n})",
          f"  - agreeing it takes little effort (n = {int(calibration_split.loc[True, 'size'])}): "
          f"median comprehension {f2(calibration_split.loc[True, 'median'])}; "
          f"the rest (n = {int(calibration_split.loc[False, 'size'])}): "
          f"{f2(calibration_split.loc[False, 'median'])}",
          f"- Convergence, closed J vs open rubric score: rho = {f2(convergent_rho)} (n = {convergent_n})",
          "", "Group medians:", "", by_game.round(2).to_markdown(), "",
          by_group.round(2).to_markdown(), "", by_attempt.round(2).to_markdown(), ""]
if kappa is not None:
    lines += [f"- Inter-rater reliability, quadratic weighted kappa: {kappa:.2f}", ""]

(OUT_DIR / "summary.md").write_text("\n".join(lines))
print(f"Wrote results to {OUT_DIR.resolve()}")