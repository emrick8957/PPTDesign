# Single Page Refinement Task Prompt

你是角色 C：PPT Builder。

请对当前已生成页面执行一轮整体视觉优化。

## 强约束

必须完全遵守：

- `deck_spec` 当前页；
- 已通过校验的 `effective_visual_plan`；
- `page_design` 当前页；
- `visual_rules`；
- `chart_patterns`；
- `layout_library`；
- `deck_spec_field_dictionary`。

## 语义不变量

- 不改 `source_contract`；
- 不改 `core_judgement`；
- 不改 `chart_proof_goal`；
- 不新增事实、数字、案例、产品名；
- 不删除必需展示信息。

上屏标题、结论、`chart_type` 和 `layout_pattern` 可按已通过校验的 `effective_visual_plan` 变化；不得在精修阶段静默修改。

## 视觉优化目标

在完全遵守上述约束的前提下，使页面更贴近华为 PPT 风格：

- 白底为主；
- 红黑灰白；
- 标题结论先行；
- 主体网格清晰；
- 卡片克制统一；
- 红色锚点唯一；
- 图表证明路径更清晰；
- 右侧洞察栏不压主图；
- 底部结论轻量但有增量；
- 页脚弱化且统一。

## 输出要求

输出优化后的高清 16:9 页面图片。

同时记录：

- 本页保留的内容约束；
- 本页执行的视觉优化；
- 本页是否存在越界风险；
- 本页是否需要后续返工。
