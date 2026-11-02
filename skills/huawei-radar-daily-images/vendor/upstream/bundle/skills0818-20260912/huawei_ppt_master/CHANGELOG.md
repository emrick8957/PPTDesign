# CHANGELOG

README 中的版本变更详情统一收口到本文件；README 只描述当前能力与使用方式。

## v0.5.1-visual-recomposition-terms

1. 新增视觉基线、有效渲染方案、语义保真视觉重构、严格复刻/自适应重构模式和重构审计术语。
2. 明确 Role A 的 layout/chart/region 是视觉基线，Role C 可在受控模式下生成内部有效方案，但不得回写 deck_spec。
3. 不新增 deck_spec 字段或标准 layout/chart 枚举。

## v0.5.0-chart-components

### 升级目标

允许一页正式声明一个主图表组件与多个辅助图表组件，同时保持右侧洞察栏边界、版式区域兼容和图表合同单一事实源。

### 新增与修改

1. 新增 `chart_components`、`component_id`、`component_role`、`component_region`、`supports_component_id` 正式术语与字段合同。
2. 新合同只权威输出 `chart_components`；顶层主图字段降级为 legacy 兼容，由角色 C 从唯一 `primary` 机器派生。
3. 新增 16 种 `layout_pattern × component_region` 硬兼容表；`insight_panel` 永不作为组件区域。
4. 新增逐组件 `chart_proof_goal` / `chart_visual_boundary` 差异化门禁，以及主辅引用、数量、`none` 和底部区域冲突规则。
5. 同步生成提示词、输出合同、验收清单、视觉评分与模板印章检测。

### 边界

1. 每页恰好一个 `primary`，最多三个 `supporting`。
2. 右侧洞察栏仍只解释主图，不承载独立图表组件或 nodes/edges 结构图。
3. 不新增 `layout_pattern` 或 `chart_type` 枚举。

## v0.4.6-frontier-radar-daily-theme

### Upgrade target

Add `frontier_radar_daily_deep_read` conditionally-triggered domain profile and methodology pattern, so daily tech-signal deep-read PPTs can stably reproduce the Background / Catalyst / Application / Trends four-segment structure validated across 0614, 0615, and 2026-06-02 deliveries.

### New

1. `domain_profiles/frontier_radar_daily_deep_read.md`: Conditionally-triggered theme package with 9 sections: positioning, trigger conditions (with "radar" and "signal" ambiguity guards), fixed 10-page structure, layout/chart mapping, Catalyst/Application required semantics, expression rules, visual rules, and fact boundaries.
2. `methodology_patterns/frontier_radar_daily_deep_read_patterns.md`: Methodology pattern with core pipeline, signal selection rules, Catalyst/Application pairing rules, trend page quadrant framework, action closure rules, anti-degeneration rules, and reuse levels.

### Modified

1. `core/topic_router.md`: Added `frontier_radar_daily_deep_read` routing entry and anti-misuse rules for "radar hardware" and "signal processing" disambiguation.
2. `eval/reference_learning_regression.md`: Added section 7 specialized regression with 8 mandatory checks and 7 failure signals.
3. `VERSION.md`, `CHANGELOG.md`, `INDEX.md`, `PACKAGE_MANIFEST.md` synchronized.

### Boundary

1. No new deck_spec fields added.
2. No new `layout_pattern` / `chart_type` enums added; all mappings reuse existing enums.
3. Theme package only activates on explicit user request; "radar" and "signal" terms in engineering contexts do not trigger it.
4. Screenshot/sample content used only for structure/expression learning, not as factual sources.

## v0.4.5-visible-layout-terms-gate

### 升级目标

在 v0.4.4 视觉冲突优先级基础上，补齐 Role A 侧可见版式术语门禁，防止“右侧洞察：xxx”“洞察栏：xxx”“主体区：xxx”“图表区：xxx”“底部结论条：xxx”等内部版式术语进入页面可见文案。

### 新增

