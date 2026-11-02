# 字段差异化规则

## 1. 定位

本文件定义 `deck_spec.json`、逐页文案和页面设计说明中哪些字段必须承载逐页设计决策，哪些字段应作为全局默认下沉，避免机械套版。

本文件是字段差异化清单的唯一真相源；`eval/template_stamp_detection.md` 只引用本文件，不重复维护清单。

## 2. 字段分层

### 2.1 允许重复 / 建议下沉为全局默认

- 基础配色：白底、红黑灰白、红色克制；
- 字体气质；
- 页脚来源格式、页码等正式元素；
- 左右安全边距；
- 全局负面视觉边界；
- 输出格式说明；
- `chart_data` 的结构骨架、键名、列名、节点字段名：允许相似，仅判断语义内容是否机械重复。

### 2.2 必须逐页有设计增量

- `core_judgement`；
- `chart_proof_goal`；
- `chart_visual_boundary`；
- `visual_notes` 或 page_design overrides；
- `speaker_notes`；
- page_copy 中的图表内容、版式说明、讲解口径；
- page_design 中的区域划分、图表区、强调元素、PPTX Builder 注意事项、page_type_gate。

### 2.3 可半重复但必须带差异项

- `page_goal`：可有统一受众目标，但应加入本页特定动作；
- `visual_notes`：可引用全局默认，但必须给出本页主图、主红锚点、布局偏离项；
- `speaker_notes`：可统一“先判断、再证据、后动作”，但必须写明本页先解释什么机制或图形关系。

## 3. core_judgement

### 3.1 规则

- 不得等于 `conclusion`；
- 不得只是固定前缀 + `conclusion`；
- 允许是对 `conclusion` 的提炼、收口或管理化表达，但必须是不同表述，并承载本页唯一带走点；
- 背景页、上下文页不强制增加动作建议，避免为了差异化制造冗余。

### 3.2 FAIL 特征

- 与 `conclusion` 完全相同；
- 仅增加固定前缀，如“本页唯一要带走的判断：”；
- 未形成唯一带走点，只是复述背景信息。

### 3.3 PASS 特征

- 可从 `conclusion` 提炼，但措辞不同；
- 明确高层应该带走的判断；
- 可包含动作、取舍、风险边界或管理含义，但不强制所有页都动作化。

### 3.4 反例

```text
conclusion：复杂度上升导致单点 AI 难以支撑系统级工程决策。
core_judgement：本页唯一要带走的判断：复杂度上升导致单点 AI 难以支撑系统级工程决策。
```

### 3.5 正例

```text
core_judgement：本页要让高层判断，AI 试点不能继续按工具点推进，必须先补工程语义和流程闭环。
```

```text
core_judgement：本页核心判断不是“AI 可用”，而是现有工程流程缺少可被 AI 读取、验证和回写的系统语义底座。
```

## 4. chart_proof_goal

### 4.1 规则

- 必须回答主图证明什么关系；
- 至少命中一类：因果、对比、演进、闭环、分层、决策、权衡；
- 不得只是 `display_text` 的拼接；
- 应与 `chart_semantic_mapping.main_visual_logic` 一致。

### 4.2 FAIL 特征

- 固定前缀 + `display_text` 拼接 + 固定后缀；
- 只说“共同支撑判断”，没有说明支撑关系；
- 看不出主图为什么必须选当前 `chart_type`。

### 4.3 PASS 特征

- 明确图表证明的关系类型；
- 能解释为什么图表不是装饰；
- 能约束主图结构选择。

### 4.4 反例

```text
主图表必须证明：真实系统、语义模型、仿真、AI/XAI 共同支撑该页判断，而不是做装饰。
```

```text
主图表必须证明：样板选择、数据/模型责任、接口标准、审查机制共同支撑该页判断。
```

### 4.5 正例

```text
主图必须证明真实系统数据进入语义模型，经仿真与 AI/XAI 审查后再回写治理，形成自学习闭环；否则该页会退化为静态架构堆栈。
```

```text
主图必须证明四类拍板事项之间存在先后依赖：先定样板边界，再定数据/模型责任，最后固化接口和审查机制；否则会退化为普通任务清单。
```

## 5. 逻辑关系不得退化为清单

### 5.1 规则

当 `chart_proof_goal` 或 `chart_semantic_mapping.main_visual_logic` 声明钻取、因果、门禁、血缘、闭环、决策或权衡关系时，page_design 必须要求主视觉呈现对应关系。不得把关系型页面降级为同权卡片、字段表或指标清单。

### 5.2 反例

```text
title：一条钻取路径把应用慢追到模型、资源池、单卡与 Trace
chart_proof_goal：证明钻取路径可闭环定位慢请求根因。
page_design：主体区使用四个并列卡片，分别列出应用、模型、资源池、Trace 指标；底部写一句“支持全链路钻取”。

判定：FAIL。页面声明钻取路径，但主视觉没有路径、箭头、层级、起点终点或根因定位顺序。
```

