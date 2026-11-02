> 版本: v1.5 | 最后更新: 2026-06-20 | 维护者: 角色 A (huawei_ppt_master)

# Huawei PPT 术语字典

> 目的：统一 `huawei_ppt_master` 与 `huawei_ppt_builder` 对页面区域、语义合同、渲染合同、版式、图表、视觉门禁和交付物的理解，避免同一术语被不同角色按不同含义执行。
>
> 适用范围：角色 A 生成大纲、文案、页面设计说明和 `deck_spec.json`；角色 C 编译 `page_render_contract`、生成页面图片/PPTX、精修、自检和交付；角色 B 可据此评审术语是否被误用。
>
> 术语优先级：`deck_spec.json` 与字段字典定义事实/语义；`page_design.md` 定义页面级施工意图；`visual_rules.md` 定义视觉默认与负面项；`layout_library.md` 定义页面怎么排；`chart_patterns.md` 定义主图表表达什么关系；`page_render_contract` 是角色 C 的施工编译结果，不是新事实源。

---

## 1. 统一命名原则

| 术语问题 | 统一口径 |
|---|---|
| 右侧观察栏 / 右侧洞察栏 / 右侧栏 / insight panel | 推荐统一写作 **右侧洞察栏**。英文合同字段可使用 `insight_panel`。不得写成“右侧观察栏”后又解释成文字区。 |
| 底部结论条 / 底部收口 / bottom bar / bottom conclusion | 推荐统一写作 **底部结论条**。合同字段可使用 `bottom_conclusion` 和 `bottom_bar_rule`。 |
| 主体区 / ~~正文区~~ / ~~内容区~~ | 推荐统一写作 **主体区**。当需要细分时，再拆成 **图表区** 与 **文字区**。“正文区”和“内容区”已废弃，不得在新输出中使用。 |
| 标题区 / 顶部结论区 | 推荐统一写作 **标题区**。若标题承担判断，可称“结论型标题”，但仍属于标题区。 |
| 页脚区 / footer / 来源区 | 推荐统一写作 **页脚区**。来源、页码、保密标识、版权均属于页脚区或页脚附属信息。 |
| 视觉锚点 / 红色锚点 / red_anchor | 推荐统一写作 **红色锚点**，强调其是单页视觉主强调点，不是装饰色。 |
| 页面类型 / 页型 / type | 推荐统一写作 **页型**。`deck_spec.slides[].type` 与 `page_render_contract.render_intent.type` 表示同一类概念；`page_type` 仅作为历史输入兼容名，不在新合同中输出。 |
| 版式模式 / 布局模式 / layout_pattern | 推荐统一写作 **版式模式**。字段名使用 `layout_pattern`。 |
| 图表类型 / chart_type | 推荐统一写作 **图表类型**。字段名使用 `chart_type`。 |
| 语义合同 / deck_spec | 推荐统一写作 **页面语义合同**，对应 `deck_spec.json`。 |
| 渲染合同 / page_render_contract | 推荐统一写作 **页面渲染合同**，对应角色 C 的编译结果。 |

---

## 2. 页面区域术语

| 术语 | 标准定义 | 边界 / 不是什么 | 角色 A 应写什么 | 角色 C 应如何执行 |
|---|---|---|---|---|
| 页面 | 一张 PPT slide 的完整画布。 | 不是一个模块，也不是一张图表。 | 每页必须有页型、标题、结论、图表/版式选择和视觉约束。 | 按页逐一编译、渲染、自检和返工。 |
| 画布 | 页面物理空间，默认 16:9。 | 不等于主体区。 | 一般不写坐标，只写区域和比例。 | 保证安全区、页脚、标题、主体稳定。 |
| 安全区 | 页面边缘预留留白，防止内容贴边或被页脚/Logo挤压。 | 不是装饰留白。 | 写清左右安全区、上下安全区、页脚安全区、底部结论条避让。 | 默认左右不少于页面宽度 4%，上下不少于页面高度 3%，页脚与主体明显分隔。 |
| 标题区 | 页面上方约 10%-15%，承载章节弱标签、主标题、必要副标题。标题应先形成判断。 | 不承载大段正文；不应使用厚重红色标题栏。 | 写标题区对齐、标题行数、是否需要短红线/细灰线。 | 控制 1-2 行，避免挤压主体区。 |
| 主标题 | 页面第一视觉文字，通常来自 `title`。 | 不等于 `core_judgement` 的原文字段；不应只是主题名。 | 结论型表达，1-2 行。 | 直接上屏，确保层级最高但不过度口号化。 |
| 副标题 | 主标题下或页眉附近的辅助说明。 | 不替代正文；不抢主标题。 | 仅在必要时给出。 | 12-16pt 左右，灰色或弱层级。 |
| 页眉标签 | 表示章节、阶段或类别的弱标签。 | 不得成为主体节点或卡片标题。 | 可来自 `section`，必须弱化。 | 只作为页眉/章节弱标签，不放入主体图表。 |
| 主体区 | 页面中部约 75%-80%，用于承载主图、卡片、流程、对比、架构、案例等证明结构。 | 不包含页脚；不应被底部结论条过度挤压。 | 写清主体区的主图/模块组织和阅读路径。 | 建立网格、主次、对齐和图表证明关系。 |
| 图表区 | 主体区中承载主图表或证明图的区域。 | 不等于 `chart_type`；它是空间区域。 | 说明主图位置、占比、证明目标。 | 让主图证明 `chart_proof_goal`。 |
| 文字区 | 主体区中承载正文短句、解释、卡片文案的区域。 | 不承载长讲稿；长解释进 `speaker_notes`。 | 写短语化正文模块。 | 控制字号、换行、层级和文本密度。 |
| 强调区 | 页面中承载红色锚点、关键数字、风险或决策点的局部区域。 | 不应全页多处散落。 | 指定唯一主红色锚点。 | 若红色超预算，优先降级为灰/黑 + 红关键词。 |
| 右侧洞察栏 | 页面右侧的辅助解释区/结论证据栏，用于解释主图、放关键数字、风险、建议或短要点。 | 不是第二文字区，不是备注列表，不是第二张架构图。 | 写明是否使用、宽度、条目数量、与主图关系。 | 宽度继承输入规则；不超过 1/3；只解释主图。 |
| 底部结论条 | 主体区下方、页脚上方的轻量收口组件，回答“本页证明了什么”。 | 不是页脚，不是装饰条，不重复标题，不放多段 bullet。 | 写明是否允许、高度、颜色强度、是否与右侧洞察栏同时出现。 | 避开页脚和 Logo；默认轻量，红色实底慎用。 |
| 页脚区 | 页面底部 4%-6%，承载页码、保密标识、来源、版权、免责声明。 | 不承载页面结论；不与底部结论条重叠。 | 写页脚弱化和来源规则。 | 位置、字号、颜色、基线全 deck 稳定。 |
| Huawei Logo 区 | 通常位于右下角的品牌标识区域。 | 不应被结论条、页码、图表遮挡。 | 需要避让时写入视觉约束。 | 右下角留出稳定空间，避免重复页码或重合。 |

