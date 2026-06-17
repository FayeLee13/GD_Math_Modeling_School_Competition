"""Problem 3 model explainability and physical consistency analysis."""

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
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

from .dataset_config import DatasetSpec
from .problem2_modeling import build_models


@dataclass(frozen=True)
class ExplainabilityResult:
    permutation_importance: pd.DataFrame
    sensitivity: pd.DataFrame
    partial_dependence: pd.DataFrame
    consistency: pd.DataFrame


PHYSICAL_EXPECTED_DIRECTIONS: dict[str, dict[str, dict[str, int]]] = {
    "heat": {
        "T": {
            "qprime": 1,
            "Tin": 1,
            "R": 1,
            "L": 1,
            "k": -1,
            "mdot": -1,
            "Cp": -1,
        }
    },
    "rea": {
        "max_power": {"rod_worth": 1, "beta": -1},
        "burst_width": {"rod_worth": -1, "beta": 1},
        "max_Tf": {"rod_worth": 1, "h_gap": -1},
        "avg_Tcool": {"rod_worth": 1, "gamma_frac": 1},
    },
    "xs": {
        "k": {
            "FissionFast": 1,
            "FissionThermal": 1,
            "CaptureFast": -1,
            "CaptureThermal": -1,
            "Scatter12": 1,
            "Scatter21": -1,
        }
    },
    "chf": {
        "CHF (kW m-2)": {
            "G (kg m-2s-1)": 1,
            "P (kPa)": 1,
            "D (m)": -1,
            "L (m)": -1,
            "Xe (-)": -1,
        }
    },
}


def explain_dataset(
    spec: DatasetSpec,
    x: pd.DataFrame,
    y: pd.DataFrame,
    model_name: str,
    feature_set: str,
    random_state: int = 42,
    test_size: float = 0.2,
    top_features: int = 3,
    n_repeats: int = 6,
    n_jobs: int = 2,
) -> ExplainabilityResult:
    x_num = x.apply(pd.to_numeric, errors="coerce")
    y_num = y.apply(pd.to_numeric, errors="coerce")

    indices = np.arange(len(x_num))
    train_idx, test_idx = train_test_split(indices, test_size=test_size, random_state=random_state)
    x_train = x_num.iloc[train_idx].reset_index(drop=True)
    x_test = x_num.iloc[test_idx].reset_index(drop=True)
    y_train = y_num.iloc[train_idx].reset_index(drop=True)
    y_test = y_num.iloc[test_idx].reset_index(drop=True)

    model = clone(build_models(random_state)[model_name])
    fit_target = y_train.iloc[:, 0] if y_train.shape[1] == 1 and model_name != "GradientBoosting" else y_train
    model.fit(x_train, fit_target)

    perm = permutation_importance(
        model,
        x_test,
        y_test.iloc[:, 0] if y_test.shape[1] == 1 and model_name != "GradientBoosting" else y_test,
        scoring="r2",
        n_repeats=n_repeats,
        random_state=random_state,
        n_jobs=n_jobs,
    )
    permutation_table = pd.DataFrame(
        {
            "dataset": spec.name,
            "feature_set": feature_set,
            "model": model_name,
            "feature": x_num.columns,
            "importance_mean": perm.importances_mean,
            "importance_std": perm.importances_std,
        }
    ).sort_values("importance_mean", ascending=False, ignore_index=True)
    permutation_table["importance_rank"] = np.arange(1, len(permutation_table) + 1)
    permutation_table["physical_score"] = permutation_table["feature"].map(spec.physical_scores or {}).fillna(0.5)

    top = permutation_table.head(top_features)["feature"].tolist()
    sensitivity = sensitivity_analysis(spec, model, x_test, y_test, top)
    pdp = partial_dependence_response(spec, model, x_test, top[:2], grid_points=15)
    consistency = physical_consistency(spec, model_name, permutation_table, sensitivity, y_test)

    return ExplainabilityResult(
        permutation_importance=permutation_table,
        sensitivity=sensitivity,
        partial_dependence=pdp,
        consistency=consistency,
    )


