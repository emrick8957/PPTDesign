# 固定版本与兼容裁决

本入口使用用户提供的 skills0818.zip 原始内容，不以同名工作区文件替换。Master版本v0.5.1-visual-recomposition-terms；Builder版本1.6.0-adaptive-recomposition。包名日期与内部版本日期属于不同来源，不据文件名改写内部版本号。source/skills0818.zip保留原包，bundle.lock.json绑定全部固定文件的SHA-256。

以下引用已确认在包内缺失。本入口将它们标为历史/辅助索引的废弃引用，使用包内真实存在的现行规则覆盖对应职责；不从huawei_ppt_builder_html复制不同版本文件，也不伪造这些文件曾存在。

| Builder中的缺失引用 | 当前使用的规则（相对Builder） |
|---|---|
| libraries/huawei_visual_refinement_rules.md | libraries/c2_5_execution_policy.md；libraries/page_visual_refinement_matrix.md；libraries/visual_recomposition_policy.md |
| policies/content_boundary_policy.md | SKILL.md的核心不变量与一票失败项；policies/field_visibility_policy.md；Master的core/output_contracts.md |
| policies/artifact_boundary_policy.md | SKILL.md默认交付；workflows/page_images_workflow.md；本入口固定PNG、不生成PPTX |
| libraries/page_type_gate_library.md | libraries/page_visual_refinement_matrix.md；Master的templates/page_types.md和日报主题包 |
| examples/regression/frontier_radar_daily/fixtures/frontier_radar_daily_Golden_Style.zip | templates/Golden_Style.zip及本包提取的golden_reference/Golden_Style/style1 |

现行SKILL入口直接引用的执行依赖全部保留。新增其他缺失文件不能类推豁免；先检查实际依赖，缺失会影响正确性时停止对应阶段并说明。

## 已知规则冲突

- 本轮用户要求优先：正文无底部结论条，禁止指定转折句式；忽略历史样张/Builder旧wording中相反示例。Master文案、视觉和本主题包共同约束画面。
- 主题固定十页，但真实信号可只有1–2条，不虚构补齐；P2的优先级只用于信号关注，不提前写P10行动方案。
- 图片任务使用page_images_workflow现行阶段入口。C2.6按该工作流与提示词执行整页imagegen重绘；README将其列为条件阶段的旧概述不覆盖本入口默认链路。
- C4定向修图使用imagegen，保留语义。C4.1做跨页诊断，避免无意义重绘文字；必要修图返回对应阶段并留痕。
- 交付阈值按每页至少92且无硬失败项；评分是目视自检，不是独立质量认证。不能先给分再用工具输出反证图片正确。
- 分辨率是交付规格：保留工具原图，必要时仅做尺寸归一，并在manifest披露原始尺寸。公共区域需一致，生成式图片的少量浮动不得表述为精确坐标完全一致。
- 材料已完整且用户调用本流程时，不执行通用ppt-master的额外确认管线。用户明确只读时，不开始生成。