---

## 3. 视觉组件术语

| 术语 | 标准定义 | 正确使用 | 常见误用 |
|---|---|---|---|
| 红色锚点 | 单页最重要的红色视觉强调点，用于核心判断、关键风险、核心节点、最终输出或阶段门槛之一。 | 每页 1 个主锚点，允许 3~5 个；高密度页允许4~6个且面积须小于主锚点。 | 同页红标题、红编号、红箭头、红卡片、红底栏一起出现。 |
| 主红色视觉锚点 | 红色锚点中的最高优先级元素。 | 绑定 `core_judgement` 或主图关键节点。 | 只因“好看”把多个数字染红。 |
| 辅助红色强调 | 弱于主锚点的小范围红色关键词、细线、小圆点或局部数字。 | 最多 6 个左右，面积小。 | 辅助强调反而比主锚点更醒目。 |
| 窄红线 | 用于标题定锚、模块轻强调或底部轻收口的细线。 | 替代厚重红条。 | 多条红线形成 L 型包围感或装饰感。 |
| 卡片 | 白底或极浅灰底、细灰边的模块容器。 | 承载短标题、短句、关键数字、图标。 | 大圆角、重阴影、玻璃拟态、所有卡片同权。 |
| 主卡 | 页面中承担主判断或主结论的卡片。 | 最多 1 张，视觉强于支撑卡。 | 多张主卡同权，导致无焦点。 |
| 支撑卡 | 支撑主判断的次级卡片。 | 3-5 张常见，层级弱于主卡。 | 每张都有红标题和红图标。 |
| 注释卡 | 低优先级说明、来源、条件或补充信息。 | 浅灰、细字、弱边框。 | 与主卡同权或抢焦点。 |
| 模块 | 页面中的功能性内容块，可由卡片、图表、文字、图片组成。 | 同一页模块之间应有层级或关系。 | 模块只是平均铺满页面。 |
| 主图 | 页面最重要的图表/架构/证明图。 | 服务 `chart_proof_goal`。 | 与右侧洞察栏同权或被洞察栏压缩。 |
| 图表组件 | 页面中具有独立 `chart_type`、结构化数据、证明目标和视觉边界的图表单元。 | 由 `chart_components` 组织；不是页面版式，也不是纯装饰图标。 | 把图标、标签或洞察栏短要点误报为独立图表。 |
| 主图表组件 | `component_role=primary` 的唯一图表组件，承担页面主要证明任务。 | 每页必须且只能有一个；可用 `chart_type=none` 表示无主图表页。 | 与辅助组件同权，或出现两个 primary。 |
| 辅助图表组件 | `component_role=supporting` 的图表组件，用于证据化、解释、局部比较或行动收口。 | 不得形成第二核心判断，不得使用 `chart_type=none`。 | 抢占主图、主红色锚点或另起一套叙事。 |
| 主证明图 | 案例页/证据页中的核心图片、截图或图卡，用于证明标题判断。 | 必须配证明点或标注。 | 图片墙、截图墙、Logo 墙。 |
| 右上角斜角标签 | 右上角斜切标签，用于重点、新阶段、专项说明。 | 少量使用。 | 每页滥用，变成模板印章。 |
| 图卡拼贴 | 多张图片/案例卡片组成的证明网格。 | 用于案例证明或行业覆盖，必须有共同证明点。 | 变成图片墙。 |
| 中心主题 + 环绕卡片 | 中心主体周围组织角色/场景/能力。 | 用于平台、生态、组织协同、能力体系。 | 中心一个大词，周围一圈无关系名词。 |

---

## 4. 角色与文件术语

