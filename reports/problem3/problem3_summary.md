# B题问题3：模型可解释性分析结果

本报告由 `scripts/run_problem3_explainability.py` 自动生成，基于问题2全特征最佳模型执行 TPCI-EM 解释流程。

## 方法说明

- 事前解释：沿用题面变量物理含义和问题1物理合理性评分。
- 事中解释：使用排列重要性识别模型实际依赖变量。
- 事后解释：对关键变量进行 ±10% 敏感性扰动，并为前两个关键变量生成部分响应数据。
- 一致性判断：综合关键变量物理合理性、排列重要性和已知方向扰动结果，给出高/中/低物理一致性等级。

## 物理一致性总表

| dataset | model | output_dim | top_features | top_physical_score | positive_importance_ratio_top3 | known_direction_consistency_rate | physical_consistency_level | interpretation_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chf | RandomForest | 1 | L (m), Xe (-), G (kg m-2s-1) | 1.0 | 1.0 | 1.0 | high | Key dependencies are physically plausible and response checks are mostly regular. |
| heat | GradientBoosting | 1 | qprime, k, L | 1.0 | 1.0 | 0.6666666666666666 | high | Key dependencies are physically plausible and response checks are mostly regular. |
| xs | Ridge | 1 | FissionThermal, CaptureFast, Scatter12 | 1.0 | 1.0 | 1.0 | high | Key dependencies are physically plausible and response checks are mostly regular. |
| bwr | GradientBoosting | 5 | CRD, vanA, vanB | 0.8667 | 1.0 | not_configured | medium | Key dependencies are plausible, but explicit direction checks are limited for this dataset. |
| fp | Ridge | 4 | ax_pow, clad_T, pellet_h | 1.0 | 1.0 | not_configured | medium | Key dependencies are plausible, but explicit direction checks are limited for this dataset. |
| rea | GradientBoosting | 4 | rod_worth, beta, h_gap | 1.0 | 1.0 | 1.0 | high | Key dependencies are physically plausible and response checks are mostly regular. |
| powery | Ridge | 22 | CR6, CR2, CR5 | 1.0 | 1.0 | not_configured | medium | Key dependencies are plausible, but explicit direction checks are limited for this dataset. |
| htgr | GradientBoosting | 4 | theta5, theta8, theta1 | 1.0 | 1.0 | not_configured | medium | Key dependencies are plausible, but explicit direction checks are limited for this dataset. |
| microreactor | GradientBoosting | 4 | theta4, theta6, theta1 | 1.0 | 1.0 | not_configured | medium | Key dependencies are plausible, but explicit direction checks are limited for this dataset. |

## 排列重要性 Top 特征

