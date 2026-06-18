# B题问题1：特征分析与预处理结果

本报告由 `scripts/run_problem1_analysis.py` 自动生成，对所有数据集执行 DP-FSM 特征筛选流程。

## 方法说明

综合得分采用：`S = 0.3C + 0.3N + 0.3P - 0.1R`。

- `C`：Pearson 与 Spearman 平均绝对相关强度。
- `N`：随机森林非线性特征重要性，并按数据集内最大值归一化。
- `P`：来自物理合理性评分表的数据集级物理合理性评分，并赋给该数据集下所有输入特征。
- `R`：输入变量间平均绝对相关系数，作为冗余惩罚。

特征分级规则：`S >= 0.65` 为核心特征，`0.45 <= S < 0.65` 为候选特征，`S < 0.45` 为低优先级特征。

## 数据质量概况

| dataset | n_variables | n_input_features | total_missing | max_missing_rate | zero_std_variables | variables_with_iqr_outliers | max_iqr_outlier_rate | input_scale_range_ratio | standardization_recommended | missing_imputation_recommended | outlier_review_recommended |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chf | 7 | 6 | 0 | 0.0 | 0 | 5 | 0.052 | 1499238.3189 | True | False | True |
| heat | 8 | 7 | 0 | 0.0 | 0 | 6 | 0.007 | 8130051.3641 | True | False | False |
| xs | 9 | 8 | 0 | 0.0 | 0 | 8 | 0.012 | 567.6914 | True | False | False |
| bwr | 14 | 9 | 0 | 0.0 | 0 | 5 | 0.1375 | 256.7933 | True | False | True |
| fp | 17 | 13 | 0 | 0.0 | 0 | 15 | 0.015 | 4160869565217.391 | True | False | False |
| rea | 8 | 4 | 0 | 0.0 | 0 | 7 | 0.033 | 8790883.095 | True | False | False |
| powery | 28 | 6 | 0 | 0.0 | 0 | 4 | 0.005 | 1.0017 | False | False | False |
| htgr | 12 | 8 | 0 | 0.0 | 0 | 4 | 0.0047 | 1.0004 | False | False | False |
| microreactor | 12 | 8 | 0 | 0.0 | 0 | 3 | 0.0093 | 1.0051 | False | False | False |

## 描述性统计变量诊断示例

