# B题问题2：模型构建与精度评估结果

本报告由 `scripts/run_problem2_modeling.py` 自动生成，对全特征集和问题1筛选特征集分别训练并评价模型。

## 方法说明

- 训练测试划分：80% 训练集，20% 测试集，固定随机种子。
- 候选模型：Ridge、KNN、随机森林、梯度提升树。
- 单输出和多输出均计算 R2、MAE、RMSE、NMAE、NRMSE。
- 模型排序：`Score = 0.4 * R2排名 + 0.35 * NRMSE排名 + 0.25 * NMAE排名`，分数越小越优。

## 每个数据集的最佳模型

| dataset | feature_set | model | input_dim | output_dim | mean_r2 | mean_mae | mean_rmse | mean_nmae | mean_nrmse | std_r2 | std_nrmse | rank_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwr | full | GradientBoosting | 9 | 5 | 0.9663 | 0.0743 | 0.1546 | 0.0203 | 0.0403 | 0.0204 | 0.0187 | 1.0 |
| bwr | selected | GradientBoosting | 1 | 5 | 0.9417 | 0.0832 | 0.1765 | 0.03 | 0.0553 | 0.0281 | 0.0138 | 1.0 |
| chf | full | RandomForest | 6 | 1 | 0.9556 | 195.065 | 325.0459 | 0.015 | 0.0249 | 0.0 | 0.0 | 1.25 |
| chf | selected | KNN | 4 | 1 | 0.9413 | 242.0288 | 373.9559 | 0.0186 | 0.0287 | 0.0 | 0.0 | 1.0 |
| fp | full | Ridge | 13 | 4 | 0.9775 | 0.9555 | 1.1377 | 0.015 | 0.0178 | 0.0345 | 0.0175 | 1.0 |
| fp | selected | Ridge | 3 | 4 | 0.7362 | 2.0788 | 2.6133 | 0.0608 | 0.0749 | 0.2786 | 0.0493 | 1.0 |
| heat | full | GradientBoosting | 7 | 1 | 0.9975 | 5.9339 | 7.4742 | 0.0089 | 0.0112 | 0.0 | 0.0 | 1.0 |
| heat | selected | GradientBoosting | 1 | 1 | 0.9063 | 37.4069 | 45.4545 | 0.0558 | 0.0679 | 0.0 | 0.0 | 1.0 |
| htgr | full | GradientBoosting | 8 | 4 | 0.903 | 0.001 | 0.0013 | 0.0399 | 0.0519 | 0.0011 | 0.0009 | 1.0 |
| htgr | selected | GradientBoosting | 8 | 4 | 0.903 | 0.001 | 0.0013 | 0.0399 | 0.0519 | 0.0011 | 0.0009 | 1.0 |
| microreactor | full | GradientBoosting | 8 | 4 | 0.6581 | 2.3598804952570515e+17 | 2.8643704653862576e+17 | 0.0851 | 0.1033 | 0.0174 | 0.0042 | 1.0 |
| microreactor | selected | GradientBoosting | 8 | 4 | 0.6574 | 2.361796959095455e+17 | 2.8673938815469386e+17 | 0.0851 | 0.1034 | 0.0175 | 0.0042 | 1.0 |
| powery | full | Ridge | 6 | 22 | 0.9953 | 12.2887 | 16.5786 | 0.0096 | 0.0131 | 0.002 | 0.0021 | 1.0 |
| powery | selected | Ridge | 6 | 22 | 0.9953 | 12.2887 | 16.5786 | 0.0096 | 0.0131 | 0.002 | 0.0021 | 1.0 |
| rea | full | GradientBoosting | 4 | 4 | 0.9927 | 2.82 | 3.8795 | 0.0064 | 0.0098 | 0.0047 | 0.0007 | 1.0 |
| rea | selected | GradientBoosting | 2 | 4 | 0.9858 | 3.5018 | 4.7889 | 0.01 | 0.0149 | 0.0057 | 0.0053 | 1.25 |
| xs | full | Ridge | 8 | 1 | 0.9999 | 0.0 | 0.0001 | 0.001 | 0.0014 | 0.0 | 0.0 | 1.0 |
| xs | selected | Ridge | 4 | 1 | 0.9566 | 0.0013 | 0.0016 | 0.0286 | 0.035 | 0.0 | 0.0 | 1.0 |

## 每个输出变量的最佳模型

