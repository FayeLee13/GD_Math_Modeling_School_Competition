# B题问题1：特征分析与预处理结果

本报告由 `scripts/run_problem1_analysis.py` 自动生成，对所有数据集执行 DP-FSM 特征筛选流程。

## 方法说明

综合得分采用：`S = 0.3C + 0.3N + 0.3P - 0.1R`。

- `C`：Pearson 与 Spearman 平均绝对相关强度。
- `N`：随机森林非线性特征重要性，并按数据集内最大值归一化。
- `P`：基于题面机理的物理合理性评分。
- `R`：输入变量间平均绝对相关系数，作为冗余惩罚。

特征分级规则：`S >= 0.65` 为核心特征，`0.45 <= S < 0.65` 为候选特征，`S < 0.45` 为低优先级特征。

## 数据质量概况

| dataset      | variables | total_missing | zero_std_count |
| ------------ | --------- | ------------- | -------------- |
| bwr          | 14        | 0             | 0              |
| chf          | 7         | 0             | 0              |
| fp           | 17        | 0             | 0              |
| heat         | 8         | 0             | 0              |
| htgr         | 12        | 0             | 0              |
| microreactor | 12        | 0             | 0              |
| powery       | 28        | 0             | 0              |
| rea          | 8         | 0             | 0              |
| xs           | 9         | 0             | 0              |

## 各数据集推荐特征

| dataset      | selected_features                                              |
| ------------ | -------------------------------------------------------------- |
| bwr          | CRD                                                            |
| chf          | L (m), Xe (-), G (kg m-2s-1), P (kPa)                          |
| fp           | ax_pow, clad_T, porosity                                       |
| heat         | qprime                                                         |
| htgr         | theta1, theta8, theta5, theta4, theta2, theta3, theta7, theta6 |
| microreactor | theta6, theta4, theta7, theta3, theta1, theta5, theta2, theta8 |
| powery       | CR4, CR3, CR2, CR5, CR1, CR6                                   |
| rea          | rod_worth, beta                                                |
| xs           | FissionThermal, CaptureFast, FissionFast, CaptureThermal       |

## 各数据集 Top 特征