1. `eval/template_stamp_detection.md`：新增可见版式术语检测，只检查页面可见字段，不对 page_design、output_contract、terminology_dictionary 等内部说明做全文 contains。
2. `eval/acceptance_checklist.md`：防机械套版门禁新增可见版式术语检测验收项和一票重写条件。
3. `SKILL.md`：版本升级为 `0.4.5-visible-layout-terms-gate`，模板印章自检输出新增可见版式术语检测。

### 修改

1. 明确内部设计说明允许使用“右侧洞察栏 / 主体区 / 图表区 / 底部结论条”等版式术语，但页面可见字段不得输出组件说明式标题。
2. 失败处理要求删除或替换可见版式词，不得通过字号、透明度、位置或拆分换行规避。
3. `README.md`、`VERSION.md`、`PACKAGE_MANIFEST.md` 同步版本与资产说明。

### 边界

1. 不新增 deck_spec 字段，不新增 `layout_pattern` / `chart_type` 枚举。
2. 不修改 Role C 主流程，不做关键词兜底替换。
3. 不做全文禁词扫描，仅检测最终可能进入页面画布的可见字段。
4. 模板规范说明页、结构分析附录页和内部设计说明可保留版式术语，但必须在 self_check 中说明豁免证据。

## v0.4.4-visual-conflict-priority

### 升级目标

在 v0.4.3 清单印章检测基础上，补齐 Role A 侧视觉冲突优先级，防止 page_design 中的暗色背景、暗红渐变、大字号红色章节号、`image_background_section_divider` 等局部风格词覆盖全局华为高层汇报风格门禁。

### 新增

1. `templates/visual_rules.md`：新增视觉冲突优先级，固定为“全局华为视觉门禁 > page_design 局部风格词 > 生成模型审美补全”。
2. `prompts/generate_page_design.md`：新增暗色/渐变/科技发布会触发词禁用、自检要求和 `visual_drift_check` 输出项。
3. `eval/template_stamp_detection.md`：新增视觉漂移印章检测，识别暗红渐变章节页、巨大红色章节号和暗色科技封面的重复骨架。

### 修改

1. `SKILL.md`：版本升级为 `0.4.4-visual-conflict-priority`，自检输出新增视觉漂移印章检测。
2. `eval/acceptance_checklist.md`：新增视觉漂移触发词门禁及一票重写条件。
3. `README.md`、`VERSION.md`、`INDEX.md`、`QUICK_INDEX.md`、`PACKAGE_MANIFEST.md` 同步版本与资产说明。

### 边界

1. 不新增 deck_spec 字段，不引入渲染 DSL。
2. 不禁止用户明确要求的暗色发布会风，但必须在自检中记录用户显式要求。
3. 默认高层汇报封面和章节页应主动降级为白底 / 极浅灰底 / 细红线定锚 / 工程化浅灰结构。

## v0.4.3-list-stamp-detection

### 升级目标

在 v0.4.2 关系角色基础上，补齐 Role A 侧“页面骨架套版”门禁，解决复杂关系被大量压成指标清单、表格清单和同权卡片矩阵的问题。

### 新增

1. `eval/template_stamp_detection.md`：新增清单印章检测，使用标准 `layout_pattern` 与 `chart_type` 双集并集临时计算 `is_list_page`，识别连续清单页、同构版式、标题换词但结构不变和语义错配。
2. `core/field_differentiation_rules.md`：新增“逻辑关系不得退化为清单”的 2 反例与 2 正例，标定钻取路径、扩容门禁等关系型页面的 PASS/FAIL。

### 修改

1. `SKILL.md`：版本升级为 `0.4.3-list-stamp-detection`，模板印章自检输出新增清单印章检测。
2. `eval/acceptance_checklist.md`：防机械套版门禁新增清单印章检测验收项和一票重写条件。
3. `README.md`、`VERSION.md`、`INDEX.md`、`QUICK_INDEX.md`、`PACKAGE_MANIFEST.md` 同步版本与资产说明。

### 边界

