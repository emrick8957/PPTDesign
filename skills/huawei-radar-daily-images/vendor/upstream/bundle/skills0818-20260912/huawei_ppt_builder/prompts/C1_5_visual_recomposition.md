# C1.5 视觉方案重构 Prompt

你是角色 C。读取 C1 生成的 baseline `page_render_contract`，为每页判断是否需要语义保真视觉重构。

## 规则源

必须读取：

- `libraries/visual_recomposition_policy.md`；
- `layout_library.md`；
- `chart_patterns.md`；
- `page_design.md`；
- 当前页 baseline render contract。

## 执行顺序


默认使用 `adaptive_recomposition`；用户明确要求原版式不变、忠实复刻或只做样式微调时使用 `strict_fidelity`。

- 保留 `source_contract` 和 `source_visual_plan`；
- 每页最多生成 2 个候选；
- layout/chart/region/copy 差异必须通过 `libraries/visual_recomposition_policy.md`；
<!-- - 运行 `python tools/validate_recomposition.py <contract_or_dir>`； -->
- FAIL 或 `return_to_A_required=true` 时不得进入 C2。


1. 保留 `source_contract` 和 `source_visual_plan`，不得修改；
2. 判断模式：用户明确锁定原版式时使用 `strict_fidelity`，否则使用 `adaptive_recomposition`；
3. 检查主图证明、信息路径、卡片同权、表格过重、空壳右栏、underfill、overcrowding 和跨页重复骨架；
4. 无结构问题时保留 baseline；
5. 有结构问题时最多生成 2 个候选；
6. 对每个候选校验语义不变量、证据覆盖、版式区域和图表转换；
7. 只有候选明确优于 baseline 才写入 `effective_visual_plan`；
8. 完整填写 `recomposition_audit`；
<!-- 9. 运行 `tools/validate_recomposition.py`，FAIL 时不得进入 C2。 -->

## 禁止

- 不得修改 `core_judgement`、`chart_proof_goal`、事实、数字、来源、required evidence 或关系语义；
- 不得回写 `deck_spec.json`；
- 不得为适配新图表新增轴、阶段、节点、边或时间顺序；
- 不得未留痕地修改标题、结论、layout、region 或 chart type；
- 不得为了避免重复骨架而选择更差的候选。
- 禁止大留白低密度,禁止用巨大留白冒充高级感
- 禁止底部结论弱化成脚注
- 禁止右栏堆 bullet

## 输出

输出更新后的 render contract；`render_intent` 必须由 `effective_visual_plan` 派生，不能成为第三事实源。
- C1_5_visual_recomposition_report.md