| 术语 | 标准定义 | 边界 |
|---|---|---|
| 角色 A / huawei_ppt_master | 负责生成大纲、逐页文案、页面设计说明和 `deck_spec.json`。 | 定义“讲什么、证明什么、不能错什么”；不施工页面图片。 |
| 角色 B / huawei_ppt_skill_optimizer | 负责评审 A/C 输出、问题清单、优化建议和 patch proposal。 | 不直接覆盖 A 的正式工作文件或 Skill。 |
| 角色 C / huawei-ppt-builder | 负责读取 A 已确认输入，编译渲染合同，生成页面图片/PPTX，自检、返工和交付。 | 不改写页面语义合同；可在受控模式下生成语义保真的有效渲染方案。 |
| 输入包 | 角色 C 接收的一组 A 输出文件。 | 通常包含 `deck_spec.json`、`page_design.md`、`visual_rules.md`、`chart_patterns.md`、`layout_library.md`、字段字典等。 |
| 页面语义合同 | `deck_spec.json`，角色 A 输出的结构化事实和语义合同。 | 不是 PPTX，不是像素级 shape 指令，不直接规定坐标/字号。 |
| 页面设计说明 | `page_design.md`，角色 A 对每页版式区域、强调、页脚、视觉降噪和 Builder 注意事项的说明。 | 不改写核心观点；不重复全局视觉默认伪装成页面独有规则。 |
| 通用视觉规则 | `visual_rules.md`，定义全局华为视觉默认、区域比例、颜色、红色锚点、负面项。 | 不承担事实校验、字段解释、流程控制、评分、证据溯源。 |
| 图表模式库 | `chart_patterns.md`，定义 `chart_type` 枚举、数据结构、图表证明规则。 | 不定义页面整体排版。 |
| 页面版式库 | `layout_library.md`，定义 `layout_pattern` 枚举、页面组织语义和版式约束。 | 不定义图表数据结构。 |
| 字段字典 | `deck_spec_field_dictionary.md`，定义 deck_spec 字段职责、可见性和 logic-only 边界。 | 不负责渲染坐标。 |
| 页面渲染合同 | `page_render_contract`，角色 C 把 A 的语义设计编译成施工输入。 | 不是新的事实源，不得新增或替代 deck_spec。 |
| 语义保真视觉重构 | Role C 在不改变页面语义合同的前提下，对上屏文案组织、版式、组件区域和图表表达进行可审计调整。 | 不是自由再创作；不得新增事实、证明目标、证据或关系语义。 |
| 视觉基线 | 角色 A 在 `deck_spec.json` 与 `page_design.md` 中给出的原始 `layout_pattern`、图表组件和页面设计意图。 | 是施工起点，不是唯一合法视觉结果。 |
| 有效渲染方案 | Role C 通过重构门禁后实际用于页面图片、HTML 或 PPTX 施工的视觉方案。 | 必须可追溯到视觉基线，不得回写页面语义合同。 |
| 严格复刻模式 | `recomposition_mode=strict_fidelity`，有效渲染方案必须等于视觉基线。 | 用户明确要求原版式不变、忠实复刻或只做样式微调时使用。 |
| 自适应重构模式 | `recomposition_mode=adaptive_recomposition`，允许在语义保真门禁内选择更优视觉方案。 | 默认模式；所有差异必须进入重构审计。 |
| 重构审计 | 对视觉基线与有效渲染方案的差异、原因、语义不变量、证据覆盖、关系保真和评分变化进行结构化记录。 | logic-only，不上屏。 |
| contact sheet | 全 deck 页面缩略总览图。 | 用于扫全局重复骨架、视觉一致性和明显错误。 |
| delivery_manifest | 交付清单 JSON。 | 记录页面图片、报告、ZIP 等产物。 |
| self_check_report | 自检报告。 | 必须覆盖语义、视觉、字段可见性、关系角色和交付风险。 |
| refinement_report | 精修报告。 | 记录 C2.5/C4.1 等视觉精修动作和边界。 |

---

## 5. deck_spec 字段术语

| 字段 / 术语 | 标准定义 | 是否上屏 | 与相邻术语区别 |
|---|---|---|---|
| `deck_title` | 整份 PPT 标题。 | 可上封面。 | 不是每页标题。 |
| `audience` | 汇报对象。 | 通常不上屏。 | 用于决定表达风格和密度。 |
| `style` | 整体风格标识，如 `huawei_executive`。 | 不上屏。 | 不是页面级视觉细节。 |
| `source` | 主要来源材料。 | 可弱化进页脚/备注。 | 不应抢主体视觉。 |
| `slides` | 页面数组。 | 不上屏。 | 角色 C 按 `slide_no` 顺序消费。 |
| `slide_no` | 页码/页面顺序。 | 可作为页脚页码。 | 不等于 `page_id`，后者通常为 P01。 |
| `section` | 所属章节。 | 只可弱化为页眉标签。 | logic-ish；不得作为主体节点或洞察栏标题。 |
| `type` | 页型，唯一标准页型字段。 | 不上屏。 | 必须来自 `page_types.md`，不是版式模式；不得另行输出 `page_type`。 |
| `page_goal` | 页面沟通目标。 | 不上屏。 | 用于校验页面是否完成沟通目的。 |
| `title` | 页面主标题。 | 必须上屏。 | 不等于 `core_judgement` 原文字段。 |
| `conclusion` | 页面核心结论/一句话结论。 | 可上屏。 | 可作为主卡、底部结论条或讲解锚点。 |
| `core_judgement` | 本页唯一核心判断，指导全页内容和视觉元素。 | logic-only，永不原文上屏。 | 不得等于 `conclusion` 或固定前缀 + `conclusion`。 |
| `chart_proof_goal` | 主图表必须证明什么。 | logic-only，不上屏。 | 约束图表论证任务，不是图表标题。 |
| `chart_visual_boundary` | 主图视觉边界：不能画偏成什么、必须体现什么、红色/主次如何控制。 | 不直接上屏。 | 是约束数组，不是视觉描述散文。 |
| `chart_semantic_mapping` | 图表语义解释映射，说明主图如何证明 `chart_proof_goal`。 | 字段名不上屏。 | 高语义风险图表的最高语义约束。 |
| `chart_components` | 单页图表组件数组；新合同中的图表事实源。 | logic-only，不上屏。 | 不与顶层旧主图字段双写；legacy 输入可不含该字段。 |
| `component_id` | 单页唯一组件编号，如 `C1`、`C2`。 | logic-only，不上屏。 | 不是页码，也不是可见编号。 |
| `component_role` | 图表组件角色，只允许 `primary` 或 `supporting`。 | logic-only，不上屏。 | 不等于 chart_data 中的业务角色。 |
| `component_region` | 图表组件在版式中的相对区域，只允许 `main`、`left`、`right`、`top`、`bottom`。 | logic-only，不上屏。 | 不是 `layout_pattern`；不包含 `insight_panel`。 |
| `supports_component_id` | supporting 所支撑的 primary 组件编号。 | logic-only，不上屏。 | 必须命中同页唯一 primary。 |
| `display_text` | 页面展示文本候选。 | 可上屏。 | 应短语化，每条不超过 15 个汉字，不放长讲稿。 |
| `speaker_notes` | 讲解口径。 | 通常不上屏。 | 不应作为主体长段落堆叠。 |
| `chart_type` | 图表组件类型；在 `chart_components` 内逐组件声明。legacy 顶层写法仅表示主图表类型。 | 不上屏。 | 回答“这个图表组件表达什么关系”。 |
| `chart_data` | 主图表数据结构。 | 其中显示字段可上屏。 | 不得新增坐标/样式 DSL。 |
| `layout_pattern` | 页面版式模式。 | 不上屏。 | 回答“页面怎么排”。 |
| `visual_notes` | 页面视觉补充说明。 | 不直接上屏。 | 通用规则应下沉，不要逐页重复。 |
| `visual_focus` | 视觉焦点列表，指导扫读路径。 | 可转写为重点。 | 不是必须逐字上屏清单。 |
| `must_highlight` | 必须强调的少量内容。 | 可上屏/可红色强调。 | 用于确定红色锚点或重点词，不能太多。 |
| `text_density` | 文本密度。 | 不上屏。 | 决定字号、压缩和承载策略。 |
| `need_compression` | 是否需要压缩。 | 不上屏。 | 为 true 时优先压缩辅助文本，不删核心判断。 |
| `data_gaps` | 数据缺口/待补材料。 | 可备注，不伪装为事实。 | 不得由角色 C 自行补全。 |