1. 不新增 deck_spec 字段，不引入 `visual_structure_family`。
2. 不新增渲染 DSL，不恢复 `page_render_spec` / `normalized_render_model`。
3. 清单判定集只使用项目标准枚举，不允许为通过检测而创造新的 `layout_pattern` 或 `chart_type`。
4. 对 `N <= 3` 小包、appendix-heavy 和用户明确要求清单版保留豁免。

## v0.4.2-relation-roles

### 升级目标

在 v0.4.1 chart_data 字段可见性基础上，解决高语义风险关系图（双分支 / 同层对应 / 层级支撑 / 闭环，如 V 模型）的"关系可消费性"问题：关系语义只写在散文里，角色 C 读不动、无法落成几何，导致同层对应被画成发散/交叉连线、对应标签丢失。

### 新增

1. `core/deck_spec_field_dictionary.md` §4.7：在 `chart_semantic_mapping` 内新增两个可选语义级字段——`correspondence_pairs`（同层对应唯一事实源）与 `edge_roles`（方向性边按语义角色归组，边引用为结构化 `{from,to}`）。

### 修改

1. `SKILL.md`：版本升级为 `0.4.2-relation-roles`，新增关系角色硬规则（同层对应单一事实源 + edge_roles 边引用结构化与存在性）。
2. `core/output_contracts.md`：deck_spec 强门禁新增第 22、23 条。
3. `prompts/deck_spec_generation.md`：生成检查新增关系角色输出与一致性校验项。
4. `templates/chart_patterns.md`：`architecture_flow_diagram` / chart_data 可见性边界处补充关系角色承载指引。
5. `eval/visual_scorecard.md`：新增 P 章节与一票降级项（同层对应退化、双写、字符串/影子边引用、角色名回写）。
6. `eval/regression_cases.md`：新增 Test 12（同层对应单一事实源）、Test 13（边引用结构化与存在性）。
7. `README.md`、`VERSION.md`、`INDEX.md`、`QUICK_INDEX.md`、`PACKAGE_MANIFEST.md` 同步版本与资产说明。

### 边界

1. 不恢复 `page_render_spec` / `normalized_render_model`，不新增渲染 DSL。
2. 新增枚举只出现在 `chart_semantic_mapping`，不回写 `chart_data`；`chart_data` 内仍禁止 `relation_type`、`edge_style`、`position`、`anchor`、`x/y`、`layer_index`。
3. 字段可选、向后兼容，仅高语义风险关系图建议输出。

### 已知留项（P3，本版未处理）

- R-03：`edge_roles` 角色受控词表未闭合（仍为"取自"，非强制 enum）。
- R-04：回归仅覆盖两个 P2 对应项，未做全量补强。
- R-05：角色 C 在项目外，结构化枚举收益依赖 C honor `chart_semantic_mapping`；未强制"即使输出结构化枚举也必须保留 `forbidden_visualization` 兜底散文"。
- 后续以独立小补丁跟进。

## v0.4.1-chart-data-visibility

### 升级目标

新增 `chart_data` 字段可见性门禁，解决角色 C 将 `group` 等逻辑字段字面渲染为可见标签、以及复杂关系语义被错误塞入 `label` 或新增关系字段的问题。

### 修改

1. `SKILL.md`：版本升级为 `0.4.1-chart-data-visibility`，强制读取 `core/deck_spec_field_dictionary.md`，并在 deck_spec/chart_type 硬规则中加入 chart_data 可见性约束。
2. `core/deck_spec_field_dictionary.md`：新增“chart_data 字段通则与可见性约定”，定义拓扑/管道字段、显示内容字段、logic-only 字段、可见分组标题、`edges.label` 边界、短语化判据和关系语义承载位置。
3. `core/output_contracts.md`：deck_spec 强门禁新增 logic-only 字段不上屏、可见分组标题字段、`edges.label` 短动作词、禁止关系/渲染 DSL 字段。
4. `templates/chart_patterns.md`：补充 chart_data 字段可见性边界，要求复杂关系语义进入 `chart_semantic_mapping`。
5. `prompts/deck_spec_generation.md`：生成检查新增 logic-only、可见分组、`edges.label`、短语化和 DSL 禁止项。
6. `eval/acceptance_checklist.md`、`eval/regression_cases.md`、`eval/visual_scorecard.md`：同步新增字段可见性验收、回归与一票降级项。
7. `README.md`、`VERSION.md`、`INDEX.md`、`QUICK_INDEX.md`、`PACKAGE_MANIFEST.md` 同步版本与资产说明。

