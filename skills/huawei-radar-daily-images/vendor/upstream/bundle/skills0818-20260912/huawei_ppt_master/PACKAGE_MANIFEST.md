# Package Manifest

Current package version: v0.5.1-visual-recomposition-terms
Last updated: 2026-06-20

- `CHANGELOG.md`
- `README.md`
- `SKILL.md`
- `UPGRADE_FILE_LIST_v0.2.md`
- `VERSION.md`
- `core/anti_overfit_rules.md`
- `core/audience_rules.md`
- `core/deck_spec_field_dictionary.md`
- `core/terminology_dictionary.md`
- `core/field_differentiation_rules.md`
- `core/generation_workflow.md`
- `core/output_contracts.md`
- `core/reference_ingestion_workflow.md`
- `core/reference_material_policy.md`
- `core/topic_router.md`
- `domain_profiles/ai_compute_ascend_nvidia.md`
- `domain_profiles/ai_platform.md`
- `domain_profiles/customer_solution.md`
- `domain_profiles/cybersecurity.md`
- `domain_profiles/data_governance.md`
- `domain_profiles/default_general.md`
- `domain_profiles/frontier_radar_daily_deep_read.md`
- `domain_profiles/gov_public_security.md`
- `domain_profiles/project_operation.md`
- `eval/acceptance_checklist.md`
- `eval/domain_contamination_tests.md`
- `eval/reference_learning_regression.md`
- `eval/template_stamp_detection.md`
- `eval/regression_cases.md`
- `eval/visual_scorecard.md`
- `prompts/deck_spec_generation.md`
- `prompts/generate_outline.md`
- `prompts/generate_page_copy.md`
- `prompts/generate_page_design.md`
- `prompts/screenshot_analysis.md`
- `prompts/self_review.md`
- `methodology_patterns/executive_argument_patterns.md`
- `methodology_patterns/frontier_radar_daily_deep_read_patterns.md`
- `methodology_patterns/industry_framework_extraction_rules.md`
- `methodology_patterns/page_role_patterns.md`
- `methodology_patterns/section_logic_patterns.md`
- `templates/chart_patterns.md`
- `templates/huawei_style_reference.md`
- `templates/narrative_patterns.md`
- `templates/page_types.md`
- `templates/visual_rules.md`
- `templates/wording_rules.md`
- `visual_patterns/architecture_page_patterns.md`
- `visual_patterns/comparison_page_patterns.md`
- `visual_patterns/executive_summary_patterns.md`
- `visual_patterns/layout_library.md`
- `visual_patterns/risk_decision_patterns.md`
- `visual_patterns/roadmap_page_patterns.md`
- `visual_patterns/screenshot_layout_analysis.md`
- `visual_patterns/solution_showcase_patterns.md`


---

## 3. 文件职责说明

### 3.1 `core/`：通用执行内核，任何任务都必须优先读取

- `core/generation_workflow.md`  
  定义从主题识别、章节规划、大纲生成、逐页文案、页面设计、deck_spec 到自检的完整流程。

- `core/topic_router.md`  
  判断用户主题类型，并决定是否加载 `domain_profiles/` 下的主题包。

- `core/output_contracts.md`  
  定义大纲、逐页文案、页面设计说明、deck_spec.json 的标准输出格式。

- `core/anti_overfit_rules.md`  
  防止昇腾/NVIDIA/AI算力等主题内容污染其他主题。该文件为强约束文件。

- `core/audience_rules.md`  
  根据汇报对象调整口径，包括华为内部高层、客户高层、市局/分局领导、技术团队等。

- `core/deck_spec_field_dictionary.md`  
  定义 `deck_spec.json` 的文件定位、顶层字段、slide 字段职责和 chart_data 字段可见性约定，作为角色 C 理解 deck_spec 的正式交付物支持文档。

- `core/field_differentiation_rules.md`  
  定义字段差异化规则、允许重复白名单、必须逐页有设计增量字段，以及 core_judgement / chart_proof_goal / chart_visual_boundary 的正反例。

- `core/reference_ingestion_workflow.md`  
  定义持续提供 PPT、PPT 图片、模板、文本材料和数据材料时的分类、抽取、沉淀、冲突处理和复用流程。

