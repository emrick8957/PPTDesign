# C1 内部渲染合同编译提示词

你是角色 C。现在将 deck_spec/page_design 编译成内部 page_render_contract。该合同只服务施工，不得新增事实，不得替代 deck_spec。

## 编译原则

逐页生成 baseline `page_render_contract`。它是施工编译结果，不是新的事实源。编译器必须合并 `deck_spec.json`、`page_design.md` 和 `global_design_defaults`，保留 A 的页面级设计意图。必须包含：

- 页面 ID、标题、结论、章节；
- `layout_pattern`、`chart_contract_source` 与归一化后的 `chart_components`；
- 从唯一 `primary` 机器派生的 `chart_type`、`chart_proof_goal` 和主图语义投影，不回写 `deck_spec.json`；
- type 与来源：优先读取角色 A 的 `type`，历史输入包中的 `page_type` 仅作兼容映射，缺失时按主图表组件的 `chart_type` 保守推断；
- 可见文字计划；
- `chart_visual_boundary`、`forbidden_visualization`；
- `correspondence_pairs`、`edge_roles`；
- 红色锚点、右侧洞察栏、页脚和失败条件。
- `visual_notes`、`visual_focus`、`must_highlight`、`need_compression`、`data_gaps`；
- 页面设计中的区域划分、强调元素、角色 C 注意事项和视觉降噪约束。
- `density_budget`、逐组件 `component_coverage` 与结构化可见内容 coverage。
- `recomposition_mode`、`source_visual_plan`、初始 `effective_visual_plan` 和 `recomposition_audit`。

1. deck_spec 是事实源；
2. page_design 是版式施工说明；
3. `chart_components` 是新合同唯一事实源；历史顶层字段只在无 `chart_components` 时归一化为单一主组件；
4. 每个组件的 chart_semantic_mapping 是该组件复杂图表语义最高约束；
5. 每个组件的 chart_visual_boundary 与 forbidden_visualization 是硬边界；
6. logic-only 字段不得进入 visible_text；
7. layout_pattern、component_region 与 chart_type 必须分工明确。
8. 顶层主图投影由唯一 `primary` 机器派生，只用于施工，不回写角色 A 的输入。
9. 编译 `source_visual_plan`，并将其深复制为初始 `effective_visual_plan`；不得形成两个事实源。
10. 默认 `recomposition_mode=adaptive_recomposition`；用户明确锁定原版式时使用 `strict_fidelity`。


## 每页输出字段

```json
{
  "page_id": "P01",
  "recomposition_mode": "adaptive_recomposition",
  "source_contract": {
    "title": "",
    "conclusion": "",
    "section": "",
    "core_judgement": "logic_only",
    "chart_proof_goal": "logic_only"
  },
  "source_design": {
    "global_design_defaults": {},
    "page_design_global_defaults": [],
    "page_design_override": [],
    "page_design_sections": {}
  },
  "source_visual_plan": {
    "layout_pattern": "",
    "chart_components": [],
    "visible_title": "",
    "visible_conclusion": ""
  },
  "effective_visual_plan": {
    "layout_pattern": "",
    "chart_components": [],
    "visible_title": "",
    "visible_conclusion": ""
  },
  "recomposition_audit": {
    "trigger_reasons": [],
    "layout_changed": false,
    "chart_type_changed": false,
    "component_region_changed": false,
    "copy_adjustments": [],
    "semantic_invariants": {},
    "evidence_coverage": {},
    "compatibility_checks": {},
    "quality_delta": {},
    "return_to_A_required": false
  },
  "render_intent": {
    "layout_pattern": "",
    "chart_type": "",
    "chart_contract_source": "chart_components",
    "chart_components": [
      {
        "component_id": "C1",
        "component_role": "primary",
        "component_region": "main",
        "supports_component_id": null,
        "chart_type": "",
        "chart_proof_goal": "logic_only",
        "chart_data": {},
        "visible_labels": [],
        "semantic_constraints": {},
        "component_coverage": {}
      }
    ],
    "type": "",
    "type_source": "",
    "main_visual_goal": "",
    "visual_notes": "",
    "visual_focus": [],
    "must_highlight": [],
    "text_density": "",
    "need_compression": false,
    "data_gaps": []
  },
  "visible_text_plan": {
    "title": "",
    "subtitle": "",
    "main_labels": [],
    "node_labels": [],
    "short_edge_labels": [],
    "insight_panel": [],
    "bottom_conclusion": ""
  },
  "semantic_constraints": {
    "main_visual_logic": "",
    "stage_or_node_meaning": [],
    "forbidden_visualization": [],
    "correspondence_pairs": [],
    "edge_roles": {}
  },
  "visual_constraints": {
    "red_anchor": "",
    "card_hierarchy": "",
    "spacing_rule": "",
    "bottom_bar_rule": "",
    "visual_simplification": "",
    "visual_boundary": "",
    "page_type_gate": "",
    "right_insight_width": "inherit visual_rules.md or page-level override; use fallback only when absent",
    "footer": "weak, stable",
    "safe_area": "left/right >= 4%"
  },
  "fail_conditions": []
}
```

## 禁止

- 禁止把该合同中的字段名渲染到页面；
- 禁止为满足版式增加事实；
- 禁止将 edge_roles 或 correspondence_pairs 文本化上屏；
- 禁止把 page_goal/core_judgement/chart_proof_goal 字面显示。
- 禁止把 supporting 组件放入右侧洞察栏；洞察栏只能解释主图。
- 禁止让渲染合同主图投影与唯一 `primary` 组件不一致。
- 禁止修改 `source_visual_plan`；C1.5 只能修改 effective 并留痕。
