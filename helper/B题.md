<!-- Page 1 -->
 
 
B题：核能系统中的可解释性预测建模与特征分析 
核能系统作为高度复杂的工程系统，其运行状态受多种物理机制共同影响，如热工水力、
中子物理、 材料性能等。 在核反应堆的设计、 运行与安全评估中， 关键参数的准确预测至关重
要。然而，传统机器学习模型往往表现为“黑箱”，难以提供可解释的决策依据，这在高风险行
业中是不可接受的。 本题目旨在引导参赛者探索如何在保证预测精度的同时， 提升模型的可解
释性，适用于核能系统中的关键参数预测任务。 
基于核能系统中的数据集，如临界热流密度、燃料性能、反应堆中子分布等，见附件一，
完成以下任务： 
1.   特征分析与预处理 
分析各个数据集中各输入特征与输出变量之间的关系； 识别可能存在的冗余特征或非线性
关系；提出合理的特征选择或降维策略。 
2.   模型构建与精度评估 
在问题 1 提取的特征基础上， 划分训练集与测试集； 设计合适的模型实现预测任务， 并对
诊断结果进行评价。 充分考虑不同数据集， 分析模型在不同数据集上的性能表现， 探讨数据规
模、输出维度等对模型能力的影响。 
3.   模型可解释性分析 
可解释性是机器学习领域的重要研究方向之一。 由于机器学习模型的“黑箱”问题， 其预测
过程难以被观测和理解， 这可能造成对模型结果的不信任或盲目信任， 进而影响预测模型的应
用。模型可解释性研究的核心目标是解决模型的透明性问题，提高模型输出的理解和信任度。
请考虑问题 2 中模型的结构设计和决策过程， 结合核能系统特点与机理， 进行事前、 事中、 事
后的可解释性进行分析，分析模型是否能够反映出物理上的合理关系。 
任务要求 
建模论文：提交一篇完整的建模论文，包括问题重述、数据预处理、模型建立、结果分析
与可解释性讨论； 
代码与模型：提交完整的建模代码和数据集，并附上必要的使用说明； 

<!-- Page 2 -->
结果展示：用图表展示模型精度、特征重要性、可解释性分析结果等； 
 
 
 
附件
附件：核能系统中的数据集。
数据说明： 
数据来源于核能系统中的典型工程问题 
1. 关键热通量数据集 chf。临界热通量（CHF） ，由于在沸腾液体和加热表面之间存在不可渗透的蒸
汽层，导致传热急剧下降的条件，对轻水核反应堆（LWRs）构成了严重的安全隐患。CHF 数据集包含美国
核管理委员会 （NRC） 收集的超过60 年的垂直流动沸腾装置实验数据。 这些实验以均匀加热的通道为基础，
旨在模拟核反应堆（轻水）中的流动沸腾条件，这些实验将压力（P） 、通道直径（D） 、加热长度（L） 、质
量通量（G） 、进口温度（T_in）和出口平衡质量（Xe）作为输入/特征，以预测单个输出，CHF。 
P：压力（MPa） 
D：通道直径（m） 
L：加热长度（m） 
G：质量流速（kg/(m²·s)） 
Tin：入口温度（℃） 
Xe：出口平衡品质 
CHF：临界热流密度（kW/m²） ，即沸腾危机发生时的热流密度阈值 
参考文献：Le Corre J-M, Delipei G, Wu X, Zhao X. Benchmark on Artificial Intelligence and Machine Learning 
for Scientific Computing in Nuclear Engineering. Phase 1: Critical Heat Flux Exercise Specificiations. NEA/WKP; 
2023. 
2. 材料和燃料性能数据集 fp。瞬时场景，如反应堆启动或关闭期间，可能导致核反应堆中氧化燃料
的颗粒包壳机械相互作用（PCMIs）问题。基于 BISON 模拟，一种用于模拟核材料性能的结构力学计算机
代码，Radaideh 和 Kozlowski 为平均线性热功率为 40 𝑘𝑊/𝑚的 10 颗粒 PWR 燃料棒（一个上升瞬态场景）
生成了 400 个 PCMIs 数据点。 数据集包含基于燃料几何和物理性质的13 个输入和 4 个输出。 输入包括： 燃
料密度 （fuel_dens） 、 孔隙率 （porosity） 、 包壳厚度 （clad_thick） 、 颗粒外径 （pellet_OD） 、 颗粒高度 （pellet_h）、
间隙厚度（gap_thick） 、进口温度（inlet_T） 、铀-235 富集度（enrich） 、燃料粗糙度（rough_fuel） 、包壳粗糙
度（rough_clad） 、 轴向功率 （ax_pow） 、包壳表面温度 （clad_T） 和压力（pressure） 。输出包括：裂变气体产
生（fission_gas） 、最大燃料表面温度（max_fuel_surface_T） 、最大包壳温度（max_fuel_cl_T）和径向包壳直
径位移（radial_clad_T）。 