def sensitivity_analysis(
    spec: DatasetSpec,
    model: object,
    x_base: pd.DataFrame,
    y_test: pd.DataFrame,
    features: list[str],
) -> pd.DataFrame:
    base_pred = _as_frame(model.predict(x_base), y_test.columns)
    ranges = (y_test.max(axis=0) - y_test.min(axis=0)).replace(0, np.nan)
    rows = []
    for feature in features:
        values = x_base[feature]
        feature_range = float(values.max() - values.min())
        for direction, multiplier in [("minus_10pct", -1.0), ("plus_10pct", 1.0)]:
            perturbed = x_base.copy()
            delta = 0.1 * values.abs()
            if float(delta.mean()) == 0.0:
                delta = pd.Series(0.1 * feature_range, index=values.index)
            perturbed[feature] = values + multiplier * delta
            perturbed[feature] = perturbed[feature].clip(lower=x_base[feature].min(), upper=x_base[feature].max())
            pred = _as_frame(model.predict(perturbed), y_test.columns)
            diff = pred - base_pred
            for target in y_test.columns:
                mean_delta = float(diff[target].mean())
                rows.append(
                    {
                        "dataset": spec.name,
                        "feature": feature,
                        "target": target,
                        "perturbation": direction,
                        "mean_prediction_delta": mean_delta,
                        "normalized_mean_delta": float(mean_delta / ranges[target]) if pd.notna(ranges[target]) else np.nan,
                        "response_direction": _sign(mean_delta),
                        "expected_direction": _expected_direction(spec.name, feature, target, direction),
                        "direction_consistent": _direction_consistent(spec.name, feature, target, direction, mean_delta),
                    }
                )
    return pd.DataFrame(rows)


def partial_dependence_response(
    spec: DatasetSpec,
    model: object,
    x_base: pd.DataFrame,
    features: list[str],
    grid_points: int,
) -> pd.DataFrame:
    rows = []
    for feature in features:
        low, high = x_base[feature].quantile([0.05, 0.95])
        grid = np.linspace(float(low), float(high), grid_points)
        for value in grid:
            frame = x_base.copy()
            frame[feature] = value
            pred = _as_frame(model.predict(frame), None)
            for target in pred.columns:
                rows.append(
                    {
                        "dataset": spec.name,
                        "feature": feature,
                        "grid_value": value,
                        "target": target,
                        "mean_prediction": float(pred[target].mean()),
                    }
                )
    return pd.DataFrame(rows)


def physical_consistency(
    spec: DatasetSpec,
    model_name: str,
    permutation_table: pd.DataFrame,
    sensitivity: pd.DataFrame,
    y_test: pd.DataFrame,
) -> pd.DataFrame:
    top3 = permutation_table.head(3)
    top_physical_score = float(top3["physical_score"].mean()) if len(top3) else 0.0
    positive_importance_ratio = float((top3["importance_mean"] > 0).mean()) if len(top3) else 0.0

    known_direction = sensitivity[sensitivity["expected_direction"] != 0]
    if known_direction.empty:
        direction_consistency_rate: float | str = "not_configured"
    else:
        direction_consistency_rate = float(known_direction["direction_consistent"].mean())

    output_dim = y_test.shape[1]
    if top_physical_score >= 0.8 and positive_importance_ratio >= 0.67:
        if isinstance(direction_consistency_rate, float) and direction_consistency_rate >= 0.6:
            level = "high"
        else:
            level = "medium"
    elif top_physical_score >= 0.6 or positive_importance_ratio >= 0.5:
        level = "medium"
    else:
        level = "low"

    return pd.DataFrame(
        [
            {
                "dataset": spec.name,
                "model": model_name,
                "output_dim": output_dim,
                "top_features": ", ".join(top3["feature"].tolist()),
                "top_physical_score": top_physical_score,
                "positive_importance_ratio_top3": positive_importance_ratio,
                "known_direction_consistency_rate": direction_consistency_rate,
                "physical_consistency_level": level,
                "interpretation_note": _interpretation_note(level, direction_consistency_rate),
            }
        ]
    )


