"""Problem 1 feature analysis and preprocessing utilities."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

from .dataset_config import DatasetSpec


def describe_data_quality(name: str, x: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for role, frame in [("input", x), ("output", y)]:
        for col in frame.columns:
            series = frame[col]
            rows.append(
                {
                    "dataset": name,
                    "role": role,
                    "variable": col,
                    "n_rows": int(len(series)),
                    "missing_count": int(series.isna().sum()),
                    "missing_rate": float(series.isna().mean()),
                    "mean": _safe_float(series.mean()),
                    "std": _safe_float(series.std()),
                    "min": _safe_float(series.min()),
                    "q25": _safe_float(series.quantile(0.25)),
                    "median": _safe_float(series.median()),
                    "q75": _safe_float(series.quantile(0.75)),
                    "max": _safe_float(series.max()),
                    "zero_std": bool(series.std() == 0),
                }
            )
    return pd.DataFrame(rows)


def analyze_dataset(
    spec: DatasetSpec,
    x: pd.DataFrame,
    y: pd.DataFrame,
    figures_dir: Path,
    random_state: int = 42,
) -> dict[str, pd.DataFrame]:
    x_num = x.apply(pd.to_numeric, errors="coerce")
    y_num = y.apply(pd.to_numeric, errors="coerce")

    pearson_abs, pearson_long = _input_output_corr(spec.name, x_num, y_num, method="pearson")
    spearman_abs, spearman_long = _input_output_corr(spec.name, x_num, y_num, method="spearman")
    rf_importance = _random_forest_importance(spec.name, x_num, y_num, random_state=random_state)
    redundancy = _redundancy_summary(spec.name, x_num)
    nonlinear_flags = _nonlinear_flags(spec.name, pearson_abs, spearman_abs, rf_importance)

    score = (
        pearson_abs[["feature", "mean_abs_corr", "max_abs_corr"]]
        .rename(columns={"mean_abs_corr": "pearson_mean_abs", "max_abs_corr": "pearson_max_abs"})
        .merge(
            spearman_abs[["feature", "mean_abs_corr", "max_abs_corr"]].rename(
                columns={"mean_abs_corr": "spearman_mean_abs", "max_abs_corr": "spearman_max_abs"}
            ),
            on="feature",
            how="left",
        )
        .merge(rf_importance.drop(columns=["dataset"], errors="ignore"), on="feature", how="left")
        .merge(redundancy.drop(columns=["dataset"], errors="ignore"), on="feature", how="left")
        .merge(nonlinear_flags.drop(columns=["dataset"], errors="ignore"), on="feature", how="left")
    )

    score["correlation_strength"] = (
        score["pearson_mean_abs"].fillna(0) + score["spearman_mean_abs"].fillna(0)
    ) / 2.0
    score["physical_score"] = score["feature"].map(spec.physical_scores or {}).fillna(0.5)
    score["rf_importance_norm"] = score["rf_importance_norm"].fillna(0)
    score["redundancy_penalty"] = score["redundancy_mean_abs"].fillna(0)
    score["dp_fsm_score"] = (
        0.3 * score["correlation_strength"]
        + 0.3 * score["rf_importance_norm"]
        + 0.3 * score["physical_score"]
        - 0.1 * score["redundancy_penalty"]
    )
    score["feature_level"] = score.apply(_feature_level, axis=1)
    score["selection_decision"] = score.apply(_selection_decision, axis=1)
    score.insert(0, "dataset", spec.name)
    score = score.sort_values(["dp_fsm_score", "rf_importance_norm"], ascending=False).reset_index(drop=True)
    score["rank"] = np.arange(1, len(score) + 1)

    corr_long = pd.concat([pearson_long, spearman_long], ignore_index=True)
    redundancy_pairs = _redundancy_pairs(spec.name, x_num)

    _save_figures(spec.name, x_num, y_num, score, figures_dir)

    return {
        "feature_scores": score,
        "input_output_correlations": corr_long,
        "redundancy_pairs": redundancy_pairs,
    }


def _safe_float(value: object) -> float | None:
    try:
        if pd.isna(value):
            return None
        return float(value)
    except TypeError:
        return None


def _input_output_corr(
    dataset: str,
    x: pd.DataFrame,
    y: pd.DataFrame,
    method: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    long_rows = []
    for feature in x.columns:
        feature_values = x[feature]
        abs_values = []
        for target in y.columns:
            target_values = y[target]
            valid = feature_values.notna() & target_values.notna()
            if valid.sum() < 3 or feature_values[valid].std() == 0 or target_values[valid].std() == 0:
                corr = np.nan
            elif method == "pearson":
                corr = feature_values[valid].corr(target_values[valid], method="pearson")
            elif method == "spearman":
                corr = spearmanr(feature_values[valid], target_values[valid]).correlation
            else:
                raise ValueError(f"Unsupported correlation method: {method}")
            abs_corr = abs(corr) if pd.notna(corr) else np.nan
            abs_values.append(abs_corr)
            long_rows.append(
                {
                    "dataset": dataset,
                    "method": method,
                    "feature": feature,
                    "target": target,
                    "corr": _safe_float(corr),
                    "abs_corr": _safe_float(abs_corr),
                }
            )

        rows.append(
            {
                "feature": feature,
                "mean_abs_corr": float(np.nanmean(abs_values)) if not np.all(np.isnan(abs_values)) else 0.0,
                "max_abs_corr": float(np.nanmax(abs_values)) if not np.all(np.isnan(abs_values)) else 0.0,
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(long_rows)


def _random_forest_importance(
    dataset: str,
    x: pd.DataFrame,
    y: pd.DataFrame,
    random_state: int,
) -> pd.DataFrame:
    model = make_pipeline(
        SimpleImputer(strategy="median"),
        RandomForestRegressor(
            n_estimators=300,
            max_features="sqrt",
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
        ),
    )
    target = y.iloc[:, 0] if y.shape[1] == 1 else y
    model.fit(x, target)
    rf = model.named_steps["randomforestregressor"]
    raw = pd.Series(rf.feature_importances_, index=x.columns, dtype=float)
    max_value = raw.max()
    normalized = raw / max_value if max_value > 0 else raw
    return pd.DataFrame(
        {
            "dataset": dataset,
            "feature": raw.index,
            "rf_importance_raw": raw.values,
            "rf_importance_norm": normalized.values,
        }
    )


def _redundancy_summary(dataset: str, x: pd.DataFrame) -> pd.DataFrame:
    corr = x.corr(method="pearson").abs()
    rows = []
    for feature in x.columns:
        others = corr.loc[feature].drop(index=feature, errors="ignore").dropna()
        rows.append(
            {
                "dataset": dataset,
                "feature": feature,
                "redundancy_mean_abs": float(others.mean()) if len(others) else 0.0,
                "redundancy_max_abs": float(others.max()) if len(others) else 0.0,
                "high_redundancy": bool((others > 0.9).any()) if len(others) else False,
            }
        )
    return pd.DataFrame(rows)


def _redundancy_pairs(dataset: str, x: pd.DataFrame) -> pd.DataFrame:
    corr = x.corr(method="pearson").abs()
    rows = []
    cols = list(corr.columns)
    for i, left in enumerate(cols):
        for right in cols[i + 1 :]:
            value = corr.loc[left, right]
            rows.append(
                {
                    "dataset": dataset,
                    "feature_a": left,
                    "feature_b": right,
                    "abs_pearson_corr": _safe_float(value),
                    "is_high_redundancy": bool(pd.notna(value) and value > 0.9),
                }
            )
    return pd.DataFrame(rows).sort_values("abs_pearson_corr", ascending=False)


def _nonlinear_flags(
    dataset: str,
    pearson_abs: pd.DataFrame,
    spearman_abs: pd.DataFrame,
    rf_importance: pd.DataFrame,
) -> pd.DataFrame:
    frame = (
        pearson_abs[["feature", "mean_abs_corr"]]
        .rename(columns={"mean_abs_corr": "pearson"})
        .merge(
            spearman_abs[["feature", "mean_abs_corr"]].rename(columns={"mean_abs_corr": "spearman"}),
            on="feature",
            how="left",
        )
        .merge(rf_importance[["feature", "rf_importance_norm"]], on="feature", how="left")
    )
    frame["spearman_pearson_gap"] = (frame["spearman"] - frame["pearson"]).abs()
    frame["possible_nonlinear_relation"] = (
        ((frame["rf_importance_norm"] >= 0.5) & (frame["pearson"] < 0.25))
        | (frame["spearman_pearson_gap"] >= 0.2)
    )
    frame.insert(0, "dataset", dataset)
    return frame[["dataset", "feature", "spearman_pearson_gap", "possible_nonlinear_relation"]]


def _feature_level(row: pd.Series) -> str:
    if row["dp_fsm_score"] >= 0.65:
        return "core"
    if row["dp_fsm_score"] >= 0.45:
        return "candidate"
    return "low_priority"


def _selection_decision(row: pd.Series) -> str:
    if row["feature_level"] == "core":
        return "keep_core"
    if row["feature_level"] == "candidate":
        return "keep_candidate"
    if row["physical_score"] >= 1.0 and row["rf_importance_norm"] >= 0.3:
        return "protect_for_validation"
    return "optional_drop_or_compare"


def _save_figures(
    dataset: str,
    x: pd.DataFrame,
    y: pd.DataFrame,
    score: pd.DataFrame,
    figures_dir: Path,
) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=0.85)

    plt.figure(figsize=(8, max(3.5, 0.38 * len(score))))
    plot_data = score.sort_values("dp_fsm_score", ascending=True)
    colors = plot_data["feature_level"].map({"core": "#1f77b4", "candidate": "#ff7f0e", "low_priority": "#7f7f7f"})
    plt.barh(plot_data["feature"], plot_data["dp_fsm_score"], color=colors)
    plt.xlabel("DP-FSM score")
    plt.ylabel("Input feature")
    plt.title(f"{dataset}: feature screening score")
    plt.tight_layout()
    plt.savefig(figures_dir / f"{dataset}_feature_scores.png", dpi=180)
    plt.close()

    if x.shape[1] > 1:
        plt.figure(figsize=(max(6, 0.55 * x.shape[1]), max(5, 0.5 * x.shape[1])))
        sns.heatmap(x.corr(method="pearson"), cmap="coolwarm", center=0, square=True, linewidths=0.3)
        plt.title(f"{dataset}: input-input Pearson correlation")
        plt.tight_layout()
        plt.savefig(figures_dir / f"{dataset}_input_redundancy_heatmap.png", dpi=180)
        plt.close()

    corr = pd.DataFrame(index=x.columns, columns=y.columns, dtype=float)
    for feature in x.columns:
        for target in y.columns:
            corr.loc[feature, target] = x[feature].corr(y[target], method="spearman")
    plt.figure(figsize=(max(5, 0.55 * y.shape[1]), max(4, 0.35 * x.shape[1])))
    sns.heatmap(corr, cmap="vlag", center=0, annot=False, linewidths=0.3)
    plt.title(f"{dataset}: input-output Spearman correlation")
    plt.tight_layout()
    plt.savefig(figures_dir / f"{dataset}_input_output_corr_heatmap.png", dpi=180)
    plt.close()
