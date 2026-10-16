# Questionnaire Evaluation Pipeline

A Python pipeline that computes every evaluation metric reported in the research questionnaire study (Section 8.3). It processes raw survey data, applies rubric-based coding, and produces descriptive statistics, per-item breakdowns, and publication-ready figures.

## Prerequisites

- **Python ≥ 3.11**
- The shared virtual environment (`.venv` at the repository root)

### Python Dependencies

```bash
source .venv/bin/activate
pip install numpy pandas scipy openpyxl matplotlib
```

## Input Data

All input files are read from the data directory (defaults to the current directory):

| File | Description |
|---|---|
| `data.xlsx` | Raw questionnaire export (backgrounds, closed/open answers, Likert scales) |
| `answer_key.csv` | Correct options for the three closed questions |
| `coding_sheet_A.csv` | 0/1/2 rubric codes for the four open questions |
| `gen_behaviour.csv` | 0/1/2 rubric codes for the generation task behaviours |
| `gen_syntax.csv` | Syntax-error counts for the generation task |

## Usage

### 1. Expand Evaluation Sheets (when new responses arrive)

When new respondents appear in `data.xlsx`, run this to add blank rows for them in all coding sheets:

```bash
cd qscores
python expand_data.py [DATA_DIR]
```

This never modifies already-coded rows — it only appends new ones.

### 2. Compute Metrics

```bash
cd qscores
python compute_metrics.py [DATA_DIR] [OUT_DIR] [--exclude ID ...]
```

- `DATA_DIR` — Directory containing the input files (defaults to `.`).
- `OUT_DIR` — Directory for output CSVs (defaults to `results`).
- `--exclude ID ...` — Drop specific respondent IDs before computing (for sensitivity analysis).

### 3. Generate Figures

```bash
cd qscores
python make_figures.py [RESULTS_DIR] [FIG_DIR]
```

- `RESULTS_DIR` — Directory containing the CSVs from step 2 (defaults to `results`).
- `FIG_DIR` — Directory for output PNG figures (defaults to `fig`).

## Output Files

### Metrics (`results/`)

| File | Content |
|---|---|
| `respondents.csv` | One row per respondent: background, every score, composites |
| `closed_items.csv` | Per respondent × closed item: confusion counts, sensitivity, normalised ± score |
| `closed_options.csv` | Per option: selection rate, correctness |
| `open_items.csv` | Per respondent × open item: rubric proportion |
| `open_units.csv` | Per rubric unit: mean code, distribution |
| `items_summary.csv` | All seven comprehension items in questionnaire order |
| `generation.csv` | Per generation respondent: semantic and syntax scores |
| `generation_behaviours.csv` | Per specified behaviour: coverage across respondents |
| `generation_errors.csv` | Per syntax-error category: totals, share, respondents affected |
| `likert_items.csv` | Per Likert item: distribution, net agreement, median |
| `likert_characteristics.csv` | Per characteristic: pooled net agreement |
| `summary.md` | Headline figures in readable form |

### Figures (`fig/`)

| Figure | Description |
|---|---|
| `comprehension_by_item.png` | Per-respondent scores on the seven comprehension items |
| `closed_options.png` | Selection rates for closed-question statements |
| `open_units.png` | Mean rubric score per unit of each open question |
| `likert_diverging.png` | Fifteen quality measures as diverging stacked bars |
| `calibration.png` | Self-rated comprehensibility vs. measured comprehension |
| `generation_behaviours.png` | Coverage of each specified behaviour in the generation task |

## Project Structure

```text
qscores/
├── compute_metrics.py    Main evaluation script
├── form_data.py          Data loading and row parsing
├── expand_data.py        Expand coding sheets for new respondents
├── make_figures.py       Publication figure generation
├── data/                 Input data files (xlsx, csv)
├── out/                  Computed output CSVs
└── fig/                  Generated figures (PNG)
```