| dataset | role | variable | n_rows | missing_count | mean | std | min | q25 | median | q75 | max | skew | iqr_outlier_rate | zero_std | needs_standardization |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chf | input | D (m) | 2500 | 0 | 0.0089 | 0.0022 | 0.0022 | 0.0078 | 0.0083 | 0.0102 | 0.0162 | 0.3856 | 0.052 | False | True |
| chf | input | L (m) | 2500 | 0 | 2.6127 | 1.8507 | 0.2083 | 1.0238 | 2.0407 | 3.5617 | 15.6639 | 1.6719 | 0.0104 | False | True |
| chf | input | P (kPa) | 2500 | 0 | 9965.7529 | 5342.5665 | 98.1517 | 6657.8294 | 9971.7481 | 14257.3717 | 20987.0878 | -0.1386 | 0.0 | False | True |
| chf | input | G (kg m-2s-1) | 2500 | 0 | 1982.6244 | 1426.3857 | 26.8184 | 976.8746 | 1604.71 | 2725.833 | 7881.9149 | 1.0656 | 0.02 | False | True |
| chf | input | Tin (C) | 2500 | 0 | 198.1571 | 85.8654 | 10.8057 | 126.2616 | 212.1159 | 266.1872 | 377.068 | -0.2933 | 0.0 | False | True |
| heat | input | qprime | 1000 | 0 | 39998.4647 | 2004.4352 | 32126.9977 | 38652.4761 | 39999.2514 | 41348.8081 | 46573.9736 | -0.026 | 0.006 | False | True |
| heat | input | mdot | 1000 | 0 | 199.9944 | 10.0057 | 164.2583 | 193.2603 | 200.0007 | 206.7324 | 231.7316 | -0.0151 | 0.007 | False | True |
| heat | input | Tin | 1000 | 0 | 573.1525 | 0.0014 | 573.15 | 573.1513 | 573.1525 | 573.1537 | 573.155 | 0.0 | 0.0 | False | True |
| heat | input | R | 1000 | 0 | 0.005 | 0.0003 | 0.004 | 0.0048 | 0.005 | 0.0052 | 0.0058 | -0.0293 | 0.007 | False | True |
| heat | input | L | 1000 | 0 | 3.6599 | 0.1831 | 3.022 | 3.5365 | 3.6602 | 3.7832 | 4.2642 | -0.0057 | 0.006 | False | True |
| xs | input | FissionFast | 1000 | 0 | 0.0064 | 0.0001 | 0.0062 | 0.0064 | 0.0064 | 0.0065 | 0.0066 | -0.0677 | 0.005 | False | True |
| xs | input | CaptureFast | 1000 | 0 | 0.0094 | 0.0001 | 0.0091 | 0.0093 | 0.0094 | 0.0094 | 0.0096 | -0.0314 | 0.008 | False | True |
| xs | input | FissionThermal | 1000 | 0 | 0.13 | 0.0007 | 0.1279 | 0.1295 | 0.13 | 0.1305 | 0.1319 | -0.0401 | 0.006 | False | True |
| xs | input | CaptureThermal | 1000 | 0 | 0.081 | 0.0002 | 0.0805 | 0.0809 | 0.081 | 0.0812 | 0.0816 | -0.0602 | 0.0 | False | True |
| xs | input | Scatter12 | 1000 | 0 | 0.0154 | 0.0002 | 0.0147 | 0.0153 | 0.0154 | 0.0156 | 0.0161 | -0.1919 | 0.011 | False | True |
| bwr | input | PSZ | 2000 | 0 | 124.1184 | 8.9116 | 109.01 | 116.171 | 124.3845 | 131.805 | 139.4 | -0.0102 | 0.0 | False | True |
| bwr | input | DOM | 2000 | 0 | 212.5516 | 8.9116 | 197.27 | 204.865 | 212.2855 | 220.499 | 227.66 | 0.0102 | 0.0 | False | True |
| bwr | input | vanA | 2000 | 0 | 319.8346 | 21.9097 | 281.644 | 301.418 | 318.5835 | 338.397 | 358.682 | 0.0673 | 0.0 | False | True |
| bwr | input | vanB | 2000 | 0 | 351.7554 | 21.9097 | 312.908 | 333.193 | 353.0065 | 370.172 | 389.946 | -0.0673 | 0.0 | False | True |
| bwr | input | subcool | 2000 | 0 | 23.9953 | 1.4482 | 18.628 | 23.044 | 23.983 | 24.9748 | 28.775 | 0.0291 | 0.0095 | False | True |
| fp | input | fuel_dens | 400 | 0 | 10456.315 | 20.0988 | 10396.0 | 10443.0 | 10457.0 | 10470.0 | 10522.0 | 0.1427 | 0.0125 | False | True |
| fp | input | porosity | 400 | 0 | 0.0469 | 0.0072 | 0.0211 | 0.0421 | 0.0469 | 0.0514 | 0.0686 | 0.0482 | 0.0075 | False | True |
| fp | input | clad_thick | 400 | 0 | 0.0006 | 0.0 | 0.0006 | 0.0006 | 0.0006 | 0.0006 | 0.0006 | 0.0 | 0.0 | False | True |
| fp | input | pellet_OD | 400 | 0 | 0.0041 | 0.0 | 0.0041 | 0.0041 | 0.0041 | 0.0041 | 0.0041 | 0.0 | 0.01 | False | True |
| fp | input | pellet_h | 400 | 0 | 0.0138 | 0.0006 | 0.0121 | 0.0134 | 0.0138 | 0.0142 | 0.0157 | -0.0219 | 0.005 | False | True |
| rea | input | rod_worth | 2000 | 0 | 0.0087 | 0.0004 | 0.008 | 0.0084 | 0.0087 | 0.0091 | 0.0094 | 0.0345 | 0.0 | False | True |
| rea | input | beta | 2000 | 0 | 0.0076 | 0.0004 | 0.0065 | 0.0073 | 0.0076 | 0.0079 | 0.0088 | 0.0341 | 0.006 | False | True |
| rea | input | h_gap | 2000 | 0 | 9932.5857 | 1976.0063 | 4301.825 | 8596.942 | 9982.8281 | 11248.4067 | 16729.0556 | -0.0269 | 0.0045 | False | True |
| rea | input | gamma_frac | 2000 | 0 | 0.019 | 0.0038 | 0.0049 | 0.0165 | 0.019 | 0.0216 | 0.0312 | -0.0549 | 0.009 | False | True |
| rea | output | max_power | 2000 | 0 | 258.8202 | 208.7594 | 10.248 | 98.8205 | 199.085 | 362.37 | 1388.8 | 1.3399 | 0.026 | False | False |
| powery | input | CR1 | 1000 | 0 | 24.0024 | 2.3074 | 20.0157 | 22.0082 | 24.0023 | 25.9976 | 27.9889 | 0.0 | 0.0 | False | True |
| powery | input | CR2 | 1000 | 0 | 24.0022 | 2.3075 | 20.0157 | 22.0034 | 24.0019 | 25.9991 | 27.9906 | -0.0001 | 0.0 | False | True |
| powery | input | CR3 | 1000 | 0 | 24.0022 | 2.3073 | 20.0117 | 22.0053 | 24.0035 | 25.9946 | 27.9965 | 0.0001 | 0.0 | False | True |
| powery | input | CR4 | 1000 | 0 | 24.0023 | 2.3074 | 20.0152 | 22.0062 | 24.002 | 25.9981 | 27.9939 | -0.0001 | 0.0 | False | True |
| powery | input | CR5 | 1000 | 0 | 24.0022 | 2.3074 | 20.0142 | 22.0085 | 24.0022 | 25.9993 | 27.9923 | 0.0 | 0.0 | False | True |
| htgr | input | theta1 | 3004 | 0 | 3.1273 | 1.8131 | 0.0018 | 1.5813 | 3.1221 | 4.6905 | 6.2811 | 0.024 | 0.0 | False | True |
| htgr | input | theta2 | 3004 | 0 | 3.1256 | 1.8163 | 0.0005 | 1.568 | 3.0979 | 4.6828 | 6.2822 | 0.0108 | 0.0 | False | True |
| htgr | input | theta3 | 3004 | 0 | 3.1256 | 1.8163 | 0.0005 | 1.568 | 3.0979 | 4.6828 | 6.2822 | 0.0108 | 0.0 | False | True |
| htgr | input | theta4 | 3004 | 0 | 3.1273 | 1.8131 | 0.0018 | 1.5813 | 3.1221 | 4.6905 | 6.2811 | 0.024 | 0.0 | False | True |
| htgr | input | theta5 | 3004 | 0 | 3.1559 | 1.8131 | 0.0021 | 1.5927 | 3.1611 | 4.7019 | 6.2814 | -0.024 | 0.0 | False | True |
| microreactor | input | theta1 | 751 | 0 | 3.1513 | 1.799 | 0.0035 | 1.6289 | 3.2027 | 4.7029 | 6.2811 | -0.012 | 0.0 | False | True |
| microreactor | input | theta2 | 751 | 0 | 3.2547 | 1.8214 | 0.0063 | 1.6973 | 3.3591 | 4.8448 | 6.2831 | -0.0965 | 0.0 | False | True |
| microreactor | input | theta3 | 751 | 0 | 3.1193 | 1.8002 | 0.0058 | 1.4946 | 3.1581 | 4.6659 | 6.275 | -0.0004 | 0.0 | False | True |
| microreactor | input | theta4 | 751 | 0 | 3.2545 | 1.7804 | 0.005 | 1.8483 | 3.2089 | 4.8612 | 6.2827 | -0.0204 | 0.0 | False | True |
| microreactor | input | theta5 | 751 | 0 | 3.1417 | 1.8012 | 0.0056 | 1.6551 | 3.1264 | 4.6121 | 6.2626 | 0.0066 | 0.0 | False | True |

