# Skills Index

> huawei_ppt_master Skill 总索引。
> 用途：快速定位 huawei_ppt_master 入口、速查文件和适用场景。
> 更新时间：2026-06-20

## 目录

### 1. huawei_ppt_master
- **路径**：`skills/huawei_ppt_master/`
- **入口文件**：`skills/huawei_ppt_master/SKILL.md`
- **快速索引**：`skills/huawei_ppt_master/QUICK_INDEX.md`
- **路由总表**：`skills/huawei_ppt_master/REFERENCE_ROUTING_TABLE.md`
- **适用场景**：华为风格 PPT 大纲、逐页文案、页面设计说明、deck_spec 生成
- **视觉一致性资产**：`templates/visual_rules.md`、`templates/chart_patterns.md`、`visual_patterns/layout_library.md`、`eval/visual_scorecard.md`、`prompts/generate_page_design.md`
- **生成图片反馈资产**：正文页红色底座控制、多卡片主次层级、案例证明页、决策建议页、路线图阶段门槛、长标题压缩、总结页最终定义、visual_scorecard 一票降级项
- **deck_spec 证明契约资产**：`core/output_contracts.md`、`prompts/deck_spec_generation.md`、`templates/chart_patterns.md`、`eval/visual_scorecard.md`；新增 `core_judgement` / `chart_proof_goal` / `chart_visual_boundary`
- **deck_spec 字段字典**：`core/deck_spec_field_dictionary.md`；说明文件定位、顶层字段和 slide 字段，作为后续正式交付物支持资产
- **多图表组件合同**：`chart_components` 作为新合同唯一事实源；支持 1 个主图表组件与 0–3 个辅助图表组件，并由 `visual_patterns/layout_library.md` 提供版式—区域兼容表
- **Role C 视觉重构术语**：视觉基线、有效渲染方案、严格复刻模式、自适应重构模式与重构审计；Role C 不回写页面语义合同
- **术语字典**：`core/terminology_dictionary.md`；统一页面区域、字段边界、阶段术语、视觉组件、枚举边界和历史兼容名，作为角色 A 的术语单一真相源
- **图表语义映射资产**：`chart_semantic_mapping`；`trend_curve` 必填，高语义风险图表建议输出，用于说明主图如何证明 `chart_proof_goal`
- **防机械套版资产**：`core/field_differentiation_rules.md`、`eval/template_stamp_detection.md`；检测字段重复、字面复述、骨架填词、缺少逐页设计决策、连续清单/卡片矩阵导致的清单印章、暗色/渐变/发布会风导致的视觉漂移印章，以及内部版式术语进入页面可见文案的问题
- **视觉冲突优先级资产**：`templates/visual_rules.md`、`prompts/generate_page_design.md`、`eval/acceptance_checklist.md`、`eval/template_stamp_detection.md`；当页面级设计与华为全局视觉门禁冲突时，按“全局视觉门禁 > page_design 局部风格词 > 生成模型审美补全”主动降级页面设计
- **chart_data 字段可见性资产**：`core/deck_spec_field_dictionary.md`、`core/output_contracts.md`、`prompts/deck_spec_generation.md`；约束 logic-only 字段不上屏、`edges.label` 短语化、复杂关系语义归 `chart_semantic_mapping`
- **视觉规则重构资产**：`templates/visual_rules.md` 专职视觉指导边界、负面视觉风格总表、视觉优化优先级、默认推荐样式、`visual_boundary` / `page_type_gate` 页面设计字段
- **前沿雷达日报精读资产**：`domain_profiles/frontier_radar_daily_deep_read.md`、`methodology_patterns/frontier_radar_daily_deep_read_patterns.md`；用于前沿雷达日报、技术信号精读、论文信号洞察类 PPT 的固定 10 页结构和 Catalyst/Application 成对规则
- **典型主题**：技术方案、战略规划、竞品对比、项目复盘、客户方案、资源申请、运营治理、产品路线图、调研分析、前沿雷达日报精读、技术信号精读、论文信号洞察

## 推荐调取方式

- 想看某个 Skill 的入口规则：先读对应 `SKILL.md`
- 想快速定位某个 Skill 的常用文件：优先看该 Skill 的 `QUICK_INDEX.md`
- 想看主题路由和术语边界：优先看 `REFERENCE_ROUTING_TABLE.md`
- 想看 `deck_spec.json` 字段含义：读 `core/deck_spec_field_dictionary.md`
- 想看术语统一口径：读 `core/terminology_dictionary.md`

## 当前状态

- 当前版本：`v0.5.1-visual-recomposition-terms`
- 当前工作区已建总索引：`skills/INDEX.md`
- 当前已收录 Skill：`huawei_ppt_master`
- 后续新增 Skill 时，补充到本页即可

## 文件目录结构

## 关键目录作用


## 文件职责

