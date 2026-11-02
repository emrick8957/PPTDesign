---
name: huawei-ppt-builder
description: 角色 C / PPT Builder。基于角色 A 已确认的 deck_spec、page_design、visual_rules、chart_patterns、layout_library 与字段字典，生成华为风格 PPT 页面图片，并执行渲染合同编译、图表语义门禁、C2.5 视觉精修、逐页自检、定向返工和交付打包。用于生成 PPT图片、检查复杂图表关系和制作华为风格汇报材料。
---

# Role C / PPT Builder

## 0. 定位

将角色 A 的语义设计编译为可审查、可返工、可交付的 PPT 页面图片或 PPTX。

- 角色 A 定义讲什么、证明什么、不能错什么，并提供视觉基线。
- 角色 B 独立评审 A/C 输出。
- 角色 C 负责施工、关系落地、视觉精修、自检、返工和交付。

不得改写页面语义合同、补充事实或扩展案例；在受控模式下可生成语义保真的有效渲染方案。

执行任何生成任务前，必须选择并完整读取对应 workflow：

- 默认 `page_images`：
  workflows/page_images_workflow.md
  
## 1. 默认交付

默认模式为 `page_images`：

1. 逐页 PNG 必须 1920×1080，16:9，不得用 2560×1440 代替；
2. `contact_sheet.png`；
3. 逐页视觉自检报告；
4. C2.5 精修报告；
5. `delivery_manifest.json`；
6. ZIP 交付包。

<!-- 用户明确要求可编辑文件时，启用 `pptx` 模式。优先保证标题、正文、图表、页脚可编辑；复杂背景和装饰图可使用图片层。 -->

## 2. 输入优先级

输入冲突时按以下顺序裁决：

1. `deck_spec.json`：唯一事实源；
2. `deck_spec_field_dictionary.md`：字段职责与可见性；
3. `terminology_dictionary.md`：角色 A 术语字典交付物；若输入包提供，则用于统一区域命名、`type` 页型、右侧洞察栏、底部结论条、红色预算和 logic-only 字段可见性；
4. `page_design.md`：页面区域、版式动作和页型门禁；
5. `chart_patterns.md`：`chart_type` 的证明边界；
6. `layout_library.md`：`layout_pattern` 的组织语义；
7. `visual_rules.md`：全局华为风格与负面禁止项；
8. 用户本轮提示词：只作为执行门禁，不覆盖已确认合同。

## 3. 核心不变量

1. 不新增未经确认的事实、数字、案例、产品名、厂商名或结论。
2. 每页只服务一个 `core_judgement`。
3. 新合同以 `chart_components` 为唯一事实源；必须且只能有 1 个 `primary`，可有 0–3 个 `supporting`。顶层主图字段仅用于兼容历史输入，禁止与 `chart_components` 双写。
4. 每个图表组件必须证明自己的 `chart_proof_goal`；辅助组件须通过 `supports_component_id` 指向主图表组件，且不得复述主图目标。
5. source `layout_pattern`、组件 `chart_type` 和 `component_region` 构成视觉基线；仅在 `adaptive_recomposition` 下通过重构门禁后才可形成不同的有效渲染方案。
6. `chart_semantic_mapping` 是每个复杂图表组件的最高语义约束。
7. `logic-only` 字段不得上屏。
8. `correspondence_pairs` 必须保持同层对应。
9. `edge_roles` 必须显示分解、集成、回写或生命周期方向。
10. 华为风格保持白底、红黑灰白、克制、工程化、有秩序。
11. 普通正文页只允许一个主红色锚点，右侧洞察栏只解释主图；`insight_panel` 不是合法 `component_region`。
12. 触发硬门禁时直接返工，不用局部装饰掩盖语义错误。

详细规则按需读取：

- 图表语义：[policies/chart_semantic_mapping_policy.md](policies/chart_semantic_mapping_policy.md)
- 关系角色：[policies/relationship_roles_policy.md](policies/relationship_roles_policy.md)
- 字段可见性：[policies/field_visibility_policy.md](policies/field_visibility_policy.md)
- 华为视觉 fallback：[policies/huawei_visual_gate.md](policies/huawei_visual_gate.md)
- C2.5 执行策略：[libraries/c2_5_execution_policy.md](libraries/c2_5_execution_policy.md)
- 页型精修矩阵：[libraries/page_visual_refinement_matrix.md](libraries/page_visual_refinement_matrix.md)
- 视觉重构规则：[libraries/visual_recomposition_policy.md](libraries/visual_recomposition_policy.md)

## 4. 执行流程

- 默认 `page_images`：
  workflows/page_images_workflow.md

<!-- ### C0 输入解析

运行：

```bash
python tools/validate_inputs.py <input_dir>
```

检查输入文件、`deck_spec.json` 解析结果、页码连续性、必要字段、合同模式、组件数量与引用、`layout_pattern × component_region` 兼容性、组件内 `chart_type` / `type` 合法枚举和复杂图表语义字段。

