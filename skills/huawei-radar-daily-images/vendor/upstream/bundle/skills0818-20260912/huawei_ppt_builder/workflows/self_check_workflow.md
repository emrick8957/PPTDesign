# 自检工作流

## 输入

- 原始 6 文件；
- C2 初版页面图片；
- C2.5 精修页面图片；
- contact sheet 总览图；
- 如有：上一轮自检报告。

## 流程

1. 逐页读取 `deck_spec` 和 `page_design`；
2. 对比 C2 与 C2.5，确认只发生视觉精修；
3. 检查主图是否证明 `chart_proof_goal`；
4. 检查字段可见性；
5. 检查 `correspondence_pairs` 与 `edge_roles`；
6. 检查华为视觉风格和负面禁止风格；
7. 基于 contact sheet 检查连续多页是否重复使用同一视觉骨架；
8. 检查底部红线与右侧红线是否共同形成 L 型包围感；
9. 检查高密度页面的 OCR 可见字符数、证据单元数、主体占用率、图表结构复杂度和右侧空壳；
10. 检查 `required_evidence` coverage；
11. 检查一票失败项；
12. 按 100 分制打分；
13. 对 `<92` 分页面输出返工优先级；
14. 触发 coverage 缺失、underfill、L 型红线或重复骨架时，写入 `return_to_A_required` 或进入 C4 返工。

## 输出

逐页输出：

- 总分；
- 等级；
- C2.5 是否完成；
- 语义合同判断；
- 字段可见性；
- 关系角色；
- 红色锚点；
- 卡片层级；
- 底部结论；
- L 型红线包围感；
- contact sheet 跨页重复骨架；
- 高密度 underfill；
- density_profile；
- OCR 可见字符数；
- 证据单元数；
- 主体占用率；
- 图表结构复杂度；
- 右侧空壳；
- required_evidence coverage；
- return_to_A_required；
- return_to_A_reason；
- 页脚与安全区；
- 一票失败项；
- 主要问题；
- 修改建议；
- 是否需要返工；
- 返工优先级。