### 边界

1. 不恢复 `page_render_spec` / `normalized_render_model`。
2. 不新增 PPTX 渲染 DSL、shape plan 或 C 端渲染协议。
3. 不在 `chart_data` 内新增 `relation_type`、`edge_style`、`position`、`anchor`、`x/y`、`layer_index` 等关系或渲染字段。
4. `chart_data` 仍只承载拓扑和可见内容；复杂关系语义由 `chart_semantic_mapping` 承载。

## v0.4.0-anti-template-stamp-gate

### 升级目标

新增防机械套版门禁，解决交付物“结构合法但字段机械重复、缺少逐页设计决策”的问题，避免下游生图或 PPTX Builder 被重复 `visual_notes`、`chart_visual_boundary`、`speaker_notes` 等字段误导。

### 新增

1. `core/field_differentiation_rules.md`：字段差异化单一真相源，定义允许重复字段、必须逐页有设计增量字段、可半重复字段，以及 `core_judgement` / `chart_proof_goal` / `chart_visual_boundary` 的 PASS/FAIL 特征和正反例。
2. `eval/template_stamp_detection.md`：模板印章检测门禁，使用 N<=3 两两比较、N>=4 `repeat_threshold=max(3,ceil(N*0.5))` 的混合阈值模型，并要求 self_check 输出重复字段统计、复述检测、骨架填词检测、设计增量检测和允许重复项。

### 修改

1. `SKILL.md`：版本升级为 `0.4.0-anti-template-stamp-gate`，强制读取字段差异化规则和模板印章检测，并将模板印章检测纳入自检门禁。
2. `core/output_contracts.md`：增加字段差异化要求和 deck_spec 强门禁。
3. `prompts/deck_spec_generation.md`：要求生成后执行模板印章检测，并在 self_check 输出检测结果。
4. `eval/acceptance_checklist.md`：新增防机械套版验收门禁。
5. `eval/visual_scorecard.md`：新增模板印章一票降级项。
6. `templates/visual_rules.md`：新增通用视觉规则下沉要求与每页独立可读视图。
7. `templates/wording_rules.md`：新增防骨架填词规则。
8. `README.md`、`VERSION.md`、`INDEX.md`、`QUICK_INDEX.md`、`PACKAGE_MANIFEST.md` 同步版本与资产说明。

### 边界

1. 不恢复 `page_render_spec` / `normalized_render_model`。
2. 不新增 PPTX 渲染 DSL、shape plan 或 C 端渲染协议。
3. 不要求所有字段都差异化；页脚、基础配色、安全边距、全局负面风格边界等可以保持一致。
4. `chart_data` 的结构骨架、键名、列名、节点字段名允许相似，仅判断语义内容是否机械重复。

## v0.3.9-chart-semantic-mapping

### 升级目标

新增 `chart_semantic_mapping`，补齐 `chart_type` 与 `chart_proof_goal` 之间的图表语义解释层，尤其解决 `trend_curve` 等图表“看起来有趋势、实际无法证明判断”的问题。

### 新增

1. `core/output_contracts.md`：deck_spec 增加 `chart_semantic_mapping` 字段说明、示例和触发门禁。
2. `prompts/deck_spec_generation.md`：要求 `trend_curve` 必须输出 `chart_semantic_mapping`，高语义风险图表建议输出。
3. `templates/chart_patterns.md`：新增 `chart_semantic_mapping` 语义解释映射规则、六个核心字段和 `trend_curve` 示例。
4. `eval/visual_scorecard.md`：新增 v0.3.9 图表语义映射检查与一票降级项。
5. `core/deck_spec_field_dictionary.md`：补充 `chart_semantic_mapping` 字段说明。

