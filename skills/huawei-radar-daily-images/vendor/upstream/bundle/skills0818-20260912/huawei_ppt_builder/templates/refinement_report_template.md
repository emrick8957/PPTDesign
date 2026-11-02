# Role C 视觉精修报告

## 任务信息

- 任务模式：page_images
- 精修阶段：C2.5 Huawei Visual Refinement Pass
- 输入边界：deck_spec + page_design
- 精修原则：不改页面语义合同；按已校验的有效渲染方案施工，所有 source/effective 差异可审计

## 全局精修动作

- [ ] 统一标题区高度与标题层级
- [ ] 统一页脚样式与弱化程度
- [ ] 统一卡片圆角、边框、内边距
- [ ] 统一箭头、线条、灰度
- [ ] 控制单页红色锚点数量
- [ ] 优化右侧洞察栏宽度与信息密度
- [ ] 优化底部结论条样式
- [ ] 提升图表证明路径清晰度

## 逐页精修记录

### P01

- source_layout_pattern：
- effective_layout_pattern：
- chart_transform_summary：
- component_region_diff：
- copy_adjustments：
- semantic_invariants：PASS / FAIL
- evidence_coverage：
- relation_preservation：PASS / FAIL
- recomposition_authorized：PASS / FAIL
- unrecorded_diff：无 / 有
- 保持不变：source_contract / chart_proof_goal / chart_data / required_evidence / relations / 页脚来源
- 精修动作：
- 越界检查：通过 / 不通过
- 需要返工：是 / 否

### P02

- source_layout_pattern：
- effective_layout_pattern：
- chart_transform_summary：
- copy_adjustments：
- semantic_invariants：PASS / FAIL
- evidence_coverage：
- relation_preservation：PASS / FAIL
- recomposition_authorized：PASS / FAIL
- unrecorded_diff：无 / 有
- 保持不变：source_contract / chart_proof_goal / chart_data / required_evidence / relations / 页脚来源
- 精修动作：
- 越界检查：通过 / 不通过
- 需要返工：是 / 否

### P03

- source_layout_pattern：
- effective_layout_pattern：
- chart_transform_summary：
- copy_adjustments：
- semantic_invariants：PASS / FAIL
- evidence_coverage：
- relation_preservation：PASS / FAIL
- recomposition_authorized：PASS / FAIL
- unrecorded_diff：无 / 有
- 保持不变：source_contract / chart_proof_goal / chart_data / required_evidence / relations / 页脚来源
- 精修动作：
- 越界检查：通过 / 不通过
- 需要返工：是 / 否

## C2.5 精修结论

- 页面语义合同是否保持：是 / 否
- effective plan 是否通过重构校验：是 / 否
- 是否存在新增事实：是 / 否
- 是否存在字段越界：是 / 否
- 是否更贴近华为 PPT 风格：是 / 否
- 是否进入 C3 自检：是 / 否
