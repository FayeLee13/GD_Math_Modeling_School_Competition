"""
Generate all required charts per 标准化指标与图表.md specification.

Reads CSV results already produced by run_all.py (or the raw datasets), then
saves charts into reports/charts/{problem1,problem2,problem3}/<dataset>/.

Problem 1 charts (per dataset):
  1. Input-output correlation chart (bar for single-output, heatmap for multi-output)
  2. RF non-linear importance bar chart
  3. Input redundancy heatmap
  4. Integrated score ranking chart (horizontal bar, 3-color)

Problem 2 charts (per dataset):
  1. Model accuracy comparison table figure
  2. Three-metric faceted bar chart (R², RMSE, MAE in separate subplots)
  3. True vs predicted scatter plot (best model only, with y=x line)
  4. Full vs selected features comparison chart

Problem 3 charts (per dataset):
  1. Permutation importance horizontal bar chart
  2. Sensitivity perturbation chart (±10%, side-by-side)
  3. PDP chart (top 2~3 features)
  4. Physical consistency evaluation table figure
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dataset_config import DATASET_SPECS, load_dataset

# ──────────────────────────────────────────────
# Palette & style constants
# ──────────────────────────────────────────────
LEVEL_COLORS = {
    "core":         "#2563eb",   # vivid blue
    "candidate":    "#f59e0b",   # amber
    "low_priority": "#6b7280",   # cool grey
}
MODEL_PALETTE = sns.color_palette("tab10", 4)
STYLE = {"style": "whitegrid", "font_scale": 0.9}
DPI = 180


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate all standard charts.")
    parser.add_argument("--data-dir",     type=Path, default=Path("datasets"))
    parser.add_argument("--problem1-dir", type=Path, default=Path("reports/problem1"))
    parser.add_argument("--problem2-dir", type=Path, default=Path("reports/problem2"))
    parser.add_argument("--problem3-dir", type=Path, default=Path("reports/problem3"))
    parser.add_argument("--out-dir",      type=Path, default=Path("reports/charts"))
    return parser.parse_args()


# ══════════════════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    args = parse_args()
    sns.set_theme(**STYLE)

    # Load shared CSV outputs produced by run_all.py
    p1_tables = args.problem1_dir / "tables"
    p2_tables = args.problem2_dir / "tables"
    p3_tables = args.problem3_dir / "tables"

    scores_all   = pd.read_csv(p1_tables / "feature_scores_all.csv")
    corr_all     = pd.read_csv(p1_tables / "input_output_correlations_all.csv")
    metrics_all  = pd.read_csv(p2_tables / "model_metrics_all.csv")
    best_all     = pd.read_csv(p2_tables / "best_models_by_dataset.csv")
    preds_all    = pd.read_csv(p2_tables / "predictions_all.csv")
    comparison   = pd.read_csv(p2_tables / "feature_set_comparison.csv")
    perm_all     = pd.read_csv(p3_tables / "permutation_importance_all.csv")
    sens_all     = pd.read_csv(p3_tables / "sensitivity_analysis_all.csv")
    pdp_all      = pd.read_csv(p3_tables / "partial_response_all.csv")
    consist_all  = pd.read_csv(p3_tables / "physical_consistency_summary.csv")

    for spec in DATASET_SPECS:
        ds = spec.name
        print(f"[charts] generating charts for: {ds}", flush=True)

        out1 = args.out_dir / "problem1" / ds
        out2 = args.out_dir / "problem2" / ds
        out3 = args.out_dir / "problem3" / ds
        for d in (out1, out2, out3):
            d.mkdir(parents=True, exist_ok=True)

        # Load raw data for this dataset
        x, y = load_dataset(spec, args.data_dir)
        x_num = x.apply(pd.to_numeric, errors="coerce")
        y_num = y.apply(pd.to_numeric, errors="coerce")

        score_ds = scores_all[scores_all["dataset"] == ds]
        corr_ds  = corr_all[corr_all["dataset"] == ds]

        # ── Problem 1 ────────────────────────────────────────────────────────
        plot_p1_correlation(ds, x_num, y_num, corr_ds, out1)
        plot_p1_rf_importance(ds, score_ds, out1)
        plot_p1_redundancy_heatmap(ds, x_num, out1)
        plot_p1_score_ranking(ds, score_ds, out1)

        # ── Problem 2 ────────────────────────────────────────────────────────
        metrics_ds  = metrics_all[metrics_all["dataset"] == ds]
        best_ds     = best_all[best_all["dataset"] == ds]
        preds_ds    = preds_all[preds_all["dataset"] == ds]

        plot_p2_accuracy_table(ds, metrics_ds, out2)
        plot_p2_three_metric_facets(ds, metrics_ds, out2)
        plot_p2_parity(ds, best_ds, preds_ds, y_num, out2)
        plot_p2_feature_comparison(ds, comparison, out2)

        # ── Problem 3 ────────────────────────────────────────────────────────
        perm_ds   = perm_all[perm_all["dataset"] == ds]
        sens_ds   = sens_all[sens_all["dataset"] == ds]
        pdp_ds    = pdp_all[pdp_all["dataset"] == ds]
        cons_ds   = consist_all[consist_all["dataset"] == ds]

        plot_p3_permutation(ds, perm_ds, out3)
        plot_p3_sensitivity(ds, sens_ds, out3)
        plot_p3_pdp(ds, pdp_ds, out3)
        plot_p3_consistency_table(ds, cons_ds, out3)

    print(f"[charts] all charts saved to {args.out_dir}", flush=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Problem 1 charts
# ══════════════════════════════════════════════════════════════════════════════

def plot_p1_correlation(
    ds: str,
    x: pd.DataFrame,
    y: pd.DataFrame,
    corr_long: pd.DataFrame,
    out: Path,
) -> None:
    """Chart 1: Input-output correlation — bar (single-output) or heatmap (multi-output)."""
    single_output = y.shape[1] == 1

    # Compute Pearson and Spearman mean abs corr per feature
    def _abs_corr(method: str) -> pd.Series:
        sub = corr_long[corr_long["method"] == method]
        return sub.groupby("feature")["abs_corr"].mean()

    pearson_s  = _abs_corr("pearson")
    spearman_s = _abs_corr("spearman")

    if single_output:
        # Side-by-side bar chart
        features = list(pearson_s.index)
        x_idx = np.arange(len(features))
        width = 0.38
        fig, ax = plt.subplots(figsize=(max(7, 0.6 * len(features)), 4.5))
        ax.bar(x_idx - width / 2, pearson_s.reindex(features).fillna(0),
               width, label="Pearson |r|",  color="#2563eb", alpha=0.85)
        ax.bar(x_idx + width / 2, spearman_s.reindex(features).fillna(0),
               width, label="Spearman |ρ|", color="#f59e0b", alpha=0.85)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(features, rotation=30, ha="right")
        ax.set_ylabel("Mean |correlation|")
        ax.set_title(f"{ds}: Input–Output Correlation (Pearson & Spearman)")
        ax.legend()
        ax.set_ylim(0, 1.05)
        _tight(fig)
        fig.savefig(out / f"{ds}_p1_correlation.png", dpi=DPI)
        plt.close(fig)
    else:
        # Heatmap (use raw Pearson here for multi-output)
        heat_p = corr_long[corr_long["method"] == "pearson"].pivot_table(
            index="feature", columns="target", values="corr", aggfunc="mean"
        )
        heat_s = corr_long[corr_long["method"] == "spearman"].pivot_table(
            index="feature", columns="target", values="corr", aggfunc="mean"
        )
        fig, axes = plt.subplots(1, 2, figsize=(max(10, 0.9 * y.shape[1] + 4), max(4, 0.35 * x.shape[1])))
        for ax, heat, title in zip(
            axes,
            [heat_p, heat_s],
            ["Pearson r", "Spearman ρ"],
        ):
            sns.heatmap(heat, ax=ax, cmap="vlag", center=0, linewidths=0.25,
                        annot=(heat.shape[1] <= 8), fmt=".2f", cbar=True)
            ax.set_title(f"{ds}: {title}")
            ax.set_xlabel("Target")
            ax.set_ylabel("Feature")
        _tight(fig)
        fig.savefig(out / f"{ds}_p1_correlation.png", dpi=DPI)
        plt.close(fig)


def plot_p1_rf_importance(ds: str, score: pd.DataFrame, out: Path) -> None:
    """Chart 2: RF non-linear importance bar chart (normalized)."""
    if score.empty or "rf_importance_norm" not in score.columns:
        return
    plot_data = score.sort_values("rf_importance_norm", ascending=True)
    fig, ax = plt.subplots(figsize=(7, max(3.5, 0.38 * len(plot_data))))
    colors = [LEVEL_COLORS.get(lvl, "#6b7280") for lvl in plot_data["feature_level"]]
    ax.barh(plot_data["feature"], plot_data["rf_importance_norm"], color=colors)
    ax.set_xlabel("Normalized RF Importance")
    ax.set_ylabel("Input Feature")
    ax.set_title(f"{ds}: Random Forest Non-linear Importance (0.3N)")
    ax.set_xlim(0, 1.05)
    # Legend
    from matplotlib.patches import Patch
    legend_handles = [Patch(color=c, label=k) for k, c in LEVEL_COLORS.items()]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=8)
    _tight(fig)
    fig.savefig(out / f"{ds}_p1_rf_importance.png", dpi=DPI)
    plt.close(fig)


def plot_p1_redundancy_heatmap(ds: str, x: pd.DataFrame, out: Path) -> None:
    """Chart 3: Input variable redundancy heatmap."""
    if x.shape[1] < 2:
        return
    corr = x.corr(method="pearson")
    size = max(5, 0.6 * x.shape[1])
    fig, ax = plt.subplots(figsize=(size, size * 0.85))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)  # show lower triangle
    sns.heatmap(
        corr, ax=ax, mask=mask, cmap="coolwarm", center=0,
        square=True, linewidths=0.3,
        annot=(corr.shape[0] <= 12), fmt=".2f",
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title(f"{ds}: Input Redundancy Heatmap (Pearson |r|)")
    _tight(fig)
    fig.savefig(out / f"{ds}_p1_redundancy_heatmap.png", dpi=DPI)
    plt.close(fig)


def plot_p1_score_ranking(ds: str, score: pd.DataFrame, out: Path) -> None:
    """Chart 4: Integrated score ranking — horizontal bar, 3-color."""
    if score.empty or "dp_fsm_score" not in score.columns:
        return
    plot_data = score.sort_values("dp_fsm_score", ascending=True)
    colors = [LEVEL_COLORS.get(lvl, "#6b7280") for lvl in plot_data["feature_level"]]
    fig, ax = plt.subplots(figsize=(8, max(3.5, 0.42 * len(plot_data))))
    bars = ax.barh(plot_data["feature"], plot_data["dp_fsm_score"], color=colors)
    # Annotate values
    for bar, val in zip(bars, plot_data["dp_fsm_score"]):
        ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", fontsize=7.5)
    ax.set_xlabel("DP-FSM Score  S = 0.3C + 0.3N + 0.3P − 0.1R")
    ax.set_ylabel("Input Feature")
    ax.set_title(f"{ds}: Integrated Feature Score Ranking")
    ax.set_xlim(0, min(1.15, plot_data["dp_fsm_score"].max() * 1.25 + 0.05))
    # Threshold lines
    ax.axvline(0.65, color="#1d4ed8", linewidth=1, linestyle="--", alpha=0.6, label="Core ≥ 0.65")
    ax.axvline(0.45, color="#d97706", linewidth=1, linestyle="--", alpha=0.6, label="Candidate ≥ 0.45")
    from matplotlib.patches import Patch
    legend_handles = [
        Patch(color=LEVEL_COLORS["core"],         label="Core"),
        Patch(color=LEVEL_COLORS["candidate"],     label="Candidate"),
        Patch(color=LEVEL_COLORS["low_priority"],  label="Low priority"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=8)
    _tight(fig)
    fig.savefig(out / f"{ds}_p1_score_ranking.png", dpi=DPI)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
#  Problem 2 charts
# ══════════════════════════════════════════════════════════════════════════════

def plot_p2_accuracy_table(ds: str, metrics: pd.DataFrame, out: Path) -> None:
    """Chart 1: Model accuracy comparison rendered as a table figure."""
    if metrics.empty:
        return
    cols = ["model", "feature_set", "mean_r2", "mean_rmse", "mean_mae", "mean_nrmse", "std_r2"]
    view = metrics[cols].copy()
    for c in ["mean_r2", "mean_rmse", "mean_mae", "mean_nrmse", "std_r2"]:
        view[c] = view[c].round(4)
    view.columns = ["Model", "Feature Set", "Mean R²", "Mean RMSE", "Mean MAE", "Mean NRMSE", "Std R²"]

    n_rows = len(view) + 1
    fig, ax = plt.subplots(figsize=(12, max(2.5, 0.38 * n_rows)))
    ax.axis("off")
    tbl = ax.table(
        cellText=view.values,
        colLabels=view.columns,
        loc="center",
        cellLoc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1, 1.35)
    # Header style
    for j in range(len(view.columns)):
        tbl[(0, j)].set_facecolor("#1e3a5f")
        tbl[(0, j)].set_text_props(color="white", fontweight="bold")
    # Alternating rows
    for i in range(1, n_rows):
        bg = "#f0f4ff" if i % 2 == 0 else "white"
        for j in range(len(view.columns)):
            tbl[(i, j)].set_facecolor(bg)
    ax.set_title(f"{ds}: Model Accuracy Comparison", fontsize=11, pad=12)
    _tight(fig)
    fig.savefig(out / f"{ds}_p2_accuracy_table.png", dpi=DPI)
    plt.close(fig)


def plot_p2_three_metric_facets(ds: str, metrics: pd.DataFrame, out: Path) -> None:
    """Chart 2: Three-metric faceted bar chart — R², RMSE, MAE in 3 separate subplots."""
    if metrics.empty:
        return
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    metric_info = [
        ("mean_r2",   "Mean R²",   True,  "#2563eb"),
        ("mean_rmse", "Mean RMSE", False, "#dc2626"),
        ("mean_mae",  "Mean MAE",  False, "#f59e0b"),
    ]
    for ax, (col, label, _higher_is_better, base_color) in zip(axes, metric_info):
        if col not in metrics.columns:
            continue
        plot = metrics.copy()
        x_pos = np.arange(len(plot["model"].unique()))
        feature_sets = plot["feature_set"].unique()
        width = 0.38
        offsets = np.linspace(-width / 2 * (len(feature_sets) - 1),
                               width / 2 * (len(feature_sets) - 1),
                               len(feature_sets))
        models_ordered = sorted(plot["model"].unique())
        for offset, fs, color in zip(offsets, feature_sets, ["#2563eb", "#f59e0b"]):
            sub = plot[plot["feature_set"] == fs].set_index("model").reindex(models_ordered)
            ax.bar(x_pos + offset, sub[col].fillna(0), width * 0.9,
                   label=f"{fs}", color=color, alpha=0.85)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(models_ordered, rotation=20, ha="right", fontsize=8)
        ax.set_ylabel(label)
        ax.set_title(label)
        ax.legend(fontsize=7.5)
        if col == "mean_r2":
            ax.axhline(0, color="#555", linewidth=0.7)
    fig.suptitle(f"{ds}: Three-Metric Model Comparison", fontsize=11, y=1.01)
    _tight(fig)
    fig.savefig(out / f"{ds}_p2_three_metrics.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_p2_parity(
    ds: str,
    best: pd.DataFrame,
    preds: pd.DataFrame,
    y_num: pd.DataFrame,
    out: Path,
) -> None:
    """Chart 3: True vs predicted scatter plot — best model, y=x reference line."""
    full_best = best[best["feature_set"] == "full"]
    if full_best.empty:
        return
    best_model = full_best.sort_values("rank_score").iloc[0]["model"]
    sub = preds[(preds["model"] == best_model) & (preds["feature_set"] == "full")]
    if sub.empty:
        return

    targets = sub["target"].unique()
    ncols = min(3, len(targets))
    nrows = int(np.ceil(len(targets) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4.5 * nrows), squeeze=False)

    for idx, target in enumerate(targets):
        ax = axes[idx // ncols][idx % ncols]
        part = sub[sub["target"] == target]
        ax.scatter(part["y_true"], part["y_pred"], s=18, alpha=0.55, color="#2563eb", edgecolors="none")
        lo = min(part["y_true"].min(), part["y_pred"].min())
        hi = max(part["y_true"].max(), part["y_pred"].max())
        ax.plot([lo, hi], [lo, hi], "r--", linewidth=1.2, label="y = x")
        ax.set_xlabel("True value")
        ax.set_ylabel("Predicted value")
        ax.set_title(f"{target}")
        ax.legend(fontsize=7.5)

    # Hide unused subplots
    for idx in range(len(targets), nrows * ncols):
        axes[idx // ncols][idx % ncols].set_visible(False)

    fig.suptitle(f"{ds}: True vs Predicted — Best Model: {best_model}", fontsize=11)
    _tight(fig)
    fig.savefig(out / f"{ds}_p2_parity.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_p2_feature_comparison(ds: str, comparison: pd.DataFrame, out: Path) -> None:
    """Chart 4: Full vs selected features comparison (delta R², NRMSE, dim reduction)."""
    row = comparison[comparison["dataset"] == ds]
    if row.empty:
        return
    row = row.iloc[0]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Sub-chart A: delta R²
    ax = axes[0]
    delta_r2 = float(row.get("delta_r2_selected_minus_full", np.nan))
    color_r2 = "#16a34a" if not np.isnan(delta_r2) and delta_r2 >= -0.02 else "#dc2626"
    ax.bar(["Selected − Full"], [delta_r2 if not np.isnan(delta_r2) else 0],
           color=color_r2, alpha=0.85)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("ΔR²")
    ax.set_title("Feature Screening: ΔR²")
    if not np.isnan(delta_r2):
        ax.text(0, delta_r2 + 0.002, f"{delta_r2:+.4f}", ha="center", fontsize=9)

    # Sub-chart B: dimension reduction
    ax = axes[1]
    full_dim = int(row.get("full_input_dim", 0))
    sel_dim  = int(row.get("selected_input_dim", 0))
    ax.bar(["Full", "Selected"], [full_dim, sel_dim], color=["#2563eb", "#f59e0b"], alpha=0.85)
    ax.set_ylabel("# Features")
    ax.set_title(f"Feature Count  (reduction {1 - sel_dim/full_dim:.0%})" if full_dim > 0 else "Feature Count")
    for x_pos, val in zip([0, 1], [full_dim, sel_dim]):
        ax.text(x_pos, val + 0.05, str(val), ha="center", fontsize=9)

    # Sub-chart C: NRMSE comparison
    ax = axes[2]
    full_nrmse = float(row.get("full_mean_nrmse", np.nan))
    sel_nrmse  = float(row.get("selected_mean_nrmse", np.nan))
    vals = [v for v in [full_nrmse, sel_nrmse] if not np.isnan(v)]
    labels = [lbl for lbl, v in [("Full", full_nrmse), ("Selected", sel_nrmse)] if not np.isnan(v)]
    ax.bar(labels, vals, color=["#2563eb", "#f59e0b"], alpha=0.85)
    ax.set_ylabel("Mean NRMSE")
    ax.set_title("NRMSE Comparison")
    for x_pos, val in enumerate(vals):
        ax.text(x_pos, val + 0.001, f"{val:.4f}", ha="center", fontsize=9)

    fig.suptitle(f"{ds}: Full vs Selected Feature Set Comparison", fontsize=11)
    _tight(fig)
    fig.savefig(out / f"{ds}_p2_feature_comparison.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
#  Problem 3 charts
# ══════════════════════════════════════════════════════════════════════════════

def plot_p3_permutation(ds: str, perm: pd.DataFrame, out: Path) -> None:
    """Chart 1: Permutation importance horizontal bar chart."""
    if perm.empty:
        return
    plot_data = perm.sort_values("importance_mean", ascending=True)
    fig, ax = plt.subplots(figsize=(8, max(3.5, 0.38 * len(plot_data))))
    # Normalize for display
    max_imp = plot_data["importance_mean"].abs().max()
    norm_imp = plot_data["importance_mean"] / max_imp if max_imp > 0 else plot_data["importance_mean"]
    norm_std = plot_data["importance_std"] / max_imp if max_imp > 0 else plot_data["importance_std"]
    colors = ["#dc2626" if v < 0 else "#2563eb" for v in norm_imp]
    ax.barh(plot_data["feature"], norm_imp, xerr=norm_std, color=colors, alpha=0.85, capsize=3)
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_xlabel("Normalized Permutation Importance")
    ax.set_ylabel("Input Feature")
    ax.set_title(f"{ds}: Permutation Importance")
    _tight(fig)
    fig.savefig(out / f"{ds}_p3_permutation_importance.png", dpi=DPI)
    plt.close(fig)


def plot_p3_sensitivity(ds: str, sens: pd.DataFrame, out: Path) -> None:
    """Chart 2: Sensitivity perturbation chart — +10% and -10% side-by-side."""
    if sens.empty:
        return
    targets = list(sens["target"].unique())
    show_targets = targets[:min(5, len(targets))]
    features = list(sens["feature"].unique())

    fig, axes = plt.subplots(1, 2, figsize=(max(10, 1.8 * len(features)), max(4, 0.45 * len(features))),
                              sharey=True)
    titles = ["+10% Perturbation", "−10% Perturbation"]
    perturb_keys = ["plus_10pct", "minus_10pct"]

    for ax, key, title in zip(axes, perturb_keys, titles):
        sub = sens[sens["perturbation"] == key]
        if sub.empty:
            ax.set_title(title)
            continue
        heat = sub.pivot_table(
            index="feature", columns="target", values="normalized_mean_delta", aggfunc="mean"
        )
        # Keep only shown targets
        heat = heat[[t for t in show_targets if t in heat.columns]]
        sns.heatmap(heat, ax=ax, cmap="vlag", center=0, linewidths=0.3,
                    annot=(heat.shape[1] <= 6), fmt=".3f", cbar=True)
        ax.set_title(title)
        ax.set_xlabel("Target")
        ax.set_ylabel("Perturbed Feature" if key == "plus_10pct" else "")

    fig.suptitle(f"{ds}: Sensitivity Perturbation (±10%)", fontsize=11)
    _tight(fig)
    fig.savefig(out / f"{ds}_p3_sensitivity.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_p3_pdp(ds: str, pdp: pd.DataFrame, out: Path) -> None:
    """Chart 3: Partial Dependence Plot for top 2~3 important features."""
    if pdp.empty:
        return
    features = list(pdp["feature"].unique())[:3]
    targets  = list(pdp["target"].unique())
    show_targets = targets[:min(4, len(targets))]

    ncols = len(features)
    fig, axes = plt.subplots(1, ncols, figsize=(6 * ncols, 4.5), squeeze=False)

    cmap = matplotlib.colormaps.get_cmap("tab10").resampled(max(len(show_targets), 1))
    for col_idx, feature in enumerate(features):
        ax = axes[0][col_idx]
        group = pdp[pdp["feature"] == feature]
        for t_idx, target in enumerate(show_targets):
            part = group[group["target"] == target]
            if part.empty:
                continue
            y = part["mean_prediction"]
            rng = y.max() - y.min()
            y_norm = (y - y.min()) / rng if rng > 0 else y * 0
            ax.plot(part["grid_value"], y_norm, marker="o", markersize=4,
                    linewidth=1.6, color=cmap(t_idx), label=target)
        ax.set_xlabel(feature, fontsize=9)
        ax.set_ylabel("Normalized Mean Prediction" if col_idx == 0 else "")
        ax.set_title(f"PDP: {feature}")
        ax.legend(fontsize=7, loc="best")

    fig.suptitle(f"{ds}: Partial Dependence Plots (Top Features)", fontsize=11)
    _tight(fig)
    fig.savefig(out / f"{ds}_p3_pdp.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_p3_consistency_table(ds: str, consist: pd.DataFrame, out: Path) -> None:
    """Chart 4: Physical consistency evaluation table figure."""
    if consist.empty:
        return

    display_cols = [
        "model",
        "top_features",
        "top_physical_score",
        "positive_importance_ratio_top3",
        "known_direction_consistency_rate",
        "physical_consistency_level",
        "interpretation_note",
    ]
    col_labels = [
        "Model",
        "Top Features",
        "Phys. Score",
        "Positive Imp. Ratio",
        "Direction Consist.",
        "Consistency Level",
        "Interpretation Note",
    ]
    view = consist[[c for c in display_cols if c in consist.columns]].copy()
    for c in ["top_physical_score", "positive_importance_ratio_top3"]:
        if c in view.columns:
            view[c] = view[c].round(3)

    # Wrap long text in note column
    if "interpretation_note" in view.columns:
        view["interpretation_note"] = view["interpretation_note"].apply(
            lambda s: "\n".join([s[i:i+40] for i in range(0, len(str(s)), 40)])
        )

    n_cols = len(view.columns)
    n_rows = len(view) + 1
    fig, ax = plt.subplots(figsize=(max(14, 2.2 * n_cols), max(3, 0.6 * n_rows)))
    ax.axis("off")
    tbl = ax.table(
        cellText=view.values,
        colLabels=col_labels[:n_cols],
        loc="center",
        cellLoc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.6)

    # Color the consistency level cell
    level_cell_col = list(view.columns).index("physical_consistency_level") if "physical_consistency_level" in view.columns else -1
    level_colors_map = {"high": "#bbf7d0", "medium": "#fef9c3", "low": "#fee2e2"}
    for i in range(1, n_rows):
        for j in range(n_cols):
            tbl[(i, j)].set_facecolor("#f8fafc" if i % 2 == 0 else "white")
        if level_cell_col >= 0:
            lvl = str(view.iloc[i - 1]["physical_consistency_level"]) if "physical_consistency_level" in view.columns else ""
            tbl[(i, level_cell_col)].set_facecolor(level_colors_map.get(lvl, "white"))

    for j in range(n_cols):
        tbl[(0, j)].set_facecolor("#1e3a5f")
        tbl[(0, j)].set_text_props(color="white", fontweight="bold")

    ax.set_title(f"{ds}: Physical Consistency Evaluation", fontsize=11, pad=14)
    _tight(fig)
    fig.savefig(out / f"{ds}_p3_consistency_table.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _tight(fig: plt.Figure) -> None:
    try:
        fig.tight_layout()
    except Exception:
        pass


if __name__ == "__main__":
    main()
