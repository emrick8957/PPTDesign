# Visual Recomposition Policy

本文件是 Role C 语义保真视觉重构的单一规则源。`deck_spec.json` 仍是页面语义合同；Role C 只在页面渲染合同内生成有效渲染方案，不回写角色 A 输入。

## 1. 语义不变量

任何重构模式均不得改变：

- `core_judgement`；
- 每个组件的 `chart_proof_goal`；
- 已确认事实、数字、产品名、专业术语、来源和否定/限定词；
- `required_evidence` 及其覆盖；
- `chart_semantic_mapping` 表达的轴、阶段、层级、对应、方向和闭环语义；
- `correspondence_pairs`、`edge_roles`；
- primary/supporting 的证明责任和引用关系；
- `density_budget` 的最低证据密度。

## 2. 重构模式

- `strict_fidelity`：有效渲染方案必须与视觉基线一致，只允许几何和样式微调。
- `adaptive_recomposition`：默认模式；允许在本文件门禁内调整上屏文案、版式、组件区域和图表类型。
- 用户明确要求原版式不变、忠实复刻或只做样式微调时，必须使用 `strict_fidelity`。
- 输入合同缺失、冲突或必须新增语义才能完成页面时，必须 `return_to_A_required=true`。

## 3. 允许的重构

在 `adaptive_recomposition` 下允许：

- 将 source 标题和结论压缩为语义等价的华为式上屏短句；
- 调整分组、顺序、卡片层级、区域比例和阅读路径；
- 替换为合法 `layout_pattern` 并重新映射组件区域；
- 保持 `component_id`、role、proof goal 和引用不变，条件化替换组件 `chart_type`；
- 删除空壳右栏、降低表格权重、增强主证明图；
- 为避免连续多页同骨架，在合法候选中选择不同但等价的视觉方案。

## 4. 文案保真门禁

- `source_contract` 中标题和结论永远保留原文；
- `visible_text_plan` 和 `effective_visual_plan` 可使用优化后的上屏文案；
- 数字、日期、比例、产品名、厂商名、英文专名、来源和否定/限定词必须保留；
- “不、不得、仅、必须、可能、建议”等词不得丢失或反转；
- 不得新增建议、因果、风险、排名、结论强度或事实确定性；
- 所有调整必须写入 `copy_adjustments`；无法确认等价时保留 source 或返回 A。

## 5. layout_pattern 重构门禁

- 目标值必须来自标准 `layout_pattern` 枚举；
- 目标版式必须通过页型门禁；
- 所有有效组件区域必须通过目标版式—区域兼容表且同页唯一；
- `insight_panel` 仍不是图表组件区域；
- 不得因换版式丢失证据、关系线、表格关键行列或来源；
- 不得从无时间语义的页面切换为时间轴，不得从无坐标语义的页面切换为矩阵或趋势布局；
- 跨证明家族的版式替换默认 FAIL。

## 6. chart_type 重构门禁

变更 `chart_type` 必须同时满足：

1. source 与 target 命中下表；
2. `chart_data` 已包含 target 所需全部结构；
3. 不新增节点、边、轴、阶段、排序或层级语义；
4. `chart_proof_goal` 保持不变；
5. `chart_semantic_mapping` 可被目标图表完整表达；
6. 所有 required evidence 进入目标组件；
7. 重构后图表语义得分不得下降。

| source | target | 前置条件 |
|---|---|---|
| `key_findings_cards` | `metric_showcase_grid` | 每个目标项已有确认的 label/value 或 metric，不得伪造数字 |
| `metric_showcase_grid` | `key_findings_cards` | 所有数字、单位和口径完整保留 |
| `case_gallery_cards` | `key_findings_cards` | 每个案例已有 takeaway/proof，来源完整保留 |
| `comparison_table` | `decision_table` | 输入已明确 options、criteria、tradeoff 和 recommendation |
| `layered_stack_diagram` | `architecture_flow_diagram` | 所有 nodes、edges 和方向均已显式存在 |
| `architecture_flow_diagram` | `layered_stack_diagram` | 每个节点已有显式 layer 归属，层间方向不丢失 |

未列出的跨类型转换默认 FAIL。`trend_curve`、`roadmap_timeline_chart`、`quadrant_matrix`、`priority_matrix`、`risk_matrix` 不得由缺少轴、时间、优先级或风险维度的源数据自动生成。

## 7. 候选选择

- 每页保留 baseline，并最多生成 2 个候选；
- 先执行确定性合同校验，再做视觉评分；
- 只有所有硬门禁通过，且版式与结构、华为视觉或重复骨架问题取得明确改善时，才能采用候选；
- 若候选没有明确优于 baseline，保留 baseline；
- 若必须改变语义不变量才能改善，返回 A。

## 8. 重构审计

所有 source/effective 差异必须记录：

- trigger reasons；
- layout、chart type、component region 和上屏文案真实差异；
- 语义不变量结果；
- required evidence coverage；
- layout-region 和 chart target schema 检查；
- baseline/effective score；
- `return_to_A_required`。

任何未进入 `recomposition_audit` 的结构或文案变化均视为未授权漂移。
