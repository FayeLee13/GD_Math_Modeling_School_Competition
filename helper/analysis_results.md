# B题项目完成度评估报告

> 评估时间：2026-06-17 | 评估人：Antigravity

---

## 题目要求速览（来自 B题.md）

| 任务 | 核心要求 |
|------|---------|
| **问题1** | 分析各输入特征与输出变量关系；识别冗余特征或非线性关系；提出特征选择或降维策略 |
| **问题2** | 在问题1特征基础上划分训练测试集；设计模型实现预测；评价不同数据集上的性能；探讨数据规模、输出维度等对模型能力的影响 |
| **问题3** | 结合核能系统特点，进行事前/事中/事后可解释性分析；分析模型是否能反映物理合理关系 |
| **提交物** | 建模论文 + 完整代码 + 数据集 + 图表结果 |

---

## 问题1：特征分析与预处理

### ✅ 已完成内容

| 子任务 | 实现方式 | 文件 |
|--------|---------|------|
| 描述性统计与数据质量诊断 | `describe_data_quality()` 函数，含均值/标准差/异常值/缺失值 | `src/problem1_analysis.py` |
| Pearson + Spearman 双重相关分析 | `_input_output_corr()` 含两种方法 | `src/problem1_analysis.py` |
| 随机森林非线性重要性 | `_random_forest_importance()` 300棵树 | `src/problem1_analysis.py` |
| 冗余特征识别 | `_redundancy_summary()` 输入间绝对相关系数 | `src/problem1_analysis.py` |
| 综合得分 DP-FSM | `S = 0.3C + 0.3N + 0.3P - 0.1R` | `src/problem1_analysis.py` |
| 物理合理性评分 | 所有数据集手动标注物理评分 | `src/dataset_config.py` |
| 分级特征选择策略 | core/candidate/low_priority 三级 | `src/problem1_analysis.py` |
| 覆盖全部9个数据集 | chf/heat/xs/bwr/fp/rea/powery/htgr/microreactor | `src/dataset_config.py` |
| 图表输出 | 27张图（特征分数图/冗余热力图/输入-输出相关热力图） | `reports/problem1/figures/` |
| 表格输出 | 25个CSV（特征得分/描述统计/冗余对/物理评分等） | `reports/problem1/tables/` |
| Markdown报告 | 自动生成汇总报告 | `reports/problem1/problem1_summary.md` |

### ⚠️ 潜在问题与风险

| 编号 | 问题 | 影响程度 | 建议 |
|------|------|---------|------|
| P1-1 | **bwr 数据集特征选择过于激进**：仅 CRD 被选为核心特征（得分0.842），其他8个特征均低于0.45（低优先级），导致 selected 模型 R² 从 0.966 降至 0.942 | 中 | 在论文中解释 CRD 的绝对主导性，并保留 subcool/flow_rate 等作候选特征 |
| P1-2 | **heat 数据集仅选1个特征**（qprime），其他6个特征均为低优先级，但 Tin 在代码中几乎无变化（std极小），属于近常数变量 | 中 | 描述 Tin 方差极小问题，说明信息量不足是物理设计原因 |
| P1-3 | **非线性关系识别标志**：代码有 `possible_nonlinear_relation` 列，但对 htgr/microreactor 几乎所有特征都标记为 True，解释力度不够 | 低 | 在论文中补充解释：鼓角度与通量的关系本质是周期性三角函数，天然非线性 |
| P1-4 | **xs 数据集高冗余**：Scatter12 与 Scatter11 相关系数 0.913，bwr 中 vanA/vanB 和 PSZ/DOM 相关系数均为 1.0（完全共线） | 中 | 这些已在报告中记录；论文中应当讨论完全共线的物理原因（BWR 对称约束） |

---

## 问题2：模型构建与精度评估

### ✅ 已完成内容

