# GD_Math_Modeling_School_Competition

This repository contains materials and reproducible code for the GD math
modeling school competition, problem B.

## Problem 1: Feature Analysis and Preprocessing

Run the full DP-FSM feature screening workflow:

```powershell
python scripts/run_problem1_analysis.py
```

The script analyzes all configured datasets under `datasets/` and writes:

- `reports/problem1/problem1_summary.md`
- `reports/problem1/tables/feature_scores_all.csv`
- `reports/problem1/tables/input_output_correlations_all.csv`
- `reports/problem1/tables/redundancy_pairs_all.csv`
- `reports/problem1/tables/selected_features_by_dataset.csv`
- `reports/problem1/figures/*.png`

The implemented score follows the current problem 1 summary:

```text
S = 0.3C + 0.3N + 0.3P - 0.1R
```

where `C` is Pearson/Spearman correlation strength, `N` is normalized random
forest feature importance, `P` is physics plausibility, and `R` is input
redundancy.