| dataset | target | feature_set | model | r2 | mae | rmse | nmae | nrmse | target_rank_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwr | F-delta-H | full | GradientBoosting | 0.9835 | 0.015 | 0.0263 | 0.0199 | 0.0349 | 1.0 |
| bwr | K-eff | full | GradientBoosting | 0.9968 | 0.0027 | 0.0051 | 0.0086 | 0.0166 | 1.0 |
| bwr | Max-Fxy | full | GradientBoosting | 0.943 | 0.0062 | 0.0117 | 0.0136 | 0.0258 | 1.0 |
| bwr | Max3Pin | full | GradientBoosting | 0.9552 | 0.1671 | 0.3474 | 0.0298 | 0.0619 | 1.0 |
| bwr | Max4Pin | full | GradientBoosting | 0.953 | 0.1805 | 0.3826 | 0.0294 | 0.0624 | 1.0 |
| chf | CHF (kW m-2) | full | RandomForest | 0.9556 | 195.065 | 325.0459 | 0.015 | 0.0249 | 1.25 |
| fp | fis_gas_produced | full | Ridge | 0.9992 | 0.0 | 0.0 | 0.004 | 0.005 | 1.0 |
| fp | max_fuel_centerline_temp | full | Ridge | 0.9961 | 1.817 | 2.2055 | 0.0079 | 0.0096 | 1.0 |
| fp | max_fuel_surface_temp | full | GradientBoosting | 0.9219 | 1.6883 | 2.2847 | 0.0345 | 0.0467 | 1.0 |
| fp | radial_clad_dia | full | Ridge | 0.997 | 0.0 | 0.0 | 0.007 | 0.0086 | 1.0 |
| heat | T | full | GradientBoosting | 0.9975 | 5.9339 | 7.4742 | 0.0089 | 0.0112 | 1.0 |
| htgr | fluxQ1 | full | GradientBoosting | 0.9039 | 0.001 | 0.0013 | 0.0397 | 0.051 | 1.0 |
| htgr | fluxQ2 | full | GradientBoosting | 0.9015 | 0.0011 | 0.0014 | 0.0413 | 0.0533 | 1.0 |
| htgr | fluxQ3 | full | GradientBoosting | 0.9041 | 0.001 | 0.0013 | 0.0395 | 0.0512 | 1.25 |
| htgr | fluxQ4 | full | GradientBoosting | 0.9025 | 0.001 | 0.0013 | 0.0392 | 0.052 | 1.0 |
| microreactor | fluxQ1 | full | GradientBoosting | 0.6424 | 2.212571616912609e+17 | 2.73618847508772e+17 | 0.079 | 0.0977 | 1.25 |
| microreactor | fluxQ2 | full | GradientBoosting | 0.6558 | 2.4160928563602208e+17 | 2.958536446430868e+17 | 0.0895 | 0.1096 | 1.0 |
| microreactor | fluxQ3 | full | GradientBoosting | 0.6872 | 2.4295157258671142e+17 | 2.901292064325925e+17 | 0.0868 | 0.1036 | 1.0 |
| microreactor | fluxQ4 | full | GradientBoosting | 0.6472 | 2.381341781888263e+17 | 2.8614648757005178e+17 | 0.085 | 0.1022 | 1.0 |
| powery | A-2 | full | Ridge | 0.9888 | 7.8853 | 11.035 | 0.0134 | 0.0187 | 1.0 |
| powery | B-1 | full | Ridge | 0.9952 | 6.7895 | 9.3084 | 0.0094 | 0.0129 | 1.0 |
| powery | B-2 | selected | Ridge | 0.9948 | 7.4273 | 10.145 | 0.009 | 0.0123 | 1.0 |
| powery | B-4 | selected | Ridge | 0.9919 | 7.6245 | 10.9566 | 0.011 | 0.0158 | 1.0 |
| powery | B-5 | full | Ridge | 0.9933 | 7.8413 | 10.6389 | 0.0099 | 0.0135 | 1.0 |
| powery | B-7 | full | Ridge | 0.9956 | 6.2925 | 8.186 | 0.0091 | 0.0118 | 1.0 |
| rea | avg_Tcool | full | GradientBoosting | 0.9958 | 0.037 | 0.0488 | 0.0082 | 0.0107 | 1.0 |
| rea | burst_width | selected | GradientBoosting | 0.9854 | 0.0078 | 0.0187 | 0.0041 | 0.0099 | 1.25 |
| rea | max_Tf | full | GradientBoosting | 0.9944 | 1.9598 | 2.7736 | 0.0065 | 0.0091 | 1.0 |
| rea | max_power | selected | KNN | 0.9971 | 6.8421 | 10.9443 | 0.005 | 0.0079 | 1.0 |
| xs | k | full | Ridge | 0.9999 | 0.0 | 0.0001 | 0.001 | 0.0014 | 1.0 |

## 全特征与筛选特征对比