| 子任务 | 实现方式 | 文件 |
|--------|---------|------|
| 训练测试集划分 | 80/20，固定随机种子42 | `src/problem2_modeling.py` |
| 4个候选模型 | Ridge/KNN/RandomForest/GradientBoosting | `src/problem2_modeling.py` |
| 单输出/多输出统一框架 | MultiOutputRegressor 封装梯度提升 | `src/problem2_modeling.py` |
| 归一化指标 | NMAE/NRMSE 解决量纲不同问题 | `src/problem2_modeling.py` |
| 加权综合排名 | `Score = 0.4·R²排名 + 0.35·NRMSE排名 + 0.25·NMAE排名` | `src/problem2_modeling.py` |
| 全特征 vs 筛选特征对比 | `feature_set_comparison()` 验证问题1策略 | `src/problem2_modeling.py` |
| 多输出稳定性指标 | R² 标准差 + NRMSE 标准差 | `src/problem2_modeling.py` |
| 数据规模/维度影响分析 | `dataset_factor_table()` | `scripts/run_problem2_modeling.py` |
| 图表输出 | 20张图（模型对比/特征筛选效果/数据集难度） | `reports/problem2/figures/` |
| Markdown报告 | 含最佳模型/逐输出分析/全筛对比 | `reports/problem2/problem2_summary.md` |

### ✅ 各数据集最佳模型表现（全特征）

| 数据集 | 最佳模型 | 平均R² | 平均NRMSE | 评价 |
|--------|---------|-------|---------|------|
| xs | Ridge | **0.9999** | 0.0014 | 近完美，线性关系主导 |
| rea | GradientBoosting | **0.9927** | 0.0098 | 优秀 |
| heat | GradientBoosting | **0.9975** | 0.0112 | 优秀 |
| powery | Ridge | **0.9953** | 0.0131 | 优秀（22输出） |
| fp | Ridge | **0.9775** | 0.0178 | 良好 |
| chf | RandomForest | **0.9556** | 0.0249 | 良好 |
| bwr | GradientBoosting | **0.9663** | 0.0403 | 良好 |
| htgr | GradientBoosting | **0.9030** | 0.0519 | 可接受 |
| microreactor | GradientBoosting | **0.6581** | 0.1033 | 较差，需重点讨论 |

### ⚠️ 潜在问题与风险

| 编号 | 问题 | 影响程度 | 建议 |
|------|------|---------|------|
| P2-1 | **microreactor 精度偏低（R²=0.658）**：MAE/RMSE 数值异常大（10¹⁷量级），说明数据尺度极大或存在数值问题 | **高** | 检查 microreactor.csv 中通量值的量级是否正确；若是设计因素则需在论文中解释物理背景（通量绝对值）|
| P2-2 | **fp 特征筛选效果差**：selected（3特征）R² 从 0.9775 降至 0.7362，判定为 `too_aggressive` | 高 | 论文中应给出修正建议：放宽阈值到 S≥0.3 保留更多特征，或维持全特征建模 |
| P2-3 | **heat 特征筛选效果差**：selected（1特征 qprime）R² 从 0.9975 降至 0.9063 | 中 | 说明热传导问题中多个参数协同作用，单特征不足以刻画全貌，建议保留全特征 |
| P2-4 | **GradientBoosting 对多输出需要 MultiOutputRegressor 封装**，与其他模型实现不完全对等 | 低 | 在论文中说明实现细节，强调这是 sklearn 框架约束 |

---

## 问题3：模型可解释性分析

### ✅ 已完成内容

| 子任务 | 实现方式 | 文件 |
|--------|---------|------|
| **事前解释**：变量物理含义文档 | `FEATURE_MEANINGS` + `TARGET_MEANINGS` 字典 | `src/variable_metadata.py` |
| **事前解释**：物理预期方向配置 | `PHYSICAL_EXPECTED_DIRECTIONS`（chf/heat/xs/rea 4个数据集） | `src/variable_metadata.py` |
| **事中解释**：排列重要性 | `permutation_importance()` sklearn，6次重复 | `src/problem3_explainability.py` |
| **事后解释**：±10% 敏感性扰动 | `sensitivity_analysis()` 关键变量响应方向验证 | `src/problem3_explainability.py` |
| **事后解释**：部分依赖图 | `partial_dependence_response()` 15格网格点 | `src/problem3_explainability.py` |
| 物理一致性评级 | high/medium/low 三级，含判断闭环 | `src/problem3_explainability.py` |
| 图表输出 | 36张图（排列重要性/敏感性热力图/偏依赖图） | `reports/problem3/figures/` |
| Markdown报告 | 含一致性总表/排列重要性/扰动结果 | `reports/problem3/problem3_summary.md` |