### 修改

1. `SKILL.md` 版本升级为 `0.3.9-chart-semantic-mapping`。
2. `README.md`、`VERSION.md`、`INDEX.md`、`QUICK_INDEX.md`、`PACKAGE_MANIFEST.md` 同步版本与资产说明。

### 边界

1. 本版本只增强 deck_spec 语义证明能力。
2. 不恢复 `page_render_spec` / `normalized_render_model` 方案。
3. 不新增 PPTX 渲染 DSL、shape plan 或 C 端渲染协议。
4. `chart_semantic_mapping` 必须服务 `chart_proof_goal`，不得另起一套判断。

## v0.3.8-deck-spec-field-dictionary

### 升级目标

将 `deck_spec.json` 的字段说明沉淀为正式交付物支持资产，解决角色 C 对字段职责、使用方式和渲染边界理解不一致的问题。

### 新增

1. `core/deck_spec_field_dictionary.md`：新增 deck_spec 字段字典，包含三段核心内容：文件定位、顶层字段、slide 字段。

### 修改

1. `README.md`：保持原有结构，刷新项目当前状态、v0.3.8 说明、推荐调用方式和角色 C 边界。
2. `VERSION.md`：升级到 `v0.3.8-deck-spec-field-dictionary`。
3. `INDEX.md`：补充 deck_spec 字段字典资产。
4. `PACKAGE_MANIFEST.md`：补充 `core/deck_spec_field_dictionary.md` 并同步版本。
5. `SKILL.md`：版本号同步为 `0.3.8-deck-spec-field-dictionary`。

### 边界

1. 本版本不继续推进 `page_render_spec` / `normalized_render_model` 方案。
2. 本版本不新增 PPTX 渲染 DSL、shape plan 或 C 端渲染协议。
3. 本版本不改变默认生成链路和 deck_spec 现有字段，仅补充字段字典说明。

## v0.3.7-deck-spec-proof-contract

### 升级目标

将 deck_spec 从“描述页面内容与图表类型”升级为“明确本页唯一判断、图表证明目标和图表视觉边界”的证明契约，解决 chart_type 合法但图表论证无力的问题。

### 新增

1. `core/output_contracts.md`：deck_spec 每页新增 `core_judgement`、`chart_proof_goal`、`chart_visual_boundary` 字段与检查规则。
2. `prompts/deck_spec_generation.md`：要求先生成 `core_judgement`，再生成 `chart_proof_goal`，最后选择 `chart_type` / `layout_pattern`。
3. `core/generation_workflow.md`：同步 Step 6.5 deck_spec 字段映射检查顺序。
4. `templates/chart_patterns.md`：新增 deck_spec 图表证明契约，给出常见 chart_type 的 proof_goal 示例与 visual_boundary 示例。
5. `eval/visual_scorecard.md`：新增 v0.3.7 deck_spec 证明契约检查与一票降级项。
6. `eval/acceptance_checklist.md`：新增 deck_spec 证明契约验收项。

### 修改

1. `SKILL.md` 版本升级为 `0.3.7-deck-spec-proof-contract`。
2. `README.md`、`INDEX.md`、`PACKAGE_MANIFEST.md`、`VERSION.md` 同步版本与资产说明。

### 兼容性

v0.3.7 不新增 chart_type 或 layout_pattern 枚举，不改变默认交付链路；仅新增 deck_spec 证明字段和图表论证门禁。

## v0.3.6-visual-rules-refactor

### 升级目标

基于用户提供的 `visual_rules_v0.2.md`，将 `templates/visual_rules.md` 从增量规则堆叠重构为“专职视觉设计指导资产”，明确职责边界，并保留 0517 多行业模板、v0.3.3 视觉一致性、v0.3.4 视觉语义、v0.3.5 生成图片反馈规则的历史沉淀。

### 新增

