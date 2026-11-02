# C2.5 Visual Refinement Execution Policy

## 1. 定位

本文件只定义 Role C 的视觉精修执行边界。视觉规范由角色 A 输入包中的 `visual_rules.md` 提供，Role C 不维护第二套视觉规则。

## 2. 规则优先级

1. `deck_spec.json` 页面语义合同；
2. 已通过校验的 `effective_visual_plan`；
3. 输入包中的 `visual_rules.md`；
4. 输入包中的 `page_design.md` 页面级视觉基线；
5. `policies/huawei_visual_gate.md`，仅在输入缺少 `visual_rules.md` 时作为最小 fallback。

有效渲染方案高于视觉基线，但不得覆盖页面语义合同。Role C 不得用固定模板参数覆盖已通过校验的逐页有效方案。

## 3. 允许的视觉精修

- 调整布局对齐、留白、间距、字号、换行和局部层级；
- 调整颜色强弱、边框、线条和视觉锚点；
- 在不改变语义的前提下优化图表节点位置与连线；
- 在不删除证据的前提下调整分栏、卡片组织和图表占比。
- 按已通过校验的 `effective_visual_plan` 执行文案、版式、区域和图表重构。

## 4. 禁止的内容改写

- 不得新增未经 A 确认的事实、数字、案例、产品名或结论；
- 不得删除 `required_evidence`、图表关键节点、表格关键行列、图注或来源；
- 不得改写 `source_contract`、`core_judgement`、证明目标、事实、证据或图表关系语义；
- 不得绕过 C1.5 静默修改 `layout_pattern`、组件区域、`chart_type` 或上屏文案；
- 不得互换主辅组件或修改引用；`insight_panel` 仍不是图表组件区域；
- 不得把 `technical_deep_dive` 降级为中等密度页面；
- 不得用统一骨架覆盖页面级差异。
- 不得通过放大卡片、拉高表格、增加内边距来伪造信息密度；
- 不得把空壳右栏、空壳卡片、低密度表格判为“版式饱满”；
- 不得用大面积空白包装“高层简洁感”；

## 5. 密度保真

- 必须继承渲染合同中的 `density_budget`；
- 高密度模式不得应用中等密度的卡片数、bullet 数和右栏条目上限；
- 过载时优先调整布局、字号、分栏和页型；仍无法承载时返回 A；
- 留白自动分配：须在精修阶段动态计算页面垂直空间。如果内容量偏低（Underfill），禁止让元素紧缩在顶部，必须通过自适应增加行高、增加卡片内边距/外边距，或使用垂直等距分布（Flexbox Space-Between/Space-Around 等价逻辑）将内容拉伸排满页面安全高度区，确保视觉饱满。

## 6. return_to_A 条件

- 页面内容无法在不删减必需证据的情况下排版；
- 输入设计规则互相冲突；
- C0 校验出现 ERROR；
- 关键事实缺失，需要新增内容才能完成页面。

## 7. Fallback

仅在输入缺少 `visual_rules.md` 且 C0 无其他 ERROR 时，允许使用 `policies/huawei_visual_gate.md` 保守生成。必须在报告中记录 fallback 原因。
