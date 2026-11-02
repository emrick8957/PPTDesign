# 字段可见性策略 v0.4.1

## logic-only 字段

以下字段只用于理解和校验，不得作为页面可见文字：

- page_goal
- core_judgement
- chart_proof_goal
- chart_components.component_id
- chart_components.component_role
- chart_components.component_region
- chart_components.supports_component_id
- chart_data.group
- chart_data.emphasis
- chart_data.source_status
- chart_semantic_mapping 中的字段名
- correspondence_pairs 字段名
- edge_roles 字段名
- chart_contract_source
- recomposition_mode
- source_visual_plan
- effective_visual_plan
- recomposition_audit
- copy_adjustments

执行口径：

- logic-only 字段不仅字段名不得上屏，其字段值也不得原文上屏。
- `core_judgement` 永不原文上屏；如需表达，只能由 `title`、`conclusion`、主卡文案或图表关系进行转写。
- `display_text` 是可见字段，但应短语化，每条建议不超过 15 个汉字；不得用 `display_text` 承载讲稿式长句。
- 上述规则逐组件生效；组件合同字段和它们的 logic-only 值不得上屏，只有 `chart_data` 中明确的可见内容字段可以进入页面。

## section 使用规则

section 只能作为页眉/章节弱标签，不得作为：

- 主体卡片标题；
- 节点标签；
- 图表标签；
- 右侧洞察栏标题；
- 底部结论主语。

## 可见字段优先级

页面可见文字只使用：

1. title
2. conclusion
3. label
4. name
5. headline
6. display_text
7. lane.name
8. layer.name
9. stage.name
10. edges.label 的短动作词

## edges.label 规则

edges.label 只能作为短动作词，例如：

- 输入
- 触发
- 验证
- 回写
- 支撑
- 映射
- 汇聚
- 反馈

禁止：

- 长句；
- 复杂因果解释；
- 多层关系说明；
- 把 direction、role、correspondence 文字化。
