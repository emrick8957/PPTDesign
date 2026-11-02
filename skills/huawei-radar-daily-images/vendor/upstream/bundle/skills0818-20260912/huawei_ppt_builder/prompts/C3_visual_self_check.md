# C3 逐页视觉自检 Prompt

对照 `deck_spec`、`page_design`、`visual_rules`、渲染合同、C2 初版、C2.5 精修图和 contact sheet 总览图检查。

## 输入

- `libraries/post_generation_scoring_rubric.md`
- `deck_spec`、
- `page_design`
- `visual_rules`
- 渲染合同
- C2 初版
- C2.5 精修图
- C2.6 重构图
- contact sheet 

# 执行规则：

按 `libraries/post_generation_scoring_rubric.md` 严格执行评分。低于 92 分或触发任一一票失败项时，标记为必须返工。

1. 一票失败项判定；
2. 页面类型识别：封面 / 摘要 / 正文 / 路线图 / 对比表 / 架构图 / 结论页；
3. underfill 与 contact sheet 缩略图判定；
4. 得分上限触发判定；
5. 六项分项评分；
6. 应用上限裁剪；
7. deck 级扣分；
8. 输出返工路由：PASS / C2.5 refine / C2.6 recomposition / C4_redraw / return_to_A。

# 必须检查：

1. `source_contract`、核心判断、事实、数字、来源和证明目标是否保持；
2. 主图表组件是否证明自己的 `chart_proof_goal`，辅助组件是否分别提供不同且必要的证据；
3. `layout_pattern`、`component_region` 与组件内 `chart_type` 是否混用或不兼容；
4. `logic-only` 或内部字段名是否上屏；
5. `correspondence_pairs` 是否保持同层对应；
6. `edge_roles` 是否显示正确方向；
7. 红色是否只有一个主锚点；
8. 右侧洞察栏是否只解释主图；
9. 底部结论是否有增量；
10. 底部红线与右侧红线是否共同形成 L 型包围感；
11. contact sheet 中是否连续多页重复使用同一视觉骨架；
12. 是否出现发布会风、咨询海报风、卡通插画风或模板堆砌感；
13. 页面语义合同是否保持，source/effective 差异是否获得授权并完整留痕；
14. 高密度页面是否出现 underfill，是否保留 `required_evidence`、表格关键行列、图表关键节点、图注和来源；
15. OCR 可见字符数、证据单元数、主体占用率、图表结构复杂度是否符合 `density_budget`；
16. 右侧洞察栏是否出现空壳；
17. 是否需要写入 `return_to_A_required=true`。
18. 每页必须判断当前最大视觉问题
19. contact sheet 跨页 页脚区 风格不一致
20. 渲染合同的主图投影是否与唯一 `primary` 组件一致；
21. 是否有辅助组件进入右侧洞察栏，或洞察栏退化为第二图表区；
22. 每个 `supporting` 是否引用主图、保持次级视觉权重，且证明目标不与其他组件复述。
23. `recomposition_audit` 是否与真实 layout/chart/region/copy diff 一致；
24. required evidence coverage 是否为 100%，关系语义是否保持；
25. effective plan 是否解决 baseline 的明确问题且评分更高；
26. 是否存在未记录的图片/PPTX 与 effective plan 偏差。


# 输出

- C3_visual_self_check_report.md
报告必须包含：每页评分
    Pxx：
    内容匹配 /20
    版式结构 /15
    图表语义 /20
    字段关系 /15
    华为风格 /20
    C2.5完整度 /10
    总分：
    主要视觉缺口：
    是否触发得分上限：
    是否进入 C4_redraw：