# A/B/C 交接协议

## A → C

A 必须交付：

1. deck_spec.json；
2. page_design.md；
3. visual_rules.md；
4. chart_patterns.md；
5. layout_library.md；
6. deck_spec_field_dictionary.md；
7. 如有：page_visual_contract 或复杂页说明。

A 不应交付像素级绘图 DSL，避免压缩 C 的视觉优化空间。

C1 编译时必须合并：

1. `deck_spec.json` 中的 `global_design_defaults`；
2. 当前页 `visual_notes`、`visual_focus`、`must_highlight`、`need_compression`、`data_gaps`；
3. `chart_semantic_mapping.insight_panel_logic`；
4. `page_design.md` 中的全局默认、页面区域划分、强调元素、角色 C 注意事项和视觉降噪约束。

对于新合同，C1 只以 `chart_components` 为图表事实源，逐组件编译语义与 coverage，并从唯一 `primary` 派生施工用主图投影。若同时出现顶层主图字段、组件区域不兼容、辅助组件进入 `insight_panel` 或引用关系不完整，C 必须停止并返回 A。

页面级显式 override 高于 Role C 内置默认值。Role C 不得用固定模板参数覆盖角色 A 的逐页设计意图。

Role A 的 layout/chart/region 构成视觉基线。Role C 在 `adaptive_recomposition` 下可生成不同的有效渲染方案，但不得回写 A 输入；必须交付 `source_visual_plan`、`effective_visual_plan` 和 `recomposition_audit`。用户明确锁定版式时使用 `strict_fidelity`。

若 A 声明高密度技术汇报，建议逐页提供 `density_budget`。C 必须保留 `required_evidence`、表格关键行列、图表关键节点、图注和来源。

## C → A 返工

出现以下情况时，C 必须写入 `return_to_A_required=true` 并停止当前页或当前包继续生成：

1. C0 输入校验出现 ERROR；
2. 结构化可见内容 coverage 不完整；
3. 页面无法在不删除必需证据的情况下排版；
4. 高密度页面明显 underfill；
5. 关键事实或来源图片缺失，需要新增内容。
6. 视觉改善必须新增轴、阶段、节点、边、因果、时间顺序或其他未确认关系语义。

## C → B

C 必须交付：

1. 页面图片；
2. contact sheet；
3. self_check_report；
4. delivery_manifest；
5. 已知风险说明。
6. 重构模式、source/effective 差异和重构审计。

## B → C

B 的评审意见必须定位到：

- 页码；
- 问题类型；
- 触发门禁；
- 返工优先级；
- 修复建议。

## C 二轮优化

C 按 B 的问题清单定向返工，不改变 deck_spec 事实源。