<!-- Page 3 -->
参考文献：Le Corre J-M, Delipei G, Wu X, Zhao X. Benchmark on Artificial Intelligence and Machine Learning 
for Scientific Computing in Nuclear Engineering. Phase 1: Critical Heat Flux Exercise Specificiations. NEA/WKP; 
2023. 
3. 轻水反应堆数据集 bwr。这个模拟数据集展示了在沸水堆（BWR）微核心中的中子学波动和相应
的功率水平变化。 数据集包含九个输入， 包括： 功率整形区区域 （PSZ） 、 主导区区域 （DOM） 、 消失区A 区
域（vanA） 、消失区B 区域（vanB） 、核心进口亚冷却（亚冷却） 、控制棒组位置（CRD） 、冷却剂质量通量
（流量） 、功率密度（功率密度）和窄水隙宽度比（VFNGAP） 。数据集还包含五个输出，包括：有效中子增
殖因子 （K-eff） 、 最大平面平均燃料棒功率峰值因子 （Max3Pin） 、 最大全局燃料棒功率峰值因子 （Max4Pin）、
焓升热通道因子（F-ΔH）和最大径向燃料棒功率峰值因子（MaxFxy）。 
参考文献：Myers PA, Panczyk N, Chidige S, Craig C, Cooper J, Joynt V , et al. pyMAISE: A Python platform for 
automatic machine learning and accelerated development for nuclear power applications. Prog Nucl Energy 
2025;180:105568. 
http://dx.doi.org/10.1016/j.pnucene.2024.105568 
4. 热传导数据集 heat。该数据集来自对热传导问题的一个简单数值解， 使用1.5D 传导方法预测核燃
料中心线温度。该数据集的输入包括七个物理参数：线性热生成率（qprime） 、质量流量率（mdot） 、燃料边
界温度（Tin） 、燃料半径（R） 、燃料长度（L） 、比热容（Cp）和热导率（k） 。该数据集仅包含一个输出—
—燃料中心线温度（T）。 
参考文献：Myers PA, Panczyk N, Chidige S, Craig C, Cooper J, Joynt V , et al. pyMAISE: A Python platform for 
automatic machine learning and accelerated development for nuclear power applications. Prog Nucl Energy 
2025;180:105568. 
http://dx.doi.org/10.1016/j.pnucene.2024.105568 
5. 微反应器数据集 microreactor。高温气冷堆（HTGR）数据集使用 Serpent 对 Holos-Quad HTGR 微
型反应堆进行建模。该反应堆具有氦气冷却和石墨减速功能。按设计，反应堆的最大热功率为22 MWth ，
并通过八个圆柱形、 材料非对称的控制鼓进行控制。 随着这些鼓的旋转， 它们的碳化硼部分达到核心的变动
分数， 从而根据八个鼓的角度调整反应堆内的功率分布。 因此， 该数据集包含八个输入 （鼓角度用thetaN 表
示，其中 N 的范围为 1-8）和四个输出（每个象限的通量，用fluxQN 表示，其中 N 的范围为 1-4） 。每个输
入鼓角度的范围从-180°到 180°。 
参考文献：Price D, Radaideh MI, Kochunas B. Multiobjective optimization of nuclear microreactor reactivity control 
system operation with swarm and evolutionary algorithms. Nucl Eng Des 2022;393:111776. 
http://dx.doi.org/10.1016/j.nucengdes.2022.111776 

<!-- Page 4 -->
6. 功率控制数据集 powery，该数据集使用基于麻省理工学院（MIT）反应堆的 MCNP 模拟结果。它
试图通过其六个控制棒的位置（因此包含六个输入）来预测其22 个燃料元件中的功率（因此包含 22 个输
出） 。输入标记为CBN 的控制叶片，其中 N 的范围为 1-6，输出为每个燃料元件中的功率。 
参考文献：Radaideh MI, Du K, Seurin P, Seyler D, Gu X, Wang H, et al. NEORL: NeuroEvolution Optimization 
with Reinforcement Learning —Applications to carbon -free energy systems. Nucl Eng Des 2023;412:112423. 
http://dx.doi.org/10.1016/j.nucengdes.2023.112423 
https://www.sciencedirect.com/science/article/pii/S0029549323002728 
7. 核安全数据集 rea。该数据集最初由 Bauer 等人提出，旨在使用 PARCS 预测压水堆在发生棒束弹
出事故时的时序数据。数据包含四个输入特征：弹出棒的反应性值（rod_worth） 、延迟中子分数（beta） 、间
隙电导（h_gap）和直接加热分数（gamma_frac） ，以及四个输出特征：最大功率（max_power） 、爆发宽度
（burst_width） 、最大燃料中心线温度（max_TF）和平均出口冷却剂温度（avg_Tcool）。 
参考文献：Bauer H, Finnemann H, Galati A, Martinelli R. Results of LWR Core Transient Benchmarks. 1993 
https://www.semanticscholar.org/paper/Results-of-LWR-Core-Transient-Benchmarks-Bauer-
Finnemann/83eb916d9dbccfa82e83dfd35c87e004490a8213. 
8. 核截面数据集 xs。输入特征（8 个） ： 
FissionFast：快能群裂变截面 
FissionThermal：热能群裂变截面 
CaptureFast：快能群吸收截面 
CaptureThermal：热能群吸收截面 
Scatter11：快能群内散射截面 
Scatter22：热能群内散射截面 
Scatter12：快→热下散射截面 
Scatter21：热→快上散射截面 
输出变量（1 个） ： 
k_infinity：无限介质增殖因数 
参考文献： Radaideh MI, Surani S, O’Grady D, Kozlowski T. Shapley effect application for variance -based 
sensitivity analysis of the few -group cross -sections. Ann Nucl Energy 2019;129:264 –79. 
http://dx.doi.org/10.1016/j.anucene.2019.02.002 
https://www.sciencedirect.com/science/article/pii/S0306454919300714 