| dataset      | rank   | feature        | dp_fsm_score | feature_level | correlation_strength | rf_importance_norm | redundancy_max_abs | possible_nonlinear_relation |
| ------------ | ------ | -------------- | ------------ | ------------- | -------------------- | ------------------ | ------------------ | --------------------------- |
| **bwr**     | **1** | **CRD**       | **0.842**   | **core**     | **0.8136**          | 1.0                | 0.042              | False                       |
| bwr          | 2      | power_density  | 0.3093       | low_priority  | 0.024                | 0.0176             | 0.053              | False                       |
| bwr          | 3      | subcool        | 0.308        | low_priority  | 0.017                | 0.0172             | 0.053              | False                       |
| bwr          | 4      | flow_rate      | 0.3069       | low_priority  | 0.0141               | 0.0161             | 0.0419             | False                       |
| bwr          | 5      | VFNGAP         | 0.3052       | low_priority  | 0.0067               | 0.0141             | 0.0166             | False                       |
| chf          | 1      | L (m)          | 0.7691       | core          | 0.6272               | 1.0                | 0.3289             | False                       |
| chf          | 2      | Xe (-)         | 0.6665       | core          | 0.5314               | 0.801              | 0.6186             | False                       |
| chf          | 3      | G (kg m-2s-1)  | 0.4956       | candidate     | 0.3904               | 0.3599             | 0.6186             | False                       |
| chf          | 4      | P (kPa)        | 0.4423       | low_priority  | 0.2663               | 0.3218             | 0.6043             | False                       |
| chf          | 5      | Tin (C)        | 0.4349       | low_priority  | 0.3149               | 0.2407             | 0.6043             | False                       |
| fp           | 1      | ax_pow         | 0.76         | core          | 0.5445               | 1.0                | 0.0854             | False                       |
| fp           | 2      | clad_T         | 0.5199       | candidate     | 0.4242               | 0.3261             | 0.1432             | False                       |
| fp           | 3      | porosity       | 0.5091       | candidate     | 0.2236               | 0.4841             | 0.0789             | False                       |
| fp           | 4      | pellet_h       | 0.4073       | low_priority  | 0.2922               | 0.0802             | 0.0914             | False                       |
| fp           | 5      | inlet_T        | 0.3421       | low_priority  | 0.0787               | 0.0751             | 0.1126             | False                       |
| heat         | 1      | qprime         | 0.8593       | core          | 0.8729               | 1.0                | 0.074              | False                       |
| heat         | 2      | k              | 0.4319       | low_priority  | 0.3445               | 0.1009             | 0.0352             | False                       |
| heat         | 3      | L              | 0.329        | low_priority  | 0.0767               | 0.0278             | 0.033              | False                       |
| heat         | 4      | mdot           | 0.3252       | low_priority  | 0.0666               | 0.0221             | 0.0323             | False                       |
| heat         | 5      | Tin            | 0.3212       | low_priority  | 0.0619               | 0.0191             | 0.074              | False                       |
| htgr         | 1      | theta1         | 0.6063       | candidate     | 0.03                 | 1.0                | 0.0468             | True                        |
| htgr         | 2      | theta8         | 0.6017       | candidate     | 0.03                 | 0.9846             | 0.0468             | True                        |
| htgr         | 3      | theta5         | 0.6017       | candidate     | 0.03                 | 0.9845             | 0.0468             | True                        |
| htgr         | 4      | theta4         | 0.5988       | candidate     | 0.03                 | 0.9748             | 0.0468             | True                        |
| htgr         | 5      | theta2         | 0.5475       | candidate     | 0.0138               | 0.8205             | 0.0468             | True                        |
| microreactor | 1      | theta6         | 0.6582       | core          | 0.2002               | 1.0                | 0.0376             | True                        |
| microreactor | 2      | theta4         | 0.6193       | candidate     | 0.1227               | 0.9482             | 0.0574             | True                        |
| microreactor | 3      | theta7         | 0.5999       | candidate     | 0.1821               | 0.8267             | 0.0705             | True                        |
| microreactor | 4      | theta3         | 0.5919       | candidate     | 0.1494               | 0.8345             | 0.0894             | True                        |
| microreactor | 5      | theta1         | 0.5616       | candidate     | 0.1148               | 0.7671             | 0.0703             | True                        |
| powery       | 1      | CR4            | 0.6966       | core          | 0.3319               | 1.0                | 0.0662             | False                       |
| powery       | 2      | CR3            | 0.6898       | core          | 0.3413               | 0.9669             | 0.053              | False                       |
| powery       | 3      | CR2            | 0.6854       | core          | 0.3323               | 0.9628             | 0.0662             | False                       |
| powery       | 4      | CR5            | 0.6476       | candidate     | 0.3219               | 0.8431             | 0.0468             | False                       |
| powery       | 5      | CR1            | 0.6449       | candidate     | 0.3161               | 0.8423             | 0.053              | False                       |
| rea          | 1      | rod_worth      | 0.8198       | core          | 0.7364               | 1.0                | 0.014              | False                       |
| rea          | 2      | beta           | 0.7286       | core          | 0.5846               | 0.8459             | 0.0127             | False                       |
| rea          | 3      | h_gap          | 0.324        | low_priority  | 0.0601               | 0.0247             | 0.0332             | False                       |
| rea          | 4      | gamma_frac     | 0.3125       | low_priority  | 0.0182               | 0.0288             | 0.0332             | False                       |
| xs           | 1      | FissionThermal | 0.7922       | core          | 0.6783               | 1.0                | 0.2321             | False                       |
| xs           | 2      | CaptureFast    | 0.5705       | candidate     | 0.5375               | 0.4894             | 0.7651             | False                       |
| xs           | 3      | FissionFast    | 0.5645       | candidate     | 0.5565               | 0.4264             | 0.6708             | False                       |
| xs           | 4      | CaptureThermal | 0.4638       | candidate     | 0.3054               | 0.2838             | 0.3371             | False                       |
| xs           | 5      | Scatter11      | 0.3719       | low_priority  | 0.2731               | 0.12               | 0.9127             | False                       |

## 高冗余特征对

| dataset | feature_a | feature_b | abs_pearson_corr |
| ------- | --------- | --------- | ---------------- |
| xs      | Scatter12 | Scatter11 | 0.9127           |
| bwr     | vanA      | vanB      | 1.0              |
| bwr     | PSZ       | DOM       | 1.0              |

## 输出文件

- `tables/feature_scores_all.csv`：全部数据集特征综合得分。
- `tables/input_output_correlations_all.csv`：输入-输出 Pearson/Spearman 相关性长表。
- `tables/redundancy_pairs_all.csv`：输入变量间冗余关系。
- `tables/selected_features_by_dataset.csv`：按 DP-FSM 规则推荐的特征集。
- `figures/`：各数据集特征得分条形图、输入冗余热力图、输入-输出相关热力图。
