# Questionnaire Evaluation Pipeline

A Python pipeline that computes every evaluation metric reported in the research questionnaire study (Section 6 of the paper and Section 4.3 of the supplementary material). It processes raw survey data, applies rubric-based coding, and produces descriptive statistics, per-item breakdowns, and publication-ready figures.

## Prerequisites

- **[uv](https://docs.astral.sh/uv/)**
- The shared virtual environment (`.venv` at the repository root)

### Python Dependencies

The dependencies (numpy, pandas, scipy, openpyxl, matplotlib, tabulate) are declared in `qscores/pyproject.toml` and locked in the root `uv.lock`. pandas is held below 3.1, which changes the last digit of a float in `respondents.csv`. From the repository root:

```bash
uv sync --package regia-qscores
source .venv/bin/activate
```

## Input Data

All input files are read from the data directory (defaults to `qscores/data`):

| File | Description |
|---|---|
| `data.xlsx` | Raw questionnaire export (backgrounds, closed/open answers, Likert scales) |
| `answer_key.csv` | Correct options for the three closed questions |
| `coding_sheet_A.csv` | 0/1/2 rubric codes for the four open questions |
| `gen_behaviour.csv` | 0/1/2 rubric codes for the generation task behaviours |
| `gen_syntax.csv` | Syntax-error counts for the generation task |

## Usage

From the repository root, `make qscores` runs steps 2 and 4 below, and `make figures` runs step 3 too. The scripts can also be run one by one:

### 1. Expand Evaluation Sheets (when new responses arrive)

When new respondents appear in `data.xlsx`, run this to list the rows missing from the coding sheets, then again with `--write` to add them as blank rows:

```bash
cd qscores
python expand_data.py [DATA_DIR]           # report only
python expand_data.py [DATA_DIR] --write   # add the rows (keeps .bak copies)
```

This never modifies already-coded rows — it only appends new ones.

### 2. Compute Metrics

```bash
cd qscores
python compute_metrics.py [DATA_DIR] [OUT_DIR] [--exclude ID ...]
```

- `DATA_DIR` — Directory containing the input files (defaults to `qscores/data`).
- `OUT_DIR` — Directory for output CSVs (defaults to `qscores/results`).
- `--exclude ID ...` — Drop specific respondent IDs before computing (for sensitivity analysis).

### 3. Generate Figures

```bash
cd qscores
python make_figures.py [RESULTS_DIR] [FIG_DIR]
```

- `RESULTS_DIR` — Directory containing the CSVs from step 2 (defaults to `qscores/results`).
- `FIG_DIR` — Directory for output PNG figures (defaults to `qscores/figures`)

### 4. Compare with the Paper

```bash
cd qscores
python compare_reference.py [RESULTS_DIR] [REFERENCE_DIR]
```

Compares the regenerated CSVs with the paper's, in `reference/results`. They must match exactly, except for line endings; any difference is printed and the script exits with status 1. The figures have their own script:

```bash
cd qscores
python compare_figures.py [FIG_DIR] [REFERENCE_DIR]
```

Compares the redrawn figures with the paper's, in `reference/figures`, pixel by pixel (the compressed PNG bytes may differ). `make compare-figures`, from the repository root, redraws and compares these and the paper's benchmark fits. CI checks them on Ubuntu; on another system, a few pixels may differ.

## Output Files

`results/` and `figures/` are regenerated and not tracked. The paper's own outputs (N = 32) are in `reference/`.

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

### Figures (`figures/`)

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
├── compare_reference.py  Check the regenerated CSVs against the paper's
├── compare_figures.py    Check the redrawn figures against the paper's
├── data/                 Input data files (xlsx, csv)
├── reference/            The paper's outputs
│   ├── results/          CSVs and summary
│   └── figures/          Figures (PNG)
├── results/              Regenerated CSVs (not tracked)
└── figures/              Regenerated figures (not tracked)
```
