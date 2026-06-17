from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dataset_config import DATASET_SPECS, load_dataset
from src.problem2_modeling import (
    best_models,
    best_models_by_target,
    evaluate_dataset,
    feature_set_comparison,
    save_figures,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run problem 2 model training and evaluation.")
    parser.add_argument("--data-dir", type=Path, default=Path("datasets"))
    parser.add_argument("--problem1-dir", type=Path, default=Path("reports/problem1"))
    parser.add_argument("--out-dir", type=Path, default=Path("reports/problem2"))
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--test-size", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.out_dir / "tables"
    figures_dir = args.out_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    selected_map = load_selected_features(args.problem1_dir / "tables" / "selected_features_by_dataset.csv")

    aggregate_parts = []
    target_parts = []
    prediction_parts = []

    for spec in DATASET_SPECS:
        print(f"[problem2] modeling {spec.name} ...", flush=True)
        x, y = load_dataset(spec, args.data_dir)
        result = evaluate_dataset(
            spec=spec,
            x=x,
            y=y,
            selected_features=selected_map.get(spec.name, list(x.columns)),
            random_state=args.random_state,
            test_size=args.test_size,
        )
        aggregate_parts.append(result.aggregate_metrics)
        target_parts.append(result.target_metrics)
        prediction_parts.append(result.predictions)

    metrics = pd.concat(aggregate_parts, ignore_index=True)
    target_metrics = pd.concat(target_parts, ignore_index=True)
    predictions = pd.concat(prediction_parts, ignore_index=True)
    best = best_models(metrics)
    target_best = best_models_by_target(target_metrics)
    comparison = feature_set_comparison(best)
    factors = dataset_factor_table(best, comparison)

    metrics.to_csv(tables_dir / "model_metrics_all.csv", index=False, encoding="utf-8-sig")
    target_metrics.to_csv(tables_dir / "target_metrics_all.csv", index=False, encoding="utf-8-sig")
    target_best.to_csv(tables_dir / "best_models_by_target.csv", index=False, encoding="utf-8-sig")
    predictions.to_csv(tables_dir / "predictions_all.csv", index=False, encoding="utf-8-sig")
    best.to_csv(tables_dir / "best_models_by_dataset.csv", index=False, encoding="utf-8-sig")
    comparison.to_csv(tables_dir / "feature_set_comparison.csv", index=False, encoding="utf-8-sig")
    factors.to_csv(tables_dir / "dataset_factor_analysis.csv", index=False, encoding="utf-8-sig")

    save_figures(metrics, best, comparison, figures_dir)
    write_markdown_summary(args.out_dir / "problem2_summary.md", best, target_best, comparison, factors)
    print(f"[problem2] done. Results saved to {args.out_dir}", flush=True)


def load_selected_features(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    frame = pd.read_csv(path)
    selected = {}
    for _, row in frame.iterrows():
        features = [item.strip() for item in str(row["selected_features"]).split(",") if item.strip()]
        selected[str(row["dataset"])] = features
    return selected


def dataset_factor_table(best: pd.DataFrame, comparison: pd.DataFrame) -> pd.DataFrame:
    full_best = best[best["feature_set"] == "full"].copy()
    selected_best = best[best["feature_set"] == "selected"][
        ["dataset", "model", "mean_r2", "mean_nrmse", "input_dim"]
    ].rename(
        columns={
            "model": "selected_best_model",
            "mean_r2": "selected_best_mean_r2",
            "mean_nrmse": "selected_best_mean_nrmse",
            "input_dim": "selected_input_dim",
        }
    )
    factors = full_best[
        [
            "dataset",
            "n_samples",
            "input_dim",
            "output_dim",
            "model",
            "mean_r2",
            "mean_nrmse",
            "std_r2",
            "std_nrmse",
        ]
    ].rename(
        columns={
            "input_dim": "full_input_dim",
            "model": "full_best_model",
            "mean_r2": "full_best_mean_r2",
            "mean_nrmse": "full_best_mean_nrmse",
        }
    )
    factors = factors.merge(selected_best, on="dataset", how="left")
    if not comparison.empty:
        factors = factors.merge(
            comparison[["dataset", "dim_reduction_rate", "delta_r2_selected_minus_full", "delta_nrmse_selected_minus_full"]],
            on="dataset",
            how="left",
        )
    return factors.sort_values("full_best_mean_nrmse").reset_index(drop=True)


def write_markdown_summary(
    path: Path,
    best: pd.DataFrame,
    target_best: pd.DataFrame,
    comparison: pd.DataFrame,
    factors: pd.DataFrame,
) -> None:
    best_view = best[
        [
            "dataset",
            "feature_set",
            "model",
            "input_dim",
            "output_dim",
            "mean_r2",
            "mean_mae",
            "mean_rmse",
            "mean_nmae",
            "mean_nrmse",
            "std_r2",
            "std_nrmse",
            "rank_score",
        ]
    ].copy()
    for col in ["mean_r2", "mean_mae", "mean_rmse", "mean_nmae", "mean_nrmse", "std_r2", "std_nrmse", "rank_score"]:
        best_view[col] = best_view[col].round(4)

    target_best_view = target_best[
        [
            "dataset",
            "target",
            "feature_set",
            "model",
            "r2",
            "mae",
            "rmse",
            "nmae",
            "nrmse",
            "target_rank_score",
        ]
    ].copy()
    for col in ["r2", "mae", "rmse", "nmae", "nrmse", "target_rank_score"]:
        target_best_view[col] = target_best_view[col].round(4)

    comparison_view = comparison.copy()
    for col in comparison_view.select_dtypes(include="number").columns:
        comparison_view[col] = comparison_view[col].round(4)

    factor_view = factors.copy()
    for col in factor_view.select_dtypes(include="number").columns:
        factor_view[col] = factor_view[col].round(4)

    lines = [
        "# B题问题2：模型构建与精度评估结果",
        "",
        "本报告由 `scripts/run_problem2_modeling.py` 自动生成，对全特征集和问题1筛选特征集分别训练并评价模型。",
        "",
        "## 方法说明",
        "",
        "- 训练测试划分：80% 训练集，20% 测试集，固定随机种子。",
        "- 候选模型：Ridge、KNN、随机森林、梯度提升树。",
        "- 单输出和多输出均计算 R2、MAE、RMSE、NMAE、NRMSE。",
        "- 模型排序：`Score = 0.4 * R2排名 + 0.35 * NRMSE排名 + 0.25 * NMAE排名`，分数越小越优。",
        "",
        "## 每个数据集的最佳模型",
        "",
    ]
    lines.extend(_markdown_table(best_view))
    lines.extend(["", "## 每个输出变量的最佳模型", ""])
    lines.extend(_markdown_table(target_best_view.groupby("dataset").head(6)))
    lines.extend(["", "## 全特征与筛选特征对比", ""])
    lines.extend(_markdown_table(comparison_view))
    lines.extend(["", "## 数据规模、输入维度和输出维度影响", ""])
    lines.extend(_markdown_table(factor_view))
    lines.extend(
        [
            "",
            "## 输出文件",
            "",
            "- `tables/model_metrics_all.csv`：所有数据集、特征集、模型的聚合指标和综合排名。",
            "- `tables/target_metrics_all.csv`：每个输出变量的 R2、MAE、RMSE、NMAE、NRMSE。",
            "- `tables/best_models_by_target.csv`：每个输出变量的最佳模型和最佳特征集。",
            "- `tables/best_models_by_dataset.csv`：每个数据集和特征集下的最佳模型。",
            "- `tables/feature_set_comparison.csv`：全特征与筛选特征的最佳模型对比。",
            "- `tables/dataset_factor_analysis.csv`：样本规模、输入维度、输出维度与模型表现的汇总。",
            "- `figures/`：模型精度对比、特征筛选效果对比和数据集难度图。",
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