def save_explainability_figures(
    permutation_table: pd.DataFrame,
    sensitivity: pd.DataFrame,
    pdp: pd.DataFrame,
    figures_dir: Path,
) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=0.85)
    dataset = permutation_table["dataset"].iloc[0]

    plot_perm = permutation_table.sort_values("importance_mean", ascending=True)
    plt.close("all")
    fig, ax = plt.subplots(figsize=(8, min(7.0, max(3.5, 0.38 * len(plot_perm)))))
    ax.barh(plot_perm["feature"], plot_perm["importance_mean"], xerr=plot_perm["importance_std"], color="#1f77b4")
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_xlabel("Permutation importance (R2 decrease)")
    ax.set_ylabel("Feature")
    ax.set_title(f"{dataset}: model dependency by permutation importance")
    _safe_tight_layout(fig)
    fig.savefig(figures_dir / f"{dataset}_permutation_importance.png", dpi=160)
    plt.close(fig)

    if not sensitivity.empty:
        heat = (
            sensitivity[sensitivity["perturbation"] == "plus_10pct"]
            .pivot_table(index="feature", columns="target", values="normalized_mean_delta", aggfunc="mean")
            .fillna(0)
        )
        fig, ax = plt.subplots(figsize=(min(12.0, max(6, 0.6 * len(heat.columns))), min(7.0, max(3.5, 0.5 * len(heat)))))
        sns.heatmap(heat, cmap="vlag", center=0, linewidths=0.3, ax=ax)
        ax.set_title(f"{dataset}: +10% sensitivity response")
        ax.set_xlabel("Target")
        ax.set_ylabel("Perturbed feature")
        _safe_tight_layout(fig)
        fig.savefig(figures_dir / f"{dataset}_sensitivity_heatmap.png", dpi=160)
        plt.close(fig)

    if not pdp.empty:
        for feature, group in pdp.groupby("feature"):
            targets = list(group["target"].unique())
            show_targets = targets[: min(4, len(targets))]
            fig, ax = plt.subplots(figsize=(7.5, 4.5))
            for target in show_targets:
                part = group[group["target"] == target]
                y = part["mean_prediction"]
                y_norm = (y - y.min()) / (y.max() - y.min()) if y.max() != y.min() else y * 0
                ax.plot(part["grid_value"], y_norm, marker="o", linewidth=1.4, label=target)
            ax.set_xlabel(feature)
            ax.set_ylabel("Normalized mean prediction")
            ax.set_title(f"{dataset}: partial response for {feature}")
            ax.legend()
            _safe_tight_layout(fig)
            safe_feature = _safe_name(feature)
            fig.savefig(figures_dir / f"{dataset}_partial_response_{safe_feature}.png", dpi=160)
            plt.close(fig)


def _as_frame(prediction: object, columns: pd.Index | None) -> pd.DataFrame:
    array = np.asarray(prediction)
    if array.ndim == 1:
        array = array.reshape(-1, 1)
    if columns is None:
        columns = pd.Index([f"target_{i + 1}" for i in range(array.shape[1])])
    return pd.DataFrame(array, columns=columns)


def _expected_direction(dataset: str, feature: str, target: str, perturbation: str) -> int:
    expected = PHYSICAL_EXPECTED_DIRECTIONS.get(dataset, {}).get(target, {}).get(feature, 0)
    if perturbation == "minus_10pct":
        expected *= -1
    return expected


def _direction_consistent(dataset: str, feature: str, target: str, perturbation: str, observed_delta: float) -> bool:
    expected = _expected_direction(dataset, feature, target, perturbation)
    if expected == 0:
        return False
    return _sign(observed_delta) == expected


def _sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def _interpretation_note(level: str, direction_rate: float) -> str:
    if level == "high":
        return "Key dependencies are physically plausible and response checks are mostly regular."
    if level == "medium":
        if not isinstance(direction_rate, float):
            return "Key dependencies are plausible, but explicit direction checks are limited for this dataset."
        return "Most dependencies are plausible, but some response directions need cautious discussion."
    return "Model dependencies or response trends need careful qualification before physical interpretation."


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value).strip("_")


def _safe_tight_layout(fig: plt.Figure) -> None:
    try:
        fig.tight_layout()
    except MemoryError:
        pass
