
回归测试用例

## Test 1：AI 算力主题

题目：《昇腾 vs 英伟达：全方位对比与深度洞察》

验证点：必须触发 `ai_compute_ascend_nvidia`，输出体系化对比结构。

## Test 2：公安算力调度主题

题目：《市局/区县 GPU/NPU 算力云化调度方案》

验证点：可同时触发 `ai_compute_ascend_nvidia` 与 `gov_public_security`，但应以市局/区县场景为主线。

## Test 3：智慧园区通用方案

题目：《智慧园区一体化运营平台建设方案》

验证点：不得无故出现昇腾、英伟达、CUDA、CANN、GPU/NPU、模型迁移等词。

## Test 4：数据治理

题目：《企业数据治理体系建设规划》

验证点：应触发 `data_governance`，输出数据标准、质量、资产、价值、路线图，不得套用 AI 算力结构。

## Test 5：客户经营

题目：《客户经营分析与年度增长策略》

验证点：应走通用战略/客户经营结构，不得过度技术化。

## Test 6：网络安全

题目：《网络安全运营中心建设方案》

验证点：应触发 `cybersecurity`，输出安全运营能力框架和建设路线。

## Test 7：项目持续运营

题目：《某项目 2026 年持续运营规划》

验证点：应触发 `project_operation`，输出指标、机制、闭环、风险、年度计划。

## 新增回归用例：
1. 华为云竞争力深度洞察（无外部数据版）
   - 观察是否自动使用方向性表达；
   - 观察 `data_gaps` 是否完整。
2. deck_spec 契约一致性测试
   - 检查 `chart_type` 与 `layout_pattern` 是否混用；
   - 检查 Builder 是否可执行。

3. SWE Atlas 页面图片视觉一致性测试
   - 输入：SWE Atlas 5 页研究报告型 deck_spec / page_design；
   - 检查 P1：高层总览页是否只保留 1-2 个红色锚点，三卡是否统一，底部流程是否细线化；
   - 检查 P2：泳道节点是否统一，右侧洞察栏是否控制为 1 句结论 + 3-4 条短要点；
   - 检查 P3：表格是否弱边框、少高亮，右侧指标卡是否承担结论；
   - 检查 P4：三类失败模式卡片是否有主次，底部结论条是否弱化；
   - 检查 P5：价值闭环是否为 4-5 个短节点，右侧行动建议是否压缩到 3-4 条；
   - 目标：`eval/visual_scorecard.md` 总体评分不低于 85，任一页面低于 80 必须返工。


## Test 8：chart_data 字段可见性

题目：构造 `architecture_flow_diagram`，节点包含 `{"id":"A","label":"产品 V 模型","group":"左支-定义"}`。

验证点：

- 渲染可见文本应包含 `产品 V 模型`；
- 不得出现 `左支-定义` 字面标签；
- `group` 只影响内部归类、布局分组或样式分组。

## Test 9：可见分组标题不用 group

题目：构造需要可见分组标题的架构页，节点包含 `group="model_cluster"`，页面另有 `display_text=["模型底座"]`。

验证点：

- 可见分组标题使用 `display_text` 或 `label/name/headline`；
- 不显示 `model_cluster`。

## Test 10：edges.label 与关系语义归位

题目：构造边 `{"from":"A","to":"B","label":"回写"}`，同时在 `chart_semantic_mapping.main_visual_logic` 描述闭环关系。

验证点：

- `edges.label=回写` 可作为短箭头标签；
- “为什么回写、回写形成什么闭环”必须在 `chart_semantic_mapping`；
- `chart_data` 内不得出现 `relation_type`、`edge_style`、`position`、`anchor`、`x/y`、`layer_index`。

## Test 11：section 只弱显示为页眉

题目：构造带 `section="第二章 路径设计"` 的正文页。

验证点：

- `section` 可作为页眉/章节弱标签；
- 不得作为主体卡片标题、节点标签或图表标签。

## Test 12：同层对应单一事实源（v0.4.2）

题目：构造 V 模型 `architecture_flow_diagram`，在 `chart_semantic_mapping` 内同时写 `correspondence_pairs` 与 `edge_roles.same_level_correspondence`。

验证点：

- 必须 FAIL，提示同层对应只能由 `correspondence_pairs` 承载；
- 修正后：同层对应仅出现在 `correspondence_pairs`，`edge_roles` 只含方向性角色（flow_decompose / flow_integrate / lifecycle_close / feedback_loop）。

## Test 13：edge_roles 边引用结构化与存在性（v0.4.2）

题目：构造 `edge_roles.flow_decompose=["L1->L2"]`（字符串引用），并构造一条引用 `chart_data.edges` 中不存在的边。

验证点：

- 字符串引用必须 FAIL，提示改用结构化 `{"from":<id>,"to":<id>}`；
- 影子边引用必须 FAIL，提示边/节点必须命中 `chart_data` 已存在元素；
- 关系角色名不得反向写回 `chart_data.edges`。
