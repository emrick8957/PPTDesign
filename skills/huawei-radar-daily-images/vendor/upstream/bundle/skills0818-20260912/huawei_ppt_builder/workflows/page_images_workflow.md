# Page Images Workflow

## 目标

基于角色 A 已确认交付物，生成可直接放入 PPT 的逐页高清图片。初版不得直接交付，必须经过 `C2.5` `C2.6` `C3` `C4` `C4.1` `C5`。

## C0 输入解析

运行：

```bash
python tools/validate_inputs.py <input_dir>
```

必要输入：

- `deck_spec.json`
- `page_design.md`
- `chart_patterns.md`
- `layout_library.md`
- `deck_spec_field_dictionary.md`

规范输入：

- `visual_rules.md`

缺少 `visual_rules.md` 时允许使用最小 fallback 并输出 WARNING。缺少其余必要输入、schema 非法、枚举非法或关键字段错误时，必须停止生成并写入 `return_to_A_required=true`。新合同必须校验 `chart_components` 单源模式、组件数量/引用、逐组件语义以及 `layout_pattern × component_region` 兼容性；历史顶层合同仅作兼容读取。

视觉参考：
- `templates/Golden_Style.zip`
必须读取Golden_Style作为视觉参考

## C1 渲染合同编译

- `prompts/C1_render_contract_compile.md`

<!-- 
运行：

```bash
python tools/render_contract_builder.py <input_dir> <output_dir>
```

渲染合同必须合并 `deck_spec.json`、`page_design.md` 和 `global_design_defaults`，继承标题、结论、证明目标、可见文字、关系角色、禁止表达、红色锚点、页面级设计 overrides 和失败条件。它是施工编译结果，不是新的事实源。

渲染合同必须输出 `chart_contract_source`、归一化组件列表、逐组件 `component_coverage`、结构化可见内容 coverage 和 `density_budget`。主图顶层投影只能从唯一 `primary` 派生。coverage 不完整时阻断 C2，不得静默丢失表格、卡片、路线图、风险或决策内容。

页型映射顺序：角色 A 的 `type` → 历史 `page_type` → 主图表组件 `chart_type` 保守推断。合同必须记录 `type_source`，新合同统一输出 `type`。 -->

## C1.5 视觉方案重构

- `prompts/C1_5_visual_recomposition.md`

<!-- 默认采用 `adaptive_recomposition`；用户明确要求原版式不变、忠实复刻或只做样式微调时采用 `strict_fidelity`。

- baseline 永远保留；
- 每页最多生成 2 个候选；
- layout/chart/region/copy 变化必须进入 `effective_visual_plan` 和 `recomposition_audit`；
- 执行 `python tools/validate_recomposition.py <contract_or_dir>`；
- 校验失败或 `return_to_A_required=true` 时阻断 C2。
- 读取 `/examples/regression/frontier_radar_daily/fixtures/frontier_radar_daily_Golden_Style.zip` 作为版式与视觉语言参考，但不得复制文字和事实。 -->

## C2 初版页面图片生成

- `prompts/C2_page_image_generation.md`


<!-- 优先使用确定性渲染方式，只消费 `effective_visual_plan`，保证中文文字、页码、箭头、对应关系和层级准确。 -->

<!-- - 页面为 16:9，必须 1920×1080；
- 白底为主，红黑灰白；
- 每页只服务一个核心判断；
- 主图表组件必须服务自己的 `chart_proof_goal`，辅助组件必须提供不同证据并支撑主图；
- `logic-only` 字段不得上屏；
- 页脚统一弱化。
- 读取 `\examples\regression\frontier_radar_daily\fixtures\frontier_radar_daily_Golden_Style.zip` 作为版式与视觉语言参考，但不得复制文字和事实。 -->

<!-- 初版只作为 `C2.5` 输入。 -->

## C2.5 华为视觉精修

- `prompts/C2_5_huawei_visual_refinement.md`

<!-- 读取：

- 输入包 `visual_rules.md`；
- 已通过校验的 `effective_visual_plan`；
- 输入包 `page_design.md` 与 `deck_spec.json` 页面级 override；
- `libraries/c2_5_execution_policy.md`
- `libraries/page_visual_refinement_matrix.md`
- `prompts/C2_5_huawei_visual_refinement.md`
- 仅当输入缺少 `visual_rules.md` 时读取 `policies/huawei_visual_gate.md` fallback。
- 读取 `\examples\regression\frontier_radar_daily\fixtures\frontier_radar_daily_Golden_Style.zip` 作为版式与视觉语言参考，但不得复制文字和事实。

执行：

- 压稳标题区；
- 统一卡片、边框、内边距和箭头；
- 收束红色锚点；
- 强化主图证明路径；
- 控制右侧洞察栏宽度；
- 弱化底部结论条与页脚；
- 删除装饰性冗余。
- 保留高密度合同和所有必需证据。
- 读取 `\examples\regression\frontier_radar_daily\fixtures\frontier_radar_daily_Golden_Style.zip` 作为版式与视觉语言参考，但不得复制文字和事实。

禁止：

- 改写 `source_contract`、事实、数字、来源、证明目标或关系语义；
- 绕过 C1.5 静默改变 layout、region、chart type 或上屏文案；
- 把辅助组件移入右侧洞察栏，或把洞察栏画成第二图表区；
- 将关系图改成海报式概念图；
- 新增渐变、重阴影、大面积红底或图标群。
- 将 `technical_deep_dive` 降级为中等密度页面。
- 静默删除 `required_evidence`、表格关键行列、图表关键节点、图注或来源。 -->

## C2.6 华为视觉精修二阶段

- `prompts/C2_6_huawei_visual_refinement.md`
- 读取 `templates/Golden_Style.zip` 作为版式与视觉语言参考，但不得复制文字和事实。

<!-- 
读取：

- `prompts/C2_6_huawei_visual_refinement.md`
- 读取 `\examples\regression\frontier_radar_daily\fixtures\frontier_radar_daily_Golden_Style.zip` 作为版式与视觉语言参考，但不得复制文字和事实。 -->

## C3 自检与 C4 定向返工

- 读取 `templates/Golden_Style.zip` 作为版式与视觉语言参考，但不得复制文字和事实。

- `prompts/C3_visual_self_check.md`

- `prompts/C4_redraw_optimization.md`

<!-- 逐页检查内容、版式、图表语义、字段可见性、关系角色、华为视觉风格和精修越界。

同时检查 source/effective 真实差异、重构授权、证据覆盖、关系保真和质量增量。

- 分数 `<92`：返工；
- 触发一票失败项：返工；
- 语义错误优先于视觉美化；
- 关系错误优先于布局微调；
- 字段泄漏必须清零。
- 高密度 underfill、L 型红线和连续多页重复骨架必须清零。 -->

## C4.1 华为视觉精修三阶段

- `prompts/C4_1_huawei_visual_refinement.md`

<!-- 
读取：

- `prompts/C4_1_huawei_visual_refinement.md` -->

## C5 交付

- `prompts/C5_delivery_packaging.md`

<!-- 
```text
role_c_output/
|-- page_images/
|-- previews/contact_sheet.png
|-- reports/self_check_report.md
|-- reports/refinement_report.md
|-- delivery_manifest.json
`-- role_c_output.zip
``` -->