### 5.1 非字段和历史字段

| 名称 | 统一口径 |
|---|---|
| 正文模块 | page_copy 阶段的自然语言小节。生成 deck_spec 时必须拆入 `display_text`、`chart_data`、`speaker_notes` 或 `chart_semantic_mapping`。 |
| `body` | 不作为 deck_spec 字段。Role A 不应输出；Role C 不新增该字段的消费、兼容或硬规则。 |
| `page_type` | 历史输入兼容名。新 deck_spec 和新 page_render_contract 统一使用 `type`；如历史包仅有 `page_type`，角色 C 可迁移为 `type`。 |

---

## 6. chart_data 与可见性术语

| 术语 | 标准定义 | 可见性 |
|---|---|---|
| 拓扑/管道字段 | `nodes`、`edges`、`rows`、`columns`、`layers`、`stages`、`lanes` 等结构键。 | 结构键不上屏，内部显示字段可上屏。 |
| 显示内容字段 | `label`、`name`、`headline`、`items`、`description`、单元格文本、`edges.label`、`lane.name`、`layer.name`、`stage.name`。 | 可上屏，但必须短语化。 |
| logic-only 字段 | `page_goal`、`core_judgement`、`chart_proof_goal`、`group`、`emphasis`、`source_status` 等。 | 不得字面上屏。 |
| `group` | 内部分组、布局分组或样式分组。 | 不上屏；可见分组标题应使用 `label/name/headline` 等。 |
| `emphasis` | 强弱层级标记。 | 不上屏；只影响样式强弱。 |
| `source_status` | 来源状态判断。 | 不上屏；用于是否标注待核验。 |
| `edges.label` | 边上的短动作词或短关系词。 | 可上屏，但建议 2-6 个汉字。 |
| `relation_type` | 被禁止的自造关系字段。 | 不得出现在正式 `chart_data`。 |
| `edge_style` / `position` / `anchor` / `x/y` / `layer_index` | 被禁止的渲染 DSL 字段。 | 不得由角色 A 写入 `chart_data`。 |

---

## 7. chart_semantic_mapping 术语

| 字段 | 标准定义 | 角色 C 执行要求 |
|---|---|---|
| `chart_reading_intent` | 读者看完图后必须得出的判断。 | 页面第一眼应能支持该判断。 |
| `main_visual_logic` | 主图通过什么视觉关系证明判断。 | 主图不能只摆概念，必须体现关系。 |
| `axis_semantics` | 坐标轴、矩阵、趋势轴的语义。 | 四象限/趋势图必须坐标成立。 |
| `stage_or_node_meaning` | 阶段、节点、层级、泳道的语义。 | 节点摆放应符合含义，不按美观随意排列。 |
| `insight_panel_logic` | 右侧洞察栏如何解释主图。 | 洞察栏不得另讲一套。 |
| `forbidden_visualization` | 禁止采用的退化画法。 | 任一违反触发硬门禁/返工。 |
| `correspondence_pairs` | 左右或上下对象之间的直接同层对应关系。 | 不得丢失、发散化、跨层化或交叉化。 |
| `edge_roles` | 边的语义角色分组。 | 必须让分解、集成、回写、生命周期方向可见。 |
| `flow_decompose` | 自顶向下分解流。 | 方向应清晰。 |
| `flow_integrate` | 自底向上集成流。 | 不得与分解流混成单向链。 |
| `feedback_loop` | 闭环回写。 | 回写边必须可见。 |
| `lifecycle_close` | 生命周期收尾，通常弱化。 | 不抢主闭环或主流程。 |

---

## 8. 页型术语

| 页型 | 标准定义 | 典型结构 |
|---|---|---|
| `cover` 封面页 | PPT 首页。 | 主标题 + 副标题 + 汇报对象/部门/作者/日期/Security Level。 |
| `agenda` 目录页 | 超过 8 页时使用的目录。 | 3-5 个章节，不超过 7 个一级条目。 |
| `executive_summary` 核心结论页 | 高层一页看懂核心判断。 | 核心判断 + 关键结论 + 决策建议。 |
| `context_trend` 背景趋势页 | 说明外部趋势和内部诉求。 | 外部趋势 + 内部诉求 + 核心矛盾。 |
| `problem_diagnosis` 问题诊断页 | 说明现状、影响、根因、抓手。 | 现状问题 + 影响 + 根因 + 解决抓手。 |
| `comparison` 对比分析页 | 比较对象、状态或方案。 | 对象 A / 对象 B / 判断 / 启示。 |
| `architecture` 总体架构页 | 展示技术或业务体系结构。 | 资源层 / 平台层 / 能力层 / 应用层 / 运营层。 |
| `capability_map` 能力地图页 | 展示能力域、成熟度与补齐动作。 | 能力域 + 关键能力 + 成熟度 + 补齐动作。 |
| `roadmap` 路线图页 | 展示阶段递进和门槛。 | 短中长期，或试点 / 沉淀 / 复制。 |
| `risk_matrix` 风险闭环页 | 展示风险、影响、概率、措施和责任。 | 风险 / 影响 / 概率 / 应对措施 / 责任主体。 |
| `decision_table` 决策建议页 | 支撑高层拍板。 | 决策事项 / 推荐方案 / 资源需求 / 时间节点 / 预期产出。 |
| `thank_you` Thank you 页 | 结束页。 | Thank you + 版权/免责声明/愿景句。 |