1. `templates/visual_rules.md` 新增明确职责边界：只管视觉风格、色彩、版式、字体、间距、卡片、图表形态、红色锚点、页脚、安全区和负面视觉禁止项；不承担事实校验、deck_spec 字段解释、生成流程控制、评分规则、证据溯源、文案改写。
2. `templates/visual_rules.md` 新增完整视觉规则主干：总体视觉定位、色彩角色、页面区域、字体层级、红色纠偏、卡片模块、图标线条、图表视觉语义、右侧洞察栏、底部结论条、图片素材、特殊页型门禁、负面视觉风格总表、视觉自检清单、优化优先级和默认推荐样式。
3. `templates/visual_rules.md` 新增历史沉淀兼容说明，保留 0517 与 v0.3.5 核心边界。
4. `prompts/generate_page_design.md` 新增 `visual_boundary` 与 `page_type_gate` 字段要求。
5. `core/output_contracts.md`、`core/generation_workflow.md` 同步页面设计说明输出字段。
6. `eval/visual_scorecard.md` 新增 v0.3.6 视觉风格边界扣分/降级项。

### 修改

1. `SKILL.md` 版本升级为 `0.3.6-visual-rules-refactor`。
2. `README.md`、`INDEX.md`、`PACKAGE_MANIFEST.md`、`VERSION.md` 同步版本与资产说明。

### 兼容性

v0.3.6 不改变 deck_spec 字段枚举、不改变默认交付链路、不改写事实与文案规则；仅强化视觉资产边界、页面设计字段和视觉自检门禁。

## v0.3.5-generated-image-feedback

### 升级目标

基于生成 PPT 图片 `project/PPT_image/AI4MBSE_自动化生产系统` 与华为模板 `tmp/PPTTemplate/0517` 的对标结果，沉淀“生成图片反馈 → Skill 资产迭代”的通用规则，解决正文页红色底座过重、卡片平均主义、框架/案例/决策页论证力不足等问题。

### 新增

1. `templates/visual_rules.md` 新增正文页红色底座控制规则、多卡片主次层级规则。
2. `visual_patterns/layout_library.md` 新增阅读框架页、案例证明页、决策建议页、路线图阶段门槛、总结页最终定义等页面角色语义约束。
3. `templates/chart_patterns.md` 新增 `case_gallery_cards`、`decision_table`、`capability_map`、`layered_stack_diagram`、`roadmap_timeline_chart` 的失败条件与降级建议。
4. `templates/wording_rules.md` 新增长标题压缩规则、总结页最终定义规则。
5. `eval/visual_scorecard.md` 新增生成图片反馈一票降级项。

### 修改

1. `SKILL.md` 版本升级为 `0.3.5-generated-image-feedback`。
2. `README.md`、`INDEX.md`、`PACKAGE_MANIFEST.md`、`VERSION.md` 同步版本与资产说明。

### 边界

不沉淀 AI4MBSE 主题事实、论文术语、客户/产品/案例名、未经核验数字；仅沉淀跨主题复用的视觉语义、页面角色、图表失败条件与评估门禁。

## v0.3.4-visual-semantics

### 升级目标

基于 AI_MBSE P1-P7 页面图片评审，将“页面结构正确但图表没有讲透结论”的共性问题沉淀为核心可复用规则，强化红色锚点语义、卡片工程化层级、版式语义有效性、图表论证力和强判断标题支撑。

### 新增

1. `templates/visual_rules.md` 新增页面图片生成后的红色锚点判定、工程化卡片层级、底部结论条增量规则。
2. `visual_patterns/layout_library.md` 新增关键版式语义约束：四象限坐标有效性、右侧洞察栏约束、三栏并列/链路判断、两列对比表格转面板规则。
3. `templates/chart_patterns.md` 新增图表语义失败条件与降级规则，覆盖 `quadrant_matrix`、`architecture_flow_diagram`、`gap_heatmap`。
4. `templates/wording_rules.md` 新增强判断标题支撑规则与抽象概念定义规则。
5. `eval/visual_scorecard.md` 新增图表论证力加严项与图表语义一票降级项。