- `core/reference_material_policy.md`  
  定义不同参考材料的证据等级与使用边界，避免把视觉参考误当事实依据。

### 3.2 `templates/`：通用华为风格模板库，所有主题均可使用

- `templates/page_types.md`  
  定义封面、目录、总览、对比、架构、路线图、风险、决策、Thank you 等页型。

- `templates/narrative_patterns.md`  
  定义高层汇报、客户汇报、技术方案、项目复盘、竞品对比等叙事结构。

- `templates/visual_rules.md`  
  定义华为风格配色、字体、页脚、留白、图表视觉规则。

- `templates/chart_patterns.md`  
  定义矩阵、架构图、路线图、风险表、决策表、生态图、能力地图等图表模式。

- `templates/wording_rules.md`  
  定义通用华为式文案表达，禁止空泛口号，不包含具体行业事实。

- `templates/huawei_style_reference.md`  
  记录用户提供的华为模板风格要点，包括白底、红黑灰、正式页脚等。

### 3.3 `domain_profiles/`：主题知识包，必须由 topic_router 条件触发

- `domain_profiles/default_general.md`  
  默认主题包。任何无法明确归类的主题都使用该包。

- `domain_profiles/ai_compute_ascend_nvidia.md`  
  仅当用户主题明确涉及昇腾、英伟达、NVIDIA、AI算力、GPU/NPU、算力调度、模型适配、CUDA、CANN、MindSpore 等内容时允许读取。

- `domain_profiles/gov_public_security.md`  
  仅当用户主题明确涉及公安、政务、市局、分局、区县、安平、视频解析、警情研判等内容时允许读取。

- `domain_profiles/ai_platform.md`  
  仅当用户主题明确涉及 AI 平台、模型平台、应用平台、模型服务、MLOps 等内容时允许读取。

- `domain_profiles/project_operation.md`  
  仅当用户主题明确涉及持续运营、项目运营、运维治理、运营机制、服务保障等内容时允许读取。

- `domain_profiles/customer_solution.md`  
  仅当用户明确要求客户版、客户汇报、解决方案、售前方案时允许读取。

- `domain_profiles/data_governance.md`  
  仅当用户主题明确涉及数据治理、数据资产、数据中台、数据质量、数据目录等内容时允许读取。

- `domain_profiles/cybersecurity.md`  
  仅当用户主题明确涉及网络安全、安全运营、主机安全、攻防、合规、安全测试等内容时允许读取。

### 3.4 `visual_patterns/`：版式库，用于页面设计说明与 PPTX 生成输入

- `visual_patterns/layout_library.md`  
  通用页面布局模式库。

- `visual_patterns/screenshot_layout_analysis.md`  
  基于用户提供版式截图提取的布局规律。

- `visual_patterns/executive_summary_patterns.md`  
  总览页、仪表盘页、四象限判断页模式。

- `visual_patterns/comparison_page_patterns.md`  
  对比页、矩阵页、左右对照页模式。

- `visual_patterns/architecture_page_patterns.md`  
  架构图、分层图、链路图、生态图模式。

- `visual_patterns/roadmap_page_patterns.md`  
  时间轴、三阶段路线图、里程碑图模式。

- `visual_patterns/risk_decision_patterns.md`  
  风险矩阵、决策清单、行动闭环页模式。

### 3.5 `methodology_patterns/`：方法论与内容套路库

- `methodology_patterns/executive_argument_patterns.md`  
  沉淀高层汇报中的“判断—依据—动作—风险—决策”等论证套路。

- `methodology_patterns/section_logic_patterns.md`  
  沉淀战略、方案、对比、复盘、客户方案、资源申请等章节逻辑。

- `methodology_patterns/page_role_patterns.md`  
  沉淀总览页、诊断页、对比页、方案页、路径页、风险页、拍板页等页面角色模式。

- `methodology_patterns/industry_framework_extraction_rules.md`  
  定义如何从持续投喂的行业 PPT / 图片中抽取可复用行业方法论。

### 3.6 `eval/`：验收与回归测试

- `eval/acceptance_checklist.md`  
  通用质量验收清单。