---

## 9. 版式模式术语

| `layout_pattern` | 中文口径 | 标准定义 / 使用边界 |
|---|---|---|
| `executive_summary_dashboard` | 核心结论仪表盘 | 顶部结论型标题，左侧核心判断/数字，中部 3-5 个结论模块，右侧风险/建议/决策提示。 |
| `two_column_comparison` | 双栏对比 | 左右对象/状态/方案对比，中间或底部给差异结论。 |
| `four_quadrant_judgement` | 四象限判断 | 2x2 矩阵 + 顶部结论 + 底部建议；必须有真实 x/y 轴。 |
| `three_column_cards` | 三栏卡片 | 三类能力、问题或动作并列；若有先后/因果必须加箭头或改流程。 |
| `layered_architecture` | 分层架构 | 底座层 → 平台层 → 能力层 → 应用层 → 运营层。 |
| `stack_architecture_with_right_insights` | 架构 + 右侧洞察 | 左/中分层或流转主图，右侧 1 句结论 + 3-4 条短要点。 |
| `roadmap_timeline` | 路线图时间轴版式 | 横向时间轴 + 阶段目标 + 关键动作 + 里程碑。 |
| `trend_curve_with_strategy` | 趋势 + 策略解读 | 左侧趋势/曲线，右侧策略解读和动作。 |
| `ecosystem_map` | 生态关系版式 | 中心主体 + 周边角色 + 价值流/协同关系。 |
| `insight_panel_with_chart` | 主图表 + 洞察卡片 | 主图表 + 右侧洞察卡片 + 底部结论。 |
| `risk_decision_matrix` | 风险/决策矩阵版式 | 表格矩阵 + 重点风险 + 责任/时点/产出。 |
| `multi_module_solution_overview` | 多模块方案总览 | 顶部结论型标题 + 3-6 个能力/价值卡片 + 底部收口。 |
| `left_logic_right_proof` | 左逻辑右证明 | 左侧判断链，右侧案例图/指标/截图证明，底部启示。 |
| `hub_spoke_ecosystem_canvas` | 中心辐射生态画布 | 中心主体 + 环绕角色/能力/场景 + 连接线/价值流。 |
| `metric_case_showcase_grid` | 指标案例展示网格 | 顶部结论 + 大数字指标 + 案例/Logo/截图网格 + 价值收口。 |
| `image_background_section_divider` | 图片背景章节/过渡页 | 大图背景或半幅图 + 大标题 + 少量说明；高层普通章节页默认慎用。 |

> **详细规格引用**：各版式的区域占比、边界约束、适用条件和禁用组合，参见 `project/work/layout_library.md`。本表仅提供语义定义。

---

## 10. 图表类型术语

| `chart_type` | 中文口径 | 标准定义 |
|---|---|---|
| `none` | 无主图表 | 封面、目录、章节页、Thank you 页或纯结论页。 |
| `key_findings_cards` | 关键结论卡片组 | 多个关键判断、数字、风险、建议组成的卡片组。 |
| `quadrant_matrix` | 四象限判断矩阵 | 两组有效维度交叉下的位置判断。 |
| `comparison_table` | 多维对比表 | 对象 A/B、现状/目标、方案对比。 |
| `capability_radar` | 能力雷达图 | 多维能力成熟度或竞争力对比。 |
| `capability_map` | 能力地图 | 能力域、当前状态、目标状态、补齐动作。 |
| `layered_stack_diagram` | 分层堆栈图 | 平台、技术、数据、安全等层级关系。 |
| `architecture_flow_diagram` | 架构流转图 | 数据流、业务流、模型流、系统交互。 |
| `roadmap_timeline_chart` | 路线图时间轴图表 | 阶段路径、年度规划、里程碑。 |
| `trend_curve` | 趋势曲线图 | 增长、下降、拐点、成熟度或阶段变化。 |
| `ecosystem_relationship_map` | 生态关系图 | 中心主体与周边角色、价值流、协同关系。 |
| `gap_heatmap` | 差距热力图 | 短板、影响、紧急度、难度和优先级。 |
| `risk_matrix` | 风险矩阵 | 风险概率、影响、措施和责任闭环。 |
| `decision_table` | 决策清单表 | 拍板事项、资源、时点、责任和产出。 |
| `value_chain_loop` | 价值闭环图 | 输入、处理、输出、反馈、优化。 |
| `swimlane_process` | 泳道流程图 | 跨部门/角色/阶段协作流程。 |
| `priority_matrix` | 优先级矩阵 | 价值/难度、收益/投入、影响/紧急度等推进优先级。 |
| `metric_showcase_grid` | 指标展示网格 | 成果、规模、覆盖、增长等指标组合。 |
| `case_gallery_cards` | 案例图卡组 | 行业案例、样板、产品截图、生态伙伴展示。 |
| `hub_spoke_relationship_map` | 中心辐射关系图 | 中心平台/能力与周边角色/场景/能力关系。 |

---

## 11. layout_pattern 与 chart_type 的边界

| 判断问题 | 归属字段 | 示例 |
|---|---|---|
| 这一页标题、主体、右侧洞察、底部结论怎么组织？ | `layout_pattern` | `insight_panel_with_chart` |
| 这一页主图表表达对比、趋势、闭环、分层还是风险？ | `chart_type` | `comparison_table`、`trend_curve`、`value_chain_loop` |
| 名称描述“左中右、上下、卡片区、右侧洞察栏”？ | `layout_pattern` | `stack_architecture_with_right_insights` |
| 名称描述“矩阵、热力图、时间轴、架构图、关系图、决策表”？ | `chart_type` | `risk_matrix`、`roadmap_timeline_chart` |

禁止：