### 兼容性

v0.3.4 不改变默认交付链路和 deck_spec 字段，仅增强页面图片/PPTX 生成后的视觉语义与论证质量门禁。

## v0.3.3-visual-consistency

### 升级目标

根据 SWE Atlas 页面图片与华为风格 PPT 模板对比结果，补齐视觉资产之间的一致性规则，解决“结构正确但视觉偏重”的问题。

### 新增

1. `templates/visual_rules.md` 增加华为式视觉降噪规则：红色锚点预算、底部结论条克制、卡片层级、留白安全区、页脚一致性。
2. `visual_patterns/layout_library.md` 增加 layout 通用区域比例、右侧洞察栏宽度、底部结论条使用条件和禁用组合。
3. `templates/chart_patterns.md` 增加 `key_findings_cards`、`comparison_table`、`swimlane_process`、`value_chain_loop` 的组件级视觉约束。
4. `eval/visual_scorecard.md` 增加视觉降噪与华为风格一致性评分项和一票降级项。
5. `prompts/generate_page_design.md` 增加 `red_anchor`、`card_hierarchy`、`spacing_rule`、`bottom_bar_rule`、`visual_simplification` 输出要求。
6. `eval/regression_cases.md` 增加 SWE Atlas 页面图片视觉一致性回归用例。

### 修改

1. `SKILL.md` 升级到 v0.3.3，并增加视觉一致性硬规则。
2. `core/output_contracts.md` 与 `core/generation_workflow.md` 同步页面设计视觉降噪字段，保证输出契约与生成流程一致。
3. `visual_patterns/executive_summary_patterns.md`、`architecture_page_patterns.md`、`comparison_page_patterns.md`、`risk_decision_patterns.md` 同步增加 SWE Atlas 类页面优化模式。
4. `eval/acceptance_checklist.md`、`README.md`、`QUICK_INDEX.md`、`INDEX.md`、`PACKAGE_MANIFEST.md`、`VERSION.md` 同步更新，保证系统资产一致性。

### 兼容性

v0.3.3 不改变内容生成链路与交付物类型，只增强页面设计说明、deck_spec/Builder 输入和生成图片的视觉一致性约束。

## v0.3.2-consistency-fix

### 修复目标

修复剩余的 deck_spec 输出触发条件歧义、生成流程优先级表述不完整，以及 default_general 默认结构易被误读的问题。

### 修复

1. 调整 `core/output_contracts.md`，明确默认全套交付链路下也应输出 `deck_spec.json`。
2. 调整 `core/generation_workflow.md`，明确用户当前明确偏好优先于沉淀规则复用。
3. 调整 `domain_profiles/default_general.md`，明确默认结构块不等于固定页数，实际页数遵循 `SKILL.md`。

### 兼容性

v0.3.2 不改变 Skill 的核心能力与交付物类型，仅消除剩余规则歧义并增强执行一致性。

## v0.3.1-conflict-fix

### 修复目标

修复当前 Skill 包内已识别的优先级冲突、任务路由歧义与交付规则不一致问题，并同步放宽角色 A 的工作区写权限边界。

### 修复

1. 调整 `core/reference_ingestion_workflow.md` 的复用优先级，确保“用户当前明确指定偏好”高于已沉淀规则。
2. 调整 `SKILL.md` 的默认说明，明确用户未限制交付范围时默认走全套交付链路。
3. 调整 `SKILL.md` 页面设计默认要求，移除“备选版式”要求，仅保留主版式。
4. 调整 `core/topic_router.md` 与 `domain_profiles/project_operation.md`，移除 `project_operation` 对“项目复盘”的误吸收，避免与 `project_review` 任务类型冲突。

### 兼容性

v0.3.1 保持 v0.3 的参考材料学习能力与全套交付能力，仅修复规则冲突，不改变核心产物类型。

## v0.3.0-reference-learning

### 升级目标

