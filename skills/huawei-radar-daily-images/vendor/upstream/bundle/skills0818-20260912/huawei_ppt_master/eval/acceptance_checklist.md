# 验收清单

## 1. 内容质量

- 是否有明确汇报对象；
- 是否有总体叙事主线；
- 每页是否有明确核心结论；
- 标题是否为结论型标题；
- 是否有图表建议；
- 是否有页面设计说明；
- 是否有章节分组；
- 是否同时包含问题、判断、路径、风险和建议；
- 是否对高层有决策价值。
- 是否避免空泛口号；

## 2. 华为风格

- 是否克制商务；
- 是否红黑灰白为主；
- 是否工程化表达；
- 是否避免口号化；
- 是否保留页脚、页码 等正式元素。
- 是否版式克制
- 是否信息密度可控；
- 是否图表可执行；
- 是否红色使用克制，单页主红色锚点不超过 1-2 个，辅助红色锚点不超过6个；
- 是否避免正文页厚重红色压底条；
- 是否卡片、表格、流程/闭环图组件风格统一；
- 是否页脚位置、字号、颜色、基线一致。

## 2.x 视觉漂移触发词门禁

- 是否出现暗色/渐变/科技发布会触发词；
- 是否普通封面或章节页使用大面积红/黑；
- 是否 `image_background_section_divider` 被用于高层汇报；
- 是否章节号成为页面最大视觉块；
- 当上述页面级设计与全局华为视觉门禁冲突时，是否主动降级为白底/浅灰底/细红线定锚的工程化版式。

出现以下任一项，必须重写 page_design：

- 未经用户明确要求，普通封面页使用全屏暗色背景、暗红渐变或智算中心大图背景；
- 未经用户明确要求，章节页使用暗红/深灰渐变背景；
- 章节号或红色数字成为页面最大视觉块；
- `image_background_section_divider` 被作为高层汇报默认封面/章节页版式；
- 用“科技感、未来感、提升视觉档次、暗色拓扑”等表述覆盖白底克制华为风格。

## 3. 页面设计

- 是否为每页提供可执行版式说明；
- 是否选用了合适的 `visual_patterns`；
- 是否避免满屏文字；
- 是否说明图表承载的信息；
- 是否可转为 deck_spec.json。

## 4. 主题防污染

- 非 AI 算力主题是否无故出现昇腾、英伟达、CUDA、CANN、GPU/NPU 等词；
- 是否把专属主题结构套用到无关主题；
- 是否符合当前主题的业务语境。

## 5. 不合格条件

出现以下任一项，必须重写：

- 页标题只是名词；
- 无故引入不相关主题术语；
- 大量空泛口号；
- 没有图表建议；
- 页面设计说明不可执行；
- 没有风险或决策收口。
- 页面视觉明显偏重：红色过量、卡片同权、表格过密、底部红条压页面，且未在设计说明中给出降噪策略。

## 6 deck_spec 字段失败条件
出现以下任一项，直接判定 deck_spec 不合格，必须重写：

- `chart_type` 不在 `templates/chart_patterns.md` 枚举内；
- `layout_pattern` 不在 `visual_patterns/layout_library.md` 枚举内；
- `chart_type == layout_pattern`；
- 把 layout 名称写入 `chart_type`；
- 把 chart 名称写入 `layout_pattern`；
- 无精确匹配时直接发明新枚举值。

## 7. 高断言页面证据门禁
- 对于外部格局判断、竞品对比、优势/短板诊断、资源建议等高断言页面：
- 如无公开研究、内部材料或案例支撑，必须使用方向性表述；
- 不得把推测写成已证实事实；
- 必须在 `data_gaps` 中明确缺口；
- 必要时在结论中加入“当前判断”“初步判断”“待补材料后确认”等降级措辞。


## 8. deck_spec 证明契约

- 每页是否包含 `core_judgement`、`chart_proof_goal`、`chart_visual_boundary`；
- `core_judgement` 是否唯一、清晰、可被标题/结论/正文/图表共同支撑；
- `chart_proof_goal` 是否直接服务 `core_judgement`；
- `chart_type` 是否适合证明 `chart_proof_goal`；
- `chart_visual_boundary` 是否具体、可执行，且能防止图表退化为装饰、清单、图片墙、大表格或并列计划。


## 9. 防机械套版门禁

- 是否执行了 `eval/template_stamp_detection.md`；
- 是否在 self_check 中输出重复字段统计、复述检测、骨架填词检测、设计增量检测和允许重复项；
- 是否使用混合阈值模型，而不是固定 `>=3 页`；
- `core_judgement` 是否避免字面复述 `conclusion`，同时允许正当提炼；
- `chart_proof_goal` 是否说明主图证明关系，而非关键词拼接；
- `chart_visual_boundary` 是否逐页结合图表风险和 `forbidden_visualization`；
- `visual_notes` 和 page_design 是否将通用规则下沉为全局默认，并提供每页 overrides；
- `chart_data` 是否只检查语义内容，不因结构键名相似而误判。

### 9.1 清单印章检测