- 把 `insight_panel_with_chart`、`stack_architecture_with_right_insights` 等版式名写入 `chart_type`。
- 把 `risk_matrix`、`decision_table`、`trend_curve` 等图表名写入 `layout_pattern`。
- 让 `chart_type == layout_pattern`。

> **枚举完整性说明**：`chart_type` 的权威枚举以 `chart_patterns.md` §1 总表为准（当前 20 种）；`layout_pattern` 的权威枚举以 `layout_library.md` 为准（当前 16 种）。本字典 §9 和 §10 应与上述来源保持同步。如发现枚举不一致，以源文件总表为事实源。

---

## 12. 页面设计说明术语

| 术语 | 标准定义 |
|---|---|
| 区域划分 | 对标题区、图表区、文字区、强调区、页脚区的空间安排。 |
| 强调元素 | 本页被突出显示的关键词、数字、节点、风险或动作。 |
| PPTX Builder 注意事项 | 给角色 C 的施工提示，如避免压缩主图、保留来源、不要把 logic-only 上屏。 |
| 视觉降噪约束 | page_design 中专门约束红色、卡片、间距、底部条、装饰、负面风格和页型门禁的字段组。 |
| `red_anchor` | 本页唯一主红色强调点。 |
| `card_hierarchy` | 主卡、支撑卡、注释卡的强弱安排。 |
| `spacing_rule` | 模块间距、卡片内边距、安全区和页脚避让。 |
| `bottom_bar_rule` | 是否允许底部结论条，以及高度、颜色、强度、与页脚/右侧栏关系。 |
| `visual_simplification` | 需要弱化或删除的装饰元素。 |
| `visual_boundary` | 本页需避免的负面视觉风格和画法。 |
| `page_type_gate` | 页型门禁，如案例页不做图片墙、决策页拍板事项独立突出。 |
| `visual_drift_check` | 对暗色/渐变/发布会风/大红黑面积等漂移触发项的自检。 |

---

## 13. 渲染合同术语

| 字段 | 标准定义 |
|---|---|
| `page_id` | 角色 C 内部页面编号，如 `P01`。 |
| `source_contract` | 从 deck_spec 提取的标题、结论、章节、核心判断、证明目标。 |
| `source_design` | 从 page_design 与全局默认提取的设计信息。 |
| `global_design_defaults` | 全局视觉默认。 |
| `page_design_global_defaults` | 页面设计中继承的全局默认片段。 |
| `page_design_override` | 页面级覆盖/偏离规则。 |
| `page_design_sections` | 页面设计说明中的区域/字段结构。 |
| `render_intent` | 角色 C 的渲染意图，包括版式、图表、页型、主视觉目标、密度等。 |
| `main_visual_goal` | 主视觉要达成的证明/呈现目标。 |
| `visible_text_plan` | 可见文字计划。字段名本身不上屏。 |
| `main_labels` | 主标签文本。 |
| `node_labels` | 节点标签文本。 |
| `short_edge_labels` | 短边标签文本。 |
| `insight_panel` | 右侧洞察栏可见条目。 |
| `bottom_conclusion` | 底部结论条或底部收口可见文本。 |
| `visible_content_coverage` | 可见内容覆盖统计，检查必需证据是否入页。 |
| `required_evidence` | 必须进入页面的证据。 |
| `missing_required_evidence` | 未进入页面的必需证据。 |
| `semantic_constraints` | 语义约束，主要来自 `chart_semantic_mapping`。 |
| `visual_constraints` | 视觉约束，包含红色锚点、卡片层级、间距、底部条、右侧栏、页脚、安全区。 |
| `fail_conditions` | 本页失败/返工条件。 |
| `density_budget` | 密度预算，角色 C 精修时必须继承。 |
| `density_profile` | 密度档位，如 `executive_clean` 或 `technical_deep_dive`。 |
| `underfill_action` | 内容偏少时如何填充页面安全高度，不允许紧缩在顶部。 |
| `chart_contract_source` | 图表合同来源：`chart_components` 或 `legacy_primary_fields`。 | logic-only，用于追踪归一化路径。 |
| `component_coverage` | 每个图表组件的结构化可见内容与必需证据覆盖统计。 | logic-only，用于阻断组件内容静默丢失。 |
| `recomposition_mode` | Role C 重构模式，只允许 `strict_fidelity` 或 `adaptive_recomposition`。 | logic-only；不写回 deck_spec。 |
| `source_visual_plan` | 从角色 A 输入提取的视觉基线。 | logic-only；保留原始版式、组件和可见文案。 |
| `effective_visual_plan` | 通过重构校验后用于施工的有效渲染方案。 | logic-only；C2/C2.5/HTML/PPTX 只消费该方案。 |
| `recomposition_audit` | 记录重构触发原因、真实字段差异、语义保真、证据覆盖和质量增量。 | logic-only；不得以模型自报替代确定性校验。 |
| `copy_adjustments` | 记录 source/effective 上屏文案对照。 | logic-only；不得改变事实、数字、术语、否定词或结论强度。 |

---

## 14. 视觉门禁与失败术语