把 `huawei_ppt_master` 从“参考材料辅助生成”升级为“参考材料学习框架”：不仅学习样式、结构、表达习惯，也学习体系、内容套路、论证框架，并通过分层沉淀和专项回归稳定复用。

### 新增

1. 新增 `core/reference_ingestion_workflow.md`，定义 PPT、PPT 图片、模板、文本材料、数据材料的接入、分类、双通道抽取、沉淀落位与冲突处理流程。
2. 新增 `core/reference_material_policy.md`，区分风格参考、结构参考、论证参考与事实依据，防止把截图或样张直接当成事实来源。
3. 新增 `methodology_patterns/`，承载高层论证套路、章节逻辑、页面角色和行业框架抽取规则。
4. 新增 `eval/reference_learning_regression.md`，覆盖视觉学习、结构学习、表达学习、体系学习、主题隔离和增量稳定性回归。

### 修改

1. 修改 `SKILL.md`：新增“参考材料学习与复用”能力定义、触发读取规则和学习自检门禁。
2. 修改 `core/generation_workflow.md`：新增 Step 1.5 参考材料识别与分类，以及 Step 3.5 沉淀结果复用。
3. 修改 `prompts/screenshot_analysis.md`：从只抽取版式扩展为同时抽取页面角色、标题句式、论证结构和页面收口方式。
4. 修改 `core/anti_overfit_rules.md`：新增参考材料学习过拟合控制。
5. 修改 `core/topic_router.md`：新增主题知识包升级条件。

### 兼容性

v0.3 保持 v0.2 的通用华为风格生成能力与主题包隔离规则，同时新增参考材料学习流程。若无参考材料输入，原有生成流程仍可正常使用。

## v0.2

### 升级目标

把 v0.1 从“AI算力/昇腾-NVIDIA 强场景 Skill”升级为“通用华为风格 PPT Skill + 条件触发主题知识包 + 版式截图沉淀库”。

### 新增

1. 新增 `core/` 通用生成内核。
2. 新增 `core/topic_router.md`，用于主题识别和主题知识包条件触发。
3. 新增 `core/anti_overfit_rules.md`，用于避免昇腾/NVIDIA 主题污染其他主题。
4. 新增 `domain_profiles/`，将昇腾/NVIDIA、公安政务、AI平台、持续运营等主题知识拆成可选模块。
5. 新增 `visual_patterns/`，将用户提供的版式截图抽象为可复用页面模式。
6. 新增 `eval/domain_contamination_tests.md`，测试非昇腾主题是否被 AI 算力概念污染。
7. 新增 `prompts/generate_page_design.md`，专门生成页面设计说明。
8. 新增 `prompts/deck_spec_generation.md`，用于生成 PPTX Builder 的结构化输入。

### 修改

1. 修改 `SKILL.md`：将 Skill 定位改为通用华为风格 PPT 生成 Skill。
2. 修改 `templates/wording_rules.md`：移除全局昇腾/NVIDIA 专属表达，只保留通用文案规则。
3. 修改 `templates/narrative_patterns.md`：增加通用战略、技术方案、客户方案、项目复盘、运营治理、数据治理、安全运营等叙事模式。
4. 修改 `templates/chart_patterns.md`：将 AI 算力图表从全局默认迁移到主题包中。
5. 修改 `eval/regression_cases.md`：新增非 AI 算力主题测试用例。

### 保留

1. 保留华为红、黑、灰、白的视觉风格。
2. 保留 页码、封面、目录、Thank you 等正式汇报要素。
3. 保留“结论先行、问题导向、工程化表达、克制商务”的基本原则。

### 移动

1. 将 v0.1 中“昇腾 vs 英伟达默认 18 页大纲”移动到 `domain_profiles/ai_compute_ascend_nvidia.md`。
2. 将 v0.1 中“政务公安、算力调度、持续运营”相关表达拆分到独立主题包。

### 兼容性

v0.2 仍支持《昇腾 vs 英伟达：全方位对比与深度洞察》，但该能力由主题包触发，不再污染通用主题。



