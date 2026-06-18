"""Dataset definitions for problem 1 feature analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    input_file: str
    output_file: str | None
    input_columns: list[str]
    output_columns: list[str]
    id_columns: list[str] | None = None
    physical_scores: dict[str, float] | None = None


def _score(columns: list[str], value: float = 1.0) -> dict[str, float]:
    return {col: value for col in columns}


# Dataset-level fallback scores (used for DATASET_PHYSICAL_EVIDENCE metadata only).
# Per-variable scores are now defined individually in each DatasetSpec below,
# derived from the physical plausibility table in integrated_scores_mode_kept_utf8.md.
DATASET_PHYSICAL_SCORES: dict[str, float] = {
    "chf": 0.75,      # average of per-variable scores (0.5,0.5,1,1,1,1)
    "heat": 1.0,
    "xs": 0.875,      # average of per-variable scores
    "fp": 0.654,      # average of per-variable scores
    "bwr": 0.611,     # average of per-variable scores
    "powery": 0.5,
    "rea": 0.5,       # average of per-variable scores (1,1,0,0)
    "htgr": 1.0,      # md says P=1 for heat/microreactor/htgr
    "microreactor": 1.0,
}


def _dataset_score(dataset: str, columns: list[str]) -> dict[str, float]:
    return _score(columns, DATASET_PHYSICAL_SCORES[dataset])


DATASET_SPECS: list[DatasetSpec] = [
    DatasetSpec(
        name="chf",
        input_file="chf.csv",
        output_file=None,
        input_columns=["D (m)", "L (m)", "P (kPa)", "G (kg m-2s-1)", "Tin (C)", "Xe (-)"],
        output_columns=["CHF (kW m-2)"],
        # Per-variable physical scores from integrated_scores_mode_kept_utf8.md (CHF dataset)
        physical_scores={
            "D (m)":           0.5,   # 通道直径：几何修正变量，关系存在但不如 P/G/Xe 直接
            "L (m)":           0.5,   # 加热长度：条件性影响
            "P (kPa)":         1.0,   # 压力：CHF 的核心控制变量
            "G (kg m-2s-1)":   1.0,   # 质量通量：CHF 的经典主变量
            "Tin (C)":         1.0,   # 进口温度：通过入口亚冷度明确影响 CHF
            "Xe (-)":          1.0,   # 出口平衡品质：CHF 预测标准主变量
        },
    ),
    DatasetSpec(
        name="heat",
        input_file="heat.csv",
        output_file=None,
        input_columns=["qprime", "mdot", "Tin", "R", "L", "Cp", "k"],
        output_columns=["T"],
        # heat 数据集所有变量均有明确的热传导方程支持 → 全部 1.0
        physical_scores=_score(["qprime", "mdot", "Tin", "R", "L", "Cp", "k"], 1.0),
    ),
    DatasetSpec(
        name="xs",
        input_file="xs.csv",
        output_file=None,
        input_columns=[
            "FissionFast",
            "CaptureFast",
            "FissionThermal",
            "CaptureThermal",
            "Scatter12",
            "Scatter11",
            "Scatter21",
            "Scatter22",
        ],
        output_columns=["k"],
        # Per-variable scores from integrated_scores_mode_kept_utf8.md (XS dataset)
        physical_scores={
            "FissionFast":    1.0,   # 直接影响快群裂变产生项
            "CaptureFast":    1.0,   # 直接增加快群吸收损失
            "FissionThermal": 1.0,   # 直接影响热群裂变产生项
            "CaptureThermal": 1.0,   # 直接增加热群吸收损失
            "Scatter12":      1.0,   # 直接影响快→热慢化过程，关键群间耦合项
            "Scatter11":      0.5,   # 影响快群能谱与群内分布，属间接作用
            "Scatter21":      0.5,   # 对热→快迁移有影响，但通常不是主导项
            "Scatter22":      0.5,   # 影响热群分布，属间接作用
        },
    ),
    DatasetSpec(
        name="bwr",
        input_file="bwr_input.csv",
        output_file="bwr_output.csv",
        input_columns=[
            "PSZ",
            "DOM",
            "vanA",
            "vanB",
            "subcool",
            "CRD",
            "flow_rate",
            "power_density",
            "VFNGAP",
        ],
        output_columns=["K-eff", "Max3Pin", "Max4Pin", "F-delta-H", "Max-Fxy"],
        # Per-variable scores from integrated_scores_mode_kept_utf8.md (BWR dataset)
        physical_scores={
            "PSZ":           0.5,   # 堆芯形状/运行参数，间接作用
            "DOM":           0.5,
            "vanA":          0.5,
            "vanB":          0.5,
            "subcool":       0.5,   # 入口过冷度，有物理含义但效果通过模拟间接体现
            "CRD":           1.0,   # 控制棒驱动/插入状态，直接影响反应性
            "flow_rate":     0.5,
            "power_density": 1.0,   # 功率密度，直接影响局部功率响应
            "VFNGAP":        0.5,
        },
    ),
    DatasetSpec(
        name="fp",
        input_file="fp_inp.csv",
        output_file="fp_out.csv",
        input_columns=[
            "fuel_dens",
            "porosity",
            "clad_thick",
            "pellet_OD",
            "pellet_h",
            "gap_thick",
            "inlet_T",
            "enrich",
            "rough_fuel",
            "rough_clad",
            "ax_pow",
            "clad_T",
            "pressure",
        ],
        output_columns=[
            "fis_gas_produced",
            "max_fuel_centerline_temp",
            "max_fuel_surface_temp",
            "radial_clad_dia",
        ],
        # Per-variable scores from integrated_scores_mode_kept_utf8.md (FP dataset)
        physical_scores={
            "fuel_dens":   0.5,   # 燃料密度：有间接联系
            "porosity":    1.0,   # 孔隙率：直接影响热传导
            "clad_thick":  1.0,   # 包壳厚度：直接影响热阻
            "pellet_OD":   0.0,   # 燃料芯块外径：未找到足够直接机理
            "pellet_h":    0.0,   # 燃料芯块高度：未找到足够直接机理
            "gap_thick":   1.0,   # 间隙厚度：直接影响间隙热导
            "inlet_T":     1.0,   # 入口温度：直接影响冷却条件
            "enrich":      0.0,   # 富集度：与热性能无直接一阶关系
            "rough_fuel":  1.0,   # 燃料表面粗糙度：影响传热系数
            "rough_clad":  1.0,   # 包壳表面粗糙度：影响传热系数
            "ax_pow":      1.0,   # 轴向功率因子：直接影响热源分布
            "clad_T":      1.0,   # 包壳温度：直接边界条件
            "pressure":    0.0,   # 系统压力：对燃料性能无直接一阶作用
        },
    ),
    DatasetSpec(
        name="rea",
        input_file="rea_inputs.csv",
        output_file="rea_outputs.csv",
        input_columns=["rod_worth", "beta", "h_gap", "gamma_frac"],
        output_columns=["max_power", "burst_width", "max_Tf", "avg_Tcool"],
        # Per-variable scores from integrated_scores_mode_kept_utf8.md (REA dataset)
        physical_scores={
            "rod_worth":   1.0,   # 控制棒价值：直接决定反应性插入量，核心变量
            "beta":        1.0,   # 缓发中子份额：直接出现在点动力学方程
            "h_gap":       0.0,   # 燃料-包壳间隙传热系数：对该数据集输出无直接一阶作用
            "gamma_frac":  0.0,   # γ加热份额：对该数据集输出无直接一阶作用
        },
    ),
    DatasetSpec(
        name="powery",
        input_file="crx.csv",
        output_file="powery.csv",
        input_columns=["CR1", "CR2", "CR3", "CR4", "CR5", "CR6"],
        output_columns=[
            "A-2", "B-1", "B-2", "B-4", "B-5", "B-7", "B-8",
            "C-1", "C-2", "C-3", "C-4", "C-5", "C-6", "C-7", "C-8",
            "C-9", "C-10", "C-11", "C-12", "C-13", "C-14", "C-15",
        ],
        # md 表中 Powery 的 CR1~CR6 均评为 0.5（有明确的空间功率机制，但局部效应需仿真推断）
        physical_scores=_score(["CR1", "CR2", "CR3", "CR4", "CR5", "CR6"], 0.5),
    ),
    DatasetSpec(
        name="htgr",
        input_file="htgr.csv",
        output_file=None,
        input_columns=["theta1", "theta2", "theta3", "theta4", "theta5", "theta6", "theta7", "theta8"],
        output_columns=["fluxQ1", "fluxQ2", "fluxQ3", "fluxQ4"],
        id_columns=["index"],
        # md 最后说"heat/microreactor/htgr 数据集输入变量 P 全为 1"→ 全部改为 1.0
        physical_scores=_score(
            ["theta1", "theta2", "theta3", "theta4", "theta5", "theta6", "theta7", "theta8"], 1.0
        ),
    ),
    DatasetSpec(
        name="microreactor",
        input_file="microreactor.csv",
        output_file=None,
        input_columns=["theta1", "theta2", "theta3", "theta4", "theta5", "theta6", "theta7", "theta8"],
        output_columns=["fluxQ1", "fluxQ2", "fluxQ3", "fluxQ4"],
        id_columns=["sample number"],
        # md 最后说"heat/microreactor/htgr 数据集输入变量 P 全为 1"→ 全部改为 1.0
        physical_scores=_score(
            ["theta1", "theta2", "theta3", "theta4", "theta5", "theta6", "theta7", "theta8"], 1.0
        ),
    ),
]


def load_dataset(spec: DatasetSpec, data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load X and y for one dataset spec."""
    input_path = data_dir / spec.input_file
    x_source = pd.read_csv(input_path)

    if spec.output_file is None:
        y_source = x_source
    else:
        output_path = data_dir / spec.output_file
        y_source = pd.read_csv(output_path)
        if len(x_source) != len(y_source):
            raise ValueError(
                f"{spec.name}: input rows ({len(x_source)}) != output rows ({len(y_source)})"
            )

    missing_x = [col for col in spec.input_columns if col not in x_source.columns]
    missing_y = [col for col in spec.output_columns if col not in y_source.columns]
    if missing_x or missing_y:
        raise KeyError(f"{spec.name}: missing input columns {missing_x}, missing output columns {missing_y}")

    x = x_source[spec.input_columns].copy()
    y = y_source[spec.output_columns].copy()
    return x, y