## 物理合理性评分依据示例

| dataset | feature | physical_meaning | physical_score | relevance_level | formula_type | score_basis | score_rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| chf | D (m) | flow channel hydraulic diameter | 0.5 | indirect_or_conditional_physics | Type III: empirical or engineering relation | P=0.5 because the variables have accepted thermal-hydraulic relevance, but the support is mainly empirical rather than a closed-form first-principles equation. | flow channel hydraulic diameter; P=0.5 because the variables have accepted thermal-hydraulic relevance, but the support is mainly empirical rather than a closed-form first-principles equation. |
| chf | L (m) | heated length of the channel | 0.5 | indirect_or_conditional_physics | Type III: empirical or engineering relation | P=0.5 because the variables have accepted thermal-hydraulic relevance, but the support is mainly empirical rather than a closed-form first-principles equation. | heated length of the channel; P=0.5 because the variables have accepted thermal-hydraulic relevance, but the support is mainly empirical rather than a closed-form first-principles equation. |
| chf | P (kPa) | system pressure | 1.0 | strong_formula_or_standard_model | Type III: empirical or engineering relation | P=0.5 because the variables have accepted thermal-hydraulic relevance, but the support is mainly empirical rather than a closed-form first-principles equation. | system pressure; P=0.5 because the variables have accepted thermal-hydraulic relevance, but the support is mainly empirical rather than a closed-form first-principles equation. |
| chf | G (kg m-2s-1) | mass flux | 1.0 | strong_formula_or_standard_model | Type III: empirical or engineering relation | P=0.5 because the variables have accepted thermal-hydraulic relevance, but the support is mainly empirical rather than a closed-form first-principles equation. | mass flux; P=0.5 because the variables have accepted thermal-hydraulic relevance, but the support is mainly empirical rather than a closed-form first-principles equation. |
| heat | qprime | linear heat generation rate | 1.0 | strong_formula_or_standard_model | Type I/II/III: governing equation, analytic relation, and engineering approximation | P=1.0 because the dataset variables are directly supported by standard heat-transfer equations and analytic temperature-rise relations. | linear heat generation rate; P=1.0 because the dataset variables are directly supported by standard heat-transfer equations and analytic temperature-rise relations. |
| heat | mdot | coolant mass flow rate | 1.0 | strong_formula_or_standard_model | Type I/II/III: governing equation, analytic relation, and engineering approximation | P=1.0 because the dataset variables are directly supported by standard heat-transfer equations and analytic temperature-rise relations. | coolant mass flow rate; P=1.0 because the dataset variables are directly supported by standard heat-transfer equations and analytic temperature-rise relations. |
| heat | Tin | inlet temperature | 1.0 | strong_formula_or_standard_model | Type I/II/III: governing equation, analytic relation, and engineering approximation | P=1.0 because the dataset variables are directly supported by standard heat-transfer equations and analytic temperature-rise relations. | inlet temperature; P=1.0 because the dataset variables are directly supported by standard heat-transfer equations and analytic temperature-rise relations. |
| heat | R | fuel or heat-source radius | 1.0 | strong_formula_or_standard_model | Type I/II/III: governing equation, analytic relation, and engineering approximation | P=1.0 because the dataset variables are directly supported by standard heat-transfer equations and analytic temperature-rise relations. | fuel or heat-source radius; P=1.0 because the dataset variables are directly supported by standard heat-transfer equations and analytic temperature-rise relations. |
| xs | FissionFast | fast-group fission cross section | 1.0 | strong_formula_or_standard_model | Type I/II: standard formula and approximate reactor-physics model | P=1.0 because neutron production and loss mechanisms are explicit and strongly tied to the input cross sections. | fast-group fission cross section; P=1.0 because neutron production and loss mechanisms are explicit and strongly tied to the input cross sections. |
| xs | CaptureFast | fast-group capture cross section | 1.0 | strong_formula_or_standard_model | Type I/II: standard formula and approximate reactor-physics model | P=1.0 because neutron production and loss mechanisms are explicit and strongly tied to the input cross sections. | fast-group capture cross section; P=1.0 because neutron production and loss mechanisms are explicit and strongly tied to the input cross sections. |
| xs | FissionThermal | thermal-group fission cross section | 1.0 | strong_formula_or_standard_model | Type I/II: standard formula and approximate reactor-physics model | P=1.0 because neutron production and loss mechanisms are explicit and strongly tied to the input cross sections. | thermal-group fission cross section; P=1.0 because neutron production and loss mechanisms are explicit and strongly tied to the input cross sections. |
| xs | CaptureThermal | thermal-group capture cross section | 1.0 | strong_formula_or_standard_model | Type I/II: standard formula and approximate reactor-physics model | P=1.0 because neutron production and loss mechanisms are explicit and strongly tied to the input cross sections. | thermal-group capture cross section; P=1.0 because neutron production and loss mechanisms are explicit and strongly tied to the input cross sections. |
| bwr | PSZ | BWR core operating or shape parameter from the problem data | 0.5 | indirect_or_conditional_physics | Type I/III: diffusion equation plus engineering peaking relations | P=0.5 because control and operating variables are physically meaningful, but their dataset-level effect is mediated by reactor-core simulation and engineering response factors. | BWR core operating or shape parameter from the problem data; P=0.5 because control and operating variables are physically meaningful, but their dataset-level effect is mediated by reactor-core simulation and engineering response factors. |
| bwr | DOM | BWR core operating or shape parameter from the problem data | 0.5 | indirect_or_conditional_physics | Type I/III: diffusion equation plus engineering peaking relations | P=0.5 because control and operating variables are physically meaningful, but their dataset-level effect is mediated by reactor-core simulation and engineering response factors. | BWR core operating or shape parameter from the problem data; P=0.5 because control and operating variables are physically meaningful, but their dataset-level effect is mediated by reactor-core simulation and engineering response factors. |
| bwr | vanA | BWR vaned-device or flow-distribution parameter A | 0.5 | indirect_or_conditional_physics | Type I/III: diffusion equation plus engineering peaking relations | P=0.5 because control and operating variables are physically meaningful, but their dataset-level effect is mediated by reactor-core simulation and engineering response factors. | BWR vaned-device or flow-distribution parameter A; P=0.5 because control and operating variables are physically meaningful, but their dataset-level effect is mediated by reactor-core simulation and engineering response factors. |
| bwr | vanB | BWR vaned-device or flow-distribution parameter B | 0.5 | indirect_or_conditional_physics | Type I/III: diffusion equation plus engineering peaking relations | P=0.5 because control and operating variables are physically meaningful, but their dataset-level effect is mediated by reactor-core simulation and engineering response factors. | BWR vaned-device or flow-distribution parameter B; P=0.5 because control and operating variables are physically meaningful, but their dataset-level effect is mediated by reactor-core simulation and engineering response factors. |
| fp | fuel_dens | fuel density | 0.5 | indirect_or_conditional_physics | Type I/II/III: standard model plus engineering approximations | P=0.5 because the physical mechanism is clear, but several relationships are engineering-model or approximate rather than direct closed-form effects for every variable. | fuel density; P=0.5 because the physical mechanism is clear, but several relationships are engineering-model or approximate rather than direct closed-form effects for every variable. |
| fp | porosity | fuel porosity | 1.0 | strong_formula_or_standard_model | Type I/II/III: standard model plus engineering approximations | P=0.5 because the physical mechanism is clear, but several relationships are engineering-model or approximate rather than direct closed-form effects for every variable. | fuel porosity; P=0.5 because the physical mechanism is clear, but several relationships are engineering-model or approximate rather than direct closed-form effects for every variable. |
| fp | clad_thick | cladding thickness | 1.0 | strong_formula_or_standard_model | Type I/II/III: standard model plus engineering approximations | P=0.5 because the physical mechanism is clear, but several relationships are engineering-model or approximate rather than direct closed-form effects for every variable. | cladding thickness; P=0.5 because the physical mechanism is clear, but several relationships are engineering-model or approximate rather than direct closed-form effects for every variable. |
| fp | pellet_OD | fuel pellet outer diameter | 0.0 | unsupported_or_contradictory | Type I/II/III: standard model plus engineering approximations | P=0.5 because the physical mechanism is clear, but several relationships are engineering-model or approximate rather than direct closed-form effects for every variable. | fuel pellet outer diameter; P=0.5 because the physical mechanism is clear, but several relationships are engineering-model or approximate rather than direct closed-form effects for every variable. |
| rea | rod_worth | reactivity worth of the control rod | 1.0 | strong_formula_or_standard_model | Type I/II: standard transient and heat-transfer equations | P=0.5 because the main variables have clear transient-physics meaning, but the dataset response is coupled and condition-dependent. | reactivity worth of the control rod; P=0.5 because the main variables have clear transient-physics meaning, but the dataset response is coupled and condition-dependent. |
| rea | beta | effective delayed neutron fraction | 1.0 | strong_formula_or_standard_model | Type I/II: standard transient and heat-transfer equations | P=0.5 because the main variables have clear transient-physics meaning, but the dataset response is coupled and condition-dependent. | effective delayed neutron fraction; P=0.5 because the main variables have clear transient-physics meaning, but the dataset response is coupled and condition-dependent. |
| rea | h_gap | fuel-cladding gap heat-transfer coefficient | 0.0 | unsupported_or_contradictory | Type I/II: standard transient and heat-transfer equations | P=0.5 because the main variables have clear transient-physics meaning, but the dataset response is coupled and condition-dependent. | fuel-cladding gap heat-transfer coefficient; P=0.5 because the main variables have clear transient-physics meaning, but the dataset response is coupled and condition-dependent. |
| rea | gamma_frac | gamma heating fraction | 0.0 | unsupported_or_contradictory | Type I/II: standard transient and heat-transfer equations | P=0.5 because the main variables have clear transient-physics meaning, but the dataset response is coupled and condition-dependent. | gamma heating fraction; P=0.5 because the main variables have clear transient-physics meaning, but the dataset response is coupled and condition-dependent. |
| powery | CR1 | control rod group 1 position or setting | 0.5 | indirect_or_conditional_physics | Type I/II: diffusion theory and spatial power integration | P=0.5 because control rod settings have a clear spatial-power mechanism, but exact local effects require further simulation-dependent inference. | control rod group 1 position or setting; P=0.5 because control rod settings have a clear spatial-power mechanism, but exact local effects require further simulation-dependent inference. |
| powery | CR2 | control rod group 2 position or setting | 0.5 | indirect_or_conditional_physics | Type I/II: diffusion theory and spatial power integration | P=0.5 because control rod settings have a clear spatial-power mechanism, but exact local effects require further simulation-dependent inference. | control rod group 2 position or setting; P=0.5 because control rod settings have a clear spatial-power mechanism, but exact local effects require further simulation-dependent inference. |
| powery | CR3 | control rod group 3 position or setting | 0.5 | indirect_or_conditional_physics | Type I/II: diffusion theory and spatial power integration | P=0.5 because control rod settings have a clear spatial-power mechanism, but exact local effects require further simulation-dependent inference. | control rod group 3 position or setting; P=0.5 because control rod settings have a clear spatial-power mechanism, but exact local effects require further simulation-dependent inference. |
| powery | CR4 | control rod group 4 position or setting | 0.5 | indirect_or_conditional_physics | Type I/II: diffusion theory and spatial power integration | P=0.5 because control rod settings have a clear spatial-power mechanism, but exact local effects require further simulation-dependent inference. | control rod group 4 position or setting; P=0.5 because control rod settings have a clear spatial-power mechanism, but exact local effects require further simulation-dependent inference. |
| htgr | theta1 | HTGR design or angular parameter 1 | 1.0 | strong_formula_or_standard_model | Type I/II: diffusion theory and quadrant-flux relation | P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. | HTGR design or angular parameter 1; P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. |
| htgr | theta2 | HTGR design or angular parameter 2 | 1.0 | strong_formula_or_standard_model | Type I/II: diffusion theory and quadrant-flux relation | P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. | HTGR design or angular parameter 2; P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. |
| htgr | theta3 | HTGR design or angular parameter 3 | 1.0 | strong_formula_or_standard_model | Type I/II: diffusion theory and quadrant-flux relation | P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. | HTGR design or angular parameter 3; P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. |
| htgr | theta4 | HTGR design or angular parameter 4 | 1.0 | strong_formula_or_standard_model | Type I/II: diffusion theory and quadrant-flux relation | P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. | HTGR design or angular parameter 4; P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. |
| microreactor | theta1 | microreactor design or angular parameter 1 | 1.0 | strong_formula_or_standard_model | Type I/II: diffusion theory and quadrant-flux relation | P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. | microreactor design or angular parameter 1; P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. |
| microreactor | theta2 | microreactor design or angular parameter 2 | 1.0 | strong_formula_or_standard_model | Type I/II: diffusion theory and quadrant-flux relation | P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. | microreactor design or angular parameter 2; P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. |
| microreactor | theta3 | microreactor design or angular parameter 3 | 1.0 | strong_formula_or_standard_model | Type I/II: diffusion theory and quadrant-flux relation | P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. | microreactor design or angular parameter 3; P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. |
| microreactor | theta4 | microreactor design or angular parameter 4 | 1.0 | strong_formula_or_standard_model | Type I/II: diffusion theory and quadrant-flux relation | P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. | microreactor design or angular parameter 4; P=0.5 because the theta variables have a plausible control-drum mechanism, but the detailed quadrant response is geometry- and simulation-dependent. |

