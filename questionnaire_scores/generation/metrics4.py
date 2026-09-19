#!/usr/bin/env python3
"""
Regia questionnaire -- CODE GENERATION task: rubric tooling.

  python3 score_gen.py init      -> submission files + blank coding sheets
  python3 score_gen.py migrate   -> rebuild sheets after a rubric change, keeping codes
  python3 score_gen.py score     -> attempt, coverage, accuracy, constructs, syntax

Measurement axes, deliberately never collapsed into one number:
  LEVEL 1  attempt      - all 21 respondents; non-attempt is a rate, never a zero
  AXIS A   behaviours   - 15 atomic requirements from the specification prose
  AXIS B   constructs   - 5 units from the task's structural suggestions
  AXIS C   syntax       - per submission, NOT per requirement

Behaviour codes: '-' not attempted | 0 wrong | 1 partial | 2 correct | blank not yet coded
Construct / syntax codes: 0 | 1 | 2
Requires: pandas, numpy, matplotlib, statsmodels, openpyxl
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from statsmodels.stats.proportion import proportion_confint

SRC = "Regia__an_anonymous_questionnaire_for_assessing_its_intuitiveness_and_usability_1-21_.xlsx"
OUT, SUBDIR, GEN_COL = ".", "submissions", 15
CHAR_CAP, TOKEN_MAX, MAXCODE = 4000, 20, 2
NOT_ATTEMPTED = "-"

BEHAVIOURS = [
 ("B1",  "Princess exists as a ROLE in the banquet plot"),
 ("B2",  "during reception, the Princess greets the Guests"),
 ("B3",  "during feast, the Princess refuses to eat unless she likes the food"),
 ("B4",  "Pretender exists as a ROLE and initially behaves as a Guest"),
 ("B5",  "during feast, the Pretender can talk to other Guests"),
 ("B6",  "during feast, if no food is to her liking, the Princess asks the Pretender to search"),
 ("B7",  "the Pretender checks around for available food"),
 ("B8",  "on finding an appropriate dish, gives it to the Princess, ENDING the quest"),
 ("B9",  "during feast, the Princess can ask the Pretender to dance, starting a Ball"),
 ("B10", "during the Ball, the Pretender FORGETS its other duties and only talks with her"),
 ("B11", "a Guest greeted by the Princess becomes enamoured"),
 ("B12", "a Guest who spoke with the Pretender becomes its friend"),
 ("B13", "during the Ball, a friendly Guest cheers the couple"),
 ("B14", "during the Ball, an enamoured Guest insults the couple, starting a duel"),
 ("B15", "a Guest that is neither or both just watches"),
]

CONSTRUCTS = [
 ("S1", "new ROLEs plus PLAYBOOKs for Princess and Pretender"),
 ("S2", "a new PHASE for the ball, reached by a TRANSITION"),
 ("S3", "a SUBPLOT for the food search, with role MAPPING, that terminates"),
 ("S4", "Guest playbook and main plot modified coherently with the additions"),
 ("S5", "careful ASSIGN / UNASSIGN of playbooks to the Pretender"),
]

ERRORS = {
 "E1": "missing terminating dots",
 "E2": "block structure / indentation not per grammar",
 "E3": "DO omitted before an action",
 "E4": "invented control construct (WHEN ALWAYS, WHEN true, ...)",
 "E5": "playbook name used where a role is expected, or vice versa",
 "E6": "ASSIGN / UNASSIGN omitted or misused",
 "E7": "SIGNAL misused (wrong direction or target)",
 "E8": "vocabulary used without being declared",
 "E9": "identifier case inconsistency (host vs Host)",
 "E10": "subplot start or role MAPPING malformed",
}

ATTEMPT_LEVELS = ["none", "token", "substantive"]


def submissions():
    df = pd.read_excel(SRC)
    out = {}
    for r, v in enumerate(df.iloc[:, GEN_COL].fillna(""), 1):
        t = str(v).replace("\xa0", " ")
        n = len(t.strip())
        out[r] = {"text": t, "chars": len(t), "at_cap": len(t) >= CHAR_CAP,
                  "lines": sum(1 for L in t.splitlines() if L.strip()),
                  "attempt_auto": "none" if n < 3 else
                                  ("token" if n < TOKEN_MAX else "substantive")}
    return out


def _sheets(subs, old=None):
    """Build the three level-2 sheets, optionally preserving codes from `old`."""
    def prev(sheetname, key, col, default=""):
        if old is None or sheetname not in old:
            return default
        o = old[sheetname]
        return o.loc[key, col] if key in o.index else default

    beh, con, syn = [], [], []
    for r, s in subs.items():
        if s["attempt_auto"] != "substantive":
            continue
        for bid, desc in BEHAVIOURS:
            beh.append({"respondent": r, "behaviour": bid,
                        "code": prev("beh", (r, bid), "code"),
                        "in_scope": prev("beh", (r, bid), "in_scope", 1),
                        "desc": desc, "flag": prev("beh", (r, bid), "flag")})
        for sid, desc in CONSTRUCTS:
            con.append({"respondent": r, "construct": sid,
                        "code": prev("con", (r, sid), "code"),
                        "in_scope": prev("con", (r, sid), "in_scope", 1),
                        "desc": desc, "flag": prev("con", (r, sid), "flag")})
        row = {"respondent": r, "nonblank_lines": s["lines"],
               "syntax_conformance": prev("syn", r, "syntax_conformance"),
               "notes": prev("syn", r, "notes")}
        for e in ERRORS:
            row[e] = prev("syn", r, e, 0)
        syn.append(row)
    return (pd.DataFrame(beh).sort_values(["behaviour", "respondent"]),
            pd.DataFrame(con).sort_values(["construct", "respondent"]),
            pd.DataFrame(syn))


def init(force=False):
    subs = submissions()
    if os.path.exists(f"{OUT}/gen_behaviour.csv") and not force:
        sys.exit("sheets exist; pass --force to overwrite (or use migrate)")
    os.makedirs(f"{OUT}/{SUBDIR}", exist_ok=True)
    for r, s in subs.items():
        if s["attempt_auto"] == "substantive":
            open(f"{OUT}/{SUBDIR}/R{r:02d}.regia", "w").write(s["text"])

    pd.DataFrame([{"respondent": r, "chars": s["chars"],
                   "nonblank_lines": s["lines"],
                   "attempt_auto": s["attempt_auto"], "attempt": s["attempt_auto"],
                   "completion": "truncated_at_cap" if s["at_cap"] else "complete",
                   "notes": ""} for r, s in subs.items()]
                 ).to_csv(f"{OUT}/gen_attempt.csv", index=False)

    beh, con, syn = _sheets(subs)
    beh.to_csv(f"{OUT}/gen_behaviour.csv", index=False)
    con.to_csv(f"{OUT}/gen_construct.csv", index=False)
    syn.to_csv(f"{OUT}/gen_syntax.csv", index=False)
    pd.DataFrame([{"code": k, "meaning": v} for k, v in ERRORS.items()]
                 ).to_csv(f"{OUT}/gen_error_codes.csv", index=False)
    n = sum(1 for s in subs.values() if s["attempt_auto"] == "substantive")
    print(f"{len(subs)} respondents, {n} substantive attempts "
          f"({sum(s['at_cap'] for s in subs.values())} at the {CHAR_CAP}-char cap)")
    print(f"wrote {SUBDIR}/*.regia, gen_attempt.csv, "
          f"gen_behaviour.csv ({len(beh)}), gen_construct.csv ({len(con)}), "
          f"gen_syntax.csv ({len(syn)})")


def migrate():
    subs = submissions()
    old = {}
    for tag, f, keys in (("beh", "gen_behaviour.csv", ["respondent", "behaviour"]),
                         ("con", "gen_construct.csv", ["respondent", "construct"]),
                         ("syn", "gen_syntax.csv", ["respondent"])):
        d = pd.read_csv(f"{OUT}/{f}", dtype={"code": object, "flag": object,
                                             "notes": object})
        old[tag] = d.set_index(keys[0] if len(keys) == 1 else keys)
    beh, con, syn = _sheets(subs, old)
    for d, f in ((beh, "gen_behaviour"), (con, "gen_construct"), (syn, "gen_syntax")):
        d.to_csv(f"{OUT}/{f}_migrated.csv", index=False)
        filled = (d.code.astype(str).str.strip().ne("").sum()
                  if "code" in d else len(d))
        print(f"{f}: {len(d)} rows, {filled} carrying a value")
    print("wrote *_migrated.csv - check, then rename over the originals")


def _num(s):
    """Behaviour code -> numeric, with '-' meaning not attempted (NaN)."""
    s = str(s).strip()
    return np.nan if s in ("", "nan", NOT_ATTEMPTED) else float(s)


def score():
    A = pd.read_csv(f"{OUT}/gen_attempt.csv", dtype={"completion": object,
                                                     "notes": object})
    n = len(A)
    print("=== LEVEL 1: attempt (all respondents) ===")
    for lv in ATTEMPT_LEVELS:
        k = int((A.attempt == lv).sum())
        lo, hi = proportion_confint(k, n, method="wilson")
        print(f"  {lv:12s} {k:2d}/{n}  {k/n:5.1%}  Wilson 95% CI [{lo:.1%}, {hi:.1%}]")
    print("\n  completion of substantive attempts:")
    for k, v in A[A.attempt == "substantive"].completion.fillna(
            "complete").value_counts().items():
        print(f"    {k:24s} {v}")

    B = pd.read_csv(f"{OUT}/gen_behaviour.csv", dtype={"code": object, "flag": object})
    B["raw"] = B.code.astype(str).str.strip()
    B = B[B.raw.ne("") & B.raw.ne("nan")]
    if B.empty:
        print("\nno behaviour codes yet - stopping"); return
    B["attempted"] = (B.raw != NOT_ATTEMPTED).astype(int)
    B["sval"] = B.raw.map(_num)          # NB: not 'sem' - collides with DataFrame.sem

    rows = []
    for r, g in B.groupby("respondent"):
        ins = g[g.in_scope == 1]
        att = ins[ins.attempted == 1]
        rows.append({"respondent": r, "n_in_scope": len(ins),
                     "n_attempted": len(att),
                     "coverage": len(att) / len(ins) if len(ins) else np.nan,
                     "accuracy": att["sval"].mean() / MAXCODE if len(att) else np.nan,
                     "spec_realised": att["sval"].sum() / (MAXCODE * len(ins))
                                      if len(ins) else np.nan})
    P = pd.DataFrame(rows)

    C = pd.read_csv(f"{OUT}/gen_construct.csv", dtype={"code": object, "flag": object})
    C["val"] = C.code.map(_num)
    P = P.merge(C[C.in_scope == 1].groupby("respondent").val.mean()
                .div(MAXCODE).rename("constructs"), on="respondent", how="left")

    S = pd.read_csv(f"{OUT}/gen_syntax.csv", dtype={"notes": object})
    ecols = [e for e in ERRORS if e in S.columns]
    S["n_errors"] = S[ecols].fillna(0).sum(axis=1)
    S["err_per_100_lines"] = S.n_errors / S.nonblank_lines.replace(0, np.nan) * 100
    P = P.merge(S[["respondent", "syntax_conformance", "n_errors",
                   "err_per_100_lines"]], on="respondent", how="left")
    P.round(4).to_csv(f"{OUT}/gen_scores_per_respondent.csv", index=False)

    print(f"\n=== AXES A/B/C: substantive attempts only (n = {len(P)}) ===")
    print(P.round(3).to_string(index=False))
    for col, label in (("coverage", "behavioural coverage (attempted / in scope)"),
                       ("accuracy", "semantic accuracy (given attempt)"),
                       ("spec_realised", "spec realised (coverage x accuracy)"),
                       ("constructs", "construct idiomaticity"),
                       ("err_per_100_lines", "syntax errors per 100 lines")):
        v = P[col].dropna()
        if len(v):
            print(f"  {label:48s} mean {v.mean():.3f}  "
                  f"range {v.min():.3f}-{v.max():.3f}")

    Bd = (B[B.in_scope == 1].groupby("behaviour")
          .agg(attempt_rate=("attempted", "mean"),
               accuracy=("sval", lambda s: s.mean() / MAXCODE),
               n_in_scope=("in_scope", "sum")).reindex([b for b, _ in BEHAVIOURS]))
    Bd.round(3).to_csv(f"{OUT}/gen_behaviour_stats.csv")
    print("\nper behaviour:"); print(Bd.round(3).to_string())

    Cd = (C[C.in_scope == 1].groupby("construct")
          .agg(idiomaticity=("val", lambda s: s.mean() / MAXCODE),
               n=("val", "size")).reindex([s for s, _ in CONSTRUCTS]))
    Cd.round(3).to_csv(f"{OUT}/gen_construct_stats.csv")
    print("\nper construct:"); print(Cd.round(3).to_string())

    tot = S[ecols].fillna(0).sum().sort_values(ascending=False)
    print("\nerror taxonomy (total occurrences):")
    for e, k in tot.items():
        if k: print(f"  {e:4s} {int(k):3d}  {ERRORS[e]}")

    figures(A, B, C, P)


def figures(A, B, C, P):
    bids = [b for b, _ in BEHAVIOURS]
    resp = sorted(B.respondent.unique())
    G = np.full((len(resp), len(bids)), np.nan)
    for i, r in enumerate(resp):
        for j, b in enumerate(bids):
            row = B[(B.respondent == r) & (B.behaviour == b)]
            if row.empty: continue
            row = row.iloc[0]
            G[i, j] = (4 if row.in_scope == 0 else
                       0 if row.attempted == 0 else
                       1 if row["sval"] == 0 else 2 if row["sval"] == 1 else 3)
    cmap = matplotlib.colors.ListedColormap(
        ["#f2f2f0", "#c0392b", "#e8d5a8", "#2e7d5b", "#c9c9d6"])
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.4),
                             gridspec_kw={"width_ratios": [3.2, 1.5]})
    ax = axes[0]
    ax.imshow(G, cmap=cmap, vmin=0, vmax=4, aspect="auto", interpolation="nearest")
    ax.set_xticks(range(len(bids))); ax.set_xticklabels(bids, fontsize=8)
    ax.set_yticks(range(len(resp)))
    ax.set_yticklabels([f"R{r:02d}" for r in resp], fontsize=8)
    ax.set_title("Axis A - behavioural coverage and semantic accuracy",
                 fontsize=11, weight="bold")
    for j in range(len(bids) + 1): ax.axvline(j - .5, color="white", lw=1.2)
    for i in range(len(resp) + 1): ax.axhline(i - .5, color="white", lw=1.2)
    h = [Rectangle((0, 0), 1, 1, fc=c) for c in
         ["#2e7d5b", "#e8d5a8", "#c0392b", "#f2f2f0", "#c9c9d6"]]
    ax.legend(h, ["correct", "partial", "wrong", "not attempted", "out of scope"],
              loc="upper center", bbox_to_anchor=(.5, -.07), ncol=5,
              frameon=False, fontsize=8)

    ax = axes[1]
    cids = [s for s, _ in CONSTRUCTS]
    vals = [C[(C.construct == s) & (C.in_scope == 1)].val.mean() / MAXCODE
            for s in cids]
    ax.barh(np.arange(len(cids))[::-1], [0 if np.isnan(v) else v for v in vals],
            color="#5b7f9a", height=.6)
    ax.set_yticks(np.arange(len(cids))[::-1]); ax.set_yticklabels(cids, fontsize=9)
    ax.set_xlim(0, 1); ax.set_xlabel("mean idiomaticity", fontsize=9)
    ax.set_title("Axis B - construct use", fontsize=11, weight="bold")
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig_generation.png", dpi=160,
                                    bbox_inches="tight")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "init"
    if cmd == "init": init(force="--force" in sys.argv)
    else: {"migrate": migrate, "score": score}[cmd]()