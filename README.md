# GD 数学建模校赛 — B题：核反应堆代理模型特征分析与可解释性研究

本仓库包含B题的**可复现代码、数据集和分析报告**，覆盖问题1（特征筛选）、问题2（模型训练）、问题3（可解释性）三个完整工作流。

---

## 目录

- [环境配置](#环境配置)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [问题1：特征分析与预处理](#问题1特征分析与预处理)
- [问题2：模型构建与精度评估](#问题2模型构建与精度评估)
- [问题3：模型可解释性分析](#问题3模型可解释性分析)
- [图表生成](#图表生成)
- [物理评分说明](#物理评分说明)
- [输出文件总览](#输出文件总览)

---

## 环境配置

推荐使用已有的 Conda 环境 `pytorch_gpu`：

```powershell
conda activate pytorch_gpu
```

如需从头安装依赖：

```powershell
pip install -r requirements.txt
```

**所有脚本均需在仓库根目录下执行。**

---

## 快速开始

### 一键运行全部流程（推荐）

```powershell
# Step 1: 依次运行问题1→2→3的全部分析与训练
python scripts/run_all.py

# Step 2: 按照《标准化指标与图表.md》规范生成108张标准图表
python scripts/run_charts.py
```

运行完成后，所有结果（表格、Markdown报告、图表）将保存在 `reports/` 目录下。

### 单独运行各问题

```powershell
# 问题1：特征分析与预处理（DP-FSM方法）
python scripts/run_problem1_analysis.py

# 问题2：模型训练与精度评估（MCAS-PM方法）
python scripts/run_problem2_modeling.py

# 问题3：可解释性分析（TPCI-EM方法）
python scripts/run_problem3_explainability.py --n-repeats 6 --n-jobs 2

# 图表生成（依赖前三个的输出，须最后运行）
python scripts/run_charts.py
```

### 可选参数

| 脚本 | 参数 | 默认值 | 说明 |
|---|---|---|---|
| `run_problem1_analysis.py` | `--data-dir` | `datasets` | 原始数据目录 |
| | `--out-dir` | `reports/problem1` | 输出目录 |
| | `--random-state` | `42` | 随机种子 |
| `run_problem2_modeling.py` | `--test-size` | `0.2` | 测试集比例 |
| | `--problem1-dir` | `reports/problem1` | 读取问题1筛选结果 |
| `run_problem3_explainability.py` | `--n-repeats` | `6` | 排列重要性重复次数 |
| | `--n-jobs` | `2` | 并行进程数 |
| | `--top-features` | `3` | PDP 取前N个特征 |
| `run_charts.py` | `--out-dir` | `reports/charts` | 图表输出目录 |

---

## 项目结构

```
GD_Math_Modeling_School_Competition/
│
├── datasets/                    # 原始数据集（CSV格式）
│   ├── chf.csv                  # 临界热流密度数据集
│   ├── heat.csv                 # 热传导数据集
│   ├── xs.csv                   # 截面数据集
│   ├── bwr_input.csv / bwr_output.csv
│   ├── fp_inp.csv / fp_out.csv
│   ├── rea_inputs.csv / rea_outputs.csv
│   ├── crx.csv / powery.csv
│   ├── htgr.csv
│   └── microreactor.csv
│
├── src/                         # 核心计算模块
│   ├── dataset_config.py        # 数据集定义 + 逐变量物理评分
│   ├── problem1_analysis.py     # DP-FSM特征筛选逻辑
│   ├── problem2_modeling.py     # 模型训练与评估逻辑
│   ├── problem3_explainability.py # 排列重要性/敏感性/PDP逻辑
│   └── variable_metadata.py    # 变量物理含义与方向预期
│
├── scripts/                     # 可执行脚本
│   ├── run_all.py               # 一键运行问题1→2→3
│   ├── run_problem1_analysis.py
│   ├── run_problem2_modeling.py
│   ├── run_problem3_explainability.py
│   └── run_charts.py            # 生成所有标准图表（108张）
│
├── reports/                     # 所有输出结果
│   ├── problem1/
│   │   ├── problem1_summary.md  # 自动生成的Markdown报告
│   │   ├── tables/              # CSV数据表
│   │   └── figures/             # 旧版图（3张/数据集）
│   ├── problem2/
│   │   ├── problem2_summary.md
│   │   ├── tables/
│   │   └── figures/
│   ├── problem3/
│   │   ├── problem3_summary.md
│   │   ├── tables/
│   │   └── figures/
│   └── charts/                  # ★ 新版标准图表（108张）
│       ├── CHARTS_CONCLUSIONS.md  # 图表阅读指南与综合结论
│       ├── problem1/<dataset>/  # 每数据集4张问题1图
│       ├── problem2/<dataset>/  # 每数据集4张问题2图
│       └── problem3/<dataset>/  # 每数据集4张问题3图
│
├── docs/                        # 文档
├── integrated_scores_mode_kept_utf8.md  # 物理评分参照表（源文件）
├── 标准化指标与图表.md            # 图表规范文档（源文件）
├── B题.md                       # 题目原文
└── requirements.txt
```

---

## 问题1：特征分析与预处理

### 方法：DP-FSM（Data-Physics Feature Scoring Method）

综合得分公式：

```
S = 0.3C + 0.3N + 0.3P - 0.1R
```

| 符号 | 含义 | 计算方式 |
|---|---|---|
| **C** | 相关强度 | Pearson 与 Spearman 平均绝对相关系数 |
| **N** | 非线性重要性 | 随机森林特征重要性（按数据集内最大值归一化） |
| **P** | 物理合理性 | 来自 `integrated_scores_mode_kept_utf8.md` 的**逐变量**评分（0/0.5/1.0） |
| **R** | 冗余惩罚 | 输入变量间平均绝对 Pearson 相关系数 |

**特征分级规则：**
- `S ≥ 0.65` → **核心特征**（Core，蓝色）
- `0.45 ≤ S < 0.65` → **候选特征**（Candidate，橙色）
- `S < 0.45` → **低优先级特征**（Low priority，灰色）

### 主要输出

```
reports/problem1/
├── problem1_summary.md              # 完整报告
├── tables/feature_scores_all.csv    # 全部特征DP-FSM得分
├── tables/selected_features_by_dataset.csv  # 推荐特征集
└── tables/physical_score_rationale.csv      # 物理评分依据
```

---

## 问题2：模型构建与精度评估

### 方法：MCAS-PM（Multi-Candidate Automated Selection with Physical-score-weighted Metrics）

**候选模型：** Ridge、KNN、随机森林（RF）、梯度提升树（GBT）

**评估指标：** R²、MAE、RMSE、NMAE、NRMSE

**模型综合排名公式：**
```
Score = 0.4×R²排名 + 0.35×NRMSE排名 + 0.25×NMAE排名  （分数越小越优）
```

同时对**全特征集**和**问题1筛选特征集**分别训练，便于对比特征筛选效果。

### 各数据集最佳全特征模型

| 数据集 | 最佳模型 | Mean R² | Mean NRMSE |
|---|---|---|---|
| xs | Ridge | **0.9999** | 0.0014 |
| rea | GradientBoosting | 0.9927 | 0.0098 |
| heat | GradientBoosting | 0.9975 | 0.0112 |
| powery | Ridge | 0.9953 | 0.0131 |
| fp | Ridge | 0.9775 | 0.0178 |
| chf | RandomForest | 0.9556 | 0.0249 |
| bwr | GradientBoosting | 0.9663 | 0.0403 |
| htgr | GradientBoosting | 0.9030 | 0.0519 |
| microreactor | GradientBoosting | 0.6581 | 0.1033 |

### 主要输出

```
reports/problem2/
├── problem2_summary.md
├── tables/model_metrics_all.csv
├── tables/best_models_by_dataset.csv
└── tables/feature_set_comparison.csv
```

---

## 问题3：模型可解释性分析

### 方法：TPCI-EM（Three-Phase Consistency Interpretability with Evidence Mapping）

三阶段解释框架：

1. **事前（Pre-hoc）：** 物理变量含义 + 物理评分（来自问题1）
2. **事中（In-hoc）：** 排列重要性（Permutation Importance）— 识别模型实际依赖变量
3. **事后（Post-hoc）：** ±10% 敏感性扰动 + 部分依赖图（PDP）

**物理一致性判断规则：**

| 条件 | 等级 |
|---|---|
| 顶部物理评分 ≥ 0.8 + 正重要性比例 ≥ 67% + 方向一致性 ≥ 60% | **High** |
| 顶部物理评分 ≥ 0.6 或 正重要性比例 ≥ 50% | **Medium** |
| 其他 | **Low** |

### 主要输出

```
reports/problem3/
├── problem3_summary.md
├── tables/permutation_importance_all.csv
├── tables/sensitivity_analysis_all.csv
└── tables/physical_consistency_summary.csv
```

---

## 图表生成

`run_charts.py` 按《标准化指标与图表.md》规范，为9个数据集各生成12张图表，共 **108张PNG**，保存在 `reports/charts/`。

**图表目录结构：**
```
reports/charts/
├── CHARTS_CONCLUSIONS.md          # ★ 图表阅读指南 + 综合结论
├── problem1/<dataset>/
│   ├── <ds>_p1_correlation.png         # 输入-输出相关性图
│   ├── <ds>_p1_rf_importance.png       # RF非线性重要性条形图
│   ├── <ds>_p1_redundancy_heatmap.png  # 输入变量冗余热力图
│   └── <ds>_p1_score_ranking.png       # 综合得分排序图（三色）
├── problem2/<dataset>/
│   ├── <ds>_p2_accuracy_table.png      # 模型精度对比表
│   ├── <ds>_p2_three_metrics.png       # 三指标分面柱状图
│   ├── <ds>_p2_parity.png              # 真实值-预测值散点图
│   └── <ds>_p2_feature_comparison.png  # 全特征vs筛选特征对比
└── problem3/<dataset>/
    ├── <ds>_p3_permutation_importance.png  # 排列重要性水平条形图
    ├── <ds>_p3_sensitivity.png              # ±10%敏感性扰动热力图
    ├── <ds>_p3_pdp.png                     # 部分依赖图（PDP）
    └── <ds>_p3_consistency_table.png       # 物理一致性评价表
```

> 📊 **详细的图表阅读指南与综合结论**请查阅 [`reports/charts/CHARTS_CONCLUSIONS.md`](reports/charts/CHARTS_CONCLUSIONS.md)

---

## 物理评分说明

物理评分 P 来自 [`integrated_scores_mode_kept_utf8.md`](integrated_scores_mode_kept_utf8.md)，已更新为**逐变量细化评分**（非数据集统一值）：

| 评分 | 含义 |
|---|---|
| **1.0** | 存在明确物理方程或可靠文献支持，作用方向合理 |
| **0.5** | 存在间接或条件性物理联系，证据不完整 |
| **0.0** | 未找到足够直接的合理机理 |

典型变化：
- **REA**：`rod_worth/beta` 改为 1.0；`h_gap/gamma_frac` 改为 0.0
- **FP**：`pellet_OD/pellet_h/enrich/pressure` 改为 0.0
- **CHF**：`P(kPa)/G/Tin/Xe` 改为 1.0
- **XS**：`Scatter11/21/22` 改为 0.5

---

## 输出文件总览

| 路径 | 内容 |
|---|---|
| `reports/problem1/problem1_summary.md` | 问题1完整报告（含推荐特征、数据质量、物理评分） |
| `reports/problem2/problem2_summary.md` | 问题2完整报告（含最佳模型、特征筛选对比） |
| `reports/problem3/problem3_summary.md` | 问题3完整报告（含排列重要性、物理一致性） |
| `reports/charts/CHARTS_CONCLUSIONS.md` | **图表阅读指南 + 综合分析结论** |
| `reports/charts/problem{1,2,3}/<ds>/*.png` | 108张标准图表 |
| `reports/problem*/tables/*.csv` | 所有数值结果CSV表 |

---

> 项目架构详情见 [`docs/project_architecture.md`](docs/project_architecture.md)