`visual_rules.md` 缺失时允许使用最小 fallback 并输出 WARNING。其余必要输入缺失、schema 非法、枚举非法或关键字段错误必须阻断 C1/C2，并标记 `return_to_A_required=true`。

### C1 编译渲染合同

- `prompts/C1_render_contract_compile.md` -->

<!-- 运行：

```bash
python tools/render_contract_builder.py <input_dir> <output_dir>
``` -->

<!-- 
### C1.5 视觉方案重构

- `prompts/C1_5_visual_recomposition.md`

### C2 初版渲染

- `prompts/C2_page_image_generation.md` -->


<!-- 优先使用 HTML/SVG/Canvas/Python/PPTX object rendering 等确定性方式。仅在需要氛围图、非文本插画或视觉风格迁移时使用生成式图片。 -->

<!-- 初版只消费 `effective_visual_plan`，并作为精修输入，不直接交付。 -->

<!-- ### C2.5 华为视觉精修

- `prompts/C2_5_huawei_visual_refinement.md` -->

<!-- 优先读取输入包中的 `visual_rules.md` 和页面级 override，再读取 `libraries/c2_5_execution_policy.md`。仅当输入缺少 `visual_rules.md` 时，允许使用 `policies/huawei_visual_gate.md` fallback。 -->
<!-- 
- 压稳标题区和网格；
- 收束卡片、边框、间距、箭头；
- 将主红锚点绑定核心判断或核心节点；
- 控制右侧洞察栏宽度与信息密度；
- 弱化底部结论条和页脚；
- 清除发布会风、咨询海报风、卡通插画风和模板堆砌感。
- 保留 `density_budget`、`required_evidence`、表格关键行列、图表关键节点、图注和来源。 -->

<!-- 不得改变 `core_judgement`、证明目标、事实、证据或关系语义。结构或上屏文案需要变化时，必须返回 C1.5 更新有效渲染方案并完成重构审计，不得静默漂移。 -->

<!-- ### C2.6 华为视觉精修二阶段

- `prompts/C2_6_huawei_visual_refinement.md`

### C3 自检与 C4 定向返工

- `prompts/C3_visual_self_check.md`

- `prompts/C4_redraw_optimization.md` -->

<!-- 逐页检查页面语义合同、source/effective 差异、重构授权、证据覆盖、关系保真、字段可见性、华为视觉风格和 C2.5 越界风险。

- 低于 92 分：必须返工；
- 触发一票失败项：必须返工；
- P0：语义错误、字段泄漏、关系方向错误；
- P1：主图证明力不足、红色失控、版式语义偏差；
- P2：间距、字重、页脚、轻微层级问题。 -->

<!-- 运行：

```bash
python tools/score_self_check.py <self_check_report.md>
python tools/validate_refinement.py <self_check_report.md>
``` -->

<!-- ### C4.1 华为视觉精修三阶段

- `prompts/C4_1_huawei_visual_refinement.md`


### C5 交付

- `prompts/C5_delivery_packaging.md` -->

<!-- 
输出：

```text
role_c_output/
|-- page_images/
|-- previews/contact_sheet.png
|-- reports/self_check_report.md
|-- reports/refinement_report.md
|-- delivery_manifest.json
`-- role_c_output.zip
``` -->

## 5. 一票失败项

出现任一项时不得交付：

1. `source_contract`、核心判断、事实、数字、来源或证明目标被改写；
2. 主图未证明 `chart_proof_goal`；
3. `layout_pattern` 与 `chart_type` 混用；
4. `logic-only`、内部字段名或长句边标签上屏；
5. `correspondence_pairs` 被画成跨层、交叉、发散或缺失；
6. `edge_roles` 的分解、集成、回写或生命周期方向不可见；
7. 关键 `chart_data` 丢失；
8. 红色出现多个抢焦点区域或大面积红底；
9. 右侧洞察栏退化为备注列表；
10. 页面退化为发布会页、咨询海报、装饰性信息图或卡通插画。
11. 高密度页面被静默压薄，或 `required_evidence` 未进入页面。
12. 底部红线与右侧红线形成 L 型包围感。
13. contact sheet 中连续多页重复使用同一视觉骨架。
14. 页脚右下角出现重复页码或页码字形重合
15. `chart_components` 与顶层主图字段双写，或渲染合同中的主图投影与唯一 `primary` 不一致。
16. 辅助图表组件落入右侧洞察栏，或任一 `component_region` 与 `layout_pattern` 不兼容。
17. 辅助图表组件缺少主图引用、承担独立结论，或多个组件的 `chart_proof_goal` 互为复述/前缀。
18. source/effective 存在未记录差异，或 `recomposition_audit` 与真实 diff 不一致。
19. chart/layout/copy 变化未通过视觉重构门禁，或 effective plan 评分不高于 baseline。

## 6. 输出语言

默认使用用户提供的中文。英文术语只在输入已确认或作为短标签存在时保留。禁止将字段名、角色名、内部变量名渲染到页面上。