| 术语 | 标准定义 |
|---|---|
| 华为视觉门禁 | 白底、红黑灰白、克制、工程化、有秩序、标题结论先行、图表服务判断等硬性视觉边界。 |
| 全局华为视觉门禁 | 优先级高于 page_design 局部风格词和生成模型审美补全。 |
| 视觉漂移 | 页面偏向发布会、咨询海报、卡通插画、政务宣传、Excel 报表、论文截图或信息碎片风。 |
| 互联网发布会风 | 大渐变、炫光、科技蓝紫、霓虹、超大口号、大图压底、产品发布会主视觉。 |
| 咨询海报风 | 大圆角卡片、柔和阴影、玻璃拟态、浅色大色块、卡片拼贴、每张卡都像重点。 |
| 卡通插画风 | 手绘、拟人、表情符号、潮流贴纸、过度可爱化。 |
| 政务宣传风 | 大红底、金色字、飘带、旗帜纹理、强装饰边框、口号压过逻辑。 |
| Excel 报表风 | 全页表格、密集网格线、字号过小、无视觉重点。 |
| 学术论文截图风 | 满页段落，没有视觉结论。 |
| 信息碎片风 | 过多小卡片、小图标、小标签无层级铺满页面，像移动端信息流截图，缺乏主次和阅读路径。 |
| 模板印章 | 多页重复套同一视觉骨架或固定装饰，导致内容差异被模板吞没。 |
| 一票失败项 | 触发后不得交付，必须返工或返回 A 的硬错误。 |
| P0 | 语义错误、字段泄漏、关系方向错误。 |
| P1 | 主图证明力不足、红色失控、版式语义偏差。 |
| P2 | 间距、字重、页脚、轻微层级问题。 |
| return_to_A | 角色 C 无法在不改事实/删证据的情况下完成，需要返回角色 A。 |
| fallback | 输入缺少 `visual_rules.md` 时，角色 C 使用最小 `huawei_visual_gate.md` 保守生成。 |
| 红色面积预算 | 单页红色元素（含主锚点、辅助强调、窄红线、红色关键词背景）的总面积不超过页面面积的 **5%**。此预算优先级高于 SKILL.md 中的宽松口径。 |

---

## 15. 密度与压缩术语

| 术语 | 标准定义 |
|---|---|
| 信息密度 | 单页信息块、卡片、bullet、图表节点、右侧栏条目数量和文字长度的综合量。 |
| 中等密度 | 普通正文页约 3-5 个信息块；右侧洞察栏不超过 3 条要点。 |
| 高密度 | 普通正文页 5 个以上信息块；右侧洞察栏可到 8 条要点，但必须有网格和呼吸感。 |
| `executive_clean` | 面向高层扫读的简洁密度。 |
| `technical_deep_dive` | 技术深挖密度，不得被角色 C 静默降级。 |
| `need_compression` | 标记页面需要压缩。压缩应优先处理辅助文本，不删核心判断或必需证据。 |
| Underfill | 内容偏少导致页面空、上方紧缩。 | 
| 密度保真 | 角色 C 精修必须保留 A 的密度意图和 `required_evidence`。 |

---

## 16. 易混术语对照

| 易混组 | 区别 |
|---|---|
| `title` vs `conclusion` vs `core_judgement` | `title` 是上屏主标题；`conclusion` 是可上屏的一句话结论；`core_judgement` 是 logic-only 的唯一判断锚点。 |
| `chart_proof_goal` vs `main_visual_goal` | `chart_proof_goal` 来自 A，规定主图要证明什么；`main_visual_goal` 是 C 编译后的主视觉施工目标。 |
| `chart_visual_boundary` vs `visual_boundary` | 前者约束主图表不能怎么画；后者约束页面视觉负面风格和边界。 |
| `layout_pattern` vs `chart_type` | 前者管页面怎么排；后者管单个图表组件表达什么关系。 |
| `type` vs `layout_pattern` | `type` 是页型/沟通角色，如决策页/路线图页；版式模式是空间组织，如双栏/架构+右栏。 |
| 主体区 vs 图表区 | 主体区是大区域；图表区是主体区内的主图空间。 |
| 正文区 vs 文字区 | “正文区”已废弃，容易被误解为主体区或长文本区；新输出统一写“文字区”，且只承载短语化可见文本。 |
| 右侧洞察栏 vs 右侧备注栏 | 洞察栏必须解释主图、提供证据或建议；备注栏只是附加说明，华为风格中不推荐作为主组件。 |
| 底部结论条 vs 页脚 | 底部结论条是页面收口；页脚是页码/来源/版权/保密标识。二者不能重叠。 |
| 底部结论条 vs 主结论卡 | 底部条在主体下方轻收口；主结论卡在主体中承担主判断，视觉优先级更高。 |
| 红色锚点 vs 红色装饰 | 锚点服务语义；装饰只为好看，禁止。 |
| 卡片组 vs 图表 | 卡片组可以是 `key_findings_cards`；但普通装饰卡片不必都算主图表。 |
| 证据页 vs 案例页 | 证据页可用数据/图表/截图；案例页必须有案例来源或待核验标注。 |
| 轻量底部结论条 vs 厚重红色横幅 | 前者推荐；后者普通正文页慎用，容易触发红色过重。 |
| `layout_pattern` vs `component_region` | 前者定义整页组织；后者定义单个图表组件在该版式中的相对槽位。 |
| `component_region=right` vs 右侧洞察栏 | `right` 是版式兼容表明确允许的右侧图表区；右侧洞察栏只解释主图，不承载独立图表。 |
| component contract vs legacy contract | 新合同以 `chart_components` 为唯一图表事实源；legacy 合同仅兼容历史顶层主图字段。 |
| primary vs 顶层旧主图字段 | primary 是新合同事实源；顶层兼容值只在 Role C 的 normalized/render contract 中机器派生。 |

### 16.1 组件区域槽位与页面区域映射

| `component_region` | 页面区域含义 | 约束 |
|---|---|---|
| `main` | 主体区中的主要图表区 | primary 优先使用。 |
| `left` | 主体区左侧图表区 | 必须由版式—区域兼容表允许。 |
| `right` | 主体区右侧图表区 | 不得冒充右侧洞察栏。 |
| `top` | 主体区顶部辅助图表区 | 不是标题区。 |
| `bottom` | 主体区底部辅助图表区 | 不是底部结论条或页脚区；与启用的底部结论条互斥。 |

右侧洞察栏不属于 `component_region`。关键数字、排名和极简证据卡继续由 `insight_panel_logic` / `visible_text_plan.insight_panel` 承载；含坐标轴、nodes/edges、层级、阶段、泳道、矩阵或独立 `chart_data` 的图表必须进入合法图表区域。

---

## 17. 当前发现的需统一口径点