- 是否执行了 `eval/template_stamp_detection.md` 中的清单印章检测；
- 是否在 self_check 中输出清单页占比、连续清单检测、同构版式检测、语义错配检测、逻辑升级豁免和标题换词检测；
- 是否基于 `layout_pattern` 与 `chart_type` 双集并集计算 `is_list_page`，而不是依赖新增字段；
- 清单判定集是否仅使用项目标准枚举，未引入临时版式名或虚构 `chart_type`；
- 当 `N <= 3` 时，是否豁免全 deck 占比限制，仅检查连续重复和语义错配；
- 当 `N >= 4` 时，是否执行 `>40% WARN`、`>55% FAIL` 的清单页占比规则；
- 是否检查连续 3 页清单页 FAIL、连续 4 页同构 `layout_pattern + chart_type` FAIL；
- 是否检查 `chart_proof_goal` 声明复杂关系但 page_design 退化为同权卡片/表格的语义错配；
- 是否对 appendix-heavy、用户明确要求清单版、表格作为辅助证据等例外给出证据。

### 9.2 可见版式术语检测

- 是否执行了 `eval/template_stamp_detection.md` 中的可见版式术语检测；
- 是否只检查页面可见字段，而不是对 page_design / output_contract / terminology_dictionary 做全文 contains；
- 是否检查页面可见文字中不得出现“洞察栏 / 右侧洞察栏 / 右侧洞察 / 主体区 / 图表区 / 底部结论条”等内部版式术语上屏问题；
- 是否重点检测“右侧洞察：xxx”“洞察栏：xxx”“主体区：xxx”“图表区：xxx”“底部结论条：xxx”等组件说明式标题；
- 是否区分“内部设计说明允许出现”和“页面可见文字禁止出现”；
- 是否优先通过删除版式标题或替换为业务语义标题完成修复；
- 是否在 self_check 中输出命中页码、命中文案、所属可见字段、内部说明豁免证据和修复方式。

出现以下任一项，必须重写：

- 模板印章检测出现 FAIL；
- `core_judgement` 等于 `conclusion` 或固定前缀 + `conclusion`；
- `chart_proof_goal` 只是固定前缀 + 关键词拼接 + 固定后缀，未说明关系；
- `chart_visual_boundary` 在混合阈值模型下触发重复 FAIL；
- page_design 的本页红色锚点、图表区、page_type_gate 在混合阈值模型下触发重复 FAIL。
- 正文页连续 3 页及以上被判定为清单页；
- `N >= 4` 且清单页占比 > 55%，且不是明确 appendix-heavy 或用户指定清单版；
- `chart_proof_goal` 声明钻取、因果、门禁、血缘、闭环、决策或权衡关系，但 page_design 只有同权卡片或表格；
- 标题不同但 5 页及以上使用高度相似的 `layout_pattern + chart_type` 和主体结构；
- `chart_visual_boundary` 明确禁止清单化，但 page_design 仍以清单/卡片/表格作为唯一主体；
- 为通过清单检测而创造新的非标准 `layout_pattern` 或 `chart_type`。
- 页面主标题、副标题或一级模块标题中出现内部版式术语；
- 页面可见文字出现“右侧洞察：xxx”“洞察栏：xxx”“主体区：xxx”“图表区：xxx”“底部结论条：xxx”等组件说明式标题；
- 全 deck 有 2 页及以上出现内部版式术语上屏；
- 连续 2 页出现相同的组件说明式标题模式；
- 仅通过缩小字号、降低透明度、移动位置、拆分换行规避检测，而没有删除或替换版式术语。


## 10. chart_data 字段可见性门禁

- `chart_data` 中 logic-only 字段是否未作为可见标签上屏，包括 `group`、`emphasis`、`source_status`；
- 若需要可见分组标题，是否使用 `label`、`name`、`headline`、`display_text`、`lane.name`、`layer.name` 或 `stage.name`，而非复用 `group`；
- `edges.label` 是否仅承载短动作词或短关系词；
- 复杂方向、同层对应、层级支撑、闭环回写等关系语义是否进入 `chart_semantic_mapping`；
- `label` / `name` / `headline` / `items` / `edges.label` 是否短语化，长解释是否放入 `description`、`speaker_notes` 或 `chart_semantic_mapping`；
- `chart_data` 内是否未新增 `relation_type`、`edge_style`、`position`、`anchor`、`x/y`、`layer_index` 等关系或渲染 DSL 字段。

出现以下任一项，必须重写：

- `group`、`emphasis`、`source_status` 等 logic-only 字段被字面上屏；
- `edges.label` 被写成长句或复杂关系解释；
- 复杂关系语义只塞进 `label`，未进入 `chart_semantic_mapping`；
- `chart_data` 内出现 `relation_type` 或坐标/shape/edge_style 等 DSL 字段。

## 11. 图表组件合同门禁

- 新输出是否以 `chart_components` 为唯一图表事实源；
- 是否与顶层 legacy 主图字段混用；
- 是否恰好一个 primary、0~3 个 supporting；
- 每个组件 `component_id` 和 `component_region` 是否同页唯一；
- 每个 role-region 是否命中 `layout_library.md` 兼容表；
- 是否错误使用 `component_region=insight_panel`；
- supporting 是否全部引用 primary，且未使用 `chart_type=none`；
- primary 为 none 时是否不存在 supporting；
- supporting proof goal 是否提供独立增量，而非复述 primary 或其他 supporting；
- 每个组件是否分别满足 chart type、chart data、语义映射和视觉边界规则；
- `bottom` supporting 是否与底部结论条互斥；
- 组件字段是否保持 logic-only。

出现以下任一项，必须 FAIL：

- component 与 legacy 合同混用；
- 多 primary、无 primary、supporting 超过 3 个；
- region 非法、重复或与 layout 不兼容；
- supporting 占用右侧洞察栏；
- supporting proof goal 等于 primary 或同页其他 supporting；
- 组件数量增加但没有证明增量；
- 任一必需组件或 component coverage 丢失。
