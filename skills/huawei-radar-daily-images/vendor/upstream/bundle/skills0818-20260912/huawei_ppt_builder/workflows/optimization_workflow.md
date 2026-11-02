# 优化工作流

## 输入

- 上一轮页面图片；
- 自检报告；
- 精修报告；
- 原始输入文件。

## 修复顺序

1. 修复内容越界、字段泄漏和事实源偏移；
2. 修复 `chart_proof_goal`、`correspondence_pairs`、`edge_roles` 等语义错误；
3. 修复 `layout_pattern` 与 `chart_type` 混用；
4. 收束红色锚点、右侧洞察栏和卡片层级；
5. 调整间距、字重、页脚和安全区。

不得用局部美化掩盖语义错误。返工后重新执行 C2.5 和 C3。

## 输出

- `optimized_page_images/`
- `reports/refinement_report.md`
- `reports/after_optimization_self_check.md`
- ZIP 交付包