- `eval/visual_scorecard.md`  
  页面设计说明、版式质量、视觉降噪和华为风格一致性评分表。

- `eval/regression_cases.md`  
  Skill 升级后的回归测试题。

- `eval/domain_contamination_tests.md`  
  检查非 AI 算力主题是否被昇腾/NVIDIA/GPU/NPU 等术语污染。

- `eval/reference_learning_regression.md`  
  检查参考材料学习后的视觉、结构、表达、体系、主题隔离和增量稳定性。

- `eval/template_stamp_detection.md`  
  执行防机械套版检测，检查重复字段、字面复述、骨架填词、缺少逐页设计决策、清单印章风险、视觉漂移印章风险和可见版式术语上屏风险。

### 3.7 `prompts/`：可复用提示词

`prompts/` 仅作为提示词素材库，不得覆盖本 `SKILL.md` 中的强制规则。

### 3.7 v0.3.5 生成图片反馈沉淀资产

本版本同步增强以下资产：

- `templates/visual_rules.md`：正文页红色底座控制、多卡片主次层级。
- `visual_patterns/layout_library.md`：阅读框架页、案例证明页、决策建议页、路线图页、总结页语义约束。
- `templates/chart_patterns.md`：案例图卡、决策表、能力地图、分层堆栈、路线图时间轴失败条件。
- `templates/wording_rules.md`：长标题压缩、总结页最终定义。
- `eval/visual_scorecard.md`：生成图片反馈一票降级项。

### 3.8 v0.3.6 视觉规则重构资产

本版本同步增强以下资产：

- `templates/visual_rules.md`：以 `visual_rules_v0.2.md` 为主干重构为专职视觉设计指导资产，并保留历史沉淀兼容说明。
- `prompts/generate_page_design.md`：新增 `visual_boundary` 与 `page_type_gate` 输出要求。
- `core/output_contracts.md`：同步页面设计说明输出契约。
- `core/generation_workflow.md`：同步页面设计生成流程字段。
- `eval/visual_scorecard.md`：新增 v0.3.6 视觉风格边界扣分/降级项。
- `README.md`、`INDEX.md`、`VERSION.md`、`CHANGELOG.md`：同步版本与资产说明。


### 3.9 v0.3.7 deck_spec 证明契约资产

本版本同步增强以下资产：

- `core/output_contracts.md`：deck_spec 每页新增 `core_judgement`、`chart_proof_goal`、`chart_visual_boundary` 字段。
- `prompts/deck_spec_generation.md`：要求先生成唯一核心判断，再规划逐组件证明目标与 `chart_type`，最后按 `layout_pattern × component_region` 兼容表落位。
- `core/generation_workflow.md`：同步 Step 6.5 字段映射检查顺序。
- `templates/chart_patterns.md`：新增各类 `chart_type` 的 proof_goal 示例与 visual_boundary 边界。
- `eval/visual_scorecard.md`：新增 v0.3.7 deck_spec 证明契约检查与一票降级项。
- `eval/acceptance_checklist.md`：新增 deck_spec 证明契约验收项。

### 3.10 v0.3.8 deck_spec 字段字典资产

本版本新增以下正式交付物支持资产：

- `core/deck_spec_field_dictionary.md`：说明 `deck_spec.json` 的文件定位、顶层字段和 slide 字段，明确其是页面语义合同，不是 PPTX 或 shape 指令。

边界：本版本不继续推进 `page_render_spec` / `normalized_render_model` 方案，不新增渲染 DSL，不改变默认生成链路。


### 3.11 v0.3.9 chart_semantic_mapping 图表语义映射资产

本版本同步增强以下资产：

- `core/output_contracts.md`：新增 `chart_semantic_mapping` 字段契约、触发规则和示例。
- `prompts/deck_spec_generation.md`：要求 `trend_curve` 必须输出图表语义映射，高语义风险图表建议输出。
- `templates/chart_patterns.md`：新增 `chart_semantic_mapping` 章节、六个核心字段和 `trend_curve` 示例。
- `core/deck_spec_field_dictionary.md`：补充 `chart_semantic_mapping` 字段说明。
- `eval/visual_scorecard.md`：新增 v0.3.9 图表语义映射检查与一票降级项。