| dataset | model | importance_rank | feature | importance_mean | importance_std | physical_score |
| --- | --- | --- | --- | --- | --- | --- |
| bwr | GradientBoosting | 1 | CRD | 1.9128 | 0.1095 | 1.0 |
| bwr | GradientBoosting | 2 | vanA | 0.0182 | 0.0009 | 0.8 |
| bwr | GradientBoosting | 3 | vanB | 0.0166 | 0.0013 | 0.8 |
| bwr | GradientBoosting | 4 | DOM | 0.0083 | 0.0007 | 0.8 |
| bwr | GradientBoosting | 5 | PSZ | 0.0077 | 0.001 | 0.8 |
| chf | RandomForest | 1 | L (m) | 0.4563 | 0.0225 | 1.0 |
| chf | RandomForest | 2 | Xe (-) | 0.3469 | 0.0271 | 1.0 |
| chf | RandomForest | 3 | G (kg m-2s-1) | 0.1806 | 0.0112 | 1.0 |
| chf | RandomForest | 4 | P (kPa) | 0.139 | 0.0063 | 1.0 |
| chf | RandomForest | 5 | Tin (C) | 0.0938 | 0.0083 | 1.0 |
| fp | Ridge | 1 | ax_pow | 1.0174 | 0.0836 | 1.0 |
| fp | Ridge | 2 | clad_T | 0.4709 | 0.0466 | 1.0 |
| fp | Ridge | 3 | pellet_h | 0.3552 | 0.0311 | 1.0 |
| fp | Ridge | 4 | porosity | 0.2501 | 0.0356 | 1.0 |
| fp | Ridge | 5 | rough_fuel | 0.1128 | 0.0167 | 0.6 |
| heat | GradientBoosting | 1 | qprime | 2.0286 | 0.0891 | 1.0 |
| heat | GradientBoosting | 2 | k | 0.1577 | 0.0107 | 1.0 |
| heat | GradientBoosting | 3 | L | 0.0024 | 0.0002 | 1.0 |
| heat | GradientBoosting | 4 | mdot | 0.0022 | 0.0002 | 1.0 |
| heat | GradientBoosting | 5 | Cp | 0.0003 | 0.0 | 1.0 |
| htgr | GradientBoosting | 1 | theta5 | 0.2115 | 0.009 | 1.0 |
| htgr | GradientBoosting | 2 | theta8 | 0.2044 | 0.0054 | 1.0 |
| htgr | GradientBoosting | 3 | theta1 | 0.2037 | 0.0084 | 1.0 |
| htgr | GradientBoosting | 4 | theta4 | 0.1992 | 0.0061 | 1.0 |
| htgr | GradientBoosting | 5 | theta2 | 0.1878 | 0.0056 | 1.0 |
| microreactor | GradientBoosting | 1 | theta4 | 0.1954 | 0.0161 | 1.0 |
| microreactor | GradientBoosting | 2 | theta6 | 0.1537 | 0.0091 | 1.0 |
| microreactor | GradientBoosting | 3 | theta1 | 0.1485 | 0.0052 | 1.0 |
| microreactor | GradientBoosting | 4 | theta7 | 0.1423 | 0.0047 | 1.0 |
| microreactor | GradientBoosting | 5 | theta3 | 0.1416 | 0.0127 | 1.0 |
| powery | Ridge | 1 | CR6 | 0.3469 | 0.0198 | 1.0 |
| powery | Ridge | 2 | CR2 | 0.3388 | 0.0217 | 1.0 |
| powery | Ridge | 3 | CR5 | 0.3374 | 0.0235 | 1.0 |
| powery | Ridge | 4 | CR3 | 0.3332 | 0.0273 | 1.0 |
| powery | Ridge | 5 | CR4 | 0.3228 | 0.0244 | 1.0 |
| rea | GradientBoosting | 1 | rod_worth | 1.1119 | 0.0732 | 1.0 |
| rea | GradientBoosting | 2 | beta | 0.8964 | 0.0465 | 1.0 |
| rea | GradientBoosting | 3 | h_gap | 0.0116 | 0.0005 | 1.0 |
| rea | GradientBoosting | 4 | gamma_frac | 0.0012 | 0.0003 | 1.0 |
| xs | Ridge | 1 | FissionThermal | 0.9159 | 0.0762 | 1.0 |
| xs | Ridge | 2 | CaptureFast | 0.6158 | 0.0542 | 1.0 |
| xs | Ridge | 3 | Scatter12 | 0.2704 | 0.0203 | 1.0 |
| xs | Ridge | 4 | CaptureThermal | 0.2162 | 0.01 | 1.0 |
| xs | Ridge | 5 | FissionFast | 0.1891 | 0.0113 | 1.0 |

## +10% 敏感性扰动摘要

