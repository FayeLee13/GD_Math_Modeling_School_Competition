"""Problem 2 model training and accuracy evaluation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.base import clone
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

from .dataset_config import DatasetSpec


@dataclass(frozen=True)
class EvaluationResult:
    aggregate_metrics: pd.DataFrame
    target_metrics: pd.DataFrame
    predictions: pd.DataFrame


def build_models(random_state: int) -> dict[str, object]:
    return {
        "Ridge": make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            Ridge(alpha=1.0),
        ),
        "KNN": make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            KNeighborsRegressor(n_neighbors=7, weights="distance"),
        ),
        "RandomForest": make_pipeline(
            SimpleImputer(strategy="median"),
            RandomForestRegressor(
                n_estimators=300,
                max_features="sqrt",
                min_samples_leaf=2,
                random_state=random_state,
                n_jobs=-1,
            ),
        ),
        "GradientBoosting": make_pipeline(
            SimpleImputer(strategy="median"),
            MultiOutputRegressor(
                GradientBoostingRegressor(
                    n_estimators=160,
                    learning_rate=0.05,
                    max_depth=3,
                    random_state=random_state,
                )
            ),
        ),
    }


def evaluate_dataset(
    spec: DatasetSpec,
    x: pd.DataFrame,
    y: pd.DataFrame,
    selected_features: list[str],
    random_state: int = 42,
    test_size: float = 0.2,
) -> EvaluationResult:
    x_num = x.apply(pd.to_numeric, errors="coerce")
    y_num = y.apply(pd.to_numeric, errors="coerce")
    selected = [feature for feature in selected_features if feature in x_num.columns]
    if not selected:
        selected = list(x_num.columns)

    feature_sets = {
        "full": list(x_num.columns),
        "selected": selected,
    }
    models = build_models(random_state)

    aggregate_rows: list[dict[str, object]] = []
    target_rows: list[dict[str, object]] = []
    prediction_rows: list[dict[str, object]] = []

    indices = np.arange(len(x_num))
    train_idx, test_idx = train_test_split(indices, test_size=test_size, random_state=random_state)
    y_train = y_num.iloc[train_idx].reset_index(drop=True)
    y_test = y_num.iloc[test_idx].reset_index(drop=True)
    target_ranges = (y_num.max(axis=0) - y_num.min(axis=0)).replace(0, np.nan)

    for feature_set_name, features in feature_sets.items():
        x_train = x_num.iloc[train_idx][features].reset_index(drop=True)
        x_test = x_num.iloc[test_idx][features].reset_index(drop=True)

        for model_name, model_template in models.items():
            model = clone(model_template)
            fit_target = y_train.iloc[:, 0] if y_train.shape[1] == 1 and model_name != "GradientBoosting" else y_train
            model.fit(x_train, fit_target)
            pred = np.asarray(model.predict(x_test))
            if pred.ndim == 1:
                pred = pred.reshape(-1, 1)
            pred_frame = pd.DataFrame(pred, columns=y_num.columns)

            target_metrics = _target_metrics(
                spec=spec,
                feature_set=feature_set_name,
                model_name=model_name,
                y_true=y_test,
                y_pred=pred_frame,
                target_ranges=target_ranges,
            )
            target_rows.extend(target_metrics.to_dict(orient="records"))

            aggregate_rows.append(
                _aggregate_metrics(
                    spec=spec,
                    feature_set=feature_set_name,
                    model_name=model_name,
                    n_samples=len(x_num),
                    n_train=len(train_idx),
                    n_test=len(test_idx),
                    input_dim=len(features),
                    output_dim=y_num.shape[1],
                    target_metrics=target_metrics,
                )
            )

            prediction_rows.extend(
                _prediction_rows(
                    spec.name,
                    feature_set_name,
                    model_name,
                    test_idx,
                    y_test,
                    pred_frame,
                )
            )

    aggregate = pd.DataFrame(aggregate_rows)
    aggregate = add_rank_scores(aggregate)
    return EvaluationResult(
        aggregate_metrics=aggregate,
        target_metrics=pd.DataFrame(target_rows),
        predictions=pd.DataFrame(prediction_rows),
    )


def add_rank_scores(metrics: pd.DataFrame) -> pd.DataFrame:
    ranked_frames = []
    for (_, feature_set), group in metrics.groupby(["dataset", "feature_set"], sort=False):
        ranked = group.copy()
        ranked["r2_rank"] = ranked["mean_r2"].rank(ascending=False, method="min")
        ranked["nrmse_rank"] = ranked["mean_nrmse"].rank(ascending=True, method="min")
        ranked["nmae_rank"] = ranked["mean_nmae"].rank(ascending=True, method="min")
        ranked["rank_score"] = (
            0.4 * ranked["r2_rank"] + 0.35 * ranked["nrmse_rank"] + 0.25 * ranked["nmae_rank"]
        )
        ranked["model_rank"] = ranked["rank_score"].rank(ascending=True, method="min").astype(int)
        ranked_frames.append(ranked)
    return pd.concat(ranked_frames, ignore_index=True)


def best_models(metrics: pd.DataFrame) -> pd.DataFrame:
    best = (
        metrics.sort_values(
            ["dataset", "feature_set", "rank_score", "mean_nrmse", "mean_nmae"],
            ascending=[True, True, True, True, True],
        )
        .groupby(["dataset", "feature_set"], as_index=False)
        .head(1)
        .reset_index(drop=True)
    )
    return best


def feature_set_comparison(best: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for dataset, group in best.groupby("dataset"):
        full = group[group["feature_set"] == "full"]
        selected = group[group["feature_set"] == "selected"]
        if full.empty or selected.empty:
            continue
        full_row = full.iloc[0]
        selected_row = selected.iloc[0]
        rows.append(
            {
                "dataset": dataset,
                "full_best_model": full_row["model"],
                "selected_best_model": selected_row["model"],
                "full_input_dim": int(full_row["input_dim"]),
                "selected_input_dim": int(selected_row["input_dim"]),
                "dim_reduction_rate": 1.0 - float(selected_row["input_dim"]) / float(full_row["input_dim"]),
                "full_mean_r2": float(full_row["mean_r2"]),
                "selected_mean_r2": float(selected_row["mean_r2"]),
                "delta_r2_selected_minus_full": float(selected_row["mean_r2"] - full_row["mean_r2"]),
                "full_mean_nrmse": float(full_row["mean_nrmse"]),
                "selected_mean_nrmse": float(selected_row["mean_nrmse"]),
                "delta_nrmse_selected_minus_full": float(selected_row["mean_nrmse"] - full_row["mean_nrmse"]),
                "screening_assessment": _screening_assessment(
                    float(selected_row["mean_r2"] - full_row["mean_r2"]),
                    float(selected_row["input_dim"]),
                    float(full_row["input_dim"]),
                ),
            }
        )
    return pd.DataFrame(rows)


def save_figures(metrics: pd.DataFrame, best: pd.DataFrame, comparison: pd.DataFrame, figures_dir: Path) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=0.85)

    for dataset, group in metrics.groupby("dataset"):
        plt.figure(figsize=(9, 4.8))
        sns.barplot(data=group, x="model", y="mean_r2", hue="feature_set")
        plt.axhline(0, color="#555555", linewidth=0.8)
        plt.title(f"{dataset}: model comparison by mean R2")
        plt.xlabel("Model")
        plt.ylabel("Mean R2")
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(figures_dir / f"{dataset}_mean_r2_by_model.png", dpi=180)
        plt.close()

        plt.figure(figsize=(9, 4.8))
        sns.barplot(data=group, x="model", y="mean_nrmse", hue="feature_set")
        plt.title(f"{dataset}: model comparison by mean NRMSE")
        plt.xlabel("Model")
        plt.ylabel("Mean NRMSE")
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(figures_dir / f"{dataset}_mean_nrmse_by_model.png", dpi=180)
        plt.close()

    if not comparison.empty:
        plot = comparison.sort_values("delta_r2_selected_minus_full")
        plt.figure(figsize=(9, max(4.5, 0.45 * len(plot))))
        colors = ["#d62728" if value < -0.02 else "#2ca02c" for value in plot["delta_r2_selected_minus_full"]]
        plt.barh(plot["dataset"], plot["delta_r2_selected_minus_full"], color=colors)
        plt.axvline(0, color="#333333", linewidth=0.8)
        plt.xlabel("Delta mean R2 (selected - full)")
        plt.ylabel("Dataset")
        plt.title("Feature screening validation by best-model R2")
        plt.tight_layout()
        plt.savefig(figures_dir / "feature_set_delta_r2.png", dpi=180)
        plt.close()

    if not best.empty:
        plot = best[best["feature_set"] == "full"].sort_values("mean_nrmse")
        plt.figure(figsize=(9, max(4.5, 0.45 * len(plot))))
        sns.barplot(data=plot, y="dataset", x="mean_nrmse", hue="model", dodge=False)
        plt.xlabel("Best full-feature mean NRMSE")
        plt.ylabel("Dataset")
        plt.title("Dataset difficulty overview")
        plt.tight_layout()
        plt.savefig(figures_dir / "dataset_difficulty_nrmse.png", dpi=180)
        plt.close()


def _target_metrics(
    spec: DatasetSpec,
    feature_set: str,
    model_name: str,
    y_true: pd.DataFrame,
    y_pred: pd.DataFrame,
    target_ranges: pd.Series,
) -> pd.DataFrame:
    rows = []
    for target in y_true.columns:
        true = y_true[target].to_numpy()
        pred = y_pred[target].to_numpy()
        mae = mean_absolute_error(true, pred)
        rmse = mean_squared_error(true, pred) ** 0.5
        r2 = r2_score(true, pred)
        value_range = target_ranges[target]
        rows.append(
            {
                "dataset": spec.name,
                "feature_set": feature_set,
                "model": model_name,
                "target": target,
                "r2": float(r2),
                "mae": float(mae),
                "rmse": float(rmse),
                "nmae": float(mae / value_range) if pd.notna(value_range) else np.nan,
                "nrmse": float(rmse / value_range) if pd.notna(value_range) else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _aggregate_metrics(
    spec: DatasetSpec,
    feature_set: str,
    model_name: str,
    n_samples: int,
    n_train: int,
    n_test: int,
    input_dim: int,
    output_dim: int,
    target_metrics: pd.DataFrame,
) -> dict[str, object]:
    return {
        "dataset": spec.name,
        "feature_set": feature_set,
        "model": model_name,
        "n_samples": n_samples,
        "n_train": n_train,
        "n_test": n_test,
        "input_dim": input_dim,
        "output_dim": output_dim,
        "mean_r2": float(target_metrics["r2"].mean()),
        "mean_mae": float(target_metrics["mae"].mean()),
        "mean_rmse": float(target_metrics["rmse"].mean()),
        "mean_nmae": float(target_metrics["nmae"].mean()),
        "mean_nrmse": float(target_metrics["nrmse"].mean()),
        "std_r2": float(target_metrics["r2"].std(ddof=0)),
        "std_nrmse": float(target_metrics["nrmse"].std(ddof=0)),
    }


def _prediction_rows(
    dataset: str,
    feature_set: str,
    model_name: str,
    test_idx: np.ndarray,
    y_true: pd.DataFrame,
    y_pred: pd.DataFrame,
) -> list[dict[str, object]]:
    rows = []
    for row_pos, original_index in enumerate(test_idx):
        for target in y_true.columns:
            rows.append(
                {
                    "dataset": dataset,
                    "feature_set": feature_set,
                    "model": model_name,
                    "row_index": int(original_index),
                    "target": target,
                    "y_true": float(y_true.iloc[row_pos][target]),
                    "y_pred": float(y_pred.iloc[row_pos][target]),
                    "residual": float(y_true.iloc[row_pos][target] - y_pred.iloc[row_pos][target]),
                }
            )
    return rows


def _screening_assessment(delta_r2: float, selected_dim: float, full_dim: float) -> str:
    if selected_dim == full_dim:
        return "no_dimension_reduction"
    if delta_r2 >= -0.02:
        return "effective_with_small_loss"
    if delta_r2 >= -0.05:
        return "usable_but_accuracy_loss"
    return "too_aggressive_keep_full_or_relax_threshold"
