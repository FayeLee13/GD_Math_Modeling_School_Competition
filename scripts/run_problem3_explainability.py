from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dataset_config import DATASET_SPECS, load_dataset
from src.problem3_explainability import (
    explain_dataset,
    save_explainability_figures,
)
from src.variable_metadata import build_expected_direction_table, build_variable_physical_meaning


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run problem 3 explainability analysis.")
    parser.add_argument("--data-dir", type=Path, default=Path("datasets"))
    parser.add_argument("--problem2-dir", type=Path, default=Path("reports/problem2"))
    parser.add_argument("--out-dir", type=Path, default=Path("reports/problem3"))
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--top-features", type=int, default=3)
    parser.add_argument("--n-repeats", type=int, default=6)
    parser.add_argument("--n-jobs", type=int, default=2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.out_dir / "tables"
    figures_dir = args.out_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    best = pd.read_csv(args.problem2_dir / "tables" / "best_models_by_dataset.csv")
    best_full = best[best["feature_set"] == "full"].copy()
    model_map = dict(zip(best_full["dataset"], best_full["model"]))

    permutation_parts = []
    sensitivity_parts = []
    pdp_parts = []
    consistency_parts = []

    for spec in DATASET_SPECS:
        model_name = model_map.get(spec.name)
        if model_name is None:
            raise KeyError(f"No full-feature best model found for {spec.name}")
        print(f"[problem3] explaining {spec.name} with {model_name} ...", flush=True)
        x, y = load_dataset(spec, args.data_dir)
        result = explain_dataset(
            spec=spec,
            x=x,
            y=y,
            model_name=model_name,
            feature_set="full",
            random_state=args.random_state,
            test_size=args.test_size,
            top_features=args.top_features,
            n_repeats=args.n_repeats,
            n_jobs=args.n_jobs,
        )
        permutation_parts.append(result.permutation_importance)
        sensitivity_parts.append(result.sensitivity)
        pdp_parts.append(result.partial_dependence)
        consistency_parts.append(result.consistency)
        save_explainability_figures(
            result.permutation_importance,
            result.sensitivity,
            result.partial_dependence,
            figures_dir,
        )

    permutation = pd.concat(permutation_parts, ignore_index=True)
    sensitivity = pd.concat(sensitivity_parts, ignore_index=True)
    pdp = pd.concat(pdp_parts, ignore_index=True)
    consistency = pd.concat(consistency_parts, ignore_index=True)
    variable_meaning = build_variable_physical_meaning(DATASET_SPECS)
    expected_directions = build_expected_direction_table(DATASET_SPECS)

    variable_meaning.to_csv(tables_dir / "variable_physical_meaning.csv", index=False, encoding="utf-8-sig")
    expected_directions.to_csv(tables_dir / "expected_direction_checks.csv", index=False, encoding="utf-8-sig")
    permutation.to_csv(tables_dir / "permutation_importance_all.csv", index=False, encoding="utf-8-sig")
    sensitivity.to_csv(tables_dir / "sensitivity_analysis_all.csv", index=False, encoding="utf-8-sig")
    pdp.to_csv(tables_dir / "partial_response_all.csv", index=False, encoding="utf-8-sig")
    consistency.to_csv(tables_dir / "physical_consistency_summary.csv", index=False, encoding="utf-8-sig")

    write_markdown_summary(args.out_dir / "problem3_summary.md", consistency, permutation, sensitivity, variable_meaning)
    print(f"[problem3] done. Results saved to {args.out_dir}", flush=True)


def write_markdown_summary(
    path: Path,
    consistency: pd.DataFrame,
    permutation: pd.DataFrame,
    sensitivity: pd.DataFrame,
    variable_meaning: pd.DataFrame,
) -> None:
    consistency_view = consistency.copy()
    for col in consistency_view.select_dtypes(include="number").columns:
        consistency_view[col] = consistency_view[col].round(4)

    top_perm = permutation.sort_values(["dataset", "importance_rank"]).groupby("dataset").head(5).copy()
    for col in ["importance_mean", "importance_std", "physical_score"]:
        top_perm[col] = top_perm[col].round(4)
    top_perm = top_perm[
        [
            "dataset",
            "model",
            "importance_rank",
            "feature",
            "importance_mean",
            "importance_std",
            "physical_score",
        ]
    ]

    sensitivity_view = sensitivity[sensitivity["perturbation"] == "plus_10pct"].copy()
    sensitivity_view = sensitivity_view.sort_values(["dataset", "feature", "target"]).groupby("dataset").head(12)
    for col in ["mean_prediction_delta", "normalized_mean_delta"]:
        sensitivity_view[col] = sensitivity_view[col].round(5)
    sensitivity_view = sensitivity_view[
        [
            "dataset",
            "feature",
            "target",
            "mean_prediction_delta",
            "normalized_mean_delta",
            "response_direction",
            "expected_direction",
            "direction_consistent",
        ]
    ]

    meaning_view = variable_meaning[
        [
            "dataset",
            "role",
            "variable",
            "physical_meaning",
            "physical_score",
            "expected_direction_summary",
        ]
    ].copy()

    lines = [
        "# B题问题3：模型可解释性分析结果",
        "",
        "本报告由 `scripts/run_problem3_explainability.py` 自动生成，基于问题2全特征最佳模型执行 TPCI-EM 解释流程。",
        "",
        "## 方法说明",
        "",
        "- 事前解释：沿用题面变量物理含义和问题1物理合理性评分。",
        "- 事中解释：使用排列重要性识别模型实际依赖变量。",
        "- 事后解释：对关键变量进行 ±10% 敏感性扰动，并为前两个关键变量生成部分响应数据。",
        "- 一致性判断：综合关键变量物理合理性、排列重要性和已知方向扰动结果，给出高/中/低物理一致性等级。",
        "",
        "## 变量物理含义示例",
        "",
    ]
    lines.extend(_markdown_table(meaning_view.groupby("dataset").head(6)))
    lines.extend(
        [
            "",
        "## 物理一致性总表",
        "",
        ]
    )
    lines.extend(_markdown_table(consistency_view))
    lines.extend(["", "## 排列重要性 Top 特征", ""])
    lines.extend(_markdown_table(top_perm))
    lines.extend(["", "## +10% 敏感性扰动摘要", ""])
    lines.extend(_markdown_table(sensitivity_view))
    lines.extend(
        [
            "",
            "## 输出文件",
            "",
            "- `tables/variable_physical_meaning.csv`：输入/输出变量的物理含义、物理评分和方向预期摘要。",
            "- `tables/expected_direction_checks.csv`：已配置的物理方向预期，用于敏感性一致性判断。",
            "- `tables/permutation_importance_all.csv`：所有数据集的排列重要性。",
            "- `tables/sensitivity_analysis_all.csv`：关键变量 ±10% 敏感性扰动结果。",
            "- `tables/partial_response_all.csv`：关键变量部分响应数据。",
            "- `tables/physical_consistency_summary.csv`：物理一致性等级和解释备注。",
            "- `figures/`：排列重要性图、敏感性热力图和关键变量部分响应图。",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _markdown_table(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return ["无。"]
    values = frame.astype(str)
    header = "| " + " | ".join(values.columns) + " |"
    sep = "| " + " | ".join(["---"] * len(values.columns)) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in values.to_numpy()]
    return [header, sep, *rows]


if __name__ == "__main__":
    main()
