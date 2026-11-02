# 生成页面设计说明提示词

请基于已确认大纲和逐页文案，为每页生成页面设计说明。

要求：

1. 从 `visual_patterns/layout_library.md` 中选择版式模式；
2. 说明标题区、主体区、图表区、文字区、强调区、页脚区；其中“正文区”和“内容区”为废弃术语，不得在新输出中使用；
3. 说明图表承载的信息；
4. 说明 PPTX Builder 应如何实现；
5. 如内容过长，标记 need_compression=true；
6. 不改写核心观点。
7. 必须遵守 `templates/visual_rules.md` 的职责边界：视觉规则只管视觉，不改写事实、不解释 deck_spec 字段、不替代评分规则。
8. 每页必须输出视觉降噪约束：
   - `red_anchor`：本页唯一主红色强调点；
   - `card_hierarchy`：卡片强/中/弱层级安排；
   - `spacing_rule`：模块间距、卡片内边距和页脚安全区；
   - `bottom_bar_rule`：是否允许底部结论条，若允许需说明高度和颜色强度；
   - `visual_simplification`：需要弱化或删除的装饰元素；
   - `visual_boundary`：本页需避免的负面视觉风格，如互联网发布会风、咨询海报风、卡通插画风、Excel 报表风；
   - `page_type_gate`：本页页型门禁，如案例页不做图片墙、决策页拍板事项独立突出、路线图必须有阶段门槛、总结页必须形成最终定义。
9. 当页面级设计与 `templates/visual_rules.md` 的全局华为视觉门禁冲突时，必须主动降级页面设计，优先级为：

```text
全局华为视觉门禁 > page_design 局部风格词 > 生成模型审美补全
```

10. 高层汇报默认不使用暗色科技发布会风。除非用户明确要求，page_design 不得输出以下触发词或等价表达：
   - 暗色背景、暗红渐变、深红渐变、冷灰到深红渐变；
   - 科技感背景、futuristic ambience、霓虹、炫光、透视网格；
   - 暗色智算中心拓扑背景、大图背景、背景图压底；
   - 巨大红色章节号、超大章节数字、大面积红色块，黑色块；
   - `image_background_section_divider` 作为普通高层汇报封面或章节页版式。
11. 若原始构想需要“稳重章节页”，应改写为：
   - 白底或极浅灰底；
   - 小号章节编号或细红线定锚；
   - 浅灰工程网格 / 资源池轮廓作为弱背景；
   - 标题黑色，红色只用于短线、标签或关键词。
12. page_design 生成后必须执行视觉漂移触发词自检，并在 self_check 中输出：
   - 是否出现暗色/渐变/科技发布会触发词；
   - 是否普通封面或章节页使用大面积红/黑；
   - 是否 `image_background_section_divider` 被用于高层汇报；
   - 是否章节号成为页面最大视觉块。
13. 每页必须输出“图表组件计划”：
   - 列出唯一 primary 的 `component_id`、`chart_type`、`component_region`、证明目标和视觉边界；
   - 逐个列出 0~3 个 supporting 的 `component_id`、`chart_type`、`component_region`、`supports_component_id`、增量证明目标和降级边界；
   - `component_region` 必须命中 `layout_library.md` 兼容表且同页唯一；
   - 禁止 `component_region=insight_panel`，右侧洞察栏只解释主图；
   - `bottom` supporting 与底部结论条互斥；
   - 无合法区域、组件过多或 supporting 复述 primary 时必须拆页。

输出页面设计说明时，每页至少包含以下字段：

```text
版式模式：
区域划分：
标题区：
图表区：
图表组件计划：
  primary：
  supporting：
  组件阅读顺序：
  版式—区域兼容检查：
文字区：
强调元素：
页脚：
视觉降噪约束：
  red_anchor：
  card_hierarchy：
  spacing_rule：
  bottom_bar_rule：
  visual_simplification：
  visual_boundary：
  page_type_gate：
visual_drift_check：
  dark_or_gradient_trigger：
  large_red_black_area：
  image_background_section_divider_used：
  section_number_dominates：
  conflict_resolution：
PPTX Builder 注意事项：
```