```text
title：扩容触发必须先过治理门禁
chart_proof_goal：证明空闲治理、模型优化、调度优化后仍有缺口才进入扩容。
page_design：主体区使用四个同权卡片，分别写空闲治理、模型优化、调度优化、扩容建议。

判定：FAIL。页面声明门禁，但同权卡片没有判断条件、通过/不通过路径，也没有“治理后仍缺口”的门槛。
```

### 5.3 正例

```text
title：一条钻取路径把应用慢追到模型、资源池、单卡与 Trace
chart_proof_goal：证明钻取路径可闭环定位慢请求根因。
page_design：主体区画横向钻取链路：应用 P95 异常 -> Trace 慢 Span -> 模型 Endpoint -> 资源池 -> 节点 -> 单卡；红色只标当前异常路径，右侧保留根因候选和回写动作。

判定：PASS。主视觉呈现起点、路径、层级、异常节点和回写动作，能够证明标题判断。
```

```text
title：扩容触发必须先过治理门禁
chart_proof_goal：证明空闲治理、模型优化、调度优化后仍有缺口才进入扩容。
page_design：主体区画决策门禁树：需求缺口 -> 空闲回收是否满足 -> 模型优化是否满足 -> 调度优化是否满足 -> 扩容立项；每个门禁都有通过/不通过路径和验收口径。

判定：PASS。主视觉明确条件、顺序和通过/不通过路径，卡片不再是同权清单。
```

## 6. chart_visual_boundary

### 6.1 规则

- 必须结合本页 `chart_type` 和 `chart_semantic_mapping.forbidden_visualization`；
- 至少 2 条来自本页图表风险；
- 必须说明该图表不得退化成什么形态；
- 不得多页复用同一组泛化约束。

### 6.2 FAIL 特征

- 多页完全同一组泛化禁令；
- 只写“不得无主次、保留红色锚点”等通用规则；
- 未吸收 `forbidden_visualization` 中的本页专属风险。

### 6.3 PASS 特征

- 明确 `chart_type` 最容易画偏的形态；
- 能约束红色、主次、方向、箭头、层级、表格吞没等问题；
- 与本页标题判断和 `chart_semantic_mapping` 一致。

### 6.4 反例

```text
不得画成无主次的信息堆叠；必须保留唯一主红色锚点；图表必须能解释标题判断。
```

```text
不得做装饰；不得信息过多；必须突出重点。
```

### 6.5 正例

```text
不得把七类 AI 介入点画成七个孤立散点；不得把产品 V 与生产 V 画成互不关联的两套图；红色只用于贯穿双 V 的生命周期主线。
```

```text
不得把自学习数字孪生画成静态三层架构；必须表现真实系统→语义模型→仿真/AI审查→模型回写的闭环箭头；AI/XAI 不得被画成孤立装饰节点。
```

## 7. visual_notes / page_design

- 通用视觉规范应下沉为 `global_design_defaults`；
- 每页 `visual_notes` / page_design overrides 只写本页主图、红色锚点、布局偏离、主次策略、压缩策略；
- 必须保留每页独立可读视图：

```text
page_design_view(Pn) = global_design_defaults + page_design_overrides(Pn)
```

若下游外部模型按“每页完整段落”消费，则输出时应把 `page_design_view(Pn)` 展开为该页完整提示，避免丢失上下文。

## 8. 图表组件字段差异化规则

### 8.1 组件级 chart_proof_goal

- primary 的 `chart_proof_goal` 必须直接证明页面 `core_judgement`；
- supporting 的 `chart_proof_goal` 必须说明它为 primary 提供哪类增量：证据、解释、局部比较、验证或行动收口；
- supporting 目标不得等于 primary 目标；
- supporting 目标不得只是“辅助证明 / 共同支撑 / 补充说明”加 primary 原句；
- supporting 之间不得互为复述、固定前缀替换或关键词换序；
- 若 supporting 无独立增量，应合并进 primary 的 `chart_data` 或删除，不得保留为组件。

### 8.2 组件级 chart_visual_boundary

- 每个组件至少两条边界来自该组件 `chart_type` 的特有误画风险；
- supporting 边界必须包含“不压过 primary”之外的独有图表风险；
- 同页两个及以上组件使用完全相同边界：FAIL；
- 多页 supporting 边界达到混合阈值重复：按模板印章规则 WARN / FAIL。

### 8.3 页内两两比较

对同页组件的 `chart_proof_goal` 和 `chart_visual_boundary` 做两两比较：

- 任意两个 supporting proof goal 全同：FAIL；
- supporting 与 primary proof goal 全同：FAIL；
- 两个组件仅 `chart_type` 不同、证明目标和证据相同：WARN，建议合并；
- 组件数量增加但没有新的证明关系：FAIL，判定为组件堆砌；
- 仅有图标、标签、洞察栏短要点或装饰线，不得登记为 supporting。

### 8.4 允许重复项

- 页面唯一 `core_judgement`；
- 全局配色、页脚、安全区；
- supporting 的 `supports_component_id` 均指向 primary；
- 通用字段骨架和合法枚举；
- Role C 从 primary 派生的兼容主图值。
