# Quality Gate Checklist

## C0 输入门禁

- [ ] 5 个必要输入文件存在
- [ ] `visual_rules.md` 存在；若缺失，已记录 WARNING 并启用最小 fallback
- [ ] `deck_spec.json` 可解析
- [ ] 页码连续且唯一
- [ ] 每页必要字段完整
- [ ] 合同模式唯一：`chart_components` 与历史顶层主图字段未双写
- [ ] 每页恰好 1 个 `primary`、最多 3 个 `supporting`，组件 ID/区域唯一且引用有效
- [ ] `layout_pattern × component_region` 兼容；没有组件使用 `insight_panel`
- [ ] 逐组件 `chart_proof_goal` 已差异化
- [ ] 复杂图表关系语义已解析
- [ ] 任一 ERROR 已阻断 C1/C2，并写入 `return_to_A_required=true`

## C1 渲染合同门禁

- [ ] 每页标题、结论和章节已解析
- [ ] `chart_contract_source`、归一化 `chart_components` 与主图派生投影已解析
- [ ] 每个组件的 `chart_type`、`chart_proof_goal`、语义和区域已解析
- [ ] 可见字段与 `logic-only` 字段已区分
- [ ] `correspondence_pairs` 已保持同层对应
- [ ] `edge_roles` 已保持方向表达
- [ ] 结构化可见内容 coverage 完整
- [ ] `density_budget` 已继承或保守推断
- [ ] 每个组件的 `component_coverage` 完整

## C2 初版生成门禁

- [ ] `source_contract` 未被改写；上屏标题/结论与 effective plan 一致
- [ ] `source_visual_plan`、`effective_visual_plan` 和 `recomposition_audit` 完整
<!-- - [ ] `validate_recomposition.py` 通过 -->
- [ ] 主图与辅助组件分别证明自己的 `chart_proof_goal`，且主辅视觉权重明确
- [ ] `layout_pattern`、`component_region` 与组件内 `chart_type` 未混用
- [ ] 未新增事实
- [ ] 页脚完整

## C2.5 精修门禁

- [ ] `source_contract`、`core_judgement`、事实、证明目标和关系语义未被改写
- [ ] layout/chart/region/copy 变化均来自 effective plan，没有静默漂移
- [ ] 文案调整保留数字、专名、来源、否定词和结论强度
- [ ] 未新增事实、数字、案例、产品名
- [ ] 未删除必需信息
- [ ] 单页主红色锚点不超过 1 个
- [ ] 普通正文页红色面积保持低水平，建议不超过约 5%
- [ ] 普通正文页红色总面积不超过 5%，且只有 1 个主红色锚点、不超过6个辅助红色锚点
- [ ] 卡片统一、边框克制、无重阴影
- [ ] 主图证明路径更清晰
- [ ] 右侧洞察栏未压过主图
- [ ] 右侧洞察栏内没有独立图表组件或 nodes/edges 结构图
- [ ] 右侧洞察栏宽度符合分级规则：普通页 18%-28%，复杂架构/高密度页 25%-32%，不超过 1/3
- [ ] 底部结论条提供增量
- [ ] 底部结论条未与页脚、Logo 或右侧洞察栏形成强视觉竞争
- [ ] 页面未出现“正文区/内容区”等废弃区域术语
- [ ] 底部红线与右侧红线未共同形成 L 型包围感
- [ ] 高密度页面未被静默压薄
- [ ] `required_evidence`、表格关键行列、图表关键节点、图注和来源未被删除
- [ ] 页脚统一弱化
- [ ] 页面无发布会风、咨询海报风、卡通插画风或模板堆砌感

## C3 交付门禁

- [ ] 所有页面分数 `>=92`
- [ ] 无一票失败项
- [ ] 已生成精修报告
- [ ] 已生成 contact sheet
- [ ] 已生成 delivery manifest
- [ ] 已记录 OCR 可见字符数、证据单元数、主体占用率、图表结构复杂度和右侧空壳判断
- [ ] contact sheet 中不存在连续多页重复骨架
- [ ] 语义不变量、重构授权、证据覆盖、关系保真和未记录差异判断均通过
- [ ] effective score 高于 baseline，或 source/effective 无变化