## 各数据集推荐特征

| dataset | selected_features |
| --- | --- |
| bwr | CRD |
| chf | Xe (-), L (m), G (kg m-2s-1), P (kPa) |
| fp | ax_pow, clad_T, porosity |
| heat | qprime |
| htgr | theta1, theta8, theta5, theta4, theta2, theta3, theta7, theta6 |
| microreactor | theta6, theta4, theta7, theta3, theta1, theta5, theta2, theta8 |
| powery | CR4, CR3, CR2, CR5, CR1 |
| rea | rod_worth, beta |
| xs | FissionThermal, CaptureFast, FissionFast, CaptureThermal |

## 各数据集 Top 特征

| dataset | rank | feature | dp_fsm_score | feature_level | correlation_strength | rf_importance_norm | redundancy_max_abs | possible_nonlinear_relation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwr | 1 | CRD | 0.842 | core | 0.8136 | 1.0 | 0.042 | False |
| bwr | 2 | power_density | 0.3093 | low_priority | 0.024 | 0.0176 | 0.053 | False |
| bwr | 3 | DOM | 0.1653 | low_priority | 0.0835 | 0.0155 | 1.0 | False |
| bwr | 4 | PSZ | 0.1651 | low_priority | 0.0835 | 0.0148 | 1.0 | False |
| bwr | 5 | subcool | 0.158 | low_priority | 0.017 | 0.0172 | 0.053 | False |
| chf | 1 | Xe (-) | 0.6665 | core | 0.5314 | 0.801 | 0.6186 | False |
| chf | 2 | L (m) | 0.6191 | candidate | 0.6272 | 1.0 | 0.3289 | False |
| chf | 3 | G (kg m-2s-1) | 0.4956 | candidate | 0.3904 | 0.3599 | 0.6186 | False |
| chf | 4 | P (kPa) | 0.4423 | low_priority | 0.2663 | 0.3218 | 0.6043 | False |
| chf | 5 | Tin (C) | 0.4349 | low_priority | 0.3149 | 0.2407 | 0.6043 | False |
| fp | 1 | ax_pow | 0.76 | core | 0.5445 | 1.0 | 0.0854 | False |
| fp | 2 | clad_T | 0.5199 | candidate | 0.4242 | 0.3261 | 0.1432 | False |
| fp | 3 | porosity | 0.5091 | candidate | 0.2236 | 0.4841 | 0.0789 | False |
| fp | 4 | rough_fuel | 0.4012 | low_priority | 0.2116 | 0.1374 | 0.0868 | False |
| fp | 5 | inlet_T | 0.3421 | low_priority | 0.0787 | 0.0751 | 0.1126 | False |
| heat | 1 | qprime | 0.8593 | core | 0.8729 | 1.0 | 0.074 | False |
| heat | 2 | k | 0.4319 | low_priority | 0.3445 | 0.1009 | 0.0352 | False |
| heat | 3 | L | 0.329 | low_priority | 0.0767 | 0.0278 | 0.033 | False |
| heat | 4 | mdot | 0.3252 | low_priority | 0.0666 | 0.0221 | 0.0323 | False |
| heat | 5 | Tin | 0.3212 | low_priority | 0.0619 | 0.0191 | 0.074 | False |
| htgr | 1 | theta1 | 0.6063 | candidate | 0.03 | 1.0 | 0.0468 | True |
| htgr | 2 | theta8 | 0.6017 | candidate | 0.03 | 0.9846 | 0.0468 | True |
| htgr | 3 | theta5 | 0.6017 | candidate | 0.03 | 0.9845 | 0.0468 | True |
| htgr | 4 | theta4 | 0.5988 | candidate | 0.03 | 0.9748 | 0.0468 | True |
| htgr | 5 | theta2 | 0.5475 | candidate | 0.0138 | 0.8205 | 0.0468 | True |
| microreactor | 1 | theta6 | 0.6582 | core | 0.2002 | 1.0 | 0.0376 | True |
| microreactor | 2 | theta4 | 0.6193 | candidate | 0.1227 | 0.9482 | 0.0574 | True |
| microreactor | 3 | theta7 | 0.5999 | candidate | 0.1821 | 0.8267 | 0.0705 | True |
| microreactor | 4 | theta3 | 0.5919 | candidate | 0.1494 | 0.8345 | 0.0894 | True |
| microreactor | 5 | theta1 | 0.5616 | candidate | 0.1148 | 0.7671 | 0.0703 | True |
| powery | 1 | CR4 | 0.5466 | candidate | 0.3319 | 1.0 | 0.0662 | False |
| powery | 2 | CR3 | 0.5398 | candidate | 0.3413 | 0.9669 | 0.053 | False |
| powery | 3 | CR2 | 0.5354 | candidate | 0.3323 | 0.9628 | 0.0662 | False |
| powery | 4 | CR5 | 0.4976 | candidate | 0.3219 | 0.8431 | 0.0468 | False |
| powery | 5 | CR1 | 0.4949 | candidate | 0.3161 | 0.8423 | 0.053 | False |
| rea | 1 | rod_worth | 0.8198 | core | 0.7364 | 1.0 | 0.014 | False |
| rea | 2 | beta | 0.7286 | core | 0.5846 | 0.8459 | 0.0127 | False |
| rea | 3 | h_gap | 0.024 | low_priority | 0.0601 | 0.0247 | 0.0332 | False |
| rea | 4 | gamma_frac | 0.0125 | low_priority | 0.0182 | 0.0288 | 0.0332 | False |
| xs | 1 | FissionThermal | 0.7922 | core | 0.6783 | 1.0 | 0.2321 | False |
| xs | 2 | CaptureFast | 0.5705 | candidate | 0.5375 | 0.4894 | 0.7651 | False |
| xs | 3 | FissionFast | 0.5645 | candidate | 0.5565 | 0.4264 | 0.6708 | False |
| xs | 4 | CaptureThermal | 0.4638 | candidate | 0.3054 | 0.2838 | 0.3371 | False |
| xs | 5 | Scatter12 | 0.3691 | low_priority | 0.2374 | 0.1204 | 0.9127 | False |

## 高冗余特征对

| dataset | feature_a | feature_b | abs_pearson_corr |
| --- | --- | --- | --- |
| xs | Scatter12 | Scatter11 | 0.9127 |
| bwr | vanA | vanB | 1.0 |
| bwr | PSZ | DOM | 1.0 |

## 输出文件

- `tables/feature_scores_all.csv`：全部数据集特征综合得分。
- `tables/data_quality_summary.csv`：变量级描述性统计和数据质量诊断。
- `tables/preprocessing_diagnostics.csv`：数据集级预处理建议。
- `tables/physical_score_rationale.csv`：物理合理性评分、变量含义和评分依据。
- `tables/input_output_correlations_all.csv`：输入-输出 Pearson/Spearman 相关性长表。
- `tables/redundancy_pairs_all.csv`：输入变量间冗余关系。
- `tables/selected_features_by_dataset.csv`：按 DP-FSM 规则推荐的特征集。
- `figures/`：各数据集特征得分条形图、输入冗余热力图、输入-输出相关热力图。