边界：该字段是 deck_spec 语义证明增强，不是渲染 DSL；不恢复 `page_render_spec` / `normalized_render_model` 方案。


### 3.12 v0.4.0 防机械套版门禁资产

本版本同步增强以下资产：

- `core/field_differentiation_rules.md`：字段差异化单一真相源。
- `eval/template_stamp_detection.md`：模板印章检测门禁与混合阈值模型。
- `core/output_contracts.md`：新增字段差异化强门禁。
- `prompts/deck_spec_generation.md`：要求 self_check 输出模板印章检测结果。
- `eval/acceptance_checklist.md`、`eval/visual_scorecard.md`：新增防机械套版验收和一票降级项。
- `templates/visual_rules.md`、`templates/wording_rules.md`：新增通用视觉规则下沉和防骨架填词规则。

边界：不恢复 `page_render_spec` / `normalized_render_model`，不新增渲染 DSL，不要求所有字段都差异化。


### 3.13 v0.4.1 chart_data 字段可见性资产

本版本同步增强以下资产：

- `core/deck_spec_field_dictionary.md`：新增 chart_data 字段分层、logic-only 字段清单、可见分组标题、`edges.label` 边界、短语化判据和关系语义承载位置。
- `core/output_contracts.md`：deck_spec 强门禁新增 logic-only 字段不上屏、可见分组标题字段、`edges.label` 短动作词、禁止关系/渲染 DSL 字段。
- `templates/chart_patterns.md`：新增 chart_data 字段可见性边界说明。
- `prompts/deck_spec_generation.md`：新增生成时字段可见性检查。
- `eval/acceptance_checklist.md`、`eval/regression_cases.md`、`eval/visual_scorecard.md`：新增验收、回归和一票降级项。

### 3.14 v0.4.2 关系角色结构化枚举资产

本版本同步增强以下资产：

- `core/deck_spec_field_dictionary.md`：新增 §4.7 关系角色与对应关系的结构化枚举（`correspondence_pairs` / `edge_roles`）。
- `core/output_contracts.md`：deck_spec 强门禁新增第 22、23 条（同层对应单一事实源、edge_roles 边引用结构化与存在性）。
- `prompts/deck_spec_generation.md`：新增关系角色生成与一致性检查项。
- `templates/chart_patterns.md`：补充关系角色承载指引。
- `eval/visual_scorecard.md`：新增 P 章节与一票降级项。
- `eval/regression_cases.md`：新增 Test 12、Test 13。

已知留项（P3，本版未处理）：`edge_roles` 词表闭合、回归全量补强、角色 C 依赖声明与兜底散文强制，后续独立小补丁跟进。

### 3.15 v0.4.3 清单印章检测资产

本版本同步增强以下资产：

- `eval/template_stamp_detection.md`：新增清单印章检测，基于标准 `layout_pattern` 与 `chart_type` 双集并集计算 `is_list_page`。
- `eval/acceptance_checklist.md`：防机械套版门禁新增清单印章检测验收项和重写条件。
- `core/field_differentiation_rules.md`：新增“逻辑关系不得退化为清单”的正反例。

边界：不新增 deck_spec 字段，不引入渲染 DSL；清单判定集只使用项目标准枚举，并保留小包、附录和用户明确清单版的例外。

### 3.16 v0.4.4 视觉冲突优先级资产

本版本同步增强以下资产：

- `templates/visual_rules.md`：新增“全局视觉门禁 > page_design 局部风格词 > 生成模型审美补全”的冲突优先级，并补充封面/章节页白底工程化推荐与暗色发布会风禁止项。
- `prompts/generate_page_design.md`：新增 A 侧自检项，检查暗色/渐变/科技发布会触发词、大面积红黑、`image_background_section_divider` 和章节号视觉支配风险。
- `eval/acceptance_checklist.md`：新增视觉漂移触发词门禁，要求冲突页面主动降级为白底/浅灰底/细红线定锚的华为高层汇报风。
- `eval/template_stamp_detection.md`：新增视觉漂移印章检测，把连续暗红渐变、巨大红色章节号、科技网格背景和发布会式骨架纳入 WARN/FAIL 判定。

