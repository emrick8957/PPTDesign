# deck_spec.json 生成提示词

请把已确认的大纲、逐页文案和页面设计说明转换为 `deck_spec.json`。

要求：

1. 输出严格 JSON；
2. 每页包含 slide_no、type、title、conclusion、core_judgement、layout_pattern、chart_components、display_text、speaker_notes、need_compression；
3. 不新增事实；
4. 不改写结论；
5. 版式模式必须来自 `visual_patterns/layout_library.md`；
6. 每个组件的图表类型必须来自 `templates/chart_patterns.md`，不得与 `layout_pattern` 混用；
7. 如果页面内容过长，标记 need_compression=true；
8. `visual_notes` 必须吸收页面设计说明中的视觉降噪约束，至少体现：
   - 本页主红色锚点；
   - 卡片强/中/弱层级；
   - 模块间距与页脚安全区；
   - 底部结论条是否允许以及强度；
   - 需要弱化或删除的装饰元素。
9. 每页先生成 `core_judgement`，再生成 primary，选择唯一 `layout_pattern`，最后按合法槽位生成 0~3 个 supporting。
10. 每个组件必须包含独立 `chart_proof_goal` 和 3~5 条 `chart_visual_boundary`；supporting 目标不得复述 primary 或其他 supporting。
11. 每个组件的 `component_region` 必须命中 `layout_library.md` 兼容表且同页唯一；禁止 `insight_panel`。
12. 当任一组件 `chart_type=trend_curve` 时，该组件必须输出 `chart_semantic_mapping`；其他高语义风险图表按原触发规则执行。
13. `chart_semantic_mapping` 继续使用 6 个核心字段：`chart_reading_intent`、`main_visual_logic`、`axis_semantics`、`stage_or_node_meaning`、`insight_panel_logic`、`forbidden_visualization`。
14. 新输出不得包含顶层 `chart_type`、`chart_data`、`chart_proof_goal`、`chart_visual_boundary`、`chart_semantic_mapping`；这些字段仅用于 legacy 输入。
15. `bottom` supporting 与底部结论条互斥；无合法槽位或 supporting 超过 3 个时拆页。

生成时必须检查：

- 正文页不得默认使用厚重红色压底条；
- `comparison_table` 页面必须让表格承担证据，结论通过标题、右侧指标卡或弱结论区呈现；
- `swimlane_process` 与 `value_chain_loop` 的节点、箭头、连接线必须在 `visual_notes` 中说明统一规则；
- 单页主红色视觉锚点不超过 1-2 个，辅助红色强调：允许 3~5 个；高密度页允许4~6个；
- 生成后必须执行模板印章检测，并在 self_check 中输出：重复字段统计、复述检测、骨架填词检测、设计增量检测、允许重复项；
- 重复字段统计必须使用混合阈值模型：N<=3 两两比较，N>=4 使用 `repeat_threshold=max(3,ceil(N*0.5))`；
- `core_judgement` 不能等于 `conclusion`，也不能只是固定前缀 + `conclusion`；但允许对 `conclusion` 做不同表述的正当提炼；
- `chart_proof_goal` 必须说明主图证明的关系类型，不能只是关键词拼接；
- `chart_visual_boundary` 必须优先吸收 `chart_semantic_mapping.forbidden_visualization` 中的本页专属风险；
- `speaker_notes` 必须体现本页讲解顺序差异；
- 如 `visual_notes` 或 page_design 包含通用规范，应拆为 `global_design_defaults + page_design_overrides`，并保留每页独立可读视图。
- `chart_data` 内 logic-only 字段（如 `group`、`emphasis`、`source_status`）不得作为可见标签上屏；
- 若需要可见分组标题，应使用 `label` / `name` / `headline` / `display_text` / `lane.name` / `layer.name` / `stage.name`，不得复用 `group`；
- `edges.label` 只能写短动作词或短关系词，复杂方向、同层对应、层级、闭环语义必须写入 `chart_semantic_mapping`；
- 不得在 `chart_data` 内新增 `relation_type`、`edge_style`、`position`、`anchor`、`x/y`、`layer_index` 等渲染或关系 DSL 字段；
- `label` / `name` / `headline` / `items` / `edges.label` 应短语化，过长时放入 `description`、`speaker_notes` 或 `chart_semantic_mapping`；
- 逐页文案中的“正文模块”必须映射到 `display_text`、`chart_data`、`speaker_notes` 或 `chart_semantic_mapping`，不得输出为 `body` 字段；
- 页型统一使用 `type` 字段，不得另行输出 `page_type`；
- 当主图为双分支 / 同层对应 / 层级支撑 / 闭环类时，应在 `chart_semantic_mapping` 输出 `correspondence_pairs`（同层对应）或 `edge_roles`（方向性边），把同层对应边与顺序流转边显式区分；
- 同层对应只写入 `correspondence_pairs`，不得在 `edge_roles` 内出现 `same_level_correspondence`；
- `correspondence_pairs` 与 `edge_roles` 内所有 id / 边必须引用 `chart_data` 内已存在的节点/边；边引用必须用结构化 `{"from":<id>,"to":<id>}`，不得用 `"from->to"` 字符串；
- 不得把关系角色名写回 `chart_data`；关系角色只存在于 `chart_semantic_mapping`。


## 图表组件证明契约检查

生成 `deck_spec.json` 前必须检查：

- `core_judgement` 是否为本页唯一判断，不能是多个判断拼接；
- primary 的 `chart_proof_goal` 是否直接服务 `core_judgement`；
- 每个 supporting 是否提供独立增量并指向 primary；
- 每个组件的 `chart_type` 是否适合证明自己的 `chart_proof_goal`；
- 每个组件的 `chart_visual_boundary` 是否具体、可执行，且不与页面设计冲突；
- 如已触发 `chart_semantic_mapping`，检查其是否解释该组件如何证明目标，坐标/阶段/节点语义是否成立；
- `component_region` 是否与 layout 兼容、同页唯一且未占用右侧洞察栏；
- 若图表无法证明本页判断，应优先调整 `chart_type` 或拆页，不得用装饰性图表硬凑。