### ✅ 物理一致性评级汇总

| 数据集 | 一致性等级 | Top3关键特征 | 已知方向一致率 |
|--------|---------|------------|--------------|
| chf | **High** | L(m), Xe(-), G | 100% |
| xs | **High** | FissionThermal, CaptureFast, Scatter12 | 100% |
| rea | **High** | rod_worth, beta, h_gap | 100% |
| heat | **High** | qprime, k, L | 66.7% |
| bwr | Medium | CRD, vanA, vanB | 未配置 |
| fp | Medium | ax_pow, clad_T, pellet_h | 未配置 |
| powery | Medium | CR6, CR2, CR5 | 未配置 |
| htgr | Medium | theta5, theta8, theta1 | 未配置 |
| microreactor | Medium | theta4, theta6, theta1 | 未配置 |

### ⚠️ 潜在问题与风险

| 编号 | 问题 | 影响程度 | 建议 |
|------|------|---------|------|
| P3-1 | **heat/k 物理方向不一致**：导热系数 k 增加时，模型预测温度 T 也增加（方向=+1），但物理上导热系数增加应使温度**降低**（正确方向=-1）。一致性判断为 False | **高** | 论文中须专门讨论：这可能是因为训练数据中 k 与 qprime 存在正相关，模型混淆了统计相关与因果关系。这本身就是"黑箱问题"的典型体现，可作为论文亮点 |
| P3-2 | **5个数据集的物理方向预期未配置**（bwr/fp/powery/htgr/microreactor），导致方向一致性无法定量评估 | 中 | 补充这些数据集的物理方向预期；或在论文中说明：theta/CR 类控制参数与通量的关系是对称性决定的，难以简单给出单调方向 |
| P3-3 | **SHAP 未实现**（文档标注为"选做加分项"） | 低 | 若时间允许可补充；否则在论文中说明已用排列重要性替代 |
| P3-4 | **Ridge 模型解释**：对于 xs/fp/powery 数据集使用 Ridge 作为最优模型，但代码中未提取标准化系数作为额外解释证据 | 低 | 在论文中补充 Ridge 系数分析，增强事中解释深度 |

---

## 提交物完整度评估

| 提交要求 | 现状 | 状态 |
|---------|------|------|
| **建模论文** | 有3个 docx 分问题摘要文件，但**无完整的建模论文（问题重述/数据预处理/模型建立/结果分析/可解释性讨论）** | ❌ **缺失** |
| **代码（完整）** | src/ + scripts/ 覆盖全流程，可一键运行 `python scripts/run_all.py` | ✅ 完整 |
| **数据集** | datasets/ 含全部13个数据文件，覆盖9个数据集 | ✅ 完整 |
| **结果图表** | 83张图表（问题1: 27张，问题2: 20张，问题3: 36张） | ✅ 完整 |
| **使用说明** | README.md 存在但未详细查看 | ⚠️ 需确认 |

---

## 总体评分与优先建议

### 综合评分
```
问题1（特征分析）：  90/100  ✅ 框架完整，结果可靠
问题2（模型建模）：  88/100  ✅ 精度良好，需补充 microreactor 异常讨论
问题3（可解释性）：  82/100  ⚠️ heat/k 方向异常是重要讨论点
提交物完整度：       60/100  ❌ 缺少完整建模论文
```

### 🔴 最高优先级（必须完成）
1. **撰写完整建模论文**：包含问题重述、数学模型描述（含公式）、结果分析与讨论、可解释性闭环

### 🟡 次要优先级（显著提升质量）
2. **专题讨论 heat/k 物理方向异常**：这是"黑箱问题"的绝佳案例，写好了是加分项
3. **补充 microreactor 数值异常分析**：解释 10¹⁷ 量级的 MAE/RMSE 来源
4. **对 fp/heat 特征筛选过激问题给出修正建议**：在论文中说明阈值敏感性

### 🟢 可选增强（加分项）
5. 补充 bwr/fp/powery 等数据集的物理方向预期并重新运行验证
6. 为 Ridge 最优模型补充标准化系数可视化
7. 完善 README.md 使用说明
