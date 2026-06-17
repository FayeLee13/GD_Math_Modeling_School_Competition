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

## Problem 2: Model Construction and Accuracy Evaluation

Run the full MCAS-PM model comparison workflow:

```powershell
python scripts/run_problem2_modeling.py
```

The script trains Ridge, KNN, random forest, and gradient boosting models on
both the full feature set and the problem 1 selected feature set. It writes:

- `reports/problem2/problem2_summary.md`
- `reports/problem2/tables/model_metrics_all.csv`
- `reports/problem2/tables/target_metrics_all.csv`
- `reports/problem2/tables/best_models_by_dataset.csv`
- `reports/problem2/tables/feature_set_comparison.csv`
- `reports/problem2/tables/dataset_factor_analysis.csv`
- `reports/problem2/figures/*.png`

The ranking score follows the current problem 2 summary:

```text
Score = 0.4 * R2 rank + 0.35 * NRMSE rank + 0.25 * NMAE rank
```
