# 输入输出物理合理性汇总表（多输出部分按行保留众数）

**评分标准：**
* **1 分**：存在明确物理机制、公式或可靠文献支持，且作用方向合理；
* **0.5 分**：存在间接或条件性物理联系，但证据不完整；
* **0 分**：未找到足够直接的合理机理，不强行给分。

**说明：**
在保留六个数据集的基础上，对多输入多输出数据集（FP、BWR、Powery、REA）采用**按行保留众数**的方式，即固定每一行输入，在该行多个输出评分中取出现次数最多的值作为最终保留值；若众数并列，则取较高分。

---

## 1. CHF 数据集
* **输入变量**：`P`、`D`、`L`、`G`、`Tin`、`Xe`
* **输出变量**：`CHF`

| 输入变量 | 输出变量 | 评分 | 说明 |
| :--- | :--- | :--- | :--- |
| **P** | CHF | 1.0 | 压力是 CHF 的核心控制变量之一。 |
| **D** | CHF | 0.5 | 通道直径属于几何修正变量，关系存在但不如 P/G/Xe 直接。 |
| **L** | CHF | 0.5 | 加热长度影响流动发展和干涸条件，属于条件性影响。 |
| **G** | CHF | 1.0 | 质量通量是 CHF 的经典主变量。 |
| **Tin** | CHF | 1.0 | 进口温度通过入口亚冷度影响 CHF，关系明确。 |
| **Xe** | CHF | 1.0 | 出口平衡品质是 CHF 预测中的标准主变量之一。 |

---

## 2. FP 数据集
* **输入变量**：`fuel_dens`、`porosity`、`clad_thick`、`pellet_OD`、`pellet_h`、`gap_thick`、`inlet_T`、`enrich`、`rough_fuel`、`rough_clad`、`ax_pow`、`clad_T`、`pressure`
* **说明**：多输出部分按行保留众数后仅保留一列最终评分。

| 输入变量 | 最终保留值 |
| :--- | :---: |
| **fuel_dens** | 0.5 |
| **porosity** | 1.0 |
| **clad_thick** | 1.0 |
| **pellet_OD** | 0.0 |
| **pellet_h** | 0.0 |
| **gap_thick** | 1.0 |
| **inlet_T** | 1.0 |
| **enrich** | 0.0 |
| **rough_fuel** | 1.0 |
| **rough_clad** | 1.0 |
| **ax_pow** | 1.0 |
| **clad_T** | 1.0 |
| **pressure** | 0.0 |

---

## 3. BWR 数据集
* **输入变量**：`PSZ`、`DOM`、`vanA`、`vanB`、`subcool`、`CRD`、`flow_rate`、`power_density`、`VFNGAP`
* **说明**：多输出部分按行保留众数后仅保留一列最终评分。

| 输入变量 | 最终保留值 |
| :--- | :---: |
| **PSZ** | 0.5 |
| **DOM** | 0.5 |
| **vanA** | 0.5 |
| **vanB** | 0.5 |
| **subcool** | 0.5 |
| **CRD** | 1.0 |
| **flow_rate** | 0.5 |
| **power_density** | 1.0 |
| **VFNGAP** | 0.5 |

---

## 4. Powery 数据集
* **输入变量**：`CR1` ~ `CR6`
* **说明**：原始输出为 22 个燃料元件功率，当前按行保留众数后仅保留一列最终评分。

| 输入变量 | 最终保留值 |
| :--- | :---: |
| **CR1** | 0.5 |
| **CR2** | 0.5 |
| **CR3** | 0.5 |
| **CR4** | 0.5 |
| **CR5** | 0.5 |
| **CR6** | 0.5 |

---

## 5. REA 数据集
* **输入变量**：`rod_worth`、`beta`、`h_gap`、`gamma_frac`
* **说明**：多输出部分按行保留众数后仅保留一列最终评分。

| 输入变量 | 最终保留值 |
| :--- | :---: |
| **rod_worth** | 1.0 |
| **beta** | 1.0 |
| **h_gap** | 0.0 |
| **gamma_frac** | 0.0 |

---

## 6. XS 数据集
* **输入变量**：`FissionFast`、`FissionThermal`、`CaptureFast`、`CaptureThermal`、`Scatter11`、`Scatter22`、`Scatter12`、`Scatter21`
* **输出变量**：`k_infinity`

| 输入变量 | 输出变量 | 评分 | 说明 |
| :--- | :--- | :---: | :--- |
| **FissionFast** | k_infinity | 1.0 | 直接影响快群裂变产生项。 |
| **FissionThermal** | k_infinity | 1.0 | 直接影响热群裂变产生项。 |
| **CaptureFast** | k_infinity | 1.0 | 直接增加快群吸收损失。 |
| **CaptureThermal** | k_infinity | 1.0 | 直接增加热群吸收损失。 |
| **Scatter11** | k_infinity | 0.5 | 影响快群能谱与群内分布，属间接作用。 |
| **Scatter22** | k_infinity | 0.5 | 影响热群分布，属间接作用。 |
| **Scatter12** | k_infinity | 1.0 | 直接影响快→热慢化过程，是关键群间耦合项。 |
| **Scatter21** | k_infinity | 0.5 | 对热→快迁移有影响，但通常不是主导项。 |

---

## 7. heat / microreactor / htgr 数据集
* 输入变量 `P` 全为 1。