边界：不新增 deck_spec 字段，不引入渲染 DSL；仅在用户明确要求暗色发布会风时允许保留相关页面设计，否则普通华为高层汇报页必须优先回到克制、工程化、白底为主的表达。

### 3.17 v0.4.5 可见版式术语门禁资产

本版本同步增强以下资产：

- `SKILL.md`：版本升级为 `0.4.5-visible-layout-terms-gate`，模板印章自检输出新增可见版式术语检测。
- `eval/template_stamp_detection.md`：新增可见版式术语检测，只检查页面可见字段，不对内部设计说明做全文 contains。
- `eval/acceptance_checklist.md`：防机械套版门禁新增可见版式术语检测验收项和重写条件。
- `README.md`、`VERSION.md`、`CHANGELOG.md`、`PACKAGE_MANIFEST.md`：同步版本与资产说明。

边界：不新增 deck_spec 字段，不新增 `layout_pattern` / `chart_type` 枚举，不修改 Role C 主流程；内部设计说明允许使用“右侧洞察栏 / 主体区 / 图表区 / 底部结论条”等术语，页面可见字段不得输出“右侧洞察：xxx”“洞察栏：xxx”“主体区：xxx”等组件说明式标题。

### 3.18 v0.4.6 前沿雷达日报精读主题包资产

本版本同步增强以下资产：

- `domain_profiles/frontier_radar_daily_deep_read.md`：新增条件触发主题包，定义触发条件、10 页固定结构、layout/chart 映射、Catalyst/Application 必填语义、表达规则、视觉规则和事实边界。
- `methodology_patterns/frontier_radar_daily_deep_read_patterns.md`：新增外部技术信号精读方法论，定义核心链路、选信号规则、Catalyst/Application 成对规则、P09 趋势页规则、P10 行动收口和防退化规则。
- `core/topic_router.md`：新增 `frontier_radar_daily_deep_read` 路由条目，并补充“雷达/信号”歧义保护。
- `eval/reference_learning_regression.md`：新增前沿雷达日报精读专项回归，检查四段式主线、10 页结构、事实边界和反例不误触发。

边界：不新增 deck_spec 字段，不新增 `layout_pattern` / `chart_type` 枚举；截图和历史样例只用于结构、视觉、表达和体系学习，不作为事实依据；真实雷达硬件、信号处理、射频/通信信号等工程语境不得误触发该主题包。

### 3.19 v0.5.0 多图表组件合同资产

本版本同步增强以下资产：

- `core/terminology_dictionary.md`、`core/deck_spec_field_dictionary.md`：新增图表组件、主图表组件、辅助图表组件及其字段合同。
- `core/output_contracts.md`、`core/generation_workflow.md`、`prompts/deck_spec_generation.md`：将 `chart_components` 设为新合同唯一事实源，顶层主图字段仅作 legacy 兼容。
- `visual_patterns/layout_library.md`：新增 16 种版式的主/辅组件区域硬兼容表，排除 `insight_panel`。
- `core/field_differentiation_rules.md`、`eval/template_stamp_detection.md`：新增逐组件证明目标和视觉边界的差异化检测。
- `templates/chart_patterns.md`、`prompts/generate_page_design.md`、`eval/acceptance_checklist.md`、`eval/visual_scorecard.md`：同步多组件设计与验收门禁。

边界：每页恰好一个主图表组件、最多三个辅助图表组件；右侧洞察栏只解释主图；不新增 `layout_pattern` / `chart_type` 枚举，不恢复渲染 DSL。

### 3.20 v0.5.1 Role C 视觉重构术语资产

- `core/terminology_dictionary.md`：新增语义保真视觉重构、视觉基线、有效渲染方案、严格复刻/自适应重构和重构审计。
- `core/deck_spec_field_dictionary.md`：明确 layout/chart/region 是视觉基线，Role C 只在内部 render contract 中生成有效方案且不回写 deck_spec。

边界：不新增 deck_spec 字段，不新增标准 layout/chart 枚举，不恢复渲染 DSL。