| dataset | full_best_model | selected_best_model | full_input_dim | selected_input_dim | dim_reduction_rate | full_mean_r2 | selected_mean_r2 | delta_r2_selected_minus_full | full_mean_nrmse | selected_mean_nrmse | delta_nrmse_selected_minus_full | screening_assessment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwr | GradientBoosting | GradientBoosting | 9 | 1 | 0.8889 | 0.9663 | 0.9417 | -0.0246 | 0.0403 | 0.0553 | 0.015 | usable_but_accuracy_loss |
| chf | RandomForest | KNN | 6 | 4 | 0.3333 | 0.9556 | 0.9413 | -0.0144 | 0.0249 | 0.0287 | 0.0038 | effective_with_small_loss |
| fp | Ridge | Ridge | 13 | 3 | 0.7692 | 0.9775 | 0.7362 | -0.2414 | 0.0178 | 0.0749 | 0.0571 | too_aggressive_keep_full_or_relax_threshold |
| heat | GradientBoosting | GradientBoosting | 7 | 1 | 0.8571 | 0.9975 | 0.9063 | -0.0912 | 0.0112 | 0.0679 | 0.0567 | too_aggressive_keep_full_or_relax_threshold |
| htgr | GradientBoosting | GradientBoosting | 8 | 8 | 0.0 | 0.903 | 0.903 | -0.0 | 0.0519 | 0.0519 | 0.0 | no_dimension_reduction |
| microreactor | GradientBoosting | GradientBoosting | 8 | 8 | 0.0 | 0.6581 | 0.6574 | -0.0007 | 0.1033 | 0.1034 | 0.0001 | no_dimension_reduction |
| powery | Ridge | Ridge | 6 | 6 | 0.0 | 0.9953 | 0.9953 | -0.0 | 0.0131 | 0.0131 | 0.0 | no_dimension_reduction |
| rea | GradientBoosting | GradientBoosting | 4 | 2 | 0.5 | 0.9927 | 0.9858 | -0.0069 | 0.0098 | 0.0149 | 0.0051 | effective_with_small_loss |
| xs | Ridge | Ridge | 8 | 4 | 0.5 | 0.9999 | 0.9566 | -0.0433 | 0.0014 | 0.035 | 0.0336 | usable_but_accuracy_loss |

## 数据规模、输入维度和输出维度影响

| dataset | n_samples | full_input_dim | output_dim | full_best_model | full_best_mean_r2 | full_best_mean_nrmse | std_r2 | std_nrmse | selected_best_model | selected_best_mean_r2 | selected_best_mean_nrmse | selected_input_dim | dim_reduction_rate | delta_r2_selected_minus_full | delta_nrmse_selected_minus_full |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xs | 1000 | 8 | 1 | Ridge | 0.9999 | 0.0014 | 0.0 | 0.0 | Ridge | 0.9566 | 0.035 | 4 | 0.5 | -0.0433 | 0.0336 |
| rea | 2000 | 4 | 4 | GradientBoosting | 0.9927 | 0.0098 | 0.0047 | 0.0007 | GradientBoosting | 0.9858 | 0.0149 | 2 | 0.5 | -0.0069 | 0.0051 |
| heat | 1000 | 7 | 1 | GradientBoosting | 0.9975 | 0.0112 | 0.0 | 0.0 | GradientBoosting | 0.9063 | 0.0679 | 1 | 0.8571 | -0.0912 | 0.0567 |
| powery | 1000 | 6 | 22 | Ridge | 0.9953 | 0.0131 | 0.002 | 0.0021 | Ridge | 0.9953 | 0.0131 | 6 | 0.0 | -0.0 | 0.0 |
| fp | 400 | 13 | 4 | Ridge | 0.9775 | 0.0178 | 0.0345 | 0.0175 | Ridge | 0.7362 | 0.0749 | 3 | 0.7692 | -0.2414 | 0.0571 |
| chf | 2500 | 6 | 1 | RandomForest | 0.9556 | 0.0249 | 0.0 | 0.0 | KNN | 0.9413 | 0.0287 | 4 | 0.3333 | -0.0144 | 0.0038 |
| bwr | 2000 | 9 | 5 | GradientBoosting | 0.9663 | 0.0403 | 0.0204 | 0.0187 | GradientBoosting | 0.9417 | 0.0553 | 1 | 0.8889 | -0.0246 | 0.015 |
| htgr | 3004 | 8 | 4 | GradientBoosting | 0.903 | 0.0519 | 0.0011 | 0.0009 | GradientBoosting | 0.903 | 0.0519 | 8 | 0.0 | -0.0 | 0.0 |
| microreactor | 751 | 8 | 4 | GradientBoosting | 0.6581 | 0.1033 | 0.0174 | 0.0042 | GradientBoosting | 0.6574 | 0.1034 | 8 | 0.0 | -0.0007 | 0.0001 |

## 输出文件

- `tables/model_metrics_all.csv`：所有数据集、特征集、模型的聚合指标和综合排名。
- `tables/target_metrics_all.csv`：每个输出变量的 R2、MAE、RMSE、NMAE、NRMSE。
- `tables/best_models_by_target.csv`：每个输出变量的最佳模型和最佳特征集。
- `tables/best_models_by_dataset.csv`：每个数据集和特征集下的最佳模型。
- `tables/feature_set_comparison.csv`：全特征与筛选特征的最佳模型对比。
- `tables/dataset_factor_analysis.csv`：样本规模、输入维度、输出维度与模型表现的汇总。
- `figures/`：模型精度对比、特征筛选效果对比和数据集难度图。
