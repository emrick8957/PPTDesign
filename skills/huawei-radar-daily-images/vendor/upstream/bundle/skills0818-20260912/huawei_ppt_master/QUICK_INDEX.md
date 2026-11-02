# huawei_ppt_master 快速索引

## 常用速查文件

- 主题路由与术语边界总表：`skills/huawei_ppt_master/REFERENCE_ROUTING_TABLE.md`
- Skill 入口规则：`skills/huawei_ppt_master/SKILL.md`
- 执行流程：`skills/huawei_ppt_master/core/generation_workflow.md`
- 主题路由规则：`skills/huawei_ppt_master/core/topic_router.md`
- 前沿雷达日报精读主题包：`skills/huawei_ppt_master/domain_profiles/frontier_radar_daily_deep_read.md`
- 前沿雷达日报精读方法论：`skills/huawei_ppt_master/methodology_patterns/frontier_radar_daily_deep_read_patterns.md`
- 防污染规则：`skills/huawei_ppt_master/core/anti_overfit_rules.md`
- deck_spec 字段字典：`skills/huawei_ppt_master/core/deck_spec_field_dictionary.md`
- 多图表组件合同与区域兼容表：`skills/huawei_ppt_master/core/deck_spec_field_dictionary.md`、`skills/huawei_ppt_master/visual_patterns/layout_library.md`
- Role C 视觉基线与有效渲染方案术语：`skills/huawei_ppt_master/core/terminology_dictionary.md`
- chart_data 字段可见性：`skills/huawei_ppt_master/core/deck_spec_field_dictionary.md` 中 “chart_data 字段通则与可见性约定”
- 图表语义映射规则：`skills/huawei_ppt_master/templates/chart_patterns.md` 中 `chart_semantic_mapping` 章节
- 字段差异化规则：`skills/huawei_ppt_master/core/field_differentiation_rules.md`
- 模板印章检测 / 清单印章检测 / 视觉漂移印章检测 / 可见版式术语检测：`skills/huawei_ppt_master/eval/template_stamp_detection.md`

## 快速用途

- 想看“什么主题触发什么包” → 先读 `REFERENCE_ROUTING_TABLE.md`
- 想看“完整规则” → 读 `SKILL.md`
- 想看“执行步骤” → 读 `generation_workflow.md`
- 想看“前沿雷达日报精读 / 技术信号精读 / 论文信号洞察如何固定生成 10 页结构” → 读 `domain_profiles/frontier_radar_daily_deep_read.md` 与 `methodology_patterns/frontier_radar_daily_deep_read_patterns.md`
- 想看“雷达/信号字面命中为什么不能自动触发前沿雷达日报主题包” → 读 `core/topic_router.md`
- 想看“为什么某主题不能写昇腾/NVIDIA” → 读 `anti_overfit_rules.md`
- 想看“页面为什么不够华为风格/视觉偏重” → 读 `templates/visual_rules.md`、`visual_patterns/layout_library.md`、`templates/chart_patterns.md`、`eval/visual_scorecard.md`
- 想看“页面设计说明必须给 Builder 哪些视觉约束” → 读 `prompts/generate_page_design.md` 与 `core/output_contracts.md`
- 想看“页面级暗色/渐变/科技发布会词与全局华为风格冲突时怎么处理” → 读 `templates/visual_rules.md`、`prompts/generate_page_design.md`、`eval/acceptance_checklist.md` 与 `eval/template_stamp_detection.md`

- 想看“deck_spec.json 每个字段给角色 C 怎么理解” → 读 `core/deck_spec_field_dictionary.md`
- 想看“一页如何设计一个主图表组件与多个辅助图表组件、哪些区域可用” → 读 `core/deck_spec_field_dictionary.md` 的 `chart_components` 合同与 `visual_patterns/layout_library.md` 的版式—区域兼容表。

- 想看“trend_curve 等图表如何证明 chart_proof_goal” → 读 `templates/chart_patterns.md` 的 `chart_semantic_mapping` 章节
- 想看“如何避免多页字段机械套版、清单页连续疲劳、卡片矩阵同构、暗色发布会风漂移或版式术语上屏” → 读 `core/field_differentiation_rules.md` 与 `eval/template_stamp_detection.md`

- 想看“group/edges.label/section 等字段是否应该上屏” → 读 `core/deck_spec_field_dictionary.md` 的 chart_data 字段可见性章节，并对照 `core/output_contracts.md` 的 deck_spec 强门禁。
- 想看“V 模型等同层对应/双分支关系如何让角色 C 可消费” → 读 `core/deck_spec_field_dictionary.md` §4.7 关系角色结构化枚举（`correspondence_pairs` / `edge_roles`）。