| 问题 | 当前差异 | 建议统一 | 状态 | 修改文件 |
|---|---|---|---|---|
| 右侧洞察栏宽度 | `project/work/visual_rules.md` 写 25%-32%；`skills/huawei_ppt_master/templates/visual_rules.md` 写 18%-28%，且后文又有“不超过 32%”类口径。 | 统一为：普通页推荐 18%-28%；复杂架构页或高密度页可放宽到 25%-32%；绝不超过 1/3。 | 已修复 | `project/work/visual_rules.md`、`project/work/layout_library.md`、`skills/huawei_ppt_master/templates/visual_rules.md`、`skills/huawei_ppt_master/visual_patterns/layout_library.md`、builder tokens/prompts |
| 右侧洞察栏定位 | 一个版本强调“辅助解释区”，另一个版本强调“结论证据栏”。 | 统一为：右侧洞察栏是辅助解释区，也是结论证据栏；核心要求是解释主图，不成为第二文字区。 | 已修复 | `skills/huawei_ppt_master/templates/visual_rules.md`、builder field/prompt docs |
| 底部结论条与右侧洞察栏能否同时出现 | visual_rules 中有“不建议和右侧洞察栏同时出现”；layout_library 的 `insight_panel_with_chart` 又定义“主图表 + 右侧洞察卡片 + 底部结论”。 | 统一为：允许同时出现，但只允许“右侧洞察栏 + 轻量底部结论条”；不得同时使用强右栏、厚重大红底部条和多个红色大数字。 | 已修复 | `skills/huawei_ppt_master/templates/visual_rules.md`、`project/work/layout_library.md`、builder/html builder prompts |
| 主体区 / 正文区 / 图表区 / 文字区 | `visual_rules.md` 说主体区；`generate_page_design.md` 要求标题区、图表区、正文区、强调区、页脚区；输出契约又写图表区、文字区。 | 统一为：一级区域为标题区/主体区/页脚区；主体区可细分图表区/文字区/强调区/右侧洞察栏/底部结论条；“正文区”和“内容区”废弃。 | 已修复 | `skills/huawei_ppt_master/prompts/generate_page_design.md`、`skills/huawei_ppt_master/core/output_contracts.md`、builder/html builder prompts/checklists |
| `section` 可见性 | deck_spec 中可作为页眉小标签；field_visibility_policy 禁止作为主体/洞察栏/底部结论主语。 | 统一为：`section` 只作为页眉弱标签，绝不进入主体图表和结论组件。 | 已对齐 | - |
| `visual_rules.md` 来源 | builder 规定优先读取输入包中的 visual_rules，缺失才 fallback；master 模板也有 visual_rules。 | 统一为：C 执行时以输入包 `visual_rules.md` 为准；skill 模板是生成/更新输入包的来源，不在 C 阶段覆盖输入。 | 已对齐 | - |

---

## 18. 推荐写法模板

### 18.1 page_design 区域写法

```text
区域划分：
- 标题区：顶部 10%-15%，左对齐结论型标题，短红线定锚。
- 主体区：左/中部为主图表，右侧为洞察栏；主图优先级高于洞察栏。
- 底部结论条：使用浅灰底 + 红色关键词，位于主体下方、页脚上方。
- 页脚区：页码、来源、保密标识弱化，避让 Huawei Logo。
```

### 18.2 右侧洞察栏写法

```text
右侧洞察栏：
- 作用：解释主图，不另起一套正文。
- 内容：1 句短结论 + 3 条短要点。
- 视觉：白底/极浅灰底、灰色细边、红色只用于关键词或关键数字。
- 宽度：普通页 18%-28%；复杂架构页可到 25%-32%；不超过 1/3。
```

### 18.3 底部结论条写法

```text
bottom_bar_rule：
- 允许轻量底部结论条。
- 高度控制在页面高度 5%-9%，避开页脚和右下 Logo。
- 使用浅灰底或白底灰边 + 窄红线，不使用厚重大红横幅。
- 内容只写一句收口，不重复标题，不放 bullet。
```

### 18.4 layout/chart 边界写法

```json
{
  "layout_pattern": "insight_panel_with_chart",
  "chart_type": "comparison_table",
  "chart_proof_goal": "证明两个方案在成本、生态和落地风险上的差异，并导出推荐方向",
  "chart_visual_boundary": [
    "表格承担证据，不得铺满全页",
    "右侧洞察栏只总结差异和行动含义",
    "红色只用于推荐方向或最高风险"
  ]
}
```

---

## 19. 一句话总则

`huawei_ppt_master` 负责把“判断、证据、边界”说清楚；`huawei_ppt_builder` 负责把这些语义落成“可见、可读、可审查”的页面。所有术语都应服务这个分工：不要让版式词替代图表语义，不要让视觉词改写事实，也不要让渲染合同变成新的内容源。

---

## 20. 变更日志

| 版本 | 日期 | 变更内容 |
|---|---|---|
| v1.0 | 2026-06-05 | 初版发布。含 19 章节，覆盖区域、组件、角色、字段、图表、版式、门禁、密度、易混对照和推荐写法。 |
| v1.1 | 2026-06-05 | 应用角色 B 评审补丁（P0 x4、P1 x5、P2 x3）：统一 `core_judgement` 永不上屏、废弃“正文区/内容区”、补红色面积预算、枚举完整性说明、安全区/页脚/红色数量/display_text 限制、信息碎片风、口径状态列和版本日志。 |
| v1.2 | 2026-06-05 | 评审通过后启动术语治理落地，更新 `huawei_ppt_master`、`huawei_ppt_builder`、`huawei_ppt_builder_html` 及项目工作区镜像说明文档，并将 §17 待修复项推进为已修复。 |
| v1.3 | 2026-06-05 | 响应 body/type 术语修复：明确 `body` 不作为 deck_spec 字段、Role C 不新增 body 规则；页型统一使用 `type`，`page_type` 仅作历史输入兼容名。 |
| v1.4 | 2026-06-19 | 新增图表组件合同术语、主/辅组件、组件区域、合同来源和逐组件 coverage；明确右侧洞察栏不是图表组件槽位，新合同禁止与顶层旧主图字段双写。 |
| v1.5 | 2026-06-20 | 新增语义保真视觉重构、视觉基线、有效渲染方案、严格复刻/自适应重构模式及重构审计字段；明确 Role C 不回写页面语义合同。 |
