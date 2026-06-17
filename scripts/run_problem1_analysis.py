from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dataset_config import DATASET_SPECS, load_dataset
from src.problem1_analysis import (
    analyze_dataset,
    describe_data_quality,
    summarize_preprocessing_diagnostics,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run problem 1 feature analysis for all datasets.")
    parser.add_argument("--data-dir", type=Path, default=Path("datasets"))
    parser.add_argument("--out-dir", type=Path, default=Path("reports/problem1"))
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.out_dir / "tables"
    figures_dir = args.out_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    all_quality = []
    all_scores = []
    all_corr = []
    all_redundancy = []

    for spec in DATASET_SPECS:
        print(f"[problem1] analyzing {spec.name} ...", flush=True)
        x, y = load_dataset(spec, args.data_dir)
        all_quality.append(describe_data_quality(spec.name, x, y))
        result = analyze_dataset(spec, x, y, figures_dir=figures_dir, random_state=args.random_state)
        all_scores.append(result["feature_scores"])
        all_corr.append(result["input_output_correlations"])
        all_redundancy.append(result["redundancy_pairs"])

        result["feature_scores"].to_csv(tables_dir / f"{spec.name}_feature_scores.csv", index=False, encoding="utf-8-sig")
        result["redundancy_pairs"].to_csv(tables_dir / f"{spec.name}_redundancy_pairs.csv", index=False, encoding="utf-8-sig")

    quality = pd.concat(all_quality, ignore_index=True)
    preprocessing = summarize_preprocessing_diagnostics(quality)
    scores = pd.concat(all_scores, ignore_index=True)
    correlations = pd.concat(all_corr, ignore_index=True)
    redundancy = pd.concat(all_redundancy, ignore_index=True)

    quality.to_csv(tables_dir / "data_quality_summary.csv", index=False, encoding="utf-8-sig")
    preprocessing.to_csv(tables_dir / "preprocessing_diagnostics.csv", index=False, encoding="utf-8-sig")
    scores.to_csv(tables_dir / "feature_scores_all.csv", index=False, encoding="utf-8-sig")
    correlations.to_csv(tables_dir / "input_output_correlations_all.csv", index=False, encoding="utf-8-sig")
    redundancy.to_csv(tables_dir / "redundancy_pairs_all.csv", index=False, encoding="utf-8-sig")

    selected = (
        scores[scores["selection_decision"].isin(["keep_core", "keep_candidate", "protect_for_validation"])]
        .groupby("dataset")["feature"]
        .apply(lambda values: ", ".join(values))
        .reset_index(name="selected_features")
    )
    selected.to_csv(tables_dir / "selected_features_by_dataset.csv", index=False, encoding="utf-8-sig")

    write_markdown_summary(args.out_dir / "problem1_summary.md", scores, quality, preprocessing, redundancy, selected)
    print(f"[problem1] done. Results saved to {args.out_dir}", flush=True)


def write_markdown_summary(
    path: Path,
    scores: pd.DataFrame,
    quality: pd.DataFrame,
    preprocessing: pd.DataFrame,
    redundancy: pd.DataFrame,
    selected: pd.DataFrame,
) -> None:
    lines = [
        "# B题问题1：特征分析与预处理结果",
        "",
        "本报告由 `scripts/run_problem1_analysis.py` 自动生成，对所有数据集执行 DP-FSM 特征筛选流程。",
        "",
        "## 方法说明",
        "",
        "综合得分采用：`S = 0.3C + 0.3N + 0.3P - 0.1R`。",
        "",
        "- `C`：Pearson 与 Spearman 平均绝对相关强度。",
        "- `N`：随机森林非线性特征重要性，并按数据集内最大值归一化。",
        "- `P`：基于题面机理的物理合理性评分。",
        "- `R`：输入变量间平均绝对相关系数，作为冗余惩罚。",
        "",
        "特征分级规则：`S >= 0.65` 为核心特征，`0.45 <= S < 0.65` 为候选特征，`S < 0.45` 为低优先级特征。",
        "",
        "## 数据质量概况",
        "",
    ]
    preprocessing_view = preprocessing.copy()
    for col in ["max_missing_rate", "max_iqr_outlier_rate", "input_scale_range_ratio"]:
        preprocessing_view[col] = preprocessing_view[col].round(4)
    lines.extend(_markdown_table(preprocessing_view))
    lines.extend(["", "## 描述性统计变量诊断示例", ""])
    quality_view = quality[
        [
            "dataset",
            "role",
            "variable",
            "n_rows",
            "missing_count",
            "mean",
            "std",
            "min",
            "q25",
            "median",
            "q75",
            "max",
            "skew",
            "iqr_outlier_rate",
            "zero_std",
            "needs_standardization",
        ]
    ].copy()
    numeric_cols = ["mean", "std", "min", "q25", "median", "q75", "max", "skew", "iqr_outlier_rate"]
    for col in numeric_cols:
        quality_view[col] = quality_view[col].round(4)
    lines.extend(_markdown_table(quality_view.groupby("dataset").head(5)))
    lines.extend(["", "## 各数据集推荐特征", ""])
    lines.extend(_markdown_table(selected))
    lines.extend(["", "## 各数据集 Top 特征", ""])
    top = scores.sort_values(["dataset", "rank"]).groupby("dataset").head(5)
    top = top[
        [
            "dataset",
            "rank",
            "feature",
            "dp_fsm_score",
            "feature_level",
            "correlation_strength",
            "rf_importance_norm",
            "redundancy_max_abs",
            "possible_nonlinear_relation",
        ]
    ].copy()
    for col in ["dp_fsm_score", "correlation_strength", "rf_importance_norm", "redundancy_max_abs"]:
        top[col] = top[col].round(4)
    lines.extend(_markdown_table(top))
    high_redundancy = redundancy[redundancy["is_high_redundancy"]].copy()
    lines.extend(["", "## 高冗余特征对", ""])
    if high_redundancy.empty:
        lines.append("未发现绝对 Pearson 相关系数超过 0.9 的高冗余输入特征对。")
    else:
        high_redundancy["abs_pearson_corr"] = high_redundancy["abs_pearson_corr"].round(4)
        lines.extend(_markdown_table(high_redundancy[["dataset", "feature_a", "feature_b", "abs_pearson_corr"]]))
    lines.extend(
        [
            "",
            "## 输出文件",
            "",
            "- `tables/feature_scores_all.csv`：全部数据集特征综合得分。",
            "- `tables/data_quality_summary.csv`：变量级描述性统计和数据质量诊断。",
            "- `tables/preprocessing_diagnostics.csv`：数据集级预处理建议。",
            "- `tables/input_output_correlations_all.csv`：输入-输出 Pearson/Spearman 相关性长表。",
            "- `tables/redundancy_pairs_all.csv`：输入变量间冗余关系。",
            "- `tables/selected_features_by_dataset.csv`：按 DP-FSM 规则推荐的特征集。",
            "- `figures/`：各数据集特征得分条形图、输入冗余热力图、输入-输出相关热力图。",
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