| dataset | feature | target | mean_prediction_delta | normalized_mean_delta | response_direction | expected_direction | direction_consistent |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bwr | CRD | F-delta-H | -0.01824 | -0.02502 | -1 | 0 | False |
| bwr | CRD | K-eff | 0.0041 | 0.01359 | 1 | 0 | False |
| bwr | CRD | Max-Fxy | -0.02534 | -0.05879 | -1 | 0 | False |
| bwr | CRD | Max3Pin | -0.11945 | -0.02205 | -1 | 0 | False |
| bwr | CRD | Max4Pin | -0.12119 | -0.02051 | -1 | 0 | False |
| bwr | vanA | F-delta-H | -0.00046 | -0.00063 | -1 | 0 | False |
| bwr | vanA | K-eff | -0.00057 | -0.00189 | -1 | 0 | False |
| bwr | vanA | Max-Fxy | -0.00049 | -0.00113 | -1 | 0 | False |
| bwr | vanA | Max3Pin | 0.04882 | 0.00901 | 1 | 0 | False |
| bwr | vanA | Max4Pin | 0.00238 | 0.0004 | 1 | 0 | False |
| bwr | vanB | F-delta-H | 0.00644 | 0.00883 | 1 | 0 | False |
| bwr | vanB | K-eff | 0.00037 | 0.00122 | 1 | 0 | False |
| chf | G (kg m-2s-1) | CHF (kW m-2) | 55.2096 | 0.00571 | 1 | 1 | True |
| chf | L (m) | CHF (kW m-2) | -114.53493 | -0.01185 | -1 | -1 | True |
| chf | Xe (-) | CHF (kW m-2) | -44.00816 | -0.00455 | -1 | -1 | True |
| fp | ax_pow | fis_gas_produced | 0.0 | 0.21632 | 1 | 0 | False |
| fp | ax_pow | max_fuel_centerline_temp | 75.29978 | 0.40977 | 1 | 0 | False |
| fp | ax_pow | max_fuel_surface_temp | 4.92265 | 0.12225 | 1 | 0 | False |
| fp | ax_pow | radial_clad_dia | 0.0 | 0.39153 | 1 | 0 | False |
| fp | clad_T | fis_gas_produced | -0.0 | -0.00012 | -1 | 0 | False |
| fp | clad_T | max_fuel_centerline_temp | 24.14059 | 0.13137 | 1 | 0 | False |
| fp | clad_T | max_fuel_surface_temp | 12.43522 | 0.30881 | 1 | 0 | False |
| fp | clad_T | radial_clad_dia | 0.0 | 0.18396 | 1 | 0 | False |
| fp | pellet_h | fis_gas_produced | 0.0 | 0.32919 | 1 | 0 | False |
| fp | pellet_h | max_fuel_centerline_temp | -0.54927 | -0.00299 | -1 | 0 | False |
| fp | pellet_h | max_fuel_surface_temp | -0.66992 | -0.01664 | -1 | 0 | False |
| fp | pellet_h | radial_clad_dia | -0.0 | -0.00445 | -1 | 0 | False |
| heat | L | T | 5.95865 | 0.0114 | 1 | 1 | True |
| heat | k | T | 96.68639 | 0.18493 | 1 | -1 | False |
| heat | qprime | T | 183.72323 | 0.35141 | 1 | 1 | True |
| htgr | theta1 | fluxQ1 | -0.00025 | -0.01075 | -1 | 0 | False |
| htgr | theta1 | fluxQ2 | 5e-05 | 0.00211 | 1 | 0 | False |
| htgr | theta1 | fluxQ3 | 0.00012 | 0.00566 | 1 | 0 | False |
| htgr | theta1 | fluxQ4 | 1e-05 | 0.00062 | 1 | 0 | False |
| htgr | theta5 | fluxQ1 | 0.0001 | 0.00426 | 1 | 0 | False |
| htgr | theta5 | fluxQ2 | -0.0 | -0.0 | -1 | 0 | False |
| htgr | theta5 | fluxQ3 | -0.00024 | -0.01091 | -1 | 0 | False |
| htgr | theta5 | fluxQ4 | 5e-05 | 0.00212 | 1 | 0 | False |
| htgr | theta8 | fluxQ1 | 0.0 | 0.00019 | 1 | 0 | False |
| htgr | theta8 | fluxQ2 | 0.0001 | 0.00406 | 1 | 0 | False |
| htgr | theta8 | fluxQ3 | 6e-05 | 0.00299 | 1 | 0 | False |
| htgr | theta8 | fluxQ4 | -0.00028 | -0.01151 | -1 | 0 | False |
| microreactor | theta1 | fluxQ1 | 1.484322406985343e+16 | 0.00707 | 1 | 0 | False |
| microreactor | theta1 | fluxQ2 | 2393968657772517.0 | 0.001 | 1 | 0 | False |
| microreactor | theta1 | fluxQ3 | -5010540731065839.0 | -0.00251 | -1 | 0 | False |
| microreactor | theta1 | fluxQ4 | -9523796614597218.0 | -0.00397 | -1 | 0 | False |
| microreactor | theta4 | fluxQ1 | 6698201969266064.0 | 0.00319 | 1 | 0 | False |
| microreactor | theta4 | fluxQ2 | -2.3931823437279284e+16 | -0.00997 | -1 | 0 | False |
| microreactor | theta4 | fluxQ3 | 8177000446583923.0 | 0.00409 | 1 | 0 | False |
| microreactor | theta4 | fluxQ4 | 1.7574467809769214e+16 | 0.00732 | 1 | 0 | False |
| microreactor | theta6 | fluxQ1 | 440745868331482.75 | 0.00021 | 1 | 0 | False |
| microreactor | theta6 | fluxQ2 | 3689468667171683.5 | 0.00154 | 1 | 0 | False |
| microreactor | theta6 | fluxQ3 | -1.831403402775111e+16 | -0.00916 | -1 | 0 | False |
| microreactor | theta6 | fluxQ4 | -3180665249333438.0 | -0.00133 | -1 | 0 | False |
| powery | CR2 | A-2 | -24.99538 | -0.04647 | -1 | 0 | False |
| powery | CR2 | B-1 | -28.22817 | -0.04334 | -1 | 0 | False |
| powery | CR2 | B-2 | 27.20897 | 0.04162 | 1 | 0 | False |
| powery | CR2 | B-4 | -5.28695 | -0.00839 | -1 | 0 | False |
| powery | CR2 | B-5 | -52.5258 | -0.08677 | -1 | 0 | False |
| powery | CR2 | B-7 | -76.06214 | -0.1206 | -1 | 0 | False |
| powery | CR2 | B-8 | -71.64012 | -0.11347 | -1 | 0 | False |
| powery | CR2 | C-1 | -21.09893 | -0.0145 | -1 | 0 | False |
| powery | CR2 | C-10 | -77.86472 | -0.06415 | -1 | 0 | False |
| powery | CR2 | C-11 | -79.0122 | -0.06161 | -1 | 0 | False |
| powery | CR2 | C-12 | -79.12048 | -0.06191 | -1 | 0 | False |
| powery | CR2 | C-13 | -75.44395 | -0.04963 | -1 | 0 | False |
| rea | beta | avg_Tcool | -0.71377 | -0.1693 | -1 | 0 | False |
| rea | beta | burst_width | 0.24416 | 0.14843 | 1 | 1 | True |
| rea | beta | max_Tf | -41.94932 | -0.15776 | -1 | 0 | False |
| rea | beta | max_power | -161.05601 | -0.12433 | -1 | -1 | True |
| rea | h_gap | avg_Tcool | 0.03084 | 0.00731 | 1 | 0 | False |
| rea | h_gap | burst_width | 0.00027 | 0.00016 | 1 | 0 | False |
| rea | h_gap | max_Tf | -1.18871 | -0.00447 | -1 | -1 | True |
| rea | h_gap | max_power | 0.90282 | 0.0007 | 1 | 0 | False |
| rea | rod_worth | avg_Tcool | 0.87246 | 0.20695 | 1 | 1 | True |
| rea | rod_worth | burst_width | -0.08475 | -0.05152 | -1 | -1 | True |
| rea | rod_worth | max_Tf | 37.29589 | 0.14026 | 1 | 1 | True |
| rea | rod_worth | max_power | 239.61256 | 0.18497 | 1 | 1 | True |
| xs | CaptureFast | k | -0.01179 | -0.25757 | -1 | -1 | True |
| xs | FissionThermal | k | 0.01231 | 0.26876 | 1 | 1 | True |
| xs | Scatter12 | k | 0.00702 | 0.15333 | 1 | 1 | True |

## 输出文件

- `tables/permutation_importance_all.csv`：所有数据集的排列重要性。
- `tables/sensitivity_analysis_all.csv`：关键变量 ±10% 敏感性扰动结果。
- `tables/partial_response_all.csv`：关键变量部分响应数据。
- `tables/physical_consistency_summary.csv`：物理一致性等级和解释备注。
- `figures/`：排列重要性图、敏感性热力图和关键变量部分响应图。
